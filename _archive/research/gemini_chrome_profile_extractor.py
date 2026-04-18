"""
Gemini Session Extractor - Using Real Chrome Profile
Connects to your existing Chrome with stored authentication
No login required - uses your authenticated session
"""

import json
import asyncio
import time
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


async def extract_with_chrome_profile():
    """
    Extract Gemini sessions using your real Chrome profile.
    This uses your existing authentication - no login required.
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
    
    # Chrome profile path (Windows default)
    chrome_user_data = Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"))
    
    if not chrome_user_data.exists():
        print(f"[!] Chrome profile not found at: {chrome_user_data}")
        print("[!] Trying alternative paths...")
        
        # Try other possible locations
        alt_paths = [
            Path(os.path.expandvars(r"%APPDATA%\Google\Chrome")),
            Path(os.path.expandvars(r"%USERPROFILE%\AppData\Local\Google\Chrome")),
        ]
        
        for alt_path in alt_paths:
            if alt_path.exists():
                chrome_user_data = alt_path
                print(f"[✓] Found Chrome at: {chrome_user_data}")
                break
        else:
            print("[!] Could not find Chrome profile")
            return sessions
    
    print(f"[1] Using Chrome profile: {chrome_user_data}")
    
    async with async_playwright() as p:
        try:
            print("[2] Launching Chrome with your existing profile...")
            
            # Launch with persistent context (keeps cookies, auth, etc)
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(chrome_user_data),
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-first-run",
                ]
            )
            
            # Get or create a page
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("[3] Navigating to Gemini...")
            try:
                await page.goto("https://gemini.google.com", wait_until="domcontentloaded", timeout=15000)
            except:
                # If first navigation fails, try with less strict waiting
                await page.goto("https://gemini.google.com", wait_until="load", timeout=15000)
            
            print("[4] Waiting for page content to load...")
            await page.wait_for_timeout(3000)
            
            # Check if we're authenticated
            current_url = page.url
            print(f"    Current URL: {current_url[:80]}...")
            
            if "accounts.google.com" in current_url or "signin" in current_url:
                print("[!] Still on login page - you may need to sign in manually")
                print("    Waiting 10 seconds for you to authenticate in the browser window...")
                await page.wait_for_timeout(10000)
            
            # Extract conversations from sidebar
            print("\n[5] Extracting conversations...")
            
            # Click on conversation sidebar if needed
            try:
                await page.wait_for_selector("nav", timeout=5000)
                print("    [✓] Found navigation sidebar")
            except:
                print("    [!] Navigation sidebar not found")
            
            # Get conversation links
            links = await page.locator("a[href*='gemini.google.com/c/']").all()
            print(f"    Found {len(links)} conversations")
            
            for idx, link in enumerate(links[:50]):
                try:
                    text = await link.inner_text()
                    href = await link.get_attribute("href")
                    
                    if text and text.strip():
                        sessions["conversations"].append({
                            "index": len(sessions["conversations"]),
                            "title": text.strip()[:100],
                            "url": href,
                            "timestamp": datetime.now().isoformat()
                        })
                        print(f"      [{len(sessions['conversations'])}] {text.strip()[:70]}")
                except:
                    pass
            
            # Extract visible messages from current conversation
            print("\n[6] Extracting messages from current view...")
            
            articles = await page.locator("[role='article']").all()
            print(f"    Found {len(articles)} message elements")
            
            for idx, article in enumerate(articles[:50]):
                try:
                    text = await article.inner_text()
                    if text and len(text.strip()) > 3:
                        sessions["messages"].append({
                            "index": len(sessions["messages"]),
                            "content": text.strip()[:400],
                            "full_length": len(text),
                            "timestamp": datetime.now().isoformat()
                        })
                except:
                    pass
            
            print(f"    Extracted {len(sessions['messages'])} messages")
            
            # Get page metadata
            print("\n[7] Capturing metadata...")
            page_title = await page.title()
            
            sessions["metadata"].update({
                "page_title": page_title,
                "current_url": current_url,
                "total_conversations": len(sessions["conversations"]),
                "total_messages_extracted": len(sessions["messages"]),
                "extraction_status": "success",
                "extraction_method": "real_chrome_profile",
                "chrome_profile_path": str(chrome_user_data)
            })
            
            print(f"\n[✓] EXTRACTION COMPLETE")
            print(f"    Conversations: {len(sessions['conversations'])}")
            print(f"    Messages: {len(sessions['messages'])}")
            
        except Exception as e:
            print(f"\n[!] Error: {e}")
            import traceback
            traceback.print_exc()
            sessions["metadata"]["extraction_status"] = f"error: {str(e)}"
        
        finally:
            print("\n[8] Closing browser...")
            try:
                await context.close()
            except:
                pass
    
    return sessions


def save_sessions(sessions, filename="gemini_sessions_extracted.json"):
    """Save extracted sessions to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)
    
    print(f"[✓] Saved to: {filename}")
    
    # Show file stats
    file_size = os.path.getsize(filename)
    print(f"    File size: {file_size:,} bytes")
    
    return filename


def main():
    print("=" * 70)
    print("GEMINI SESSION EXTRACTOR - CHROME PROFILE")
    print("=" * 70)
    print("\nUsing your existing Chrome authentication")
    print("No manual login required - extraction fully automated")
    print("=" * 70)
    
    # Run extraction
    sessions = asyncio.run(extract_with_chrome_profile())
    
    # Save results
    output_file = save_sessions(sessions)
    
    # Display summary
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"Conversations found: {sessions['metadata']['total_conversations']}")
    print(f"Messages extracted: {sessions['metadata']['total_messages_extracted']}")
    print(f"Status: {sessions['metadata']['extraction_status']}")
    print(f"Saved to: {output_file}")
    print("=" * 70)
    
    # Show first conversation if found
    if sessions["conversations"]:
        print("\nFirst 5 conversations:")
        for conv in sessions["conversations"][:5]:
            print(f"  - {conv['title']}")
    
    # Show first message if found
    if sessions["messages"]:
        print("\nFirst message excerpt:")
        print(f"  {sessions['messages'][0]['content'][:150]}...")
    
    return output_file


if __name__ == "__main__":
    main()
