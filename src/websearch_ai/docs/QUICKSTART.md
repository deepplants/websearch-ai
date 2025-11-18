# websearch - Quick Start Guide

<div align="center">

**📚 [Documentation Hub](README.md)** | **🏠 [Main README](../README.md)** | **📐 [Structure](STRUCTURE.md)** | **⚙️ [Config](CONFIG.md)**

</div>

---

Get up and running with the web search pipeline in 5 minutes!

## 📦 Installation

```bash
# Navigate to the directory
cd /path/to/cabbo-tools/servers

# Install dependencies
pip install -r websearch/requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

## 🚀 Basic Usage

### 1. Command Line (Simplest)

```bash
# Run a search
python -m websearch.cli "latest developments in quantum computing"

# The pipeline will:
# 1. Generate better search queries
# 2. Search DuckDuckGo
# 3. Filter by relevance
# 4. Fetch and extract content
# 5. Summarize each result
# 6. Merge into final answer
```

### 2. Python Script (Most Common)

```python
import asyncio
from websearch import Settings, WebSearchPipeline

async def main():
    # Load configuration
    settings = Settings.from_yaml()
    
    # Create pipeline
    pipeline = WebSearchPipeline(settings)
    
    # Run search
    results, final_answer = await pipeline.run(
        "What are the latest AI breakthroughs in 2025?"
    )
    
    # Print results
    print("\nFinal Answer:")
    print(final_answer)
    
    print("\n\nSources:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Relevance: {result.relevance}/5")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Custom Configuration (Advanced)

```python
import asyncio
import os
from websearch import Settings, WebSearchPipeline

async def main():
    # Create custom settings
    settings = Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model="gpt-4.1-nano",
        search_num_better_queries=12,  # More thorough search
        min_relevance_score=4,          # Higher quality threshold
        max_concurrent_fetches=30,      # Faster fetching
        log_level="DEBUG"               # Verbose logging
    )
    
    # Create and run pipeline
    pipeline = WebSearchPipeline(settings)
    results, answer = await pipeline.run("your query here")
    
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
```

## ⚙️ Configuration

### Option 1: Environment Variable (Recommended)

```bash
export OPENAI_API_KEY="sk-your-key-here"
python -m websearch.cli "your query"
```

### Option 2: YAML Configuration

Edit `config/config.yaml`:

```yaml
openai:
  api_key: "sk-your-key-here"  # Or use env variable
  model: "gpt-4.1-nano"
  temperature: 0.2

search:
  num_better_queries: 10
  max_results_per_query: 5

filtering:
  min_relevance_score: 3
  disallowed_domains:
    - youtube.com
    - youtu.be
```

### Option 3: Programmatic

```python
from websearch import Settings

settings = Settings(
    openai_api_key="your-key",
    search_num_better_queries=8,
    min_relevance_score=3
)
```

## 🎯 Common Use Cases

### Research Mode (Comprehensive)

```python
settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    search_num_better_queries=15,      # Very thorough
    search_max_results_per_query=8,
    min_relevance_score=4,             # High quality only
    llm_tokens_summarize=3000,         # Detailed summaries
    llm_tokens_merge=6000              # Comprehensive answer
)
```

### Fast Mode (Quick Results)

```python
settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    search_num_better_queries=5,       # Fewer queries
    search_max_results_per_query=3,
    min_relevance_score=2,             # Lower threshold
    max_concurrent_fetches=30          # Faster fetching
)
```

### Domain Filtering

```python
settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    disallowed_domains=[
        "youtube.com",
        "twitter.com",
        "facebook.com",
        "reddit.com"
    ]
)
```

## 📖 Examples

Check out `examples/usage_examples.py` for comprehensive examples:

```bash
python websearch/examples/usage_examples.py
```

This includes examples for:
1. Basic usage with defaults
2. Custom configuration
3. Fast mode
4. Research mode
5. Custom YAML configuration
6. Domain filtering

