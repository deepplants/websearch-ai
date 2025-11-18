"""
HTTP fetcher with rate limiting and politeness.
"""
import asyncio
import logging
import time
from typing import Dict, Optional
from urllib.parse import urlparse

import aiohttp
import trafilatura

from ..config import Settings
from ..managers import CacheManager, RobotsChecker

logger = logging.getLogger(__name__)


class HTTPFetcher:
    """Handles HTTP fetching with rate limiting and politeness."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.domain_last_fetch: Dict[str, float] = {}
        self.domain_locks: Dict[str, asyncio.Lock] = {}
        self.semaphore = asyncio.Semaphore(settings.max_concurrent_fetches)
        
        self.headers = {
            "User-Agent": settings.user_agent,
            "Accept-Encoding": settings.accept_encoding
        }
    
    async def _wait_for_domain(self, domain: str) -> None:
        """Enforce per-domain rate limiting."""
        last_fetch = self.domain_last_fetch.get(domain, 0)
        wait_time = self.settings.per_domain_delay - (time.time() - last_fetch)
        if wait_time > 0:
            await asyncio.sleep(wait_time)
    
    async def _fetch_url(
        self, 
        url: str, 
        session: aiohttp.ClientSession, 
        proxy: Optional[str] = None
    ) -> Optional[str]:
        """Fetch a single URL with proper error handling."""
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Get or create lock for this domain
        lock = self.domain_locks.setdefault(domain, asyncio.Lock())
        
        async with lock:
            await self._wait_for_domain(domain)
            
            try:
                kwargs: Dict = {}
                if proxy:
                    kwargs["proxy"] = proxy
                
                timeout = aiohttp.ClientTimeout(total=self.settings.fetch_timeout)
                async with session.get(url, timeout=timeout, **kwargs) as resp:
                    if resp.status != 200:
                        logger.warning(f"Non-200 status ({resp.status}) for {url}")
                        return None
                    
                    content_type = resp.headers.get("Content-Type", "").lower()
                    
                    # Skip PDFs
                    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
                        logger.info(f"Skipping PDF: {url}")
                        self.domain_last_fetch[domain] = time.time()
                        return None
                    
                    # Handle content encoding
                    try:
                        html = await resp.text()
                    except Exception as encoding_error:
                        if "zstd" in str(encoding_error).lower():
                            logger.warning(f"Zstd encoding error for {url}, retrying")
                            retry_headers = {"Accept-Encoding": "gzip, deflate, br"}
                            async with session.get(
                                url, headers=retry_headers, timeout=timeout, **kwargs
                            ) as retry_resp:
                                if retry_resp.status != 200:
                                    logger.warning(f"Retry failed for {url}")
                                    return None
                                html = await retry_resp.text()
                        else:
                            logger.error(f"Content encoding error for {url}: {encoding_error}")
                            return None
                    
                    self.domain_last_fetch[domain] = time.time()
                    
                    # Extract text using trafilatura
                    text = trafilatura.extract(
                        html, 
                        include_tables=False, 
                        include_comments=False
                    )
                    
                    if not text:
                        logger.warning(f"No text extracted from {url}")
                        return None
                    
                    logger.info(f"Successfully fetched {url} ({len(text)} chars)")
                    return text
                    
            except asyncio.TimeoutError:
                logger.warning(f"Timeout fetching {url}")
                return None
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
                return None
    
    async def fetch_with_cache(
        self,
        url: str,
        session: aiohttp.ClientSession,
        cache: Optional[CacheManager],
        robots_checker: RobotsChecker,
        proxy: Optional[str] = None
    ) -> Optional[str]:
        """Fetch URL with caching and robots.txt checking."""
        # Check cache first (if enabled)
        if cache:
            cached = await cache.read(url)
            if cached:
                return cached
        
        # Check robots.txt
        if not await robots_checker.is_allowed(url, session):
            logger.info(f"Blocked by robots.txt: {url}")
            return None
        
        # Fetch with rate limiting
        async with self.semaphore:
            text = await self._fetch_url(url, session, proxy)
        
        # Cache result (if enabled)
        if text and cache:
            await cache.write(url, text)
        
        return text

