"""
SPIRAL_GIF_GENERATOR.py
=======================

Generates animated GIF of the complete hierarchy spiral.

Uses HierarchicalPosition data from all 10 primitives to:
1. Calculate spiral coordinates (x, y, z)
2. Project to 2D canvas
3. Render frames with rotating spiral
4. Animate through hierarchy levels
5. Convert frames to GIF

Output: spiral_hierarchy_animation.gif (animated spiral showing all 10 primitives)
"""

import sys
sys.path.insert(0, r'c:\Determined')

from typing import List, Tuple, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import math
import os
import time

try:
    from UNIVERSAL_ENTITY_CONNECTION_FRAMEWORK import PrimitiveRegistry, HierarchicalPosition
except ImportError as e:
    print(f"Error importing framework: {e}")
    sys.exit(1)

OUTPUT_DIR = r"c:\Determined\spiral_renders"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color scheme for hierarchy levels
LEVEL_COLORS = {
    0: "#E8E8E8",  # Level 0: Raw fields (light gray)
    1: "#FF6B6B",  # Level 1: Orientation primitives (red)
    2: "#4ECDC4",  # Level 2: Entities & connections (teal)
    3: "#45B7D1",  # Level 3: World states (blue)
    4: "#FFA07A",  # Level 4: Domain frameworks (light salmon)
    5: "#98D8C8",  # Level 5: Renderer & registry (mint)
    6: "#F7DC6F",  # Level 6: Meta-level (gold)
}

PRIMITIVE_INFO = {
    "OrientationPrimitives": "Anchors",
    "ImprovedEntity": "Entities",
    "ImprovedConnection": "Connections",
    "ImprovedWorldState": "World State",
    "DomainFrameworkContainer": "Frameworks",
    "PrimitiveRegistry": "Registry",
    "LedgerContainer": "Ledger",
    "RendererContainer": "Renderer",
    "HierarchicalPosition": "Position",
    "ImprovedPrimitiveContainer": "Improved Container",
}


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def project_spiral_to_2d(
    x: float, y: float, z: float,
    canvas_width: int, canvas_height: int,
    rotation_angle: float = 0.0,
    scale: float = 1.0
) -> Tuple[int, int]:
    """
    Project 3D spiral point to 2D canvas.
    
    • X, Y define spiral rotation in XY plane
    • Z defines vertical (time) axis
    • Rotation angle rotates the entire view
    • Scale adjusts zoom level
    """
    # Apply rotation to x, y
    rot_rad = math.radians(rotation_angle)
    x_rot = x * math.cos(rot_rad) - y * math.sin(rot_rad)
    y_rot = x * math.sin(rot_rad) + y * math.cos(rot_rad)
    
    # Apply scale
    x_rot *= scale
    y_rot *= scale
    
    # Project to 2D (perspective projection)
    # Z pushes point further away/closer to camera
    perspective = 1.0 + (z / 2000.0)  # Slight perspective effect
    x_2d = (x_rot / perspective)
    y_2d = (y_rot / perspective)
    
    # Center on canvas and invert Y for normal coordinates
    canvas_x = int(canvas_width / 2 + x_2d)
    canvas_y = int(canvas_height / 2 - y_2d - z / 5)  # Z also affects vertical position
    
    return canvas_x, canvas_y


