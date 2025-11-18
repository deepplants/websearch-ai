"""
Configuration management for the web search pipeline.
"""
import os
import logging
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Settings(BaseModel):
    """Application settings with validation."""
    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key (required)")
    openai_model: str = Field(default="gpt-4.1-nano", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.2, ge=0, le=2, description="Temperature for LLM")
    
    # LLM Token Limits
    llm_tokens_better_queries: int = Field(default=512, gt=0)
    llm_tokens_relevance_check: int = Field(default=100, gt=0)
    llm_tokens_summarize: int = Field(default=2048, gt=0)
    llm_tokens_merge: int = Field(default=4096, gt=0)
    llm_tokens_coverage: int = Field(default=1024, gt=0)
    
    # Search Configuration
    search_max_results_per_query: int = Field(default=5, gt=0)
    search_total_max_results: int = Field(default=12, gt=0)
    search_num_better_queries: int = Field(default=10, gt=0)
    
    # HTTP Fetching Configuration
    max_concurrent_fetches: int = Field(default=20, gt=0)
    per_domain_delay: float = Field(default=0.8, gt=0)
    fetch_timeout: int = Field(default=30, gt=0)
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    accept_encoding: str = Field(default="gzip, deflate, br")
    max_content_chars: int = Field(default=8000, gt=0)
    
    # Filtering Configuration
    min_relevance_score: int = Field(default=3, ge=0, le=5)
    disallowed_domains: List[str] = Field(default_factory=lambda: ["youtube.com", "youtu.be"])
    
    # Cache Configuration
    cache_dir: str = Field(default="cache_async")
    cache_enabled: bool = Field(default=True)
    
    # Proxy Configuration
    use_proxies: bool = Field(default=False)
    proxies: List[str] = Field(default_factory=list)
    
    # Paths
    prompts_path: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "prompts" / "prompts.yaml")
    config_path: Optional[Path] = Field(default=None)
    
    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def from_yaml(cls, config_path: Optional[Path | str] = None) -> "Settings":
        """Load settings from YAML file and environment variables."""
        if config_path is None:
            config_path = Path(__file__).with_name("config.yaml")
        elif isinstance(config_path, str):
            config_path = Path(config_path)
        
        # Load YAML config
        config_data = {}
        if config_path.exists():
            with config_path.open("r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f) or {}
            
            # Flatten nested YAML structure
            config_data = {
                # OpenAI settings
                "openai_api_key": yaml_data.get("openai", {}).get("api_key"),
                "openai_model": yaml_data.get("openai", {}).get("model", "gpt-4.1-nano"),
                "openai_temperature": yaml_data.get("openai", {}).get("temperature", 0.2),
                
                # LLM tokens
                "llm_tokens_better_queries": yaml_data.get("llm_tokens", {}).get("better_queries", 512),
                "llm_tokens_relevance_check": yaml_data.get("llm_tokens", {}).get("relevance_check", 100),
                "llm_tokens_summarize": yaml_data.get("llm_tokens", {}).get("summarize_content", 2048),
                "llm_tokens_merge": yaml_data.get("llm_tokens", {}).get("merge_summaries", 4096),
                "llm_tokens_coverage": yaml_data.get("llm_tokens", {}).get("coverage_check", 1024),
                
                # Search settings
                "search_max_results_per_query": yaml_data.get("search", {}).get("max_results_per_query", 5),
                "search_total_max_results": yaml_data.get("search", {}).get("total_max_results", 12),
                "search_num_better_queries": yaml_data.get("search", {}).get("num_better_queries", 10),
                
                # Fetching settings
                "max_concurrent_fetches": yaml_data.get("fetching", {}).get("max_concurrent_fetches", 20),
                "per_domain_delay": yaml_data.get("fetching", {}).get("per_domain_delay", 0.8),
                "fetch_timeout": yaml_data.get("fetching", {}).get("fetch_timeout", 30),
                "user_agent": yaml_data.get("fetching", {}).get("user_agent", "Mozilla/5.0..."),
                "accept_encoding": yaml_data.get("fetching", {}).get("accept_encoding", "gzip, deflate, br"),
                "max_content_chars": yaml_data.get("fetching", {}).get("max_content_chars", 8000),
                
                # Filtering settings
                "min_relevance_score": yaml_data.get("filtering", {}).get("min_relevance_score", 3),
                "disallowed_domains": yaml_data.get("filtering", {}).get("disallowed_domains", ["youtube.com", "youtu.be"]),
                
                # Cache settings
                "cache_dir": yaml_data.get("cache", {}).get("directory", "cache_async"),
                "cache_enabled": yaml_data.get("cache", {}).get("enabled", True),
                
                # Proxy settings
                "use_proxies": yaml_data.get("proxy", {}).get("use_proxies", False),
                "proxies": yaml_data.get("proxy", {}).get("proxies", []),
                
                # Paths
                "prompts_path": Path(__file__).parent.parent / "prompts" / yaml_data.get("paths", {}).get("prompts_file", "prompts.yaml"),
                "config_path": config_path,
                
                # Logging
                "log_level": yaml_data.get("logging", {}).get("level", "INFO"),
                "log_format": yaml_data.get("logging", {}).get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            }
        
        # Override with environment variables
        api_key_from_env = os.getenv("OPENAI_API_KEY")
        if api_key_from_env:
            config_data["openai_api_key"] = api_key_from_env
        
        # Validate API key
        if not config_data.get("openai_api_key"):
            raise ValueError(
                "OPENAI_API_KEY is required but not set. "
                "Please set it in config.yaml or as an environment variable."
            )
        
        return cls(**config_data)
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Create Settings from YAML config file (with env variable overrides)."""
        return cls.from_yaml()

