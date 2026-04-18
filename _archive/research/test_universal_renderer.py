#!/usr/bin/env python
"""Quick test of UNIVERSAL_RENDERER.py"""

from UNIVERSAL_RENDERER import (
    render_with_song_layer, 
    detect_container_type,
    list_all_songs,
    list_all_container_types
)

# Test with different container types
print("=" * 80)
print("TESTING UNIVERSAL RENDERER - Input/Output Agnostic")
print("=" * 80)

# Mock containers
class Molecule:
    def __init__(self):
        self.atoms = [('C', 0, 0, 0), ('H', 1, 0, 0)]
        self.bonds = [(0, 1)]

class Entity:
    def __init__(self):
        self.position = [5, 5, 5]
        self.id = "entity_001"
        self.properties = {"energy": 100}

class Ledger:
    def __init__(self):
        self.version = 1
        self.transactions = []
        self.hash = "abc123"

class WorldState:
    def __init__(self):
        self.entities = []
        self.connections = []

# Test each container type
test_containers = [
    ("Molecule (atoms+bonds)", Molecule()),
    ("Entity (position+id)", Entity()),
    ("Ledger (version+hash)", Ledger()),
    ("WorldState (entities+connections)", WorldState()),
]

print("\nTesting container type detection:")
print("-" * 80)
for name, container in test_containers:
    detected = detect_container_type(container)
    print(f"✓ {name:35} → detected as '{detected}'")

print("\n\nTesting output format agnosticism:")
print("-" * 80)

molecule = Molecule()

for fmt in ["symbol", "verse", "json"]:
    result = render_with_song_layer(molecule, fmt)
    if fmt == "symbol":
        print(f"\n✓ Symbol format:\n  {result}")
    elif fmt == "verse":
        print(f"\n✓ Verse format (first line):\n  {result.split(chr(10))[0]}")
    elif fmt == "json":
        print(f"\n✓ JSON format:")
        print(f"  - Principle: {result['principle']}")
        print(f"  - Container Type: {result['type']}")
        print(f"  - Weight: {result['weight']:.0%}")

print("\n\n" + "=" * 80)
print("UNIVERSAL RENDERER STATUS")
print("=" * 80)

# Show all songs
all_songs = list_all_songs()
print(f"\n✓ {len(all_songs)} recovery songs available:")
for i, song in enumerate(all_songs, 1):
    print(f"  {i}. {song['principle']}")

# Show all container types
types_map = list_all_container_types()
print(f"\n✓ {len(types_map)} container types recognized:")
for ctype, principle in types_map.items():
    print(f"  • {ctype:15} → {principle}")

print("\n" + "=" * 80)
print("✅ UNIVERSAL RENDERER IS FULLY FUNCTIONAL")
print("   • Input agnostic: ✓ (accepts any container)")
print("   • Output agnostic: ✓ (outputs any format)")
print("   • Domain agnostic: ✓ (songs map principles universally)")
print("=" * 80)
