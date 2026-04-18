"""
Gemini Session Extractor - Advanced DOM & Storage Access
Uses JavaScript execution to access dynamically-loaded conversation data
"""

import json
import asyncio
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


async def extract_advanced():
    """
    Extract Gemini sessions by:
    1. Waiting for full JS rendering
    2. Accessing browser storage (localStorage, IndexedDB)
    3. Executing JS to access internal app state
    """
    
    chrome_user_data = Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"))
    
    print(f"[1] Using Chrome profile: {chrome_user_data}")
    
    sessions = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "messages": [],
        "metadata": {}
    }
    
    async with async_playwright() as p:
        try:
            print("[2] Launching Chrome with persistent context...")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(chrome_user_data),
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                ]
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            # Set longer timeout
            page.set_default_timeout(30000)
            
            print("[3] Navigating to Gemini...")
            await page.goto("https://gemini.google.com", wait_until="domcontentloaded", timeout=15000)
            
            print("[4] Waiting for app to fully load (15 seconds)...")
            await page.wait_for_timeout(15000)
            
            current_url = page.url
            print(f"    URL: {current_url[:80]}")
            
            # Check authentication
            if "signin" in current_url or "accounts" in current_url:
                print("[!] Still on login page - authentication needed")
                return sessions
            
            # Try to access localStorage
            print("\n[5] Extracting from localStorage...")
            local_storage = await page.evaluate("() => localStorage")
            print(f"    localStorage entries: {len(local_storage) if local_storage else 0}")
            
            # Try to access sessionStorage
            print("[6] Checking sessionStorage...")
            try:
                session_storage = await page.evaluate("() => Object.keys(sessionStorage)")
                print(f"    sessionStorage keys: {len(session_storage)}")
            except:
                print("    [!] sessionStorage not accessible")
            
            # Try to find data in window object
            print("[7] Searching window object for conversation data...")
            try:
                window_keys = await page.evaluate("""
                    () => {
                        const keys = Object.keys(window);
                        return keys.filter(k => 
                            k.toLowerCase().includes('chat') || 
                            k.toLowerCase().includes('message') ||
                            k.toLowerCase().includes('conversation') ||
                            k.toLowerCase().includes('gemini')
                        );
                    }
                """)
                print(f"    Found {len(window_keys)} relevant window properties:")
                for key in window_keys[:10]:
                    print(f"      - {key}")
            except Exception as e:
                print(f"    [!] Error accessing window: {e}")
            
            # Try to get conversation list elements (wait longer for JS to render)
            print("\n[8] Looking for rendered conversations...")
            
            # Scroll down to potentially load more content
            await page.evaluate("window.scrollBy(0, window.innerHeight)")
            await page.wait_for_timeout(2000)
            
            # Try various selectors for conversations
            selectors = [
                "a[href*='/c/']",
                "[data-testid*='conversation']",
                "[role='button'][tabindex='0']",
                "div[role='button']"
            ]
            
            for selector in selectors:
                try:
                    elements = await page.locator(selector).count()
                    if elements > 0:
                        print(f"    Found {elements} elements with: {selector}")
                        
                        items = await page.locator(selector).all()
                        for item in items[:10]:
                            try:
                                text = await item.inner_text()
                                if text and len(text) > 3 and len(text) < 200:
                                    print(f"      - {text[:50]}")
                            except:
                                pass
                except:
                    pass
            
            # Try to access more detailed page content
            print("\n[9] Extracting detailed page content...")
            
            # Get all text from main content area
            try:
                main_text = await page.locator("main").inner_text()
                if main_text:
                    lines = main_text.split('\n')[:20]
                    print(f"    Main content ({len(lines)} lines):")
                    for line in lines:
                        if line.strip():
                            print(f"      {line.strip()[:60]}")
            except:
                print("    [!] Could not access main content")
            
            # Save page structure info
            page_title = await page.title()
            html = await page.content()
            
            sessions["metadata"] = {
                "page_title": page_title,
                "current_url": current_url,
                "page_load_time": "20+ seconds",
                "html_length": len(html),
                "extraction_status": "completed"
            }
            
            print("\n[✓] Extraction complete")
            
        except Exception as e:
            print(f"\n[!] Error: {e}")
            import traceback
            traceback.print_exc()
            sessions["metadata"]["error"] = str(e)
        
        finally:
            print("\n[10] Closing browser...")
            try:
                await context.close()
            except:
                pass
    
    return sessions


def main():
    print("=" * 70)
    print("GEMINI EXTRACTOR - ADVANCED (JS + Storage Access)")
    print("=" * 70)
    print("\nExtracting conversations using JavaScript execution...")
    
    sessions = asyncio.run(extract_advanced())
    
    # Save results
    with open("gemini_advanced_extract.json", "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2)
    
    print("\n" + "=" * 70)
    print("RESULTS SAVED TO: gemini_advanced_extract.json")
    print("=" * 70)


if __name__ == "__main__":
    main()
