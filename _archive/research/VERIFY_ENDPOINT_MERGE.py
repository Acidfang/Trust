#!/usr/bin/env python3
"""
Lightweight verification for merged endpoint - code structure only.

Checks that duplicate function definitions are removed without
requiring the full ChatDev runtime to load.
"""

import re
from pathlib import Path

def verify_merged_endpoint():
    """Check that serve_entity_image is defined once and routes are clean."""
    
    api_file = Path("c:\\Determined\\ENCYCLOPEDIA_API_SERVER.py")
    
    print("\n" + "=" * 70)
    print("ENDPOINT MERGE VERIFICATION")
    print("=" * 70)
    
    if not api_file.exists():
        print(f"✗ ERROR: {api_file} not found")
        return False
    
    with open(api_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count function definitions
    func_matches = re.findall(r'def serve_entity_image\(', content)
    route_matches = re.findall(r"@app\.route\('/api/image/<entity_name>'\)", content)
    
    print("\n[TEST 1] Function definition count")
    print("-" * 70)
    print(f"Found {len(func_matches)} definition(s) of 'serve_entity_image'")
    
    if len(func_matches) == 1:
        print("✓ Single function definition (GOOD)")
        func_ok = True
    else:
        print(f"✗ ERROR: Found {len(func_matches)} definitions (should be 1)")
        func_ok = False
    
    print("\n[TEST 2] Route decorator count")
    print("-" * 70)
    print(f"Found {len(route_matches)} route decorator(s) for '/api/image/<entity_name>'")
    
    if len(route_matches) == 1:
        print("✓ Single route definition (GOOD)")
        route_ok = True
    else:
        print(f"✗ ERROR: Found {len(route_matches)} routes (should be 1)")
        route_ok = False
    
    # Check function content for zoom support
    print("\n[TEST 3] Zoom parameter support")
    print("-" * 70)
    
    zoom_check_patterns = [
        r'request\.args\.get\([\'"]zoom[\'"]',
        r'generate_molecule_zoom_level',
        r'zoom_level = request\.args\.get',
    ]
    
    zoom_found = all(re.search(pattern, content) for pattern in zoom_check_patterns)
    
    if zoom_found:
        print("✓ Zoom parameter handling present")
        print("✓ Zoom level generator calls present")
        print("✓ Merged function contains both zoom and non-zoom logic")
        zoom_ok = True
    else:
        print("✗ Missing zoom parameter support")
        zoom_ok = False
    
    # Extract and check function body
    print("\n[TEST 4] Function signature and caching")
    print("-" * 70)
    
    func_pattern = r'def serve_entity_image\(entity_name\):.*?(?=\n@|if __name__|$)'
    func_matches = re.findall(func_pattern, content, re.DOTALL)
    
    if func_matches:
        func_body = func_matches[0]
        
        # Check for caching
        has_cache_check = 'cache_path.exists()' in func_body
        has_zoom_routing = "if zoom_level is not None:" in func_body
        has_error_handling = "except Exception as e:" in func_body
        
        print(f"Cache checking:    {'✓' if has_cache_check else '✗'}")
        print(f"Zoom routing:      {'✓' if has_zoom_routing else '✗'}")
        print(f"Error handling:    {'✓' if has_error_handling else '✗'}")
        
        sig_ok = has_cache_check and has_zoom_routing and has_error_handling
    else:
        print("✗ Could not find function body")
        sig_ok = False
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    all_ok = func_ok and route_ok and zoom_ok and sig_ok
    
    checks = [
        ("Single function definition", func_ok),
        ("Single route decorator", route_ok),
        ("Zoom parameter support", zoom_ok),
        ("Function signature & caching", sig_ok),
    ]
    
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
    
    print("\n" + "-" * 70)
    if all_ok:
        print("✓ MERGE VERIFICATION PASSED")
        print("\nChanges made:")
        print("  1. Merged serve_entity_image_with_zoom into serve_entity_image")
        print("  2. Removed duplicate function definition at line ~696")
        print("  3. Single endpoint now handles both zoom and non-zoom")
        print("  4. Zoom support: /api/image/Water Molecule?zoom=0-3")
        print("  5. Non-zoom fallback: /api/image/<entity_name>")
        return True
    else:
        print("✗ MERGE VERIFICATION FAILED")
        return False

if __name__ == '__main__':
    import sys
    success = verify_merged_endpoint()
    sys.exit(0 if success else 1)
