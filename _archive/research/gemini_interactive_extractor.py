"""
Gemini Chat Session Extractor - Interactive Mode
Opens browser, waits for manual login, then extracts sessions
"""

import json
import asyncio
import time
from datetime import datetime
from playwright.async_api import async_playwright


async def extract_gemini_interactive():
    """
    Extract Gemini sessions with interactive manual login.
    Waits for user to authenticate before extraction.
    """
    
    sessions = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "messages": [],
        "metadata": {
            "total_conversations": 0,
            "extraction_status": "initializing"
        }
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("=" * 70)
            print("GEMINI SESSION EXTRACTOR - INTERACTIVE MODE")
            print("=" * 70)
            print("\n[1] Opening Gemini in browser...")
            await page.goto("https://gemini.google.com", wait_until="domcontentloaded")
            
            print("[2] Waiting for you to log in...")
            print("\n    IMPORTANT: Please log in to your Google account in the browser")
            print("    Once logged in and you see your conversations, press ENTER here...")
            
            # Wait for user to press enter
            input("\n    Press ENTER after you've logged in: ")
            
            print("\n[3] Giving page time to fully load...")
            await page.wait_for_timeout(5000)
            
            # Check current URL to verify login
            current_url = page.url
            print(f"[4] Current URL: {current_url[:80]}...")
            
            if "accounts.google.com" in current_url:
                print("\n[!] ERROR: Still on login page")
                print("    Please complete the Google login in the browser.")
                input("    Try again - press ENTER after logging in: ")
                await page.wait_for_timeout(5000)
            
            # Extract conversations from sidebar
            print("\n[5] Extracting conversations from sidebar...")
            
            # Try multiple selectors for conversation links
            selectors = [
                "a[href*='gemini.google.com/c/']",
                "a[href*='gemini.google.com/']",
                "nav a",
                "[role='navigation'] a",
            ]
            
            found_conversations = False
            for selector in selectors:
                try:
                    links = await page.locator(selector).all()
                    if links:
                        print(f"    Using selector: {selector}")
                        print(f"    Found {len(links)} links")
                        
                        for idx, link in enumerate(links[:50]):
                            try:
                                text = await link.inner_text()
                                href = await link.get_attribute("href")
                                
                                # Filter out nav links that aren't conversations
                                if text and len(text.strip()) > 1 and ("gemini.google.com" in str(href) or "chat" in text.lower()):
                                    sessions["conversations"].append({
                                        "index": len(sessions["conversations"]),
                                        "title": text.strip()[:100],
                                        "url": href,
                                        "timestamp": datetime.now().isoformat()
                                    })
                                    
                                    if text.strip():
                                        print(f"      [{len(sessions['conversations'])}] {text.strip()[:60]}")
                                    
                                    found_conversations = True
                            except:
                                pass
                        
                        if found_conversations:
                            break
                except:
                    pass
            
            if not found_conversations:
                print("    [!] No conversations found - page may still be loading")
                print("    Attempting to extract page content anyway...")
            
            # Extract visible messages
            print("\n[6] Extracting conversation messages...")
            
            # Get messages using various selectors
            message_selectors = [
                "[role='article']",
                "[data-message-id]",
                "div[class*='message']",
                "[class*='Message']"
            ]
            
            total_messages = 0
            for msg_selector in message_selectors:
                try:
                    elements = await page.locator(msg_selector).all()
                    
                    for elem in elements[:40]:
                        try:
                            text = await elem.inner_text()
                            if text and len(text.strip()) > 2:
                                sessions["messages"].append({
                                    "index": total_messages,
                                    "content": text.strip()[:300],
                                    "full_length": len(text),
                                    "timestamp": datetime.now().isoformat()
                                })
                                total_messages += 1
                        except:
                            pass
                    
                    if total_messages > 0:
                        break
                except:
                    pass
            
            print(f"    Extracted {total_messages} messages")
            
            # Get page metadata
            print("\n[7] Capturing page metadata...")
            
            page_title = await page.title()
            full_content = await page.content()
            
            sessions["metadata"].update({
                "page_title": page_title,
                "current_url": current_url,
                "total_conversations": len(sessions["conversations"]),
                "total_messages_extracted": total_messages,
                "extraction_status": "success",
                "content_length": len(full_content),
                "html_preview": full_content[:2000]  # First 2k of HTML for debugging
            })
            
            print(f"\n[✓] EXTRACTION COMPLETE")
            print(f"    Conversations: {len(sessions['conversations'])}")
            print(f"    Messages: {total_messages}")
            
        except Exception as e:
            print(f"\n[!] Error: {e}")
            sessions["metadata"]["extraction_status"] = f"error: {str(e)}"
        
        finally:
            print("\n[8] Closing browser...")
            await browser.close()
    
    return sessions


def save_sessions(sessions, filename="gemini_sessions.json"):
    """Save extracted sessions to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)
    
    print(f"[✓] Saved to: {filename}")
    return filename


def main():
    # Run extraction
    sessions = asyncio.run(extract_gemini_interactive())
    
    # Save results
    output_file = save_sessions(sessions)
    
    # Display summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Conversations found: {sessions['metadata']['total_conversations']}")
    print(f"Messages extracted: {sessions['metadata']['total_messages_extracted']}")
    print(f"Status: {sessions['metadata']['extraction_status']}")
    print(f"Saved to: {output_file}")
    print("=" * 70)
    
    return output_file


if __name__ == "__main__":
    main()
