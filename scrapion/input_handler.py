"""Input validation and parsing module"""

from enum import Enum
from typing import Union


class InputType(Enum):
    """Enum for input types"""
    URL = "url"
    QUERY = "query"


class InputHandler:
    """Handles input parsing and validation"""

    @staticmethod
    def parse_input(raw_input: str) -> tuple[InputType, str]:
        """
        Detect if input is a URL or search query

        Args:
            raw_input: Raw user input string

        Returns:
            Tuple of (InputType, cleaned_input)
        """
        raw_input = raw_input.strip()

        if InputHandler.is_valid_url(raw_input):
            return InputType.URL, raw_input
        else:
            return InputType.QUERY, InputHandler.sanitize_query(raw_input)

    @staticmethod
    def is_valid_url(input_str: str) -> bool:
        """
        Check if input matches URL pattern

        Args:
            input_str: String to check

        Returns:
            True if input starts with http:// or https://
        """
        return input_str.startswith("http://") or input_str.startswith("https://")

    @staticmethod
    def sanitize_query(query: str) -> str:
        """
        Sanitize search query

        Args:
            query: Raw query string

        Returns:
            Sanitized query string
        """
        return query.strip()
