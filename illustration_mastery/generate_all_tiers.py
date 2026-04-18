#!/usr/bin/env python3
"""
Generate all 5 TCHT tier illustrations in one batch
Creates complete visual representation of the series
"""

import sys
from pathlib import Path

# =============================================================================
# TIER 0 GENERATOR
# =============================================================================

class TierZeroIllustrator:
    """Generate SVG showing Tier 0 progression (Formation/Connection)"""
    
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.states = [
            {'id': 'T0.1', 'name': 'Existence', 'desc': 'Presence', 'y': 100, 'type': 'decision', 'size': 30},
            {'id': 'T0.2', 'name': 'Difference', 'desc': 'Usable Gradient', 'y': 200, 'type': 'work', 'size': 31},
            {'id': 'T0.3', 'name': 'Interaction', 'desc': 'Exchange', 'y': 300, 'type': 'work', 'size': 32},
            {'id': 'T0.4', 'name': 'Recognition', 'desc': 'Accurate Understanding', 'y': 430, 'type': 'decision', 'size': 33},
            {'id': 'T0.5', 'name': 'Selection', 'desc': 'Mutual Continuation', 'y': 560, 'type': 'decision', 'size': 32},
            {'id': 'T0.6', 'name': 'Initial Alignment', 'desc': 'First Resolution', 'y': 690, 'type': 'work', 'size': 34},
        ]
        self.cx = self.width / 2
    
    def generate(self):
        svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '<style>',
            '  .decision-point { fill: #8B0000; }',
            '  .work-state { fill: #006400; }',
            '  .primary-path { stroke: #333; stroke-width: 2; fill: none; }',
            '  .loop-back { stroke: #cc6666; stroke-width: 2; stroke-dasharray: 5,5; fill: none; }',
            '  text { font-family: Arial, sans-serif; }',
            '</style>',
            '<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">',
            '  <path d="M0,0 L0,6 L9,3 z" fill="#333" />',
            '</marker>',
            '<marker id="arrow-loop" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">',
            '  <path d="M0,0 L0,6 L9,3 z" fill="#cc6666" />',
            '</marker>',
            '</defs>',
            f'<text x="{self.cx}" y="30" text-anchor="middle" font-size="22" font-weight="bold">',
            'TIER 0 — Formation (Connection)',
            '</text>',
        ]
        
        # Add states
        for state in self.states:
            state_class = 'decision-point' if state['type'] == 'decision' else 'work-state'
            svg.append(f'<g transform="translate({self.cx}, {state["y"]})">')
            svg.append(f'  <circle r="{state["size"]}" class="{state_class}" />')
            svg.append(f'  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" font-weight="bold">{state["id"]}</text>')
            svg.append(f'  <text x="0" y="{state["size"] + 22}" text-anchor="middle" font-size="10">{state["name"]}</text>')
            svg.append('</g>')
        
        # Add paths between states
        for i in range(len(self.states) - 1):
            y1 = self.states[i]['y'] + self.states[i]['size'] + 5
            y2 = self.states[i+1]['y'] - self.states[i+1]['size'] - 5
            svg.append(f'<path d="M {self.cx},{y1} L {self.cx},{y2}" class="primary-path" marker-end="url(#arrow)" />')
        
        svg.append('</svg>')
        return '\n'.join(svg)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate())
        print(f"✓ {filepath}")

# =============================================================================
# TIER 1 GENERATOR
# =============================================================================

