#!/usr/bin/env python3
import urllib.request
import urllib.error
import time

BASE_URL = "http://localhost:4000"

# Test pages
pages = [
    "/",
    "/goal-blindness/",
    "/spiral-field-renderer/",
    "/whitepaper/",
    "/election-1/",
    "/election-2/",
    "/election-3/",
    "/election-4/",
    "/zero-error/intro/",
    "/zero-error/detector/",
    "/for-developers/",
    "/for-ai/",
]

print("=" * 70)
print("JEKYLL SITE VERIFICATION - ALL PAGES")
print("=" * 70 + "\n")

passed = 0
failed = 0

for page in pages:
    url = BASE_URL + page
    try:
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        has_html = "<!DOCTYPE" in content or "<html" in content.lower()
        has_content = len(content) > 1000
        has_nav = "navigation" in content.lower() or "nav" in content.lower()
        
        status = "✅" if response.status == 200 else "⚠️"
        print(f"{status} {page}")
        print(f"   Status: {response.status}, Size: {len(content)} bytes")
        print(f"   HTML: {has_html}, Content: {has_content}, Nav: {has_nav}")
        passed += 1
    except urllib.error.HTTPError as e:
        print(f"❌ {page}")
        print(f"   HTTP Error: {e.code}")
        failed += 1
    except Exception as e:
        print(f"❌ {page}")
        print(f"   Error: {str(e)}")
        failed += 1
    print()

print("=" * 70)
print(f"Results: {passed} ✅ passed, {failed} ❌ failed")
print("=" * 70)
