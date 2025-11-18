# Installation Guide - WebSearch AI

This guide explains how to install and use the `websearch-ai` library in your projects.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Verifying Installation](#verifying-installation)
- [Quick Start](#quick-start)
- [Publishing to PyPI](#publishing-to-pypi)

## Prerequisites

- Python 3.12 or higher
- pip or uv package manager
- OpenAI API key

## Installation Methods

### 1. Install from Source (Development)

For development or if you want to modify the code:

```bash
# Clone the repository
cd /path/to/workdir

# Install in editable mode with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .

# Install with development dependencies
uv pip install -e ".[dev]"
```

### 2. Install from Built Wheel

If you have the wheel file (`.whl`):

```bash
# Install using uv
uv pip install /path/to/websearch_ai-2.0.0-py3-none-any.whl

# Or using pip
pip install /path/to/websearch_ai-2.0.0-py3-none-any.whl
```

### 3. Install from PyPI (Once Published)

After publishing to PyPI:

```bash
# Using uv
uv pip install websearch-ai

# Or using pip
pip install websearch-ai
```

## Verifying Installation

After installation, verify that the package is correctly installed:

### 1. Check Package Installation

```bash
# Using uv
uv pip list | grep websearch-ai

# Or using pip
pip list | grep websearch-ai
```

### 2. Test Import in Python

```python
python3 -c "import websearch_ai; print(websearch_ai.__version__)"
```

Expected output: `2.0.0`

### 3. Test CLI Command

```bash
# Check if CLI is available
websearch-ai --help
```

Note: If the CLI command is not found, you may need to add the Python scripts directory to your PATH, or use:

```bash
python3 -m websearch_ai.cli "test query"
```

## Quick Start

### 1. Set Up Environment

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# Optional: Set other configuration
export OPENAI_MODEL='gpt-4o-mini'
export LOG_LEVEL='INFO'
```

### 2. Using as a Library

Create a Python script (`test_search.py`):

```python
import asyncio
from websearch_ai import WebSearchPipeline, Settings

async def main():
    # Initialize settings from environment
    settings = Settings.from_env()
    
    # Create pipeline
    pipeline = WebSearchPipeline(settings)
    
    # Run a search
    results, answer = await pipeline.run("What are the latest AI developments?")
    
    # Print results
    print(f"\nFinal Answer:\n{answer}\n")
    print(f"\nFound {len(results)} sources:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   URL: {result.url}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python3 test_search.py
```

### 3. Using the CLI

```bash
# Run a search
websearch-ai "latest nvidia earnings 2025"

# Or using module syntax
python3 -m websearch_ai.cli "your search query here"
```

## Building the Package

If you want to build the package yourself:

```bash
# Install build tools (if not already installed)
uv pip install build

# Build the package
uv build

# The built files will be in the dist/ directory:
# - dist/websearch_ai-2.0.0-py3-none-any.whl (wheel)
# - dist/websearch_ai-2.0.0.tar.gz (source distribution)
```

## Publishing to PyPI

### Prerequisites for Publishing

1. Create accounts on:
   - [PyPI](https://pypi.org/) (production)
   - [TestPyPI](https://test.pypi.org/) (testing)

2. Install twine:
```bash
uv pip install twine
```

### Publish to TestPyPI (Testing)

```bash
# Build the package
uv build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ websearch-ai
```

### Publish to PyPI (Production)

```bash
# Build the package
uv build

# Upload to PyPI
twine upload dist/*

# Now anyone can install it
pip install websearch-ai
```

### Using API Tokens (Recommended)

Instead of username/password, use API tokens:

1. Generate an API token from PyPI/TestPyPI account settings
2. Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
username = __token__
password = pypi-your-test-api-token-here
```

Then upload:

```bash
twine upload dist/*  # Uses credentials from ~/.pypirc
```

## Development Installation

For development with all tools:

```bash
# Install with development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install

# Run tests
pytest

# Run tests with coverage
pytest --cov=websearch_ai --cov-report=html

# Format code
ruff format .

# Lint code
ruff check .

# Fix linting issues automatically
ruff check --fix .
```

## Troubleshooting

### CLI Command Not Found

If `websearch-ai` command is not found after installation:

1. Check if the scripts directory is in your PATH:
```bash
# For uv virtual environment
which websearch-ai
```

2. Use the module syntax instead:
```bash
python3 -m websearch_ai.cli "your query"
```

### Import Errors

If you get import errors:

1. Verify the package is installed:
```bash
pip list | grep websearch-ai
```

2. Check Python path:
```python
import sys
print('\n'.join(sys.path))
```

3. Reinstall the package:
```bash
pip uninstall websearch-ai
pip install -e .
```

### Missing Dependencies

If you get missing dependency errors:

```bash
# Reinstall with dependencies
pip install -e . --force-reinstall
```

## Uninstallation

To remove the package:

```bash
# Using uv
uv pip uninstall websearch-ai

# Or using pip
pip uninstall websearch-ai
```

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/yourusername/websearch-ai/issues
- Email: davide@deepplants.com

## Next Steps

- Read the [README.md](README.md) for features and API reference
- Check the [docs/](src/websearch_ai/docs/) directory for detailed documentation
- See [examples/](src/websearch_ai/examples/) for more usage examples
- Review [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines

