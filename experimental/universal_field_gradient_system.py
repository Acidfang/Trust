"""
Universal Field Gradient Visualization System
==============================================

All visualizations show ONE UNIVERSAL FIELD at different organizational resolutions.

Field rendering: Colors represent element type, gradient intensity represents concentration.
Same principle at all levels: s/p/d/f regions → atoms → molecules → cells → tissues → organs → organisms

Framework establishes that it's not DIFFERENT THINGS at DIFFERENT SCALES,
but ONE FIELD with DIFFERENT ORGANIZATIONAL PATTERNS at each scale.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter


class UniversalFieldGradient:
    """
    Universal field visualization at any resolution.
    Shows field concentration/density using color gradients.
    """
    
    # Element fields with colors
    ELEMENT_COLORS = {
        'H': '#00FFFF',  # Aqua - Hydrogen everywhere
        'C': '#808080',  # Gray - Carbon backbone
        'N': '#000080',  # Navy - Nitrogen networks
        'O': '#FF0000',  # Red - Oxygen active
        'P': '#FFD700',  # Gold - Phosphorus key points
        'S': '#FFFF00',  # Yellow - Sulfur bonds
    }
    
    def __init__(self, resolution_name="electron", width=800, height=800):
        """Initialize field gradient renderer"""
        self.resolution_name = resolution_name
        self.width = width
        self.height = height
        self.field_data = np.zeros((height, width))
    
    def add_field_region(self, center_x, center_y, radius, intensity=1.0, element='H'):
        """
        Add a field concentration region (Gaussian blob).
        
        Args:
            center_x, center_y: Center position (0-1 scale)
            radius: Gaussian sigma (controls spread)
            intensity: Peak intensity (0-1 scale)
            element: Element type (determines color)
        """
        # Convert to pixel coordinates
        px = int(center_x * self.width)
        py = int(center_y * self.height)
        
        # Create Gaussian field
        y, x = np.ogrid[:self.height, :self.width]
        gaussian = np.exp(-((x - px)**2 + (y - py)**2) / (2 * radius**2))
        self.field_data += gaussian * intensity
        
        return element, (px, py, radius)
    
    def render_field_gradient(self, element='H', filename=None):
        """
        Render field as gradient visualization.
        
        Shows field concentration density using color gradient.
        """
        fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
        field_normalized = self.field_data / (np.max(self.field_data) + 1e-10)
        
        # Create custom colormap: dark background → bright element color
        element_color = self.ELEMENT_COLORS.get(element, '#FFFFFF')
        colors = ['#000000', element_color]
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('field', colors, N=n_bins)
        
        # Display field as heatmap
        im = ax.imshow(field_normalized, cmap=cmap, origin='lower', extent=[0, 1, 0, 1])
        
        # Add contour lines showing field structure
        levels = np.linspace(0.1, 1.0, 5)
        contours = ax.contour(field_normalized, levels=levels, colors='white', alpha=0.3, linewidths=0.5)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        title = f"{self.resolution_name.upper()} FIELD GRADIENT\n{element} Element Field Concentration"
        fig.suptitle(title, fontsize=12, weight='bold', color='white')
        fig.patch.set_facecolor('#000000')
        
        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='#000000')
            print(f"✓ Saved {filename}")
        
        plt.close()
    
    def render_composite_field(self, field_regions, filename=None):
        """
        Render composite field with multiple elements.
        
        Args:
            field_regions: List of (element, x, y, radius, intensity) tuples
            filename: Output file
        """
        fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
        fig.patch.set_facecolor('#000000')
        ax.set_facecolor('#000000')
        
        # Create RGB field
        field_rgb = np.zeros((self.height, self.width, 3))
        
        for element, x, y, radius, intensity in field_regions:
            # Create Gaussian for this element
            gx, gy = np.ogrid[:self.height, :self.width]
            gaussian = np.exp(-((gx - y)**2 + (gy - x)**2) / (2 * radius**2))
            gaussian = gaussian * intensity
            
            # Get element color (hex to RGB)
            color_hex = self.ELEMENT_COLORS.get(element, '#FFFFFF')
            color_rgb = tuple(int(color_hex[i:i+2], 16)/255 for i in (1, 3, 5))
            
            # Add to field
            for c in range(3):
                field_rgb[:, :, c] += gaussian * color_rgb[c]
        
        # Normalize
        field_rgb = field_rgb / (np.max(field_rgb) + 1e-10)
        
        # Display
        ax.imshow(field_rgb, origin='lower', extent=[0, 1, 0, 1])
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        title = f"{self.resolution_name.upper()} COMPOSITE FIELD\nMultiple Element Fields Overlapping"
        fig.suptitle(title, fontsize=12, weight='bold', color='white')
        
        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='#000000')
            print(f"✓ Saved {filename}")
        
        plt.close()


def generate_electron_field_gradient():
    """
    Generate field gradient for electron orbital (Resolution 1).
    Show s/p/d/f orbitals as field concentration regions.
    """
    field = UniversalFieldGradient("electron", 800, 800)
    
    # Quadrant positions: s=top(90°), p=right(0°), d=bottom(270°), f=left(180°)
    print("\nElectron Field Gradient Generation:")
    print("-" * 60)
    
    # s-orbital field at TOP center
    field.add_field_region(0.5, 0.85, radius=60, intensity=1.0, element='H')
    
    # p-orbital field at RIGHT center
    field.add_field_region(0.85, 0.5, radius=60, intensity=0.8, element='H')
    
    # d-orbital field at BOTTOM center
    field.add_field_region(0.5, 0.15, radius=60, intensity=0.6, element='H')
    
    # f-orbital field at LEFT center
    field.add_field_region(0.15, 0.5, radius=60, intensity=0.4, element='H')
    
    field.render_composite_field(
        [('H', 400, 680, 60, 1.0),    # s at top
         ('H', 680, 400, 60, 0.8),    # p at right
         ('H', 400, 120, 60, 0.6),    # d at bottom
         ('H', 120, 400, 60, 0.4)],   # f at left
        filename="electron_field_gradient.png"
    )
    print("✓ Electron field gradient created (s/p/d/f regions)")


def generate_atom_field_gradient(element, z, config):
    """
    Generate field gradient for atom (Resolution 2).
    Show electron shell organization as field concentration.
    """
    field = UniversalFieldGradient(f"atom_{element}", 800, 800)
    
    print(f"\nAtom Field Gradient: {element} (Z={z})")
    print("-" * 60)
    
    # Create shell fields
    field_regions = []
    
    # Inner shell (1s, 2s, 2p) - tighter concentration
    if z >= 1:
        field_regions.append(('H', 400, 400, 80, 1.0))
    
    # Middle shells - looser concentration
    if z > 2:
        field_regions.append(('H', 400, 400, 150, 0.7))
    
    # Outer shells
    if z > 10:
        field_regions.append(('H', 400, 400, 220, 0.4))
    
    field.render_composite_field(
        field_regions,
        filename=f"atom_field_{element}_gradient.png"
    )
    print(f"✓ Atom field gradient created ({z} electron shells)")


def generate_molecule_field_gradient(name, elements_list, bond_positions):
    """
    Generate field gradient for molecule (Resolution 3).
    Show overlapping element fields in characteristic geometry.
    """
    field = UniversalFieldGradient(f"molecule_{name}", 1000, 1000)
    
    print(f"\nMolecule Field Gradient: {name}")
    print("-" * 60)
    
    # Create field regions for each atom in molecule
    field_regions = []
    for element, x, y in bond_positions:
        # Scale coordinates to pixel space
        px = int(x * 1000)
        py = int(y * 1000)
        field_regions.append((element, px, py, 100, 1.0))
    
    field.render_composite_field(
        field_regions,
        filename=f"molecule_field_{name}_gradient.png"
    )
    print(f"✓ Molecule field gradient created ({name})")


def generate_cell_field_gradient():
    """
    Generate field gradient for cell (Resolution 4).
    Show organelles as localized field concentration regions.
    """
    field = UniversalFieldGradient("cell", 1000, 1000)
    
    print(f"\nCell Field Gradient: Simple Eukaryotic Cell")
    print("-" * 60)
    
    # Nucleus field (CHNOP)
    nucleus_fields = [
        ('C', 500, 500, 150, 1.0),
        ('N', 500, 500, 140, 0.8),
        ('O', 500, 500, 130, 0.6),
        ('P', 500, 500, 120, 0.4),
    ]
    
    # Mitochondria fields (CHNOS) - distributed
    mitochondria_fields = [
        ('C', 700, 700, 80, 0.8),
        ('N', 700, 700, 75, 0.6),
        ('O', 700, 700, 70, 0.5),
        ('S', 700, 700, 65, 0.3),
        
        ('C', 300, 700, 80, 0.8),
        ('N', 300, 700, 75, 0.6),
        ('O', 300, 700, 70, 0.5),
        
        ('C', 700, 300, 80, 0.8),
        ('N', 700, 300, 75, 0.6),
        ('O', 700, 300, 70, 0.5),
        
        ('C', 300, 300, 80, 0.8),
        ('N', 300, 300, 75, 0.6),
        ('O', 300, 300, 70, 0.5),
    ]
    
    # Membrane field (CHNOS) - boundary
    membrane_fields = [
        ('C', 500, 950, 50, 0.5),
        ('N', 500, 950, 45, 0.4),
        ('O', 500, 950, 40, 0.3),
    ]
    
    all_fields = nucleus_fields + mitochondria_fields + membrane_fields
    
    field.render_composite_field(
        all_fields,
        filename="cell_field_gradient.png"
    )
    print(f"✓ Cell field gradient created (nucleus + mitochondria + membrane)")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("UNIVERSAL FIELD GRADIENT VISUALIZATION SYSTEM")
    print("="*80)
    print("\nGenerating field gradient visualizations for all resolution levels...")
    print("Each shows element field concentration (ONE UNIVERSAL FIELD at different scales)")
    
    # Generate electron field
    generate_electron_field_gradient()
    
    # Generate sample atom fields
    generate_atom_field_gradient("H", 1, "1s¹")
    generate_atom_field_gradient("C", 6, "1s² 2s² 2p²")
    generate_atom_field_gradient("O", 8, "1s² 2s² 2p⁴")
    
    # Generate sample molecule fields
    generate_molecule_field_gradient("H2", ['H', 'H'], 
                                   [('H', 0.3, 0.5), ('H', 0.7, 0.5)])
    
    generate_molecule_field_gradient("H2O", ['H', 'O', 'H'],
                                   [('H', 0.3, 0.3), ('O', 0.5, 0.5), ('H', 0.7, 0.3)])
    
    generate_molecule_field_gradient("CO2", ['O', 'C', 'O'],
                                   [('O', 0.2, 0.5), ('C', 0.5, 0.5), ('O', 0.8, 0.5)])
    
    # Generate cell field
    generate_cell_field_gradient()
    
    print("\n" + "="*80)
    print("FIELD GRADIENT SYSTEM COMPLETE")
    print("="*80)
    print("\nKey insight: Same UNIVERSAL FIELD at all resolutions")
    print("  • Visualizations show FIELD CONCENTRATION, not particles/shapes")
    print("  • Colors represent ELEMENT TYPES (C/H/N/O/P/S)")
    print("  • Gradients represent FIELD INTENSITY (high intensity = strong manifestation)")
    print("  • Same rendering principle from electrons to organisms")
    print("="*80 + "\n")
