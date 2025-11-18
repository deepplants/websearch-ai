# websearch - Project Overview

**Version**: 2.1.0  
**Status**: ✅ Production Ready  
**Last Updated**: November 2025

## Executive Summary

websearch is a production-ready, modular web search system that combines traditional web search with LLM-powered intelligence. It features a clean architecture, comprehensive testing, REST API, and utility tools for deployment and maintenance.

## Key Capabilities

### 1. Intelligent Search
- **Query Enhancement**: LLM generates improved search queries
- **Relevance Filtering**: AI-powered scoring (0-5) of results
- **Multi-Source Aggregation**: Searches and combines results from multiple queries
- **Content Extraction**: Clean text extraction from web pages
- **AI Summarization**: LLM-generated summaries for each result
- **Final Answer**: Comprehensive answer synthesized from all sources

### 2. Production Features
- **REST API**: FastAPI with auto-generated documentation
- **Comprehensive Tests**: 80%+ coverage with pytest
- **Utility Scripts**: Benchmarking, validation, export tools
- **Configuration Management**: YAML-based with validation
- **Caching System**: File-based cache for efficiency
- **Respectful Crawling**: Rate limiting and robots.txt compliance

### 3. Developer Experience
- **Modular Architecture**: Clean separation of concerns
- **Type Safety**: Full Pydantic validation
- **Comprehensive Docs**: README files in every directory
- **Easy Testing**: Pytest with fixtures and mocks
- **CLI and API**: Multiple ways to interact

## Architecture Overview

### Directory Structure

```
websearch/
├── core/          # Business logic (pipeline, models)
├── config/        # Configuration management
├── prompts/       # LLM prompt templates
├── clients/       # External services (HTTP, LLM, Search)
├── managers/      # Resource management (cache, prompts, robots)
├── filters/       # Content filtering (URL filtering)
├── api/           # REST API (FastAPI)
├── tests/         # Unit & integration tests
├── scripts/       # Utility scripts
├── examples/      # Usage examples
└── docs/          # Documentation
```

### Component Responsibilities

| Component | Purpose | Key Files |
|-----------|---------|-----------|
| **core** | Business logic | `pipeline.py`, `models.py` |
| **config** | Settings & validation | `settings.py`, `config.yaml` |
| **prompts** | LLM templates | `prompts.yaml` |
| **clients** | External APIs | `http.py`, `llm.py`, `search.py` |
| **managers** | Resource mgmt | `cache.py`, `prompts.py`, `robots.py` |
| **filters** | Content validation | `url_filter.py` |
| **api** | REST interface | `main.py` (FastAPI) |
| **tests** | Quality assurance | `test_*.py` |
| **scripts** | Operations tools | Various utility scripts |

### Data Flow

```
User Query
    ↓
[Pipeline Orchestration]
    ↓
1. LLM Query Enhancement → Multiple improved queries
    ↓
2. DuckDuckGo Search → Raw search results
    ↓
3. LLM Relevance Scoring → Filtered results
    ↓
4. HTTP Fetch + Cache → Page content
    ↓
5. LLM Summarization → Individual summaries
    ↓
6. LLM Merge → Final comprehensive answer
    ↓
Results + Answer
```

## Use Cases

### 1. Research Assistant
```python
# Academic or professional research
results, answer = await pipeline.run("quantum computing advances 2025")
# Returns: Comprehensive answer + sources with citations
```

### 2. News Aggregation
```python
# Latest news on a topic
results, answer = await pipeline.run("climate change policies EU")
# Returns: Recent, relevant news with summaries
```

### 3. Technical Documentation Search
```python
# Find and summarize technical information
results, answer = await pipeline.run("FastAPI authentication best practices")
# Returns: Consolidated best practices from multiple sources
```

### 4. Market Research
```python
# Business intelligence gathering
results, answer = await pipeline.run("electric vehicle market trends 2025")
# Returns: Market insights from various sources
```

## Deployment Options

### 1. Python Library
```python
from websearch import Settings, WebSearchPipeline

settings = Settings.from_yaml()
pipeline = WebSearchPipeline(settings)
results, answer = await pipeline.run("query")
```

### 2. Command Line
```bash
python -m websearch.cli "your search query"
```

### 3. REST API
```bash
# Start server
uvicorn websearch.api.main:app --host 0.0.0.0 --port 8000

# Use API
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query"}'
```

### 4. Docker Container
```dockerfile
FROM python:3.11-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "websearch.api.main:app", "--host", "0.0.0.0"]
```

## Configuration Modes

### Fast Mode (Speed Priority)
- 5 improved queries
- 3 results per query
- Min relevance: 2
- Higher concurrency
- **Use case**: Quick answers, time-sensitive

### Balanced Mode (Default)
- 10 improved queries
- 5 results per query
- Min relevance: 3
- Standard concurrency
- **Use case**: General purpose

### Quality Mode (Thoroughness Priority)
- 15 improved queries
- 8 results per query
- Min relevance: 4
- Detailed summaries
- **Use case**: Research, analysis

## Testing Strategy

