# Troubleshooting Guide

<div align="center">

**📚 [Documentation Hub](README.md)** | **🏠 [Main README](../README.md)** | **⚡ [Quick Start](QUICKSTART.md)** | **⚙️ [Config](CONFIG.md)**

</div>

---

Common issues and their solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Errors](#configuration-errors)
- [API Key Problems](#api-key-problems)
- [Import Errors](#import-errors)
- [Performance Issues](#performance-issues)
- [Network Errors](#network-errors)
- [API Issues](#api-issues)
- [Test Failures](#test-failures)

## Installation Issues

### Dependencies Not Installing

**Problem:** `pip install -r requirements.txt` fails

**Solutions:**
```bash
# Update pip
python -m pip install --upgrade pip

# Install with --no-cache
pip install --no-cache-dir -r requirements.txt

# Try Python 3.11+
python3.11 -m pip install -r requirements.txt
```

### Module Not Found After Installation

**Problem:** `ModuleNotFoundError` after installing

**Solutions:**
```bash
# Ensure you're in the correct directory
cd /path/to/cabbo-tools/servers

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall in development mode
cd websearch
pip install -e .
```

## Configuration Errors

### OPENAI_API_KEY Not Set

**Problem:** `OPENAI_API_KEY is required but not set`

**Solutions:**
```bash
# Set environment variable
export OPENAI_API_KEY="sk-your-key-here"

# Or add to config.yaml
openai:
  api_key: "sk-your-key-here"

# Or add to .bashrc/.zshrc for persistence
echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.bashrc
source ~/.bashrc
```

### Configuration Validation Failed

**Problem:** `Configuration validation failed`

**Solution:**
```bash
# Validate your configuration
python scripts/validate_config.py

# Check for common errors
# - Temperature not 0-2
# - Relevance score not 0-5
# - Missing required fields
```

### Prompts File Not Found

**Problem:** `Prompt configuration missing at prompts/prompts.yaml`

**Solution:**
```bash
# Check if prompts.yaml exists
ls prompts/prompts.yaml

# If missing, restore from version control
git checkout prompts/prompts.yaml

# Or check the path in config
python -c "from websearch import Settings; s = Settings.from_yaml(); print(s.prompts_path)"
```

## API Key Problems

### Invalid API Key

**Problem:** `OpenAI API call failed: Invalid API key`

**Solutions:**
```bash
# Verify key format (starts with sk-)
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Get new key from OpenAI dashboard
# https://platform.openai.com/api-keys
```

### Rate Limit Exceeded

**Problem:** `Rate limit exceeded`

**Solutions:**
```python
# Reduce concurrent requests
settings = Settings(
    openai_api_key="your-key",
    search_num_better_queries=5,  # Reduce queries
    max_concurrent_fetches=10      # Reduce concurrency
)

# Add delays between requests
# Or upgrade OpenAI plan
```

### Insufficient Quota

**Problem:** `You exceeded your current quota`

**Solutions:**
- Check usage at https://platform.openai.com/usage
- Add payment method
- Wait for quota reset
- Use smaller models or fewer tokens

## Import Errors

### Cannot Import websearch

**Problem:** `ModuleNotFoundError: No module named 'websearch'`

**Solutions:**
```bash
# Run from correct directory
cd /path/to/cabbo-tools/servers
python -m websearch.cli "query"

# Or add to Python path
export PYTHONPATH="/path/to/cabbo-tools/servers:$PYTHONPATH"

# Or use absolute imports
import sys
sys.path.insert(0, '/path/to/cabbo-tools/servers')
from websearch import Settings
```

### Import Error in Tests

**Problem:** Tests fail with import errors

**Solutions:**
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run from project root
cd /path/to/cabbo-tools/servers
pytest websearch/tests/
```

## Performance Issues

### Very Slow Searches

**Problem:** Searches take > 2 minutes

**Solutions:**
```python
# Use Fast Mode
settings = Settings(
    openai_api_key="key",
    search_num_better_queries=5,     # Reduce from 10
    search_max_results_per_query=3,  # Reduce from 5
    min_relevance_score=2,           # Lower threshold
    max_concurrent_fetches=30        # Increase concurrency
)

# Enable caching
settings.cache_enabled = True
```

### High Memory Usage

**Problem:** Process using too much memory

**Solutions:**
```yaml
fetching:
  max_content_chars: 5000  # Reduce from 8000
  max_concurrent_fetches: 10  # Reduce from 20

search:
  total_max_results: 8  # Reduce from 12
```

### Cache Growing Too Large

**Problem:** Cache directory is huge

**Solution:**
```bash
# Clear cache
python scripts/clear_cache.py

# Reduce cache usage
cache:
  enabled: false  # Disable if not needed
```

## Network Errors

### Timeout Errors

**Problem:** `asyncio.TimeoutError` or `aiohttp.ClientTimeout`

**Solutions:**
```yaml
fetching:
  fetch_timeout: 60  # Increase from 30
  max_concurrent_fetches: 10  # Reduce concurrency
```

### Connection Refused

**Problem:** `Connection refused` when starting API

**Solutions:**
```bash
# Check if port is already in use
lsof -i :8000

# Use different port
uvicorn websearch.api.main:app --port 8001

# Kill process using port
kill -9 <PID>
```

### SSL Certificate Errors

**Problem:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions:**
```bash
# Update certificates
pip install --upgrade certifi

# Or temporarily disable verification (NOT recommended)
export CURL_CA_BUNDLE=""
```

## API Issues

### API Not Starting

**Problem:** `uvicorn` command not found or fails

**Solutions:**
```bash
# Install API dependencies
pip install -r api/requirements.txt

# Check uvicorn installation
which uvicorn

# Run with python -m
python -m uvicorn websearch.api.main:app --reload
```

### CORS Errors

**Problem:** CORS policy blocking requests

**Solution:**
The API has CORS enabled by default. If issues persist:

```python
# In api/main.py, verify CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 422 Validation Error

**Problem:** `422 Unprocessable Entity`

**Solution:**
Check request format:

```bash
# Correct format
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "your query",
    "min_relevance_score": 3
  }'

# query field is required
# min_relevance_score must be 0-5
```

## Test Failures

### Tests Not Running

**Problem:** `pytest` not found or tests don't run

**Solutions:**
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run from correct directory
cd /path/to/cabbo-tools/servers
pytest websearch/tests/

# Verbose output
pytest websearch/tests/ -v
```

### Async Test Failures

**Problem:** Tests fail with async errors

**Solution:**
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Check pytest.ini or setup.cfg
# Should have: asyncio_mode = auto
```

### Import Errors in Tests

**Problem:** Tests can't import modules

**Solutions:**
```bash
# Ensure proper directory structure
cd /path/to/cabbo-tools/servers
pytest websearch/tests/

# Check conftest.py exists
ls websearch/tests/conftest.py
```

## Getting More Help

### Enable Debug Logging

```python
settings = Settings(
    openai_api_key="key",
    log_level="DEBUG"  # Show detailed logs
)
```

### Check Logs

```bash
# Redirect output to file
python -m websearch.cli "query" 2>&1 | tee debug.log

# API logs
uvicorn websearch.api.main:app --log-level debug
```

### Run Diagnostic Commands

```bash
# Validate configuration
python scripts/validate_config.py

# Test imports
python -c "from websearch import *; print('✓ OK')"

# Check version
python -c "from websearch import __version__; print(__version__)"

# Test API health
curl http://localhost:8000/health
```

---

<div align="center">

### 🧭 Navigation

**[📚 Documentation Hub](README.md)** | **[🏠 Main README](../README.md)** | **[⚡ Quick Start](QUICKSTART.md)**

**[🧪 Tests](../tests/README.md)** | **[🛠️ Scripts](../scripts/README.md)** | **[🌐 API](../api/README.md)**

[⚙️ Configuration](CONFIG.md) | [❓ FAQ](FAQ.md) | [⚡ Performance](PERFORMANCE.md)

---

**Still Having Issues?**
- Check the [FAQ](FAQ.md)
- Review [Configuration Guide](CONFIG.md)
- See [Performance Guide](PERFORMANCE.md)
- Report a bug with detailed logs

</div>

