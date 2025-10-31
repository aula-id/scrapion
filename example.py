#!/usr/bin/env python3
"""Example usage of the scrapion library"""

from scrapion import Client


def main():
    # Create client
    client = Client()

    # Example 1: Single URL mode
    print("=" * 60)
    print("Example 1: Single URL Mode")
    print("=" * 60)
    report1 = client.run("https://example.com")
    print("\nReport (stdout):")
    client.output_report("stdio")

    # Example 2: Search query mode
    print("\n" + "=" * 60)
    print("Example 2: Search Query Mode")
    print("=" * 60)
    report2 = client.run("rust programming tutorial")
    print("\nReport (stdout):")
    client.output_report("stdio")

    # Example 3: Save to file
    print("\n" + "=" * 60)
    print("Example 3: Save to File")
    print("=" * 60)
    client.run("python async")
    client.output_report("file", "/tmp/scrapion_report.json")


if __name__ == "__main__":
    main()
