"""
Draw Spiral the Way UFM Defines It
===================================

UFM Definition:
"A spiral is the spatial configuration that gradient resolution takes when confined—
not linear propagation, but spatial cycling."

Key Properties:
- Logarithmic spiral: r = a·e^(k·θ)
- Self-similar (constant pitch angle)
- Spiral direction determines force type:
  * Outward spiral (⊙→⊗): Expansion-containment (electron-like)
  * Inward spiral (⊗→⊙): Contraction-release (positron-like)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from PIL import Image, ImageDraw
import math

# ═══════════════════════════════════════════════════════════════════════════
# SPIRAL DRAWING PRIMITIVES
# ═══════════════════════════════════════════════════════════════════════════

def logarithmic_spiral(r_max=5.0, pitch_angle=12.0, num_turns=3.0):
    """
    Generate logarithmic spiral points: r = a·e^(k·θ)
    
    Args:
        r_max: Maximum radius
        pitch_angle: Angle of spiral arms (degrees), ~12° for galaxies
        num_turns: How many spiral rotations to draw
    
    Returns:
        (theta, r) arrays defining the spiral in polar coordinates
    """
    # Pitch angle → k coefficient
    # tan(pitch) = k, so k = tan(pitch_radians)
    k = math.tan(math.radians(pitch_angle))
    
    # Coefficient a such that r_max = a·e^(k·2π·num_turns)
    a = r_max / math.exp(k * 2 * math.pi * num_turns)
    
    # Theta from 0 to 2π·num_turns
    theta = np.linspace(0, 2 * math.pi * num_turns, 500)
    r = a * np.exp(k * theta)
    
    return theta, r, k, a


def polar_to_cartesian(theta, r):
    """Convert polar coordinates to Cartesian"""
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def hsv_to_rgb_tuple(h, s, v):
    """HSV (h: 0-360, s: 0-1, v: 0-1) → RGB (0-255)"""
    h_norm = (h % 360) / 360.0
    rgb = hsv_to_rgb([h_norm, s, v])
    return tuple(int(c * 255) for c in rgb)


def draw_spiral_field(width=512, height=512, 
                      spiral_type='outward',
                      pitch_angle=12.0,
                      show_phase=True):
    """
    Draw spiral as a 2D field visualization.
    
    Args:
        spiral_type: 'outward' (electron-like) or 'inward' (positron-like)
        pitch_angle: Logarithmic spiral pitch in degrees
        show_phase: If True, color by phase (cycling direction)
    """
    # Create image
    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    pixels = img.load()
    
    # Center coordinates
    cx, cy = width / 2, height / 2
    scale = width / 10  # 10 units across the image
    
    # Generate spiral
    theta_array, r_array, k, a = logarithmic_spiral(r_max=4.0, pitch_angle=pitch_angle)
    x_spiral, y_spiral = polar_to_cartesian(theta_array, r_array)
    
    # For each pixel, determine:
    # 1. Distance to spiral curve
    # 2. Angle in spiral (phase)
    # 3. Color based on direction and phase
    
    for py in range(height):
        for px in range(width):
            # Convert pixel to world coordinates
            wx = (px - cx) / scale
            wy = (py - cy) / scale
            
            # Current angle in spiral frame
            angle = np.arctan2(wy, wx)
            dist = np.sqrt(wx**2 + wy**2)
            
            # Spiral equation: r = a·e^(k·θ)
            # What r *should* be at this angle?
            r_spiral_here = a * np.exp(k * angle)
            
            # Distance to spiral curve
            distance_to_spiral = abs(dist - r_spiral_here)
            
            # Phase: position along the spiral (angle in turns)
            phase_turns = angle / (2 * np.pi)
            
            # Color based on spiral direction
            if spiral_type == 'outward':
                # Outward: Blue→Cyan→Green (expanding)
                # Phase determines hue rotation
                hue = 240 + phase_turns * 120  # Blue to cyan to green
                saturation = 1.0 - (distance_to_spiral / 0.3)  # High saturation near spiral
                value = 1.0 - (distance_to_spiral / 0.5)  # Bright on spiral, dark away
                
            else:  # inward
                # Inward: Red→Magenta→Blue (contracting)
                hue = 0 + phase_turns * 120  # Red to magenta to blue
                saturation = 1.0 - (distance_to_spiral / 0.3)
                value = 1.0 - (distance_to_spiral / 0.5)
            
            # Clamp values
            saturation = max(0, min(1, saturation))
            value = max(0, min(1, value))
            
            # Only draw if reasonably close to spiral
            if distance_to_spiral < 1.0:
                try:
                    color = hsv_to_rgb_tuple(hue, saturation, value)
                    pixels[px, py] = color
                except:
                    pass
    
    return img


def draw_spiral_parametric(width=512, height=512,
                           spiral_type='outward',
                           pitch_angle=12.0,
                           line_width=3):
    """
    Draw spiral as a parametric curve (direct line drawing).
    Shows the spiral path clearly with directional color.
    """
    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    cx, cy = width / 2, height / 2
    scale = width / 10
    
    # Generate spiral
    theta_array, r_array, k, a = logarithmic_spiral(r_max=4.0, pitch_angle=pitch_angle)
    x_spiral, y_spiral = polar_to_cartesian(theta_array, r_array)
    
    # Draw spiral as line with color gradient
    for i in range(len(theta_array) - 1):
        x1 = cx + x_spiral[i] * scale
        y1 = cy + y_spiral[i] * scale
        x2 = cx + x_spiral[i+1] * scale
        y2 = cy + y_spiral[i+1] * scale
        
        # Phase along spiral (0-1)
        phase = i / len(theta_array)
        
        if spiral_type == 'outward':
            # Blue → Cyan → Green
            hue = 240 + phase * 120
        else:
            # Red → Magenta → Blue
            hue = 0 + phase * 120
        
        color = hsv_to_rgb_tuple(hue, 1.0, 1.0)
        
        draw.line([(x1, y1), (x2, y2)], fill=color, width=line_width)
    
    return img


def draw_dual_spiral(width=512, height=512, pitch_angle=12.0):
    """
    Draw both outward and inward spirals to show UFM duality.
    Outward = electron-like (left side)
    Inward = positron-like (right side)
    """
    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    cx, cy = width / 2, height / 2
    scale = width / 10
    
    # ━━━ Left side: OUTWARD spiral (electron-like) ━━━
    theta_array, r_array, k, a = logarithmic_spiral(r_max=3.0, pitch_angle=pitch_angle)
    x_spiral, y_spiral = polar_to_cartesian(theta_array, r_array)
    
    for i in range(len(theta_array) - 1):
        # LEFT SIDE: x ≤ cx
        x1 = cx/2 + x_spiral[i] * scale/2
        y1 = cy + y_spiral[i] * scale
        x2 = cx/2 + x_spiral[i+1] * scale/2
        y2 = cy + y_spiral[i+1] * scale
        
        phase = i / len(theta_array)
        hue = 240 + phase * 120  # Blue→Cyan→Green
        color = hsv_to_rgb_tuple(hue, 1.0, 0.9)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    
    # ━━━ Right side: INWARD spiral (positron-like) ━━━
    # Inward: reverse the spiral direction
    theta_array_inv = theta_array[::-1]
    r_array_inv = r_array[::-1]
    x_spiral_inv, y_spiral_inv = polar_to_cartesian(theta_array_inv, r_array_inv)
    
    for i in range(len(theta_array_inv) - 1):
        # RIGHT SIDE: x ≥ cx
        x1 = cx + cx/2 + x_spiral_inv[i] * scale/2
        y1 = cy + y_spiral_inv[i] * scale
        x2 = cx + cx/2 + x_spiral_inv[i+1] * scale/2
        y2 = cy + y_spiral_inv[i+1] * scale
        
        phase = i / len(theta_array_inv)
        hue = 0 + phase * 120  # Red→Magenta→Blue
        color = hsv_to_rgb_tuple(hue, 1.0, 0.9)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    
    # Labels
    draw.text((width/4, 20), "OUTWARD (Electron)", fill=(100, 200, 255))
    draw.text((3*width/4 - 80, 20), "INWARD (Positron)", fill=(255, 100, 100))
    
    return img


# ═══════════════════════════════════════════════════════════════════════════
# MAIN: Draw spirals
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  SPIRAL DRAWING - UFM DEFINITION                          ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # 1. Outward spiral (electron-like)
    print("1️⃣  Drawing OUTWARD spiral (electron-like, blue→green)")
    img_outward = draw_spiral_field(spiral_type='outward', pitch_angle=12.0)
    img_outward.save('spiral_outward_field.png')
    print("   ✓ Saved: spiral_outward_field.png\n")
    
    # 2. Inward spiral (positron-like)
    print("2️⃣  Drawing INWARD spiral (positron-like, red→blue)")
    img_inward = draw_spiral_field(spiral_type='inward', pitch_angle=12.0)
    img_inward.save('spiral_inward_field.png')
    print("   ✓ Saved: spiral_inward_field.png\n")
    
    # 3. Parametric lines (cleaner spiral visualization)
    print("3️⃣  Drawing parametric OUTWARD spiral (clean lines)")
    img_para_out = draw_spiral_parametric(spiral_type='outward', pitch_angle=12.0)
    img_para_out.save('spiral_outward_parametric.png')
    print("   ✓ Saved: spiral_outward_parametric.png\n")
    
    print("4️⃣  Drawing parametric INWARD spiral (clean lines)")
    img_para_in = draw_spiral_parametric(spiral_type='inward', pitch_angle=12.0)
    img_para_in.save('spiral_inward_parametric.png')
    print("   ✓ Saved: spiral_inward_parametric.png\n")
    
    # 4. Dual spiral showing electron-positron duality
    print("5️⃣  Drawing DUAL SPIRAL (electron ⊙ vs positron ⊗)")
    img_dual = draw_dual_spiral(pitch_angle=12.0)
    img_dual.save('spiral_dual_ufm.png')
    print("   ✓ Saved: spiral_dual_ufm.png\n")
    
    print("✨ All spirals drawn according to UFM definition:")
    print("   - Logarithmic spiral: r = a·e^(k·θ)")
    print("   - Pitch angle: 12° (Milky Way-like)")
    print("   - Direction encoding: Hue cycle shows phase/rotation")
    print("   - Outward (blue→green): electron-like expansion")
    print("   - Inward (red→blue): positron-like contraction\n")
