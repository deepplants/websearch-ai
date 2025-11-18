"""Tests for main module."""

from template_project.main import hello


def test_hello_default() -> None:
    """Test hello function with default argument."""
    assert hello() == "Hello, World!"


def test_hello_custom() -> None:
    """Test hello function with custom name."""
    assert hello("Alice") == "Hello, Alice!"


def test_hello_empty_string() -> None:
    """Test hello function with empty string."""
    assert hello("") == "Hello, !"

