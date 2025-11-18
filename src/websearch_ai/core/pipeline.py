"""
Main web search pipeline orchestration.
"""
import asyncio
import logging
from typing import List, Optional

import aiohttp

from ..config import Settings
from .models import SearchResult, BetterQueries
from ..managers import CacheManager, PromptManager, RobotsChecker
from ..clients import HTTPFetcher, LLMClient, SearchEngine
from ..filters import URLFilter

logger = logging.getLogger(__name__)


class WebSearchPipeline:
    """Main pipeline for web search and content aggregation."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.prompt_manager = PromptManager(settings.prompts_path)
        self.cache = CacheManager(settings.cache_dir) if settings.cache_enabled else None
        self.robots_checker = RobotsChecker()
        self.fetcher = HTTPFetcher(settings)
        self.search_engine = SearchEngine(settings)
        self.llm = LLMClient(settings)
        self.url_filter = URLFilter(settings.disallowed_domains)
    
    async def _generate_better_queries(self, query: str) -> List[str]:
        """Generate improved search queries using LLM."""
        prompt_template = self.prompt_manager.get_prompt("better_queries_prompt")
        prompt = self.prompt_manager.format_prompt(prompt_template, query=query)
        
        result = await self.llm.call_structured(
            prompt, 
            BetterQueries, 
            max_tokens=self.settings.llm_tokens_better_queries
        )
        
        if not result:
            logger.warning("Failed to generate better queries, using original")
            return [query]
        
        queries_list = result.queries  # type: ignore
        # Limit to configured number of queries
        queries_list = queries_list[:self.settings.search_num_better_queries]
        logger.info(f"Generated {len(queries_list)} better queries: {queries_list}")
        return queries_list
    
    async def _perform_searches(
        self, 
        queries: List[str]
    ) -> List[SearchResult]:
        """Perform searches for all queries and collect unique results."""
        all_results = []
        seen_urls = set()
        
        for query in queries:
            results = self.search_engine.search(query, self.settings.search_max_results_per_query)
            
            for r in results:
                url = r.get("url")
                if not url or url in seen_urls:
                    continue
                
                if not self.url_filter.is_allowed(url):
                    logger.debug(f"Filtered out disallowed URL: {url}")
                    continue
                
                seen_urls.add(url)
                all_results.append(SearchResult(
                    better_query=query,
                    title=r.get("title", ""),
                    url=url,
                    snippet=r.get("snippet", ""),
                    relevance=0,
                    complete_text=None,
                    summary=None
                ))
        
        logger.info(f"Collected {len(all_results)} unique URLs")
        return all_results
    
    async def _calculate_relevance(
        self, 
        result: SearchResult, 
        original_query: str
    ) -> SearchResult:
        """Calculate relevance score for a search result."""
        prompt_template = self.prompt_manager.get_prompt("relevance_filtering_prompt")
        prompt = self.prompt_manager.format_prompt(
            prompt_template,
            query=original_query,
            content=f"{result.title}\n{result.snippet}"
        )
        
        relevance_str = await self.llm.call_text(prompt, max_tokens=self.settings.llm_tokens_relevance_check)
        
        try:
            result.relevance = int(relevance_str)
        except ValueError:
            logger.warning(f"Invalid relevance score '{relevance_str}' for {result.url}")
            result.relevance = 0
        
        return result
    
    async def _filter_by_relevance(
        self, 
        results: List[SearchResult],
        original_query: str,
        min_relevance: Optional[int] = None
    ) -> List[SearchResult]:
        """Filter results by relevance score."""
        if min_relevance is None:
            min_relevance = self.settings.min_relevance_score
        
        tasks = [
            self._calculate_relevance(r, original_query) 
            for r in results
        ]
        results_with_relevance = await asyncio.gather(*tasks)
        
        filtered = [r for r in results_with_relevance if r.relevance >= min_relevance]
        filtered.sort(key=lambda x: x.relevance, reverse=True)
        
        logger.info(
            f"Filtered to {len(filtered)} relevant results "
            f"(from {len(results)}, threshold={min_relevance})"
        )
        return filtered
    
    async def _fetch_content(
        self, 
        results: List[SearchResult]
    ) -> List[Optional[str]]:
        """Fetch content for all URLs."""
        async with aiohttp.ClientSession(headers=self.fetcher.headers) as session:
            tasks = []
            for i, result in enumerate(results):
                proxy = None
                if self.settings.use_proxies and self.settings.proxies:
                    proxy = self.settings.proxies[i % len(self.settings.proxies)]
                
                tasks.append(self.fetcher.fetch_with_cache(
                    result.url,
                    session,
                    self.cache,
                    self.robots_checker,
                    proxy
                ))
            
            pages = await asyncio.gather(*tasks)
            successful = sum(1 for p in pages if p)
            logger.info(f"Fetched content from {successful}/{len(results)} URLs")
            return pages
    
    async def _summarize_content(
        self,
        result: SearchResult,
        content: Optional[str],
        original_query: str,
        max_chars: Optional[int] = None
    ) -> Optional[SearchResult]:
        """Summarize content from a URL."""
        if not content:
            return None
        
        if max_chars is None:
            max_chars = self.settings.max_content_chars
        
        # Truncate content
        truncated = content[:max_chars]
        if len(content) > max_chars:
            # Try to end at a sentence
            truncated = truncated.rsplit(".", 1)[0] + "."
        
        # Generate summary
        prompt_template = self.prompt_manager.get_prompt("summarize_text_prompt")
        prompt = self.prompt_manager.format_prompt(
            prompt_template,
            query=original_query,
            content=truncated
        )
        
        summary = await self.llm.call_text(prompt, max_tokens=self.settings.llm_tokens_summarize)
        
        return SearchResult(
            better_query=result.better_query,
            title=result.title,
            url=result.url,
            snippet=result.snippet,
            relevance=result.relevance,
            complete_text=f"{content[:200]}... + ({len(content)} chars)",
            summary=summary
        )
    
    async def _generate_summaries(
        self,
        results: List[SearchResult],
        contents: List[Optional[str]],
        original_query: str
    ) -> List[SearchResult]:
        """Generate summaries for all fetched content."""
        tasks = [
            self._summarize_content(result, content, original_query)
            for result, content in zip(results, contents)
        ]
        
        summaries = await asyncio.gather(*tasks)
        valid_summaries = [s for s in summaries if s is not None]
        
        logger.info(f"Generated {len(valid_summaries)} summaries")
        return valid_summaries
    
    async def _merge_summaries(
        self,
        summaries: List[SearchResult],
        original_query: str
    ) -> str:
        """Merge all summaries into a final answer."""
        if not summaries:
            return "No content available to generate answer."
        
        summaries_text_parts = [
            f"URL: {item.url}\nSummary: {item.summary}"
            for item in summaries
        ]
        summaries_text = "\n\n".join(summaries_text_parts)
        
        prompt_template = self.prompt_manager.get_prompt("merge_summaries_prompt")
        prompt = self.prompt_manager.format_prompt(
            prompt_template,
            query=original_query,
            summaries=summaries_text
        )
        
        logger.info("Merging summaries into final answer...")
        final_answer = await self.llm.call_text(prompt, max_tokens=self.settings.llm_tokens_merge)
        return final_answer
    
    async def run(self, query: str) -> tuple[List[SearchResult], str]:
        """
        Execute the complete web search pipeline.
        
        Args:
            query: The search query
            
        Returns:
            Tuple of (list of search results with summaries, final merged answer)
        """
        logger.info(f"Starting pipeline for query: {query}")
        
        # Step 1: Generate better queries
        better_queries = await self._generate_better_queries(query)
        
        # Step 2: Perform searches
        search_results = await self._perform_searches(better_queries)
        
        if not search_results:
            logger.error("No search results found")
            return [], "No search results found."
        
        # Step 3: Filter by relevance
        filtered_results = await self._filter_by_relevance(search_results, query)
        
        if not filtered_results:
            logger.error("No relevant results after filtering")
            return [], "No relevant results found."
        
        # Step 4: Fetch content
        contents = await self._fetch_content(filtered_results)
        
        # Step 5: Generate summaries
        summaries = await self._generate_summaries(
            filtered_results,
            contents,
            query
        )
        
        # Step 6: Merge summaries
        final_answer = await self._merge_summaries(summaries, query)
        
        logger.info("Pipeline completed successfully")
        return summaries, final_answer

