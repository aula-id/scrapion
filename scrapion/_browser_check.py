"""Browser availability checker for Playwright"""

import subprocess
import sys
from pathlib import Path


def check_firefox_installed() -> bool:
    """Check if Playwright Firefox is installed"""
    home = Path.home()
    playwright_dir = home / ".cache" / "ms-playwright"

    if not playwright_dir.exists():
        return False

    firefox_dirs = list(playwright_dir.glob("firefox-*"))
    return len(firefox_dirs) > 0


def install_firefox_silent() -> bool:
    """Silently install Playwright Firefox browser"""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "playwright", "install", "firefox"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False


def ensure_firefox_available():
    """Ensure Firefox is available, auto-install if needed (fully automatic)"""
    if check_firefox_installed():
        return

    print("Scrapion: Firefox browser not found, installing automatically...")
    if install_firefox_silent():
        print("✓ Firefox installed successfully!")
    else:
        print("✗ Auto-install failed. Please run manually: playwright install firefox")
