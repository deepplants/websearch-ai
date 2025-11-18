"""
Robots.txt checker for respecting web crawling policies.
"""

import logging
import urllib.robotparser
from urllib.parse import urlparse

import aiohttp

logger = logging.getLogger(__name__)


class RobotsChecker:
    """Checks and caches robots.txt rules."""

    def __init__(self):
        self._cache: dict[str, urllib.robotparser.RobotFileParser] = {}

    async def is_allowed(self, url: str, session: aiohttp.ClientSession) -> bool:
        """Check if URL is allowed by robots.txt."""
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        if base in self._cache:
            rp = self._cache[base]
            return rp.can_fetch("*", url)

        robots_url = f"{base}/robots.txt"
        try:
            async with session.get(robots_url, timeout=10) as resp:
                text = await resp.text()

            rp = urllib.robotparser.RobotFileParser()
            rp.parse(text.splitlines())
            self._cache[base] = rp

            allowed = rp.can_fetch("*", url)
            logger.debug(f"Robots.txt check for {url}: {allowed}")
            return allowed
        except Exception as e:
            logger.debug(f"Could not fetch robots.txt for {base}: {e}")
            # Conservative approach: allow if robots.txt is unreachable
            return True
