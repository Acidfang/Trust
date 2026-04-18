import asyncio
from playwright.async_api import async_playwright
import time

async def fetch_with_custom_headers():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        # Set headers to appear more like a normal browser
        await page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://www.google.com/',
        })
        
        try:
            print("Navigating with custom headers...")
            response = await page.goto('https://share.google/aimode/l4zX8GJdxDmfKTmn8', wait_until='domcontentloaded', timeout=60000)
            
            print(f"Response status: {response.status if response else 'no response'}")
            
            print("Waiting for page...")
            await page.wait_for_timeout(5000)
            
            title = await page.title()
            print(f"Title: {title[:100]}")
            
            url = page.url
            print(f"Current URL: {url[:150]}")
            
            # Check if we're still on reCAPTCHA
            if 'recaptcha' in url or 'google.com/sorry' in url:
                print("Still blocked by reCAPTCHA/rate limit")
            else:
                print("✓ Got past reCAPTCHA")
            
            content = await page.content()
            print(f"Content length: {len(content)} bytes")
            
            # Save it
            with open('c:\\Determined\\custom_headers_response.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Try to get text
            try:
                text = await page.evaluate('() => document.documentElement.innerText')
                if text and len(text) > 100:
                    print(f"Text available: {len(text)} chars")
                    with open('c:\\Determined\\custom_headers_text.txt', 'w', encoding='utf-8') as f:
                        f.write(text)
            except:
                pass
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

asyncio.run(fetch_with_custom_headers())
