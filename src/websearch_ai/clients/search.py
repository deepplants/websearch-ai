"""
Search engine client for DuckDuckGo.
"""
import logging
from typing import Dict, List, Optional

from ddgs import DDGS

from ..config import Settings

logger = logging.getLogger(__name__)


class SearchEngine:
    """Handles search queries using DuckDuckGo."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
    
    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict]:
        """Perform a search query."""
        if max_results is None:
            max_results = self.settings.search_max_results_per_query
        
        try:
            with DDGS() as ddgs:  # type: ignore
                results = []
                for r in ddgs.text(query, max_results=max_results):  # type: ignore
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href"),
                        "snippet": r.get("body", "")
                    })
                logger.info(f"Search returned {len(results)} results for: {query}")
                return results
        except Exception as e:
            logger.error(f"Search failed for query '{query}': {e}")
            return []

