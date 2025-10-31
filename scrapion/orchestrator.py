"""Main orchestration module following CONCEPT.md workflow"""

import asyncio
import json
import os
from typing import Optional

from .input_handler import InputHandler, InputType
from .list_manager import UrlListManager, UrlSource
from .report_generator import Report
from .search_engine import search_initiate_nomarkdown
from .web_access import sync_run
from ._browser_check import ensure_firefox_available


class Client:
    """Main scraping client following CONCEPT.md flow"""

    def __init__(self, skip_browser_check: bool = False):
        """
        Initialize Scrapion client

        Args:
            skip_browser_check: If True, skip Firefox browser check (default: False)
        """
        self.report: Optional[Report] = None
        self.list_manager: Optional[UrlListManager] = None

        # Check Firefox availability unless explicitly skipped or disabled via env var
        if not skip_browser_check and os.getenv("SCRAPION_SKIP_BROWSER_CHECK") != "1":
            ensure_firefox_available()

    def run(self, user_input: str) -> Report:
        """
        Main orchestration flow

        Args:
            user_input: User input (URL or search query)

        Returns:
            Populated Report object
        """
        # Phase 1: Input Processing
        input_type, processed_input = InputHandler.parse_input(user_input)

        if input_type == InputType.URL:
            return self._process_single_url(processed_input)
        else:
            return self._process_search_query(processed_input)

    def _process_single_url(self, url: str) -> Report:
        """
        Process single URL input

        Args:
            url: URL to process

        Returns:
            Report with results
        """
        print(f"[PHASE 1] Single URL mode: {url}")

        # Initialize report and list manager
        self.report = Report(query=url, mode="single_url", total_urls=1)
        self.list_manager = UrlListManager.from_single_url(url)

        # Phase 3: Scraping Loop
        return self._scraping_loop()

    def _process_search_query(self, query: str) -> Report:
        """
        Process search query input

        Args:
            query: Search query

        Returns:
            Report with results
        """
        print(f"[PHASE 1] Multi-URL mode: {query}")

        # Initialize report
        self.report = Report(query=query, mode="multi_url", total_urls=10)

        # Phase 2: Search and List Creation
        print("[PHASE 2] Executing search...")
        urls = self._search_and_extract_urls(query)

        if not urls:
            print("[PHASE 2] No search results found")
            return self.report

        print(f"[PHASE 2] Found {len(urls)} URLs")

        # Initialize list manager
        self.list_manager = UrlListManager.from_urls(urls)
        stats = self.list_manager.get_stats()
        print(f"[PHASE 2] Main list: {stats['main_list_size']}, Backup list: {stats['backup_list_size']}")

        # Phase 3: Scraping Loop
        return self._scraping_loop()

    def _search_and_extract_urls(self, query: str) -> list[str]:
        """
        Execute search and extract URLs

        Args:
            query: Search query

        Returns:
            List of URLs from search results
        """
        try:
            results_json = search_initiate_nomarkdown(query)
            results = json.loads(results_json)

            urls = []
            for result in results:
                if isinstance(result, dict) and "link" in result:
                    urls.append(result["link"])

            return urls[:10]  # Limit to 10 results
        except Exception as e:
            print(f"[SEARCH] Error: {e}")
            return []

    def _scraping_loop(self) -> Report:
        """
        Phase 3: Main scraping loop following CONCEPT.md

        Returns:
            Populated report
        """
        print("[PHASE 3] Starting scraping loop...")

        # Get first URL
        url = self.list_manager.get_next_from_main()

        while url:
            print(f"[SCRAPE] Attempting: {url}")

            try:
                # Scrape content
                content = sync_run(url)

                # Mark success
                source = UrlSource.MAIN_LIST if self.list_manager.is_main_exhausted() else UrlSource.MAIN_LIST
                self.report.add_success(url, content, source.value)
                print(f"[SCRAPE] Success: {url}")

                # Check if from main list
                if self.list_manager.is_from_list(url):
                    # Case A: Accessible + From List → Exit
                    print("[PHASE 3] Content from main list, generating report")
                    break
                else:
                    # Case B: Accessible + NOT From List → Try backup
                    print("[PHASE 3] Content from backup, continuing...")
                    url = self.list_manager.get_next_from_backup()
                    if not url:
                        print("[PHASE 3] Backup exhausted, generating report")
                        break

            except Exception as e:
                print(f"[SCRAPE] Failed: {url} - {e}")

                # Check if from list
                if self.list_manager.is_from_list(url):
                    # Case C: NOT Accessible + From List → Get next from main
                    url = self.list_manager.get_next_from_main()
                    if not url:
                        # Try backup
                        url = self.list_manager.get_next_from_backup()
                        if not url:
                            print("[PHASE 3] All lists exhausted, generating report")
                            break
                else:
                    # Case D: NOT Accessible + NOT From List → Exit
                    print("[PHASE 3] Single URL failed, generating report")
                    self.report.add_failure(url, source=UrlSource.SINGLE_URL.value)
                    break

        print("[PHASE 4] Report generated")
        return self.report

    def output_report(self, report_type: str, output_path: Optional[str] = None) -> None:
        """
        Output report to stdio or file

        Args:
            report_type: "stdio" or "file"
            output_path: Path for file output (required if report_type is "file")
        """
        if not self.report:
            print("No report generated")
            return

        if report_type == "file":
            if not output_path:
                raise ValueError("output_path required when report_type is 'file'")
            self.report.save_to_file(output_path)
        else:
            self.report.print_to_stdout()
