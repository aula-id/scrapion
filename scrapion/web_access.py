# main.py
import asyncio
from pyvirtualdisplay import Display
from playwright.async_api import async_playwright
from markdownify import markdownify as md
import gc

async def get_web_content_as_markdown(url: str) -> str:
        # Use smaller display for better performance
    # display = Display(
    #     visible=False, 
    #     size=(1024, 768),  # Smaller resolution
    #     color_depth=16,    # Reduced color depth
    #     extra_args=['-nocursor']  # Disable cursor for performance
    # )
    # display.start()
        
    """
    Fetches the content of a URL using a stealth-configured headless browser
    and converts the main content to Markdown.

    Args:
        url: The URL of the webpage to read.

    Returns:
        The content of the webpage as a Markdown string.
        Returns an error message if navigation fails.
    """
    try:
        async with async_playwright() as p:
            # Launch a browser. 
            # IMPORTANT: Changed headless=True to headless=False.
            # This opens a visible browser window, which is much less likely
            # to be detected as a bot by services like Cloudflare.
            browser = await p.firefox.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            page = await browser.new_page()

            # Navigate to the URL with a longer timeout to allow for challenges
            await page.goto(url, timeout=90000)

            # Wait for the page to load completely
            await page.wait_for_load_state('networkidle')

            # wait for 0.5 seconds to ensure the page is fully loaded
            await asyncio.sleep(0.2)

            await page.goto(url.replace("view-source:",""), timeout=30000, wait_until='networkidle')

            # Get the full HTML content of the page
            html_content = await page.content()

            # Close the browser
            await browser.close()

            # Convert HTML to Markdown
            markdown_content = md(html_content, heading_style="ATX")

            return markdown_content

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(str(error_message)[:100])
        return error_message
    finally:
        await browser.close()
        gc.collect()  # Force garbage collection


async def test():
    """
    Main function to run the web content reader script.
    """

    # Get the content and print it
    markdown_output = await get_web_content_as_markdown("view-source:https://google.com")

    # Optionally, save to a file
    save_to_file = input("Do you want to save this to a file? (y/n): ").lower()
    if save_to_file == 'y':
        # Create a simple filename from the URL
        filename = "test.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_output)

def sync_run(uri):
    initial_uri = "view-source:"+uri
    return asyncio.run(get_web_content_as_markdown(initial_uri))