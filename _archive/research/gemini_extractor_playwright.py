"""
Gemini Chat Session Extractor via Playwright
Extracts conversation titles and content from gemini.google.com
"""

import json
import asyncio
import time
from datetime import datetime
from playwright.async_api import async_playwright


async def extract_gemini_sessions_async():
    """
    Extract Gemini chat sessions using Playwright (async version).
    Provides better cross-version compatibility than Selenium.
    """
    
    sessions = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "metadata": {
            "total_conversations": 0,
            "extraction_status": "in_progress"
        }
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("[1] Opening Gemini in browser...")
            await page.goto("https://gemini.google.com", wait_until="domcontentloaded")
            
            # Wait for page to load
            print("[2] Waiting for page to load...")
            await page.wait_for_timeout(5000)
            
            # Check if logged in
            try:
                await page.wait_for_selector("[role='article']", timeout=10000)
                print("[3] Page loaded successfully")
            except:
                print("[!] Page still loading - waiting for manual login if needed...")
                await page.wait_for_timeout(3000)
            
            # Extract conversation titles from sidebar
            print("[4] Extracting conversation titles from sidebar...")
            
            # Look for conversation links in the sidebar
            conversation_links = await page.locator("a[href*='gemini.google.com/']").all()
            
            print(f"[5] Found {len(conversation_links)} potential conversation links")
            
            for idx, link in enumerate(conversation_links):
                try:
                    # Get text and href
                    title_elem = await link.locator("div").first
                    title = await title_elem.inner_text()
                    href = await link.get_attribute("href")
                    
                    if title and title.strip():
                        sessions["conversations"].append({
                            "index": idx,
                            "title": title.strip()[:100],
                            "url": href,
                            "extracted": False
                        })
                        
                        print(f"  [{idx+1}] {title.strip()[:60]}")
                except Exception as e:
                    pass
            
            # Extract visible conversation content
            print("\n[6] Extracting conversation content...")
            
            # Get all visible text (messages)
            content = await page.content()
            
            # Look for message containers
            articles = await page.locator("[role='article']").all()
            messages = []
            
            for article in articles[:30]:  # First 30 messages
                try:
                    text = await article.inner_text()
                    if text and len(text.strip()) > 3:
                        messages.append({
                            "type": "message",
                            "content": text.strip()[:500],
                            "full_length": len(text)
                        })
                except:
                    pass
            
            sessions["messages"] = messages
            
            # Extract page metadata
            print("[7] Extracting metadata...")
            
            page_title = await page.title()
            current_url = page.url
            
            sessions["metadata"].update({
                "page_title": page_title,
                "current_url": current_url,
                "total_conversations": len(sessions["conversations"]),
                "total_messages_extracted": len(messages),
                "extraction_status": "success"
            })
            
            print(f"\n[✓] Extraction complete!")
            print(f"    - Conversations found: {len(sessions['conversations'])}")
            print(f"    - Messages extracted: {len(messages)}")
            
        except Exception as e:
            print(f"[!] Error during extraction: {e}")
            sessions["metadata"]["extraction_status"] = f"error: {str(e)}"
        
        finally:
            await browser.close()
            print("[8] Browser closed")
    
    return sessions


def extract_gemini_sessions():
    """Wrapper to run async extraction"""
    return asyncio.run(extract_gemini_sessions_async())


def save_sessions(sessions, filename="gemini_sessions.json"):
    """Save extracted sessions to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)
    
    print(f"[✓] Sessions saved to {filename}")
    return filename


def main():
    print("=" * 60)
    print("GEMINI SESSION EXTRACTOR (Playwright)")
    print("=" * 60)
    print("\nThis will:")
    print("1. Open Gemini in your browser")
    print("2. Extract conversation titles and content")
    print("3. Save to gemini_sessions.json")
    print("\nNote: You may need to log in manually in the browser")
    print("=" * 60)
    
    # Run extraction
    sessions = extract_gemini_sessions()
    
    # Save results
    output_file = save_sessions(sessions)
    
    # Display summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Extracted: {sessions['metadata']['total_conversations']} conversations")
    print(f"Messages: {sessions['metadata']['total_messages_extracted']}")
    print(f"Status: {sessions['metadata']['extraction_status']}")
    print(f"Saved to: {output_file}")
    print("=" * 60)
    
    return output_file


if __name__ == "__main__":
    output_file = main()
