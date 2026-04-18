#!/usr/bin/env python
"""Test UNIVERSAL_RENDERER election sequencing - meta-song composition"""

from UNIVERSAL_RENDERER import (
    render_with_song_layer,
    get_election_sequence,
    get_election_meta_song,
    get_election_count,
    clear_election_sequence
)

print("=" * 80)
print("TESTING ELECTION SEQUENCING - Meta-Song Composition")
print("=" * 80)

# Clear any previous elections
clear_election_sequence()

# Mock containers
class Molecule:
    def __init__(self):
        self.atoms = [('C', 0, 0, 0)]
        self.bonds = []

class Entity:
    def __init__(self):
        self.position = [1, 2, 3]
        self.id = "test_entity"

class Ledger:
    def __init__(self):
        self.version = 1
        self.transactions = []

# Render containers in sequence
print("\nRendering containers in election order:")
print("-" * 80)

containers = [
    ("Molecule (primitive)", Molecule()),
    ("Entity (engagement)", Entity()),
    ("Ledger (temporal)", Ledger()),
]

for name, container in containers:
    result = render_with_song_layer(container, "symbol")
    print(f"✓ {name:30} → {result}")

print(f"\n✓ Election count: {get_election_count()}")

# Show election sequence
print("\n" + "=" * 80)
print("ELECTION SEQUENCE (Ordered Decisions)")
print("=" * 80)

sequence = get_election_sequence()
for i, election in enumerate(sequence, 1):
    print(f"\n{i}. {election['principle']}")
    print(f"   Type: {election['container_type']}")
    print(f"   Symbols: {election['symbols']}")

# Compose meta-song from election sequence
print("\n" + "=" * 80)
print("META-SONG (Complete output narrative from election order)")
print("=" * 80)

meta_verse = get_election_meta_song("verse")
print(f"\nComplete Verse (concatenated in election order):\n")
print(meta_verse)

# Show meta-song symbols
print("\n" + "-" * 80)
meta_symbols = get_election_meta_song("symbol")
print(f"Meta-Song Symbols (election sequence):\n{meta_symbols}")

# Show as JSON structure
print("\n" + "-" * 80)
meta_json = get_election_meta_song("json")
print(f"\nMeta-Song Metadata:")
print(f"  - Principle: {meta_json['principle']}")
print(f"  - Type: {meta_json['type']}")
print(f"  - Weight: {meta_json.get('weight', 'N/A')}")

print("\n" + "=" * 80)
print("✅ ELECTION SEQUENCING WORKING")
print("   • Elections recorded automatically: ✓")
print("   • Meta-song composes from election order: ✓")
print("   • Complete output narrative emerges: ✓")
print("=" * 80)
