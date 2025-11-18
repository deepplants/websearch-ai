# Python Project Template

A modern Python 2025+ project template with best practices.

> **📖 Want to use this template?** See [docs/USING_TEMPLATE.md](docs/USING_TEMPLATE.md) for detailed instructions on creating a new project from this template.

## Features

- 🐍 Python 3.12+
- 📦 Modern packaging with `pyproject.toml` and `uv`
- ✅ Testing with `pytest` and coverage
- 🎨 Code formatting and linting with `ruff` (replaces Black, Isort, Flake8)
- 🔒 Pre-commit hooks
- 🚀 CI/CD with GitHub Actions
- 📝 Type hints throughout (checked with Pyright)

## Quick Start (Using This Template)

### Option 1: GitHub Template (Easiest)

1. Click **"Use this template"** on GitHub
2. Create your new repository
3. Clone it and run:
   ```bash
   ./scripts/setup.sh
   ```

### Option 2: Manual Setup

See [docs/USING_TEMPLATE.md](docs/USING_TEMPLATE.md) for complete instructions.

---

## Setup (After Creating Your Project)

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (Python package installer)

### Installation

1. Install dependencies:
```bash
uv sync --all-extras
```

2. Install pre-commit hooks (optional but recommended):
```bash
uv run pre-commit install
```

## Development

### Running Tests

```bash
# Run all tests
uv run dev-test

# Run tests with coverage
uv run dev-test-cov
```

### Code Quality

```bash
# Format code (Ruff replaces Black + Isort)
uv run dev-format

# Run linting
uv run dev-lint

# Clean build artifacts
uv run dev-clean
```

### Available Scripts

All development scripts are defined in `pyproject.toml` and can be run with `uv run`:
- `dev-test` - Run tests
- `dev-test-cov` - Run tests with coverage
- `dev-lint` - Run linting checks (Ruff)
- `dev-format` - Format code (Ruff formatter)
- `dev-clean` - Clean build artifacts

> **Note:** Type checking is handled by Pyright (default in VS Code/Cursor). If you prefer using a Makefile, you can keep the provided `Makefile` as a convenience wrapper. However, all functionality is available through the `pyproject.toml` scripts.

## Project Structure

```
template_project/
├── docs/
│   ├── CHANGELOG.md
│   └── CONTRIBUTING.md
├── src/
│   └── template_project/
│       ├── __init__.py
│       └── main.py
├── scripts/
│   ├── __init__.py
│   ├── __main__.py
│   └── setup.sh
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .pre-commit-config.yaml
├── pyproject.toml
├── pyrightconfig.json
├── README.md
├── LICENSE
└── uv.lock
```

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

Quick start:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`uv run dev-test` and `uv run dev-lint`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
