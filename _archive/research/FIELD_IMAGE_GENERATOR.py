#!/usr/bin/env python3
"""
FIELD IMAGE GENERATOR — Auto-generate entity visualizations from field theory

Automatically generates SVG and PNG visualizations for any entity based on:
- Core attributes (energy, coherence, charge, spin, etc.)
- Field narratives (evolution, composition, environment, unique, purpose)
- Scale hierarchy (from electron to civilization)

All visualizations follow omnipresent field principles:
- Field is base state (background)
- Entity manifests through coherence concentration
- Attributes appear as field patterns and resonances
"""

import os
import json
import math
from pathlib import Path
from typing import Dict, Any, List, Tuple

# For PNG generation: pip install pillow cairosvg (optional, SVG is default)
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None
    ImageDraw = None


class FieldImageGenerator:
    """Generate visualizations of entities as field manifestations."""
    
    def __init__(self, output_dir: str = r"c:\Determined\wiki_assets\entity_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Color palette for field visualization
        self.colors = {
            'field_background': '#0a1e3f',      # Deep blue - omnipresent field
            'coherence': '#00ff88',              # Bright green - high coherence
            'entropy': '#ff4455',                # Red - entropy/diffusion
            'structure': '#4488ff',              # Blue - ordered patterns
            'energy': '#ffaa00',                 # Orange - energetic state
            'consciousness': '#ff00ff',          # Magenta - awareness/consciousness
            'wave': '#00ddff',                   # Cyan - wave patterns
        }
        
        # Element colors for atomic visualizations
        self.element_colors = {
            'H': '#eeeeee',   # Hydrogen - light gray
            'C': '#888888',   # Carbon - gray
            'N': '#0000ff',   # Nitrogen - blue
            'O': '#ff0000',   # Oxygen - red
            'P': '#ffaa00',   # Phosphorus - orange/gold
            'S': '#ffff00',   # Sulfur - yellow
        }
    
    def analyze_complexity(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze entity to determine complexity level.
        
        Returns complexity metrics that drive visualization generation.
        """
        attributes = entity_data.get('attributes', {})
        name = entity_data.get('name', 'Unknown')
        
        # Calculate complexity factors
        attribute_count = len(attributes)
        
        # Scale determination (from entity name/metrics)
        scale_map = {
            'Electron': 0,      # 10^-10 m - fundamental
            'Atom': 1,          # 10^-10 m - simple
            'Water Molecule': 2, # Multiple atoms bonded
            'Cell': 3,          # 10^-5 m - organelles
            'Human': 4,         # 1.7 m - organs, systems
            'Ecosystem': 5,     # Km+ - interconnected organisms
            'Civilization': 6,  # Global - information systems
        }
        
        complexity_level = scale_map.get(name, 3)
        
        # Coherence measure (if present)
        coherence_attr = str(attributes).lower()
        is_conscious = 'conscious' in coherence_attr or 'awareness' in coherence_attr or 'agency' in coherence_attr
        is_networked = 'network' in coherence_attr or 'interconnect' in coherence_attr
        is_organized = 'organelle' in coherence_attr or 'organ' in coherence_attr
        
        return {
            'name': name,
            'level': complexity_level,
            'attribute_count': attribute_count,
            'is_conscious': is_conscious,
            'is_networked': is_networked,
            'is_organized': is_organized,
            'total_complexity': (complexity_level * 2) + attribute_count + 
                               (5 if is_conscious else 0) + 
                               (3 if is_networked else 0) + 
                               (2 if is_organized else 0),
        }
    
    def generate_adaptive_visualization(self, entity_data: Dict[str, Any]) -> str:
        """
        Analyze entity and generate appropriate complex visualization.
        
        Automatically determines visualization complexity based on entity properties.
        """
        complexity = self.analyze_complexity(entity_data)
        name = complexity['name']
        
        # Route to appropriate generator based on analysis
        if name == 'Electron':
            return self.generate_electron_visualization()
        elif name == 'Atom':
            return self.generate_atom_visualization()
        elif name == 'Water Molecule':
            return self.generate_water_molecule_visualization()
        elif name == 'Cell':
            return self.generate_cell_visualization(entity_data)
        elif name == 'Human':
            return self.generate_human_visualization()
        elif name == 'Ecosystem':
            return self.generate_ecosystem_visualization(entity_data)
        elif name == 'Civilization':
            return self.generate_civilization_visualization(entity_data)
        else:
            # For unknown entities, generate based on complexity level
            return self.generate_complexity_based_visualization(entity_data, complexity)
    
    def generate_electron_visualization(self) -> str:
        """Generate electron field visualization as SVG."""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <!-- Background: Omnipresent field -->
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </radialGradient>
        <radialGradient id="electronField" cx="50%" cy="50%" r="55%">
            <stop offset="0%" style="stop-color:{self.colors['consciousness']};stop-opacity:0.8" />
            <stop offset="50%" style="stop-color:{self.colors['coherence']};stop-opacity:0.4" />
            <stop offset="100%" style="stop-color:{self.colors['field_background']};stop-opacity:0" />
        </radialGradient>
    </defs>
    
    <!-- Field background -->
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Electron orbital clouds (4 quadrants for s, p, d, f orbitals) -->
    <g opacity="0.6">
        <!-- S orbital (spherical) -->
        <circle cx="300" cy="300" r="80" fill="none" stroke="{self.colors['coherence']}" stroke-width="2" opacity="0.8"/>
        
        <!-- P orbitals (dumbbell shaped) -->
        <ellipse cx="300" cy="200" rx="70" ry="90" fill="none" stroke="{self.colors['wave']}" stroke-width="2" opacity="0.6"/>
        <ellipse cx="300" cy="400" rx="70" ry="90" fill="none" stroke="{self.colors['wave']}" stroke-width="2" opacity="0.6"/>
        
        <!-- D orbitals (cloverleaf) -->
        <ellipse cx="200" cy="300" rx="90" ry="70" fill="none" stroke="{self.colors['energy']}" stroke-width="2" opacity="0.6"/>
        <ellipse cx="400" cy="300" rx="90" ry="70" fill="none" stroke="{self.colors['energy']}" stroke-width="2" opacity="0.6"/>
    </g>
    
    <!-- Nucleus/center point -->
    <circle cx="300" cy="300" r="15" fill="{self.colors['consciousness']}" opacity="0.9"/>
    
    <!-- Orbiting electrons (probability clouds) -->
    <g stroke="{self.colors['energy']}" stroke-width="2" fill="none" opacity="0.7">
        <circle cx="300" cy="300" r="60"/>
        <circle cx="300" cy="300" r="120"/>
        <circle cx="300" cy="300" r="180"/>
    </g>
    
    <!-- Quantum superposition indicator (blurred effect simulation) -->
    <circle cx="300" cy="300" r="100" fill="url(#electronField)" opacity="0.4"/>
    
    <!-- Scale indicator -->
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="16" font-family="monospace">
        10⁻¹⁰ m (Angstrom) | Fundamental Particle
    </text>
</svg>'''
        return svg
    
    def generate_water_molecule_visualization(self) -> str:
        """Generate water molecule field visualization as SVG."""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <!-- Background: Omnipresent field -->
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000011;stop-opacity:1" />
        </radialGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Field background -->
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Water molecule structure: H-O-H -->
    <!-- Central oxygen atom (negative pole) -->
    <circle cx="300" cy="300" r="40" fill="{self.element_colors['O']}" opacity="0.8" filter="url(#glow)"/>
    <circle cx="300" cy="300" r="50" fill="none" stroke="{self.element_colors['O']}" stroke-width="2" opacity="0.4"/>
    
    <!-- Hydrogen atoms (positive poles) -->
    <circle cx="200" cy="240" r="25" fill="{self.element_colors['H']}" opacity="0.8" filter="url(#glow)"/>
    <circle cx="200" cy="240" r="35" fill="none" stroke="{self.element_colors['H']}" stroke-width="2" opacity="0.3"/>
    
    <circle cx="380" cy="240" r="25" fill="{self.element_colors['H']}" opacity="0.8" filter="url(#glow)"/>
    <circle cx="380" cy="240" r="35" fill="none" stroke="{self.element_colors['H']}" stroke-width="2" opacity="0.3"/>
    
    <!-- Covalent bonds (electron sharing) -->
    <line x1="270" y1="280" x2="210" y2="255" stroke="{self.colors['coherence']}" stroke-width="3" opacity="0.6"/>
    <line x1="270" y1="280" x2="210" y2="255" stroke="{self.colors['coherence']}" stroke-width="1" opacity="0.3" stroke-dasharray="5,5"/>
    
    <line x1="330" y1="280" x2="370" y2="255" stroke="{self.colors['coherence']}" stroke-width="3" opacity="0.6"/>
    <line x1="330" y1="280" x2="370" y2="255" stroke="{self.colors['coherence']}" stroke-width="1" opacity="0.3" stroke-dasharray="5,5"/>
    
    <!-- Electron density field (dipole moment) -->
    <ellipse cx="300" cy="320" rx="90" ry="60" fill="none" stroke="{self.colors['energy']}" stroke-width="2" opacity="0.4"/>
    
    <!-- Hydrophilic region indicator -->
    <circle cx="300" cy="300" r="80" fill="{self.colors['wave']}" opacity="0.15"/>
    
    <!-- Hydrogen bond indicators (dotted lines to potential partners) -->
    <g stroke="{self.colors['entropy']}" stroke-width="1" stroke-dasharray="3,3" opacity="0.3">
        <line x1="300" y1="360" x2="300" y2="450"/>
        <line x1="260" y1="330" x2="150" y2="350"/>
        <line x1="340" y1="330" x2="450" y2="350"/>
    </g>
    
    <!-- Scale and attributes -->
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="16" font-family="monospace">
        1.5 × 10⁻¹⁰ m | 3 atoms | Polar molecule
    </text>
    
    <!-- Field coherence indicator -->
    <text x="300" y="580" text-anchor="middle" fill="{self.colors['energy']}" font-size="12" font-family="monospace">
        τ ≈ 0.72 | Asymmetric charge distribution
    </text>
</svg>'''
        return svg
    
    def generate_human_visualization(self) -> str:
        """Generate human organism field visualization as SVG."""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <!-- Background: Omnipresent field -->
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </radialGradient>
        <filter id="coherenceGlow">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Field background -->
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Human silhouette as coherence concentration -->
    <g opacity="0.7">
        <!-- Head: consciousness center -->
        <circle cx="300" cy="120" r="35" fill="{self.colors['consciousness']}" filter="url(#coherenceGlow)" opacity="0.8"/>
        
        <!-- Spine: information flow axis -->
        <line x1="300" y1="155" x2="300" y2="420" stroke="{self.colors['energy']}" stroke-width="8" opacity="0.6"/>
        
        <!-- Heart: coherence heartbeat -->
        <circle cx="300" cy="280" r="20" fill="{self.colors['coherence']}" opacity="0.9" filter="url(#coherenceGlow)"/>
        <circle cx="300" cy="280" r="40" fill="none" stroke="{self.colors['coherence']}" stroke-width="2" opacity="0.5" stroke-dasharray="5,5"/>
        <circle cx="300" cy="280" r="60" fill="none" stroke="{self.colors['energy']}" stroke-width="1" opacity="0.3" stroke-dasharray="8,4"/>
        
        <!-- Brain: consciousness network -->
        <ellipse cx="285" cy="110" rx="12" ry="15" fill="{self.colors['consciousness']}" opacity="0.7"/>
        <ellipse cx="315" cy="110" rx="12" ry="15" fill="{self.colors['consciousness']}" opacity="0.7"/>
        
        <!-- Nervous system: decision network (election pathways) -->
        <g stroke="{self.colors['wave']}" stroke-width="1.5" opacity="0.5">
            <path d="M 300 155 L 250 200 L 200 280 L 180 380"/>
            <path d="M 300 155 L 350 200 L 400 280 L 420 380"/>
            <path d="M 300 280 L 280 350 L 260 420"/>
            <path d="M 300 280 L 320 350 L 340 420"/>
        </g>
        
        <!-- Limbs: expression nodes -->
        <g stroke="{self.colors['structure']}" stroke-width="8" stroke-linecap="round" opacity="0.6">
            <!-- Arms -->
            <line x1="280" y1="210" x2="180" y2="220"/>
            <line x1="320" y1="210" x2="420" y2="220"/>
            
            <!-- Legs -->
            <line x1="285" y1="420" x2="250" y2="520"/>
            <line x1="315" y1="420" x2="350" y2="520"/>
        </g>
    </g>
    
    <!-- Coherence field envelope (τ measure) -->
    <ellipse cx="300" cy="300" rx="140" ry="180" fill="none" stroke="{self.colors['coherence']}" stroke-width="2" opacity="0.4" stroke-dasharray="10,5"/>
    
    <!-- Emotion/consciousness aura -->
    <circle cx="300" cy="300" r="200" fill="none" stroke="{self.colors['consciousness']}" stroke-width="1" opacity="0.2" stroke-dasharray="3,3"/>
    
    <!-- Information flow pattern -->
    <g stroke="{self.colors['energy']}" stroke-width="0.5" opacity="0.3">
        <circle cx="300" cy="120" r="50"/>
        <circle cx="300" cy="280" r="70"/>
        <circle cx="300" cy="420" r="55"/>
    </g>
    
    <!-- Scale and attributes -->
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="14" font-family="monospace">
        ~1.7 m | 37 trillion cells | Conscious organism
    </text>
    
    <!-- Coherence measure -->
    <text x="300" y="580" text-anchor="middle" fill="{self.colors['consciousness']}" font-size="12" font-family="monospace">
        τ ≈ 0.85 | Unified field perception + Agency
    </text>
</svg>'''
        return svg
    
    def generate_atom_visualization(self, element: str = "Carbon") -> str:
        """Generate generic atom visualization for any element."""
        element_code = element[0] if element else "C"
        color = self.element_colors.get(element_code, self.colors['structure'])
        protons = {"H": 1, "C": 6, "N": 7, "O": 8, "P": 15, "S": 16}.get(element_code, 6)
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </radialGradient>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Nucleus -->
    <circle cx="300" cy="300" r="20" fill="{color}" opacity="0.9"/>
    
    <!-- Orbital shells -->
    <g stroke="{self.colors['coherence']}" stroke-width="2" fill="none" opacity="0.6">
        <circle cx="300" cy="300" r="80"/>
        <circle cx="300" cy="300" r="150"/>
        <circle cx="300" cy="300" r="200"/>
    </g>
    
    <!-- Electrons on orbitals -->
    <g fill="{self.colors['wave']}" opacity="0.8">
        <circle cx="300" cy="220" r="6"/>
        <circle cx="380" cy="300" r="6"/>
        <circle cx="300" cy="380" r="6"/>
        <circle cx="220" cy="300" r="6"/>
    </g>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="14" font-family="monospace">
        {element} atom | {protons} protons | Quantum coherence
    </text>
</svg>'''
        return svg
    
    def generate_cell_visualization(self, entity_data: Dict[str, Any]) -> str:
        """Generate cell visualization showing nested complexity (organelles, nucleus, etc.)"""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </radialGradient>
        <filter id="cellGlow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Cell membrane (coherence boundary) -->
    <circle cx="300" cy="300" r="180" fill="none" stroke="{self.colors['coherence']}" stroke-width="3" opacity="0.8"/>
    <circle cx="300" cy="300" r="185" fill="none" stroke="{self.colors['energy']}" stroke-width="1" opacity="0.4" stroke-dasharray="5,5"/>
    
    <!-- Nucleus (central control) -->
    <circle cx="300" cy="300" r="60" fill="{self.colors['consciousness']}" opacity="0.3"/>
    <circle cx="300" cy="300" r="60" fill="none" stroke="{self.colors['consciousness']}" stroke-width="2" opacity="0.7"/>
    
    <!-- DNA core (information spiral) -->
    <g stroke="{self.colors['wave']}" stroke-width="2" fill="none" opacity="0.6">
        <circle cx="300" cy="300" r="20"/>
        <ellipse cx="300" cy="300" rx="15" ry="25"/>
        <ellipse cx="300" cy="300" rx="25" ry="15"/>
    </g>
    
    <!-- Mitochondria (energy centers) -->
    <g fill="none" stroke="{self.colors['energy']}" stroke-width="2" opacity="0.6" filter="url(#cellGlow)">
        <ellipse cx="200" cy="200" rx="30" ry="45"/>
        <ellipse cx="400" cy="200" rx="30" ry="45"/>
        <ellipse cx="200" cy="400" rx="30" ry="45"/>
        <ellipse cx="400" cy="400" rx="30" ry="45"/>
    </g>
    
    <!-- Endoplasmic reticulum (network) -->
    <g stroke="{self.colors['structure']}" stroke-width="1.5" fill="none" opacity="0.4">
        <path d="M 150 300 Q 200 250 250 300 Q 200 350 150 300"/>
        <path d="M 450 300 Q 400 250 350 300 Q 400 350 450 300"/>
        <path d="M 300 150 Q 250 200 300 250 Q 350 200 300 150"/>
        <path d="M 300 450 Q 250 400 300 350 Q 350 400 300 450"/>
    </g>
    
    <!-- Ribosomes (protein centers) -->
    <g fill="{self.colors['wave']}" opacity="0.5">
        <circle cx="250" cy="250" r="8"/>
        <circle cx="350" cy="250" r="8"/>
        <circle cx="250" cy="350" r="8"/>
        <circle cx="350" cy="350" r="8"/>
        <circle cx="300" cy="380" r="8"/>
        <circle cx="300" cy="220" r="8"/>
    </g>
    
    <!-- Vesicles (transport bubbles) -->
    <g fill="{self.colors['coherence']}" opacity="0.3">
        <circle cx="180" cy="280" r="12"/>
        <circle cx="420" cy="320" r="12"/>
        <circle cx="320" cy="470" r="12"/>
        <circle cx="280" cy="140" r="12"/>
    </g>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="13" font-family="monospace">
        10^-5 m | 37 trillion cells | Boundary + Complexity
    </text>
    <text x="300" y="580" text-anchor="middle" fill="{self.colors['structure']}" font-size="11" font-family="monospace">
        Nucleus | Organelles | Membrane | Specialized Complexity
    </text>
</svg>'''
        return svg
    
    def generate_ecosystem_visualization(self, entity_data: Dict[str, Any]) -> str:
        """Generate ecosystem visualization showing interconnected complexity"""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#001030;stop-opacity:1" />
        </radialGradient>
        <filter id="ecosysGlow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Ecosystem boundary (sphere of influence) -->
    <circle cx="300" cy="300" r="190" fill="none" stroke="{self.colors['coherence']}" stroke-width="2" opacity="0.6" stroke-dasharray="8,4"/>
    
    <!-- Trophic levels (concentric rings showing energy flow) -->
    <g fill="none" stroke-width="1" opacity="0.3">
        <circle cx="300" cy="300" r="50" stroke="{self.colors['entropy']}"/>
        <circle cx="300" cy="300" r="100" stroke="{self.colors['energy']}"/>
        <circle cx="300" cy="300" r="150" stroke="{self.colors['structure']}"/>
    </g>
    
    <!-- Producers (plants) -->
    <g fill="{self.colors['coherence']}" opacity="0.6" filter="url(#ecosysGlow)">
        <polygon points="300,150 310,180 280,180"/>
        <polygon points="150,300 180,310 180,280"/>
        <polygon points="450,300 420,310 420,280"/>
        <polygon points="300,450 290,420 310,420"/>
    </g>
    
    <!-- Primary consumers (herbivores) -->
    <g fill="{self.colors['wave']}" opacity="0.6" filter="url(#ecosysGlow)">
        <circle cx="220" cy="220" r="15"/>
        <circle cx="380" cy="220" r="15"/>
        <circle cx="220" cy="380" r="15"/>
        <circle cx="380" cy="380" r="15"/>
    </g>
    
    <!-- Secondary consumers (carnivores) -->
    <g fill="{self.colors['energy']}" opacity="0.5" filter="url(#ecosysGlow)">
        <rect x="270" y="250" width="30" height="30" rx="5"/>
        <rect x="300" y="320" width="30" height="30" rx="5"/>
    </g>
    
    <!-- Decomposers (center nucleus) -->
    <circle cx="300" cy="300" r="25" fill="{self.colors['entropy']}" opacity="0.5"/>
    <circle cx="300" cy="300" r="25" fill="none" stroke="{self.colors['entropy']}" stroke-width="2" opacity="0.7"/>
    
    <!-- Energy flow pathways (arrows showing food chains) -->
    <g stroke="{self.colors['coherence']}" stroke-width="1.5" fill="none" opacity="0.4" marker-end="url(#arrowhead)">
        <path d="M 300 175 L 240 240"/>
        <path d="M 240 240 L 300 275"/>
        <path d="M 300 175 L 360 240"/>
        <path d="M 360 240 L 300 275"/>
        <path d="M 150 300 L 220 220"/>
        <path d="M 150 300 L 220 380"/>
        <path d="M 450 300 L 380 220"/>
        <path d="M 450 300 L 380 380"/>
    </g>
    
    <!-- Define arrow marker -->
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="{self.colors['coherence']}" opacity="0.5"/>
        </marker>
    </defs>
    
    <!-- Feedback loops -->
    <g stroke="{self.colors['structure']}" stroke-width="1" fill="none" opacity="0.3" stroke-dasharray="3,3">
        <circle cx="300" cy="300" r="120"/>
        <circle cx="300" cy="300" r="170"/>
    </g>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="13" font-family="monospace">
        Km+ | Interconnected Web | Multiple Species
    </text>
    <text x="300" y="580" text-anchor="middle" fill="{self.colors['structure']}" font-size="11" font-family="monospace">
        Producers | Consumers | Decomposers | Feedback Complexity
    </text>
</svg>'''
        return svg
    
    def generate_civilization_visualization(self, entity_data: Dict[str, Any]) -> str:
        """Generate civilization visualization showing abstract information complexity"""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000020;stop-opacity:1" />
        </radialGradient>
        <filter id="civGlow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Global consciousness network -->
    <circle cx="300" cy="300" r="190" fill="none" stroke="{self.colors['consciousness']}" stroke-width="2" opacity="0.7"/>
    <circle cx="300" cy="300" r="190" fill="none" stroke="{self.colors['wave']}" stroke-width="1" opacity="0.3" stroke-dasharray="10,5"/>
    
    <!-- Information centers (cities/organizations) -->
    <g fill="{self.colors['consciousness']}" opacity="0.6" filter="url(#civGlow)">
        <rect x="110" y="250" width="40" height="40" rx="5"/>
        <rect x="450" y="250" width="40" height="40" rx="5"/>
        <rect x="270" y="80" width="40" height="40" rx="5"/>
        <rect x="270" y="480" width="40" height="40" rx="5"/>
    </g>
    
    <!-- Knowledge systems (connected hubs) -->
    <g fill="{self.colors['energy']}" opacity="0.5">
        <circle cx="180" cy="180" r="12"/>
        <circle cx="420" cy="180" r="12"/>
        <circle cx="180" cy="420" r="12"/>
        <circle cx="420" cy="420" r="12"/>
    </g>
    
    <!-- Cultural structures -->
    <g fill="{self.colors['structure']}" opacity="0.4">
        <polygon points="300,200 320,240 280,240"/>
        <polygon points="300,400 280,360 320,360"/>
        <polygon points="200,300 160,310 160,290"/>
        <polygon points="400,300 440,310 440,290"/>
    </g>
    
    <!-- Global communication network -->
    <g stroke="{self.colors['coherence']}" stroke-width="1.5" fill="none" opacity="0.4">
        <path d="M 130 270 L 180 180"/>
        <path d="M 470 270 L 420 180"/>
        <path d="M 130 270 L 180 420"/>
        <path d="M 470 270 L 420 420"/>
        <path d="M 290 100 L 300 200"/>
        <path d="M 310 100 L 300 200"/>
        <path d="M 290 500 L 300 400"/>
        <path d="M 310 500 L 300 400"/>
        <path d="M 170 300 L 240 300"/>
        <path d="M 430 300 L 360 300"/>
    </g>
    
    <!-- Complex nested systems (fractality) -->
    <g fill="none" stroke="{self.colors['wave']}" stroke-width="1" opacity="0.3" stroke-dasharray="2,2">
        <circle cx="300" cy="300" r="80"/>
        <circle cx="300" cy="300" r="130"/>
        <circle cx="300" cy="300" r="160"/>
    </g>
    
    <!-- Information flow nodes -->
    <g fill="{self.colors['entropy']}" opacity="0.4">
        <circle cx="300" cy="180" r="8"/>
        <circle cx="180" cy="300" r="8"/>
        <circle cx="300" cy="420" r="8"/>
        <circle cx="420" cy="300" r="8"/>
        <circle cx="380" cy="380" r="6"/>
        <circle cx="220" cy="220" r="6"/>
    </g>
    
    <!-- Central consciousness/decision point -->
    <circle cx="300" cy="300" r="30" fill="{self.colors['consciousness']}" opacity="0.3"/>
    <circle cx="300" cy="300" r="30" fill="none" stroke="{self.colors['consciousness']}" stroke-width="2" opacity="0.6"/>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['consciousness']}" font-size="13" font-family="monospace">
        Global Scale | Information Systems | Abstract Complexity
    </text>
    <text x="300" y="580" text-anchor="middle" fill="{self.colors['coherence']}" font-size="11" font-family="monospace">
        Cities | Nations | Culture | Technology | Values | Knowledge
    </text>
</svg>'''
        return svg
    
    def generate_complexity_based_visualization(self, entity_data: Dict[str, Any], complexity: Dict[str, Any]) -> str:
        """
        Generate adaptive visualization based on complexity analysis.
        
        For unknown entities, creates visualization matching their determined complexity level.
        """
        level = complexity['level']
        name = complexity['name']
        total = complexity['total_complexity']
        
        # Determine base complexity
        if total < 10:
            # Simple particle-like
            return self._generate_simple_particle_visualization(name, level)
        elif total < 20:
            # Structured but not complex
            return self._generate_structured_entity_visualization(name, level)
        elif total < 35:
            # Complex organized system
            return self._generate_complex_system_visualization(name, level)
        else:
            # Highly complex, networked system
            return self._generate_hypercomplex_network_visualization(name, level)
    
    def _generate_simple_particle_visualization(self, name: str, level: int) -> str:
        """Generate visualization for simple particle-like entities."""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </radialGradient>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Fundamental entity -->
    <circle cx="300" cy="300" r="50" fill="{self.colors['wave']}" opacity="0.7"/>
    <circle cx="300" cy="300" r="80" fill="none" stroke="{self.colors['coherence']}" stroke-width="2" opacity="0.5"/>
    <circle cx="300" cy="300" r="120" fill="none" stroke="{self.colors['energy']}" stroke-width="1" opacity="0.3"/>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="14" font-family="monospace">
        {name} | Fundamental Entity | Level {level}
    </text>
</svg>'''
        return svg
    
    def _generate_structured_entity_visualization(self, name: str, level: int) -> str:
        """Generate visualization for structured entities with internal organization."""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </radialGradient>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Structured system with parts -->
    <circle cx="300" cy="300" r="140" fill="none" stroke="{self.colors['coherence']}" stroke-width="2" opacity="0.6"/>
    
    <!-- Internal structure -->
    <circle cx="300" cy="300" r="60" fill="none" stroke="{self.colors['structure']}" stroke-width="2" opacity="0.5"/>
    <circle cx="300" cy="300" r="20" fill="{self.colors['energy']}" opacity="0.5"/>
    
    <!-- Structural elements -->
    <g fill="{self.colors['wave']}" opacity="0.4">
        <circle cx="240" cy="240" r="15"/>
        <circle cx="360" cy="240" r="15"/>
        <circle cx="240" cy="360" r="15"/>
        <circle cx="360" cy="360" r="15"/>
    </g>
    
    <!-- Connectivity -->
    <g stroke="{self.colors['wave']}" stroke-width="1" fill="none" opacity="0.3">
        <line x1="300" y1="300" x2="240" y2="240"/>
        <line x1="300" y1="300" x2="360" y2="240"/>
        <line x1="300" y1="300" x2="240" y2="360"/>
        <line x1="300" y1="300" x2="360" y2="360"/>
    </g>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['coherence']}" font-size="14" font-family="monospace">
        {name} | Structured System | Level {level}
    </text>
</svg>'''
        return svg
    
    def _generate_complex_system_visualization(self, name: str, level: int) -> str:
        """Generate visualization for complex organized systems."""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </radialGradient>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Complex boundary -->
    <circle cx="300" cy="300" r="160" fill="none" stroke="{self.colors['consciousness']}" stroke-width="2" opacity="0.6"/>
    
    <!-- Multiple nested systems -->
    <g fill="none" stroke="{self.colors['structure']}" stroke-width="1.5" opacity="0.4">
        <circle cx="300" cy="300" r="70"/>
        <circle cx="300" cy="300" r="110"/>
    </g>
    
    <!-- Complex centers -->
    <g fill="{self.colors['consciousness']}" opacity="0.5">
        <circle cx="300" cy="200" r="20"/>
        <circle cx="200" cy="300" r="20"/>
        <circle cx="400" cy="300" r="20"/>
        <circle cx="300" cy="400" r="20"/>
    </g>
    
    <!-- Internal complexity nodes -->
    <g fill="{self.colors['energy']}" opacity="0.4">
        <circle cx="280" cy="250" r="12"/>
        <circle cx="320" cy="250" r="12"/>
        <circle cx="280" cy="350" r="12"/>
        <circle cx="320" cy="350" r="12"/>
    </g>
    
    <!-- Interconnection network -->
    <g stroke="{self.colors['wave']}" stroke-width="1.5" fill="none" opacity="0.3">
        <line x1="300" y1="200" x2="200" y2="300"/>
        <line x1="300" y1="200" x2="400" y2="300"/>
        <line x1="200" y1="300" x2="300" y2="400"/>
        <line x1="400" y1="300" x2="300" y2="400"/>
        <circle cx="300" cy="300" r="40"/>
    </g>
    
    <!-- Information flow -->
    <g stroke="{self.colors['coherence']}" stroke-width="1" fill="none" opacity="0.2" stroke-dasharray="3,3">
        <circle cx="300" cy="300" r="90"/>
        <circle cx="300" cy="300" r="140"/>
    </g>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['consciousness']}" font-size="14" font-family="monospace">
        {name} | Complex System | Level {level}
    </text>
</svg>'''
        return svg
    
    def _generate_hypercomplex_network_visualization(self, name: str, level: int) -> str:
        """Generate visualization for highly complex networked systems."""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="fieldGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.colors['field_background']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000020;stop-opacity:1" />
        </radialGradient>
    </defs>
    
    <rect width="600" height="600" fill="url(#fieldGradient)"/>
    
    <!-- Global network boundary -->
    <circle cx="300" cy="300" r="170" fill="none" stroke="{self.colors['consciousness']}" stroke-width="2" opacity="0.7"/>
    
    <!-- Hypercomplex nested layers -->
    <g fill="none" stroke-width="1" opacity="0.3">
        <circle cx="300" cy="300" r="50" stroke="{self.colors['coherence']}"/>
        <circle cx="300" cy="300" r="90" stroke="{self.colors['structure']}"/>
        <circle cx="300" cy="300" r="130" stroke="{self.colors['energy']}"/>
        <circle cx="300" cy="300" r="160" stroke="{self.colors['wave']}"/>
    </g>
    
    <!-- Major network hubs -->
    <g fill="{self.colors['consciousness']}" opacity="0.6">
        <circle cx="300" cy="170" r="18"/>
        <circle cx="170" cy="300" r="18"/>
        <circle cx="430" cy="300" r="18"/>
        <circle cx="300" cy="430" r="18"/>
    </g>
    
    <!-- Secondary nodes -->
    <g fill="{self.colors['energy']}" opacity="0.5">
        <circle cx="240" cy="220" r="12"/>
        <circle cx="360" cy="220" r="12"/>
        <circle cx="240" cy="380" r="12"/>
        <circle cx="360" cy="380" r="12"/>
    </g>
    
    <!-- Tertiary nodes -->
    <g fill="{self.colors['wave']}" opacity="0.4">
        <circle cx="220" cy="300" r="8"/>
        <circle cx="380" cy="300" r="8"/>
        <circle cx="300" cy="220" r="8"/>
        <circle cx="300" cy="380" r="8"/>
    </g>
    
    <!-- Complex interconnection web -->
    <g stroke="{self.colors['coherence']}" stroke-width="1" fill="none" opacity="0.3">
        <line x1="300" y1="170" x2="170" y2="300"/>
        <line x1="300" y1="170" x2="430" y2="300"/>
        <line x1="170" y1="300" x2="300" y2="430"/>
        <line x1="430" y1="300" x2="300" y2="430"/>
        <line x1="240" y1="220" x2="360" y2="220"/>
        <line x1="240" y1="380" x2="360" y2="380"/>
        <line x1="220" y1="300" x2="380" y2="300"/>
    </g>
    
    <!-- Feedback loops -->
    <g stroke="{self.colors['structure']}" stroke-width="1" fill="none" opacity="0.25" stroke-dasharray="4,2">
        <circle cx="300" cy="300" r="75"/>
        <circle cx="300" cy="300" r="120"/>
    </g>
    
    <!-- Central integration point -->
    <circle cx="300" cy="300" r="25" fill="{self.colors['consciousness']}" opacity="0.3"/>
    <circle cx="300" cy="300" r="25" fill="none" stroke="{self.colors['consciousness']}" stroke-width="2" opacity="0.6"/>
    
    <text x="300" y="560" text-anchor="middle" fill="{self.colors['consciousness']}" font-size="13" font-family="monospace">
        {name} | Hypercomplex Network | Level {level}
    </text>
    <text x="300" y="580" text-anchor="middle" fill="{self.colors['coherence']}" font-size="11" font-family="monospace">
        Multi-scale Integration | Feedback Loops | Emergent Properties
    </text>
</svg>'''
        return svg
    
    def save_visualization(self, name: str, svg_content: str) -> str:
        """Save SVG visualization to file."""
        filepath = self.output_dir / f"{name}.svg"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Generated: {filepath}")
        return str(filepath)
    
    def generate_all_standard_entities(self) -> Dict[str, str]:
        """Generate visualizations for all standard entities."""
        visualizations = {
            'electron_field.svg': self.generate_electron_visualization(),
            'water_molecule_field.svg': self.generate_water_molecule_visualization(),
            'human_field.svg': self.generate_human_visualization(),
        }
        
        results = {}
        for filename, svg_content in visualizations.items():
            base_name = filename.replace('.svg', '')
            self.save_visualization(base_name, svg_content)
            results[base_name] = str(self.output_dir / filename)
        
        return results


def main():
    """Generate all entity visualizations."""
    print("=" * 70)
    print("FIELD IMAGE GENERATOR — Auto-generating entity visualizations")
    print("=" * 70)
    
    generator = FieldImageGenerator()
    results = generator.generate_all_standard_entities()
    
    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nGenerated {len(results)} visualizations:")
    for name, path in results.items():
        print(f"  ✓ {name}")
    
    print(f"\nLocation: {generator.output_dir}")
    print("\nThese visualizations can be used by ENCYCLOPEDIA.html")
    print("Load via: http://localhost:5000/?entity=Electron")


if __name__ == "__main__":
    main()
