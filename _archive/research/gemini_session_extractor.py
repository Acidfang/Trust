"""
Gemini Chat Session Extractor via Browser Automation
Extracts conversation titles and content from gemini.google.com
"""

import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def extract_gemini_sessions(headless=False, timeout=30):
    """
    Extract Gemini chat sessions from browser.
    
    Args:
        headless: If True, run browser in headless mode (no visible window)
        timeout: Time to wait for page load (seconds)
    
    Returns:
        dict with extracted sessions
    """
    
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    sessions = {
        "extracted_at": datetime.now().isoformat(),
        "conversations": [],
        "metadata": {
            "total_conversations": 0,
            "extraction_status": "in_progress"
        }
    }
    
    try:
        print("[1] Opening Gemini in browser...")
        driver.get("https://gemini.google.com")
        
        # Wait for page to load
        print("[2] Waiting for page to load...")
        time.sleep(5)
        
        # Check if logged in
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_elements_located((By.CSS_SELECTOR, "[role='article']"))
            )
            print("[3] Page loaded successfully")
        except:
            print("[!] Page may not have loaded - open browser manually and log in if needed")
            print("[!] Browser will remain open. Press ENTER after logging in...")
            input()
            time.sleep(3)
        
        # Extract conversation titles from sidebar
        print("[4] Extracting conversation titles from sidebar...")
        
        conversation_links = driver.find_elements(
            By.CSS_SELECTOR, 
            "a[href*='gemini.google.com/'][role='button']"
        )
        
        print(f"[5] Found {len(conversation_links)} conversation links")
        
        for idx, link in enumerate(conversation_links):
            try:
                title = link.get_attribute("aria-label") or link.text or "Untitled"
                href = link.get_attribute("href")
                
                sessions["conversations"].append({
                    "index": idx,
                    "title": title.strip(),
                    "url": href,
                    "extracted": False
                })
                
                print(f"  [{idx+1}] {title[:60]}")
            except Exception as e:
                print(f"  [!] Error extracting conversation {idx}: {e}")
        
        # Extract conversation content from current view
        print("\n[6] Extracting conversation content...")
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for message containers
        messages = []
        
        # Try different selectors for message content
        selectors_to_try = [
            "[role='article']",
            "[data-message]",
            ".message",
            "[class*='message']"
        ]
        
        for selector in selectors_to_try:
            elements = soup.select(selector)
            if elements:
                print(f"  Found {len(elements)} message elements using selector: {selector}")
                
                for elem in elements[:50]:  # Limit to first 50
                    text = elem.get_text(strip=True)
                    if text and len(text) > 3:
                        messages.append({
                            "type": "message",
                            "content": text[:500],  # Truncate long messages
                            "full_length": len(text)
                        })
                break
        
        sessions["messages"] = messages[:20]  # Store first 20 messages
        
        # Extract page metadata
        print("[7] Extracting page metadata...")
        
        title = driver.title
        current_url = driver.current_url
        
        sessions["metadata"].update({
            "page_title": title,
            "current_url": current_url,
            "total_conversations": len(sessions["conversations"]),
            "total_messages_extracted": len(messages),
            "extraction_status": "success"
        })
        
        print(f"\n[✓] Extraction complete!")
        print(f"    - Conversations found: {len(sessions['conversations'])}")
        print(f"    - Messages extracted: {len(messages)}")
        
    except Exception as e:
        print(f"[!] Error during extraction: {e}")
        sessions["metadata"]["extraction_status"] = f"error: {str(e)}"
    
    finally:
        driver.quit()
        print("[8] Browser closed")
    
    return sessions


def save_sessions(sessions, filename="gemini_sessions.json"):
    """Save extracted sessions to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)
    
    print(f"[✓] Sessions saved to {filename}")
    return filename


def main():
    print("=" * 60)
    print("GEMINI SESSION EXTRACTOR")
    print("=" * 60)
    print("\nThis will:")
    print("1. Open Gemini in your browser")
    print("2. Extract conversation titles and content")
    print("3. Save to gemini_sessions.json")
    print("\nNote: You may need to log in manually in the browser")
    print("=" * 60)
    
    # Run extraction (with visible browser for manual login)
    sessions = extract_gemini_sessions(headless=False, timeout=30)
    
    # Save results
    output_file = save_sessions(sessions)
    
    # Display summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Extracted: {sessions['metadata']['total_conversations']} conversations")
    print(f"Messages: {sessions['metadata']['total_messages_extracted']}")
    print(f"Saved to: {output_file}")
    print("=" * 60)
    
    return output_file


if __name__ == "__main__":
    output_file = main()
