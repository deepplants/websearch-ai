# Web Search Pipeline v2.0 - Modular & Configurable

> **Well-organized, production-ready web search with LLM-powered summarization**

A modular web search system with intelligent query expansion, relevance filtering, content extraction, and AI-powered summarization.

<div align="left">

[📚 <b>Documentation Hub</b> &larr;](../docs/README.md)

</div>

## 🎯 Features

### Core Features
- ✅ **Clean Architecture**: Organized into core, config, clients, managers, filters
- ✅ **Modular Design**: Each component has a single, clear responsibility
- ✅ **YAML Configuration**: All parameters configurable via YAML
- ✅ **LLM-Powered**: Query improvement, relevance scoring, and summarization
- ✅ **Respectful Crawling**: Rate limiting, robots.txt compliance, domain filtering
- ✅ **File-Based Caching**: Efficient caching of fetched content
- ✅ **Type-Safe**: Pydantic models with full validation
- ✅ **Production Ready**: Comprehensive logging and error handling

### New Additions (v2.1)
- ✅ **REST API**: FastAPI-based REST API with auto-generated docs
- ✅ **Comprehensive Tests**: Unit and integration tests with pytest
- ✅ **Utility Scripts**: Tools for testing, benchmarking, and maintenance
- ✅ **Export Capabilities**: Export results to JSON, CSV, Markdown
- ✅ **Performance Benchmarks**: Measure and optimize performance
- ✅ **Configuration Validation**: Validate settings before deployment

## 📁 Project Structure

```
websearch/
├── __init__.py                 # Package exports
├── cli.py                      # Command-line interface
├── README.md                   # Main documentation
├── requirements.txt            # Python dependencies
│
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── models.py              # Data models (SearchResult, BetterQueries)
│   └── pipeline.py            # Main orchestration pipeline
│
├── config/                     # Configuration management
│   ├── __init__.py
│   ├── settings.py            # Settings class with validation
│   ├── config.yaml            # Main configuration file
│   └── config.example.yaml    # Example configuration
│
├── prompts/                    # LLM prompt templates
│   ├── __init__.py
│   └── prompts.yaml           # All prompt templates
│
├── clients/                    # External service clients
│   ├── __init__.py
│   ├── http.py                # HTTP fetcher with rate limiting
│   ├── llm.py                 # OpenAI LLM client
│   └── search.py              # DuckDuckGo search engine
│
├── managers/                   # Core managers
│   ├── __init__.py
│   ├── cache.py               # File-based cache manager
│   ├── prompts.py             # Prompt loader & formatter
│   └── robots.py              # Robots.txt checker
│
├── filters/                    # Content filters
│   ├── __init__.py
│   └── url_filter.py          # Domain-based URL filtering
│
├── api/                        # REST API (NEW!)
│   ├── __init__.py
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # API dependencies
│   └── README.md              # API documentation
│
├── tests/                      # Unit tests (NEW!)
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── requirements.txt       # Test dependencies
│   ├── test_*.py              # Test modules
│   └── README.md              # Testing guide
│
├── scripts/                    # Utility scripts (NEW!)
│   ├── run_tests.sh           # Run test suite
│   ├── clear_cache.py         # Clear cache
│   ├── validate_config.py     # Validate configuration
│   ├── benchmark.py           # Performance benchmarks
│   ├── export_results.py      # Export search results
│   └── README.md              # Scripts documentation
│
├── examples/                   # Usage examples
│   └── usage_examples.py      # Comprehensive examples
│
└── docs/                       # Documentation
    ├── README.md              # Documentation index
    ├── README_CONFIG.md       # Configuration guide
    ├── REFACTORING.md         # Refactoring details
    ├── CHANGES.md             # Changelog
    └── MIGRATION_GUIDE.md     # Migration instructions
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

```bash
# Run a search from command line
python -m websearch.cli "latest AI developments 2025"

