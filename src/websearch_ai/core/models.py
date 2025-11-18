"""
Data models for the web search pipeline.
"""

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """Represents a single search result with its metadata."""

    better_query: str = Field(
        ..., description="The better search query that resulted in this result"
    )
    title: str = Field(..., description="The title of the search result")
    url: str = Field(..., description="The URL of the search result")
    snippet: str = Field(..., description="The snippet of the search result")
    relevance: int = Field(0, description="The relevance score of the search result")
    complete_text: str | None = Field(
        None, description="The complete text of the search result"
    )
    summary: str | None = Field(None, description="The summary of the search result")

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return self.model_dump()


class BetterQueries(BaseModel):
    """Pydantic model for LLM-generated better queries."""

    queries: list[str] = Field(
        ..., description="List of better search queries", min_length=1
    )
