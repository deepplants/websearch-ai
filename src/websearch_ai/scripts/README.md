# Utility Scripts

Collection of utility scripts for the web search pipeline.

<div align="left">

[📚 <b>Documentation Hub</b> &larr;](../docs/README.md)

</div>

## Available Scripts

### 1. Run Tests (`run_tests.sh`)

Run all tests with coverage report.

```bash
bash scripts/run_tests.sh
```

Features:
- Automatically installs test dependencies
- Runs all tests with verbose output
- Generates coverage report
- Creates HTML coverage report in `htmlcov/`

### 2. Clear Cache (`clear_cache.py`)

Clear the cache directory to force fresh fetches.

```bash
# Clear default cache
python scripts/clear_cache.py

# Clear custom cache directory
python scripts/clear_cache.py --cache-dir my_cache
```

Features:
- Shows cache size before deletion
- Counts cached files
- Safely recreates cache directory

### 3. Validate Config (`validate_config.py`)

Validate configuration files for correctness.

```bash
# Validate default config
python scripts/validate_config.py

# Validate custom config
python scripts/validate_config.py --config custom_config.yaml
```

Features:
- Checks all configuration values
- Validates against Pydantic schema
- Verifies file paths exist
- Shows detailed error messages
- Checks API key presence

### 4. Benchmark (`benchmark.py`)

Benchmark different configuration presets.

```bash
# Basic benchmark
python scripts/benchmark.py

# Custom query
python scripts/benchmark.py --query "quantum computing 2025"

# More runs for accuracy
python scripts/benchmark.py --runs 5
```

Features:
- Tests Fast, Balanced, and Quality modes
- Multiple runs for statistical accuracy
- Shows average, min, max times
- Compares result counts
- Identifies fastest configuration

Output example:
```
Fast Mode:
  Average Time: 15.32s
  Range: 14.21s - 16.89s
  Std Dev: 1.12s
  Avg Results: 3.7
```

### 5. Export Results (`export_results.py`)

Export search results to various formats.

```bash
# Export to JSON
python scripts/export_results.py "AI news 2025" --format json --output results.json

# Export to CSV
python scripts/export_results.py "climate change" --format csv --output data.csv

# Export to Markdown
python scripts/export_results.py "web development" --format markdown --output report.md
```

Features:
- Multiple export formats (JSON, CSV, Markdown)
- Includes final answer and all sources
- Preserves all metadata
- UTF-8 encoding for international content

#### Export Formats

**JSON**: Machine-readable, includes all fields
```json
{
  "final_answer": "...",
  "results": [
    {
      "title": "...",
      "url": "...",
      "relevance": 5,
      "summary": "..."
    }
  ]
}
```

**CSV**: Spreadsheet-compatible, easy analysis
```csv
Title,URL,Relevance,Query,Snippet,Summary
"Result 1","https://...","5","query","...","..."
```

**Markdown**: Human-readable, documentation-friendly
```markdown
# Search Results

## Final Answer
...

## Sources
### 1. Result Title
**URL:** https://...
**Summary:** ...
```

## Making Scripts Executable

```bash
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

## Common Workflows

### Before Deployment

```bash
# 1. Validate configuration
python scripts/validate_config.py

# 2. Clear old cache
python scripts/clear_cache.py

# 3. Run tests
bash scripts/run_tests.sh
```

### Performance Tuning

```bash
# 1. Benchmark current config
python scripts/benchmark.py

# 2. Adjust config based on results

# 3. Benchmark again to compare
python scripts/benchmark.py --runs 5
```

### Research Workflow

```bash
# 1. Run search and export results
python scripts/export_results.py "research topic" --format markdown --output report.md

# 2. Review Markdown report

# 3. Export to JSON for further processing
python scripts/export_results.py "research topic" --format json --output data.json
```

## Script Development

### Adding a New Script

1. Create script file in `scripts/`
2. Add shebang: `#!/usr/bin/env python3`
3. Add docstring with usage
4. Add to this README
5. Make executable: `chmod +x scripts/your_script.py`

### Script Template

```python
#!/usr/bin/env python3
"""
Brief description of what the script does.

Usage:
    python scripts/your_script.py [options]
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from websearch import Settings, WebSearchPipeline


def main():
    parser = argparse.ArgumentParser(description="Your script description")
    parser.add_argument("--option", help="Option description")
    
    args = parser.parse_args()
    
    # Your script logic here
    print("✅ Done!")


if __name__ == "__main__":
    main()
```

## Troubleshooting

### Import Errors

Make sure you're running from the correct directory:

```bash
# Run from servers/ directory
cd /path/to/cabbo-tools/servers
python websearch/scripts/script_name.py
```

### Permission Errors (Shell Scripts)

```bash
chmod +x scripts/*.sh
```

### Cache Errors

If cache clearing fails, manually delete:

```bash
rm -rf cache_async/*
```

---

**Status**: ✅ All scripts tested and working  
**Last Updated**: November 2025

