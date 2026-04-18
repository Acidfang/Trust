import asyncio
from playwright.async_api import async_playwright
import json
import time

async def try_endpoints():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Try different endpoint variations
        endpoints = [
            'https://share.google/api/aimode/l4zX8GJdxDmfKTmn8',
            'https://share.google/aimode/l4zX8GJdxDmfKTmn8/conversation',
            'https://share.google/aimode/l4zX8GJdxDmfKTmn8.json',
            'https://share.google/aimode/l4zX8GJdxDmfKTmn8/export',
            'https://share.google/api/threads/l4zX8GJdxDmfKTmn8',
            'https://aistudio.google.com/share/l4zX8GJdxDmfKTmn8',
        ]
        
        for endpoint in endpoints:
            page = await browser.new_page()
            try:
                print(f"\nTrying: {endpoint}")
                response = await page.goto(endpoint, wait_until='networkidle', timeout=15000)
                
                if response:
                    print(f"Status: {response.status}")
                    content = await page.content()
                    text_content = await page.evaluate('() => document.body.innerText')
                    
                    # Check if it's JSON
                    if len(content) > 100 and content.strip().startswith('{'):
                        print(f"✓ Got JSON response ({len(content)} bytes)")
                        try:
                            data = json.loads(content)
                            print(f"Keys: {list(data.keys())[:10]}")
                            # Save it
                            with open(f'c:\\Determined\\share_response_{endpoints.index(endpoint)}.json', 'w') as f:
                                json.dump(data, f, indent=2)
                            print("Saved!")
                        except:
                            print(content[:300])
                    
                    # Check for conversation indicators
                    if 'messages' in text_content.lower() or 'response' in text_content.lower():
                        print(f"✓ Contains conversation-like content")
                        with open(f'c:\\Determined\\share_response_{endpoints.index(endpoint)}.txt', 'w', encoding='utf-8') as f:
                            f.write(text_content[:5000])
                    
                    if len(content) < 10000:
                        print(f"Size: {len(content)} bytes")
                
            except Exception as e:
                print(f"Error: {str(e)[:120]}")
            finally:
                await page.close()
                time.sleep(1)  # Rate limit
        
        await browser.close()

asyncio.run(try_endpoints())
