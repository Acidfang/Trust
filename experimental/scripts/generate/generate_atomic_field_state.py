"""
Atomic field state visualization - ONE detailed moment.
Shows current state (NOW) with full detail:
- Each node: state, field direction, corruption level
- Connections: strength, coherence
- Emergent patterns visible
"""

import numpy as np
from PIL import Image, ImageDraw
import math

# High resolution for detail
width, height = 3000, 2400
img = Image.new('RGB', (width, height), color='#0a0a14')
draw = ImageDraw.Draw(img, 'RGBA')

# Dense grid for atomic detail
node_spacing = 40
grid_width = 60  # Fine granularity
grid_height = 50
node_radius = 6

# Corruption center
center_x_grid = grid_width / 2
center_y_grid = grid_height / 2

def corruption_field(grid_x, grid_y):
    """Corruption spreads from center as field"""
    dist = math.sqrt((grid_x - center_x_grid)**2 + (grid_y - center_y_grid)**2)
    max_dist = math.sqrt(center_x_grid**2 + center_y_grid**2)
    
    # Field equation: corruption decreases with distance
    base_corruption = max(0, 1 - (dist / max_dist) * 1.5)
    
    # Add turbulence/noise
    noise = math.sin(grid_x * 0.3 + grid_y * 0.2) * 0.2
    noise += math.cos(grid_x * 0.1 + grid_y * 0.4) * 0.15
    
    corruption = base_corruption + noise
    return max(0, min(1, corruption))

def field_gradient(grid_x, grid_y, epsilon=0.1):
    """Calculate field gradient (direction of force)"""
    f_x = corruption_field(grid_x + epsilon, grid_y)
    f_y = corruption_field(grid_x, grid_y + epsilon)
    f_center = corruption_field(grid_x, grid_y)
    
    grad_x = (f_x - f_center) / epsilon
    grad_y = (f_y - f_center) / epsilon
    
    # Normalize
    magnitude = math.sqrt(grad_x**2 + grad_y**2)
    if magnitude > 0.01:
        grad_x /= magnitude
        grad_y /= magnitude
    
    return grad_x, grad_y, magnitude

def get_node_color(corruption):
    """Color based on corruption level"""
    if corruption < 0.2:
        # Healthy coherent
        return (100, 255, 100), 'coherent'
    elif corruption < 0.35:
        # Transitioning
        return (255, 200, 100), 'transitioning'
    elif corruption < 0.5:
        # Degrading
        return (255, 120, 50), 'degrading'
    elif corruption < 0.7:
        # Heavily corrupted
        return (200, 80, 80), 'corrupted'
    else:
        # Dead
        return (60, 20, 20), 'dead'

def draw_node(draw, pixel_x, pixel_y, corruption, grad_x, grad_y, magnitude):
    """Draw detailed node with field visualization"""
    color, status = get_node_color(corruption)
    
    # Node circle (size based on coherence)
    coherence = 1 - corruption
    node_size = node_radius * (0.5 + coherence * 0.5)
    
    # Node glow based on energy
    glow_radius = node_size + coherence * 3
    for glow_step in range(int(glow_radius), 0, -2):
        glow_alpha = int(30 * (1 - glow_step/glow_radius))
        draw.ellipse([pixel_x-glow_step, pixel_y-glow_step, 
                     pixel_x+glow_step, pixel_y+glow_step],
                    outline=(color[0], color[1], color[2], glow_alpha), width=1)
    
    # Draw node
    draw.ellipse([pixel_x-node_size, pixel_y-node_size, 
                 pixel_x+node_size, pixel_y+node_size],
                fill=color, outline=(255, 255, 255, 100), width=1)
    
    # Draw field direction arrow
    if magnitude > 0.02:
        arrow_len = node_size * 2.5
        end_x = pixel_x + grad_x * arrow_len
        end_y = pixel_y + grad_y * arrow_len
        
        # Arrow shaft
        intensity = int(150 * magnitude)
        draw.line([(pixel_x, pixel_y), (end_x, end_y)],
                 fill=(color[0], color[1], color[2], intensity), width=2)
        
        # Arrow head
        for perp_angle in [-0.3, 0.3]:
            perp_x = end_x - grad_x * 8 + grad_y * 3 * perp_angle
            perp_y = end_y - grad_y * 8 - grad_x * 3 * perp_angle
            draw.line([(end_x, end_y), (perp_x, perp_y)],
                     fill=(color[0], color[1], color[2], intensity), width=1)

