#!/usr/bin/env python3
"""
COMPREHENSIVE FIELD ANALYSIS
Read the entire information field at once.
Compare reference vs. current as unified systems.
Identify ALL differences simultaneously.
"""

import xml.etree.ElementTree as ET
import json
from collections import defaultdict

# ============= PARSE CURRENT SVG AS COMPLETE FIELD =============

def parse_svg_complete(filepath):
    """Parse SVG and extract COMPLETE structure as one field"""
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    field = {
        'viewBox': root.get('viewBox'),
        'dimensions': {'width': 1400, 'height': 1800},
        'sections': {},
        'all_elements': [],
        'text_inventory': [],
        'visual_hierarchy': [],
        'decorative_elements': [],
        'connectors': []
    }
    
    # Extract ALL text as unified message
    texts = root.findall('.//svg:text', ns)
    text_messages = []
    for text_elem in texts:
        y = float(text_elem.get('y', 0))
        x = float(text_elem.get('x', 0))
        text = text_elem.text or ""
        tspans = [t.text for t in text_elem.findall('svg:tspan', ns) if t.text]
        full_text = text + " ".join(tspans)
        
        # Categorize by Y position (section detection)
        if y < 250: section = "HEADER"
        elif y < 530: section = "ROW1_BOUNDARIES"
        elif y < 840: section = "ROW2_LIMITS"
        elif y < 1150: section = "ROW3_PARADOXES"
        elif y < 1330: section = "CENTRAL_STATEMENT"
        elif y < 1600: section = "CLOSING_STATEMENTS"
        else: section = "FOOTER"
        
        text_messages.append({
            'text': full_text.strip(),
            'x': x,
            'y': y,
            'section': section,
            'class': text_elem.get('class', '')
        })
    
    field['text_inventory'] = sorted(text_messages, key=lambda t: t['y'])
    
    # Extract ALL visual elements (rects, paths, circles)
    rects = root.findall('.//svg:rect', ns)
    paths = root.findall('.//svg:path', ns)
    circles = root.findall('.//svg:circle', ns)
    lines = root.findall('.//svg:line', ns)
    polygons = root.findall('.//svg:polygon', ns)
    
    field['visual_hierarchy'] = {
        'rects': len(rects),
        'paths': len(paths),
        'circles': len(circles),
        'lines': len(lines),
        'polygons': len(polygons),
        'total': len(rects) + len(paths) + len(circles) + len(lines) + len(polygons)
    }
    
    # Categorize visual elements by opacity (tier hierarchy)
    opacity_distribution = defaultdict(int)
    for elem in rects + paths + circles + lines:
        opacity = elem.get('opacity', '1.0')
        opacity_distribution[opacity] += 1
    
    field['opacity_tiers'] = dict(opacity_distribution)
    
    # Look for connectors (vertical lines between sections)
    connectors_found = []
    for line in lines:
        x1, y1 = float(line.get('x1', 0)), float(line.get('y1', 0))
        x2, y2 = float(line.get('x2', 0)), float(line.get('y2', 0))
        if x1 == x2:  # Vertical line
            connectors_found.append({
                'type': 'vertical_line',
                'x': x1,
                'y_range': (y1, y2),
                'stroke_width': line.get('stroke-width'),
                'opacity': line.get('opacity')
            })
    
    for path in paths:
        d = path.get('d', '')
        if 'M' in d and 'L' in d:
            connectors_found.append({
                'type': 'path_line',
                'd': d,
                'opacity': path.get('opacity')
            })
    
    field['connectors'] = connectors_found
    
    # Decorative elements (accent circles, accent paths)
    decorative = []
    for circle in circles:
        opacity = float(circle.get('opacity', '1.0'))
        if opacity <= 0.25:  # Likely decorative
            decorative.append({
                'type': 'accent_circle',
                'cx': circle.get('cx'),
                'cy': circle.get('cy'),
                'r': circle.get('r'),
                'opacity': circle.get('opacity')
            })
    
    field['decorative_elements'] = decorative
    
    return field

