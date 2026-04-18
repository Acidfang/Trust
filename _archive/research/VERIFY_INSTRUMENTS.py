#!/usr/bin/env python3
"""
INSTRUMENT VERIFICATION — Checking that all instruments know how they're playing

Date: April 3, 2026
Purpose: Verify that the new features (zoom, spider navigation) don't break existing instruments
"""

from FIELD_IMAGE_GENERATOR_V5 import DeterministicFieldBuilder

print("\n" + "="*80)
print("INSTRUMENT VERIFICATION — April 3, 2026")
print("Verifying that systems know how they're playing")
print("="*80)

b = DeterministicFieldBuilder()

# Test atomic-scale instruments (EXISTING)
print("\nATOMIC-SCALE INSTRUMENTS (EXISTING):\n")
atomic_tests = [
    ("Electron", lambda: b._generate_electron_measured()),
    ("Hydrogen Atom", lambda: b.generate_generic_atom_svg("Hydrogen", 1)),
    ("Water Molecule", lambda: b.generate_molecule_vsepr_svg("H₂O", "O", 8, [("H", 1), ("H", 1)], 2)),
    ("Carbon Atom", lambda: b.generate_generic_atom_svg("Carbon", 6)),
    ("Oxygen Atom", lambda: b.generate_generic_atom_svg("Oxygen", 8)),
]

atomic_pass = 0
for name, generator in atomic_tests:
    try:
        output = generator()
        is_valid = '<svg' in output and '</svg>' in output
        size = len(output)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        if is_valid:
            atomic_pass += 1
        print(f"  {name:25} | {size:6} bytes | {status}")
    except Exception as e:
        print(f"  {name:25} | ERROR: {str(e)[:45]}")

print(f"\n  Result: {atomic_pass}/{len(atomic_tests)} instruments playing correctly")

# Test zoom levels (NEW)
print("\nZOOM LEVEL INSTRUMENTS (NEW):\n")
zoom_tests = [
    ("Water Zoom 0 (Molecule)", lambda: b.generate_molecule_zoom_level("water", 0)),
    ("Water Zoom 1 (Atoms)", lambda: b.generate_molecule_zoom_level("water", 1)),
    ("Water Zoom 2 (Electrons)", lambda: b.generate_molecule_zoom_level("water", 2)),
    ("Water Zoom 3 (Orbitals)", lambda: b.generate_molecule_zoom_level("water", 3)),
]

zoom_pass = 0
for name, generator in zoom_tests:
    try:
        output = generator()
        is_valid = '<svg' in output and '</svg>' in output
        has_zoom = 'ZOOM' in output
        size = len(output)
        status = f"✓ VALID" if (is_valid and has_zoom) else "✗ INVALID"
        if is_valid and has_zoom:
            zoom_pass += 1
        print(f"  {name:30} | {size:6} bytes | {status}")
    except Exception as e:
        print(f"  {name:30} | ERROR: {str(e)[:40]}")

print(f"\n  Result: {zoom_pass}/{len(zoom_tests)} zoom levels working correctly")

# Test spider navigation (NEW)
print("\nSPIDER NAVIGATION INSTRUMENTS (NEW):\n")
spider_tests = [
    ("Water Spider", lambda: b.generate_complexity_cascade_spider("Water Molecule")),
    ("Electron Spider", lambda: b.generate_complexity_cascade_spider("Electron")),
]

spider_pass = 0
for name, generator in spider_tests:
    try:
        output = generator()
        is_valid = '<svg' in output and '</svg>' in output
        is_interactive = 'navigateTo' in output and 'onclick=' in output
        size = len(output)
        status = f"✓ INTERACTIVE" if (is_valid and is_interactive) else "✗ NOT INTERACTIVE"
        if is_valid and is_interactive:
            spider_pass += 1
        print(f"  {name:30} | {size:6} bytes | {status}")
    except Exception as e:
        print(f"  {name:30} | ERROR: {str(e)[:40]}")

print(f"\n  Result: {spider_pass}/{len(spider_tests)} spider views working correctly")

# Final summary
print("\n" + "="*80)
total_pass = atomic_pass + zoom_pass + spider_pass
total_tests = len(atomic_tests) + len(zoom_tests) + len(spider_tests)
print(f"OVERALL RESULT: {total_pass}/{total_tests} instruments verified")
print("="*80)

if total_pass == total_tests:
    print("✓ ALL INSTRUMENTS KNOW HOW THEY'RE PLAYING\n")
else:
    print(f"✗ {total_tests - total_pass} instruments need attention\n")
