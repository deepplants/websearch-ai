# Using This Template

This guide explains how to use this template to create a new project.

## Option 1: GitHub Template Repository (Recommended) ⭐

### Step 1: Enable Template Repository

1. Go to your repository on GitHub
2. Click **Settings**
3. Scroll down to **Template repository**
4. Check ✅ **Template repository**
5. Click **Save**

Now users can create new repos from your template with one click!

### Step 2: Create New Project from Template

1. Go to your template repository on GitHub
2. Click **Use this template** → **Create a new repository**
3. Choose a name for your new project
4. Create the repository
5. Clone it locally:
   ```bash
   git clone <your-new-repo-url>
   cd <your-new-project-name>
   ```

### Step 3: Run Setup Script

```bash
# Make setup script executable
chmod +x scripts/setup.sh

# Run setup (will prompt for project name)
./scripts/setup.sh
```

Or manually follow Option 2 steps below.

---

## Option 2: Manual Setup

### Step 1: Clone Template

```bash
git clone <template-repo-url>
cd <template-repo-name>
```

### Step 2: Rename Project

Replace `template_project` with your project name everywhere:

**Files to update:**
1. `pyproject.toml` - Change `name = "template_project"` to your project name
2. `pyproject.toml` - Update `--cov=template_project` to your project name
3. `src/template_project/` - Rename directory to your project name
4. `tests/test_main.py` - Update imports from `template_project` to your name
5. `README.md` - Update all references

**Quick find/replace:**
```bash
# Replace in all files (be careful!)
find . -type f -name "*.py" -o -name "*.toml" -o -name "*.md" | \
  xargs sed -i 's/template_project/YOUR_PROJECT_NAME/g'
```

### Step 3: Update Project Info

1. **pyproject.toml:**
   - Update `name`, `description`, `authors`
   - Update `version` to `0.1.0`

2. **README.md:**
   - Update project name and description
   - Update repository URL

3. **LICENSE:**
   - Update copyright year and name (if needed)

### Step 4: Clean Up

```bash
# Remove template-specific files
rm -rf .git
rm uv.lock  # Will be regenerated

# Initialize new git repo
git init
git add .
git commit -m "Initial commit from template"
```

### Step 5: Setup New Repository

```bash
# Create new repo on GitHub, then:
git remote add origin <your-new-repo-url>
git branch -M main
git push -u origin main
```

---

## Option 3: Automated Setup Script

We provide a setup script to automate the process:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The script will:
1. Ask for your project name
2. Replace all occurrences of `template_project`
3. Update `pyproject.toml` with your info
4. Rename directories
5. Clean up template files
6. Initialize new git repo

---

## What Gets Replaced

The setup process replaces:
- ✅ Package name in `pyproject.toml`
- ✅ Directory name `src/template_project/` → `src/YOUR_NAME/`
- ✅ Import statements in Python files
- ✅ Coverage configuration
- ✅ README references

---

## After Setup

1. **Install dependencies:**
   ```bash
   uv sync --all-extras
   ```

2. **Install pre-commit hooks:**
   ```bash
   uv run pre-commit install
   ```

3. **Run tests:**
   ```bash
   uv run dev-test
   ```

4. **Start coding!** 🚀

---

## Tips

- **Project name format:** Use lowercase with underscores (e.g., `my_awesome_project`)
- **Package name:** Should match the directory name in `src/`
- **Git history:** The template's git history is preserved unless you remove `.git`
- **Customization:** Feel free to modify any files after setup

