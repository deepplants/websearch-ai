# Contributing

Thank you for your interest in contributing to this project!

## Development Setup

1. Fork and clone the repository
2. Install dependencies: `uv sync --all-extras`
3. Install pre-commit hooks: `uv run pre-commit install`
4. Create a branch for your changes: `git checkout -b feature/your-feature`

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Format code with Ruff (run `uv run dev-format`)
- Ensure code passes Ruff checks (run `uv run dev-lint`)

## Testing

- Write tests for all new features
- Ensure all tests pass: `uv run dev-test`
- Aim for high test coverage
- Tests should be in the `tests/` directory

## Commit Messages

- Use clear, descriptive commit messages
- Reference issue numbers if applicable
- Follow conventional commit format when possible

## Pull Requests

1. Ensure all tests pass
2. Update documentation if needed
3. Update `docs/CHANGELOG.md` with your changes
4. Create a clear PR description explaining your changes

## Questions?

Feel free to open an issue for any questions or clarifications.

