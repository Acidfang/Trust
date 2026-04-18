"""
Multi-molecule field visualization showing field interactions
Demonstrates how field manifestations organize at larger scales

GIF ANIMATION CONTAINER SPECIFICATION
======================================
When saving multi-molecule animations as GIFs, all outputs must conform to:
  See: c:\Determined\GIF_ANIMATION_SPECIFICATION.md
  
Container constraints by animation type:
  - Azimuth rotation: 36 frames, 1.2s duration
  - Threshold breathing: 36 frames, 1.8s duration
  - Element focus: 12 frames, 0.4s duration
  - Layer cycling: 12 frames, 0.6s duration
  - Evolution (time-based): 36 frames, 1.2s duration
  
File budget scales with resolution level (Molecular: 2.5 MB max)
"""

import numpy as np
import matplotlib.pyplot as plt
from field_gradient_visualization_system import FieldGradientRenderer


def render_three_water_molecules(filename="three_water_molecules_field.png"):
    """
    Render 3 H₂O molecules showing field interactions
    
    Positions arranged to show typical hydrogen bonding pattern
    Field overlaps show where molecular interactions occur
    """
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = renderer.create_field_grid(width=1200, height=1000)
    
    center_x, center_y = 600, 500
    
    # Three water molecules positioned with typical H-bonding geometry
    # Water molecules arranged in a line showing hydrogen bonding chain
    
    # Water molecule 1 (left) - bent geometry
    w1_o_x, w1_o_y = 250, 500
    w1_h1_angle = 52.25 * np.pi / 180
    w1_h2_angle = -52.25 * np.pi / 180
    w1_radius = 120
    
    w1_h1_x = int(w1_o_x + w1_radius * np.sin(w1_h1_angle))
    w1_h1_y = int(w1_o_y + w1_radius * np.cos(w1_h1_angle))
    w1_h2_x = int(w1_o_x + w1_radius * np.sin(w1_h2_angle))
    w1_h2_y = int(w1_o_y + w1_radius * np.cos(w1_h2_angle))
    
    # Water molecule 2 (center) - bent geometry, rotated differently
    w2_o_x, w2_o_y = 600, 450
    w2_h1_angle = 62.25 * np.pi / 180
    w2_h2_angle = -42.25 * np.pi / 180
    w2_radius = 120
    
    w2_h1_x = int(w2_o_x + w2_radius * np.sin(w2_h1_angle))
    w2_h1_y = int(w2_o_y + w2_radius * np.cos(w2_h1_angle))
    w2_h2_x = int(w2_o_x + w2_radius * np.sin(w2_h2_angle))
    w2_h2_y = int(w2_o_y + w2_radius * np.cos(w2_h2_angle))
    
    # Water molecule 3 (right) - bent geometry
    w3_o_x, w3_o_y = 950, 500
    w3_h1_angle = 52.25 * np.pi / 180
    w3_h2_angle = -52.25 * np.pi / 180
    w3_radius = 120
    
    w3_h1_x = int(w3_o_x + w3_radius * np.sin(w3_h1_angle))
    w3_h1_y = int(w3_o_y + w3_radius * np.cos(w3_h1_angle))
    w3_h2_x = int(w3_o_x + w3_radius * np.sin(w3_h2_angle))
    w3_h2_y = int(w3_o_y + w3_radius * np.cos(w3_h2_angle))
    
    # Add all field regions
    molecules_atoms = [
        # Water 1
        ("O", w1_o_x, w1_o_y, 8),
        ("H", w1_h1_x, w1_h1_y, 1),
        ("H", w1_h2_x, w1_h2_y, 1),
        # Water 2
        ("O", w2_o_x, w2_o_y, 8),
        ("H", w2_h1_x, w2_h1_y, 1),
        ("H", w2_h2_x, w2_h2_y, 1),
        # Water 3
        ("O", w3_o_x, w3_o_y, 8),
        ("H", w3_h1_x, w3_h1_y, 1),
        ("H", w3_h2_x, w3_h2_y, 1),
    ]
    
    for element, atom_x, atom_y, z in molecules_atoms:
        # Enhanced clarity: tighter fields, stronger cores
        if element == "H":
            # Hydrogen: clear bonding arms
            concentration = min(1.0, (z / 16.0) * 3.0)
            sigma = 42  # Tighter for clarity
        else:  # Oxygen
            # Oxygen: strong distinct core
            concentration = 1.0  # Full strength oxygen
            sigma = 35  # Tighter core
        
        grid = renderer.add_field_region(grid, atom_x, atom_y, concentration,
                                       sigma=sigma, element_type=element)
    
    # Render with ISOSURFACE mode (sharp, professional standard)
    fig, ax = renderer.render_field_2d(grid, 
                                     title="Three Water Molecules\nField Manifestation & Interaction",
                                     use_isosurface=True, isovalue=0.6)
    fig.savefig(filename, bbox_inches='tight', facecolor='#000000')
    plt.close(fig)
    print(f"✓ Saved: {filename}")


