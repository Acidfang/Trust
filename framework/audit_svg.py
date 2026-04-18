#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sys

# Load SVG
try:
    tree = ET.parse('SYSTEM_BOUNDARIES_INFOGRAPHIC.svg')
    root = tree.getroot()
except Exception as e:
    print(f"Error loading SVG: {e}")
    sys.exit(1)

# Namespace handling
ns = {'svg': 'http://www.w3.org/2000/svg'}

# Extract text elements
texts = []
for text_elem in root.findall('.//svg:text', ns):
    if text_elem.text:
        texts.append({
            'x': text_elem.get('x'),
            'y': text_elem.get('y'),
            'class': text_elem.get('class'),
            'text': text_elem.text.strip(),
            'tspans': [t.text for t in text_elem.findall('svg:tspan', ns) if t.text]
        })

# Extract rects with opacity
rects = []
for rect_elem in root.findall('.//svg:rect', ns):
    x = rect_elem.get('x')
    y = rect_elem.get('y')
    opacity = rect_elem.get('opacity')
    if opacity:
        rects.append({
            'x': x, 'y': y, 'opacity': opacity,
            'stroke': rect_elem.get('stroke'),
            'stroke-width': rect_elem.get('stroke-width')
        })

print("=== CONTENT AUDIT ===\n")

# Group text by Y position
card_positions = {
    '270': 'ROW 1 - BOUNDARIES (Opacity 0.8)',
    '580': 'ROW 2 - LIMITS (Opacity 0.5)', 
    '890': 'ROW 3 - PARADOXES (Opacity 0.3)'
}

for y_pos, label in card_positions.items():
    print(f"\n{label}")
    card_texts = [t for t in texts if t.get('y') and int(t.get('y')) > int(y_pos) and int(t.get('y')) < int(y_pos) + 260]
    for t in sorted(card_texts, key=lambda x: int(x.get('x', 0))):
        if t.get('y'):  # All card content
            print(f"  {t['text']}")

print("\n\n=== VISUAL HIERARCHY AUDIT ===\n")
print("Opacity distribution (card borders):")
for opacity in ['0.8', '0.5', '0.3']:
    count = len([r for r in rects if r.get('opacity') == opacity and r.get('y') in ['270', '580', '890']])
    print(f"  {opacity}: {count} card borders (expected: 3)")

print("\n=== ICON AUDIT ===\n")
print("Icon primitives:")
paths = root.findall('.//svg:path', ns)
circles = root.findall('.//svg:circle', ns)
polygons = root.findall('.//svg:polygon', ns)
print(f"  Paths: {len(paths)}")
print(f"  Circles: {len(circles)}")
print(f"  Polygons: {len(polygons)}")
print(f"  TOTAL: {len(paths) + len(circles) + len(polygons)}")
print(f"  (Expected: ~24-27 for 9 cards with icons)")

print("\n=== CENTRAL STATEMENT AUDIT ===\n")
statement_texts = [t for t in texts if 'statement-text' in str(t.get('class', ''))]
for t in statement_texts:
    print(f"  {t['text']}")

print("\n=== CLOSING STATEMENTS AUDIT ===\n")
closing_texts = [t for t in texts if 'closing-text' in str(t.get('class', ''))]
for i, t in enumerate(closing_texts):
    combined = t['text']
    if t.get('tspans'):
        combined += ' ' + ' '.join(t['tspans'])
    print(f"  {i+1}. {combined}")

print("\n=== MEANING & INTENT CHECK ===\n")
print("Does the visual communicate:")
print("  1. Systems have boundaries? ", "✓ YES" if any('BOUNDARY' in t['text'] for t in texts) else "✗ MISSING")
print("  2. Systems have limits? ", "✓ YES" if any('LIMIT' in t['text'] for t in texts) else "✗ MISSING")
print("  3. Paradoxes/tension? ", "✓ YES" if any('PARADOX' in t['text'] for t in texts) else "✗ MISSING")
print("  4. Bounded yet can select? ", "✓ YES" if any('BOUNDED' in t['text'] and 'SELECT' in t['text'] for t in texts) else "✗ MISSING")

EOF