# Or using the module directly
cd /path/to/servers
python -m websearch.cli "your search query"
```

### Python API

```python
from websearch import Settings, WebSearchPipeline

# Load configuration from config.yaml
settings = Settings.from_yaml()

# Create and run pipeline
pipeline = WebSearchPipeline(settings)
results, final_answer = await pipeline.run("your query here")

# Access results
for result in results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    print(f"Relevance: {result.relevance}/5")
    print(f"Summary: {result.summary}\n")

print(f"Final Answer:\n{final_answer}")
```

## ⚙️ Configuration

### YAML Configuration

Edit `config/config.yaml`:

```yaml
openai:
  model: "gpt-4.1-nano"
  temperature: 0.2

search:
  num_better_queries: 10        # Number of improved queries to generate
  max_results_per_query: 5      # Results per query

filtering:
  min_relevance_score: 3        # Minimum relevance (0-5)
  disallowed_domains:
    - youtube.com
    - youtu.be

llm_tokens:
  better_queries: 512
  relevance_check: 100
  summarize_content: 2048
  merge_summaries: 4096

fetching:
  max_concurrent_fetches: 20
  per_domain_delay: 0.8
  fetch_timeout: 30

cache:
  enabled: true
  directory: "cache_async"

logging:
  level: "INFO"
```

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional (overrides config.yaml)
export LOG_LEVEL="DEBUG"
```

### Configuration Presets

**Fast Mode** (quick results, less thorough):
```yaml
search:
  num_better_queries: 5
  max_results_per_query: 3
filtering:
  min_relevance_score: 2
```

**Research Mode** (comprehensive, slower):
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

## 🏗️ Architecture

### Pipeline Flow

```
User Query
    ↓
1. Generate Better Queries (LLM)
    ↓
2. Perform Searches (DuckDuckGo)
    ↓
3. Filter by Relevance (LLM Scoring)
    ↓
4. Fetch Content (HTTP + Cache + Robots.txt)
    ↓
5. Summarize Each (LLM)
    ↓
6. Merge Summaries (LLM)
    ↓
Final Answer
```

### Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **core/** | Main business logic and data models |
| **config/** | Settings management and validation |
| **prompts/** | LLM prompt templates |
| **clients/** | External service wrappers (HTTP, LLM, Search) |
| **managers/** | Cache, prompts, and robots.txt management |
| **filters/** | URL validation and filtering |
| **cli.py** | Command-line interface |
| **examples/** | Usage examples and demos |

### Key Classes

- **`WebSearchPipeline`**: Main orchestrator for the search workflow
- **`Settings`**: Configuration with Pydantic validation
- **`SearchResult`**: Type-safe search result model
- **`LLMClient`**: OpenAI API wrapper
- **`HTTPFetcher`**: Rate-limited HTTP client
- **`CacheManager`**: File-based caching
- **`URLFilter`**: Domain filtering

## 💻 Usage Examples

### 1. Basic Search

```python
from websearch import Settings, WebSearchPipeline

settings = Settings.from_yaml()
pipeline = WebSearchPipeline(settings)

results, answer = await pipeline.run("quantum computing breakthroughs 2025")
print(answer)
```

### 2. Custom Configuration

```python
from websearch import Settings, WebSearchPipeline

settings = Settings(
    openai_api_key="your-key",
    search_num_better_queries=15,
    min_relevance_score=4,
    log_level="DEBUG"
)

pipeline = WebSearchPipeline(settings)
results, answer = await pipeline.run("climate change solutions")
```

### 3. Using Individual Components

```python
from websearch.clients import SearchEngine
from websearch.config import Settings

settings = Settings.from_yaml()
search_engine = SearchEngine(settings)

results = search_engine.search("machine learning", max_results=10)
for r in results:
    print(f"{r['title']}: {r['url']}")
```

### 4. Custom Domain Filtering

```python
from websearch import Settings, WebSearchPipeline

settings = Settings.from_yaml()
settings.disallowed_domains = [
    "youtube.com", "twitter.com", "facebook.com"
]

pipeline = WebSearchPipeline(settings)
results, answer = await pipeline.run("social media trends")
```

## 🧪 Testing

```bash
# Test imports
python -c "from websearch import *; print('✅ All imports OK')"

# Run examples
cd /path/to/servers/websearch
python examples/usage_examples.py

# Run CLI with test query
python -m websearch.cli "test query"
```

## 📊 Statistics

- **Total Files**: 35+ Python files + YAML configs
- **Code Modules**: 16 core files
- **Test Files**: 7 test modules
- **Utility Scripts**: 5 scripts
- **API Endpoints**: 5 REST endpoints
- **Average File Size**: ~65 lines
- **Longest File**: pipeline.py (~289 lines)
- **Test Coverage**: Unit + Integration tests
- **Lint Status**: ✅ Clean
- **API Documentation**: Auto-generated (Swagger + ReDoc)

## 🆕 What's New in v2.1

### REST API
Full-featured REST API with FastAPI:
```bash
# Start API server
python -m uvicorn websearch.api.main:app --reload

# Visit interactive docs
open http://localhost:8000/docs
```

### Comprehensive Tests
Unit and integration tests with pytest:
```bash
# Run all tests
pytest tests/

# With coverage report
pytest tests/ --cov=websearch
```

### Utility Scripts
Production-ready tools:
```bash
# Validate configuration
python scripts/validate_config.py

# Benchmark performance
python scripts/benchmark.py

# Export results to JSON/CSV/Markdown
python scripts/export_results.py "query" --format json

# Clear cache
python scripts/clear_cache.py
```

See the [API README](api/README.md), [Tests README](tests/README.md), and [Scripts README](scripts/README.md) for details.

## 🔄 Migration from Old Structure

### Import Changes

**Before:**
```python
from web_search_improved import Settings, WebSearchPipeline
from config import Settings
from models import SearchResult
```

**After:**
```python
from websearch import Settings, WebSearchPipeline
from websearch.config import Settings
from websearch.core import SearchResult
```

### File Locations

| Old | New |
|-----|-----|
| `config.py` | `config/settings.py` |
| `models.py` | `core/models.py` |
| `pipeline.py` | `core/pipeline.py` |
| `web_search_refactored.py` | `cli.py` |
| `example_usage.py` | `examples/usage_examples.py` |
| `config/prompts.yaml` | `prompts/prompts.yaml` |

## 🛠️ Development

### Adding New Features

**New Search Engine:**
```python
# clients/brave_search.py
from ..config import Settings

class BraveSearchEngine:
    def __init__(self, settings: Settings):
        self.settings = settings
    
    def search(self, query: str, max_results: int):
        # Implementation
        pass
```

**New Filter:**
```python
# filters/content_filter.py
class ContentFilter:
    def filter(self, content: str) -> bool:
        # Implementation
        pass
```

**New Cache Backend:**
```python
# managers/redis_cache.py
class RedisCache:
    async def read(self, key: str):
        pass
    
    async def write(self, key: str, value: str):
        pass
```

### Code Style

- Use type hints for all function parameters and returns
- Add docstrings to all classes and public methods
- Keep files focused and under 300 lines
- Use relative imports within the package
- Follow PEP 8 naming conventions

## 📝 Dependencies

- `openai` - LLM API client
- `pydantic` - Data validation
- `aiohttp` - Async HTTP client
- `trafilatura` - Content extraction
- `ddgs` - DuckDuckGo search
- `pyyaml` - YAML configuration
- `aiofiles` - Async file operations

## 🤝 Contributing

The modular structure makes contributions easy:
1. Each component is independent with clear interfaces
2. Easy to test individual components
3. Minimal cross-component dependencies
4. Well-documented code

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- OpenAI for GPT models
- DuckDuckGo for free search API
- Trafilatura for content extraction

---

**Version**: 2.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: November 2025

For detailed documentation, see the `docs/` directory.

