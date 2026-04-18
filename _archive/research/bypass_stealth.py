import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def fetch_with_stealth():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Apply stealth measures
        await stealth_async(page)
        
        try:
            print("Navigating with stealth mode...")
            await page.goto('https://share.google/aimode/l4zX8GJdxDmfKTmn8', wait_until='networkidle', timeout=30000)
            
            print("Waiting for content...")
            await page.wait_for_timeout(3000)
            
            title = await page.title()
            print(f"Page title: {title[:100]}")
            
            content = await page.content()
            print(f"Page content: {len(content)} bytes")
            
            # Check for conversation elements
            if 'conversation' in content.lower():
                print("✓ Found 'conversation'")
            if 'message' in content.lower():
                print("✓ Found 'message'")
            
            # Save HTML
            with open('c:\\Determined\\stealth_full.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Get text content
            text = await page.evaluate('() => document.body.innerText')
            print(f"Text content: {len(text)} chars")
            
            if len(text) > 500:
                with open('c:\\Determined\\stealth_text.txt', 'w', encoding='utf-8') as f:
                    f.write(text[:5000])
                print("Saved text")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

asyncio.run(fetch_with_stealth())
