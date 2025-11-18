# websearch - Project Structure Reference

<div align="center">

**📚 [Documentation Hub](README.md)** | **🏠 [Main README](../README.md)** | **⚡ [Quick Start](QUICKSTART.md)** | **⚙️ [Config](CONFIG.md)**

</div>

---

## Directory Overview

```
websearch/
├── core/              # Core business logic
├── config/            # Configuration management
├── prompts/           # LLM prompt templates
├── clients/           # External service wrappers
├── managers/          # Resource managers
├── filters/           # Content filters
├── examples/          # Usage examples
└── docs/              # Documentation
```

## Module Responsibilities

### 📦 `core/`
**Purpose**: Core business logic and data models

- `models.py` - Pydantic data models
  - `SearchResult` - Search result with metadata
  - `BetterQueries` - LLM-generated query improvements
- `pipeline.py` - Main orchestration pipeline
  - `WebSearchPipeline` - Coordinates the entire search workflow

### ⚙️ `config/`
**Purpose**: Configuration management

- `settings.py` - Settings class with Pydantic validation
  - `Settings` - All application settings
  - `Settings.from_yaml()` - Load from YAML file
  - `Settings.from_env()` - Load with env overrides
- `config.yaml` - Main configuration file
- `config.example.yaml` - Example configuration template

### 💬 `prompts/`
**Purpose**: LLM prompt templates

- `prompts.yaml` - All LLM prompts
  - `better_queries_prompt`
  - `relevance_filtering_prompt`
  - `summarize_text_prompt`
  - `merge_summaries_prompt`

### 🔌 `clients/`
**Purpose**: External service client wrappers

- `http.py` - HTTP fetcher with rate limiting
  - `HTTPFetcher` - Async HTTP client with politeness
- `llm.py` - OpenAI LLM client
  - `LLMClient` - Text and structured LLM calls
- `search.py` - DuckDuckGo search engine
  - `SearchEngine` - Search query execution

### 🛠️ `managers/`
**Purpose**: Resource and lifecycle management

- `cache.py` - File-based cache manager
  - `CacheManager` - Read/write cached content
- `prompts.py` - Prompt loader and formatter
  - `PromptManager` - Load and format prompts from YAML
- `robots.py` - Robots.txt compliance checker
  - `RobotsChecker` - Check URL permissions

### 🔍 `filters/`
**Purpose**: Content filtering and validation

- `url_filter.py` - Domain-based URL filtering
  - `URLFilter` - Block disallowed domains

### 📖 `examples/`
**Purpose**: Usage examples and demos

- `usage_examples.py` - Comprehensive usage examples
  - Basic usage
  - Custom configuration
  - Fast mode
  - Research mode
  - Custom YAML
  - Domain filtering

### 📚 `docs/`
**Purpose**: Documentation

- `README.md` - Main documentation (this is now in root)
- `README_CONFIG.md` - Configuration guide
- `REFACTORING.md` - Refactoring details
- `CHANGES.md` - Changelog
- `MIGRATION_GUIDE.md` - Migration instructions

## Key Files

### `__init__.py` (root)
Package exports for convenient imports
```python
from websearch import (
    Settings,
    SearchResult,
    BetterQueries,
    WebSearchPipeline,
    # ... more exports
)
```

### `cli.py`
Command-line interface entry point
```bash
python -m websearch.cli "your query"
```

## Import Patterns

### From External Code
```python
# Import main classes
from websearch import Settings, WebSearchPipeline, SearchResult

# Import specific components
from websearch.clients import LLMClient, SearchEngine
from websearch.managers import CacheManager
```

### Within the Package
```python
# From core/ files
from ..config import Settings
from ..clients import HTTPFetcher
from .models import SearchResult

# From config/ files
from .settings import Settings
```

## Design Principles

### 1. Single Responsibility
Each file has one clear purpose:
- `http.py` - HTTP fetching only
- `cache.py` - Caching only
- `url_filter.py` - URL filtering only

### 2. Clear Boundaries
- **core/** - Business logic
- **config/** - Configuration only
- **clients/** - External APIs
- **managers/** - Resource management
- **filters/** - Validation logic

### 3. Minimal Dependencies
- Files depend on abstractions, not implementations
- Most files only import from `config.Settings`
- Clear dependency graph

### 4. Easy Testing
- Each component can be tested independently
- Mock-friendly interfaces
- Dependency injection via constructor

## Dependency Graph

```
cli.py
  └── core.WebSearchPipeline
       ├── config.Settings
       ├── core.models (SearchResult, BetterQueries)
       ├── clients.LLMClient
       ├── clients.SearchEngine
       ├── clients.HTTPFetcher
       ├── managers.CacheManager
       ├── managers.PromptManager
       ├── managers.RobotsChecker
       └── filters.URLFilter
```

## File Size Guidelines

- Most files: 50-150 lines
- Complex files (like pipeline): 200-300 lines
- Config/data files: Any size (YAML, etc.)
- Keep focused and readable

## Adding New Components

### New Client
```python
# clients/new_client.py
from ..config import Settings

class NewClient:
    def __init__(self, settings: Settings):
        self.settings = settings
```

Then add to `clients/__init__.py`:
```python
from .new_client import NewClient
__all__ = [..., "NewClient"]
```

### New Manager
```python
# managers/new_manager.py
class NewManager:
    def __init__(self, config_param: str):
        self.config_param = config_param
```

### New Filter
```python
# filters/new_filter.py
class NewFilter:
    def filter(self, item) -> bool:
        return True  # or False
```

## Best Practices

1. **Type Hints**: Always use type hints
2. **Docstrings**: Add docstrings to classes and public methods
3. **Logging**: Use logging instead of print()
4. **Error Handling**: Handle exceptions gracefully
5. **Async**: Use async/await for I/O operations
6. **Validation**: Use Pydantic for data validation

## Testing Strategy

```bash
# Import test
python -c "from websearch import *"

# Module test
python -m websearch.cli "test query"

# Example test
python websearch/examples/usage_examples.py
```

---

<div align="center">

### 🧭 Navigation

**[📚 Documentation Hub](README.md)** | **[🏠 Main README](../README.md)** | **[⚡ Quick Start](QUICKSTART.md)**

**[🧪 Tests](../tests/README.md)** | **[🛠️ Scripts](../scripts/README.md)** | **[🌐 API](../api/README.md)**

[⚙️ Configuration](CONFIG.md) | [🏗️ Architecture](ARCHITECTURE.md) | [💻 Development](DEVELOPMENT.md)

---

**Related Documentation:**
- [Development Guide](DEVELOPMENT.md) - Contributing to the project
- [Architecture Guide](ARCHITECTURE.md) - System design details
- [API Reference](../api/README.md) - REST API documentation

</div>

---

**Last Updated**: November 2025  
**Structure Version**: 2.1

