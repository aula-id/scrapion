"""URL list management module"""

from enum import Enum
from typing import Optional


class UrlSource(Enum):
    """Enum for URL source"""
    MAIN_LIST = "main_list"
    BACKUP_LIST = "backup_list"
    SINGLE_URL = "single_url"


class UrlListManager:
    """Manages main (1-5) and backup (6-10) URL lists"""

    def __init__(self, urls: list[str] = None, single_url: Optional[str] = None):
        """
        Initialize list manager

        Args:
            urls: List of URLs to split (max 10)
            single_url: If provided, use single URL mode
        """
        self.main_list = []
        self.backup_list = []
        self.main_index = 0
        self.backup_index = 0
        self.single_url = single_url

        if urls:
            self._split_lists(urls)
        elif single_url:
            self.main_list = [single_url]

    @staticmethod
    def from_urls(urls: list[str]) -> "UrlListManager":
        """Create manager from URL list (search results)"""
        return UrlListManager(urls=urls)

    @staticmethod
    def from_single_url(url: str) -> "UrlListManager":
        """Create manager for single URL mode"""
        return UrlListManager(single_url=url)

    def _split_lists(self, urls: list[str]) -> None:
        """
        Split URLs into main (1-5) and backup (6-10) lists

        Args:
            urls: List of URLs to split
        """
        if len(urls) <= 5:
            self.main_list = urls.copy()
            self.backup_list = []
        else:
            self.main_list = urls[0:5]
            self.backup_list = urls[5:10]

    def get_next_from_main(self) -> Optional[str]:
        """
        Get next URL from main list

        Returns:
            Next URL or None if exhausted
        """
        if self.main_index < len(self.main_list):
            url = self.main_list[self.main_index]
            self.main_index += 1
            return url
        return None

    def get_next_from_backup(self) -> Optional[str]:
        """
        Get next URL from backup list

        Returns:
            Next URL or None if exhausted
        """
        if self.backup_index < len(self.backup_list):
            url = self.backup_list[self.backup_index]
            self.backup_index += 1
            return url
        return None

    def is_from_list(self, url: str) -> bool:
        """
        Check if URL is from list (not single URL mode)

        Args:
            url: URL to check

        Returns:
            True if from list, False if single URL mode
        """
        if self.single_url:
            return self.single_url != url
        return True

    def is_main_exhausted(self) -> bool:
        """Check if main list is exhausted"""
        return self.main_index >= len(self.main_list)

    def is_backup_exhausted(self) -> bool:
        """Check if backup list is exhausted"""
        return self.backup_index >= len(self.backup_list)

    def get_stats(self) -> dict:
        """Get list statistics"""
        return {
            "main_list_size": len(self.main_list),
            "backup_list_size": len(self.backup_list),
            "main_remaining": len(self.main_list) - self.main_index,
            "backup_remaining": len(self.backup_list) - self.backup_index,
        }
