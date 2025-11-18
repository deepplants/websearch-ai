#!/usr/bin/env python3
"""
Example usage of the web search pipeline with YAML configuration.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from websearch import Settings, WebSearchPipeline


async def example_basic():
    """Basic usage with default config.yaml"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Usage with Default Config")
    print("=" * 80)

    # Load settings from default config.yaml
    settings = Settings.from_yaml()
    print(f"✓ Loaded config with model: {settings.openai_model}")
    print(
        f"✓ Search will generate {settings.search_num_better_queries} improved queries"
    )
    print(f"✓ Minimum relevance score: {settings.min_relevance_score}")

    # Create pipeline
    _pipeline = WebSearchPipeline(settings)

    # Run search (uncomment to actually run)
    # results, final_answer = await _pipeline.run("latest AI developments 2025")
    # print(final_answer)


async def example_custom_config():
    """Usage with custom configuration"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Custom Configuration")
    print("=" * 80)

    # Create custom settings programmatically
    settings = Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model="gpt-4.1-nano",
        openai_temperature=0.3,
        search_num_better_queries=8,
        search_max_results_per_query=4,
        min_relevance_score=4,  # Higher quality threshold
        llm_tokens_summarize=3000,  # More detailed summaries
        log_level="DEBUG",  # Verbose logging
    )

    print(f"✓ Custom config: {settings.search_num_better_queries} queries")
    print(f"✓ High quality mode: min relevance = {settings.min_relevance_score}")

    _pipeline = WebSearchPipeline(settings)
    # Run your search...


async def example_fast_mode():
    """Fast mode configuration for quick results"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Fast Mode (Quick & Less Thorough)")
    print("=" * 80)

    settings = Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        search_num_better_queries=5,
        search_max_results_per_query=3,
        min_relevance_score=2,
        llm_tokens_summarize=1500,
        llm_tokens_merge=3000,
        max_concurrent_fetches=30,
        log_level="INFO",
    )

    print(f"✓ Fast mode: {settings.search_num_better_queries} queries only")
    print(f"✓ Lower threshold: min relevance = {settings.min_relevance_score}")
    print(f"✓ Higher concurrency: {settings.max_concurrent_fetches} fetches")

    _pipeline = WebSearchPipeline(settings)
    # Run your search...


async def example_research_mode():
    """Research mode for comprehensive analysis"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Research Mode (Comprehensive & Thorough)")
    print("=" * 80)

    settings = Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        search_num_better_queries=15,
        search_max_results_per_query=8,
        min_relevance_score=4,
        llm_tokens_summarize=3000,
        llm_tokens_merge=6000,
        llm_tokens_coverage=2000,
        max_content_chars=10000,
        log_level="DEBUG",
    )

    print(f"✓ Research mode: {settings.search_num_better_queries} queries")
    print(f"✓ High quality: min relevance = {settings.min_relevance_score}")
    print(f"✓ Detailed summaries: {settings.llm_tokens_summarize} tokens")
    print(f"✓ Comprehensive merge: {settings.llm_tokens_merge} tokens")

    _pipeline = WebSearchPipeline(settings)
    # Run your search...


async def example_with_custom_yaml():
    """Load from a custom YAML file"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Custom YAML File")
    print("=" * 80)

    # Create a custom config file
    custom_yaml = """
openai:
  model: "gpt-4.1-nano"
  temperature: 0.1

search:
  num_better_queries: 12
  max_results_per_query: 6

filtering:
  min_relevance_score: 3
  disallowed_domains:
    - youtube.com
    - youtu.be
    - twitter.com  # Additional filter

logging:
  level: "INFO"
"""

    # Write temporary config
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(custom_yaml)
        temp_path = f.name

    try:
        # Load from custom file
        settings = Settings.from_yaml(temp_path)
        print(f"✓ Loaded from custom file: {temp_path}")
        print(f"✓ Disallowed domains: {len(settings.disallowed_domains)}")
        print(f"✓ Temperature: {settings.openai_temperature}")

        _pipeline = WebSearchPipeline(settings)
    finally:
        # Clean up
        os.unlink(temp_path)


async def example_domain_filtering():
    """Example with custom domain filtering"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Custom Domain Filtering")
    print("=" * 80)

    settings = Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        disallowed_domains=[
            "youtube.com",
            "youtu.be",
            "facebook.com",
            "twitter.com",
            "instagram.com",
            "tiktok.com",
        ],
        min_relevance_score=3,
    )

    print(f"✓ Filtering {len(settings.disallowed_domains)} domains:")
    for domain in settings.disallowed_domains:
        print(f"   - {domain}")

    _pipeline = WebSearchPipeline(settings)
    # Run your search...


async def main():
    """Run all examples"""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set in environment")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\nRunning examples with dummy key (they won't actually execute)...\n")
        os.environ["OPENAI_API_KEY"] = "dummy-key-for-examples"

    # Run all examples
    await example_basic()
    await example_custom_config()
    await example_fast_mode()
    await example_research_mode()
    await example_with_custom_yaml()
    await example_domain_filtering()

    print("\n" + "=" * 80)
    print("✅ All examples completed!")
    print("=" * 80)
    print("\nTo actually run a search, uncomment the pipeline.run() lines")
    print("and provide a valid OPENAI_API_KEY.\n")


if __name__ == "__main__":
    asyncio.run(main())
