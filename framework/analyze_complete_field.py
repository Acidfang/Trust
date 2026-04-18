#!/usr/bin/env python3
"""
COMPREHENSIVE FIELD ANALYSIS
Read the entire SVG as ONE unified information field.
Compare it completely against the reference structure.
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
import json

def parse_svg(filepath):
    """Parse SVG and extract complete structure"""
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Count all elements
    rects = root.findall('.//svg:rect', ns)
    paths = root.findall('.//svg:path', ns)
    circles = root.findall('.//svg:circle', ns)
    lines = root.findall('.//svg:line', ns)
    texts = root.findall('.//svg:text', ns)
    
    # Extract text by section
    text_by_section = defaultdict(list)
    for text_elem in texts:
        y = float(text_elem.get('y', 0))
        text = text_elem.text or ""
        
        if y < 250: section = "HEADER"
        elif y < 530: section = "ROW1"
        elif y < 840: section = "ROW2"
        elif y < 1150: section = "ROW3"
        elif y < 1330: section = "CENTRAL"
        elif y < 1600: section = "CLOSING"
        else: section = "FOOTER"
        
        if text.strip():
            text_by_section[section].append(text.strip())
    
    # Count opacity distribution
    opacity_count = defaultdict(int)
    for elem in rects + circles + lines + paths:
        opacity = elem.get('opacity', '1.0')
        opacity_count[opacity] += 1
    
    return {
        'rects': len(rects),
        'paths': len(paths),
        'circles': len(circles),
        'lines': len(lines),
        'texts': len(texts),
        'total_visual': len(rects) + len(paths) + len(circles) + len(lines),
        'text_by_section': dict(text_by_section),
        'opacity_distribution': dict(opacity_count)
    }

# Run analysis
try:
    data = parse_svg('SYSTEM_BOUNDARIES_INFOGRAPHIC.svg')
    
    print("="*70)
    print("COMPREHENSIVE FIELD STRUCTURE ANALYSIS")
    print("="*70 + "\n")
    
    print("VISUAL ELEMENT COUNT:")
    print(f"  Rectangles: {data['rects']} (expected: ~13)")
    print(f"  Paths: {data['paths']} (expected: ~40+)")
    print(f"  Circles: {data['circles']} (expected: ~80+)")
    print(f"  Lines: {data['lines']} (expected: ~15+)")
    print(f"  Text elements: {data['texts']} (expected: ~35+)")
    print(f"  TOTAL VISUAL: {data['total_visual']}\n")
    
    print("OPACITY TIER DISTRIBUTION (Binary Hierarchy):")
    for opacity in sorted(data['opacity_distribution'].keys(), key=lambda x: float(x) if x != '1.0' else 1.0, reverse=True):
        count = data['opacity_distribution'][opacity]
        print(f"  {opacity}: {count:3d} elements")
    
    print("\nTEXT CONTENT BY SECTION:")
    for section in ['HEADER', 'ROW1', 'ROW2', 'ROW3', 'CENTRAL', 'CLOSING', 'FOOTER']:
        texts = data['text_by_section'].get(section, [])
        print(f"  {section}: {len(texts)} text items")
        for text in texts[:2]:
            print(f"    - {text[:50]}...")
    
    print("\n" + "="*70)
    print("FIELD COMPLETENESS CHECK")
    print("="*70)
    
    # Expected structure
    checks = {
        'ROW1 has at least 6 items': len(data['text_by_section'].get('ROW1', [])) >= 6,
        'ROW2 has at least 6 items': len(data['text_by_section'].get('ROW2', [])) >= 6,
        'ROW3 has at least 6 items': len(data['text_by_section'].get('ROW3', [])) >= 6,
        'CENTRAL has text': len(data['text_by_section'].get('CENTRAL', [])) > 0,
        'CLOSING has text': len(data['text_by_section'].get('CLOSING', [])) > 0,
        'FOOTER has text': len(data['text_by_section'].get('FOOTER', [])) > 0,
        'Total circles >= 80': data['circles'] >= 80,
        'Total paths >= 40': data['paths'] >= 40,
        'Opacity 0.8 present': '0.8' in data['opacity_distribution'],
        'Opacity 0.5 present': '0.5' in data['opacity_distribution'],
        'Opacity 0.3 present': '0.3' in data['opacity_distribution'],
    }
    
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    print("\n" + "="*70)
    print("WHAT'S COMPLETE vs. WHAT'S MISSING")
    print("="*70)
    
    complete = sum(1 for v in checks.values() if v)
    total = len(checks)
    print(f"Completeness: {complete}/{total} checks passed\n")
    
    if complete == total:
        print("The ENTIRE FIELD is COMPLETE.")
    else:
        print("GAPS IDENTIFIED:")
        for check, result in checks.items():
            if not result:
                print(f"  - {check}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
