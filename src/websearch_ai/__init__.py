"""
Web Search Pipeline - Modular and configurable web search with LLM summarization.
"""

from .clients import HTTPFetcher, LLMClient, SearchEngine
from .config import Settings
from .core import BetterQueries, SearchResult, WebSearchPipeline
from .filters import URLFilter
from .managers import CacheManager, PromptManager, RobotsChecker

__version__ = "2.0.0"

__all__ = [
    "Settings",
    "SearchResult",
    "BetterQueries",
    "WebSearchPipeline",
    "CacheManager",
    "PromptManager",
    "RobotsChecker",
    "HTTPFetcher",
    "LLMClient",
    "SearchEngine",
    "URLFilter",
]
