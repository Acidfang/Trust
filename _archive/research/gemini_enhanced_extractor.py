"""
Gemini Session Extractor - Enhanced with DOM Inspection
Uses real Chrome profile and deeply inspects page structure
"""

import json
import asyncio
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


async def extract_with_inspection():
    """
    Extract Gemini sessions with detailed DOM inspection.
    Waits for dynamic content to load and inspects actual page structure.
    """
    
    sessions = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "messages": [],
        "metadata": {
            "total_conversations": 0,
            "total_messages_extracted": 0,
            "extraction_status": "initializing",
            "page_structure": {}
        }
    }
    
    chrome_user_data = Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"))
    
    print(f"[1] Chrome profile: {chrome_user_data}")
    
    async with async_playwright() as p:
        try:
            print("[2] Launching Chrome...")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(chrome_user_data),
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                ]
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("[3] Loading Gemini...")
            await page.goto("https://gemini.google.com", wait_until="load", timeout=45000)
            
            print("[4] Waiting for dynamic content (60+ seconds)...")
            # Give the React/Angular app time to fully render
            await page.wait_for_timeout(20000)
            
            # Try to wait for main content to appear
            try:
                await page.wait_for_selector("main", timeout=15000)
                print("    [✓] Main content detected")
            except:
                print("    [!] Main content not found, continuing anyway")
            
            # Wait more for dynamic app state
            print("    Waiting 30 more seconds for conversations to load...")
            await page.wait_for_timeout(30000)
            
            # Scroll to trigger lazy loading
            await page.evaluate("window.scrollBy(0, window.innerHeight * 5)")
            await page.wait_for_timeout(5000)
            await page.evaluate("window.scrollBy(0, -window.innerHeight * 5)")  # Scroll back
            await page.wait_for_timeout(5000)
            
            # Try to find what's actually on the page
            current_url = page.url
            page_title = await page.title()
            print(f"    URL: {current_url[:80]}")
            print(f"    Title: {page_title}")
            
            # Get page content for inspection
            html = await page.content()
            
            # Check what's actually rendered
            print("\n[5] Inspecting page structure...")
            
            # Look for conversation elements with various approaches
            structure_info = {
                "has_nav": await page.locator("nav").count() > 0,
                "has_sidebar": await page.locator("[role='navigation']").count() > 0,
                "has_articles": await page.locator("[role='article']").count() > 0,
                "has_buttons": await page.locator("button").count(),
                "has_divs_with_messages": await page.locator("div[class*='message']").count(),
                "total_divs": await page.locator("div").count(),
            }
            
            print("    Page structure found:")
            for key, value in structure_info.items():
                print(f"      - {key}: {value}")
            
            sessions["metadata"]["page_structure"] = structure_info
            
            # Extract conversations - try multiple selectors
            print("\n[6] Extracting conversations...")
            
            selectors_to_try = [
                "a[href*='gemini.google.com/c/']",
                "a[href*='gemini.google.com/']",
                "[role='button'][href*='c/']",
                "div[role='link']",
                "a span"
            ]
            
            found_any = False
            for selector in selectors_to_try:
                links = await page.locator(selector).all()
                if links:
                    print(f"    Selector '{selector}' found {len(links)} elements")
                    
                    for link in links[:20]:
                        try:
                            text = (await link.inner_text()).strip()
                            href = await link.get_attribute("href") or ""
                            
                            # Only add if it looks like a conversation
                            if text and (len(text) > 3 and len(text) < 200):
                                if text not in [c['title'] for c in sessions["conversations"]]:
                                    sessions["conversations"].append({
                                        "index": len(sessions["conversations"]),
                                        "title": text[:100],
                                        "url": href,
                                        "selector_used": selector
                                    })
                                    print(f"      [{len(sessions['conversations'])}] {text[:60]}")
                                    found_any = True
                        except:
                            pass
                    
                    if found_any:
                        break
            
            if not found_any:
                print("    [!] No conversations found with standard selectors")
            
            # Extract messages
            print("\n[7] Waiting before extracting messages (15 seconds)...")
            await page.wait_for_timeout(15000)
            
            print("    Scrolling to load all content...")
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)
            
            print("    Extracting conversations and messages...")
            message_count = await page.locator("[role='article']").count()
            print(f"    Found {message_count} article elements")
            
            articles = await page.locator("[role='article']").all()
            
            for article in articles[:40]:
                try:
                    text = (await article.inner_text()).strip()
                    if text and len(text) > 5:
                        sessions["messages"].append({
                            "content": text[:300],
                            "full_length": len(text)
                        })
                except:
                    pass
            
            print(f"    Extracted {len(sessions['messages'])} messages")
            
            # Get page full screenshot for debugging
            print("\n[8] Taking page screenshot...")
            try:
                await page.screenshot(path="gemini_screenshot.png")
                print("    [✓] Screenshot saved: gemini_screenshot.png")
            except:
                print("    [!] Could not save screenshot")
            
            # Save raw HTML for inspection
            print("[9] Saving page HTML...")
            with open("gemini_page_source.html", "w", encoding="utf-8") as f:
                f.write(html[:50000])  # First 50KB
            print("    [✓] HTML saved: gemini_page_source.html")
            
            sessions["metadata"].update({
                "total_conversations": len(sessions["conversations"]),
                "total_messages_extracted": len(sessions["messages"]),
                "extraction_status": "success",
                "html_length": len(html)
            })
            
            print(f"\n[✓] EXTRACTION COMPLETE")
            print(f"    Conversations: {len(sessions['conversations'])}")
            print(f"    Messages: {len(sessions['messages'])}")
            
        except Exception as e:
            print(f"\n[!] Error: {e}")
            import traceback
            traceback.print_exc()
            sessions["metadata"].update({
                "extraction_status": f"error: {str(e)}",
                "total_conversations": len(sessions["conversations"]),
                "total_messages_extracted": len(sessions["messages"])
            })
        
        finally:
            print("\n[10] Closing browser...")
            try:
                await context.close()
            except:
                pass
    
    return sessions


def main():
    print("=" * 70)
    print("GEMINI SESSION EXTRACTOR - ENHANCED INSPECTION")
    print("=" * 70)
    
    sessions = asyncio.run(extract_with_inspection())
    
    # Save to JSON
    with open("gemini_sessions_extracted.json", "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Conversations: {sessions['metadata']['total_conversations']}")
    print(f"Messages: {sessions['metadata']['total_messages_extracted']}")
    print(f"Files created:")
    print(f"  - gemini_sessions_extracted.json")
    print(f"  - gemini_screenshot.png")
    print(f"  - gemini_page_source.html")
    print("=" * 70)


if __name__ == "__main__":
    main()