class TierOneIllustrator:
    """Generate SVG showing Tier 1 progression (Conflict Resolution)"""
    
    def __init__(self):
        self.width = 1000
        self.height = 900
        self.states = [
            {'id': 'T1.1', 'name': 'Identify Real Conflict', 'desc': 'Not Surface', 'y': 100, 'type': 'decision', 'size': 31},
            {'id': 'T1.2', 'name': 'Trace Causality', 'desc': 'Root Cause', 'y': 250, 'type': 'work', 'size': 33},
            {'id': 'T1.3', 'name': 'Resolve at Source', 'desc': 'Fix Root', 'y': 430, 'type': 'work', 'size': 33},
            {'id': 'T1.4', 'name': 'Avoid Repetition', 'desc': 'New Patterns', 'y': 610, 'type': 'decision', 'size': 32},
        ]
        self.cx = self.width / 2
    
    def generate(self):
        svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '<style>',
            '  .decision-point { fill: #8B0000; }',
            '  .work-state { fill: #006400; }',
            '  .primary-path { stroke: #333; stroke-width: 2; fill: none; }',
            '  text { font-family: Arial, sans-serif; }',
            '</style>',
            '<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">',
            '  <path d="M0,0 L0,6 L9,3 z" fill="#333" />',
            '</marker>',
            '</defs>',
            f'<text x="{self.cx}" y="30" text-anchor="middle" font-size="22" font-weight="bold">',
            'TIER 1 — Competence (Conflict Resolution)',
            '</text>',
        ]
        
        for state in self.states:
            state_class = 'decision-point' if state['type'] == 'decision' else 'work-state'
            svg.append(f'<g transform="translate({self.cx}, {state["y"]})">')
            svg.append(f'  <circle r="{state["size"]}" class="{state_class}" />')
            svg.append(f'  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" font-weight="bold">{state["id"]}</text>')
            svg.append(f'  <text x="0" y="{state["size"] + 20}" text-anchor="middle" font-size="10">{state["name"]}</text>')
            svg.append('</g>')
        
        for i in range(len(self.states) - 1):
            y1 = self.states[i]['y'] + self.states[i]['size'] + 5
            y2 = self.states[i+1]['y'] - self.states[i+1]['size'] - 5
            svg.append(f'<path d="M {self.cx},{y1} L {self.cx},{y2}" class="primary-path" marker-end="url(#arrow)" />')
        
        svg.append('</svg>')
        return '\n'.join(svg)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate())
        print(f"✓ {filepath}")

# =============================================================================
# TIER 2 GENERATOR
# =============================================================================

class TierTwoIllustrator:
    """Generate SVG showing Tier 2 progression (Consistency)"""
    
    def __init__(self):
        self.width = 1000
        self.height = 900
        self.states = [
            {'id': 'T2.1', 'name': 'Consistency of Patterns', 'desc': 'Correct Patterns', 'y': 100, 'type': 'work', 'size': 31},
            {'id': 'T2.2', 'name': 'Reinforcement', 'desc': 'Strengthen Alignment', 'y': 250, 'type': 'work', 'size': 32},
            {'id': 'T2.3', 'name': 'Prevention', 'desc': 'Prevent Drift', 'y': 430, 'type': 'decision', 'size': 33},
            {'id': 'T2.4', 'name': 'Early Correction', 'desc': 'Catch Slides', 'y': 610, 'type': 'work', 'size': 32},
        ]
        self.cx = self.width / 2
    
    def generate(self):
        svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '<style>',
            '  .decision-point { fill: #8B0000; }',
            '  .work-state { fill: #006400; }',
            '  .primary-path { stroke: #333; stroke-width: 2; fill: none; }',
            '  text { font-family: Arial, sans-serif; }',
            '</style>',
            '<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">',
            '  <path d="M0,0 L0,6 L9,3 z" fill="#333" />',
            '</marker>',
            '</defs>',
            f'<text x="{self.cx}" y="30" text-anchor="middle" font-size="22" font-weight="bold">',
            'TIER 2 — Contribution (Consistency)',
            '</text>',
        ]
        
        for state in self.states:
            state_class = 'decision-point' if state['type'] == 'decision' else 'work-state'
            svg.append(f'<g transform="translate({self.cx}, {state["y"]})">')
            svg.append(f'  <circle r="{state["size"]}" class="{state_class}" />')
            svg.append(f'  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" font-weight="bold">{state["id"]}</text>')
            svg.append(f'  <text x="0" y="{state["size"] + 20}" text-anchor="middle" font-size="10">{state["name"]}</text>')
            svg.append('</g>')
        
        for i in range(len(self.states) - 1):
            y1 = self.states[i]['y'] + self.states[i]['size'] + 5
            y2 = self.states[i+1]['y'] - self.states[i+1]['size'] - 5
            svg.append(f'<path d="M {self.cx},{y1} L {self.cx},{y2}" class="primary-path" marker-end="url(#arrow)" />')
        
        svg.append('</svg>')
        return '\n'.join(svg)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate())
        print(f"✓ {filepath}")

