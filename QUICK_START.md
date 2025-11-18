# Quick Start Guide - WebSearch AI Library

Your package has been successfully converted to an installable library! 🎉

## What Changed?

✅ Package renamed from `websearch-ai` to `websearch_ai` (Python-compatible naming)
✅ All dependencies moved to `pyproject.toml`
✅ CLI entry point configured
✅ Package builds successfully (wheel + source distribution created)
✅ Ready for installation in other projects
✅ Ready for PyPI publishing

## Built Distribution Files

```
dist/
├── websearch_ai-2.0.0-py3-none-any.whl  (57KB) - Wheel distribution
└── websearch_ai-2.0.0.tar.gz            (44KB) - Source distribution
```

## Installation Options

### Option 1: Install Locally for Development
```bash
# In this directory
uv pip install -e .

# Or with pip
pip install -e .
```

### Option 2: Install from Built Wheel
```bash
uv pip install dist/websearch_ai-2.0.0-py3-none-any.whl
```

### Option 3: Install in Another Project
```bash
# From local directory
pip install /path/to/workdir

# From wheel file
pip install /path/to/workdir/dist/websearch_ai-2.0.0-py3-none-any.whl
```

## Usage Examples

### 1. As a Library in Python Code

```python
import asyncio
from websearch_ai import WebSearchPipeline, Settings

async def main():
    # Set your OpenAI API key first:
    # export OPENAI_API_KEY='your-api-key'
    
    settings = Settings.from_env()
    pipeline = WebSearchPipeline(settings)
    
    results, answer = await pipeline.run("What are the latest AI trends?")
    
    print(f"Answer: {answer}")
    print(f"Found {len(results)} sources")

asyncio.run(main())
```

### 2. Using the CLI

```bash
# Set your API key
export OPENAI_API_KEY='your-api-key-here'

# Run a search
websearch-ai "latest nvidia earnings"

# Or using module syntax
python -m websearch_ai.cli "your query here"
```

### 3. Run the Example Script

```bash
export OPENAI_API_KEY='your-api-key'
python example_usage.py "latest AI developments"
```

## Testing the Installation

Run these commands to verify everything works:

```bash
# 1. Check if package is installed
uv pip list | grep websearch-ai

# 2. Test import
python -c "import websearch_ai; print(websearch_ai.__version__)"

# 3. Check CLI
websearch-ai --help || python -m websearch_ai.cli --help
```

## Development Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=websearch_ai --cov-report=html

# Format code
ruff format .

# Lint code
ruff check .

# Build package
uv build

# Clean build artifacts
python -c "import shutil; shutil.rmtree('dist', ignore_errors=True); shutil.rmtree('build', ignore_errors=True)"
```

## Publishing to PyPI

### Step 1: Create PyPI Account
1. Sign up at https://pypi.org
2. Sign up at https://test.pypi.org (for testing)

### Step 2: Install Twine
```bash
uv pip install twine
```

### Step 3: Test on TestPyPI (Recommended)
```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ websearch-ai
```

### Step 4: Publish to PyPI
```bash
# Upload to production PyPI
twine upload dist/*

# Now anyone can install it
pip install websearch-ai
```

## Project Structure

```
websearch-ai/
├── src/websearch_ai/          # Main package (importable as websearch_ai)
│   ├── __init__.py            # Package exports
│   ├── cli.py                 # Command-line interface
│   ├── clients/               # HTTP, LLM, search clients
│   ├── config/                # Configuration & settings
│   ├── core/                  # Pipeline & models
│   ├── filters/               # URL filtering
│   ├── managers/              # Cache, prompts, robots
│   ├── prompts/               # LLM prompts
│   ├── examples/              # Usage examples
│   ├── docs/                  # Documentation
│   ├── scripts/               # Utility scripts
│   └── tests/                 # Test suite
├── dist/                      # Built distributions
├── docs/                      # Project documentation
├── scripts/                   # Development scripts
├── pyproject.toml            # Package configuration
├── MANIFEST.in               # Distribution file includes
├── README.md                 # Main documentation
├── INSTALLATION.md           # Installation guide
├── CONVERSION_SUMMARY.md     # Detailed conversion notes
└── example_usage.py          # Simple usage example
```

## Important Notes

### Package Naming
- **PyPI name:** `websearch-ai` (use for `pip install websearch-ai`)
- **Import name:** `websearch_ai` (use for `import websearch_ai`)
- This is standard practice (like `scikit-learn` → `import sklearn`)

### Python Version
- Requires Python 3.12+

### API Key Required
- OpenAI API key needed for LLM functionality
- Set via: `export OPENAI_API_KEY='your-key'`

## Documentation

- **README.md** - Main documentation with API reference
- **INSTALLATION.md** - Detailed installation instructions
- **CONVERSION_SUMMARY.md** - Technical details of the conversion
- **src/websearch_ai/docs/** - Additional documentation

## Troubleshooting

### CLI Command Not Found
If `websearch-ai` command doesn't work after installation:
```bash
# Use module syntax instead
python -m websearch_ai.cli "your query"
```

### Import Errors
```bash
# Verify installation
pip list | grep websearch-ai

# Reinstall if needed
pip uninstall websearch-ai
pip install -e .
```

### Missing OpenAI API Key
```bash
# Set your API key
export OPENAI_API_KEY='sk-your-key-here'

# Or add to your shell profile
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.bashrc
```

## Next Steps

1. ✅ **Test Locally:** Install and test in a virtual environment
2. ✅ **Update URLs:** Replace placeholder GitHub URLs in `pyproject.toml`
3. ✅ **Test on TestPyPI:** Upload and test before production release
4. ✅ **Create Git Tag:** `git tag -a v2.0.0 -m "Release 2.0.0"`
5. ✅ **Publish to PyPI:** Make it available for everyone
6. ✅ **Create GitHub Release:** Upload distributions and release notes

## Support

- **Email:** davide@deepplants.com
- **Issues:** (Add your GitHub repo URL)

---

**🎉 Your library is ready to use and share!**

For detailed information, see:
- `README.md` - Full documentation
- `INSTALLATION.md` - Installation guide
- `CONVERSION_SUMMARY.md` - Technical details

