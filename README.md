# WebSearch AI

A modular and configurable web search library with LLM summarization powered by OpenAI and DuckDuckGo.

## Features

- 🔍 **Web Search**: Integrated DuckDuckGo search engine
- 🤖 **LLM Integration**: OpenAI-powered content summarization
- ⚡ **Async/Await**: Fast asynchronous HTTP operations
- 🎯 **Content Extraction**: Trafilatura-based HTML content extraction
- 💾 **Caching**: Built-in cache management for efficiency
- 🛡️ **Robots.txt**: Respectful crawling with robots.txt compliance
- 🔧 **Configurable**: YAML-based configuration system
- 📦 **Modular**: Clean architecture with dependency injection

## Installation

### From PyPI (once published)

```bash
pip install websearch-ai
```

### From Source

```bash
# Clone the repository
git clone <your-repo-url>
cd workdir

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

### Development Installation

```bash
# Install with development dependencies
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

## Quick Start

### As a Library

```python
import asyncio
from websearch_ai import WebSearchPipeline, Settings

async def main():
    # Initialize with settings
    settings = Settings.from_env()  # Loads from environment variables
    pipeline = WebSearchPipeline(settings)
    
    # Run a search
    results, answer = await pipeline.run("What are the latest AI developments?")
    
    # Process results
    print(f"Final Answer: {answer}")
    for result in results:
        print(f"- {result.title}: {result.url}")

if __name__ == "__main__":
    asyncio.run(main())
```

### As a CLI Tool

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# Run a search
websearch-ai "latest nvidia earnings 2025"

# Or use as a module
python -m websearch_ai.cli "your search query"
```

## Configuration

### Environment Variables

```bash
# Required
export OPENAI_API_KEY='your-api-key-here'

# Optional
export OPENAI_MODEL='gpt-4o-mini'  # Default model
export LOG_LEVEL='INFO'  # Logging level
```

### YAML Configuration

Create a `config.yaml` file (see `src/websearch_ai/config/config.example.yaml` for full options):

```yaml
openai:
  api_key: ${OPENAI_API_KEY}
  model: gpt-4o-mini
  
search:
  max_results: 5
  timeout: 30
  
cache:
  enabled: true
  ttl: 86400
```

## API Reference

### Core Classes

#### `WebSearchPipeline`

Main pipeline for orchestrating web search and summarization.

```python
from websearch_ai import WebSearchPipeline, Settings

settings = Settings.from_env()
pipeline = WebSearchPipeline(settings)
results, answer = await pipeline.run("query")
```

#### `Settings`

Configuration management using Pydantic.

```python
from websearch_ai import Settings

# From environment variables
settings = Settings.from_env()

# From YAML file
settings = Settings.from_yaml("config.yaml")
```

#### `SearchResult`

Data model for search results.

```python
from websearch_ai import SearchResult

result = SearchResult(
    title="Example",
    url="https://example.com",
    snippet="Description",
    content="Full content"
)
```

### Managers

#### `CacheManager`

Manages caching of search results and content.

```python
from websearch_ai import CacheManager

cache = CacheManager(cache_dir=".cache", ttl=86400)
await cache.get("key")
await cache.set("key", "value")
```

#### `PromptManager`

Manages LLM prompts from YAML files.

```python
from websearch_ai import PromptManager

prompts = PromptManager("prompts.yaml")
prompt = prompts.get("search_prompt", query="test")
```

#### `RobotsChecker`

Checks robots.txt compliance before fetching.

```python
from websearch_ai import RobotsChecker

checker = RobotsChecker()
allowed = await checker.can_fetch("https://example.com")
```

### Clients

#### `SearchEngine`

DuckDuckGo search integration.

```python
from websearch_ai import SearchEngine

engine = SearchEngine(max_results=5)
results = await engine.search("query")
```

#### `HTTPFetcher`

Async HTTP client with rate limiting.

```python
from websearch_ai import HTTPFetcher

fetcher = HTTPFetcher(timeout=30)
html = await fetcher.fetch("https://example.com")
```

#### `LLMClient`

OpenAI API client wrapper.

```python
from websearch_ai import LLMClient

client = LLMClient(api_key="key", model="gpt-4o-mini")
response = await client.complete("prompt")
```

## Development

### Setup

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=websearch_ai --cov-report=html

# Run specific test file
pytest src/websearch_ai/tests/test_models.py
```

### Code Quality

```bash
# Format code
ruff format .

# Run linter
ruff check .

# Fix linting issues
ruff check --fix .
```

## Requirements

- Python 3.12+
- OpenAI API key
- Internet connection

## Dependencies

Core dependencies:
- `openai>=1.0.0` - OpenAI API client
- `pydantic>=2.0.0` - Data validation and settings
- `aiohttp>=3.9.0` - Async HTTP client
- `aiofiles>=23.0.0` - Async file operations
- `pyyaml>=6.0` - YAML configuration
- `ddgs>=0.1.0` - DuckDuckGo search
- `trafilatura>=1.6.0` - Content extraction

Development dependencies:
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage reporting
- `pytest-asyncio>=0.21.0` - Async test support
- `ruff>=0.1.6` - Linting and formatting
- `pre-commit>=3.0` - Git hooks

## Project Structure

```
src/websearch_ai/
├── __init__.py           # Package exports
├── cli.py                # Command-line interface
├── config/               # Configuration management
│   ├── settings.py
│   └── config.yaml
├── core/                 # Core pipeline logic
│   ├── models.py
│   └── pipeline.py
├── clients/              # External service clients
│   ├── http.py
│   ├── llm.py
│   └── search.py
├── managers/             # Resource managers
│   ├── cache.py
│   ├── prompts.py
│   └── robots.py
├── filters/              # URL and content filters
│   └── url_filter.py
├── prompts/              # LLM prompt templates
│   └── prompts.yaml
├── tests/                # Test suite
└── docs/                 # Documentation
```

## Examples

See the `src/websearch_ai/examples/` directory for more usage examples.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Davide Palleschi (davide@deepplants.com)

## Changelog

See [CHANGELOG.md](docs/CHANGELOG.md) for version history and updates.
