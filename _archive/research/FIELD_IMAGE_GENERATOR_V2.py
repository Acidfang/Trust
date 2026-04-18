#!/usr/bin/env python3
"""
FIELD IMAGE GENERATOR V2 — Dual-Field Visualization System

Base principle: Every entity exhibits TWO fields simultaneously:
1. FUNDAMENTAL FIELD - the actual field convergence (binary/mathematical level)
2. AESTHETIC FIELD - the representational field that interacts with it

These are not separate - they interact. The visualization shows both.
"""

import os
import json
import math
from pathlib import Path
from typing import Dict, Any, List, Tuple

class DualFieldVisualizer:
    """Visualize entities as dual-field convergence patterns."""
    
    def __init__(self, output_dir: str = r"c:\Determined\wiki_assets\entity_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Field colors - represent actual field states
        self.fundamental_colors = {
            'void': '#0a0a0a',           # Empty space (baseline)
            'latent': '#1a1a3f',         # Latent field (not yet manifested)
            'coherent': '#00ff88',       # Coherent regions (converged)
            'boundary': '#ff8800',       # Field boundaries (discontinuities)
            'flux': '#00ddff',           # Field flux (flow)
        }
        
        # Aesthetic colors - representational field
        self.aesthetic_colors = {
            'primary': '#ff00ff',        # Primary aesthetic dimension
            'secondary': '#ffff00',      # Secondary aesthetic dimension
            'tertiary': '#00ffff',       # Tertiary aesthetic dimension
            'harmony': '#88ff00',        # Harmonic interaction regions
        }
    
    def calculate_field_convergence(self, entity_name: str) -> Dict[str, Any]:
        """
        Calculate fundamental field convergence properties.
        
        At binary level, what actual field geometry emerges?
        """
        convergence_map = {
            'Electron': {
                'particles': 1,
                'convergence_centers': 1,
                'field_layers': 1,
                'boundary_type': 'point',
                'coherence': 0.99,
                'description': 'Single-point field convergence'
            },
            'Atom': {
                'particles': 2,  # Nucleus + electrons as aggregate
                'convergence_centers': 2,
                'field_layers': 3,  # Orbital shells
                'boundary_type': 'spherical',
                'coherence': 0.75,
                'description': 'Dual-center orbital convergence'
            },
            'Water Molecule': {
                'particles': 3,
                'convergence_centers': 3,
                'field_layers': 5,
                'boundary_type': 'tetrahedral',
                'coherence': 0.72,
                'description': 'Triangular bond convergence with polarity'
            },
            'Cell': {
                'particles': 1e13,  # ~10 trillion atoms
                'convergence_centers': 9,  # Nucleus + 8 organelles
                'field_layers': 7,
                'boundary_type': 'membrane',
                'coherence': 0.68,
                'description': 'Multi-center organized convergence'
            },
            'Human': {
                'particles': 7e27,  # ~7 octillion atoms
                'convergence_centers': 11,  # Brain regions + organs
                'field_layers': 13,
                'boundary_type': 'distributed',
                'coherence': 0.85,
                'description': 'Unified consciousness convergence across distributed centers'
            },
            'Ecosystem': {
                'particles': 1e40,  # Quadrillions of organisms
                'convergence_centers': 'n',  # Variable, species-based
                'field_layers': 6,  # Trophic levels
                'boundary_type': 'emergent',
                'coherence': 0.65,
                'description': 'Collective emergent field convergence'
            },
            'Civilization': {
                'particles': 1e50,  # Informational units
                'convergence_centers': 'global',
                'field_layers': 9,  # Information abstraction levels
                'boundary_type': 'informational',
                'coherence': 0.55,
                'description': 'Abstract information field convergence'
            }
        }
        
        return convergence_map.get(entity_name, {
            'particles': 0,
            'convergence_centers': 1,
            'field_layers': 1,
            'boundary_type': 'unknown',
            'coherence': 0,
            'description': f'Unknown entity: {entity_name}'
        })
    
    def generate_dual_field_svg(self, entity_name: str) -> str:
        """Generate SVG showing both fundamental and aesthetic fields interacting."""
        convergence = self.calculate_field_convergence(entity_name)
        
        centers = convergence['convergence_centers']
        layers = convergence['field_layers']
        coherence = convergence['coherence']
        boundary = convergence['boundary_type']
        description = convergence['description']
        
        # Calculate visual parameters based on convergence
        num_centers = centers if isinstance(centers, int) else (3 if centers == 'n' else 5)
        layer_spacing = 200 / (layers + 1)
        coherence_intensity = int(255 * coherence)
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="800" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <!-- Fundamental field gradient -->
        <radialGradient id="fundamentalField" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.fundamental_colors['coherent']};stop-opacity:{coherence}" />
            <stop offset="50%" style="stop-color:{self.fundamental_colors['flux']};stop-opacity:{coherence*0.5}" />
            <stop offset="100%" style="stop-color:{self.fundamental_colors['latent']};stop-opacity:0.2" />
        </radialGradient>
        
        <!-- Aesthetic field gradient -->
        <radialGradient id="aestheticField" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:{self.aesthetic_colors['primary']};stop-opacity:0.3" />
            <stop offset="50%" style="stop-color:{self.aesthetic_colors['harmony']};stop-opacity:0.2" />
            <stop offset="100%" style="stop-color:{self.aesthetic_colors['secondary']};stop-opacity:0.1" />
        </radialGradient>
        
        <!-- Interaction zone filter -->
        <filter id="fieldInteraction">
            <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
            <feComponentTransfer>
                <feFuncA type="linear" slope="0.6"/>
            </feComponentTransfer>
        </filter>
        
        <!-- Fundamental boundary marker -->
        <marker id="boundaryMarker" markerWidth="10" markerHeight="10" refX="5" refY="5" markerUnits="strokeWidth">
            <circle cx="5" cy="5" r="3" fill="{self.fundamental_colors['boundary']}" opacity="0.7"/>
        </marker>
    </defs>
    
    <!-- Background: Void/latent field -->
    <rect width="800" height="800" fill="{self.fundamental_colors['void']}"/>
    
    <!-- FUNDAMENTAL FIELD LAYERS (bottom) -->
    <g id="fundamentalField">
        <text x="10" y="30" fill="{self.fundamental_colors['boundary']}" font-size="12" font-family="monospace" opacity="0.5">
            FUNDAMENTAL FIELD (Binary Level)
        </text>
