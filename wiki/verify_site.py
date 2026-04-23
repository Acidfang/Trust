#!/usr/bin/env python3
"""
Verify the generated Jekyll site
"""

import os
import urllib.request
from pathlib import Path

print("\n" + "="*70)
print("JEKYLL SITE VERIFICATION")
print("="*70 + "\n")

test_urls = [
    ('/', 'Home/Index'),
    ('/goal-blindness/', 'Goal-Blindness'),
    ('/spiral-field-renderer/', 'Spiral Renderer (with Three.js)'),
    ('/whitepaper/', 'Whitepaper'),
    ('/election-1/', 'Election 1'),
    ('/zero-error/intro/', 'Zero-Error Intro'),
]

base_url = 'http://localhost:4000'
all_passed = True

for url_path, description in test_urls:
    try:
        url = base_url + url_path
        resp = urllib.request.urlopen(url, timeout=5)
        html = resp.read().decode('utf-8')
        
        # Check if it's proper HTML (not error)
        has_doctype = html.lower().startswith('<!doctype')
        has_nav = 'nav' in html.lower()
        has_content = '<main' in html.lower() or '<article' in html.lower()
        
        # Check for Three.js in spiral renderer
        has_threejs = False
        if 'spiral' in description.lower():
            has_threejs = '<script' in html and ('three' in html.lower() or 'webgl' in html.lower())
        
        status = "✅" if (has_doctype and has_content) else "⚠️"
        print(f"{status} {description}")
        print(f"   URL: {url}")
        print(f"   HTML: {has_doctype}, Content: {has_content}, Nav: {has_nav}")
        if 'spiral' in description.lower():
            print(f"   Three.js: {has_threejs}")
        print()
        
        if not (has_doctype and has_content):
            all_passed = False
            
    except Exception as e:
        print(f"❌ {description}")
        print(f"   Error: {e}\n")
        all_passed = False

# Check files in _site
print("\n" + "-"*70)
site_dir = Path('_site')
if site_dir.exists():
    html_files = list(site_dir.rglob('*.html'))
    print(f"\nGenerated files: {len(html_files)} HTML files")
    print(f"Total site size: {sum(f.stat().st_size for f in html_files) / 1024:.1f} KB")
    
    # Check specific files
    critical_files = [
        'index.html',
        'goal-blindness.html',
        'spiral-field-renderer.html',
        'whitepaper.html',
    ]
    
    for cf in critical_files:
        file_path = site_dir / cf
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {cf} ({size} bytes)")
        else:
            print(f"  ✗ {cf} (MISSING)")
            all_passed = False

print("\n" + "="*70)
if all_passed:
    print("✅ VERIFICATION PASSED - Site is ready!")
else:
    print("⚠️  VERIFICATION INCOMPLETE - Check issues above")
print("="*70 + "\n")