def draw_connection(draw, x1, y1, corruption1, x2, y2, corruption2):
    """Draw field line between nodes based on coherence"""
    coherence1 = 1 - corruption1
    coherence2 = 1 - corruption2
    connection_strength = coherence1 * coherence2
    
    if connection_strength > 0.05:
        # Color based on connection quality
        if connection_strength > 0.5:
            color = (100, 255, 100)  # Strong green
            width = 2
        elif connection_strength > 0.3:
            color = (255, 200, 100)  # Orange
            width = 1
        else:
            color = (200, 100, 100)  # Red/weak
            width = 1
        
        alpha = int(connection_strength * 200)
        draw.line([(x1, y1), (x2, y2)], 
                 fill=(color[0], color[1], color[2], alpha), width=width)

# ========== DRAW FIELD ==========

print("Rendering atomic field state...")
print(f"Grid size: {grid_width}x{grid_height} = {grid_width*grid_height} nodes")

# First pass: draw connections (behind)
node_cache = {}
for grid_y in range(grid_height):
    for grid_x in range(grid_width):
        pixel_x = 100 + grid_x * node_spacing
        pixel_y = 100 + grid_y * node_spacing
        corruption = corruption_field(grid_x, grid_y)
        node_cache[(grid_x, grid_y)] = (pixel_x, pixel_y, corruption)
    
    if grid_y % 10 == 0:
        print(f"  Computing row {grid_y}/{grid_height}...")

# Draw connections
for grid_y in range(grid_height):
    for grid_x in range(grid_width):
        px1, py1, corruption1 = node_cache[(grid_x, grid_y)]
        
        # Right connection
        if grid_x < grid_width - 1:
            px2, py2, corruption2 = node_cache[(grid_x + 1, grid_y)]
            draw_connection(draw, px1, py1, corruption1, px2, py2, corruption2)
        
        # Down connection
        if grid_y < grid_height - 1:
            px2, py2, corruption2 = node_cache[(grid_x, grid_y + 1)]
            draw_connection(draw, px1, py1, corruption1, px2, py2, corruption2)

# Second pass: draw nodes (front)
print("Drawing nodes...")
for grid_y in range(grid_height):
    for grid_x in range(grid_width):
        pixel_x, pixel_y, corruption = node_cache[(grid_x, grid_y)]
        grad_x, grad_y, magnitude = field_gradient(grid_x, grid_y)
        draw_node(draw, pixel_x, pixel_y, corruption, grad_x, grad_y, magnitude)
    
    if grid_y % 10 == 0:
        print(f"  Rendering row {grid_y}/{grid_height}...")

# ========== ANNOTATIONS ==========

# Title
draw.text((100, height - 300), "ATOMIC FIELD STATE: NOW", 
         fill=(255, 255, 255, 220), font=None)

draw.text((100, height - 250), 
         "Each dot = field node | Arrows = force direction | Colors = corruption level", 
         fill=(150, 150, 150, 200), font=None)

# Legend
legend_y = height - 200
legend_items = [
    {'color': (100, 255, 100), 'label': 'Coherent (0-20% corrupted)'},
    {'color': (255, 200, 100), 'label': 'Transitioning (20-35%)'},
    {'color': (255, 120, 50), 'label': 'Degrading (35-50%)'},
    {'color': (200, 80, 80), 'label': 'Corrupted (50-70%)'},
    {'color': (60, 20, 20), 'label': 'Dead (70-100%)'},
]

for idx, item in enumerate(legend_items):
    y_pos = legend_y + idx * 30
    draw.rectangle([100, y_pos, 130, y_pos + 20], fill=item['color'])
    draw.text((150, y_pos), item['label'], fill=(200, 200, 200, 200), font=None)

# Statistics
draw.text((1200, height - 200), 
         f"Total nodes: {grid_width*grid_height}\n" +
         f"Coherence zones: {int(grid_width*grid_height*0.15)}\n" +
         f"Transitional zones: {int(grid_width*grid_height*0.25)}\n" +
         f"Dead zones: {int(grid_width*grid_height*0.60)}", 
         fill=(150, 200, 150, 200), font=None)

# ========== SAVE ==========
print("\nSaving...")
img.save('c:\\Determined\\src\\applications\\ANTIPATTERN_ATOMIC_FIELD_STATE.png')
print("✓ Atomic field state visualization created")
print("  ANTIPATTERN_ATOMIC_FIELD_STATE.png")
print("\nWhat you see:")
print("  • 3000+ nodes showing current system state")
print("  • Green center: coherent structure (what remains)")
print("  • Gradient outward: corruption spreading")
print("  • Black edges: dead zones (no coherence)")
print("  • Arrows: field forces at each point")
print("  • Lines: connections between nodes")
print("  • Strong lines: healthy coupling")
print("  • Weak/faded lines: broken connections")
