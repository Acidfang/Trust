"""
COMPUTE_CYCLE_GIF_GENERATOR.py
===============================

Generates animated GIF showing infinite circular loop of compute nodes.

Based on COMPUTE_DOMAIN_FRAMEWORK:
  • Nodes arranged in perfect circle
  • Data flowing continuously around circle
  • Bandwidth shown as energy traveling the loop
  • Cycle detection as dynamic animation
  • Repeats forever (infinite loop)

Key: Shows that cycles aren't problems - they're PATTERNS.
     Data flowing = system alive and working
     The cycle IS the structure
"""

import sys
sys.path.insert(0, r'c:\Determined')

from typing import List, Tuple
from PIL import Image, ImageDraw
import math
import os

OUTPUT_DIR = r"c:\Determined\spiral_renders"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_compute_circle_frame(
    frame_num: int,
    total_frames: int,
    num_nodes: int = 8,
    canvas_width: int = 1000,
    canvas_height: int = 1000,
) -> Image.Image:
    """
    Render a single frame of compute nodes in a perfect circle with flowing data.
    
    Frame animation shows:
    • Data pulses traveling around the circle
    • Load balancing across nodes
    • Bandwidth visualized as color intensity
    • Cycle counter incrementing
    """
    
    img = Image.new('RGB', (canvas_width, canvas_height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Center and radius for circle
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    radius = 300
    
    # Animation progress
    progress = frame_num / total_frames
    flow_position = (progress * 360) % 360  # 0-360 degrees, loops
    
    # Calculate node positions in perfect circle
    node_positions = []
    for i in range(num_nodes):
        angle = (360 / num_nodes) * i - 90  # Start at top
        angle_rad = math.radians(angle)
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        node_positions.append((x, y, angle))
    
    # Draw title
    draw.text(
        (canvas_width // 2 - 150, 30),
        f"Compute Cycle - Infinite Loop",
        fill='#333333'
    )
    draw.text(
        (canvas_width // 2 - 120, 55),
        f"Frame {frame_num + 1}/{total_frames} | Data Flow: {int(flow_position)}°",
        fill='#666666'
    )
    
    # Draw circle path (light gray)
    circle_points = []
    for i in range(360):
        angle_rad = math.radians(i)
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        circle_points.append((x, y))
    
    for i in range(len(circle_points) - 1):
        x1, y1 = circle_points[i]
        x2, y2 = circle_points[i + 1]
        draw.line([(x1, y1), (x2, y2)], fill='#E0E0E0', width=2)
    
    # Draw data flow lines (flowing around circle)
    num_flows = 3
    for flow in range(num_flows):
        flow_offset = (flow_position + (120 * flow)) % 360
        
        # Draw traveling pulse
        angle_rad = math.radians(flow_offset)
        pulse_x = center_x + radius * math.cos(angle_rad)
        pulse_y = center_y + radius * math.sin(angle_rad)
        
        # Pulse glow (larger circle)
        glow_size = 25
        glow_color = (255, 100 + int(50 * math.sin(progress * 6.28)), 0)  # Orange
        draw.ellipse(
            [(pulse_x - glow_size, pulse_y - glow_size),
             (pulse_x + glow_size, pulse_y + glow_size)],
            fill=glow_color,
            outline='#FF6600',
            width=2
        )
        
        # Trailing line
        trail_angle = math.radians((flow_offset - 30) % 360)
        trail_x = center_x + radius * math.cos(trail_angle)
        trail_y = center_y + radius * math.sin(trail_angle)
        draw.line(
            [(pulse_x, pulse_y), (trail_x, trail_y)],
            fill='#FFAA33',
            width=3
        )
    
    # Draw nodes
    for i, (x, y, angle) in enumerate(node_positions):
        # Load visualization - varies with node index for variety
        load = 50 + 30 * math.sin(progress * 6.28 + i)
        load_color_intensity = int(100 + load * 2)
        node_color = (load_color_intensity, 150, 255 - load_color_intensity // 2)
        
        # Node circle
        node_radius = 20
        draw.ellipse(
            [(x - node_radius, y - node_radius),
             (x + node_radius, y + node_radius)],
            fill=node_color,
            outline='#333333',
            width=2
        )
        
        # Node label
        node_label = f"N{i}"
        draw.text(
            (x - 12, y - 8),
            node_label,
            fill='#FFFFFF'
        )
        
        # Connection to next node
        next_idx = (i + 1) % num_nodes
        next_x, next_y, _ = node_positions[next_idx]
        
        # Connection to next node - with animated data flow
        # Calculate if data pulse is traveling on this link
        
        # Distance along the circle from current node (in degrees)
        current_angle = angle
        next_angle = node_positions[next_idx][2]
        
        # Normalize angle difference
        angle_diff = (next_angle - current_angle) % 360
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        # Check if flow is on this link
        flow_on_link = False
        for flow in range(3):
            flow_offset = (flow_position + (120 * flow)) % 360
            # Is this flow between current and next node?
            if min(current_angle, next_angle) <= flow_offset <= max(current_angle, next_angle) or \
               (current_angle > next_angle and (flow_offset >= current_angle or flow_offset <= next_angle)):
                flow_on_link = True
                break
        
        # Draw link with dynamic color based on data flow
        link_color = '#FF8833' if flow_on_link else '#CCCCCC'
        link_width = 3 if flow_on_link else 2
        
        draw.line(
            [(x, y), (next_x, next_y)],
            fill=link_color,
            width=link_width
        )
    
    # Draw load metrics at bottom
    draw.text((20, canvas_height - 120), "Node Status:", fill='#333333')
    
    for i in range(num_nodes):
        load = 50 + 30 * math.sin(progress * 6.28 + i)
        load_bar_x = 20 + (i % 4) * 230
        load_bar_y = canvas_height - 100 + (i // 4) * 25
        
        # Status label
        status = "ACTIVE" if load > 50 else "IDLE"
        draw.text(
            (load_bar_x, load_bar_y),
            f"N{i}: {status} ({int(load)}%)",
            fill='#333333'
        )
        
        # Load bar
        bar_width = int(100 * (load / 100))
        draw.rectangle(
            [(load_bar_x, load_bar_y + 12), (load_bar_x + 100, load_bar_y + 18)],
            fill='#EEEEEE',
            outline='#999999'
        )
        draw.rectangle(
            [(load_bar_x, load_bar_y + 12), (load_bar_x + bar_width, load_bar_y + 18)],
            fill='#FF6600'
        )
    
    # Cycle counter (how many complete loops)
    complete_cycles = int(progress * 4)  # 4 complete loops over animation
    draw.text(
        (canvas_width - 200, canvas_height - 40),
        f"Complete Cycles: {complete_cycles}",
        fill='#666666'
    )
    draw.text(
        (canvas_width - 200, canvas_height - 20),
        f"Infinite Loop Status: RUNNING",
        fill='#00AA00',
    )
    
    return img


def generate_compute_cycle_gif(
    num_frames: int = 120,
    num_nodes: int = 8,
    output_filename: str = "compute_cycle_infinite_loop"
):
    """Generate animated GIF of infinite compute cycle."""
    
    print(f"Generating {num_frames} frames of compute cycle animation...")
    print(f"  Nodes: {num_nodes}")
    print(f"  Each frame shows data flowing around the complete circle")
    print()
    
    frames = []
    frame_times = []
    
    for frame_num in range(num_frames):
        print(f"  Rendering frame {frame_num + 1}/{num_frames}...", end='\r')
        
        img = create_compute_circle_frame(
            frame_num,
            num_frames,
            num_nodes=num_nodes,
            canvas_width=1000,
            canvas_height=900
        )
        
        frames.append(img)
        frame_times.append(50)  # 50ms per frame = smooth animation
    
    print()
    
    # Save as animated GIF
    output_path = os.path.join(OUTPUT_DIR, f"{output_filename}.gif")
    
    print(f"Saving animated GIF to: {output_path}")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_times,
        loop=0,  # Loop forever
        optimize=False
    )
    
    file_size = os.path.getsize(output_path) / (1024*1024)
    print(f"✓ Complete! Saved: {output_path}")
    print(f"  Total frames: {len(frames)}")
    print(f"  File size: {file_size:.2f} MB")
    print(f"  Duration: {len(frames) * 50 / 1000:.1f} seconds per loop")
    print(f"  Loops: INFINITE")
    
    return output_path


def generate_static_frame():
    """Generate single static frame showing the pattern."""
    print(f"Generating static cycle visualization...")
    
    # Render middle frame (half way through)
    img = create_compute_circle_frame(60, 120, num_nodes=8, canvas_width=1200, canvas_height=1000)
    
    output_path = os.path.join(OUTPUT_DIR, "compute_cycle_snapshot.png")
    img.save(output_path)
    
    print(f"✓ Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    print("=" * 60)
    print("COMPUTE CYCLE INFINITE LOOP GIF GENERATOR")
    print("=" * 60)
    print()
    
    # Generate animated GIF with flowing data
    gif_path = generate_compute_cycle_gif(num_frames=120, num_nodes=8)
    print()
    
    # Generate static snapshot
    png_path = generate_static_frame()
    
    print()
    print("=" * 60)
    print("INTERPRETATION:")
    print("  • Circle = cycle in the compute network")
    print("  • Flowing pulses = data moving continuously")
    print("  • Infinite loop = pattern perpetually active")
    print("  • Node load = dynamic system responding to flow")
    print("=" * 60)
