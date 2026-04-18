"""
GEMINI LAZY EXTRACTOR - The Simplest Possible Approach
Just get the data from what's already loaded in the page via JavaScript
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright")
    sys.exit(1)


async def extract_gemini_data_lazy():
    """
    Absolute laziest way: Open Gemini, wait for user to log in,
    then run JavaScript to pull ALL data from the page
    """
    
    print("=" * 70)
    print("GEMINI LAZY EXTRACTOR")
    print("=" * 70)
    print()
    
    results = {
        "extracted_at": datetime.now().isoformat(),
        "data": None,
        "error": None
    }
    
    async with async_playwright() as p:
        print("[1] Opening browser...")
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("[2] Loading Gemini...")
        try:
            await page.goto("https://gemini.google.com", timeout=45000)
        except Exception as e:
            print(f"    Navigation error (page may have redirected): {e}")
        
        print("[3] WAITING FOR YOU TO LOG IN...")
        print()
        print("    ⚠️  BROWSER WINDOW SHOULD NOW BE OPEN")
        print("    → Click the browser window")
        print("    → Log in to your Google account") 
        print("    → Wait for Gemini conversations to load")
        print("    → THEN come back here and press ENTER")
        print()
        
        # Keep browser window open for 5 minutes max, poll for login
        print("    Waiting... (max 5 minutes)")
        for seconds in range(300):
            current_url = page.url
            if "gemini.google.com/app" in current_url:
                print(f"    ✓ Login detected! ({seconds}s)")
                break
            if seconds % 30 == 0 and seconds > 0:
                print(f"    ⏱️  Still waiting ({seconds}s)... Press ENTER when logged in")
            await page.wait_for_timeout(1000)
        
        print()
        input("    Press ENTER when ready: ")
        
        print("[4] Giving page time to settle...")
        await page.wait_for_timeout(3000)
        
        print("[5] Extracting data from page memory...")
        
        # Just ask the page what it has
        extracted_data = await page.evaluate("""
            async () => {
                const data = {
                    window_keys: Object.keys(window).filter(k => 
                        k.includes('chat') || k.includes('conversation') || 
                        k.includes('gemini') || k.includes('data') ||
                        k.includes('message') || k.includes('redux') ||
                        k.includes('store')
                    ),
                    page_title: document.title,
                    page_url: window.location.href,
                    local_storage: {},
                    session_storage: {},
                    indexeddb: {},
                    page_text_content: {
                        body: document.body.innerText.substring(0, 5000),
                        all_text_nodes: Array.from(document.querySelectorAll('*'))
                            .filter(el => el.children.length === 0 && el.innerText)
                            .map(el => el.innerText.trim())
                            .filter(t => t.length > 20 && t.length < 500)
                            .slice(0, 50)
                    },
                    links: Array.from(document.querySelectorAll('a'))
                        .map(a => ({
                            text: a.innerText,
                            href: a.href
                        }))
                        .filter(a => a.text && a.href)
                };
                
                // Try to get localStorage (ALL keys)
                try {
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        if (key) {
                            try {
                                const value = localStorage.getItem(key);
                                // Only include keys with meaningful data
                                if (value && value.length > 50) {
                                    data.local_storage[key] = {
                                        size: value.length,
                                        preview: value.substring(0, 500)
                                    };
                                }
                            } catch (e) {}
                        }
                    }
                } catch (e) {}
                
                // Try to get sessionStorage (ALL keys)
                try {
                    for (let i = 0; i < sessionStorage.length; i++) {
                        const key = sessionStorage.key(i);
                        if (key) {
                            try {
                                const value = sessionStorage.getItem(key);
                                if (value && value.length > 50) {
                                    data.session_storage[key] = {
                                        size: value.length,
                                        preview: value.substring(0, 500)
                                    };
                                }
                            } catch (e) {}
                        }
                    }
                } catch (e) {}
                
                // Try to get IndexedDB
                try {
                    const dbs = await indexedDB.databases();
                    for (const dbInfo of dbs) {
                        try {
                            const req = indexedDB.open(dbInfo.name);
                            await new Promise((resolve, reject) => {
                                req.onsuccess = () => {
                                    const db = req.result;
                                    data.indexeddb[dbInfo.name] = {
                                        stores: Array.from(db.objectStoreNames)
                                    };
                                    db.close();
                                    resolve();
                                };
                                req.onerror = reject;
                                req.onblocked = () => setTimeout(resolve, 100);
                            });
                        } catch (e) {}
                    }
                } catch (e) {}
                
                return data;
            }
        """)

        
        results["data"] = extracted_data
        
        print(f"    ✓ Title: {extracted_data['page_title']}")
        print(f"    ✓ URL: {extracted_data['page_url']}")
        print(f"    ✓ Found {len(extracted_data['links'])} links")
        print(f"    ✓ Found {len(extracted_data['local_storage'])} localStorage items")
        print(f"    ✓ Found {len(extracted_data['indexeddb'])} IndexedDB databases")
        print(f"    ✓ Text content: {len(extracted_data['page_text_content']['body'])} chars")
        print()
        
        # Save it
        output_file = Path("gemini_lazy_data.json")
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"[6] Saved to: {output_file}")
        print()
        print("=" * 70)
        print("DONE - Check gemini_lazy_data.json for all extracted data")
        print("=" * 70)
        
        await browser.close()
    
    return results


if __name__ == "__main__":
    asyncio.run(extract_gemini_data_lazy())
