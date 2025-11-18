#!/bin/bash
# Run all tests with coverage

set -e

echo "🧪 Running websearch Tests..."
echo "================================"

# Navigate to project root
cd "$(dirname "$0")/.."

# Install test dependencies if needed
if ! python -c "import pytest" 2>/dev/null; then
    echo "📦 Installing test dependencies..."
    pip install -r tests/requirements.txt
fi

# Run tests with coverage
echo ""
echo "Running tests..."
pytest tests/ -v --cov=websearch --cov-report=term-missing --cov-report=html

echo ""
echo "✅ Tests complete!"
echo "📊 Coverage report generated in htmlcov/index.html"

