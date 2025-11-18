"""
Unit tests for CacheManager.
"""

import pytest
from websearch.managers import CacheManager


class TestCacheManager:
    """Tests for CacheManager class."""

    @pytest.mark.asyncio
    async def test_create_cache_manager(self, temp_cache_dir):
        """Test creating cache manager."""
        cache = CacheManager(temp_cache_dir)
        assert cache.cache_dir.exists()
        assert cache.cache_dir.is_dir()

    @pytest.mark.asyncio
    async def test_write_and_read_cache(self, temp_cache_dir):
        """Test writing and reading from cache."""
        cache = CacheManager(temp_cache_dir)

        url = "https://example.com/test"
        content = "This is test content for caching"

        # Write to cache
        await cache.write(url, content)

        # Read from cache
        cached_content = await cache.read(url)
        assert cached_content == content

    @pytest.mark.asyncio
    async def test_read_nonexistent_cache(self, temp_cache_dir):
        """Test reading from cache when entry doesn't exist."""
        cache = CacheManager(temp_cache_dir)

        url = "https://example.com/nonexistent"
        cached_content = await cache.read(url)

        assert cached_content is None

    @pytest.mark.asyncio
    async def test_cache_different_urls(self, temp_cache_dir):
        """Test caching multiple different URLs."""
        cache = CacheManager(temp_cache_dir)

        url1 = "https://example.com/page1"
        url2 = "https://example.com/page2"
        content1 = "Content for page 1"
        content2 = "Content for page 2"

        await cache.write(url1, content1)
        await cache.write(url2, content2)

        assert await cache.read(url1) == content1
        assert await cache.read(url2) == content2

    @pytest.mark.asyncio
    async def test_cache_overwrites(self, temp_cache_dir):
        """Test that cache overwrites previous content."""
        cache = CacheManager(temp_cache_dir)

        url = "https://example.com/test"
        content1 = "Original content"
        content2 = "Updated content"

        await cache.write(url, content1)
        await cache.write(url, content2)

        cached = await cache.read(url)
        assert cached == content2
