#!/usr/bin/env python3
"""
Generate comprehensive TCHT state matrix visualization
Shows all 31 states across 5 tiers in one view
"""

from pathlib import Path

class TCHTMatrixGenerator:
    """Create a matrix showing all tiers and states"""
    
    def __init__(self):
        self.tiers = [
            {'name': 'Tier -1: Self (Coherence)', 'color': '#FFE5E5', 'states': 10},
            {'name': 'Tier 0: Formation (Connection)', 'color': '#E5F0FF', 'states': 6},
            {'name': 'Tier 1: Competence (Conflict)', 'color': '#E5FFE5', 'states': 4},
            {'name': 'Tier 2: Contribution (Consistency)', 'color': '#FFF5E5', 'states': 7},
            {'name': 'Tier 3: Transcendence', 'color': '#F0E5FF', 'states': 7},
        ]
        
        self.all_states = [
            # Tier -1
            {'tier': -1, 'id': 'T-1.1', 'name': 'Awareness', 'type': 'decision'},
            {'tier': -1, 'id': 'T-1.2', 'name': 'Distinction', 'type': 'work'},
            {'tier': -1, 'id': 'T-1.3', 'name': 'Causality', 'type': 'work'},
            {'tier': -1, 'id': 'T-1.4', 'name': 'Regulation', 'type': 'decision'},
            {'tier': -1, 'id': 'T-1.5', 'name': 'Consistency', 'type': 'work'},
            {'tier': -1, 'id': 'T-1.6', 'name': 'Correction', 'type': 'work'},
            {'tier': -1, 'id': 'T-1.7', 'name': 'Alignment', 'type': 'work'},
            {'tier': -1, 'id': 'T-1.8', 'name': 'Persistence', 'type': 'decision'},
            {'tier': -1, 'id': 'T-1.9', 'name': 'Adaptability', 'type': 'decision'},
            {'tier': -1, 'id': 'T-1.10', 'name': 'Integrity', 'type': 'work'},
            # Tier 0
            {'tier': 0, 'id': 'T0.1', 'name': 'Existence', 'type': 'decision'},
            {'tier': 0, 'id': 'T0.2', 'name': 'Difference', 'type': 'work'},
            {'tier': 0, 'id': 'T0.3', 'name': 'Interaction', 'type': 'work'},
            {'tier': 0, 'id': 'T0.4', 'name': 'Recognition', 'type': 'decision'},
            {'tier': 0, 'id': 'T0.5', 'name': 'Selection', 'type': 'decision'},
            {'tier': 0, 'id': 'T0.6', 'name': 'Initial Alignment', 'type': 'work'},
            # Tier 1
            {'tier': 1, 'id': 'T1.1', 'name': 'Identify Real Conflict', 'type': 'decision'},
            {'tier': 1, 'id': 'T1.2', 'name': 'Trace Causality', 'type': 'work'},
            {'tier': 1, 'id': 'T1.3', 'name': 'Resolve at Source', 'type': 'work'},
            {'tier': 1, 'id': 'T1.4', 'name': 'Avoid Repetition', 'type': 'decision'},
            # Tier 2
            {'tier': 2, 'id': 'T2.1', 'name': 'Consistency of Patterns', 'type': 'work'},
            {'tier': 2, 'id': 'T2.2', 'name': 'Reinforcement', 'type': 'work'},
            {'tier': 2, 'id': 'T2.3', 'name': 'Prevention', 'type': 'decision'},
            {'tier': 2, 'id': 'T2.4', 'name': 'Early Correction', 'type': 'work'},
            # Tier 3
            {'tier': 3, 'id': 'T3.1', 'name': 'Adaptation', 'type': 'work'},
            {'tier': 3, 'id': 'T3.2', 'name': 'Resilience', 'type': 'work'},
            {'tier': 3, 'id': 'T3.3', 'name': 'Expansion', 'type': 'decision'},
            {'tier': 3, 'id': 'T3.4', 'name': 'Integration', 'type': 'work'},
            {'tier': 3, 'id': 'T3.5', 'name': 'Synchronization', 'type': 'work'},
            {'tier': 3, 'id': 'T3.6', 'name': 'Refinement', 'type': 'decision'},
            {'tier': 3, 'id': 'T3.7', 'name': 'Scaling', 'type': 'work'},
        ]
    
    def generate(self):
        width = 1400
        height = 2200
        
        svg = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '<style>',
            '  .tier-header { font-size: 16px; font-weight: bold; }',
            '  .state-cell { font-size: 12px; font-weight: bold; }',
            '  .state-name { font-size: 11px; fill: #333; }',
            '  .decision-bg { fill: #8B0000; }',
            '  .work-bg { fill: #006400; }',
            '  .tier-label { font-size: 14px; font-weight: bold; }',
            '</style>',
            '</defs>',
            
            # Title
            f'<text x="{width/2}" y="40" text-anchor="middle" font-size="28" font-weight="bold">',
            'TCHT Complete State Matrix: All 31 States Across 5 Tiers',
            '</text>',
        ]
        
        # Process each tier
        y_offset = 100
        
        for tier_idx, tier_info in enumerate(self.tiers):
            tier_label = tier_info['name']
            tier_num = tier_idx - 1  # -1, 0, 1, 2, 3
            
            # Tier header
            svg.append(
                f'<rect x="20" y="{y_offset}" width="{width-40}" height="50" '
                f'fill="{tier_info["color"]}" stroke="#333" stroke-width="2" />'
            )
            svg.append(
                f'<text x="40" y="{y_offset + 35}" class="tier-label">'
                f'{tier_label}'
                '</text>'
            )
            
            y_offset += 70
            
            # States in this tier
            tier_states = [s for s in self.all_states if s['tier'] == tier_num]
            
            # Grid layout: 2 columns
            for i, state in enumerate(tier_states):
                col = i % 2
                row = i // 2
                
                x = 40 + (col * (width - 80) // 2)
                y = y_offset + (row * 90)
                cell_width = (width - 80) // 2 - 20
                
                # State container
                bg_class = 'decision-bg' if state['type'] == 'decision' else 'work-bg'
                svg.append(
                    f'<rect x="{x}" y="{y}" width="{cell_width}" height="80" '
                    f'class="{bg_class}" opacity="0.15" stroke="#999" stroke-width="1" rx="5" />'
                )
                
                # State ID and type indicator
                state_circle_x = x + 20
                state_circle_y = y + 20
                circle_r = 8
                circle_color = '#8B0000' if state['type'] == 'decision' else '#006400'
                svg.append(
                    f'<circle cx="{state_circle_x}" cy="{state_circle_y}" r="{circle_r}" fill="{circle_color}" />'
                )
                
                # State label
                svg.append(
                    f'<text x="{state_circle_x + 20}" y="{state_circle_y + 5}" class="state-cell" fill="#000">'
                    f'{state["id"]}'
                    '</text>'
                )
                
                # State name
                svg.append(
                    f'<text x="{x + 20}" y="{y + 50}" class="state-name">'
                    f'{state["name"]}'
                    '</text>'
                )
                
                # Type label
                type_label = 'DECISION' if state['type'] == 'decision' else 'WORK'
                svg.append(
                    f'<text x="{x + 20}" y="{y + 70}" font-size="9" fill="#666">'
                    f'{type_label}'
                    '</text>'
                )
            
            # Update y_offset for next tier
            rows_in_tier = (len(tier_states) + 1) // 2
            y_offset += (rows_in_tier * 90) + 40
        
        # Legend
        legend_y = y_offset + 40
        svg.append(
            f'<text x="40" y="{legend_y}" font-size="14" font-weight="bold">Legend:</text>'
        )
        
        svg.append(
            f'<circle cx="250" cy="{legend_y - 8}" r="6" fill="#8B0000" />'
        )
        svg.append(
            f'<text x="265" y="{legend_y}" font-size="12">Decision Point (choice required)</text>'
        )
        
        svg.append(
            f'<circle cx="600" cy="{legend_y - 8}" r="6" fill="#006400" />'
        )
        svg.append(
            f'<text x="615" y="{legend_y}" font-size="12">Work State (action required)</text>'
        )
        
        svg.append('</svg>')
        return '\n'.join(svg)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate())
        print(f"✓ State matrix saved: {filepath}")


if __name__ == '__main__':
    output_dir = Path(__file__).parent / 'examples'
    output_dir.mkdir(exist_ok=True)
    
    print("Generating TCHT complete state matrix...")
    generator = TCHTMatrixGenerator()
    generator.save(output_dir / 'all_states_matrix.svg')
    print(f"\nMatrix shows all 31 states across 5 tiers")
    print(f"  10 states in Tier -1")
    print(f"  6 states in Tier 0")
    print(f"  4 states in Tier 1")
    print(f"  4 states in Tier 2")
    print(f"  7 states in Tier 3")
