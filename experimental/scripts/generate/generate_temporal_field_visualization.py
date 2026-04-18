"""
Temporal field evolution visualization.
Shows complete trajectory: before → during → now
What persisted, merged, faded at each stage.
"""

import numpy as np
from PIL import Image, ImageDraw
import math

# Create timeline visualization: 4 stages of field evolution
width, height = 2000, 1200
img = Image.new('RGB', (width, height), color='#1a1a2e')
draw = ImageDraw.Draw(img, 'RGBA')

# 4 time periods
time_stages = [
    {'name': 'BEFORE', 'x_start': 0, 'coherence': 0.95, 'entropy': 0.05},
    {'name': 'PERTURBATION', 'x_start': 500, 'coherence': 0.75, 'entropy': 0.25},
    {'name': 'DEGRADATION', 'x_start': 1000, 'coherence': 0.40, 'entropy': 0.60},
    {'name': 'NOW', 'x_start': 1500, 'coherence': 0.10, 'entropy': 0.90},
]

# Field node parameters
node_radius = 8
node_spacing = 40
grid_width = 8  # nodes wide
grid_height = 6  # nodes tall

def get_node_state(stage_idx, grid_x, grid_y, total_nodes):
    """
    Determine node state based on:
    - Time stage (how far corruption has spread)
    - Position (distance from corruption center)
    - Some noise (randomness within bounds)
    """
    stage = time_stages[stage_idx]
    
    # Corruption center
    center_x = grid_width / 2
    center_y = grid_height / 2
    
    # Distance from center
    dist = math.sqrt((grid_x - center_x)**2 + (grid_y - center_y)**2)
    max_dist = math.sqrt(center_x**2 + center_y**2)
    
    # Corruption spreads outward over time
    corruption_radius = stage_idx * 1.5  # Spreads more each stage
    
    if dist < corruption_radius:
        # In corruption zone
        corruption_amount = 1.0 - (dist / corruption_radius)
    else:
        # Outside corruption zone
        corruption_amount = 0
    
    return {
        'corruption': corruption_amount,
        'coherence': 1.0 - corruption_amount,
        'stage': stage_idx,
        'grid_pos': (grid_x, grid_y),
    }

def get_node_color(node_state):
    """Color based on node state"""
    corruption = node_state['corruption']
    
    if corruption < 0.2:
        # Healthy: bright green
        r = int(50 + (1-corruption) * 200)
        g = int(200 + (1-corruption) * 55)
        b = int(50)
        status = 'coherent'
    elif corruption < 0.5:
        # Degrading: yellow to orange
        r = int(255)
        g = int(200 - corruption * 100)
        b = int(50)
        status = 'degrading'
    elif corruption < 0.8:
        # Corrupted: orange to red
        r = int(255)
        g = int(100 - corruption * 50)
        b = int(50)
        status = 'corrupted'
    else:
        # Dead: dark red/black
        r = int(80)
        g = int(20)
        b = int(20)
        status = 'dead'
    
    return {
        'rgb': (r, g, b),
        'status': status,
        'corruption': corruption
    }

def draw_field_node(draw, x, y, node_state, radius=8):
    """Draw a single field node"""
    color_info = get_node_color(node_state)
    rgb = color_info['rgb']
    
    # Draw node circle
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                fill=rgb, outline=(200, 200, 200), width=1)
    
    # Draw radiating lines showing field direction
    corruption = node_state['corruption']
    if corruption < 0.5:
        # Healthy: radiate outward (organized)
        for angle in np.linspace(0, 2*np.pi, 6, endpoint=False):
            line_len = radius * 1.5
            end_x = x + line_len * math.cos(angle)
            end_y = y + line_len * math.sin(angle)
            draw.line([(x, y), (end_x, end_y)], fill=(rgb[0], rgb[1], rgb[2], 100), width=1)
    elif corruption < 0.8:
        # Degrading: chaotic directions
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            # Add randomness to angle
            angle_jitter = angle + (corruption - 0.5) * 0.5
            line_len = radius * (1 - corruption * 0.3)
            end_x = x + line_len * math.cos(angle_jitter)
            end_y = y + line_len * math.sin(angle_jitter)
            draw.line([(x, y), (end_x, end_y)], fill=(rgb[0], rgb[1], rgb[2], 50), width=1)
    else:
        # Dead: inward (entropy/collapse)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            line_len = radius * 0.5
            end_x = x - line_len * math.cos(angle)
            end_y = y - line_len * math.sin(angle)
            draw.line([(x, y), (end_x, end_y)], fill=(100, 20, 20, 80), width=1)
    
    return color_info['status']

def draw_connection(draw, x1, y1, x2, y2, state1, state2):
    """Draw field line connecting two nodes"""
    # Strength based on coherence of both nodes
    coherence1 = 1.0 - state1['corruption']
    coherence2 = 1.0 - state2['corruption']
    connection_strength = coherence1 * coherence2
    
    if connection_strength > 0.3:
        # Draw field line
        color_intensity = int(connection_strength * 200)
        draw.line([(x1, y1), (x2, y2)], 
                 fill=(color_intensity, color_intensity + 50, color_intensity, 
                       int(connection_strength * 150)), width=2)

