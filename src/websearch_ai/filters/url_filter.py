"""
URL filter for blocking disallowed domains.
"""

import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class URLFilter:
    """Filters and validates URLs."""

    def __init__(self, disallowed_domains: list[str]):
        self.disallowed_domains = set(disallowed_domains)

    def is_allowed(self, url: str) -> bool:
        """Check if URL is allowed (not in disallowed list)."""
        try:
            parsed = urlparse(url)
            host = parsed.netloc.lower()
            return not any(domain in host for domain in self.disallowed_domains)
        except Exception as e:
            logger.warning(f"Failed to parse URL {url}: {e}")
            return False
