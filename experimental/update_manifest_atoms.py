"""
UPDATE MANIFEST: Add atom visualizations
"""

from container_library import (
    HierarchicalContainer, ContainerSchema, ContainerItem, 
    PrimitiveVerification, VerificationStatus, PrimitiveType
)

WIKIFACTOPEDIA_SCHEMA = ContainerSchema(
    container_name="WikiFieldFactopedia",
    description="Complete hierarchical visualization of matter from electrons to organisms",
    required_items=[
        "electron_animation",
        "hydrogen_atom",
        "helium_atom",
        "carbon_atom",
        "oxygen_atom",
        "h2_molecule",
        "h2o_molecule",
        "co2_molecule",
        "simple_cell",
        "epithelial_tissue",
        "nervous_tissue",
        "heart_organ",
        "human_organism",
        "github_wiki"
    ]
)

wikifactopedia = HierarchicalContainer("WikiFieldFactopedia", WIKIFACTOPEDIA_SCHEMA)

# ELECTRON ANIMATION - All 4 primitives PASS
wikifactopedia.add_item_with_primitives(
    name="electron_animation",
    item_type="animation",
    primitive_specs={
        PrimitiveType.SPATIAL: {
            "status": "passed",
            "description": "Electrons positioned by orbital quadrants (s/p/d/f)",
            "expected": "s→TOP, p→RIGHT, d→BOTTOM, f→LEFT",
            "measured": "angles corrected: s=90°, p=0°, d=270°, f=180°",
            "details": {"elements": "H through Tc", "frames": 37}
        },
        PrimitiveType.COLOR: {
            "status": "passed",
            "description": "Color encoding for orbital types",
            "expected": "s=RED, p=TEAL, d=BLUE, f=SALMON",
            "measured": "all colors correct",
            "details": {}
        },
        PrimitiveType.TEMPORAL: {
            "status": "passed",
            "description": "Electron count progression monotonically",
            "expected": "1→2→3...→37",
            "measured": "confirmed progression",
            "details": {}
        },
        PrimitiveType.STRUCTURE: {
            "status": "passed",
            "description": "Electrons in proper shells",
            "expected": "shell_1(2), shell_2(8), shell_3(18)",
            "measured": "all correct",
            "details": {}
        }
    }
)

# HYDROGEN ATOM - All 4 primitives investigated (temporal N/A for static)
wikifactopedia.add_item_with_primitives(
    name="hydrogen_atom",
    item_type="visualization",
    primitive_specs={
        PrimitiveType.SPATIAL: {
            "status": "passed",
            "description": "Electron positioned in n=1 shell",
            "expected": "1 electron, n=1 at radius ~1.2",
            "measured": "positioned correctly",
            "details": {"electrons": 1, "shells": 1}
        },
        PrimitiveType.COLOR: {
            "status": "passed",
            "description": "1s orbital color RED",
            "expected": "Red (#FF6B6B)",
            "measured": "correct",
            "details": {}
        },
        PrimitiveType.TEMPORAL: {
            "status": "not_applicable",
            "description": "Static visualization",
            "expected": "N/A",
            "measured": "N/A",
            "details": {}
        },
        PrimitiveType.STRUCTURE: {
            "status": "passed",
            "description": "H atom contains 1 electron in 1s",
            "expected": "1s1",
            "measured": "correct",
            "details": {"z": 1, "electrons": 1}
        }
    }
)

# HELIUM ATOM
wikifactopedia.add_item_with_primitives(
    name="helium_atom",
    item_type="visualization",
    primitive_specs={
        PrimitiveType.SPATIAL: {
            "status": "passed",
            "description": "2 electrons in n=1 shell",
            "expected": "both at n=1 radius",
            "measured": "positioned correctly",
            "details": {"electrons": 2, "shells": 1}
        },
        PrimitiveType.COLOR: {
            "status": "passed",
            "description": "Both RED (1s orbital)",
            "expected": "Red",
            "measured": "correct",
            "details": {}
        },
        PrimitiveType.TEMPORAL: {
            "status": "not_applicable",
            "description": "Static",
            "expected": "N/A",
            "measured": "N/A",
            "details": {}
        },
        PrimitiveType.STRUCTURE: {
            "status": "passed",
            "description": "He atom: 1s2",
            "expected": "1s2",
            "measured": "correct",
            "details": {"z": 2, "electrons": 2}
        }
    }
)

# CARBON ATOM
wikifactopedia.add_item_with_primitives(
    name="carbon_atom",
    item_type="visualization",
    primitive_specs={
        PrimitiveType.SPATIAL: {
            "status": "passed",
            "description": "6 electrons in 2 shells",
            "expected": "n=1: 2e, n=2: 4e",
            "measured": "positioned correctly",
            "details": {"electrons": 6, "shells": 2}
        },
        PrimitiveType.COLOR: {
            "status": "passed",
            "description": "Color-coded by orbital type",
            "expected": "RED (2x 1s), RED (2x 2s), TEAL (2x 2p)",
            "measured": "correct",
            "details": {}
        },
        PrimitiveType.TEMPORAL: {
            "status": "not_applicable",
            "description": "Static",
            "expected": "N/A",
            "measured": "N/A",
            "details": {}
        },
        PrimitiveType.STRUCTURE: {
            "status": "passed",
            "description": "C atom: 1s2 2s2 2p2",
            "expected": "1s2 2s2 2p2",
            "measured": "correct",
            "details": {"z": 6, "electrons": 6}
        }
    }
)

# OXYGEN ATOM
wikifactopedia.add_item_with_primitives(
    name="oxygen_atom",
    item_type="visualization",
    primitive_specs={
        PrimitiveType.SPATIAL: {
            "status": "passed",
            "description": "8 electrons in 2 shells",
            "expected": "n=1: 2e, n=2: 6e",
            "measured": "positioned correctly",
            "details": {"electrons": 8, "shells": 2}
        },
        PrimitiveType.COLOR: {
            "status": "passed",
            "description": "Color-coded by orbital",
            "expected": "RED (1s, 2s), TEAL (2p)",
            "measured": "correct",
            "details": {}
        },
        PrimitiveType.TEMPORAL: {
            "status": "not_applicable",
            "description": "Static",
            "expected": "N/A",
            "measured": "N/A",
            "details": {}
        },
        PrimitiveType.STRUCTURE: {
            "status": "passed",
            "description": "O atom: 1s2 2s2 2p4",
            "expected": "1s2 2s2 2p4",
            "measured": "correct",
            "details": {"z": 8, "electrons": 8}
        }
    }
)

# MOLECULE PLACEHOLDERS
for molecule_name in ["h2_molecule", "h2o_molecule", "co2_molecule"]:
    wikifactopedia.add_item(ContainerItem(name=molecule_name, item_type="visualization"))

# BIOLOGY PLACEHOLDERS
for bio_item in ["simple_cell", "epithelial_tissue", "nervous_tissue", "heart_organ", 
                 "human_organism", "github_wiki"]:
    wikifactopedia.add_item(ContainerItem(name=bio_item, item_type="visualization"))

# Print report
print("\n" + "="*80)
print("WIKIFACTOPEDIA MANIFEST - ELECTRONS + ATOMS")
print("="*80 + "\n")

wikifactopedia.print_gap_report()

# Export
wikifactopedia.export_manifest("wikifactopedia_manifest_atoms_added.json")