# ========== DRAW EACH TIME STAGE ==========
for stage_idx, stage in enumerate(time_stages):
    stage_x = stage['x_start']
    stage_y = 200
    
    # Stage title
    draw.text((stage_x + 150, 50), stage['name'], 
             fill=(255, 255, 255, 200), font=None)
    
    # Coherence/Entropy stats
    coherence_pct = int(stage['coherence'] * 100)
    entropy_pct = int(stage['entropy'] * 100)
    draw.text((stage_x + 100, 100), 
             f"Coherence: {coherence_pct}%\nEntropy: {entropy_pct}%", 
             fill=(100, 200, 100, 150), font=None)
    
    # Draw grid of nodes
    node_positions = {}  # Store for connection drawing
    node_statuses = {'coherent': 0, 'degrading': 0, 'corrupted': 0, 'dead': 0}
    
    for grid_y in range(grid_height):
        for grid_x in range(grid_width):
            # Calculate pixel position
            pixel_x = stage_x + 50 + grid_x * node_spacing
            pixel_y = stage_y + 50 + grid_y * node_spacing
            
            # Get node state
            node_state = get_node_state(stage_idx, grid_x, grid_y, grid_width * grid_height)
            node_positions[(grid_x, grid_y)] = (pixel_x, pixel_y, node_state)
            
            # Draw node
            status = draw_field_node(draw, pixel_x, pixel_y, node_state, radius=node_radius)
            node_statuses[status] += 1
    
    # Draw connections BEFORE nodes to appear behind
    for (gx1, gy1), (px1, py1, state1) in node_positions.items():
        # Connect to right neighbor
        if gx1 < grid_width - 1:
            (gx2, gy2) = (gx1 + 1, gy1)
            if (gx2, gy2) in node_positions:
                (px2, py2, state2) = node_positions[(gx2, gy2)]
                draw_connection(draw, px1, py1, px2, py2, state1, state2)
        
        # Connect to bottom neighbor
        if gy1 < grid_height - 1:
            (gx2, gy2) = (gx1, gy1 + 1)
            if (gx2, gy2) in node_positions:
                (px2, py2, state2) = node_positions[(gx2, gy2)]
                draw_connection(draw, px1, py1, px2, py2, state1, state2)

# ========== BOTTOM: TRAJECTORY SUMMARY ==========
summary_y = 900

# Draw fields legend
draw.text((50, summary_y), "FIELDS PERSISTING/MERGING/FADING:", 
         fill=(255, 255, 255, 200), font=None)

trajectory_items = [
    {'name': 'Fundamental Structure', 'color': (50, 250, 50), 'status': 'Persists'},
    {'name': 'Organization Patterns', 'color': (200, 200, 50), 'status': 'Merging'},
    {'name': 'Energy Coherence', 'color': (250, 100, 50), 'status': 'Fading'},
    {'name': 'Noise/Entropy', 'color': (80, 20, 20), 'status': 'Rising'},
]

for idx, item in enumerate(trajectory_items):
    y_pos = summary_y + 50 + idx * 40
    
    # Color box
    draw.rectangle([50, y_pos, 80, y_pos+30], fill=item['color'])
    
    # Label
    draw.text((100, y_pos), f"{item['name']}: {item['status']}", 
             fill=(200, 200, 200, 200), font=None)

# ========== BOTTOM RIGHT: WHAT CHANGED AT EACH TRANSITION ==========
changes_y = summary_y

transitions = [
    "BEFORE→PERTURBATION: Coherence breaks. Singularity introduces asymmetry.",
    "PERTURBATION→DEGRADATION: Corruption spreads. Fields begin to decouple.",
    "DEGRADATION→NOW: Critical mass reached. Most fields faded or merged into single dead state.",
]

for idx, change in enumerate(transitions):
    y_pos = changes_y + 50 + idx * 60
    draw.text((800, y_pos), change, fill=(255, 150, 100, 180), font=None)

# ========== OUTCOME AT EACH POINT ==========
outcomes_y = summary_y + 150

outcomes = [
    {'time': 'BEFORE', 'outcome': 'All nodes coherent. All fields aligned.'},
    {'time': 'PERTURBATION', 'outcome': '75% coherent. Fields begin to diverge.'},
    {'time': 'DEGRADATION', 'outcome': '40% coherent. Multiple states present.'},
    {'time': 'NOW', 'outcome': '10% coherent. System collapsed into entropy.'},
]

draw.text((50, outcomes_y), "OUTCOME AT EACH POINT IN TIME:", 
         fill=(150, 200, 255, 200), font=None)

for idx, outcome in enumerate(outcomes):
    y_pos = outcomes_y + 50 + idx * 35
    draw.text((100, y_pos), f"{outcome['time']}: {outcome['outcome']}", 
             fill=(180, 180, 180, 180), font=None)

# ========== SAVE ==========
img.save('c:\\Determined\\src\\applications\\ANTIPATTERN_TEMPORAL_FIELD_EVOLUTION.png')
print("✓ Temporal field evolution visualization created")
print("  ANTIPATTERN_TEMPORAL_FIELD_EVOLUTION.png")
print("\nShows:")
print("  • 4 time stages: BEFORE → PERTURBATION → DEGRADATION → NOW")
print("  • Green nodes: coherent/healthy")
print("  • Yellow nodes: degrading")
print("  • Red nodes: corrupted")
print("  • Black nodes: dead")
print("  • Radiating lines show field direction")
print("  • Connected lines show field coherence between nodes")
print("  • Complete trajectory of how reality arrived at current state")
