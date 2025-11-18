"""
Cache manager for storing fetched content.
"""

import hashlib
import logging
from pathlib import Path

import aiofiles

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages file-based caching of fetched content."""

    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Cache directory: {self.cache_dir}")

    def _get_cache_path(self, url: str) -> Path:
        """Generate cache file path for a URL."""
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}.txt"

    async def read(self, url: str) -> str | None:
        """Read cached content for a URL."""
        cache_path = self._get_cache_path(url)
        if cache_path.exists():
            try:
                async with aiofiles.open(cache_path, encoding="utf-8") as f:
                    content = await f.read()
                logger.debug(f"Cache hit for URL: {url}")
                return content
            except Exception as e:
                logger.warning(f"Failed to read cache for {url}: {e}")
        return None

    async def write(self, url: str, content: str) -> None:
        """Write content to cache for a URL."""
        cache_path = self._get_cache_path(url)
        try:
            async with aiofiles.open(cache_path, "w", encoding="utf-8") as f:
                await f.write(content)
            logger.debug(f"Cached content for URL: {url}")
        except Exception as e:
            logger.warning(f"Failed to write cache for {url}: {e}")
