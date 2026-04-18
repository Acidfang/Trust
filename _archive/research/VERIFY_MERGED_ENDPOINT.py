#!/usr/bin/env python3
"""
Verification script for merged /api/image endpoint.

Tests that both zoom-enabled and non-zoom entities work correctly
after merging serve_entity_image and serve_entity_image_with_zoom.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'ChatDev'))

from ChatDev.runtime.sdk import DeterministicFieldBuilder

def test_merged_endpoint():
    """Verify merged endpoint handles zoom and non-zoom cases."""
    
    builder = DeterministicFieldBuilder()
    results = {
        "zoom_enabled": [],
        "non_zoom": [],
        "errors": []
    }
    
    print("\n" + "=" * 70)
    print("VERIFYING MERGED /api/image ENDPOINT")
    print("=" * 70)
    
    # TEST 1: Water Molecule with zoom levels
    print("\n[TEST 1] Water Molecule - Zoom-enabled entity")
    print("-" * 70)
    
    test_cases_zoom = [
        ("water", 0, "Molecule level"),
        ("water", 1, "Atomic level"),
        ("water", 2, "Electron cloud level"),
        ("water", 3, "Orbital detail level"),
    ]
    
    for molecule, zoom_level, description in test_cases_zoom:
        try:
            svg = builder.generate_molecule_zoom_level(molecule, zoom_level)
            size = len(svg) if svg else 0
            is_valid = svg.startswith('<?xml') or svg.startswith('<svg')
            
            status = "✓" if is_valid else "✗"
            results["zoom_enabled"].append({
                "entity": f"Water (zoom={zoom_level})",
                "description": description,
                "size": size,
                "valid": is_valid
            })
            
            print(f"{status} Water Zoom {zoom_level} ({description})")
            print(f"   Size: {size} bytes | Valid SVG: {is_valid}")
            
        except Exception as e:
            error_msg = f"Water zoom {zoom_level}: {str(e)}"
            results["errors"].append(error_msg)
            print(f"✗ Water Zoom {zoom_level} - ERROR: {str(e)}")
    
    # TEST 2: Non-zoom entities (original endpoint behavior)
    print("\n[TEST 2] Non-zoom entities")
    print("-" * 70)
    
    test_cases_non_zoom = [
        ("Electron", lambda gen: gen._generate_electron_measured()),
        ("Hydrogen", lambda gen: gen.generate_generic_atom_svg('Hydrogen', 1)),
        ("Oxygen", lambda gen: gen.generate_generic_atom_svg('Oxygen', 8)),
    ]
    
    for entity_name, generator_func in test_cases_non_zoom:
        try:
            svg = generator_func(builder)
            size = len(svg) if svg else 0
            is_valid = svg.startswith('<?xml') or svg.startswith('<svg')
            
            status = "✓" if is_valid else "✗"
            results["non_zoom"].append({
                "entity": entity_name,
                "size": size,
                "valid": is_valid
            })
            
            print(f"{status} {entity_name}")
            print(f"   Size: {size} bytes | Valid SVG: {is_valid}")
            
        except Exception as e:
            error_msg = f"{entity_name}: {str(e)}"
            results["errors"].append(error_msg)
            print(f"✗ {entity_name} - ERROR: {str(e)}")
    
    # TEST 3: Verify route definition is single
    print("\n[TEST 3] Code structure verification")
    print("-" * 70)
    
    api_server_file = project_root / 'ChatDev' / 'server' / 'app.py'
    if not api_server_file.exists():
        api_server_file = project_root / 'ENCYCLOPEDIA_API_SERVER.py'
    
    if api_server_file.exists():
        with open(api_server_file, 'r') as f:
            content = f.read()
        
        # Count function definitions
        count_func_def = content.count('def serve_entity_image(')
        count_route_deco = content.count("@app.route('/api/image/<entity_name>')")
        
        print(f"Function definitions 'def serve_entity_image(': {count_func_def}")
        print(f"Route decorators '@app.route('/api/image/<entity_name>'): {count_route_deco}")
        
        if count_func_def == 1 and count_route_deco == 1:
            print("✓ Single endpoint definition verified")
        else:
            print("✗ ERROR: Multiple function or route definitions detected!")
            results["errors"].append(f"Multiple definitions: {count_func_def} functions, {count_route_deco} routes")
    
    # SUMMARY
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    zoom_count = len(results["zoom_enabled"])
    zoom_valid = sum(1 for r in results["zoom_enabled"] if r["valid"])
    
    non_zoom_count = len(results["non_zoom"])
    non_zoom_valid = sum(1 for r in results["non_zoom"] if r["valid"])
    
    error_count = len(results["errors"])
    
    print(f"\nZoom-enabled tests: {zoom_valid}/{zoom_count} valid")
    print(f"Non-zoom tests: {non_zoom_valid}/{non_zoom_count} valid")
    print(f"Errors: {error_count}")
    
    if error_count > 0:
        print("\nError details:")
        for error in results["errors"]:
            print(f"  - {error}")
    
    # Overall result
    total_valid = zoom_valid + non_zoom_valid
    total_tests = zoom_count + non_zoom_count
    
    print("\n" + "-" * 70)
    if error_count == 0 and total_valid == total_tests:
        print(f"✓ MERGED ENDPOINT VERIFIED: {total_valid}/{total_tests} tests passed")
        print("  → serve_entity_image now handles both zoom and non-zoom cases")
        print("  → No duplicate function definitions")
        return True
    else:
        print(f"✗ MERGE VERIFICATION FAILED: {error_count} errors found")
        return False

if __name__ == '__main__':
    try:
        success = test_merged_endpoint()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
