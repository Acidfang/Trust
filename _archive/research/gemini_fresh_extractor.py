"""
Gemini Session Extractor - Fresh Context (no profile conflicts)
Opens browser in normal mode without profile decryption issues
"""

import json
import asyncio
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


async def extract_gemini_sessions():
    """
    Extract Gemini sessions using a fresh browser context.
    No Chrome profile conflicts - just opens normally.
    """
    
    sessions = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "messages": [],
        "metadata": {
            "total_conversations": 0,
            "total_messages_extracted": 0,
            "extraction_status": "initializing",
        }
    }
    
    async with async_playwright() as p:
        try:
            print("[1] Launching Chromium browser (fresh context)...")
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            print("[2] Navigating to Gemini...")
            await page.goto("https://gemini.google.com", wait_until="load", timeout=45000)
            
            print("[3] Waiting for app to load (60+ seconds)...")
            print("    This gives the app time to render conversations...")
            
            # First wait
            await page.wait_for_timeout(20000)
            print("    ✓ 20 seconds elapsed")
            
            # Wait for main
            try:
                await page.wait_for_selector("main", timeout=15000)
                print("    ✓ Main content detected")
            except:
                print("    ⚠ Main content not detected, continuing...")
            
            # Second wait for dynamic content
            print("    Waiting 25 more seconds...")
            await page.wait_for_timeout(25000)
            print("    ✓ 45 seconds total elapsed")
            
            # Scroll to trigger lazy loading
            print("    Scrolling to load more content...")
            await page.evaluate("window.scrollBy(0, window.innerHeight * 5)")
            await page.wait_for_timeout(5000)
            
            current_url = page.url
            page_title = await page.title()
            print(f"\n[4] Page Status:")
            print(f"    URL: {current_url[:80]}")
            print(f"    Title: {page_title}")
            
            # Get page structure
            print("\n[5] Analyzing page structure...")
            
            structure = {
                "nav_elements": await page.locator("nav").count(),
                "sidebar_elements": await page.locator("[role='navigation']").count(),
                "article_elements": await page.locator("[role='article']").count(),
                "button_count": await page.locator("button").count(),
            }
            
            for key, value in structure.items():
                print(f"    {key}: {value}")
            
            # Extract conversations
            print("\n[6] Searching for conversations...")
            
            selectors_to_try = [
                "a[href*='/c/']",
                "a[href*='gemini.google.com/c/']",
                "[role='button'][href*='/c/']",
                "nav a",
            ]
            
            found_convos = 0
            for selector in selectors_to_try:
                try:
                    elements = await page.locator(selector).count()
                    if elements > 0:
                        print(f"    Found {elements} with selector: {selector}")
                        
                        items = await page.locator(selector).all()
                        for item in items[:20]:
                            try:
                                text = (await item.inner_text()).strip()
                                href = await item.get_attribute("href") or ""
                                
                                if text and 3 < len(text) < 200 and text not in [c['title'] for c in sessions["conversations"]]:
                                    sessions["conversations"].append({
                                        "index": len(sessions["conversations"]),
                                        "title": text[:100],
                                        "url": href
                                    })
                                    found_convos += 1
                                    if found_convos <= 10:
                                        print(f"      [{found_convos}] {text[:60]}")
                            except:
                                pass
                        
                        if found_convos > 0:
                            break
                except:
                    pass
            
            if found_convos == 0:
                print("    No conversations found")
            
            # Extract messages
            print(f"\n[7] Waiting before message extraction (15 seconds)...")
            await page.wait_for_timeout(15000)
            
            print("    Scrolling to bottom...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)
            
            # Look for messages
            message_count = await page.locator("[role='article']").count()
            print(f"    Found {message_count} message elements")
            
            if message_count > 0:
                articles = await page.locator("[role='article']").all()
                for article in articles[:30]:
                    try:
                        text = (await article.inner_text()).strip()
                        if text and len(text) > 5:
                            sessions["messages"].append({
                                "content": text[:400],
                                "length": len(text)
                            })
                    except:
                        pass
            
            print(f"    Extracted {len(sessions['messages'])} messages")
            
            # Get HTML snapshot
            print("\n[8] Saving page data...")
            html = await page.content()
            with open("gemini_snapshot.html", "w", encoding="utf-8") as f:
                f.write(html[:100000])
            print("    ✓ HTML snapshot saved")
            
            # Take screenshot
            try:
                await page.screenshot(path="gemini_snapshot.png")
                print("    ✓ Screenshot saved")
            except:
                pass
            
            sessions["metadata"].update({
                "total_conversations": len(sessions["conversations"]),
                "total_messages_extracted": len(sessions["messages"]),
                "extraction_status": "success",
                "page_url": current_url,
                "page_title": page_title,
            })
            
            print(f"\n[✓] EXTRACTION COMPLETE")
            print(f"    Conversations: {len(sessions['conversations'])}")
            print(f"    Messages: {len(sessions['messages'])}")
            
            await browser.close()
            
        except Exception as e:
            print(f"\n[!] Error: {e}")
            import traceback
            traceback.print_exc()
            sessions["metadata"].update({
                "extraction_status": f"error: {str(e)}",
                "total_conversations": len(sessions["conversations"]),
                "total_messages_extracted": len(sessions["messages"])
            })
    
    return sessions


def main():
    print("=" * 70)
    print("GEMINI SESSION EXTRACTOR - FRESH CONTEXT")
    print("=" * 70)
    print("\nExtracting conversations with extended wait times...")
    print("Total wait time: ~100+ seconds for full app load\n")
    
    sessions = asyncio.run(extract_gemini_sessions())
    
    # Save results
    with open("gemini_extracted_fresh.json", "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Conversations found: {sessions['metadata']['total_conversations']}")
    print(f"Messages extracted: {sessions['metadata']['total_messages_extracted']}")
    print(f"Status: {sessions['metadata']['extraction_status']}")
    print(f"\nFiles saved:")
    print(f"  - gemini_extracted_fresh.json")
    print(f"  - gemini_snapshot.html")
    print(f"  - gemini_snapshot.png")
    print("=" * 70)


if __name__ == "__main__":
    main()
