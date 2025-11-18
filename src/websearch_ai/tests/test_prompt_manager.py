"""
Unit tests for PromptManager.
"""


import pytest
from websearch.managers import PromptManager


class TestPromptManager:
    """Tests for PromptManager class."""

    def test_create_prompt_manager(self, mock_prompts_yaml):
        """Test creating prompt manager."""
        manager = PromptManager(mock_prompts_yaml)
        assert manager.prompts_path == mock_prompts_yaml

    def test_load_prompts(self, mock_prompts_yaml):
        """Test loading prompts from YAML."""
        manager = PromptManager(mock_prompts_yaml)
        prompts = manager.load_prompts()

        assert isinstance(prompts, dict)
        assert "better_queries_prompt" in prompts
        assert "relevance_filtering_prompt" in prompts
        assert "summarize_text_prompt" in prompts
        assert "merge_summaries_prompt" in prompts

    def test_get_prompt(self, mock_prompts_yaml):
        """Test getting specific prompt."""
        manager = PromptManager(mock_prompts_yaml)

        prompt = manager.get_prompt("better_queries_prompt")
        assert "Generate better search queries" in prompt

    def test_get_nonexistent_prompt(self, mock_prompts_yaml):
        """Test getting non-existent prompt raises error."""
        manager = PromptManager(mock_prompts_yaml)

        with pytest.raises(KeyError):
            manager.get_prompt("nonexistent_prompt")

    def test_format_prompt(self, mock_prompts_yaml):
        """Test formatting prompt with values."""
        manager = PromptManager(mock_prompts_yaml)

        template = manager.get_prompt("better_queries_prompt")
        formatted = manager.format_prompt(template, query="test query")

        assert "test query" in formatted
        assert "{query}" not in formatted

    def test_format_prompt_escapes_braces(self, mock_prompts_yaml):
        """Test that format_prompt escapes braces in values."""
        manager = PromptManager(mock_prompts_yaml)

        template = "Process: {value}"
        formatted = manager.format_prompt(template, value="data {key: value}")

        # Braces in the value should be escaped
        assert "data {{key: value}}" in formatted

    def test_load_missing_file(self, tmp_path):
        """Test loading from non-existent file raises error."""
        missing_file = tmp_path / "missing.yaml"
        manager = PromptManager(missing_file)

        with pytest.raises(FileNotFoundError):
            manager.load_prompts()