## 🔍 Understanding the Pipeline

The search pipeline has 6 main steps:

```
Your Query
    ↓
[1] Generate Better Queries (LLM)
    • Expands your query into multiple improved versions
    ↓
[2] Perform Searches (DuckDuckGo)
    • Searches for each improved query
    • Collects unique results
    ↓
[3] Filter by Relevance (LLM)
    • Scores each result 0-5 for relevance
    • Keeps only results above threshold
    ↓
[4] Fetch Content (HTTP)
    • Fetches full page content
    • Respects robots.txt and rate limits
    • Uses cache when available
    ↓
[5] Summarize (LLM)
    • Summarizes each page relative to your query
    ↓
[6] Merge Summaries (LLM)
    • Combines all summaries into final answer
    ↓
Final Answer + Sources
```

## 🛠️ Troubleshooting

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY="your-key-here"
```

### "No module named 'websearch'"
```bash
# Make sure you're in the parent directory
cd /path/to/cabbo-tools/servers
python -m websearch.cli "query"
```

### "Import errors"
```bash
# Reinstall dependencies
pip install -r websearch/requirements.txt
```

### Slow performance
```python
# Use fast mode settings
settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    search_num_better_queries=5,
    max_concurrent_fetches=30
)
```

### Too many irrelevant results
```python
# Increase relevance threshold
settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    min_relevance_score=4  # Only high-quality results
)
```

## 📊 Tips & Best Practices

1. **Start with defaults** - They're tuned for balanced performance
2. **Use caching** - Speeds up repeated searches
3. **Adjust relevance threshold** - Higher for quality, lower for coverage
4. **Monitor API usage** - LLM calls can add up
5. **Use domain filtering** - Block low-quality sources
6. **Enable logging** - Set `log_level="DEBUG"` to see what's happening

## 🎓 Next Steps

1. **Read the full README** - `README.md` for detailed documentation
2. **Check structure guide** - `STRUCTURE.md` for architecture details
3. **Explore examples** - `examples/usage_examples.py` for more patterns
4. **Customize configuration** - `config/config.yaml` for your needs
5. **Read the docs** - `docs/` folder for in-depth guides

## 📚 Key Files

- `cli.py` - Command-line interface
- `core/pipeline.py` - Main search pipeline
- `core/models.py` - Data models
- `config/settings.py` - Configuration management
- `config/config.yaml` - Configuration file
- `prompts/prompts.yaml` - LLM prompt templates

## 💡 Quick Tips

**Want more results?**
```python
settings.search_num_better_queries = 15
settings.search_max_results_per_query = 8
```

**Want faster results?**
```python
settings.search_num_better_queries = 5
settings.max_concurrent_fetches = 30
```

**Want better quality?**
```python
settings.min_relevance_score = 4
settings.llm_tokens_summarize = 3000
```

**Want to block certain sites?**
```python
settings.disallowed_domains = ["youtube.com", "twitter.com"]
```

---

**Ready to search?**

```bash
export OPENAI_API_KEY="your-key"
python -m websearch.cli "your amazing query here"
```

Happy searching! 🔍✨

---

<div align="center">

### 🧭 Navigation

**[📚 Documentation Hub](README.md)** | **[🏠 Main README](../README.md)** | **[📐 Project Structure](STRUCTURE.md)**

**[🧪 Tests](../tests/README.md)** | **[🛠️ Scripts](../scripts/README.md)** | **[🌐 API](../api/README.md)**

[⚙️ Configuration](CONFIG.md) | [🚀 Deployment](DEPLOYMENT.md) | [🐛 Troubleshooting](TROUBLESHOOTING.md)

---

**Next Steps:**
- Read the [Full Documentation](README.md)
- Explore [Configuration Options](CONFIG.md)
- Check out [Examples](../examples/usage_examples.py)
- Try the [REST API](../api/README.md)

</div>