def render_multi_molecule_analysis(filename="multi_molecule_analysis.png"):
    """
    Show 5 molecules in 3D array pattern - higher resolution view
    Demonstrates how field organization creates larger structures
    """
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = renderer.create_field_grid(width=1400, height=1200)
    
    # 5 water molecules in + pattern (center + 4 neighbors)
    positions = [
        (700, 600),   # Center
        (700, 400),   # Top
        (500, 600),   # Left
        (900, 600),   # Right
        (700, 800),   # Bottom
    ]
    
    for mol_center_x, mol_center_y in positions:
        # Each water: O at center, 2 H atoms
        # Vary orientation for each molecule
        angle_offset = np.random.uniform(0, 60) * np.pi / 180
        
        # O field - strong distinct core
        grid = renderer.add_field_region(grid, mol_center_x, mol_center_y,
                                       concentration=1.0, sigma=45, element_type="O")
        
        # H1 field - clear visibility
        h1_angle = (52.25 + angle_offset) * np.pi / 180
        h1_x = int(mol_center_x + 120 * np.sin(h1_angle))
        h1_y = int(mol_center_y + 120 * np.cos(h1_angle))
        grid = renderer.add_field_region(grid, h1_x, h1_y,
                                       concentration=0.7, sigma=45, element_type="H")
        
        # H2 field - clear visibility
        h2_angle = (-52.25 + angle_offset) * np.pi / 180
        h2_x = int(mol_center_x + 120 * np.sin(h2_angle))
        h2_y = int(mol_center_y + 120 * np.cos(h2_angle))
        grid = renderer.add_field_region(grid, h2_x, h2_y,
                                       concentration=0.7, sigma=45, element_type="H")
    
    # Render with ISOSURFACE mode (sharp, professional standard)
    fig, ax = renderer.render_field_2d(grid, 
                                     title="Five Water Molecules\nField Patterns at Molecular Scale",
                                     use_isosurface=True, isovalue=0.6)
    fig.savefig(filename, bbox_inches='tight', facecolor='#000000')
    plt.close(fig)
    print(f"✓ Saved: {filename}")


def render_water_crystal_pattern(filename="water_crystal_pattern.png"):
    """
    Show 9+ water molecules in organized grid
    Demonstrates emergence of organized field patterns at larger scale
    """
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = renderer.create_field_grid(width=1600, height=1400)
    
    # 3x3 grid of water molecules
    spacing = 250
    start_x, start_y = 300, 250
    
    for row in range(3):
        for col in range(3):
            mol_x = start_x + col * spacing
            mol_y = start_y + row * spacing
            
            # Each molecule slightly rotated for realistic pattern
            angle_offset = (row * 30 + col * 20) * np.pi / 180
            
            # O field - strong distinct core
            grid = renderer.add_field_region(grid, mol_x, mol_y,
                                           concentration=1.0, sigma=38, element_type="O")
            
            # H1 field - clear structure
            h1_angle = (52.25 + angle_offset) * np.pi / 180
            h1_x = int(mol_x + 100 * np.sin(h1_angle))
            h1_y = int(mol_y + 100 * np.cos(h1_angle))
            grid = renderer.add_field_region(grid, h1_x, h1_y,
                                           concentration=0.65, sigma=40, element_type="H")
            
            # H2 field - clear structure
            h2_angle = (-52.25 + angle_offset) * np.pi / 180
            h2_x = int(mol_x + 100 * np.sin(h2_angle))
            h2_y = int(mol_y + 100 * np.cos(h2_angle))
            grid = renderer.add_field_region(grid, h2_x, h2_y,
                                           concentration=0.65, sigma=40, element_type="H")
    
    # Render with ISOSURFACE mode (sharp, professional standard)
    fig, ax = renderer.render_field_2d(grid, 
                                     title="Water Crystal Pattern\n9 Molecules - Emergent Field Organization",
                                     use_isosurface=True, isovalue=0.6)
    fig.savefig(filename, bbox_inches='tight', facecolor='#000000')
    plt.close(fig)
    print(f"✓ Saved: {filename}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("MULTI-MOLECULE FIELD VISUALIZATIONS")
    print("="*80)
    print("\nShowing how molecular fields interact and organize:\n")
    
    print("1. Three water molecules (hydrogen bonding chain)...")
    render_three_water_molecules(filename="three_water_molecules_field.png")
    
    print("\n2. Five water molecules (+ pattern)...")
    render_multi_molecule_analysis(filename="five_water_molecules_field.png")
    
    print("\n3. Nine water molecules (3x3 crystal pattern)...")
    render_water_crystal_pattern(filename="water_crystal_pattern.png")
    
    print("\n" + "="*80)
    print("Multi-molecule visualizations complete")
    print("Shows field interactions at progressively larger scales")
    print("="*80 + "\n")
