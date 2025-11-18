"""
Web Search Pipeline - Modular and configurable web search with LLM summarization.
"""
from .config import Settings
from .core import SearchResult, BetterQueries, WebSearchPipeline
from .managers import CacheManager, PromptManager, RobotsChecker
from .clients import HTTPFetcher, LLMClient, SearchEngine
from .filters import URLFilter

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
