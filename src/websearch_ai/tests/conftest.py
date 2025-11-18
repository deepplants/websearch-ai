"""
Pytest configuration and shared fixtures.
"""

import pytest
from websearch.config import Settings


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create a temporary cache directory."""
    cache_dir = tmp_path / "cache_test"
    cache_dir.mkdir()
    return str(cache_dir)


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def mock_settings(temp_cache_dir):
    """Create mock settings for testing."""
    return Settings(
        openai_api_key="test-key",
        openai_model="gpt-4.1-nano",
        openai_temperature=0.2,
        cache_dir=temp_cache_dir,
        cache_enabled=True,
        search_num_better_queries=3,
        search_max_results_per_query=2,
        min_relevance_score=1,
        disallowed_domains=["youtube.com"],
        log_level="ERROR",  # Quiet during tests
    )


@pytest.fixture
def sample_search_results():
    """Sample search results for testing."""
    from websearch.core import SearchResult

    return [
        SearchResult(
            better_query="test query 1",
            title="Test Result 1",
            url="https://example.com/1",
            snippet="This is a test snippet 1",
            relevance=4,
            complete_text="Full text content 1",
            summary="Summary of result 1",
        ),
        SearchResult(
            better_query="test query 2",
            title="Test Result 2",
            url="https://example.com/2",
            snippet="This is a test snippet 2",
            relevance=5,
            complete_text="Full text content 2",
            summary="Summary of result 2",
        ),
    ]


@pytest.fixture
def mock_prompts_yaml(tmp_path):
    """Create a mock prompts.yaml file."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    prompts_file = prompts_dir / "prompts.yaml"

    content = """
better_queries_prompt: |
  Generate better search queries for: {query}

relevance_filtering_prompt: |
  Rate relevance for query: {query}
  Content: {content}

summarize_text_prompt: |
  Summarize for query: {query}
  Content: {content}

merge_summaries_prompt: |
  Merge summaries for query: {query}
  Summaries: {summaries}
"""
    prompts_file.write_text(content)
    return prompts_file
