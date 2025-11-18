"""Development scripts for the project."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> None:
    """Run a command and exit on failure."""
    print(f"Running: {description}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        sys.exit(result.returncode)


def test() -> None:
    """Run tests."""
    run_command(["pytest"], "Tests")


def test_cov() -> None:
    """Run tests with coverage."""
    run_command(
        ["pytest", "--cov=websearch_ai", "--cov-report=html", "--cov-report=term-missing"],
        "Tests with coverage",
    )


def lint() -> None:
    """Run linting checks."""
    run_command(["ruff", "check", "."], "Ruff linting")


def format_code() -> None:
    """Format code with Ruff (replaces Black + Isort)."""
    run_command(["ruff", "format", "."], "Ruff formatting")
    run_command(["ruff", "check", "--fix", "."], "Ruff auto-fix")


def clean() -> None:
    """Clean build artifacts."""
    import shutil

    dirs_to_remove = [
        "build",
        "dist",
        ".pytest_cache",
        ".ruff_cache",
        "htmlcov",
    ]
    files_to_remove = [".coverage"]

    for dir_name in dirs_to_remove:
        path = Path(dir_name)
        if path.exists():
            print(f"Removing {dir_name}/")
            shutil.rmtree(path)

    for file_name in files_to_remove:
        path = Path(file_name)
        if path.exists():
            print(f"Removing {file_name}")
            path.unlink()

    # Remove __pycache__ directories
    for pycache in Path(".").rglob("__pycache__"):
        print(f"Removing {pycache}/")
        shutil.rmtree(pycache)

    # Remove .pyc files
    for pyc_file in Path(".").rglob("*.pyc"):
        print(f"Removing {pyc_file}")
        pyc_file.unlink()

    # Remove .egg-info directories
    for egg_info in Path(".").rglob("*.egg-info"):
        if egg_info.is_dir():
            print(f"Removing {egg_info}/")
            shutil.rmtree(egg_info)

    print("Clean complete!")

