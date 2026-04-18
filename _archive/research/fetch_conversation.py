import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_conversation():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            print("Attempting to extract conversation metadata and structure...")
            
            # Enable request/response logging
            responses = []
            def log_response(response):
                responses.append({
                    'url': response.url,
                    'status': response.status,
                    'headers': dict(response.headers)
                })
            
            page.on("response", log_response)
            
            # Navigate to the share link without following redirects all the way
            response = await page.goto('https://share.google/aimode/l4zX8GJdxDmfKTmn8', wait_until='networkidle', timeout=30000)
            
            print("\n=== RESPONSE CHAIN ===")
            for resp in responses[-5:]:  # Last 5 responses
                print(f"URL: {resp['url'][:100]}")
                print(f"Status: {resp['status']}")
            
            # Try to extract conversation structure
            print("\n=== LOOKING FOR CONVERSATION DATA ===")
            
            # Check for any data attributes
            data_elements = await page.evaluate('''
                () => {
                    const data = {};
                    // Look for any window variables
                    try {
                        if (window.__data) data.window__data = window.__data;
                        if (window.data) data.window_data = window.data;
                    } catch(e) {}
                    
                    // Look for meta tags with data
                    const metas = Array.from(document.querySelectorAll('meta')).map(m => ({
                        name: m.getAttribute('name'),
                        content: m.getAttribute('content')?.substring(0, 200)
                    }));
                    data.metas = metas;
                    
                    // Look for any JSON in script tags
                    const scripts = Array.from(document.querySelectorAll('script')).filter(s => !s.src);
                    const jsonScripts = scripts.map(s => {
                        try {
                            const parsed = JSON.parse(s.textContent);
                            return {parsed: typeof parsed, keys: Object.keys(parsed).slice(0, 5)};
                        } catch(e) {
                            return s.textContent.substring(0, 200);
                        }
                    });
                    data.scripts = jsonScripts.slice(0, 3);
                    
                    return data;
                }
            ''')
            
            print(json.dumps(data_elements, indent=2)[:1000])
            
            # Try to get full page content
            print("\n=== FULL PAGE CONTENT ===")
            content = await page.content()
            
            # Save it for analysis
            with open('c:\\Determined\\share_link_raw_response.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Saved raw HTML ({len(content)} bytes)")
            
            # Extract the actual query string data again more carefully
            print("\n=== EXTRACTING QUERY DATA ===")
            text = await page.evaluate('() => document.body.innerText')
            
            # Look for conversation patterns
            if 'message' in text.lower() or 'user' in text.lower() or 'assistant' in text.lower():
                print("Found conversation indicators")
            
            # Try to see if there are any links or further access points
            links = await page.evaluate('''
                () => Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.textContent.substring(0, 50)
                }))
            ''')
            
            if links:
                print(f"\n=== FOUND {len(links)} LINKS ===")
                for link in links[:10]:
                    print(f"  {link['text']}: {link['href'][:100]}")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

asyncio.run(fetch_conversation())
