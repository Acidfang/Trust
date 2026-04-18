import undetected_chromedriver as uc
import time
import json

async def fetch_share_conversation():
    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options, version_main=None)
    
    try:
        print("Navigating to share link with undetected-chromedriver...")
        driver.get('https://share.google/aimode/l4zX8GJdxDmfKTmn8')
        
        # Wait for page to load
        time.sleep(5)
        
        # Check if we got past the reCAPTCHA
        print("Page title:", driver.title)
        
        # Get page content
        content = driver.page_source
        print(f"\nPage source length: {len(content)} bytes")
        
        if 'google.com/search' in content or 'recaptcha' in content.lower():
            print("Still on reCAPTCHA/redirect page")
        else:
            print("✓ Got past reCAPTCHA")
        
        # Look for conversation elements
        try:
            # Look for message elements
            messages = driver.find_elements("css selector", "[role='article']")
            print(f"\nFound {len(messages)} message elements")
            
            # Also try common chat patterns
            divs = driver.find_elements("css selector", "div[class*='message']")
            print(f"Found {len(divs)} divs with 'message' in class")
        except:
            print("No message elements found with standard selectors")
        
        # Save the page
        with open('c:\\Determined\\share_link_undetected.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("\nSaved page source to share_link_undetected.html")
        
        # Try to extract text
        text = driver.find_element("tag name", "body").text
        if text:
            print(f"\nPage text length: {len(text)} chars")
            if 'message' in text.lower() or 'response' in text.lower():
                print("✓ Page contains conversation-like content")
                with open('c:\\Determined\\share_link_text.txt', 'w', encoding='utf-8') as f:
                    f.write(text[:5000])
        
    finally:
        driver.quit()

import asyncio
# Use synchronous version instead
import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')

print("Launching undetected browser...")
driver = uc.Chrome(options=options, version_main=None)

try:
    print("Navigating to share link...")
    driver.get('https://share.google/aimode/l4zX8GJdxDmfKTmn8')
    
    print("Waiting for page load...")
    time.sleep(8)
    
    print("Page title:", driver.title[:100])
    
    content = driver.page_source
    print(f"Page source: {len(content)} bytes")
    
    if 'conversation' in content.lower():
        print("✓ Found 'conversation' in page")
    if 'message' in content.lower():
        print("✓ Found 'message' in page")
    if 'user' in content.lower():
        print("✓ Found 'user' in page")
    
    # Save raw HTML
    with open('c:\\Determined\\share_undetected_full.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved full HTML")
    
    # Extract text content  
    try:
        body = driver.find_element("tag name", "body")
        text = body.text[:10000]
        if text:
            with open('c:\\Determined\\share_undetected_text.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved {len(text)} chars of text")
    except:
        pass
        
finally:
    driver.quit()
    print("Browser closed")
