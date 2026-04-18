"""
GEMINI EXTRACTOR - Using Existing Chrome User Profile
Connects to your real Chrome profile to access already-authenticated Gemini session
No login needed - no security blocks!
"""

import json
import asyncio
import os
from datetime import datetime
from pathlib import Path
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed")
    sys.exit(1)


async def extract_from_chrome_profile():
    """
    Extract Gemini conversations using your existing Chrome user profile.
    This works because:
    1. Chrome profile already has valid Gemini session cookies
    2. No login required - already authenticated
    3. Google sees a legitimate session, not a bot
    """
    
    print("=" * 70)
    print("GEMINI EXTRACTOR - Using Your Chrome Profile")
    print("=" * 70)
    print()
    
    results = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "messages": [],
        "debug": {},
        "error": None
    }
    
    # Find Chrome profile
    username = os.getenv('USERNAME')
    chrome_profile = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    
    print(f"[1] Chrome profile: {chrome_profile}")
    
    if not os.path.exists(chrome_profile):
        print("    [!] ERROR: Chrome profile not found")
        print("    Make sure Chrome is installed and you have a User Data\\Default profile")
        results["error"] = "Chrome profile not found"
        return results
    
    print("    ✓ Profile found")
    print()
    print("[2] Launching Playwright with user profile...")
    print("    (Note: Chrome may briefly open and close)")
    print()
    
    async with async_playwright() as p:
        try:
            # Launch Chrome with the user's profile
            print("[3] Connecting to Chrome with your profile...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=chrome_profile,
                headless=False,  # Need to see the browser to verify
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                ],
            )
            
            print("    ✓ Connected")
            
            # Create or reuse a page
            if context.pages:
                page = context.pages[0]
                print("    ✓ Using existing page")
            else:
                page = await context.new_page()
                print("    ✓ Created new page")
            
            # Navigate to Gemini
            print()
            print("[4] Navigating to Gemini...")
            await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=30000)
            
            current_url = page.url
            print(f"    ✓ URL: {current_url}")
            
            if "accounts.google.com" in current_url:
                print("\n    [!] NOT LOGGED IN")
                print("    A browser window may have opened. Please:")
                print("    1. Log in to your Google account")
                print("    2. Wait for Gemini conversations to load")
                print("    3. Close the browser window")
                print("\n    Keep running this script - it will detect when you've logged in...")
                
                # Wait up to 5 minutes for user to log in
                for i in range(300):
                    await page.wait_for_timeout(1000)
                    if "accounts.google.com" not in page.url:
                        print(f"\n    ✓ Login detected!")
                        await page.wait_for_timeout(3000)
                        current_url = page.url
                        break
                    if i % 30 == 0 and i > 0:
                        print(f"    ⏱️  Waiting for login ({i}s)...")
            
            print()
            print("[5] Extracting conversations...")
            
            # Debug DOM structure first
            selector_debug = await page.evaluate(r"""
                () => {
                    return {
                        nav_elements: document.querySelectorAll('nav').length,
                        data_test_ids: Array.from(document.querySelectorAll('[data-test-id]')).map(el => el.getAttribute('data-test-id')).slice(0, 15),
                        aria_labels: Array.from(document.querySelectorAll('[aria-label]')).map(el => el.getAttribute('aria-label')).filter(l => l && l.length > 2 && l.length < 150).slice(0, 15),
                        links_gemini: document.querySelectorAll('a[href*="/c/"]').length,
                        divs_role_button: document.querySelectorAll('div[role="button"]').length,
                    };
                }
            """)
            
            results["debug"] = selector_debug
            print(f"    DOM analysis:")
            print(f"      - nav elements: {selector_debug['nav_elements']}")
            print(f"      - links with /c/: {selector_debug['links_gemini']}")
            print(f"      - divs with role=button: {selector_debug['divs_role_button']}")
            print(f"      - aria-labels found: {len(selector_debug['aria_labels'])}")
            
            # Extract conversations
            conversation_data = await page.evaluate(r"""
                () => {
                    const conversations = [];
                    
                    // Try multiple selectors
                    let items = document.querySelectorAll('[data-test-id="conversation-list-item"]');
                    if (items.length === 0) items = document.querySelectorAll('a[href*="/c/"]');
                    if (items.length === 0) items = document.querySelectorAll('div[role="button"][aria-label]');
                    if (items.length === 0) items = document.querySelectorAll('[aria-label*="conversation"], [aria-label*="chat"]');
                    
                    for (const item of items) {
                        try {
                            const title = item.getAttribute('aria-label') || 
                                        item.innerText?.trim() || 
                                        item.textContent?.trim();
                            const url = item.href;
                            
                            if (title && title.length > 2 && title.length < 200 &&
                                !title.toLowerCase().includes('sign in') &&
                                !title.toLowerCase().includes('settings')) {
                                conversations.push({
                                    title: title,
                                    url: url || null,
                                });
                            }
                        } catch (e) {}
                    }
                    
                    // Remove duplicates
                    const seen = new Set();
                    return conversations.filter(c => {
                        if (seen.has(c.title)) return false;
                        seen.add(c.title);
                        return true;
                    });
                }
            """)
            
            results["conversations"] = conversation_data
            print(f"\n    ✓ Found {len(conversation_data)} conversations:")
            for conv in conversation_data[:10]:
                print(f"      - {conv['title'][:70]}")
            
            # Extract messages
            print()
            print("[6] Scrolling to load all messages...")
            await page.evaluate(r"""
                async () => {
                    // Scroll through entire conversation
                    let lastHeight = 0;
                    for (let i = 0; i < 15; i++) {
                        window.scrollBy(0, -1000);
                        await new Promise(r => setTimeout(r, 300));
                    }
                }
            """)
            
            print("    Extracting messages...")
            messages_data = await page.evaluate(r"""
                () => {
                    const messages = [];
                    
                    // Selector 1: role="article"
                    let items = document.querySelectorAll('[role="article"]');
                    
                    // Selector 2: message divs
                    if (items.length === 0) {
                        items = Array.from(document.querySelectorAll('div')).filter(el => {
                            const text = el.innerText;
                            return text && text.length > 30 && text.length < 6000 && 
                                   (el.querySelector('[role="button"]') === null);
                        });
                    }
                    
                    for (const item of items) {
                        try {
                            const text = item.innerText?.trim() || '';
                            if (text.length > 10 && text.length < 8000 &&
                                !text.includes('Cookie') &&
                                !text.includes('Sign in')) {
                                messages.push({
                                    content: text.substring(0, 4000),
                                    length: text.length,
                                });
                            }
                        } catch (e) {}
                    }
                    
                    // Remove duplicates
                    const seen = new Set();
                    return messages.filter(m => {
                        if (seen.has(m.content)) return false;
                        seen.add(m.content);
                        return true;
                    });
                }
            """)
            
            results["messages"] = messages_data
            print(f"    ✓ Found {len(messages_data)} unique messages")
            
            for msg in messages_data[:3]:
                print(f"      [{msg['length']} chars] {msg['content'][:60]}...")
            
        except Exception as e:
            error_msg = str(e)
            results["error"] = error_msg
            print(f"\n[!] ERROR: {e}")
        
        finally:
            print()
            print("[X] Closing...")
            try:
                await context.close()
            except Exception as e:
                print(f"    (Note: {e})")
    
    # Save results
    print()
    print("[7] Saving results...")
    
    output_file = Path("gemini_profile_extracted.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"    Saved to: {output_file}")
    print()
    print("=" * 70)
    print(f"EXTRACTION COMPLETE")
    print(f"  Conversations: {len(results['conversations'])}")
    print(f"  Messages: {len(results['messages'])}")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    asyncio.run(extract_from_chrome_profile())
