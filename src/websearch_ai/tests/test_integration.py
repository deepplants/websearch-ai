"""
Integration tests for the web search pipeline.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from websearch import BetterQueries, SearchResult, WebSearchPipeline


class TestWebSearchPipelineIntegration:
    """Integration tests for WebSearchPipeline."""

    @pytest.fixture
    def mock_llm_client(self):
        """Mock LLM client for testing."""
        with patch("websearch.core.pipeline.LLMClient") as mock:
            client = Mock()
            client.call_structured = AsyncMock(
                return_value=BetterQueries(queries=["query 1", "query 2"])
            )
            client.call_text = AsyncMock(return_value="3")
            mock.return_value = client
            yield mock

    @pytest.fixture
    def mock_search_engine(self):
        """Mock search engine for testing."""
        with patch("websearch.core.pipeline.SearchEngine") as mock:
            engine = Mock()
            engine.search = Mock(
                return_value=[
                    {
                        "title": "Result 1",
                        "url": "https://example.com/1",
                        "snippet": "Snippet 1",
                    },
                    {
                        "title": "Result 2",
                        "url": "https://example.com/2",
                        "snippet": "Snippet 2",
                    },
                ]
            )
            mock.return_value = engine
            yield mock

    @pytest.mark.asyncio
    async def test_pipeline_initialization(self, mock_settings):
        """Test pipeline initialization."""
        pipeline = WebSearchPipeline(mock_settings)

        assert pipeline.settings == mock_settings
        assert pipeline.prompt_manager is not None
        assert pipeline.url_filter is not None
        assert pipeline.fetcher is not None

    @pytest.mark.asyncio
    async def test_generate_better_queries(self, mock_settings, mock_llm_client):
        """Test generating better queries."""
        pipeline = WebSearchPipeline(mock_settings)

        with patch.object(
            pipeline.llm,
            "call_structured",
            return_value=BetterQueries(queries=["q1", "q2", "q3"]),
        ):
            queries = await pipeline._generate_better_queries("test query")

            assert len(queries) <= mock_settings.search_num_better_queries
            assert isinstance(queries, list)

    @pytest.mark.asyncio
    async def test_perform_searches(self, mock_settings, mock_search_engine):
        """Test performing searches."""
        pipeline = WebSearchPipeline(mock_settings)

        queries = ["query 1", "query 2"]
        results = await pipeline._perform_searches(queries)

        assert isinstance(results, list)
        for result in results:
            assert isinstance(result, SearchResult)
            assert result.url
            assert result.title

    @pytest.mark.asyncio
    async def test_url_filtering_in_search(self, mock_settings):
        """Test that disallowed URLs are filtered out."""
        mock_settings.disallowed_domains = ["blocked.com"]
        pipeline = WebSearchPipeline(mock_settings)

        with patch.object(
            pipeline.search_engine,
            "search",
            return_value=[
                {"title": "Allowed", "url": "https://example.com", "snippet": "OK"},
                {"title": "Blocked", "url": "https://blocked.com", "snippet": "NO"},
            ],
        ):
            results = await pipeline._perform_searches(["test"])

            # Should only have the allowed URL
            assert len(results) == 1
            assert "example.com" in results[0].url
            assert "blocked.com" not in results[0].url
