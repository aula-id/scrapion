# Installation Guide

## Installation Methods

### 1. Install from Source (Development)

For local development and testing:

```bash
# Clone the repository
git clone <repo-url>
cd scrapion

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Or use the pre-built virtualenv
source src-virtualenv/bin/activate
pip install -e .
```

### 2. Install from Source (Production)

For production use:

```bash
pip install .
```

### 3. Install from PyPI (Future)

Once published to PyPI:

```bash
pip install scrapion
```

## Post-Installation

### Install Playwright Browsers

The package requires Playwright browsers to be installed:

```bash
playwright install
```

### Verify Installation

```bash
# Check CLI is available
scrapion --help

# Test import
python3 -c "from scrapion import Client; print('Success!')"
```

## Usage After Installation

### As a CLI Tool

```bash
# Output to stdout
scrapion "https://example.com" --report stdio

# Save to file
scrapion "python tutorial" --report file --output results.json
```

### As a Python Library

```python
from scrapion import Client

client = Client()
report = client.run("https://example.com")
client.output_report("stdio")
```

## Uninstall

```bash
pip uninstall scrapion
```

## Development Installation

For development with additional tools:

```bash
pip install -e ".[dev]"
```

This installs optional development dependencies:
- pytest (for testing)
- black (for code formatting)
- flake8 (for linting)

## Directory Structure After Installation

```
your-project/
├── venv/                     # Virtual environment
│   └── lib/python3.x/
│       └── site-packages/
│           └── scrapion/      # Installed package
└── your-script.py            # Your code using scrapion
```

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. Virtual environment is activated
2. Package is installed: `pip list | grep scrapion`
3. You're in the correct directory

### Playwright Issues

If Playwright fails:
```bash
playwright install --with-deps
```

### Command Not Found

If `scrapion` command not found:
1. Check virtual environment is activated
2. Reinstall: `pip install --force-reinstall -e .`
3. Check PATH: `which scrapion`

## Building Distribution Packages

### Build wheel and sdist

```bash
pip install build
python -m build
```

This creates:
- `dist/scrapion-0.1.0-py3-none-any.whl` (wheel)
- `dist/scrapion-0.1.0.tar.gz` (source distribution)

### Upload to PyPI (Maintainers Only)

```bash
pip install twine
twine upload dist/*
```
