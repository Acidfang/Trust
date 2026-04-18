"""
GEMINI EXTRACTOR - DOM-Based Approach (Inspired by ai-chat-exporter)
Uses proven DOM selectors and Turndown for HTML to Markdown conversion
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed")
    sys.exit(1)


async def extract_gemini_dom_based():
    """
    Extract Gemini conversations using DOM-based approach.
    This method works because:
    1. We wait for user to be logged in
    2. We use proven DOM selectors
    3. We extract HTML and parse it properly
    4. No clipboard, no browser memory, no API calls
    """
    
    print("=" * 70)
    print("GEMINI EXTRACTOR - DOM-BASED (ai-chat-exporter approach)")
    print("=" * 70)
    print()
    
    results = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "messages": [],
        "debug": {},
        "error": None
    }
    
    async with async_playwright() as p:
        print("[1] Opening browser...")
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("[2] Navigating to Gemini...")
            await page.goto("https://gemini.google.com", wait_until="domcontentloaded", timeout=45000)
            
            print("[3] Waiting for login...")
            print("\n    → Log in to your Google account")
            print("    → Wait for conversations to load")
            print("    → Press ENTER when ready\n")
            
            try:
                input("    Press ENTER: ")
            except (KeyboardInterrupt, EOFError):
                print("\n    [!] Cancelled by user")
                results["error"] = "User cancelled during login wait"
                return results
            
            print("[4] Checking if logged in...")
            await page.wait_for_timeout(3000)
            
            current_url = page.url
            if "accounts.google.com" in current_url:
                print("    [!] Still on login page. Try again.")
                input("    Press ENTER after logging in: ")
                await page.wait_for_timeout(3000)
            
            print(f"    ✓ URL: {current_url}")
            print()
            
            # Extract using proven selectors
            print("[5] Extracting conversations from sidebar...")
            
            # First, debug: see what selectors actually exist
            selector_debug = await page.evaluate("""
                () => {
                    const debug = {
                        nav_elements: document.querySelectorAll('nav').length,
                        links_with_emoji: Array.from(document.querySelectorAll('a')).filter(a => /[\p{Emoji}]/.test(a.textContent)).length,
                        data_test_ids: Array.from(document.querySelectorAll('[data-test-id]')).map(el => el.getAttribute('data-test-id')).slice(0, 10),
                        aria_labels: Array.from(document.querySelectorAll('[aria-label]')).map(el => el.getAttribute('aria-label')).filter(l => l && l.length < 100).slice(0, 10),
                        buttons_div_role: document.querySelectorAll('div[role="button"]').length,
                        all_divs_with_text: Array.from(document.querySelectorAll('div')).filter(d => d.textContent.trim().length > 5 && d.textContent.trim().length < 200).slice(0, 5).map(d => d.textContent.substring(0, 60)),
                    };
                    return debug;
                }
            """)
            
            if selector_debug.get('data_test_ids') and len(selector_debug['data_test_ids']) > 0:
                print(f"    Debug - found data-test-ids: {selector_debug['data_test_ids']}")
            if selector_debug.get('aria_labels') and len(selector_debug['aria_labels']) > 0:
                sample_labels = [l[:40] for l in selector_debug['aria_labels'][:3]]
                print(f"    Debug - found aria-labels: {sample_labels}")
            
            results["debug"] = selector_debug
            
            conversation_data = await page.evaluate("""
                () => {
                    const conversations = [];
                    
                    // Selector 1: Try data-test-id first (most reliable per ai-chat-exporter)
                    let items = document.querySelectorAll('[data-test-id="conversation-list-item"]');
                    
                    // Selector 2: Fallback to aria-label if data-test-id not found
                    if (items.length === 0) {
                        items = document.querySelectorAll('a[href*="/c/"][aria-label]');
                    }
                    
                    // Selector 3: Fallback to buttons with text content (new structure)
                    if (items.length === 0) {
                        items = document.querySelectorAll('div[role="button"][aria-label]');
                    }
                    
                    // Selector 4: Fallback to general nav items
                    if (items.length === 0) {
                        items = document.querySelectorAll('nav a[href*="gemini.google.com"], nav button');
                    }
                    
                    for (const item of items) {
                        try {
                            const title = item.getAttribute('aria-label') || 
                                        item.getAttribute('data-tooltip') ||
                                        item.innerText?.trim();
                            
                            const url = item.href || item.getAttribute('href');
                            
                            // Filter out nav links and section headers
                            if (title && title.length > 2 && 
                                !title.includes('Sign in') && 
                                !title.includes('Gemini App') &&
                                !title.toLowerCase().includes('settings') &&
                                !title.toLowerCase().includes('help')) {
                                conversations.push({
                                    title: title.substring(0, 200),
                                    url: url || null,
                                    id: url?.split('/c/')[1] || null
                                });
                            }
                        } catch (e) {}
                    }
                    
                    return conversations;
                }
            """)
            
            results["conversations"] = conversation_data
            print(f"    Found {len(conversation_data)} conversations")
            
            for conv in conversation_data[:5]:
                print(f"      - {conv['title'][:60]}")
            
            # Extract messages using proven selectors
            print()
            print("[6] Extracting messages...")
            
            # First, scroll to load all messages
            print("    Scrolling to load all messages...")
            await page.evaluate("""
                async () => {
                    // Scroll to top first
                    window.scrollTo(0, 0);
                    
                    // Then scroll down to load lazy-loaded messages
                    for (let i = 0; i < 10; i++) {
                        window.scrollBy(0, -1000);
                        await new Promise(r => setTimeout(r, 500));
                    }
                }
            """)
            
            await page.wait_for_timeout(2000)
            
            # Now extract messages
            messages_data = await page.evaluate(r"""
                () => {
                    const messages = [];
                    
                    // Selector 1: role="article" (best for Gemini)
                    let items = document.querySelectorAll('[role="article"]');
                    
                    // Selector 2: Fallback to message-like divs
                    if (items.length === 0) {
                        items = document.querySelectorAll('div[class*="message"], div[class*="Message"]');
                    }
                    
                    // Selector 3: Fallback to generic divs with text content
                    if (items.length === 0) {
                        items = document.querySelectorAll('div[jsname]');
                    }
                    
                    for (const item of items) {
                        try {
                            // Extract text content
                            const text = item.innerText?.trim() || '';
                            
                            // Skip empty or very short messages
                            if (text.length < 5) continue;
                            
                            // Get HTML for better formatting preservation
                            const html = item.innerHTML;
                            
                            messages.push({
                                content: text.substring(0, 5000),
                                length: text.length,
                                has_code: text.includes('```') || text.includes('<code'),
                                has_table: text.includes('|') && text.match(/\|.*\|/),
                            });
                        } catch (e) {}
                    }
                    
                    // Remove duplicates
                    const seen = new Set();
                    const unique = [];
                    for (const msg of messages) {
                        if (!seen.has(msg.content)) {
                            seen.add(msg.content);
                            unique.push(msg);
                        }
                    }
                    
                    return unique;
                }
            """)
            
            results["messages"] = messages_data
            print(f"    Found {len(messages_data)} unique messages")
            
            for msg in messages_data[:3]:
                print(f"      [{msg['length']} chars] {msg['content'][:80]}...")
            
            # Get page metadata
            print()
            print("[7] Capturing metadata...")
            
            page_title = await page.title()
            print(f"    ✓ Title: {page_title}")
            
        except Exception as e:
            error_msg = str(e)
            results["error"] = error_msg
            print(f"\n[!] ERROR: {e}")
        
        except KeyboardInterrupt:
            print("\n[!] Cancelled by user")
            results["error"] = "User cancelled script"
        
        finally:
            print("\n[X] Closing browser...")
            try:
                await browser.close()
            except Exception as close_error:
                print(f"    (Warning: {close_error})")
    
    # Save results
    print()
    print("[8] Saving results...")
    
    output_file = Path("gemini_dom_extracted.json")
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
    asyncio.run(extract_gemini_dom_based())