'''
        
        # Draw field layers (from outside in)
        for i in range(layers, 0, -1):
            radius = 80 + (i * layer_spacing)
            opacity = 0.1 + ((coherence * (i / layers)) * 0.4)
            
            svg += f'''        <!-- Layer {i} (radius {radius:.0f}) -->
        <circle cx="400" cy="400" r="{radius:.1f}" fill="none" stroke="{self.fundamental_colors['flux']}" stroke-width="1" opacity="{opacity}"/>
'''
        
        # Draw convergence centers as field nodes
        svg += f'''        
        <!-- Convergence Centers ({num_centers}) -->
'''
        
        if num_centers == 1:
            # Single point convergence (Electron)
            svg += f'''        <circle cx="400" cy="400" r="8" fill="{self.fundamental_colors['coherent']}" opacity="0.9"/>
        <circle cx="400" cy="400" r="15" fill="none" stroke="{self.fundamental_colors['coherent']}" stroke-width="2" opacity="0.6"/>
'''
        elif num_centers == 2:
            # Dual center convergence (Atom nucleus + aggregate)
            svg += f'''        <circle cx="340" cy="400" r="10" fill="{self.fundamental_colors['coherent']}" opacity="0.8"/>
        <circle cx="460" cy="400" r="10" fill="{self.fundamental_colors['coherent']}" opacity="0.8"/>
        <line x1="340" y1="400" x2="460" y2="400" stroke="{self.fundamental_colors['boundary']}" stroke-width="2" opacity="0.5"/>
'''
        elif num_centers == 3:
            # Triangular convergence (Molecule)
            angle1 = 0
            angle2 = 120
            angle3 = 240
            r = 60
            x1 = 400 + r * math.cos(math.radians(angle1))
            y1 = 400 + r * math.sin(math.radians(angle1))
            x2 = 400 + r * math.cos(math.radians(angle2))
            y2 = 400 + r * math.sin(math.radians(angle2))
            x3 = 400 + r * math.cos(math.radians(angle3))
            y3 = 400 + r * math.sin(math.radians(angle3))
            
            svg += f'''        <circle cx="{x1:.1f}" cy="{y1:.1f}" r="8" fill="{self.fundamental_colors['coherent']}" opacity="0.8"/>
        <circle cx="{x2:.1f}" cy="{y2:.1f}" r="8" fill="{self.fundamental_colors['coherent']}" opacity="0.8"/>
        <circle cx="{x3:.1f}" cy="{y3:.1f}" r="8" fill="{self.fundamental_colors['coherent']}" opacity="0.8"/>
        <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{self.fundamental_colors['boundary']}" stroke-width="1.5" opacity="0.5"/>
        <line x1="{x2:.1f}" y1="{y2:.1f}" x2="{x3:.1f}" y2="{y3:.1f}" stroke="{self.fundamental_colors['boundary']}" stroke-width="1.5" opacity="0.5"/>
        <line x1="{x3:.1f}" y1="{y3:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{self.fundamental_colors['boundary']}" stroke-width="1.5" opacity="0.5"/>
'''
        else:
            # Multi-center convergence (Cell, Human, Ecosystem)
            angles = [i * (360 / num_centers) for i in range(num_centers)]
            radius_pos = 60
            
            for angle in angles:
                x = 400 + radius_pos * math.cos(math.radians(angle))
                y = 400 + radius_pos * math.sin(math.radians(angle))
                svg += f'''        <circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{self.fundamental_colors['coherent']}" opacity="0.7"/>