# ============= ANALYZE REFERENCE IMAGE VISUALLY =============

def analyze_reference_structure():
    """
    Analyze what the reference image SHOWS as a complete field
    (This is based on visual inspection of the reference PNG)
    """
    reference = {
        'title': 'ANTIPATTERN_REFERENCE_VERIFIED',
        'expected_structure': {
            'HEADER': {
                'title': 'Main title spanning 2 lines',
                'subtitle': 'Subtitle explaining concept',
                'decorative': 'Corner accents, accent paths'
            },
            'ROW1_BOUNDARIES': {
                'cards': 3,
                'opacity': 0.8,
                'titles': ['PERCEPTUAL BOUNDARY', 'REPRESENTATIONAL BOUNDARY', 'ACTION BOUNDARY'],
                'icons': 'Distinct visual representations for each concept',
                'structure': 'Card grid (360x260px each)'
            },
            'ROW2_LIMITS': {
                'cards': 3,
                'opacity': 0.5,
                'titles': ['RECURSION LIMIT', 'PREDICTION LIMIT', 'CONTROL LIMIT'],
                'icons': 'Distinct visual representations',
                'structure': 'Card grid (360x260px each)'
            },
            'ROW3_PARADOXES': {
                'cards': 3,
                'opacity': 0.3,
                'titles': ['IDENTITY PARADOX', 'FREEDOM PARADOX', 'META-LIMIT'],
                'icons': 'Distinct visual representations',
                'structure': 'Card grid (360x260px each)'
            },
            'VISUAL_CONTINUITY': {
                'row_connectors': 'Vertical lines at x=230, 690, 1150 connecting rows',
                'accent_dots': 'Dots at row boundaries and junctions',
                'frame_decorations': 'Corner circles, accent paths for section framing'
            },
            'CENTRAL_STATEMENT': {
                'text': 'YOU ARE BOUNDED. BUT YOU STILL SELECT.',
                'framing': 'Horizontal lines above and below, corner accents',
                'positioning': 'Centered, emphasized'
            },
            'CLOSING_STATEMENTS': {
                'count': 5,
                'box': 'Bounding rectangle with corner accent circles',
                'structure': 'Two groups (3 + divider + 2)',
                'decorative_divider': 'Line with accent dots'
            },
            'FOOTER': {
                'message': 'You are what you select. And you are shaped by what you cannot.',
                'metadata': 'System Boundaries Framework | Date | Complete Architecture',
                'decoration': 'Base accent path with circles'
            }
        },
        'key_characteristics': [
            'Complete visual continuity from header to footer',
            'No orphaned sections or visual gaps',
            'Every section framed and connected',
            'Opacity-tier encoding throughout (0.8 → 0.5 → 0.3)',
            'Decorative elements fill empty zones',
            'Connector lines create vertical visual flow',
            'Balanced visual weight top-to-bottom'
        ]
    }
    return reference

# ============= COMPREHENSIVE COMPARISON =============

