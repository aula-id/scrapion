#!/usr/bin/env python3
"""Simple CLI entry point for scrapion library"""

import argparse
import sys
from .orchestrator import Client


def main():
    parser = argparse.ArgumentParser(
        description="Web scraping automation system",
        prog="scrapion",
    )

    parser.add_argument("input", help="Input URL or search query")
    parser.add_argument(
        "--report",
        required=True,
        choices=["stdio", "file"],
        help="Report output destination",
    )
    parser.add_argument("--output", help="Output file path (required when --report file)")

    args = parser.parse_args()

    # Validate arguments
    if args.report == "file" and not args.output:
        parser.error("--output is required when --report is 'file'")

    # Run client
    client = Client()
    report = client.run(args.input)

    # Output report
    client.output_report(args.report, args.output)


if __name__ == "__main__":
    main()
