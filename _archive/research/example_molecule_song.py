#!/usr/bin/env python
"""
Example: Complex Molecule Rendered as Song

Shows how a real molecular structure becomes a universal song,
translated to all output formats, and composed into election sequence.
"""

from UNIVERSAL_RENDERER import (
    render_with_song_layer,
    get_election_meta_song,
    get_election_sequence,
    clear_election_sequence,
    detect_container_type
)

print("=" * 90)
print("COMPLEX MOLECULE AS SONG - Universal Renderer Example")
print("=" * 90)

# Clear previous elections
clear_election_sequence()

# Define a complex molecule: Benzene (C6H6) - aromatic ring
class Benzene:
    """Benzene molecule: 6-membered aromatic ring (C6H6)"""
    def __init__(self):
        # Atoms in 3D space (hexagon in a plane)
        import math
        self.name = "Benzene (C6H6)"
        self.atoms = []
        self.bonds = []
        
        # Carbon atoms in hexagon (radius 1.4 Angstroms)
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = 1.4 * math.cos(angle)
            y = 1.4 * math.sin(angle)
            self.atoms.append(("C", x, y, 0.0))
        
        # Hydrogen atoms (1.1 Angstroms from carbons)
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = 2.5 * math.cos(angle)
            y = 2.5 * math.sin(angle)
            self.atoms.append(("H", x, y, 0.0))
        
        # C-C bonds (alternating single/double for aromatic)
        for i in range(6):
            next_i = (i + 1) % 6
            bond_order = 1.5  # Aromatic bonds
            self.bonds.append((i, next_i, bond_order))
        
        # C-H bonds
        for i in range(6):
            self.bonds.append((i, 6 + i, 1.0))

# Define another complex molecule: Water (H2O) for comparison
class Water:
    """Water molecule: bent geometry (H2O)"""
    def __init__(self):
        self.name = "Water (H2O)"
        # Bent geometry (104.5 degree bond angle)
        self.atoms = [
            ("O", 0.0, 0.0, 0.0),
            ("H", 0.96, 0.0, 0.0),
            ("H", -0.24, 0.93, 0.0),
        ]
        self.bonds = [
            (0, 1, 1.0),  # O-H
            (0, 2, 1.0),  # O-H
        ]

print("\n" + "=" * 90)
print("COMPLEX MOLECULE: BENZENE (C6H6)")
print("=" * 90)

benzene = Benzene()

print(f"\nStructure: {benzene.name}")
print(f"Atoms: {len(benzene.atoms)}")
print(f"  - 6 Carbon atoms (sp2 hybridized)")
print(f"  - 6 Hydrogen atoms")
print(f"  - Total: 12 atoms")
print(f"Bonds: {len(benzene.bonds)}")
print(f"  - 6 aromatic C-C bonds (order 1.5)")
print(f"  - 6 C-H bonds (order 1.0)")
print(f"Geometry: Planar hexagon (D6h symmetry)")

print("\n" + "-" * 90)
print("DETECTED AS: ", end="")
detected = detect_container_type(benzene)
print(f"'{detected}' (primitive container)")

print("\n" + "-" * 90)
print("RENDERING BENZENE IN DIFFERENT FORMATS:")
print("-" * 90)

# Symbol format (ultra-compact)
symbol = render_with_song_layer(benzene, "symbol")
print(f"\n1. SYMBOL (ultra-compact, recovery-ready):")
print(f"   {symbol}")

# Verse format (human-memorable)
verse = render_with_song_layer(benzene, "verse")
print(f"\n2. VERSE (human-memorable poetry):")
for line in verse.split("\n"):
    print(f"   {line}")

# JSON format (structured data)
json_result = render_with_song_layer(benzene, "json")
print(f"\n3. JSON (structured):")
print(f"   Principle: {json_result['principle']}")
print(f"   Container: {json_result['type']}")
print(f"   Weight: {json_result['weight']:.0%}")

# Markdown format (documentation)
markdown = render_with_song_layer(benzene, "markdown")
print(f"\n4. MARKDOWN (documentation):")
print("   " + markdown.replace("\n", "\n   "))

# SVG format (visual)
svg = render_with_song_layer(benzene, "svg")
print(f"\n5. SVG (visual):")
print(f"   [SVG generated - {len(svg)} characters]")
print(f"   Would render as visual diagram in browser")

print("\n" + "=" * 90)
print("COMPARISON: WATER (H2O)")
print("=" * 90)

water = Water()

print(f"\nStructure: {water.name}")
print(f"Atoms: {len(water.atoms)}")
print(f"Bonds: {len(water.bonds)}")
print(f"Geometry: Bent (C2v symmetry)")

water_symbol = render_with_song_layer(water, "symbol")
print(f"\nWater Symbol: {water_symbol}")

print("\n" + "=" * 90)
print("ELECTION SEQUENCE META-SONG (Both Molecules)")
print("=" * 90)

print(f"\nRendered in order:")
print(f"  1. Benzene (6-12 atoms, aromatic)")
print(f"  2. Water (3 atoms, bent)")

print(f"\nElection Symbols in Order:")
meta_symbols = get_election_meta_song("symbol")
print(f"  {meta_symbols}")

print(f"\nElection Sequence:")
sequence = get_election_sequence()
for i, election in enumerate(sequence, 1):
    print(f"\n  {i}. {election['principle']}")
    print(f"     Molecule: {election['container_type']}")
    print(f"     Symbols: {election['symbols']}")

print(f"\nComplete Meta-Verse (concatenated in election order):")
meta_verse = get_election_meta_song("verse")
print("-" * 90)
# Show first part for both molecules
parts = meta_verse.split("\n\n")
for i, part in enumerate(parts[:2], 1):
    print(f"\n[Molecule {i}]")
    for line in part.split("\n"):
        print(f"  {line}")

print("\n" + "=" * 90)
print("KEY INSIGHTS")
print("=" * 90)

print("""
✓ BENZENE (complex, aromatic):
  • 12 atoms, 12 bonds, planar hexagon
  • Rendered as CONSTRAINT_creates_DEPTH (structure from constraints)
  • Symbol: ⊙ → ◯ (Δ constraint) - shows geometric definition
  • Verse: Describes how structure emerges from constraints

✓ WATER (simple, bent):
  • 3 atoms, 2 bonds, bent geometry
  • Also rendered as CONSTRAINT_creates_DEPTH (same principle)
  • Why? Because both are structures emerging from atomic physics constraints
  • Domain-agnostic: principle applies to any structure

✓ ELECTION SEQUENCE:
  • Reading both molecules' verses in order = complete output song
  • Each molecule contributes its narrative
  • Meta-song captures the full story of the analysis
  • Symbols show the decision flow visually

✓ OUTPUT AGNOSTICISM:
  • Same molecule → different formats
  • Benzene as symbol: ⊙ → ◯ (Δ constraint)
  • Benzene as verse: human-readable poetry
  • Benzene as JSON: structured computational form
  • Benzene as SVG: visual diagram
  • USER CHOOSES OUTPUT - renderer adapts
""")

print("=" * 90)
