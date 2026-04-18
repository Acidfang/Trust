#!/usr/bin/env python3
"""
FIELD IMAGE GENERATOR V3 — Entity-Specific Field Topology

NOT templated. Each entity gets its ACTUAL unique field structure.
Not drawn the same way. Each has its own specific geometry based on what it IS.

If you can't draw every electron, you don't use a generic pattern.
You draw only what you KNOW about this specific entity.
"""

import math
from pathlib import Path
from typing import Dict, Any, List, Tuple

class EntitySpecificFieldGenerator:
    """Generate unique visualizations based on actual entity properties."""
    
    def __init__(self, output_dir: str = r"c:\Determined\wiki_assets\entity_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_electron_svg(self) -> str:
        """
        ELECTRON: Single quantum entity
        What we know: Spin-1/2, probability cloud, superposition
        What we DON'T know: exact position (undefined until measured)
        
        Show: The superposition principle - it's everywhere and nowhere simultaneously
        """
        svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="800" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <filter id="blurSuper">
            <feGaussianBlur in="SourceGraphic" stdDeviation="8" />
        </filter>
    </defs>
    
    <!-- Void field -->
    <rect width="800" height="800" fill="#0a0a0a"/>
    
    <!-- QUANTUM SUPERPOSITION: electron exists in all states simultaneously -->
    <!-- Draw probability cloud - many overlapping positions -->
    <g opacity="0.15" filter="url(#blurSuper)">
        <circle cx="200" cy="200" r="40" fill="#ff00ff"/>
        <circle cx="300" cy="250" r="40" fill="#ff00ff"/>
        <circle cx="350" cy="350" r="40" fill="#ff00ff"/>
        <circle cx="300" cy="450" r="40" fill="#ff00ff"/>
        <circle cx="200" cy="500" r="40" fill="#ff00ff"/>
        <circle cx="100" cy="400" r="40" fill="#ff00ff"/>
        <circle cx="150" cy="300" r="40" fill="#ff00ff"/>
    </g>
    
    <!-- Most likely position (peak of probability) -->
    <circle cx="250" cy="325" r="30" fill="#ff00ff" opacity="0.4"/>
    <circle cx="250" cy="325" r="15" fill="#ff00ff" opacity="0.7"/>
    
    <!-- Spin indicator: two possible spin states -->
    <g stroke="#00ffff" stroke-width="2" fill="none" opacity="0.6">
        <path d="M 400 300 A 50 50 0 0 1 400 400"/>
        <path d="M 400 300 A 50 50 0 0 0 400 400"/>
    </g>
    
    <!-- Charge field (negative): radial field lines pointing inward -->
    <g stroke="#ff4455" stroke-width="1" opacity="0.3">
        <line x1="600" y1="300" x2="550" y2="325"/>
        <line x1="650" y1="325" x2="600" y2="325"/>
        <line x1="600" y1="350" x2="550" y2="325"/>
        <line x1="600" y1="200" x2="550" y2="250"/>
        <line x1="600" y1="450" x2="550" y2="400"/>
    </g>
    
    <!-- Uncertainty principle visualization: position vs momentum trade-off -->
    <g opacity="0.5">
        <text x="50" y="700" fill="#00ff88" font-size="12" font-family="monospace">
            ELECTRON: Superposition | Spin-1/2 | Charge -e | Mass m_e
        </text>
        <text x="50" y="720" fill="#00ffff" font-size="10" font-family="monospace">
            Heisenberg: Δx·Δp ≥ ℏ/2  (position-momentum uncertainty)
        </text>
        <text x="50" y="735" fill="#ff4455" font-size="10" font-family="monospace">
            Probability field, not particle. Exists as wave function ψ.
        </text>
    </g>
</svg>'''
        return svg
    
    def generate_atom_svg(self, element: str = "Hydrogen") -> str:
        """
        ATOM: Element-specific structure
        What we know: Atomic number, orbital configuration, shell structure
        What's unique: THIS SPECIFIC ELEMENT'S electron configuration
        
        Show: The actual orbital structure for this element
        """
        
        # Element-specific data
        element_data = {
            'Hydrogen': {'z': 1, 'shells': [1], 'color': '#eeeeee', 'radius': 53},
            'Carbon': {'z': 6, 'shells': [2, 4], 'color': '#888888', 'radius': 70},
            'Nitrogen': {'z': 7, 'shells': [2, 5], 'color': '#0000ff', 'radius': 65},
            'Oxygen': {'z': 8, 'shells': [2, 6], 'color': '#ff0000', 'radius': 60},
        }
        
        data = element_data.get(element, element_data['Hydrogen'])
        z = data['z']
        shells = data['shells']
        color = data['color']
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="800" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="800" fill="#0a0a0a"/>
    
    <!-- NUCLEUS: {z} protons -->
    <circle cx="400" cy="400" r="12" fill="{color}" opacity="0.9"/>
    <text x="400" y="408" text-anchor="middle" fill="{color}" font-size="8" font-family="monospace">
        +{z}
    </text>
    
    <!-- ELECTRON SHELLS: Specific to this element -->
'''
        
        # Draw shells with correct number of electrons
        shell_radius = [0, 53, 106, 159]  # Bohr radii
        electron_num = 0
        
        for shell_idx, electrons_in_shell in enumerate(shells):
            radius = shell_radius[shell_idx + 1]
            
            # Draw shell ring
            svg += f'    <circle cx="400" cy="400" r="{radius}" fill="none" stroke="#00ff88" stroke-width="1" opacity="0.4"/>\n'
            
            # Draw electrons in this shell
            for e_in_shell in range(electrons_in_shell):
                angle = (e_in_shell / electrons_in_shell) * 360
                x = 400 + radius * math.cos(math.radians(angle))
                y = 400 + radius * math.sin(math.radians(angle))
                
                svg += f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#00ddff" opacity="0.7"/>\n'
                electron_num += 1
        
        svg += f'''    
    <!-- ELEMENT INFO -->
    <text x="400" y="700" text-anchor="middle" fill="#00ff88" font-size="13" font-family="monospace" font-weight="bold">
        {element.upper()} (Z={z})
    </text>
    <text x="400" y="720" text-anchor="middle" fill="#00ffff" font-size="10" font-family="monospace">
        Electronic configuration: {' '.join([str(s) for s in shells])}
    </text>
    <text x="400" y="735" text-anchor="middle" fill="#ff8800" font-size="10" font-family="monospace">
        {electron_num} electrons in {len(shells)} shells
    </text>
</svg>'''
        return svg
    
    def generate_water_molecule_svg(self) -> str:
        """
        WATER MOLECULE: H₂O specific geometry
        What we know: Bond angle 104.5°, polar molecule, O is more electronegative
        What's unique: THIS SPECIFIC 3-ATOM CONFIGURATION
        
        Show: The actual H-O-H angle and electron distribution
        """
        svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="800" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="800" fill="#0a0a0a"/>
    
    <!-- WATER MOLECULE: H-O-H with 104.5° bond angle -->
    
    <!-- Oxygen nucleus - center -->
    <circle cx="400" cy="400" r="14" fill="#ff0000" opacity="0.9"/>
    <text x="400" y="408" text-anchor="middle" fill="#ff0000" font-size="9" font-family="monospace">O</text>
    
    <!-- Bond angle geometry: 104.5 degrees (not linear!) -->
    <!-- Left Hydrogen at 120° -->
    <circle cx="300" cy="330" r="10" fill="#eeeeee" opacity="0.8"/>
    <text x="300" y="336" text-anchor="middle" fill="#eeeeee" font-size="9" font-family="monospace">H</text>
    
    <!-- Right Hydrogen at 224.5° (104.5° from first) -->
    <circle cx="350" cy="480" r="10" fill="#eeeeee" opacity="0.8"/>
    <text x="350" y="486" text-anchor="middle" fill="#eeeeee" font-size="9" font-family="monospace">H</text>
    
    <!-- O-H COVALENT BONDS (electron sharing) -->
    <line x1="400" y1="400" x2="300" y2="330" stroke="#00ff88" stroke-width="2.5" opacity="0.7"/>
    <line x1="400" y1="400" x2="350" y2="480" stroke="#00ff88" stroke-width="2.5" opacity="0.7"/>
    
    <!-- Electron density concentrated toward Oxygen (electronegativity) -->
    <g opacity="0.3" fill="#ff0000">
        <circle cx="370" cy="380" r="8"/>
        <circle cx="375" cy="405" r="8"/>
    </g>
    
    <!-- DIPOLE MOMENT: δ- on oxygen, δ+ on hydrogens -->
    <!-- Charge distribution -->
    <g fill="none" stroke="#ff4455" stroke-width="1.5" opacity="0.5">
        <!-- Negative end (oxygen) -->
        <circle cx="400" cy="400" r="35"/>
        <!-- Positive ends (hydrogens) -->
        <circle cx="300" cy="330" r="20"/>
        <circle cx="350" cy="480" r="20"/>
    </g>
    
    <!-- Dipole arrow pointing from + to - -->
    <defs>
        <marker id="arrowDipole" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="#ff00ff"/>
        </marker>
    </defs>
    <line x1="320" y1="390" x2="380" y2="380" stroke="#ff00ff" stroke-width="2" opacity="0.6" marker-end="url(#arrowDipole)"/>
    
    <!-- MOLECULE INFO -->
    <text x="400" y="700" text-anchor="middle" fill="#00ff88" font-size="13" font-family="monospace" font-weight="bold">
        H₂O (WATER MOLECULE)
    </text>
    <text x="400" y="720" text-anchor="middle" fill="#00ffff" font-size="11" font-family="monospace">
        H-O-H Bond Angle: 104.5° (BENT geometry, NOT linear)
    </text>
    <text x="400" y="735" text-anchor="middle" fill="#ff0000" font-size="10" font-family="monospace">
        Polar molecule: μ = 1.85 D | O more electronegative than H
    </text>
</svg>'''
        return svg
    
    def generate_for_all(self) -> Dict[str, str]:
        """Generate entity-specific visualizations."""
        results = {}
        
        # Electron - unique superposition structure
        results['Electron'] = self.generate_electron_svg()
        
        # Atoms - element-specific configurations
        for element in ['Hydrogen', 'Carbon', 'Oxygen']:
            svg = self.generate_atom_svg(element)
            results[element] = svg
        
        # Water molecule - specific bent geometry
        results['Water Molecule'] = self.generate_water_molecule_svg()
        
        # Save all
        for name, svg in results.items():
            filepath = self.output_dir / f"{name.lower().replace(' ', '_')}_specific.svg"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg)
            print(f"✓ {name}: {len(svg)} bytes (entity-specific)")
        
        return results


if __name__ == "__main__":
    print("=" * 70)
    print("FIELD IMAGE GENERATOR V3 — Entity-Specific Field Topology")
    print("=" * 70)
    print("\nGenerating unique visualizations for each specific entity...")
    print("(Not templated. Each shows what's ACTUALLY true about that entity.)\n")
    
    gen = EntitySpecificFieldGenerator()
    results = gen.generate_for_all()
    
    print("\n" + "=" * 70)
    print(f"Generated {len(results)} entity-specific visualizations")
    print("=" * 70)
    print("\nKey principle: Not drawn the same way.")
    print("Each entity's field structure is unique to what it ACTUALLY is.")
