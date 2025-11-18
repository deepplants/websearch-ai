# websearch Documentation Hub

> **Complete documentation for the websearch intelligent search pipeline**

Welcome to the comprehensive documentation for websearch v2.1 - a production-ready, modular web search system with LLM-powered summarization.

---

## 📚 Main Documentation

### [📖 Main README](../README.md)
**The primary documentation** - Start here for an overview of the project, features, installation, and basic usage.

### [🎯 Project Overview](../PROJECT_OVERVIEW.md)
**Complete project guide** - Architecture, use cases, deployment options, performance characteristics, and roadmap.

### [📋 Implementation Summary](../IMPLEMENTATION_SUMMARY.md)
**What's new in v2.1** - Detailed summary of tests, scripts, API, and all enhancements.

---

## 🚀 Getting Started

<div style="display: flex; flex-wrap: wrap;">

  <div style="flex: 0 1 300px;">
  
  ### [⚡ Quick Start Guide](QUICKSTART.md)
  Get up and running in 5 minutes with:
  - Installation steps
  - Basic usage examples
  - Configuration options
  - Common use cases
  - Troubleshooting tips

  **Perfect for beginners!**
  </div>

  <div style="flex: 0 1 300px;">
  
  ### [📐 Project Structure](STRUCTURE.md)
  Understand the codebase:
  - Directory organization
  - Module responsibilities
  - Import patterns
  - Design principles
  - Adding new components

  **Perfect for contributors!**
  </div>

</div>

---

## 🔧 Component Documentation

### Core Components

<div style="display: flex; flex-wrap: wrap">

  <div style="flex: 0 1 240px; ">
    
#### [🧪 Tests Documentation](../tests/README.md)
- Running tests
- Test structure
- Writing new tests
- Fixtures and mocking
- Coverage reports

  </div>
  <div style="flex: 0 1 240px; ">

#### [🛠️ Scripts Documentation](../scripts/README.md)
- Utility scripts overview
- Test runner
- Cache management
- Configuration validation
- Performance benchmarking
- Export tools

  </div>
  <div style="flex: 0 1 240px; ">
    
#### [🌐 API Documentation](../api/README.md)
- REST API endpoints
- Request/response formats
- Authentication
- Usage examples
- Deployment guide
- Performance tips

  </div>
  <div style="flex: 0 1 240px; ">
    
#### [📝 Examples](../examples/usage_examples.py)
- Basic usage
- Custom configuration
- Fast mode
- Research mode
- Domain filtering

  </div>
</div>

---

## 📖 Detailed Guides

<div style="display: flex; flex-wrap: wrap">

<div style="flex: 0 1 240px;">
  
#### [⚙️ Configuration Guide](CONFIG.md)
<ul>
  <li>YAML configuration</li>
  <li>Environment variables</li>
  <li>Configuration presets</li>
  <li>Custom settings</li>
  <li>Configuration validation</li>
</ul>

</div>

<div style="flex: 0 1 240px;">

#### [🔧 Advanced Configuration](ADVANCED_CONFIG.md)
<ul>
  <li>LLM settings optimization</li>
  <li>Search parameters tuning</li>
  <li>Cache configuration</li>
  <li>Proxy setup</li>
  <li>Production settings</li>
</ul>

</div>

<div style="flex: 0 1 240px;">

#### [💻 Development Guide](DEVELOPMENT.md)
<ul>
  <li>Development setup</li>
  <li>Code style guidelines</li>
  <li>Adding new features</li>
  <li>Testing strategies</li>
  <li>Pull request process</li>
</ul>

</div>

<div style="flex: 0 1 240px;">

#### [🏗️ Architecture Guide](ARCHITECTURE.md)
<ul>
  <li>System design</li>
  <li>Component interaction</li>
  <li>Data flow</li>
  <li>Pipeline stages</li>
  <li>Extension points</li>
</ul>

</div>

<div style="flex: 0 1 240px;">

#### [🚀 Deployment Guide](DEPLOYMENT.md)
<ul>
  <li>Deployment options</li>
  <li>Docker containers</li>
  <li>Environment setup</li>
  <li>Security considerations</li>
  <li>Monitoring & logging</li>
</ul>

</div>

<div style="flex: 0 1 240px;">

#### [🔐 Security Guide](SECURITY.md)
<ul>
  <li>API key management</li>
  <li>Rate limiting</li>
  <li>Input validation</li>
  <li>CORS configuration</li>
  <li>Production hardening</li>
</ul>

</div>

</div>

---

## [📝 Changelog](CHANGELOG.md)
Version history and changes:
- v2.1.0 - Tests, Scripts, API
- v2.0.0 - Major refactoring
- Previous versions

## 📚 Reference Documentation

### API Reference

- **[REST API](../api/README.md)** - Complete REST API documentation
- **[CLI Reference](CLI.md)** - Command-line interface guide
- **[Python API](PYTHON_API.md)** - Using as a Python library

### Component Reference

- **[Core Module](CORE.md)** - Pipeline and models reference
- **[Clients Module](CLIENTS.md)** - HTTP, LLM, Search clients
- **[Managers Module](MANAGERS.md)** - Cache, prompts, robots
- **[Filters Module](FILTERS.md)** - URL filtering

---

## 🔍 Troubleshooting

### [🐛 Troubleshooting Guide](TROUBLESHOOTING.md)
Common issues and solutions:
- API key errors
- Import problems
- Performance issues
- Configuration errors
- Network issues

### [❓ FAQ](FAQ.md)
Frequently asked questions:
- General questions
- Configuration
- Performance
- API usage
- Deployment

---


## 📝 Quick Reference

### Installation
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
```

### Basic Usage
```python
from websearch import Settings, WebSearchPipeline

settings = Settings.from_yaml()
pipeline = WebSearchPipeline(settings)
results, answer = await pipeline.run("your query")
```

### Start API
```bash
uvicorn websearch.api.main:app --reload
```

### Run Tests
```bash
pytest tests/
```

---

## 🆘 Need Help?

1. **Start with** [Quick Start Guide](QUICKSTART.md)
2. **Check** [Troubleshooting](TROUBLESHOOTING.md)
3. **Read** [FAQ](FAQ.md)
4. **Review** [Main README](../README.md)
5. **Explore** component-specific READMEs

---

## 📞 Support & Contact

- **Documentation**: You're here!
- **Issues**: Report bugs and request features
- **Examples**: See [examples/](../examples/)
- **Tests**: Check [tests/](../tests/) for usage patterns

---

<div align="center">

### Navigation

[🏠 Main README](../README.md) • [⚡ Quick Start](QUICKSTART.md) • [📐 Structure](STRUCTURE.md) • [⚙️ Config](CONFIG.md)

[🧪 Tests](../tests/README.md) • [🛠️ Scripts](../scripts/README.md) • [🌐 API](../api/README.md)

---

**websearch v2.1** | **Status**: ✅ Production Ready | **Last Updated**: November 2025

</div>
