<div align="center">
  <img src="logo.png" alt="Scrapion Logo" width="200"/>

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

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd scrapion

# Install dependencies
pip install -r requirements.txt

# Or use the pre-built virtualenv
source src-virtualenv/bin/activate
```

## Usage

### As a Library

```python
from scrapion import Client

# Create orchestrator
client = Client()

# Process single URL
report = client.run("https://example.com")
client.output_report("stdio")

# Process search query
report = client.run("python async programming")
client.output_report("file", "./report.json")
```

### As a CLI Tool

```bash
# Output to stdout (JSON)
python3 cli.py "https://example.com" --report stdio
python3 cli.py "rust tutorial" --report stdio

# Save to file
python3 cli.py "machine learning" --report file --output ./results.json
```

## Architecture

### Core Modules

1. **input_handler.py**: Parse and validate user input (URL vs search query)
2. **list_manager.py**: Manage URL lists (main list 1-5, backup list 6-10)
3. **search_engine.py**: DuckDuckGo search with Playwright
4. **web_access.py**: Fetch and convert web content to markdown
5. **report_generator.py**: Generate JSON reports with metadata
6. **client.py**: Main workflow orchestrator (follows CONCEPT.md)

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

## Report Structure

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

See `example.py` for detailed usage examples.

Run examples:
```bash
source src-virtualenv/bin/activate
python3 example.py
```

## Environment Setup

### Using Pre-built Virtualenv

```bash
source src-virtualenv/bin/activate
python3 cli.py "your query" --report stdio
```

### Creating New Virtualenv

```bash
python3 -m venv src-virtualenv
source src-virtualenv/bin/activate
pip install -r requirements.txt
```

## Configuration

Edit relevant modules to customize:
- Search engine (DuckDuckGo)
- Request timeouts
- Extraction rules
- Output formats

## License

See LICENSE file for details.