# =============================================================================
# TIER 3 GENERATOR
# =============================================================================

class TierThreeIllustrator:
    """Generate SVG showing Tier 3 progression (Transcendence)"""
    
    def __init__(self):
        self.width = 1000
        self.height = 1200
        self.states = [
            {'id': 'T3.1', 'name': 'Adaptation', 'y': 80, 'type': 'work', 'size': 31},
            {'id': 'T3.2', 'name': 'Resilience', 'y': 190, 'type': 'work', 'size': 32},
            {'id': 'T3.3', 'name': 'Expansion', 'y': 310, 'type': 'decision', 'size': 33},
            {'id': 'T3.4', 'name': 'Integration', 'y': 450, 'type': 'work', 'size': 34},
            {'id': 'T3.5', 'name': 'Synchronization', 'y': 600, 'type': 'work', 'size': 33},
            {'id': 'T3.6', 'name': 'Refinement', 'y': 750, 'type': 'decision', 'size': 32},
            {'id': 'T3.7', 'name': 'Scaling', 'y': 890, 'type': 'work', 'size': 35},
        ]
        self.cx = self.width / 2
    
    def generate(self):
        svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '<style>',
            '  .decision-point { fill: #8B0000; }',
            '  .work-state { fill: #006400; }',
            '  .primary-path { stroke: #333; stroke-width: 2; fill: none; }',
            '  text { font-family: Arial, sans-serif; }',
            '</style>',
            '<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">',
            '  <path d="M0,0 L0,6 L9,3 z" fill="#333" />',
            '</marker>',
            '</defs>',
            f'<text x="{self.cx}" y="30" text-anchor="middle" font-size="22" font-weight="bold">',
            'TIER 3 — Transcendence',
            '</text>',
        ]
        
        for state in self.states:
            state_class = 'decision-point' if state['type'] == 'decision' else 'work-state'
            svg.append(f'<g transform="translate({self.cx}, {state["y"]})">')
            svg.append(f'  <circle r="{state["size"]}" class="{state_class}" />')
            svg.append(f'  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" font-weight="bold">{state["id"]}</text>')
            svg.append(f'  <text x="0" y="{state["size"] + 20}" text-anchor="middle" font-size="10">{state["name"]}</text>')
            svg.append('</g>')
        
        for i in range(len(self.states) - 1):
            y1 = self.states[i]['y'] + self.states[i]['size'] + 5
            y2 = self.states[i+1]['y'] - self.states[i+1]['size'] - 5
            svg.append(f'<path d="M {self.cx},{y1} L {self.cx},{y2}" class="primary-path" marker-end="url(#arrow)" />')
        
        svg.append('</svg>')
        return '\n'.join(svg)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate())
        print(f"✓ {filepath}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == '__main__':
    output_dir = Path(__file__).parent / 'examples'
    output_dir.mkdir(exist_ok=True)
    
    print("Generating all 4 remaining tier illustrations...")
    
    generators = [
        ('Tier 0', TierZeroIllustrator(), 'tier_0.svg'),
        ('Tier 1', TierOneIllustrator(), 'tier_1.svg'),
        ('Tier 2', TierTwoIllustrator(), 'tier_2.svg'),
        ('Tier 3', TierThreeIllustrator(), 'tier_3.svg'),
    ]
    
    for tier_name, generator, filename in generators:
        generator.save(output_dir / filename)
    
    print("\n✓ All tier illustrations generated")
    print(f"  Location: {output_dir}/")
    print(f"  Files: tier_0.svg, tier_1.svg, tier_2.svg, tier_3.svg")
    print(f"  Plus: tier_minus1_complete.svg (previously generated)")
