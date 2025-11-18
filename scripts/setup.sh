#!/usr/bin/env bash
# Setup script to initialize a new project from this template

set -e

echo "🚀 Project Setup Script"
echo "======================"
echo ""

# Get project name
read -p "Enter your project name (lowercase, underscores): " PROJECT_NAME

if [ -z "$PROJECT_NAME" ]; then
    echo "❌ Project name cannot be empty!"
    exit 1
fi

# Validate project name (lowercase, underscores, hyphens only)
if [[ ! "$PROJECT_NAME" =~ ^[a-z0-9_-]+$ ]]; then
    echo "❌ Project name should be lowercase with underscores/hyphens only!"
    exit 1
fi

# Convert to package name (replace hyphens with underscores)
PACKAGE_NAME=$(echo "$PROJECT_NAME" | tr '-' '_')

echo ""
echo "📦 Project name: $PROJECT_NAME"
echo "📦 Package name: $PACKAGE_NAME"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled"
    exit 1
fi

echo ""
echo "🔄 Replacing template_project with $PACKAGE_NAME..."

# Replace in pyproject.toml
if [ -f "pyproject.toml" ]; then
    sed -i.bak "s/template_project/$PACKAGE_NAME/g" pyproject.toml
    rm pyproject.toml.bak
    echo "✅ Updated pyproject.toml"
fi

# Replace in Python files
find . -type f -name "*.py" -not -path "./.git/*" -not -path "./.venv/*" -not -path "./venv/*" | while read -r file; do
    if [ -f "$file" ]; then
        sed -i.bak "s/template_project/$PACKAGE_NAME/g" "$file"
        rm "${file}.bak"
    fi
done
echo "✅ Updated Python files"

# Replace in README.md
if [ -f "README.md" ]; then
    sed -i.bak "s/template_project/$PROJECT_NAME/g" README.md
    sed -i.bak "s/Template Project/$PROJECT_NAME/g" README.md
    rm README.md.bak
    echo "✅ Updated README.md"
fi

# Rename src directory
if [ -d "src/template_project" ]; then
    mv "src/template_project" "src/$PACKAGE_NAME"
    echo "✅ Renamed src/template_project to src/$PACKAGE_NAME"
fi

# Update __init__.py version if needed
if [ -f "src/$PACKAGE_NAME/__init__.py" ]; then
    echo "__version__ = \"0.1.0\"" > "src/$PACKAGE_NAME/__init__.py"
    echo "✅ Updated __init__.py"
fi

# Clean up template files
echo ""
echo "🧹 Cleaning up..."

# Remove setup script itself (optional - comment out if you want to keep it)
# rm scripts/setup.sh

# Remove uv.lock (will be regenerated)
if [ -f "uv.lock" ]; then
    rm uv.lock
    echo "✅ Removed uv.lock (will be regenerated)"
fi

# Ask about git history
echo ""
read -p "Remove git history and start fresh? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf .git
    echo "✅ Removed git history"
    echo ""
    read -p "Initialize new git repo? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        git add .
        git commit -m "Initial commit from template"
        echo "✅ Initialized new git repository"
    fi
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update pyproject.toml with your author info and description"
echo "2. Update README.md with your project details"
echo "3. Run: uv sync --all-extras"
echo "4. Run: uv run pre-commit install"
echo "5. Run: uv run dev-test"
echo ""
echo "Happy coding! 🎉"

