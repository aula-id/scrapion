import asyncio
import random
import os
import gc
from pyvirtualdisplay import Display
from playwright.async_api import async_playwright
from fake_useragent import UserAgent

async def search_duckduckgo(query: str, pages_to_navigate: int = 1, markdowned=True):
    """
    Simplified DuckDuckGo search without proxies - most reliable approach
    """
    # display = Display(
    #     visible=False, 
    #     size=(480, 320),  # Smaller resolution
    #     color_depth=12,    # Reduced color depth
    #     bgcolor='white',  # Set background color to white
    #     # use other than Xvfb
    #     backend='xvfb',   # Use Xvfb for virtual display
    #     extra_args=['-nocursor']  # Disable cursor for performance
    # )
    # display.start()
    os.makedirs("screenshots", exist_ok=True)
    ua = UserAgent(browsers=['firefox'])
    all_results = []
    screenshot_counter = 1
    
    async with async_playwright() as p:
        # Simple, reliable browser configuration
        browser = await p.firefox.launch(
            headless=True,  # Set to True for server
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--start-maximized'
            ]
        )
        
        try:
            page = await browser.new_page(no_viewport=True)
            
            # Basic stealth setup
            await page.set_extra_http_headers({
                'User-Agent': ua.random,
                'Accept-Language': 'en-US,en;q=0.9'
            })
        
            # Remove webdriver property (simple stealth)
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            try:
                print(f"Navigating to DuckDuckGo HTML interface...")
                random_fbid = random.randint(1000000000, 9999999999)
                await page.goto("https://html.duckduckgo.com/html?fbid=" + str(random_fbid), timeout=90000)
                
                
                # Screenshot 1: Initial page load
                # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_initial_page_load.png")
                print(f"Screenshot {screenshot_counter}: Initial page loaded")
                screenshot_counter += 1
                
                # Wait for the search input to be available
                await page.wait_for_selector("#search_form_input_homepage")
                
                print(f"Searching for: {query}")
                
                # Screenshot 2: Before typing
                # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_before_typing.png")
                print(f"Screenshot {screenshot_counter}: Before typing query")
                screenshot_counter += 1
                
                # Human-like typing with delays
                search_input = await page.query_selector("#search_form_input_homepage")
                await search_input.click()
                await asyncio.sleep(random.uniform(0.5, 1))
                
                # Type with human-like delays between characters
                for char in query:
                    await page.keyboard.type(char)
                    await asyncio.sleep(random.uniform(0.005, 0.07))
                
                # Screenshot 3: After typing
                # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_after_typing.png")
                print(f"Screenshot {screenshot_counter}: After typing '{query}'")
                screenshot_counter += 1
                
                # Random delay before pressing Enter
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                # Submit the search
                await page.keyboard.press("Enter")
                
                # Wait for results to load
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(random.uniform(0.5, 1))
                
                # Screenshot 4: Search results loaded
                # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_search_results_loaded.png")
                print(f"Screenshot {screenshot_counter}: Search results loaded")
                screenshot_counter += 1
                
                print("Search results loaded")
                
                # Extract and print some results from first page
                page_results = await extract_results(page, 1)
                all_results.extend(page_results)
                
                # Navigate through additional pages
                for i in range(pages_to_navigate-1):
                    try:
                        print(f"\nNavigating to page {i + 2}...")
                        
                        # Human-like delay before navigation
                        await asyncio.sleep(random.uniform(2, 4))
                        
                        # Screenshot: Before looking for next button
                        # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_before_next_page_{i+2}.png")
                        print(f"Screenshot {screenshot_counter}: Before looking for next page button")
                        screenshot_counter += 1
                        
                        # Look for nav-link with submit input (next page button)
                        nav_links = await page.query_selector_all(".nav-link")
                        next_button = None
                        
                        for link in nav_links:
                            submit_input = await link.query_selector("input[type='submit']")
                            if submit_input:
                                # Check if it's likely a "Next" button
                                value = await submit_input.get_attribute("value")
                                if value and ("next" in value.lower() or ">" in value):
                                    next_button = submit_input
                                    break
                        
                        if next_button:
                            # Highlight the next button for visibility
                            await page.evaluate("(element) => element.style.border = '3px solid red'", next_button)
                            
                            # Screenshot: Next button found and highlighted
                            # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_next_button_found_{i+2}.png")
                            print(f"Screenshot {screenshot_counter}: Next button found and highlighted")
                            screenshot_counter += 1
                            
                            # Human-like delay before clicking
                            await asyncio.sleep(random.uniform(0.5, 1.5))
                            
                            await next_button.click()
                            await page.wait_for_load_state("networkidle")
                            
                            # Human-like delay after page load
                            await asyncio.sleep(random.uniform(0.02, 0.3))
                            
                            # Screenshot: After clicking next page
                            # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_page_{i+2}_loaded.png")
                            print(f"Screenshot {screenshot_counter}: Page {i+2} loaded")
                            screenshot_counter += 1
                            
                            page_results = await extract_results(page, i + 2)
                            all_results.extend(page_results)
                        else:
                            # Screenshot: No next button found
                            # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_no_more_pages.png")
                            print(f"Screenshot {screenshot_counter}: No more pages available")
                            screenshot_counter += 1
                            print("No more pages available")
                            break
                            
                    except Exception as e:
                        # Screenshot: Error occurred
                        # await page.screenshot(path=f"screenshots/duckduck_{screenshot_counter:02d}_error_page_{i+2}.png")
                        print(f"Screenshot {screenshot_counter}: Error occurred")
                        screenshot_counter += 1
                        print(f"Error navigating to page {i + 2}: {e}")
                        break
                        
            except Exception as e:
                print(f"Error during search: {e}")
            
        except Exception as e:
            print(f"Error during search: {e}")

        finally:
            await browser.close()
            # display.stop()
            gc.collect()  # Force garbage collection
    
    # Format results as markdown string instead of returning list
    if not all_results:
        return "No search results found."
    if markdowned:
        markdown_results = []
        for i, result in enumerate(all_results, 1):
            title = result['title']
            link = result['link']
            snippet = result['snippet']
            
            # Ensure UTF-8 encoding for markdown output
            title_safe = title.encode('utf-8', errors='ignore').decode('utf-8')
            snippet_safe = snippet.encode('utf-8', errors='ignore').decode('utf-8')
            
            markdown_result = f"## {i}. [{title_safe}]({link})\n\n{snippet_safe}\n"
            markdown_results.append(markdown_result)
        
        return "\n".join(markdown_results)
    
    return all_results

