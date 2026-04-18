#!/usr/bin/env python3
"""
Generate Tier -1 State Progression Illustration
Demonstrates complete visual encoding of self-examination journey through coherence

Core teaching: Self-examination requires moving through awareness, distinction, causality,
regulation, consistency, correction, alignment, persistence, adaptability, and integrity—
with necessary loops back at certain points, full reset possible at adaptability.
"""

class TierMinusOneIllustrator:
    """Generate SVG showing Tier -1 progression with all visual encodings"""
    
    def __init__(self, width=1000, height=1200):
        self.width = width
        self.height = height
        self.states = [
            {'id': 'T-1.1', 'name': 'Awareness', 'y': 100, 'type': 'decision', 'size': 30},
            {'id': 'T-1.2', 'name': 'Distinction', 'y': 200, 'type': 'work', 'size': 30},
            {'id': 'T-1.3', 'name': 'Causality', 'y': 300, 'type': 'work', 'size': 35},
            {'id': 'T-1.4', 'name': 'Regulation', 'y': 420, 'type': 'decision', 'size': 32},
            {'id': 'T-1.5', 'name': 'Consistency', 'y': 530, 'type': 'work', 'size': 30},
            {'id': 'T-1.6', 'name': 'Correction', 'y': 630, 'type': 'work', 'size': 33},
            {'id': 'T-1.7', 'name': 'Alignment', 'y': 740, 'type': 'work', 'size': 34},
            {'id': 'T-1.8', 'name': 'Persistence', 'y': 860, 'type': 'decision', 'size': 32},
            {'id': 'T-1.9', 'name': 'Adaptability', 'y': 970, 'type': 'decision', 'size': 35},
            {'id': 'T-1.10', 'name': 'Integrity', 'y': 1070, 'type': 'work', 'size': 36},
        ]
        
        # Entry markers that trigger loops
        self.loop_backs = [
            {'from': 2, 'to': 1, 'marker': 'pattern', 'style': 'loop-back'},  # T-1.3 → T-1.2
            {'from': 5, 'to': 3, 'marker': 'unjustified', 'style': 'loop-back'},  # T-1.6 → T-1.4
            {'from': 8, 'to': 0, 'marker': 'unresolved', 'style': 'escalate-path'},  # T-1.9 → T-1.1
        ]
        
        self.cx = width / 2
        self.svg_content = []
    
    def build_header(self):
        """Add title and description"""
        self.svg_content.append(
            f'<text x="{self.cx}" y="30" text-anchor="middle" '
            'font-size="24" font-weight="bold">'
            'TIER -1 State Progression: Self (Coherence)'
            '</text>'
        )
        self.svg_content.append(
            f'<text x="{self.cx}" y="50" text-anchor="middle" '
            'font-size="12" fill="#666">'
            'Awareness → Distinction → Causality → Regulation → Consistency → '
            'Correction → Alignment → Persistence → Adaptability → Integrity'
            '</text>'
        )
    
    def build_styles(self):
        """Return <style> section with all visual encodings"""
        return '''<style>
      /* State type encoding */
      .decision-point { fill: #8B0000; }  /* Dark red - decision required */
      .work-state { fill: #006400; }      /* Dark green - work required */
      .prerequisite { fill: #4169E1; }    /* Royal blue */
      
      /* Path encoding */
      .primary-path { stroke: #333; stroke-width: 2; fill: none; }
      .loop-back { stroke: #cc6666; stroke-width: 2; stroke-dasharray: 5,5; fill: none; }
      .escalate-path { stroke: #ff9999; stroke-width: 2.5; stroke-dasharray: 3,3; fill: none; }
      
      /* Text */
      text { font-family: Arial, sans-serif; }
      .state-label { font-size: 12px; font-weight: bold; }
      .note { font-size: 10px; fill: #666; }
      .annotation { font-size: 11px; }
      
      /* Boxes */
      .info-box { fill: #f9f9f9; stroke: #ccc; stroke-width: 1; }
      .gate-box { fill: #E8F0FF; stroke: #4169E1; stroke-width: 2; }
    </style>'''
    
    def build_markers(self):
        """Return arrow markers for different path types"""
        return '''<defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333" />
    </marker>
    <marker id="arrow-loop" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#cc6666" />
    </marker>
    <marker id="arrow-escalate" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#ff9999" />
    </marker>
  </defs>'''
    
    def build_states(self):
        """Add state nodes with visual encoding"""
        for i, state in enumerate(self.states):
            state_class = 'decision-point' if state['type'] == 'decision' else 'work-state'
            opacity = 0.80 + (i * 0.01)  # Slightly increase opacity downward
            
            self.svg_content.append(
                f'<!-- {state["id"]}: {state["name"]} -->'
            )
            self.svg_content.append(
                f'<g transform="translate({self.cx}, {state["y"]})">'
            )
            
            # Node circle (size encodes complexity/depth)
            self.svg_content.append(
                f'<circle r="{state["size"]}" class="{state_class}" opacity="{opacity}" />'
            )
            
            # State ID label
            self.svg_content.append(
                '<text x="0" y="0" text-anchor="middle" dy="0.3em" '
                'fill="white" class="state-label">'
                f'{state["id"]}'
                '</text>'
            )
            
            # State name label
            self.svg_content.append(
                f'<text x="0" y="{state["size"] + 20}" text-anchor="middle" class="note">'
                f'{state["name"]}'
                '</text>'
            )
            
            self.svg_content.append('</g>')
    
    def build_primary_paths(self):
        """Add straight downward paths between consecutive states"""
        self.svg_content.append('<!-- Primary progression paths -->')
        
        for i in range(len(self.states) - 1):
            y1 = self.states[i]['y'] + self.states[i]['size'] + 5
            y2 = self.states[i+1]['y'] - self.states[i+1]['size'] - 5
            self.svg_content.append(
                f'<path d="M {self.cx},{y1} L {self.cx},{y2}" '
                f'class="primary-path" marker-end="url(#arrow)" />'
            )
    
    def build_loop_backs(self):
        """Add curved paths showing loops back (encoding entry markers)"""
        self.svg_content.append('<!-- Loop-back paths (entry markers) -->')
        
        for loop in self.loop_backs:
            from_idx = loop['from']
            to_idx = loop['to']
            marker_name = loop['marker']
            style = loop['style']
            
            from_y = self.states[from_idx]['y']
            to_y = self.states[to_idx]['y']
            from_x = self.cx + self.states[from_idx]['size'] + 20
            
            # Control point for curve (off to the right)
            control_x = self.cx + 150
            control_y = (from_y + to_y) / 2
            
            marker_id = 'arrow-loop' if style == 'loop-back' else 'arrow-escalate'
            
            self.svg_content.append(
                '<!-- Loop from T-{} back to T-{} (entry: {}) -->'.format(
                    from_idx + 1, to_idx + 1, marker_name
                )
            )
            self.svg_content.append(
                f'<path d="M {from_x},{from_y} Q {control_x},{control_y} '
                f'{from_x},{to_y}" class="{style}" marker-end="url(#{marker_id})" />'
            )
            
            # Label for loop
            label_x = control_x + 30
            label_y = control_y - 10
            self.svg_content.append(
                f'<text x="{label_x}" y="{label_y}" class="note">'
                f'[entry: {marker_name}]'
                '</text>'
            )
    
    def build_prerequisite_gate(self):
        """Add gate showing completion requirement"""
        self.svg_content.append('<!-- Prerequisite Sheet as Gate -->')
        self.svg_content.append(
            '<g transform="translate(400, 1120)">'
        )
        self.svg_content.append(
            '<rect x="0" y="0" width="200" height="60" rx="5" class="gate-box" />'
        )
        self.svg_content.append(
            '<text x="100" y="20" text-anchor="middle" font-weight="bold">'
            'PREREQUISITE SHEET'
            '</text>'
        )
        self.svg_content.append(
            '<text x="100" y="40" text-anchor="middle" font-size="11">'
            'Required to enter Tier 0'
            '</text>'
        )
        self.svg_content.append(
            '<text x="100" y="55" text-anchor="middle" font-size="10" fill="#666">'
            '(All entry markers resolved)'
            '</text>'
        )
        self.svg_content.append('</g>')
    
    def build_legend(self):
        """Add legend explaining visual language"""
        self.svg_content.append('<!-- Legend -->')
        self.svg_content.append(
            '<g transform="translate(50, 1100)">'
        )
        self.svg_content.append(
            '<text font-weight="bold" font-size="12">Legend:</text>'
        )
        
        # Decision point
        self.svg_content.append(
            '<circle cx="120" cy="0" r="8" class="decision-point" />'
        )
        self.svg_content.append(
            '<text x="135" y="4" font-size="11">Decision Point</text>'
        )
        
        # Work state
        self.svg_content.append(
            '<circle cx="320" cy="0" r="8" class="work-state" />'
        )
        self.svg_content.append(
            '<text x="335" y="4" font-size="11">Work State</text>'
        )
        
        self.svg_content.append('</g>')
        
        self.svg_content.append(
            '<g transform="translate(50, 1130)">'
        )
        self.svg_content.append(
            '<line x1="0" y1="0" x2="30" y1="0" class="primary-path" marker-end="url(#arrow)" />'
        )
        self.svg_content.append(
            '<text x="40" y="4" font-size="11">Primary Path</text>'
        )
        
        self.svg_content.append(
            '<line x1="200" y1="0" x2="230" y1="0" class="loop-back" marker-end="url(#arrow-loop)" />'
        )
        self.svg_content.append(
            '<text x="240" y="4" font-size="11">Loop Back (entry marker)</text>'
        )
        
        self.svg_content.append(
            '<line x1="500" y1="0" x2="530" y1="0" class="escalate-path" marker-end="url(#arrow-escalate)" />'
        )
        self.svg_content.append(
            '<text x="540" y="4" font-size="11">Full Reset</text>'
        )
        
        self.svg_content.append('</g>')
    
    def build_annotations(self):
        """Add teaching annotations"""
        self.svg_content.append('<!-- Teaching annotations -->')
        self.svg_content.append(
            '<g transform="translate(700, 300)">'
        )
        self.svg_content.append(
            '<rect x="0" y="0" width="280" height="140" rx="5" class="info-box" />'
        )
        self.svg_content.append(
            '<text x="10" y="20" font-weight="bold" font-size="12">What This Teaches:</text>'
        )
        
        annotations = [
            "1. Clear progression (top→bottom)",
            "2. Loops back are NECESSARY",
            "3. Entry markers trigger loops",
            "4. Full reset at T-1.9 possible",
            "5. Complete Prerequisite gate",
            "(Linear journey never happens)",
        ]
        
        y = 40
        for annotation in annotations:
            self.svg_content.append(
                f'<text x="10" y="{y}" font-size="11" class="annotation">{annotation}</text>'
            )
            y += 17
        
        self.svg_content.append('</g>')
    
    def generate(self):
        """Generate complete SVG"""
        svg = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" '
            f'xmlns="http://www.w3.org/2000/svg">'
        ]
        
        # Add defs with styles and markers
        svg.append(self.build_markers())
        svg.append(self.build_styles())
        
        # Build content
        self.build_header()
        self.build_states()
        self.build_primary_paths()
        self.build_loop_backs()
        self.build_prerequisite_gate()
        self.build_legend()
        self.build_annotations()
        
        # Combine
        svg.extend(self.svg_content)
        svg.append('</svg>')
        
        return '\n'.join(svg)
    
    def save(self, filepath):
        """Save SVG to file"""
        svg = self.generate()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"✓ SVG saved: {filepath}")
        return filepath


if __name__ == '__main__':
    import sys
    from pathlib import Path
    
    # Output path
    output_dir = Path(__file__).parent / 'examples'
    output_dir.mkdir(exist_ok=True)
    
    # Generate
    print("Generating Tier -1 State Progression illustration...")
    illustrator = TierMinusOneIllustrator()
    filepath = illustrator.save(output_dir / 'tier_minus1_complete.svg')
    
    print(f"✓ Illustration ready")
    print(f"  Visual encoding:")
    print(f"    - Position (vertical): Progression through tier")
    print(f"    - Size: Complexity/depth (slightly increasing)")
    print(f"    - Color: Decision points (red) vs work states (green)")
    print(f"    - Line style: Primary (solid) vs loops (dashed)")
    print(f"    - Opacity: Accumulating depth")
    print(f"  Core teaching: Self-examination requires loops, not linear")
