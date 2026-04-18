import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            # Navigate to the URL
            print("Loading page...")
            await page.goto('https://share.google/aimode/l4zX8GJdxDmfKTmn8', wait_until='networkidle', timeout=30000)
            
            # Wait a moment for any dynamic content
            await page.wait_for_timeout(2000)
            
            # Get the rendered HTML
            content = await page.content()
            
            # Also try to extract any JSON data or text content
            text_content = await page.evaluate('() => document.body.innerText')
            
            print("=== PAGE TITLE ===")
            title = await page.title()
            print(title)
            
            print("\n=== PAGE TEXT CONTENT ===")
            print(text_content[:3000])
            
            print("\n=== PAGE HTML (first 5000 chars) ===")
            print(content[:5000])
            
            # Try to find any data attributes or scripts
            print("\n=== Looking for data elements ===")
            all_scripts = await page.evaluate('() => Array.from(document.querySelectorAll("script")).map(s => s.textContent).join("\\n---\\n")')
            print(all_scripts[:2000])
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

asyncio.run(fetch_page())