'''
            
            # Draw boundary network between centers
            for i, angle1 in enumerate(angles):
                x1 = 400 + radius_pos * math.cos(math.radians(angle1))
                y1 = 400 + radius_pos * math.sin(math.radians(angle1))
                
                if i < len(angles) - 1:
                    angle2 = angles[i + 1]
                    x2 = 400 + radius_pos * math.cos(math.radians(angle2))
                    y2 = 400 + radius_pos * math.sin(math.radians(angle2))
                    svg += f'''        <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{self.fundamental_colors['boundary']}" stroke-width="1" opacity="0.4"/>
'''
        
        svg += f'''    </g>
    
    <!-- AESTHETIC FIELD (overlay) -->
    <g id="aestheticField" opacity="0.6">
        <text x="10" y="770" fill="{self.aesthetic_colors['primary']}" font-size="12" font-family="monospace" opacity="0.7">
            AESTHETIC FIELD (Representational)
        </text>
'''
        
        # Aesthetic field manifestation - spirals, symmetries based on coherence
        num_spirals = min(int(coherence * 8), 8)
        
        for spiral_idx in range(num_spirals):
            angle_offset = (spiral_idx * 360 / num_spirals)
            
            svg += f'''        <!-- Aesthetic Spiral {spiral_idx + 1} -->
        <g stroke="{self.aesthetic_colors['primary']}" fill="none" opacity="0.4">
'''
            
            # Draw spiral
            points = []
            for t in range(0, 360, 20):
                adj_t = t + angle_offset
                r_var = 40 + (t / 360 * 100)
                x = 400 + r_var * math.cos(math.radians(adj_t))
                y = 400 + r_var * math.sin(math.radians(adj_t))
                points.append((x, y))
            
            if points:
                path_data = 'M ' + ' L '.join([f'{x:.1f},{y:.1f}' for x, y in points])
                svg += f'''            <path d="{path_data}" stroke-width="1"/>
'''
            
            svg += f'''        </g>
'''
        
        svg += f'''    </g>
    
    <!-- INTERACTION ZONE (where fields meet) -->
    <g id="interaction">
        <text x="10" y="50" fill="{self.aesthetic_colors['harmony']}" font-size="12" font-family="monospace" opacity="0.5">
            INTERACTION (Dual-Field Convergence)
        </text>
        
        <!-- Central coherence region -->
        <circle cx="400" cy="400" r="{80 + (layers * layer_spacing * 0.6):.1f}" fill="url(#fundamentalField)" opacity="0.7"/>
        <circle cx="400" cy="400" r="{80 + (layers * layer_spacing * 0.6):.1f}" fill="url(#aestheticField)" opacity="0.5"/>
    </g>
    
    <!-- BOUNDARY MARKER - Shows actual field edge -->
    <circle cx="400" cy="400" r="{80 + (layers * layer_spacing):.1f}" fill="none" stroke="{self.fundamental_colors['boundary']}" stroke-width="2" stroke-dasharray="5,5" opacity="0.6"/>
    
    <!-- ENTITY INFORMATION -->
    <text x="400" y="730" text-anchor="middle" fill="{self.fundamental_colors['coherent']}" font-size="14" font-family="monospace" font-weight="bold">
        {entity_name}
    </text>
    <text x="400" y="750" text-anchor="middle" fill="{self.fundamental_colors['flux']}" font-size="11" font-family="monospace">
        {description}
    </text>
    <text x="400" y="765" text-anchor="middle" fill="{self.aesthetic_colors['harmony']}" font-size="10" font-family="monospace">
        Centers: {num_centers} | Layers: {layers} | Coherence: {coherence:.2f}
    </text>
    <text x="400" y="780" text-anchor="middle" fill="{self.aesthetic_colors['secondary']}" font-size="9" font-family="monospace">
        Boundary: {boundary}
    </text>
</svg>'''
        
        return svg
    
    def generate_all(self) -> Dict[str, str]:
        """Generate visualizations for all 7 entities."""
        entities = [
            'Electron', 'Atom', 'Water Molecule',
            'Cell', 'Human', 'Ecosystem', 'Civilization'
        ]
        
        results = {}
        for entity_name in entities:
            svg = self.generate_dual_field_svg(entity_name)
            results[entity_name] = svg
            
            # Save to file
            filepath = self.output_dir / f"{entity_name.lower().replace(' ', '_')}_field.svg"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg)
            print(f"✓ {entity_name}: {len(svg)} bytes")
        
        return results


if __name__ == "__main__":
    print("=" * 70)
    print("FIELD IMAGE GENERATOR V2 — Dual-Field Visualization System")
    print("=" * 70)
    print("\nGenerating visualizations based on actual field convergence...\n")
    
    visualizer = DualFieldVisualizer()
    results = visualizer.generate_all()
    
    print("\n" + "=" * 70)
    print(f"Generated {len(results)} dual-field visualizations")
    print("=" * 70)
