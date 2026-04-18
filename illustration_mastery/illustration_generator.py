#!/usr/bin/env python3
"""
Meaningful Illustration Generator
Translates concepts into visual forms that embed meaning
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

class MeaningfulIllustrationBuilder:
    """
    Generates SVG illustrations where visual form encodes conceptual meaning.
    Every visual variable (color, size, position, line style) maps to a concept.
    """
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.elements = []
        self.styles = {}
        
    def set_color_scheme(self, scheme: str = 'default'):
        """Define color scheme where color encodes meaning"""
        schemes = {
            'default': {
                'unresolved': '#8B0000',    # Dark red - high tension
                'resolved': '#006400',       # Dark green - stable
                'tension': '#DC143C',        # Crimson - conflict
                'stable': '#228B22',         # Forest green - integrity
                'deferred': '#FF8C00',       # Dark orange - delayed cost
            },
            'coherence': {
                'high_potential': '#4A0000',   # Very dark - maximum tension
                'medium_potential': '#800080', # Purple - moderate tension
                'low_potential': '#008000',    # Green - resolved/stable
                'neutral': '#808080',          # Gray - unknown state
            }
        }
        self.styles = schemes.get(scheme, schemes['default'])
        return self
    
    def add_state_node(self, x: int, y: int, state_id: str, 
                       severity: int = 1, is_resolved: bool = False,
                       label: str = ''):
        """
        Add a state node where visual properties encode meaning
        
        severity: 1-5 (maps to node size and opacity)
        is_resolved: True = lighter color, False = darker color
        """
        size = 20 + (severity * 10)  # Size encodes severity
        color = self.styles['resolved'] if is_resolved else self.styles['unresolved']
        opacity = 0.5 + (severity * 0.1) if not is_resolved else 0.9
        
        self.elements.append({
            'type': 'circle',
            'cx': x,
            'cy': y,
            'r': size,
            'fill': color,
            'opacity': opacity,
            'class': f'state-{state_id}',
            'data-state': state_id
        })
        
        if label:
            self.elements.append({
                'type': 'text',
                'x': x,
                'y': y,
                'text': label,
                'text-anchor': 'middle',
                'dy': '0.3em',
                'transform': f'translate({x},{y})'
            })
        
        return self
    
    def add_choice_path(self, from_x: int, from_y: int, 
                       to_x: int, to_y: int,
                       choice_type: str = 'B',
                       consequence: str = 'resolution'):
        """
        Add a path between states where line style/width/color encodes consequence
        
        choice_type: 'A' (continue), 'B' (engage), 'C' (avoid)
        consequence: 'resolution', 'tension_increase', 'deferred', 'loop_back'
        """
        
        # Line style encodes choice type
        line_styles = {
            'A': {'stroke': self.styles['tension'], 'stroke-width': 2, 'stroke-dasharray': '2,2'},
            'B': {'stroke': self.styles['stable'], 'stroke-width': 3},
            'C': {'stroke': self.styles['deferred'], 'stroke-width': 2, 'stroke-dasharray': '5,5'},
        }
        
        style = line_styles.get(choice_type, line_styles['B'])
        
        # Use curved path (arc) to show non-linear progression
        if consequence == 'loop_back':
            # Create arc path back
            path_d = f"M {from_x},{from_y} Q {(from_x+to_x)/2},{max(from_y,to_y)-100} {to_x},{to_y}"
        else:
            # Straight path
            path_d = f"M {from_x},{from_y} L {to_x},{to_y}"
        
        self.elements.append({
            'type': 'path',
            'd': path_d,
            'fill': 'none',
            'stroke': style['stroke'],
            'stroke-width': style.get('stroke-width', 2),
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round',
            'data-choice': choice_type,
            'data-consequence': consequence,
            **{k: v for k, v in style.items() if k not in ['stroke', 'stroke-width']}
        })
        
        # Add arrow marker to show direction
        self.elements.append({
            'type': 'polygon',
            'points': f'{to_x},{to_y} {to_x-10},{to_y-5} {to_x-10},{to_y+5}',
            'fill': style['stroke'],
        })
        
        return self
    
    def add_entry_marker_weight(self, x: int, y: int, marker_name: str,
                               is_resolved: bool = False,
                               weight: float = 1.0):
        """
        Add entry marker visualization where size/darkness shows weight/consequence
        
        weight: 0-1 (0 = fully resolved/light, 1 = unresolved/heavy)
        """
        # Darker and larger when unresolved and heavy
        intensity = weight if not is_resolved else (1 - weight)
        darkness = int(0 + (intensity * 150))  # 0-150 scale for color
        size = 5 + (weight * 15)
        
        color = f'rgb({150 + darkness}, {50}, {50})' if not is_resolved else f'rgb({50}, {150}, {50})'
        
        self.elements.append({
            'type': 'rect',
            'x': x - size/2,
            'y': y - size/2,
            'width': size,
            'height': size,
            'fill': color,
            'opacity': 0.6 + (weight * 0.4),
            'data-marker': marker_name,
            'data-weight': weight,
            'class': f'marker-{marker_name}'
        })
        
        return self
    
    def add_tier_layer(self, x_start: int, y_start: int, 
                      tier_num: int, tier_name: str,
                      depth: int = 3):
        """
        Add a tier as a visual layer where depth shows hierarchy
        
        depth: how deeply nested/complex the tier is (1-5)
        """
        layer_height = 80 + (depth * 20)
        
        self.elements.append({
            'type': 'rect',
            'x': x_start,
            'y': y_start,
            'width': self.width - 40,
            'height': layer_height,
            'fill': 'none',
            'stroke': '#cccccc',
            'stroke-width': 2,
            'stroke-dasharray': '5,5',
            'opacity': 0.3,
            'data-tier': tier_num
        })
        
        self.elements.append({
            'type': 'text',
            'x': x_start + 10,
            'y': y_start + 20,
            'text': f'Tier {tier_num}: {tier_name}',
            'font-size': '14',
            'font-weight': 'bold',
            'fill': '#333',
            'data-tier-label': tier_num
        })
        
        return self
    
    def add_coherence_field(self, x: int, y: int, width: int = 200, height: int = 150):
        """
        Add a coherence field visualization as a gradient
        Darker areas = higher potential energy (unresolved)
        Lighter areas = lower potential energy (resolved)
        """
        
        # Create gradient definition
        grad_id = 'coherence-gradient'
        self.elements.append({
            'type': 'defs',
            'content': f'''
            <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:rgb(139,0,0);stop-opacity:0.8" />
              <stop offset="50%" style="stop-color:rgb(255,165,0);stop-opacity:0.6" />
              <stop offset="100%" style="stop-color:rgb(0,100,0);stop-opacity:0.8" />
            </linearGradient>
            '''
        })
        
        # Add rectangle with gradient
        self.elements.append({
            'type': 'rect',
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'fill': f'url(#{grad_id})',
            'stroke': '#333',
            'stroke-width': 2,
            'class': 'coherence-field'
        })
        
        # Add label
        self.elements.append({
            'type': 'text',
            'x': x + width/2,
            'y': y - 10,
            'text': 'Coherence Field (Potential Energy)',
            'text-anchor': 'middle',
            'font-size': '12',
            'fill': '#333'
        })
        
        # Add temperature indicators
        self.elements.append({
            'type': 'text',
            'x': x - 20,
            'y': y + 20,
            'text': 'High\nTension',
            'font-size': '10',
            'text-anchor': 'end',
            'fill': '#8B0000'
        })
        
        self.elements.append({
            'type': 'text',
            'x': x + width + 20,
            'y': y + height - 20,
            'text': 'Resolved\nStable',
            'font-size': '10',
            'text-anchor': 'start',
            'fill': '#006400'
        })
        
        return self
    
    def build_svg(self) -> str:
        """Generate complete SVG from accumulated elements"""
        svg_parts = [
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            self._build_style_section(),
            '</defs>',
        ]
        
        # Add elements
        for elem in self.elements:
            if elem['type'] == 'defs':
                svg_parts.append(elem['content'])
            elif elem['type'] == 'circle':
                attrs = ' '.join([f'{k}="{v}"' for k, v in elem.items() if k != 'type'])
                svg_parts.append(f'<circle {attrs} />')
            elif elem['type'] == 'rect':
                attrs = ' '.join([f'{k}="{v}"' for k, v in elem.items() if k != 'type'])
                svg_parts.append(f'<rect {attrs} />')
            elif elem['type'] == 'path':
                attrs = ' '.join([f'{k}="{v}"' for k, v in elem.items() if k != 'type'])
                svg_parts.append(f'<path {attrs} />')
            elif elem['type'] == 'polygon':
                attrs = ' '.join([f'{k}="{v}"' for k, v in elem.items() if k != 'type'])
                svg_parts.append(f'<polygon {attrs} />')
            elif elem['type'] == 'text':
                text_content = elem.pop('text')
                attrs = ' '.join([f'{k}="{v}"' for k, v in elem.items() if k != 'type'])
                svg_parts.append(f'<text {attrs}>{text_content}</text>')
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def _build_style_section(self) -> str:
        """Build CSS style section encoding design choices"""
        styles = '''
        <style>
            /* State styling - color encodes resolution status */
            circle[data-state] { 
                cursor: pointer;
                transition: all 0.3s ease;
            }
            circle[data-state]:hover {
                filter: brightness(1.2);
            }
            
            /* Path styling - line type encodes choice consequence */
            path[data-choice="A"] { /* Continue unexamined */
                stroke: #DC143C;
                marker-end: url(#markerA);
            }
            path[data-choice="B"] { /* Engage honestly */
                stroke: #228B22;
                marker-end: url(#markerB);
            }
            path[data-choice="C"] { /* Avoid */
                stroke: #FF8C00;
                marker-end: url(#markerC);
                stroke-dasharray: 5,5;
            }
            
            /* Entry marker styling - size/color encodes weight */
            rect[data-marker]:hover { opacity: 1 !important; }
            
            /* Coherence field - gradient shows potential energy */
            .coherence-field {
                filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
            }
            
            text { font-family: 'Segoe UI', sans-serif; }
        </style>
        
        <marker id="markerA" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#DC143C" />
        </marker>
        <marker id="markerB" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#228B22" />
        </marker>
        <marker id="markerC" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#FF8C00" />
        </marker>
        '''
        return styles
    
    def save_svg(self, filepath: str):
        """Save illustration as SVG file"""
        svg_content = self.build_svg()
        Path(filepath).write_text(svg_content)
        print(f'✓ SVG saved: {filepath}')
        return filepath


# Example: Build a decision state diagram
def create_decision_state_illustration():
    """Create an illustration showing how A/B/C choices lead to different consequences"""
    
    builder = MeaningfulIllustrationBuilder(1000, 800)
    builder.set_color_scheme('default')
    
    # Title
    builder.elements.append({
        'type': 'text',
        'x': 500,
        'y': 30,
        'text': 'Decision Consequence Paths: How Choices Lead to Different Outcomes',
        'text-anchor': 'middle',
        'font-size': '18',
        'font-weight': 'bold',
        'fill': '#333'
    })
    
    # Starting state (awareness/unresolved)
    builder.add_state_node(100, 200, 'T-1.1', severity=2, is_resolved=False, label='T-1.1')
    
    # Path A: Continue unexamined (increases tension)
    builder.add_choice_path(100, 200, 250, 350, choice_type='A', consequence='tension_increase')
    builder.add_state_node(250, 350, 'loop-A1', severity=3, is_resolved=False, label='Tension Increases')
    builder.add_choice_path(250, 350, 150, 450, choice_type='A', consequence='loop_back')
    builder.add_state_node(150, 450, 'loop-A2', severity=4, is_resolved=False, label='Pattern Repeats')
    
    # Path B: Engage honestly (leads to resolution)
    builder.add_choice_path(100, 200, 500, 350, choice_type='B', consequence='resolution')
    builder.add_state_node(500, 350, 'T-1.2', severity=2, is_resolved=False, label='T-1.2')
    builder.add_choice_path(500, 350, 500, 500, choice_type='B', consequence='resolution')
    builder.add_state_node(500, 500, 'resolved', severity=1, is_resolved=True, label='RESOLVED')
    
    # Path C: Avoid (defers to later)
    builder.add_choice_path(100, 200, 800, 350, choice_type='C', consequence='deferred')
    builder.add_state_node(800, 350, 'tier-0', severity=2, is_resolved=False, label='Tier 0 (Deferred)')
    builder.add_choice_path(800, 350, 700, 500, choice_type='C', consequence='deferred')
    builder.add_state_node(700, 500, 'conflict', severity=4, is_resolved=False, label='Conflict (Larger)')
    
    # Add annotations
    builder.elements.append({
        'type': 'text',
        'x': 200,
        'y': 300,
        'text': 'A: Continue',
        'font-size': '12',
        'fill': '#DC143C',
        'font-weight': 'bold'
    })
    
    builder.elements.append({
        'type': 'text',
        'x': 350,
        'y': 300,
        'text': 'B: Engage',
        'font-size': '12',
        'fill': '#228B22',
        'font-weight': 'bold'
    })
    
    builder.elements.append({
        'type': 'text',
        'x': 650,
        'y': 300,
        'text': 'C: Avoid',
        'font-size': '12',
        'fill': '#FF8C00',
        'font-weight': 'bold'
    })
    
    # Add legend
    builder.elements.append({
        'type': 'text',
        'x': 50,
        'y': 700,
        'text': 'Node size & darkness = severity/tension | Line color = consequence type | Curved line = returns to earlier state | Dashed line = cost deferred',
        'font-size': '11',
        'fill': '#666',
        'font-style': 'italic'
    })
    
    return builder


if __name__ == '__main__':
    output_dir = Path('c:/Determined/illustration_mastery/examples')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create decision state illustration
    print('Generating decision state diagram...')
    builder = create_decision_state_illustration()
    svg_file = str(output_dir / 'decision_consequence_paths.svg')
    builder.save_svg(svg_file)
    
    print(f'\n✓ Illustration system ready')
    print(f'Output: {output_dir}')
