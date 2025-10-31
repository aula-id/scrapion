"""Report generation module"""

import json
from datetime import datetime
from typing import Optional
from pathlib import Path


class ScrapeResult:
    """Single scrape result"""

    def __init__(
        self,
        url: str,
        status: str,
        accessible: bool,
        content: Optional[str] = None,
        source: str = "unknown",
    ):
        self.url = url
        self.status = status
        self.accessible = accessible
        self.content = content
        self.source = source
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "url": self.url,
            "status": self.status,
            "accessible": self.accessible,
            "content": self.content,
            "source": self.source,
            "timestamp": self.timestamp,
        }


class Report:
    """Scraping report"""

    def __init__(self, query: str, mode: str, total_urls: int = 10):
        self.query = query
        self.mode = mode
        self.total_urls_attempted = total_urls
        self.successful_scrapes = 0
        self.failed_scrapes = 0
        self.results = []
        self.failed_urls = []
        self.generated_at = datetime.utcnow().isoformat()

    def add_success(self, url: str, content: str, source: str) -> None:
        """
        Add successful scrape result

        Args:
            url: URL that was scraped
            content: Scraped content
            source: Source of URL (main_list, backup_list, single_url)
        """
        self.successful_scrapes += 1
        result = ScrapeResult(
            url=url,
            status="success",
            accessible=True,
            content=content,
            source=source,
        )
        self.results.append(result)

    def add_failure(self, url: str, source: str = "unknown") -> None:
        """
        Add failed scrape result

        Args:
            url: URL that failed
            source: Source of URL
        """
        self.failed_scrapes += 1
        self.failed_urls.append(url)
        result = ScrapeResult(
            url=url,
            status="failed",
            accessible=False,
            content=None,
            source=source,
        )
        self.results.append(result)

    def to_dict(self) -> dict:
        """Convert report to dictionary"""
        return {
            "query": self.query,
            "mode": self.mode,
            "total_urls_attempted": self.total_urls_attempted,
            "successful_scrapes": self.successful_scrapes,
            "failed_scrapes": self.failed_scrapes,
            "results": [r.to_dict() for r in self.results],
            "failed_urls": self.failed_urls,
            "generated_at": self.generated_at,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert report to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save_to_file(self, filepath: str) -> None:
        """
        Save report to JSON file

        Args:
            filepath: Path to save file
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())
        print(f"Report saved to: {path}")

    def print_to_stdout(self) -> None:
        """Print report to stdout (JSON)"""
        print(self.to_json())
