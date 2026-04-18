"""
GEMINI INTERACTIVE EXTRACTOR - IMPROVED
Opens browser, waits for manual login, then thoroughly extracts all visible data
"""

import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from pathlib import Path


async def extract_gemini_interactive():
    """
    Extract Gemini sessions with interactive manual login.
    User logs in manually, we extract everything visible on the page.
    """
    
    results = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "messages": [],
        "page_data": {},
        "metadata": {
            "status": "initializing"
        }
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("=" * 70)
            print("GEMINI SESSION EXTRACTOR - INTERACTIVE MODE (IMPROVED)")
            print("=" * 70)
            print()
            
            print("[1] Opening Gemini in browser...")
            await page.goto("https://gemini.google.com", wait_until="load", timeout=60000)
            
            print("[2] WAITING FOR YOUR LOGIN...")
            print()
            print("    → Browser window should be open")
            print("    → Log in to your Google account if needed")
            print("    → Make sure you see your Gemini conversations")
            print("    → Then press ENTER here")
            print()
            
            input("    Press ENTER when logged in and ready: ")
            
            print()
            print("[3] Giving page time to fully load conversations...")
            await page.wait_for_timeout(3000)
            
            current_url = page.url
            print(f"    Current URL: {current_url}")
            print()
            
            print("[4] Extracting all data from page...")
            
            # Large JavaScript extraction
            extracted_data = await page.evaluate("""
                async () => {
                    const data = {
                        page_title: document.title,
                        page_url: window.location.href,
                        page_text: document.body.innerText.substring(0, 10000),
                        conversations: [],
                        messages: [],
                        all_links: [],
                        all_text_elements: [],
                        window_objects: {}
                    };
                    
                    // Get ALL links on the page
                    const links = document.querySelectorAll('a');
                    for (const link of links) {
                        const text = link.innerText?.trim();
                        const href = link.href;
                        if (text && text.length > 0) {
                            data.all_links.push({
                                text: text.substring(0, 100),
                                href: href,
                                isConversation: href.includes('/c/') || href.includes('/app')
                            });
                        }
                    }
                    
                    // Filter for actual conversation links
                    data.conversations = data.all_links.filter(link => 
                        link.isConversation && 
                        link.text.length > 2 && 
                        !link.text.includes('Sign') && 
                        !link.text.includes('Download')
                    ).slice(0, 50);
                    
                    // Get all text content
                    const walker = document.createTreeWalker(
                        document.body,
                        NodeFilter.SHOW_TEXT,
                        null
                    );
                    
                    let node;
                    let textCount = 0;
                    while (node = walker.nextNode()) {
                        const text = node.textContent.trim();
                        if (text.length > 10 && text.length < 500 && !text.includes('[object')) {
                            data.all_text_elements.push({
                                text: text.substring(0, 200),
                                length: text.length
                            });
                            textCount++;
                            if (textCount > 100) break;
                        }
                    }
                    
                    // Try to find message containers
                    const messageElements = document.querySelectorAll(
                        '[role="article"], [data-testid*="message"], [class*="message"], [class*="Message"]'
                    );
                    
                    for (const elem of messageElements) {
                        const text = elem.innerText?.trim();
                        if (text && text.length > 5 && text.length < 2000) {
                            data.messages.push({
                                content: text.substring(0, 500),
                                length: text.length,
                                tag: elem.tagName
                            });
                        }
                    }
                    
                    // Window object inspection
                    const interestingKeys = Object.keys(window).filter(k => 
                        k.toLowerCase().includes('bard') ||
                        k.toLowerCase().includes('gemini') ||
                        k.toLowerCase().includes('chat') ||
                        k.toLowerCase().includes('conversation') ||
                        k.toLowerCase().includes('message') ||
                        k.toLowerCase().includes('store') ||
                        k.toLowerCase().includes('redux')
                    );
                    
                    for (const key of interestingKeys.slice(0, 20)) {
                        try {
                            const value = window[key];
                            data.window_objects[key] = {
                                type: typeof value,
                                isObject: value !== null && typeof value === 'object',
                                keys: typeof value === 'object' ? Object.keys(value).slice(0, 5) : null
                            };
                        } catch (e) {}
                    }
                    
                    // Local/Session storage
                    const storage = {
                        local: {},
                        session: {}
                    };
                    
                    try {
                        for (let i = 0; i < localStorage.length; i++) {
                            const key = localStorage.key(i);
                            const value = localStorage.getItem(key);
                            if (value && value.length > 50) {
                                storage.local[key] = {
                                    size: value.length,
                                    preview: value.substring(0, 150)
                                };
                            }
                        }
                    } catch (e) {}
                    
                    try {
                        for (let i = 0; i < sessionStorage.length; i++) {
                            const key = sessionStorage.key(i);
                            const value = sessionStorage.getItem(key);
                            if (value && value.length > 50) {
                                storage.session[key] = {
                                    size: value.length,
                                    preview: value.substring(0, 150)
                                };
                            }
                        }
                    } catch (e) {}
                    
                    data.storage = storage;
                    
                    return data;
                }
            """)
            
            results.update(extracted_data)
            results["metadata"]["status"] = "success"
            
            print()
            print(f"    ✓ Page title: {extracted_data['page_title']}")
            print(f"    ✓ Links found: {len(extracted_data['all_links'])}")
            print(f"    ✓ Conversations detected: {len(extracted_data['conversations'])}")
            print(f"    ✓ Messages on page: {len(extracted_data['messages'])}")
            print(f"    ✓ Text elements: {len(extracted_data['all_text_elements'])}")
            print(f"    ✓ localStorage items: {len(extracted_data['storage']['local'])}")
            print(f"    ✓ sessionStorage items: {len(extracted_data['storage']['session'])}")
            
            # Display what we found
            print()
            if extracted_data['conversations']:
                print("[5] Detected Conversations:")
                for i, conv in enumerate(extracted_data['conversations'][:10], 1):
                    print(f"    {i}. {conv['text'][:60]}")
            
            if extracted_data['messages']:
                print()
                print("[6] Messages on Page:")
                for i, msg in enumerate(extracted_data['messages'][:5], 1):
                    preview = msg['content'][:70].replace('\n', ' ')
                    print(f"    {i}. {preview}...")
            
            if extracted_data['window_objects']:
                print()
                print("[7] Window Objects Found:")
                for key in list(extracted_data['window_objects'].keys())[:10]:
                    print(f"    - {key}")
            
            # Save to file
            output_file = Path("gemini_interactive_data.json")
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            
            print()
            print(f"[8] Saved to: {output_file}")
            
        except Exception as e:
            results["metadata"]["status"] = "error"
            results["metadata"]["error"] = str(e)
            print(f"[!] ERROR: {e}")
            
            output_file = Path("gemini_interactive_data.json")
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
        
        finally:
            await browser.close()
    
    print()
    print("=" * 70)
    print("DONE - Check gemini_interactive_data.json")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    asyncio.run(extract_gemini_interactive())