async def extract_results(page, page_num: int):
    """
    Extract search results with title, link, and snippet from current page
    
    Returns:
        List of dictionaries with keys: title, link, snippet, page_number, position
    """
    results = []
    
    try:
        # Wait a bit for content to stabilize
        await asyncio.sleep(1)
        
        # Find all result containers - using the main result body containers
        result_containers = await page.query_selector_all(".result__body")
        
        # print(f"\n--- Page {page_num} Results ---")
        
        for i, container in enumerate(result_containers, 1):
            try:
                # Extract title and main link
                title_element = await container.query_selector("h2.result__title a.result__a")
                title = ""
                main_link = ""
                
                if title_element:
                    title = await title_element.text_content()
                    main_link = await title_element.get_attribute("href")
                    title = title.strip().encode('utf-8', errors='ignore').decode('utf-8') if title else ""
                
                # Extract snippet
                snippet_element = await container.query_selector("a.result__snippet")
                snippet = ""
                
                if snippet_element:
                    snippet = await snippet_element.text_content()
                    snippet = snippet.strip().encode('utf-8', errors='ignore').decode('utf-8') if snippet else ""
                
                # Only add if we have at least a title
                if title:
                    result_data = {
                        "title": title,
                        "link": main_link,
                        "snippet": snippet,
                        "page_number": page_num,
                        "position": i
                    }
                    
                    results.append(result_data)
                    
                    # Print result for immediate feedback
                    print(f"{i}. {title.encode('utf-8', errors='ignore').decode('utf-8')}")
                    print(f"   URL: {main_link}")
                    print(f"   Snippet: {snippet[:100].encode('utf-8', errors='ignore').decode('utf-8')}{'...' if len(snippet) > 100 else ''}")
                    print()
                    
            except Exception as e:
                print(f"Error extracting result {i}: {e}")
                continue
        
        print(f"Successfully extracted {len(results)} results from page {page_num}")
        
    except Exception as e:
        print(f"Error extracting results from page {page_num}: {e}")
    
    return results

def search_initiate(query: str):
    """
    Initiates the DuckDuckGo search process
    Returns markdown formatted search results
    """
    print(f"[SEARCH] Starting search for: {query}")
    
    try:
        # Always use asyncio.run to avoid event loop conflicts
        print("[SEARCH] Using asyncio.run for clean event loop")
        return asyncio.run(search_duckduckgo(query, 1))
    except Exception as e:
        print(f"[SEARCH] asyncio.run failed: {e}")
        
        # Fallback: Try with new event loop in current thread
        try:
            print("[SEARCH] Trying new event loop in current thread")
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(search_duckduckgo(query, 1))
                return result
            finally:
                new_loop.close()
                asyncio.set_event_loop(None)
        except Exception as e2:
            print(f"[SEARCH] New event loop failed: {e2}")
            
            # Final fallback: Use thread executor
            try:
                print("[SEARCH] Using ThreadPoolExecutor as final fallback")
                import concurrent.futures
                
                def run_in_thread():
                    # Create completely isolated event loop in new thread
                    thread_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(thread_loop)
                    try:
                        return thread_loop.run_until_complete(search_duckduckgo(query, 1))
                    finally:
                        thread_loop.close()
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_in_thread)
                    return future.result(timeout=60)  # 60 second timeout
            except Exception as e3:
                print(f"[SEARCH] All methods failed: {e3}")
                return f"Search failed: {str(e3)}"
            

def search_initiate_nomarkdown(query: str):
    """
    Initiates the DuckDuckGo search process
    Returns non-markdown formatted search results as JSON string
    """
    import json
    print(f"[SEARCH] Starting search for: {query}")
    
    try:
        # Always use asyncio.run to avoid event loop conflicts
        print("[SEARCH] Using asyncio.run for clean event loop")
        results = asyncio.run(search_duckduckgo(query, 1, False))
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        print(f"[SEARCH] asyncio.run failed: {e}")
        
        # Fallback: Try with new event loop in current thread
        try:
            print("[SEARCH] Trying new event loop in current thread")
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(search_duckduckgo(query, 1, False))
                return json.dumps(result, ensure_ascii=False)
            finally:
                new_loop.close()
                asyncio.set_event_loop(None)
        except Exception as e2:
            print(f"[SEARCH] New event loop failed: {e2}")
            
            # Final fallback: Use thread executor
            try:
                print("[SEARCH] Using ThreadPoolExecutor as final fallback")
                import concurrent.futures
                
                def run_in_thread():
                    # Create completely isolated event loop in new thread
                    thread_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(thread_loop)
                    try:
                        return thread_loop.run_until_complete(search_duckduckgo(query, 1, False))
                    finally:
                        thread_loop.close()
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_in_thread)
                    result = future.result(timeout=60)  # 60 second timeout
                    return json.dumps(result, ensure_ascii=False)
            except Exception as e3:
                print(f"[SEARCH] All methods failed: {e3}")
                return f"Search failed: {str(e3)}"