def render_spiral_frame(
    frame_num: int,
    total_frames: int,
    canvas_width: int = 1200,
    canvas_height: int = 1400,
) -> Image.Image:
    """Render a single frame of the spiral animation."""
    
    # Create base image
    img = Image.new('RGB', (canvas_width, canvas_height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Calculate animation parameters
    progress = frame_num / total_frames
    rotation_angle = progress * 360 * 2  # Double rotation
    scale = 1.0 + (progress * 0.3)  # Zoom out over time
    reveal_level = int(progress * 7)  # Progressively reveal levels
    
    # Get all primitives from registry
    registry = PrimitiveRegistry()
    all_primitives = registry.all_primitives()
    
    # Draw header
    draw.text(
        (canvas_width // 2 - 200, 30),
        f"Universal Hierarchy Spiral - Frame {frame_num + 1}/{total_frames}",
        fill='#333333'
    )
    draw.text(
        (canvas_width // 2 - 150, 55),
        f"Rotation: {int(rotation_angle % 360)}° | Level: {reveal_level}",
        fill='#666666'
    )
    
    # Collect points for drawing lines between levels
    level_points = {level: [] for level in range(7)}
    
    # Draw spiral path (faint background spiral)
    spiral_points = []
    for i in range(0, 360 * 4, 5):  # 4 rotations
        angle_rad = math.radians(i)
        radius_factor = i / (360 * 4)
        radius = 80 + (radius_factor * 300)
        height = radius_factor * 1200
        
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)
        z = height
        
        canvas_x, canvas_y = project_spiral_to_2d(
            x, y, z, canvas_width, canvas_height, rotation_angle, scale
        )
        spiral_points.append((canvas_x, canvas_y))
    
    # Draw spiral path (light background)
    for i in range(len(spiral_points) - 1):
        x1, y1 = spiral_points[i]
        x2, y2 = spiral_points[i + 1]
        draw.line([(x1, y1), (x2, y2)], fill='#EEEEEE', width=2)
    
    # Draw all 10 primitives
    primitive_list = list(all_primitives.items())
    
    for prim_name, prim_container in primitive_list:
        if not prim_container.hierarchical_position:
            continue
        
        hp = prim_container.hierarchical_position
        level = hp.hierarchy_level
        
        # Only draw if revealed
        if level > reveal_level:
            continue
        
        # Get spiral position
        x, y, z = hp.get_spiral_position()
        
        # Project to 2D
        canvas_x, canvas_y = project_spiral_to_2d(
            x, y, z, canvas_width, canvas_height, rotation_angle, scale
        )
        
        # Get color for this level
        color = LEVEL_COLORS.get(level, "#999999")
        rgb = hex_to_rgb(color)
        
        # Draw circle for primitive
        radius = 12 + (level * 2)
        draw.ellipse(
            [(canvas_x - radius, canvas_y - radius),
             (canvas_x + radius, canvas_y + radius)],
            fill=rgb,
            outline='#333333',
            width=2
        )
        
        # Add primitive label
        label = PRIMITIVE_INFO.get(prim_name, prim_name)[:12]
        label_x = canvas_x - 30  # Approximate text width
        label_y = canvas_y + radius + 5
        
        draw.text(
            (label_x, label_y),
            label,
            fill='#333333'
        )
        
        # Store for drawing connection lines
        level_points[level].append((canvas_x, canvas_y))
    
    # Draw level groupings (boxes around level clusters)
    for level in range(reveal_level + 1):
        points = level_points.get(level, [])
        if len(points) > 1:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            
            min_x, max_x = min(xs) - 25, max(xs) + 25
            min_y, max_y = min(ys) - 25, max(ys) + 25
            
            color = LEVEL_COLORS.get(level, "#999999")
            
            # Draw level boundary (light)
            draw.rectangle(
                [(min_x, min_y), (max_x, max_y)],
                outline=color,
                width=1
            )
    
    # Draw legend at bottom
    legend_y = canvas_height - 100
    legend_x = 20
    
    draw.text((legend_x, legend_y), "Hierarchy Levels:", fill='#333333')
    for level, color in LEVEL_COLORS.items():
        rgb = hex_to_rgb(color)
        level_label = [
            "Level 0: Raw Fields",
            "Level 1: Anchors",
            "Level 2: Entities/Connections",
            "Level 3: World States",
            "Level 4: Frameworks",
            "Level 5: Renderer/Registry",
            "Level 6: Meta-Level",
        ][level]
        
        y_pos = legend_y + 20 + (level * 12)
        
        # Color box
        draw.rectangle(
            [(legend_x, y_pos - 3), (legend_x + 12, y_pos + 9)],
            fill=rgb,
            outline='#333333'
        )
        
        # Label
        draw.text((legend_x + 18, y_pos - 5), level_label, fill='#333333')
    
    return img


def generate_spiral_gif(num_frames: int = 60, output_filename: str = "spiral_hierarchy_animation"):
    """Generate complete animated GIF of the spiral."""
    
    print(f"Generating {num_frames} frames of spiral animation...")
    
    frames = []
    frame_times = []
    
    for frame_num in range(num_frames):
        print(f"  Rendering frame {frame_num + 1}/{num_frames}...", end='\r')
        
        img = render_spiral_frame(
            frame_num,
            num_frames,
            canvas_width=1200,
            canvas_height=1400
        )
        
        frames.append(img)
        frame_times.append(100)  # 100ms per frame
    
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
    
    print(f"✓ Complete! Saved: {output_path}")
    print(f"  Total frames: {len(frames)}")
    print(f"  File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
    
    return output_path


def generate_spiral_static_png(output_filename: str = "spiral_hierarchy_complete"):
    """Generate a single high-quality PNG of the complete spiral."""
    
    print(f"Generating static spiral visualization...")
    
    # Render final frame (fully revealed)
    # Hack: render frame that's near the end
    img = render_spiral_frame(59, 60, canvas_width=1600, canvas_height=1800)
    
    output_path = os.path.join(OUTPUT_DIR, f"{output_filename}.png")
    
    print(f"Saving static PNG to: {output_path}")
    img.save(output_path)
    
    print(f"✓ Complete! Saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    print("=" * 60)
    print("SPIRAL HIERARCHY GIF GENERATOR")
    print("=" * 60)
    print()
    
    # Generate both animated GIF and static PNG
    gif_path = generate_spiral_gif(num_frames=60)
    print()
    png_path = generate_spiral_static_png()
    
    print()
    print("=" * 60)
    print("Generation complete!")
    print(f"Animated GIF: {gif_path}")
    print(f"Static PNG: {png_path}")
    print("=" * 60)
