# Configuration Guide

<div align="center">

**📚 [Documentation Hub](README.md)** | **🏠 [Main README](../README.md)** | **⚡ [Quick Start](QUICKSTART.md)** | **📐 [Structure](STRUCTURE.md)**

</div>

---

Complete guide to configuring websearch for your needs.

## Table of Contents

- [Configuration Files](#configuration-files)
- [Configuration Options](#configuration-options)
- [Environment Variables](#environment-variables)
- [Configuration Presets](#configuration-presets)
- [Custom Configuration](#custom-configuration)
- [Validation](#validation)

## Configuration Files

### Main Configuration

The main configuration file is located at `config/config.yaml`:

```yaml
openai:
  api_key: null  # Set via OPENAI_API_KEY env variable
  model: "gpt-4.1-nano"
  temperature: 0.2

search:
  num_better_queries: 10
  max_results_per_query: 5
  total_max_results: 12

filtering:
  min_relevance_score: 3
  disallowed_domains:
    - youtube.com
    - youtu.be

llm_tokens:
  better_queries: 512
  relevance_check: 100
  summarize_content: 2048
  merge_summaries: 4096
  coverage_check: 1024

fetching:
  max_concurrent_fetches: 20
  per_domain_delay: 0.8
  fetch_timeout: 30
  user_agent: "Mozilla/5.0..."
  accept_encoding: "gzip, deflate, br"
  max_content_chars: 8000

cache:
  enabled: true
  directory: "cache_async"

proxy:
  use_proxies: false
  proxies: []

paths:
  prompts_file: "prompts.yaml"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Example Configuration

See `config/config.example.yaml` for a complete example with comments.

## Configuration Options

### OpenAI Settings

```yaml
openai:
  api_key: null          # Your OpenAI API key (use env variable)
  model: "gpt-4.1-nano"  # Model to use
  temperature: 0.2       # Creativity level (0-2)
```

**Models:**
- `gpt-4.1-nano` - Fast, cost-effective (recommended)
- `gpt-4` - Higher quality, slower
- `gpt-3.5-turbo` - Faster, cheaper

**Temperature:**
- `0.0-0.3` - Deterministic, factual
- `0.4-0.7` - Balanced
- `0.8-2.0` - Creative (not recommended for search)

### Search Settings

```yaml
search:
  num_better_queries: 10        # Number of improved queries to generate
  max_results_per_query: 5      # Results per query
  total_max_results: 12         # Total results to fetch
```

**Trade-offs:**
- More queries = more comprehensive but slower
- More results = better coverage but more LLM calls
- Adjust based on your speed vs quality needs

### Filtering Settings

```yaml
filtering:
  min_relevance_score: 3        # Minimum score (0-5)
  disallowed_domains:
    - youtube.com
    - youtu.be
    - twitter.com
```

**Relevance Scores:**
- `5` - Highly relevant
- `4` - Relevant
- `3` - Somewhat relevant (default threshold)
- `2` - Marginally relevant
- `1` - Barely relevant
- `0` - Not relevant

### LLM Token Limits

```yaml
llm_tokens:
  better_queries: 512          # Query improvement
  relevance_check: 100         # Relevance scoring
  summarize_content: 2048      # Content summarization
  merge_summaries: 4096        # Final answer generation
  coverage_check: 1024         # Coverage analysis
```

**Impact:**
- Higher tokens = more detailed but more expensive
- Lower tokens = faster but less detailed

### Fetching Settings

```yaml
fetching:
  max_concurrent_fetches: 20   # Parallel fetch limit
  per_domain_delay: 0.8        # Delay between requests (seconds)
  fetch_timeout: 30            # Request timeout (seconds)
  max_content_chars: 8000      # Max content to extract
```

**Best Practices:**
- Respect rate limits with appropriate delays
- Adjust concurrent fetches based on server capacity
- Larger content = more comprehensive but slower

### Cache Settings

```yaml
cache:
  enabled: true                # Enable/disable caching
  directory: "cache_async"     # Cache directory
```

**Benefits of Caching:**
- Faster repeat searches
- Reduced bandwidth
- Lower API costs (no re-fetching)
- Offline capability

### Proxy Settings

```yaml
proxy:
  use_proxies: false
  proxies:
    - "http://proxy1:8080"
    - "http://proxy2:8080"
```

**Use Cases:**
- Bypass geo-restrictions
- Distribute load
- Improve privacy

## Environment Variables

Environment variables override YAML configuration:

```bash
# Required
export OPENAI_API_KEY="sk-your-key-here"

# Optional
export LOG_LEVEL="DEBUG"
export CACHE_ENABLED="true"
```

## Configuration Presets

### Fast Mode

Optimized for speed:

```yaml
search:
  num_better_queries: 5
  max_results_per_query: 3

filtering:
  min_relevance_score: 2

fetching:
  max_concurrent_fetches: 30

llm_tokens:
  summarize_content: 1500
  merge_summaries: 3000
```

**Use when:**
- Time is critical
- General overview needed
- Cost is a concern

### Balanced Mode (Default)

Balance between speed and quality:

```yaml
search:
  num_better_queries: 10
  max_results_per_query: 5

filtering:
  min_relevance_score: 3

llm_tokens:
  summarize_content: 2048
  merge_summaries: 4096
```

**Use when:**
- Standard searches
- Good quality needed
- Moderate time available

### Quality Mode

Optimized for comprehensiveness:

```yaml
search:
  num_better_queries: 15
  max_results_per_query: 8

filtering:
  min_relevance_score: 4

llm_tokens:
  summarize_content: 3000
  merge_summaries: 6000
```

**Use when:**
- Research and analysis
- Best quality required
- Time is not critical

## Custom Configuration

### Programmatic Configuration

```python
from websearch import Settings

settings = Settings(
    openai_api_key="your-key",
    search_num_better_queries=12,
    min_relevance_score=4,
    cache_enabled=True,
    log_level="DEBUG"
)
```

### Loading from Custom YAML

```python
from websearch import Settings

settings = Settings.from_yaml("path/to/custom_config.yaml")
```

### Overriding Specific Settings

```python
settings = Settings.from_yaml()
settings.search_num_better_queries = 15
settings.min_relevance_score = 4
```

## Validation

### Validate Configuration

Use the validation script:

```bash
python scripts/validate_config.py

# Validate custom config
python scripts/validate_config.py --config custom_config.yaml
```

### Validation Rules

- API key must be set
- Temperature: 0-2
- Relevance score: 0-5
- Token limits: > 0
- Timeouts: > 0
- Delays: > 0

### Common Validation Errors

**Missing API Key:**
```bash
export OPENAI_API_KEY="your-key"
```

**Invalid Temperature:**
```yaml
openai:
  temperature: 0.2  # Must be 0-2
```

**Invalid Relevance Score:**
```yaml
filtering:
  min_relevance_score: 3  # Must be 0-5
```

## Advanced Configuration

For advanced configuration options, see:
- [Advanced Configuration Guide](ADVANCED_CONFIG.md)
- [Performance Optimization](PERFORMANCE.md)
- [Security Configuration](SECURITY.md)

---

<div align="center">

### 🧭 Navigation

**[📚 Documentation Hub](README.md)** | **[🏠 Main README](../README.md)** | **[⚡ Quick Start](QUICKSTART.md)**

**[🧪 Tests](../tests/README.md)** | **[🛠️ Scripts](../scripts/README.md)** | **[🌐 API](../api/README.md)**

[🔧 Advanced Config](ADVANCED_CONFIG.md) | [⚡ Performance](PERFORMANCE.md) | [🐛 Troubleshooting](TROUBLESHOOTING.md)

---

**Related Guides:**
- [Performance Optimization](PERFORMANCE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Troubleshooting](TROUBLESHOOTING.md)

</div>