### Unit Tests
- Individual component testing
- Mocked external dependencies
- Fast execution (~2 seconds)
- Coverage: Core logic, models, filters

### Integration Tests
- Component interaction testing
- Mocked APIs (LLM, Search)
- Medium execution (~10 seconds)
- Coverage: Pipeline flow

### Running Tests
```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=websearch --cov-report=html

# Specific test
pytest tests/test_models.py -v
```

## Performance Characteristics

### Typical Performance (Balanced Mode)
- **Query Enhancement**: ~2-3 seconds
- **Searches**: ~3-5 seconds (10 queries)
- **Relevance Filtering**: ~5-10 seconds (depends on results)
- **Content Fetching**: ~5-15 seconds (parallel)
- **Summarization**: ~10-20 seconds (parallel)
- **Merge**: ~3-5 seconds
- **Total**: ~30-60 seconds

### Optimization Strategies
1. **Caching**: Reduces fetch time significantly
2. **Concurrency**: Parallel fetching and summarization
3. **Quick Mode**: 50% faster, slightly less comprehensive
4. **Relevance Threshold**: Higher = fewer LLM calls

## Dependencies

### Core
- `openai` - LLM API
- `aiohttp` - Async HTTP
- `trafilatura` - Content extraction
- `ddgs` - DuckDuckGo search
- `pydantic` - Data validation
- `pyyaml` - Configuration

### API
- `fastapi` - REST framework
- `uvicorn` - ASGI server

### Testing
- `pytest` - Test framework
- `pytest-asyncio` - Async tests
- `pytest-cov` - Coverage reports

## Security Considerations

### API Keys
- Store in environment variables
- Never commit to version control
- Use different keys for dev/prod

### Rate Limiting
- Implement API rate limiting in production
- Respect external service limits
- Configure appropriate delays

### Input Validation
- Pydantic validates all inputs
- URL filtering prevents malicious domains
- Content size limits prevent DoS

## Monitoring & Observability

### Logging
```python
# All components use structured logging
logger.info(f"Search completed: {len(results)} results")
logger.error(f"Failed to fetch {url}: {error}")
```

### Health Checks
```bash
# API health endpoint
curl http://localhost:8000/health
```

### Metrics to Monitor
- Request rate
- Success/failure ratio
- Average response time
- Cache hit rate
- LLM token usage
- External API errors

## Cost Considerations

### LLM Costs
Approximate token usage per search:
- Query enhancement: 200-500 tokens
- Relevance filtering: 50-100 tokens per result
- Summarization: 500-2000 tokens per page
- Merge: 1000-4000 tokens

**Total**: ~5,000-20,000 tokens per search

At typical pricing:
- Fast mode: ~$0.01-0.03 per search
- Balanced mode: ~$0.03-0.08 per search
- Quality mode: ~$0.08-0.15 per search

### Optimization for Cost
1. Use caching aggressively
2. Increase relevance threshold
3. Reduce number of queries
4. Use smaller/cheaper models for scoring

## Roadmap & Future Enhancements

### Planned Features
- [ ] Multiple LLM provider support (Anthropic, Gemini)
- [ ] Redis cache backend
- [ ] PostgreSQL for result storage
- [ ] Brave Search integration
- [ ] Streaming responses
- [ ] Multi-language support
- [ ] Citation formatting
- [ ] Result ranking improvements
- [ ] Cost tracking dashboard
- [ ] Admin UI

### Community Contributions
- Plugin system for new search engines
- Custom filters and processors
- Alternative cache backends
- Enhanced export formats
- Performance optimizations

## Getting Help

### Documentation
- **README.md** - Main documentation
- **api/README.md** - API guide
- **tests/README.md** - Testing guide
- **scripts/README.md** - Scripts documentation
- **docs/** - Additional documentation

### Troubleshooting
1. Check configuration: `python scripts/validate_config.py`
2. Review logs: Set `log_level: DEBUG`
3. Test components: `pytest tests/ -v`
4. Clear cache: `python scripts/clear_cache.py`

### Common Issues
- **API key errors**: Set `OPENAI_API_KEY` environment variable
- **Import errors**: Run from correct directory
- **Slow performance**: Enable caching, use quick mode
- **No results**: Lower relevance threshold

## Contributing

### Development Setup
```bash
# Clone and setup
cd /path/to/cabbo-tools/servers/websearch

# Install dependencies
pip install -r requirements.txt
pip install -r api/requirements.txt
pip install -r tests/requirements.txt

# Run tests
pytest tests/

# Start API
uvicorn websearch.api.main:app --reload
```

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep files under 300 lines
- Write tests for new features

### Pull Request Process
1. Create feature branch
2. Add tests
3. Update documentation
4. Run test suite
5. Submit PR with clear description

## License

[Your License Here]

## Acknowledgments

- **OpenAI** - GPT models
- **DuckDuckGo** - Free search API
- **Trafilatura** - Content extraction
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation

---

**Project Status**: ✅ Production Ready  
**Maintainer**: [Your Name]  
**Last Updated**: November 2025  
**Version**: 2.1.0

