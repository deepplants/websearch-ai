"""
Core business logic for the web search pipeline.
"""
from .models import SearchResult, BetterQueries
from .pipeline import WebSearchPipeline

__all__ = ["SearchResult", "BetterQueries", "WebSearchPipeline"]

