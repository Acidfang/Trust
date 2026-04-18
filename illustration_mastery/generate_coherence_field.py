#!/usr/bin/env python3
"""
Generate Coherence Field Visualization
Shows potential energy distribution across the system
Darker areas = higher tension (unresolved), lighter = resolved
"""

from pathlib import Path

class CoherenceFieldVisualizer:
    """Create SVG showing coherence field with entry markers"""
    
    def __init__(self):
        self.width = 1200
        self.height = 800
    
    def generate(self):
        svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            
            # Define gradients for coherence field
            '<linearGradient id="coherence-gradient-horizontal" x1="0%" y1="0%" x2="100%" y2="0%">',
            '  <stop offset="0%" style="stop-color:#8B0000;stop-opacity:0.4" />',  # High tension (red)
            '  <stop offset="50%" style="stop-color:#FFD700;stop-opacity:0.3" />',  # Medium (yellow)
            '  <stop offset="100%" style="stop-color:#006400;stop-opacity:0.2" />',  # Resolved (green)
            '</linearGradient>',
            
            '<radialGradient id="entry-marker-field" cx="50%" cy="50%" r="50%">',
            '  <stop offset="0%" style="stop-color:#FF4444;stop-opacity:0.5" />',  # Hot spot
            '  <stop offset="100%" style="stop-color:#FF4444;stop-opacity:0" />',  # Dissipates
            '</radialGradient>',
            
            '<style>',
            '  .tier-line { stroke: #333; stroke-width: 2; fill: none; }',
            '  .tier-label { font-size: 14px; font-weight: bold; }',
            '  .entry-label { font-size: 11px; fill: #333; }',
            '  .state-marker { font-size: 10px; font-weight: bold; }',
            '</style>',
            '</defs>',
            
            # Title
            f'<text x="{self.width/2}" y="35" text-anchor="middle" font-size="24" font-weight="bold">',
            'COHERENCE FIELD: Potential Energy Distribution',
            '</text>',
            
            f'<text x="{self.width/2}" y="55" text-anchor="middle" font-size="12" fill="#666">',
            'Red/Dark = High Tension (Unresolved) | Green/Light = Low Tension (Resolved)',
            '</text>',
        ]
        
        # Main coherence field background gradient
        svg.append(
            f'<rect x="50" y="100" width="{self.width - 100}" height="600" '
            'fill="url(#coherence-gradient-horizontal)" stroke="#999" stroke-width="1" />'
        )
        
        # Tier dividers and labels
        tier_positions = [
            {'x': 50, 'label': 'Tier -1\n(Self)', 'width': 150},
            {'x': 200, 'label': 'Tier 0\n(Connection)', 'width': 120},
            {'x': 320, 'label': 'Tier 1\n(Conflict)', 'width': 100},
            {'x': 420, 'label': 'Tier 2\n(Consist.)', 'width': 110},
            {'x': 530, 'label': 'Tier 3\n(Transcend.)', 'width': 470},
        ]
        
        current_x = 50
        for i, tier in enumerate(tier_positions):
            # Vertical divider
            if i > 0:
                svg.append(
                    f'<line x1="{current_x}" y1="100" x2="{current_x}" y2="700" '
                    'stroke="#666" stroke-width="1" stroke-dasharray="3,3" />'
                )
            
            # Tier label
            label_x = current_x + (tier['width'] // 2)
            svg.append(
                f'<text x="{label_x}" y="720" text-anchor="middle" class="tier-label">'
                f'{tier["label"]}'
                '</text>'
            )
            
            current_x += tier['width']
        
        # Entry marker "hot spots" showing unresolved tensions
        entry_markers = [
            # Tier -1 entry markers (high tension areas)
            {'x': 80, 'y': 200, 'name': 'pattern', 'intensity': 0.8, 'size': 60},
            {'x': 140, 'y': 350, 'name': 'unjustified', 'intensity': 0.7, 'size': 50},
            {'x': 110, 'y': 500, 'name': 'unresolved', 'intensity': 0.9, 'size': 70},
            
            # Tier 0 markers
            {'x': 220, 'y': 250, 'name': 'distorted', 'intensity': 0.6, 'size': 45},
            {'x': 280, 'y': 400, 'name': 'deferred', 'intensity': 0.7, 'size': 55},
            {'x': 240, 'y': 550, 'name': 'comfort-based', 'intensity': 0.65, 'size': 50},
            
            # Tier 1 markers
            {'x': 350, 'y': 300, 'name': 'surface conflict', 'intensity': 0.7, 'size': 48},
            {'x': 400, 'y': 450, 'name': 'unlearned', 'intensity': 0.75, 'size': 52},
            
            # Tier 2 markers  
            {'x': 460, 'y': 280, 'name': 'drift', 'intensity': 0.6, 'size': 42},
            {'x': 520, 'y': 500, 'name': 'slide', 'intensity': 0.65, 'size': 45},
            
            # Tier 3 markers (fewer, less intense - almost resolved)
            {'x': 700, 'y': 350, 'name': 'resist', 'intensity': 0.4, 'size': 35},
        ]
        
        for marker in entry_markers:
            # Entry marker heat spot (radial gradient)
            opacity = marker['intensity'] * 0.6
            svg.append(
                f'<circle cx="{marker["x"]}" cy="{marker["y"]}" r="{marker["size"]}" '
                f'fill="#FF4444" opacity="{opacity}" />'
            )
            
            # Label
            svg.append(
                f'<text x="{marker["x"]}" y="{marker["y"] + 5}" '
                'text-anchor="middle" class="entry-label" fill="white" font-weight="bold" '
                'stroke="white" stroke-width="0.5">'
                f'{marker["name"]}'
                '</text>'
            )
        
        # Overlay: Show "resolved" regions in Tiers 2 and 3
        svg.append(
            f'<rect x="530" y="100" width="470" height="600" '
            'fill="#00DD00" opacity="0.08" />'
        )
        
        svg.append(
            f'<text x="765" y="400" text-anchor="middle" font-size="14" '
            'fill="#006400" font-weight="bold" opacity="0.5">'
            'Higher Integration'
            '</text>'
        )
        
        # Legend at bottom
        legend_y = 780
        
        svg.append(
            f'<text x="50" y="{legend_y}" font-size="12" font-weight="bold">Legend:</text>'
        )
        
        svg.append(
            f'<circle cx="180" cy="{legend_y - 6}" r="8" fill="#FF4444" opacity="0.6" />'
        )
        svg.append(
            f'<text x="195" y="{legend_y}" font-size="11">'
            'Entry Marker Hot Spot (unresolved tension accumulation)'
            '</text>'
        )
        
        svg.append(
            f'<rect x="520" y="{legend_y - 12}" width="15" height="15" '
            'fill="#006400" opacity="0.2" />'
        )
        svg.append(
            f'<text x="545" y="{legend_y}" font-size="11">'
            'Resolved Region (lower tension)'
            '</text>'
        )
        
        svg.append('</svg>')
        return '\n'.join(svg)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate())
        print(f"✓ Coherence field saved: {filepath}")


if __name__ == '__main__':
    output_dir = Path(__file__).parent / 'examples'
    output_dir.mkdir(exist_ok=True)
    
    print("Generating Coherence Field visualization...")
    visualizer = CoherenceFieldVisualizer()
    visualizer.save(output_dir / 'coherence_field_distribution.svg')
    print("\nVisualization shows:")
    print("  - Potential energy distribution across all tiers")
    print("  - Entry marker 'hot spots' showing accumulated tension")
    print("  - Gradient from high tension (Tier -1) to resolved (Tier 3)")
    print("  - How unresolved markers create localized high-energy regions")
