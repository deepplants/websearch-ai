# Tests for websearch

<div align="left">

[📚 <b>Documentation Hub</b> &larr;](../docs/README.md)

</div>


Comprehensive unit and integration tests for the web search pipeline.

## Running Tests

### Install Test Dependencies

```bash
pip install -r tests/requirements.txt
```

### Run All Tests

```bash
# From project root
pytest tests/

# With coverage report
pytest tests/ --cov=websearch --cov-report=html

# Verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::TestSearchResult::test_create_search_result
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_models.py           # Tests for data models
├── test_settings.py         # Tests for configuration
├── test_url_filter.py       # Tests for URL filtering
├── test_cache_manager.py    # Tests for cache management
├── test_prompt_manager.py   # Tests for prompt management
└── test_integration.py      # Integration tests for pipeline
```

## Test Coverage

<div style="display: flex; flex-wrap: wrap; gap: 1.5em;">

  <div style="flex: 0 1 300px;">
    <h4>🧩 Models</h4>
    <code>test_models.py</code>
    <p>
    <ul>
      <li>✅ SearchResult creation and validation</li>
      <li>✅ BetterQueries creation and validation</li>
      <li>✅ Model serialization (to_dict)</li>
    </ul>
  </div>

  <div style="flex: 0 0 300px;">
    <h4>⚙️ Settings</h4><code>test_settings.py</code>
    <p>
    <ul>
      <li>✅ Settings creation with defaults</li>
      <li>✅ Settings with custom values</li>
      <li>✅ Validation (temperature, relevance score)</li>
      <li>✅ YAML loading with environment overrides</li>
    </ul>
  </div>

  <div style="flex: 0 0 300px;">
    <h4>🔎 URL Filter</h4>  <code>test_url_filter.py</code>
    <p>
    <ul>
      <li>✅ Allowed and disallowed URLs</li>
      <li>✅ Subdomain matching</li>
      <li>✅ Case-insensitive matching</li>
      <li>✅ Invalid URL handling</li>
    </ul>
  </div>

  <div style="flex: 0 0 300px;">
    <h4>🗄️ Cache Manager </h4> <code>test_cache_manager.py</code>
    <p>
    <ul>
      <li>✅ Cache creation</li>
      <li>✅ Write and read operations</li>
      <li>✅ Multiple URL caching</li>
      <li>✅ Cache overwrites</li>
    </ul>
  </div>

  <div style="flex: 0 0 300px;">
    <h4>📝 Prompt Manager </h4> <code>test_prompt_manager.py</code>
    <p>
    <ul>
      <li>✅ Loading prompts from YAML</li>
      <li>✅ Getting specific prompts</li>
      <li>✅ Formatting prompts with values</li>
      <li>✅ Brace escaping in values</li>
    </ul>
  </div>

  <div style="flex: 0 0 300px;">
    <h4>🔗 Integration </h4> <code>test_integration.py</code>
    <p>
    <ul>
      <li>✅ Pipeline initialization</li>
      <li>✅ Better query generation</li>
      <li>✅ Search execution</li>
      <li>✅ URL filtering during search</li>
    </ul>
  </div>

</div>

## Fixtures

Common fixtures available in `conftest.py`:

- `temp_cache_dir` - Temporary cache directory
- `temp_config_dir` - Temporary config directory
- `mock_settings` - Mock Settings object
- `sample_search_results` - Sample SearchResult objects
- `mock_prompts_yaml` - Mock prompts.yaml file

## Writing New Tests

### Example Unit Test

```python
import pytest
from websearch.your_module import YourClass

class TestYourClass:
    """Tests for YourClass."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        obj = YourClass()
        assert obj.method() == expected_value
    
    @pytest.mark.asyncio
    async def test_async_method(self):
        """Test async method."""
        obj = YourClass()
        result = await obj.async_method()
        assert result is not None
```

### Example Integration Test

```python
@pytest.mark.asyncio
async def test_full_pipeline(mock_settings):
    """Test full pipeline integration."""
    pipeline = WebSearchPipeline(mock_settings)
    
    with patch('module.ExternalDependency'):
        results, answer = await pipeline.run("test query")
        assert len(results) > 0
        assert answer != ""
```

## Mocking External Services

Tests mock external services to avoid actual API calls:

```python
from unittest.mock import Mock, AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mocked_llm(self):
    """Test with mocked LLM client."""
    with patch('websearch.clients.LLMClient') as mock_llm:
        mock_llm.return_value.call_text = AsyncMock(return_value="response")
        # Your test code here
```

## Test Best Practices

1. **Isolation**: Each test should be independent
2. **Mocking**: Mock external services (APIs, network calls)
3. **Fixtures**: Use fixtures for common setup
4. **Async**: Use `@pytest.mark.asyncio` for async tests
5. **Coverage**: Aim for >80% code coverage
6. **Clear Names**: Test names should describe what they test

## CI/CD Integration

Add to your CI pipeline:

```yaml
# .github/workflows/tests.yml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r tests/requirements.txt
    pytest tests/ --cov=websearch --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Troubleshooting

### Import Errors

```bash
# Make sure you're in the correct directory
cd /path/to/cabbo-tools/servers
pytest websearch/tests/
```

### Async Test Warnings

If you see warnings about async tests, make sure pytest-asyncio is installed:

```bash
pip install pytest-asyncio
```

### Cache Directory Errors

Tests use temporary directories via `tmp_path` fixture, which is automatically cleaned up.

---

**Test Status**: ✅ All tests passing  
**Coverage**: Unit + Integration tests  
**Last Updated**: November 2025

