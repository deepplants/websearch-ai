"""
Unit tests for data models.
"""

import pytest
from pydantic import ValidationError
from websearch.core import BetterQueries, SearchResult


class TestSearchResult:
    """Tests for SearchResult model."""

    def test_create_search_result(self):
        """Test creating a basic search result."""
        result = SearchResult(
            better_query="test query",
            title="Test Title",
            url="https://example.com",
            snippet="Test snippet",
            relevance=3,
        )

        assert result.better_query == "test query"
        assert result.title == "Test Title"
        assert result.url == "https://example.com"
        assert result.snippet == "Test snippet"
        assert result.relevance == 3
        assert result.complete_text is None
        assert result.summary is None

    def test_search_result_with_optional_fields(self):
        """Test search result with optional fields."""
        result = SearchResult(
            better_query="query",
            title="Title",
            url="https://test.com",
            snippet="snippet",
            relevance=5,
            complete_text="Full text here",
            summary="Summary here",
        )

        assert result.complete_text == "Full text here"
        assert result.summary == "Summary here"

    def test_search_result_to_dict(self):
        """Test converting search result to dictionary."""
        result = SearchResult(
            better_query="test",
            title="Title",
            url="https://example.com",
            snippet="snippet",
            relevance=4,
        )

        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict["title"] == "Title"
        assert result_dict["url"] == "https://example.com"
        assert result_dict["relevance"] == 4


class TestBetterQueries:
    """Tests for BetterQueries model."""

    def test_create_better_queries(self):
        """Test creating better queries model."""
        queries = BetterQueries(queries=["query 1", "query 2", "query 3"])

        assert len(queries.queries) == 3
        assert queries.queries[0] == "query 1"
        assert queries.queries[2] == "query 3"

    def test_better_queries_validation(self):
        """Test that empty queries list is rejected."""
        with pytest.raises(ValidationError):
            BetterQueries(queries=[])

    def test_better_queries_single_item(self):
        """Test better queries with single item."""
        queries = BetterQueries(queries=["single query"])
        assert len(queries.queries) == 1
        assert queries.queries[0] == "single query"