def compare_fields(current_field, reference_structure):
    """Compare complete current field against complete reference structure"""
    
    delta = {
        'status': 'COMPREHENSIVE DELTA ANALYSIS',
        'timestamp': '2026-04-11',
        'sections': {}
    }
    
    # 1. TEXT CONTENT AUDIT
    print("\n" + "="*80)
    print("SECTION 1: TEXT CONTENT COMPLETENESS")
    print("="*80)
    
    text_by_section = defaultdict(list)
    for text_item in current_field['text_inventory']:
        text_by_section[text_item['section']].append(text_item['text'])
    
    expected_content = {
        'HEADER': {'THE LIMITS OF', 'KNOWLEDGE & CONTROL', 'Every complete system'},
        'ROW1_BOUNDARIES': {'PERCEPTUAL', 'REPRESENTATIONAL', 'ACTION', 'BOUNDARY'},
        'ROW2_LIMITS': {'RECURSION', 'PREDICTION', 'CONTROL', 'LIMIT'},
        'ROW3_PARADOXES': {'IDENTITY', 'FREEDOM', 'META-LIMIT', 'PARADOX'},
        'CENTRAL_STATEMENT': {'YOU ARE BOUNDED', 'STILL SELECT'},
        'CLOSING_STATEMENTS': {'system can', 'escapes'},
        'FOOTER': {'what you select', 'shaped by'}
    }
    
    for section, expected in expected_content.items():
        found_texts = text_by_section.get(section, [])
        found_set = set()
        for text in found_texts:
            for keyword in expected:
                if keyword.lower() in text.lower():
                    found_set.add(keyword)
        
        missing = expected - found_set
        status = "✓ COMPLETE" if not missing else f"✗ MISSING: {missing}"
        print(f"{section}: {status}")
        delta['sections'][section] = {
            'text_found': len(found_set),
            'expected': len(expected),
            'missing': list(missing) if missing else []
        }
    
    # 2. VISUAL HIERARCHY AUDIT
    print("\n" + "="*80)
    print("SECTION 2: VISUAL STRUCTURE")
    print("="*80)
    
    visual = current_field['visual_hierarchy']
    print(f"Current visual inventory:")
    print(f"  Rectangles (cards/frames): {visual['rects']}")
    print(f"  Paths (icons, connectors): {visual['paths']}")
    print(f"  Circles (icon parts, accents): {visual['circles']}")
    print(f"  Lines: {visual['lines']}")
    print(f"  TOTAL VISUAL ELEMENTS: {visual['total']}")
    
    # Expected visual counts
    expected_visual = {
        'card_borders': 9,  # 3x3 grid
        'card_icons': 27,   # 9 cards × 3 elements each (approx)
        'row_connectors': 9,  # Vertical lines between rows (3 columns × 3 sets)
        'decorative_accents': 30,  # Corner circles, accent dots, accent paths
        'section_frames': 5,  # Header, central statement, closing statements, footer frames
    }
    
    delta['visual_structure'] = {
        'current_total': visual['total'],
        'expected_minimum': sum(expected_visual.values())
    }
    
    # 3. OPACITY TIER DISTRIBUTION
    print("\n" + "="*80)
    print("SECTION 3: OPACITY TIER ENCODING (Binary Hierarchy)")
    print("="*80)
    
    opcity = current_field['opacity_tiers']
    print("Opacity distribution (should follow 0.8 → 0.5 → 0.3 → decorative cascade):")
    for opacity in sorted(opcity.keys(), key=float, reverse=True):
        count = opcity[opacity]
        tier = f"TIER: Main (0.8)" if opacity == '0.8' else \
               f"TIER: Secondary (0.5)" if opacity == '0.5' else \
               f"TIER: Tertiary (0.3)" if opacity == '0.3' else \
               f"TIER: Decorative (≤0.25)"
        print(f"  {opacity}: {count:3d} elements - {tier}")
    
    delta['opacity_distribution'] = opcity
    
    # 4. CONNECTOR AUDIT
    print("\n" + "="*80)
    print("SECTION 4: VISUAL CONNECTORS (Continuity Check)")
    print("="*80)
    
    connectors = current_field['connectors']
    print(f"Found {len(connectors)} connector elements")
    
    # Count vertical connectors (should link rows)
    vertical_connectors = [c for c in connectors if c['type'] == 'vertical_line']
    print(f"  Vertical connectors: {len(vertical_connectors)}")
    
    # Expected: 3 columns × 3 row-connections = 9 vertical lines
    expected_vertical = 9
    print(f"  Expected minimum: {expected_vertical}")
    print(f"  Status: {'✓ SUFFICIENT' if len(vertical_connectors) >= expected_vertical else '✗ INSUFFICIENT'}")
    
    delta['connectors'] = {
        'vertical_found': len(vertical_connectors),
        'vertical_expected': expected_vertical,
        'path_connectors': len([c for c in connectors if c['type'] == 'path_line'])
    }
    
    # 5. DECORATIVE ELEMENT AUDIT
    print("\n" + "="*80)
    print("SECTION 5: DECORATIVE ELEMENTS (Space Fill Check)")
    print("="*80)
    
    decorative = current_field['decorative_elements']
    print(f"Found {len(decorative)} decorative accent elements")
    print(f"Expected: ~30-40 (corner circles, accent dots throughout)")
    print(f"Status: {'✓ ADEQUATE' if len(decorative) >= 25 else '✗ SPARSE'}")
    
    delta['decorative_elements'] = {
        'found': len(decorative),
        'expected_minimum': 25
    }
    
    # 6. SECTION FRAMING AUDIT
    print("\n" + "="*80)
    print("SECTION 6: SECTION FRAMING & ANCHORING")
    print("="*80)
    
    sections_to_frame = ['HEADER', 'CENTRAL_STATEMENT', 'CLOSING_STATEMENTS', 'FOOTER']
    framed_count = 0
    for line in current_field['connectors']:
        if 'path' in str(line).lower() or 'rect' in str(line).lower():
            framed_count += 1
    
    print("Sections requiring frame/anchor decorations:")
    print(f"  HEADER: Corner accents + accent paths")
    print(f"  CENTRAL_STATEMENT: Horizontal lines + corner decorations")
    print(f"  CLOSING_STATEMENTS: Bounding box + corner circles + divider")
    print(f"  FOOTER: Line frame + accent decorations")
    print(f"\nFrame elements detected: {framed_count}")
    
    # 7. COMPREHENSIVE DELTA SUMMARY
    print("\n" + "="*80)
    print("COMPREHENSIVE DELTA SUMMARY: What's Missing?")
    print("="*80)
    
    missing_items = []
    
    # Check each major component
    if len(vertical_connectors) < 9:
        missing_items.append(f"CRITICAL: Row connector lines ({len(vertical_connectors)}/9)")
    
    if len(decorative) < 25:
        missing_items.append(f"HIGH: Decorative accent elements ({len(decorative)}/25+)")
    
    for section, data in delta['sections'].items():
        if data['missing']:
            missing_items.append(f"TEXT: {section} missing {data['missing']}")
    
    if not missing_items:
        print("✓ COMPLETE: Field appears structurally sound")
    else:
        print("Identified gaps:")
        for i, item in enumerate(missing_items, 1):
            print(f"  {i}. {item}")
    
    delta['missing_items'] = missing_items
    
    # 8. THE UNIFIED FIELD PICTURE
    print("\n" + "="*80)
    print("THE UNIFIED FIELD: What you're building")
    print("="*80)
    print("The entire SVG is ONE information field:")
    print("  - HEADER to FOOTER is a continuous message")
    print("  - Opacity hierarchy encodes conceptual tiers")
    print("  - Connectors create visual flow")
    print("  - Decorative elements prevent visual gaps")
    print("  - Each section must be FRAMED")
    print("")
    print("The field is COMPLETE when:")
    print("  1. All text content present")
    print("  2. All 9 cards filled with content")
    print("  3. All rows connected by vertical lines")
    print("  4. All sections framed/anchored")
    print("  5. No visual gaps")
    print("  6. Opacity tiers applied consistently")
    
    return delta

# ============= EXECUTION =============

if __name__ == '__main__':
    print("COMPREHENSIVE FIELD ANALYSIS")
    print("Reading ALL information at once...\n")
    
    # Parse current SVG as complete field
    current = parse_svg_complete('SYSTEM_BOUNDARIES_INFOGRAPHIC.svg')
    
    # Get reference structure analysis
    reference = analyze_reference_structure()
    
    # Compare as unified systems
    delta = compare_fields(current, reference)
    
    # Output delta to JSON for programmatic inspection
    with open('FIELD_ANALYSIS_DELTA.json', 'w') as f:
        json.dump(delta, f, indent=2)
    
    print("\n" + "="*80)
    print("Analysis complete. Delta saved to FIELD_ANALYSIS_DELTA.json")
    print("="*80)
