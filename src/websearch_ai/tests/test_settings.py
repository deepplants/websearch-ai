"""
Unit tests for Settings configuration.
"""
import os
import pytest
from pathlib import Path
from websearch.config import Settings


class TestSettings:
    """Tests for Settings class."""
    
    def test_create_settings_with_defaults(self):
        """Test creating settings with default values."""
        settings = Settings(openai_api_key="test-key")
        
        assert settings.openai_api_key == "test-key"
        assert settings.openai_model == "gpt-4.1-nano"
        assert settings.openai_temperature == 0.2
        assert settings.search_num_better_queries == 10
        assert settings.min_relevance_score == 3
        assert settings.cache_enabled is True
    
    def test_create_settings_with_custom_values(self):
        """Test creating settings with custom values."""
        settings = Settings(
            openai_api_key="custom-key",
            openai_model="gpt-4",
            search_num_better_queries=15,
            min_relevance_score=4
        )
        
        assert settings.openai_api_key == "custom-key"
        assert settings.openai_model == "gpt-4"
        assert settings.search_num_better_queries == 15
        assert settings.min_relevance_score == 4
    
    def test_settings_validation_temperature(self):
        """Test that invalid temperature is rejected."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            Settings(openai_api_key="key", openai_temperature=3.0)
    
    def test_settings_validation_relevance_score(self):
        """Test that invalid relevance score is rejected."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            Settings(openai_api_key="key", min_relevance_score=10)
    
    def test_settings_disallowed_domains(self):
        """Test disallowed domains configuration."""
        settings = Settings(
            openai_api_key="key",
            disallowed_domains=["youtube.com", "twitter.com"]
        )
        
        assert len(settings.disallowed_domains) == 2
        assert "youtube.com" in settings.disallowed_domains
        assert "twitter.com" in settings.disallowed_domains
    
    def test_settings_from_yaml_with_env_override(self, tmp_path, monkeypatch):
        """Test loading settings from YAML with environment override."""
        # Create test config
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        
        config_content = """
openai:
  api_key: "yaml-key"
  model: "gpt-4.1-nano"

search:
  num_better_queries: 5
"""
        config_file.write_text(config_content)
        
        # Override with environment variable
        monkeypatch.setenv("OPENAI_API_KEY", "env-key")
        
        settings = Settings.from_yaml(config_file)
        
        # Env variable should override YAML
        assert settings.openai_api_key == "env-key"
        assert settings.search_num_better_queries == 5

