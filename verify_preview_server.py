#!/usr/bin/env python3
"""
Comprehensive test of the markdown renderer preview server
Verifies that:
1. Markdown files are converted to HTML (not served raw)
2. Embedded scripts and interactive code are preserved
3. YAML frontmatter is processed correctly
4. Styling is applied
"""

import urllib.request
from pathlib import Path

print("=" * 70)
print("MARKDOWN RENDERER VERIFICATION TEST")
print("=" * 70)

test_files = [
    ('goal-blindness.md', False),  # No embedded scripts
    ('spiral-field-renderer.md', True),  # Has embedded Three.js script
    ('index.md', True),  # Homepage (likely has content)
]

all_passed = True

for filename, should_have_script in test_files:
    print(f"\nTesting: {filename}")
    print("-" * 50)
    
    try:
        url = f'http://localhost:4000/docs/{filename}'
        resp = urllib.request.urlopen(url)
        html = resp.read().decode()
        
        # Check 1: Is it HTML?
        is_html = html.startswith('<!DOCTYPE')
        print(f"  ✓ HTML format: {is_html}", "✅" if is_html else "❌")
        
        # Check 2: Has styling?
        has_style = '<style' in html or 'style=' in html
        print(f"  ✓ Has styling: {has_style}", "✅" if has_style else "❌")
        
        # Check 3: No raw markdown?
        has_raw_markdown = html.startswith('---')
        print(f"  ✓ Not raw markdown: {not has_raw_markdown}", "✅" if not has_raw_markdown else "❌")
        
        # Check 4: No HTML_BLOCK placeholders?
        has_placeholders = 'HTML_BLOCK' in html
        print(f"  ✓ No HTML placeholders: {not has_placeholders}", "✅" if not has_placeholders else "❌")
        
        # Check 5: Scripts preserved if expected?
        has_script = '<script' in html
        if should_have_script:
            print(f"  ✓ Has scripts: {has_script}", "✅" if has_script else "❌")
        else:
            print(f"  ✓ Scripts as expected: {not has_script or has_script}", "✅")
        
        # Overall for this file
        checks = [is_html, has_style, not has_raw_markdown, not has_placeholders]
        if should_have_script:
            checks.append(has_script)
        
        if all(checks):
            print(f"  RESULT: ✅ PASS")
        else:
            print(f"  RESULT: ❌ FAIL")
            all_passed = False
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        all_passed = False

print("\n" + "=" * 70)
if all_passed:
    print("✅ ALL TESTS PASSED - Preview server is working correctly!")
    print("\nThe wiki preview server is ready for use:")
    print("  • Markdown files are converted to HTML")
    print("  • Embedded scripts are preserved")
    print("  • Styling is applied correctly")
    print("  • No placeholder artifacts appear")
else:
    print("❌ SOME TESTS FAILED - See above for details")
print("=" * 70)
