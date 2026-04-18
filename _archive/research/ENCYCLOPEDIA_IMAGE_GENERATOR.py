"""
Encyclopedia Image Generator - Universal Field Visualization
Generates contextually accurate images for encyclopedia entities

Principles:
- Physics-accurate visualizations using field theory
- Domain-appropriate for each entity scale (particle, molecule, cell, system)
- Integrates with field gradient visualization system
- Stores images for encyclopedia display
"""

import sys
sys.path.insert(0, r'c:\Determined')

from pathlib import Path
import numpy as np
from typing import Dict, Tuple, Optional
import os

class EncyclopediaImageGenerator:
    """Generate field-theory-based images for encyclopedia entries"""
    
    def __init__(self):
        self.output_dir = Path(r"c:\Determined\wiki_assets\entity_images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Import visualization system
        sys.path.insert(0, r'c:\Determined\experimental\scripts\visualization')
        from field_gradient_visualization_system import FieldGradientRenderer
        self.renderer = FieldGradientRenderer(resolution_level="atom")
    
    def generate_for_electron(self) -> str:
        """Generate physics-accurate electron field visualization
        
        Electron: fundamental particle as quantum field excitation
        Visualization shows: probability density, quantum field structure, spin state
        """
        
        # Create electron field: 1D slice through high-dimension quantum field
        width, height = 800, 800
        grid = np.zeros((height, width))
        
        # Electron probability density: Gaussian centered with tail
        center_x, center_y = width // 2, height // 2
        for y in range(height):
            for x in range(width):
                # Distance from center
                r = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                # Quantum probability density (Gaussian superposition)
                # Multiple shell structure representing orbital/spinor components
                density = (
                    0.7 * np.exp(-r**2 / (40**2)) +  # Core: tight s-orbital-like
                    0.2 * np.exp(-((r - 120)**2) / (60**2)) +  # First shell
                    0.1 * np.exp(-((r - 200)**2) / (100**2))   # Fuzzy exterior
                )
                
                grid[y, x] = density
        
        # Render with physics-appropriate technique
        fig, ax = self.renderer.render_field_2d(
            grid, 
            title="Electron - Quantum Field Excitation",
            technique="hybrid",  # Sharp core + fuzzy halo
            isovalue=0.3,
            halo_intensity=0.4,
            output="png"
        )
        
        # Save figure to wiki_assets
        output_path = self.output_dir / "electron_field.png"
        fig.savefig(str(output_path), bbox_inches='tight', dpi=100)
        import matplotlib.pyplot as plt
        plt.close(fig)
        
        return str(output_path)
    
    def generate_for_water_molecule(self) -> str:
        """Generate water molecule field visualization
        
        H₂O: three-body quantum system with covalent bonds and dipole moment
        Visualization shows: electron clouds (O red, H cyan), dipole field, bonding
        """
        
        width, height = 800, 800
        
        # Multi-element grid: oxygen and hydrogen electron distributions
        grids = {
            "O": np.zeros((height, width)),  # Red - oxygen core
            "H": np.zeros((height, width)),  # Cyan - hydrogen orbitals
        }
        
        center_x, center_y = width // 2, height // 2
        
        # Oxygen center (larger, heavier nucleus)
        oxygen_sigma = 45  # Oxygen orbital extent
        for y in range(height):
            for x in range(width):
                r = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                # Oxygen electron density: two s electrons, four p electrons
                grids["O"][y, x] = (
                    0.8 * np.exp(-r**2 / oxygen_sigma**2) +    # Core 2s electrons
                    0.5 * np.exp(-((r - 30)**2) / (40**2))      # 2p electrons
                )
        
        # Two hydrogen atoms positioned at 104.5° angle (H-O-H bond angle)
        h_distance = 80  # O-H bond distance in pixels
        h_angle1 = np.pi / 2 - (104.5 / 2) * np.pi / 180
        h_angle2 = np.pi / 2 + (104.5 / 2) * np.pi / 180
        
        # Hydrogen 1
        h1_x = int(center_x + h_distance * np.cos(h_angle1))
        h1_y = int(center_y + h_distance * np.sin(h_angle1))
        
        # Hydrogen 2
        h2_x = int(center_x + h_distance * np.cos(h_angle2))
        h2_y = int(center_y + h_distance * np.sin(h_angle2))
        
        hydrogen_sigma = 25
        for y in range(height):
            for x in range(width):
                r1 = np.sqrt((x - h1_x)**2 + (y - h1_y)**2)
                r2 = np.sqrt((x - h2_x)**2 + (y - h2_y)**2)
                
                # Each hydrogen: 1s electron
                grids["H"][y, x] += (
                    0.6 * np.exp(-r1**2 / hydrogen_sigma**2) +
                    0.6 * np.exp(-r2**2 / hydrogen_sigma**2)
                )
        
        # Render multi-element grid with element-specific colors
        fig, ax = self.renderer.render_field_2d(
            grids,
            title="Water Molecule - Electron Density & Dipole Field",
            technique="multi_layer",  # Show electron shells
            layer_count=3,
            output="png"
        )
        
        # Save figure to wiki_assets
        output_path = self.output_dir / "water_molecule_field.png"
        fig.savefig(str(output_path), bbox_inches='tight', dpi=100)
        import matplotlib.pyplot as plt
        plt.close(fig)
        
        return str(output_path)
    
    def generate_for_human(self) -> str:
        """Generate human organism field visualization
        
        Human: macroscopic biological system - field represents integrated systems
        Visualization shows: major organ regions, neural connectivity, field coherence
        """
        
        width, height = 800, 1000  # Taller for vertical organism
        grid = np.zeros((height, width))
        
        center_x = width // 2
        
        # Major organ regions - showing integrated biological fields
        
        # Brain (top) - highest signal complexity
        brain_y = int(height * 0.15)
        brain_region = np.exp(-((np.arange(height) - brain_y)**2 / (50**2))).reshape(-1, 1)
        brain_region = brain_region * np.exp(-(np.arange(width) - center_x)**2 / (30**2)).reshape(1, -1)
        grid += 0.9 * brain_region
        
        # Heart (upper center) - rhythmic oscillation field
        heart_y = int(height * 0.35)
        heart_region = np.exp(-((np.arange(height) - heart_y)**2 / (40**2))).reshape(-1, 1)
        heart_region = heart_region * np.exp(-(np.arange(width) - center_x)**2 / (25**2)).reshape(1, -1)
        grid += 0.8 * heart_region
        
        # Lungs (sides, upper) - bilateral symmetry field
        lung_y = int(height * 0.35)
        for center in [center_x - 80, center_x + 80]:
            lung_region = np.exp(-(np.arange(width) - center)**2 / (35**2)).reshape(1, -1)
            lung_region = lung_region * np.exp(-((np.arange(height) - lung_y)**2) / (60**2)).reshape(-1, 1)
            grid += 0.7 * lung_region
        
        # Digestive system (center, lower) - line of connected organs
        for organ_y in [int(height * 0.45), int(height * 0.55), int(height * 0.65)]:
            organ_region = np.exp(-((np.arange(height) - organ_y)**2 / (25**2))).reshape(-1, 1)
            organ_region = organ_region * np.exp(-(np.arange(width) - center_x)**2 / (40**2)).reshape(1, -1)
            grid += 0.6 * organ_region
        
        # Nervous system (lateral pathways) - vertical connectivity
        for x_offset in [-50, 50]:
            for y in range(0, height, 50):
                nerve_y = np.exp(-((np.arange(height) - y)**2 / (20**2)))
                nerve_x = np.exp(-(np.arange(width) - (center_x + x_offset))**2 / (15**2))
                grid[y, :] += 0.3 * nerve_x
        
        # Render organism field
        fig, ax = self.renderer.render_field_2d(
            grid,
            title="Human - Integrated Biological Systems Field",
            technique="hybrid",
            isovalue=0.4,
            halo_intensity=0.3,
            output="png"
        )
        
        # Save figure to wiki_assets
        output_path = self.output_dir / "human_field.png"
        fig.savefig(str(output_path), bbox_inches='tight', dpi=100)
        import matplotlib.pyplot as plt
        plt.close(fig)
        
        return str(output_path)
    
    def generate_for_entity(self, entity_name: str) -> Optional[str]:
        """Generate image for any entity based on type
        
        Automatically selects appropriate visualization based on entity scale
        """
        
        entity_lower = entity_name.lower()
        
        # Map entity names to generation functions
        generators = {
            "electron": self.generate_for_electron,
            "photon": self.generate_for_electron,  # Similar physics
            "quark": self.generate_for_electron,
            "particle": self.generate_for_electron,
            
            "water molecule": self.generate_for_water_molecule,
            "water": self.generate_for_water_molecule,
            "molecule": self.generate_for_water_molecule,
            
            "human": self.generate_for_human,
            "organism": self.generate_for_human,
        }
        
        # Find matching generator
        for key, generator in generators.items():
            if key in entity_lower or entity_lower in key:
                try:
                    image_path = generator()
                    print(f"✓ Generated image for {entity_name}: {image_path}")
                    return image_path
                except Exception as e:
                    print(f"✗ Error generating image for {entity_name}: {e}")
                    return None
        
        print(f"⚠ No image generator for {entity_name}")
        return None
    
    def get_image_url(self, entity_name: str) -> Optional[str]:
        """Get URL or relative path for image in encyclopedia
        
        Returns path relative to encyclopedia HTML file for <img src="">
        """
        image_path = self.generate_for_entity(entity_name)
        
        if image_path:
            # Convert absolute path to relative (from HTML location)
            # wiki_assets/entity_images/electron_field.png
            return f"../../../wiki_assets/entity_images/{Path(image_path).name}"
        
        return None


# ============================================================================
# TEST: Generate images for encyclopedia
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("ENCYCLOPEDIA IMAGE GENERATION")
    print("="*80 + "\n")
    
    generator = EncyclopediaImageGenerator()
    
    entities = ["Electron", "Water Molecule", "Human"]
    
    for entity in entities:
        print(f"\nGenerating image for: {entity}")
        image_url = generator.get_image_url(entity)
        if image_url:
            print(f"  URL for HTML: {image_url}")
        else:
            print(f"  ✗ Failed to generate image")
    
    print(f"\n✓ Images saved to: {generator.output_dir}")
