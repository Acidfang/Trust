#!/usr/bin/env python
"""
Demo: All 7 Animation Patterns in Unified Container

Shows rotating GIFs with different parameter variations
"""

import numpy as np
from field_gradient_visualization_system import FieldGradientRenderer


def create_water_molecule_grid():
    """Create a simple water molecule grid (O + 2H)"""
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = renderer.create_field_grid(width=1200, height=1000)
    
    # Oxygen at center
    grid = renderer.add_field_region(grid, center_x=600, center_y=500, 
                                    concentration=0.8, sigma=40, element_type="O")
    
    # Hydrogen atoms (bent geometry)
    # H1: left-up
    grid = renderer.add_field_region(grid, center_x=480, center_y=580,
                                    concentration=0.6, sigma=30, element_type="H")
    
    # H2: right-up
    grid = renderer.add_field_region(grid, center_x=720, center_y=580,
                                    concentration=0.6, sigma=30, element_type="H")
    
    return grid


def demo_azimuth_rotation():
    """Pattern 1: 3D surface rotating"""
    
    print("\n" + "="*70)
    print("PATTERN 1: AZIMUTH ROTATION (3D spinning)")
    print("="*70)
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = create_water_molecule_grid()
    
    # Render 3D surface rotating
    renderer.render_field_2d(
        grid, title="Water Molecule 3D Rotation",
        technique="3d_surface",
        output="gif",
        animation_type="azimuth",
        num_frames=36, fps=30
    )
    print("\nResult: water_molecule_3d_rotation.gif")
    print("Visual: Spinning 3D elevation map showing full 360° view")


def demo_threshold_animation():
    """Pattern 2: Threshold pulsing (breathing core)"""
    
    print("\n" + "="*70)
    print("PATTERN 2: THRESHOLD ANIMATION (Breathing core)")
    print("="*70)
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = create_water_molecule_grid()
    
    # Render with pulsing threshold
    renderer.render_field_2d(
        grid, title="Water Molecule Breathing",
        technique="hybrid",
        output="gif",
        animation_type="threshold",
        animation_param_range=(0.2, 0.8),
        num_frames=36, fps=20
    )
    print("\nResult: water_molecule_breathing.gif")
    print("Visual: Molecular core expands/contracts showing field extent")


def demo_element_cycling():
    """Pattern 3: Element focus cycling"""
    
    print("\n" + "="*70)
    print("PATTERN 3: ELEMENT CYCLING (Highlight each element)")
    print("="*70)
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = create_water_molecule_grid()
    
    # Render with element cycling
    renderer.render_field_2d(
        grid, title="Water Molecule Elements",
        technique="isosurface",
        output="gif",
        animation_type="element",
        num_frames=12, fps=30
    )
    print("\nResult: water_molecule_elements.gif")
    print("Visual: O highlighted → H highlighted, repeat")
    print("Use case: Show spatial location of each element type")


def demo_layer_cycling():
    """Pattern 4: Multi-layer cycling (onion peeling)"""
    
    print("\n" + "="*70)
    print("PATTERN 4: LAYER CYCLING (Onion peeling)")
    print("="*70)
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = create_water_molecule_grid()
    
    # Render with layer cycling
    renderer.render_field_2d(
        grid, title="Water Molecule Layers",
        technique="multi_layer",
        output="gif",
        animation_type="layer",
        num_frames=12, fps=20
    )
    print("\nResult: water_molecule_layers.gif")
    print("Visual: Layer 1 (tight core) → Layer 2 → Layer 3 → Layer 4 (loose periphery)")
    print("Use case: Show internal structure and density shells")


def demo_comparison():
    """Show all 4 patterns in sequence"""
    
    print("\n" + "="*70)
    print("ANIMATION PATTERN DEMO - All Patterns")
    print("="*70)
    print("\nGenerating 4 different GIFs showing different animation patterns:")
    print("1. Azimuth Rotation - 3D spinning (36 frames)")
    print("2. Threshold Animation - Breathing core (36 frames)")
    print("3. Element Cycling - Highlight each element (12 frames)")
    print("4. Layer Cycling - Onion peeling (12 frames)")
    print("\nEach pattern serves a different purpose:")
    print("  - Azimuth: See full 360° view of structure")
    print("  - Threshold: Understand spatial extent of field")
    print("  - Element: Identify location of each element")
    print("  - Layer: Explore internal density structure")
    
    print("\n" + "-"*70)
    
    demo_azimuth_rotation()
    demo_threshold_animation()
    demo_element_cycling()
    demo_layer_cycling()
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nGenerated GIFs:")
    print("  ✓ water_molecule_3d_rotation.gif      (azimuth animation)")
    print("  ✓ water_molecule_breathing.gif        (threshold animation)")
    print("  ✓ water_molecule_elements.gif         (element cycling)")
    print("  ✓ water_molecule_layers.gif           (layer cycling)")
    print("\nEach GIF demonstrates a different animation pattern,")
    print("all working in the same unified FieldGradientRenderer container.")


if __name__ == "__main__":
    demo_comparison()
