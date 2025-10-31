<div align="center">
  <img src="logo.png" alt="Scrapion Logo" width="450"/>

  # Scrapion - Web Scraping Automation System

  A Python library for automated web scraping with intelligent fallback mechanisms and accessibility handling.
</div>

## Features

- **Dual Input Modes**: Accept URLs directly or search queries
- **Smart URL Management**: Automatically split search results into main (1-5) and backup (6-10) lists
- **Intelligent Fallback**: Retry with backup URLs if primary URLs fail
- **Content Extraction**: Uses Playwright for robust web content retrieval
- **Search Integration**: DuckDuckGo search with human-like behavior to evade bot detection
- **Structured Reports**: JSON-formatted reports with success/failure tracking
- **Flexible Output**: Output to stdout or save to file
- **Auto Browser Setup**: Firefox browser automatically installs on first use

## Installation

### From PyPI (Recommended)

```bash
pip install scrapion

# Firefox browser will auto-install on first use
```

### Build from Source

```bash
# Clone the repository
git clone https://github.com/aula-id/scrapion
cd scrapion

# Install in editable mode
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
```

## Usage

### As a Library

```python
from scrapion import Client

# Create client (Firefox auto-installs if needed)
client = Client()

# Process single URL - report object contains all data
report = client.run("https://example.com")

# Access report data directly
print(f"Successful scrapes: {report.successful_scrapes}")
print(f"Results: {report.results}")
print(f"Report dict: {report.to_dict()}")

# Or output to stdout/file
client.output_report("stdio")

# Process search query
report = client.run("python async programming")
client.output_report("file", "./report.json")

# Skip browser check (useful in CI or when browser is pre-installed)
client = Client(skip_browser_check=True)
# Or via environment variable
# SCRAPION_SKIP_BROWSER_CHECK=1 python script.py
```

### As a CLI Tool

```bash
# Output to stdout (JSON)
scrapion "https://example.com" --report stdio
scrapion "rust tutorial" --report stdio

# Save to file
scrapion "machine learning" --report file --output ./results.json
```

## Architecture

### Core Modules

1. **input_handler.py**: Parse and validate user input (URL vs search query)
2. **list_manager.py**: Manage URL lists (main list 1-5, backup list 6-10)
3. **search_engine.py**: DuckDuckGo search with Playwright
4. **web_access.py**: Fetch and convert web content to markdown
5. **report_generator.py**: Generate JSON reports with metadata
6. **orchestrator.py**: Main Client class workflow orchestrator (follows CONCEPT.md)

### Workflow (CONCEPT.md)

```
User Input
    ↓
[Phase 1] Parse Input
    ├→ URL: Single URL mode
    └→ Query: Multi-URL mode

[Phase 2] Search (if query)
    ├→ Execute DuckDuckGo search
    ├→ Extract 10 URLs
    └→ Split into main (1-5) and backup (6-10)

[Phase 3] Scraping Loop
    ├→ Try main list (1-5)
    │  ├→ Success: Report and exit
    │  └→ Failure: Next from main
    └→ Try backup list (6-10)
       ├→ Success: Report and exit
       └→ Failure: Next from backup

[Phase 4] Report Generation
    └→ Compile results and output
```

## Report Object

The `client.run()` method returns a `Report` object with the following attributes:

```python
# Directly access report data
report.query                  # Original input (URL or query)
report.mode                   # "single_url" or "multi_url"
report.successful_scrapes     # Number of successful scrapes
report.failed_scrapes         # Number of failed scrapes
report.results                # List of ScrapeResult objects
report.failed_urls            # List of failed URLs

# Convert to dict or JSON
report.to_dict()              # Returns dictionary
report.to_json()              # Returns JSON string

# Output methods
report.print_to_stdout()      # Print JSON to stdout
report.save_to_file("path")   # Save to JSON file
```

### JSON Structure

```json
{
  "query": "search query or URL",
  "mode": "single_url or multi_url",
  "total_urls_attempted": 10,
  "successful_scrapes": 3,
  "failed_scrapes": 7,
  "results": [
    {
      "url": "https://example.com",
      "status": "success or failed",
      "accessible": true,
      "content": "scraped content...",
      "source": "main_list, backup_list, or single_url",
      "timestamp": "2025-10-31T08:39:07Z"
    }
  ],
  "failed_urls": ["url1", "url2"],
  "generated_at": "2025-10-31T08:39:07Z"
}
```

## Examples

See `example.py` in the source repository for detailed usage examples.

If you've built from source:
```bash
python3 example.py
```

## Configuration

### Browser Setup

Firefox browser is automatically installed on first use. To skip the browser check:

```python
# Skip via constructor parameter
client = Client(skip_browser_check=True)

# Or via environment variable
export SCRAPION_SKIP_BROWSER_CHECK=1
```

### Module Customization

Edit relevant modules to customize:
- Search engine (DuckDuckGo)
- Request timeouts
- Extraction rules
- Output formats

## License

See LICENSE file for details.
