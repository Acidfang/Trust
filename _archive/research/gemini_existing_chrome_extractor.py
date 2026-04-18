"""
GEMINI EXTRACTOR - Connects to Existing Chrome Instance
Uses your already-logged-in Chrome session to extract conversations
"""

import asyncio
import json
import subprocess
from datetime import datetime
from pathlib import Path
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright")
    sys.exit(1)


def find_chrome_debug_port():
    """Find Chrome's debug port from running processes"""
    try:
        # Look for Chrome processes with --remote-debugging-port
        result = subprocess.run(
            ["wmic", "process", "list", "brief"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # If wmic works, parse process list
        if "chrome.exe" in result.stdout:
            print("[*] Found running Chrome process")
            # Default debug port is usually 9222
            return 9222
    except Exception as e:
        print(f"[*] Could not query processes: {e}")
    
    # Try default port
    return 9222


async def extract_from_existing_chrome():
    """
    Connect to already-running Chrome and extract Gemini data
    """
    
    print("=" * 70)
    print("GEMINI EXTRACTOR - EXISTING CHROME SESSION")
    print("=" * 70)
    print()
    
    results = {
        "extracted_at": datetime.now().isoformat(),
        "data": None,
        "error": None
    }
    
    # Method 1: Try to connect to existing Chrome on debug port
    print("[1] Attempting to connect to running Chrome...")
    
    debug_port = find_chrome_debug_port()
    print(f"    Trying debug port: {debug_port}")
    
    try:
        async with async_playwright() as p:
            print("[2] Connecting to Chrome via CDP...")
            
            # Try to connect to existing instance
            browser = await p.chromium.connect_over_cdp(f"http://localhost:{debug_port}")
            
            print("    ✓ Connected to existing Chrome instance")
            
            # Get the first page (or create new context)
            contexts = browser.contexts
            if contexts:
                context = contexts[0]
                pages = context.pages
                if pages:
                    page = pages[0]
                    print(f"    ✓ Using existing page at: {page.url}")
                else:
                    page = await context.new_page()
                    print("    ✓ Created new page in existing context")
            else:
                context = await browser.new_context()
                page = await context.new_page()
                print("    ✓ Created new context and page")
            
            # Navigate to Gemini if not already there
            if "gemini.google.com" not in page.url:
                print("[3] Navigating to Gemini...")
                await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=30000)
            else:
                print("[3] Already on Gemini page")
            
            print(f"    Current URL: {page.url}")
            
            # Wait a moment for page to settle
            await page.wait_for_timeout(2000)
            
            print("[4] Extracting data from page...")
            
            # Extract conversations and data
            extracted_data = await page.evaluate("""
                async () => {
                    const data = {
                        page_title: document.title,
                        page_url: window.location.href,
                        conversations: [],
                        messages: [],
                        storage: {
                            local_storage: {},
                            session_storage: {},
                            indexeddb: []
                        }
                    };
                    
                    // Extract conversation links from sidebar
                    const conversations = document.querySelectorAll('a[href*="gemini.google.com/c/"], a[href*="/app"]');
                    for (const conv of conversations) {
                        const text = conv.innerText?.trim();
                        const href = conv.href;
                        
                        // Filter out nav items, keep actual conversations
                        if (text && text.length > 2 && href && !text.includes('Sign in') && !text.includes('Gemini App')) {
                            data.conversations.push({
                                title: text,
                                url: href,
                                id: href.split('/c/')[1] || null
                            });
                        }
                    }
                    
                    // Extract visible messages
                    const messages = document.querySelectorAll('[role="article"], [class*="message"], [class*="Message"]');
                    for (const msg of messages) {
                        const text = msg.innerText?.trim();
                        if (text && text.length > 10 && text.length < 5000) {
                            data.messages.push({
                                content: text,
                                length: text.length
                            });
                        }
                    }
                    
                    // Get localStorage
                    try {
                        for (let i = 0; i < localStorage.length; i++) {
                            const key = localStorage.key(i);
                            const value = localStorage.getItem(key);
                            if (value && value.length > 50) {
                                data.storage.local_storage[key] = {
                                    size: value.length,
                                    preview: value.substring(0, 200)
                                };
                            }
                        }
                    } catch (e) {}
                    
                    // Get sessionStorage
                    try {
                        for (let i = 0; i < sessionStorage.length; i++) {
                            const key = sessionStorage.key(i);
                            const value = sessionStorage.getItem(key);
                            if (value && value.length > 50) {
                                data.storage.session_storage[key] = {
                                    size: value.length,
                                    preview: value.substring(0, 200)
                                };
                            }
                        }
                    } catch (e) {}
                    
                    // Get IndexedDB database names
                    try {
                        const dbs = await indexedDB.databases();
                        data.storage.indexeddb = dbs.map(db => db.name);
                    } catch (e) {}
                    
                    return data;
                }
            """)
            
            results["data"] = extracted_data
            
            print(f"    ✓ Title: {extracted_data['page_title']}")
            print(f"    ✓ Conversations found: {len(extracted_data['conversations'])}")
            print(f"    ✓ Messages extracted: {len(extracted_data['messages'])}")
            print(f"    ✓ localStorage items: {len(extracted_data['storage']['local_storage'])}")
            print(f"    ✓ sessionStorage items: {len(extracted_data['storage']['session_storage'])}")
            print(f"    ✓ IndexedDB databases: {len(extracted_data['storage']['indexeddb'])}")
            
            if extracted_data['conversations']:
                print("\n    Conversations:")
                for conv in extracted_data['conversations'][:5]:
                    print(f"      - {conv['title'][:60]}")
            
            if extracted_data['messages']:
                print("\n    Sample messages:")
                for msg in extracted_data['messages'][:3]:
                    print(f"      - {msg['content'][:80]}...")
            
            # Save to file
            output_file = Path("gemini_existing_chrome_data.json")
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            
            print(f"\n[5] Saved to: {output_file}")
            
            await browser.close()
    
    except Exception as e:
        error_msg = str(e)
        results["error"] = error_msg
        print(f"\n[!] ERROR: {error_msg}")
        
        if "ECONNREFUSED" in error_msg or "Connection refused" in error_msg:
            print("\n    Chrome debug port not accessible. Try:")
            print("    1. Close all Chrome windows")
            print("    2. Open Chrome with: chrome.exe --remote-debugging-port=9222")
            print("    3. Log in to Gemini")
            print("    4. Run this script again")
        
        # Save error
        output_file = Path("gemini_existing_chrome_data.json")
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        return results
    
    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    asyncio.run(extract_from_existing_chrome())
