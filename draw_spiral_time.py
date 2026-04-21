"""
Spiral Drawing Over Time - UFM Definition
===========================================

UFM Key Insight:
"A spiral is NOT a static geometry, but the TEMPORAL PROCESS of gradient resolution.
The spiral UNFOLDS through moments in time."

Each moment in time shows:
- The current position in the spiral (phase)
- How energy cycles through space (inward or outward)
- The progression from one state to the next

This is the TIME DIMENSION of spirals.
"""

import numpy as np
from PIL import Image, ImageDraw
import math

# ═══════════════════════════════════════════════════════════════════════════
# TIME-BASED SPIRAL PRIMITIVES
# ═══════════════════════════════════════════════════════════════════════════

def logarithmic_spiral_at_time(t, r_max=5.0, pitch_angle=12.0, num_turns=3.0):
    """
    Get spiral at a specific moment in time.
    
    At time t:
    - The spiral advances by some phase rotation
    - Energy position moves along the spiral path
    - Direction (inward/outward) determines causality
    """
    k = math.tan(math.radians(pitch_angle))
    a = r_max / math.exp(k * 2 * math.pi * num_turns)
    
    # Full spiral from 0 to num_turns revolutions
    theta = np.linspace(0, 2 * math.pi * num_turns, 500)
    r = a * np.exp(k * theta)
    
    # At time t, the "active" part of the spiral is at phase position t*num_turns
    # Earlier phases are "past", later phases are "future"
    phase_position = t * num_turns * 2 * math.pi  # Where we are NOW
    
    return theta, r, k, a, phase_position


def draw_spiral_timeline(width=1024, height=256, 
                         spiral_type='outward',
                         num_frames=16):
    """
    Draw timeline showing spiral evolution across moments.
    
    Each frame shows:
    - Left side: The spiral geometry (static reference)
    - Center: Energy position at THIS moment
    - Right side: "Trail" of previous energy positions
    """
    frames = []
    
    for frame_num in range(num_frames):
        img = Image.new('RGB', (width, height), color=(20, 20, 25))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Time parameter: 0 to 1 (one complete cycle)
        t = frame_num / num_frames
        
        # Get spiral geometry with fixed pitch
        theta_array, r_array, k, a, phase_at_t = logarithmic_spiral_at_time(
            t=t, r_max=3.0, pitch_angle=12.0, num_turns=2.0
        )
        
        # Normalize to screen coordinates
        x_spiral = r_array * np.cos(theta_array)
        y_spiral = r_array * np.sin(theta_array)
        
        # Scale and center
        scale = width / 12
        cx = width / 2
        cy = height / 2
        
        # ━━━ Draw the spiral path (reference) ━━━
        for i in range(len(theta_array) - 1):
            x1 = cx + x_spiral[i] * scale
            y1 = cy + y_spiral[i] * scale
            x2 = cx + x_spiral[i+1] * scale
            y2 = cy + y_spiral[i+1] * scale
            
            # Darker, dimmer reference spiral
            draw.line([(x1, y1), (x2, y2)], fill=(80, 80, 90), width=1)
        
        # ━━━ Determine current energy position on spiral ━━━
        # Find which segment we're currently on
        current_phase_idx = int((t * 2.0) * len(theta_array)) % len(theta_array)
        
        # Current position
        x_curr = cx + x_spiral[current_phase_idx] * scale
        y_curr = cy + y_spiral[current_phase_idx] * scale
        
        # ━━━ Draw trail of past positions ━━━
        trail_length = min(frame_num + 1, 8)  # Show up to 8 previous positions
        for i in range(trail_length):
            past_t = (frame_num - i) / num_frames
            past_phase_idx = int((past_t * 2.0) * len(theta_array)) % len(theta_array)
            
            x_past = cx + x_spiral[past_phase_idx] * scale
            y_past = cy + y_spiral[past_phase_idx] * scale
            
            # Fade from current (bright) to past (dim)
            fade = 1.0 - (i / trail_length)
            
            if spiral_type == 'outward':
                color = (int(100 * fade), int(200 * fade), int(255 * fade), int(150 * fade))
            else:
                color = (int(255 * fade), int(100 * fade), int(100 * fade), int(150 * fade))
            
            draw.ellipse(
                [(x_past - 3, y_past - 3), (x_past + 3, y_past + 3)],
                fill=color
            )
        
        # ━━━ Draw current energy position (bright, prominent) ━━━
        if spiral_type == 'outward':
            color_current = (100, 200, 255)  # Blue
        else:
            color_current = (255, 100, 100)  # Red
        
        draw.ellipse(
            [(x_curr - 5, y_curr - 5), (x_curr + 5, y_curr + 5)],
            fill=color_current,
            outline=(255, 255, 255)
        )
        
        # ━━━ Labels ━━━
        time_percent = int(t * 100)
        direction = "OUTWARD ⊙" if spiral_type == 'outward' else "INWARD ⊗"
        draw.text((10, 10), f"t={time_percent}%  {direction}", fill=(150, 200, 255))
        
        # Phase indicator
        phase_turns = (t * 2.0) % 2.0
        draw.text((10, 30), f"Phase: {phase_turns:.2f} turns", fill=(150, 200, 255))
        
        frames.append(img)
    
    return frames


def create_animated_gif(frames, filename, duration=100):
    """Save frames as animated GIF"""
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )


def draw_spiral_3d_time_surface(width=512, height=512,
                                spiral_type='outward',
                                show_time_axis=True):
    """
    Draw spiral as a 3D surface projection showing TIME as the third axis.
    
    The spiral unfolds through time:
    - X axis: Position around the spiral
    - Y axis: Distance from center (radial)
    - Color: Time progression (dark = past, bright = present)
    """
    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Time steps
    num_time_steps = 20
    
    # For each time moment
    for t_idx in range(num_time_steps):
        t = t_idx / num_time_steps
        
        # Get spiral at this time with fixed pitch
        theta_array, r_array, k, a, phase_at_t = logarithmic_spiral_at_time(
            t=t, r_max=4.0, pitch_angle=12.0, num_turns=3.0
        )
        
        x_spiral = r_array * np.cos(theta_array)
        y_spiral = r_array * np.sin(theta_array)
        
        scale = width / 12
        cx = width / 2
        cy = height / 2
        
        # Draw the spiral at this time point
        for i in range(len(theta_array) - 1):
            x1 = cx + x_spiral[i] * scale
            y1 = cy + y_spiral[i] * scale
            x2 = cx + x_spiral[i+1] * scale
            y2 = cy + y_spiral[i+1] * scale
            
            # Color intensity based on time (past=dim, present=bright)
            brightness = t_idx / num_time_steps
            
            if spiral_type == 'outward':
                r_val = int(100 * brightness)
                g_val = int(200 * brightness)
                b_val = int(255 * brightness)
            else:
                r_val = int(255 * brightness)
                g_val = int(100 * brightness)
                b_val = int(100 * brightness)
            
            # Earlier time = thinner, dimmer lines
            line_width = 1 + int(2 * brightness)
            
            draw.line([(x1, y1), (x2, y2)], 
                     fill=(r_val, g_val, b_val), 
                     width=line_width)
    
    # Add time axis label
    if show_time_axis:
        draw.text((10, 10), "TIME →", fill=(150, 150, 150))
        draw.text((10, height - 25), "(Past = Dim) → (Present = Bright)", 
                 fill=(100, 150, 200))
    
    return img


def draw_spiral_state_diagram(width=600, height=400,
                              spiral_type='outward'):
    """
    Show how a spiral represents the STATE EVOLUTION of the system.
    
    Each point on the spiral = a moment in time
    The spiral PATH = the trajectory of the system's state
    The DIRECTION = causality (inward or outward)
    """
    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title area
    title = f"Spiral as State Evolution ({spiral_type.upper()})"
    draw.text((width//2 - 150, 20), title, fill=(100, 200, 255))
    
    # Draw spiral with fixed pitch
    theta_array, r_array, k, a, _ = logarithmic_spiral_at_time(
        t=0.5, r_max=3.0, pitch_angle=12.0, num_turns=2.5
    )
    
    x_spiral = r_array * np.cos(theta_array)
    y_spiral = r_array * np.sin(theta_array)
    
    scale = width / 10
    cx = width / 2
    cy = height / 2 + 20
    
    # ━━━ Draw spiral with numbered time points ━━━
    num_time_marks = 8
    
    for i in range(len(theta_array) - 1):
        x1 = cx + x_spiral[i] * scale
        y1 = cy + y_spiral[i] * scale
        x2 = cx + x_spiral[i+1] * scale
        y2 = cy + y_spiral[i+1] * scale
        
        phase_fraction = i / len(theta_array)
        
        if spiral_type == 'outward':
            color = (100 + int(100 * phase_fraction), 
                    200 - int(100 * phase_fraction), 
                    255 - int(100 * phase_fraction))
        else:
            color = (255 - int(100 * phase_fraction),
                    100 + int(100 * phase_fraction),
                    100 + int(100 * phase_fraction))
        
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    
    # Mark time points
    for mark_num in range(num_time_marks):
        mark_idx = int((mark_num / num_time_marks) * len(theta_array))
        if mark_idx < len(theta_array):
            x_mark = cx + x_spiral[mark_idx] * scale
            y_mark = cy + y_spiral[mark_idx] * scale
            
            draw.ellipse(
                [(x_mark - 4, y_mark - 4), (x_mark + 4, y_mark + 4)],
                fill=(255, 255, 255),
                outline=(100, 100, 100)
            )
            
            draw.text((x_mark + 8, y_mark - 5), 
                     f"t{mark_num}", 
                     fill=(150, 150, 200))
    
    # Add annotations
    if spiral_type == 'outward':
        draw.text((20, height - 120), 
                 "⊙ Outward Spiral:", 
                 fill=(100, 200, 255))
        draw.text((20, height - 100), 
                 "→ Energy radiates away", 
                 fill=(150, 200, 255))
        draw.text((20, height - 80), 
                 "→ State expands over time", 
                 fill=(150, 200, 255))
        draw.text((20, height - 60), 
                 "→ Repulsive force manifestation", 
                 fill=(150, 200, 255))
    else:
        draw.text((20, height - 120), 
                 "⊗ Inward Spiral:", 
                 fill=(255, 100, 100))
        draw.text((20, height - 100), 
                 "→ Energy accumulates toward center", 
                 fill=(255, 150, 150))
        draw.text((20, height - 80), 
                 "→ State contracts over time", 
                 fill=(255, 150, 150))
        draw.text((20, height - 60), 
                 "→ Attractive force manifestation", 
                 fill=(255, 150, 150))
    
    return img


# ═══════════════════════════════════════════════════════════════════════════
# MAIN: Draw spirals THROUGH TIME
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  SPIRAL DRAWING THROUGH TIME - UFM DEFINITION             ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # 1. Timeline visualization (outward)
    print("1️⃣  Creating timeline: OUTWARD spiral evolution")
    frames_out = draw_spiral_timeline(spiral_type='outward', num_frames=16)
    create_animated_gif(frames_out, 'spiral_timeline_outward.gif', duration=150)
    print("   ✓ Saved: spiral_timeline_outward.gif (animated)\n")
    
    # 2. Timeline visualization (inward)
    print("2️⃣  Creating timeline: INWARD spiral evolution")
    frames_in = draw_spiral_timeline(spiral_type='inward', num_frames=16)
    create_animated_gif(frames_in, 'spiral_timeline_inward.gif', duration=150)
    print("   ✓ Saved: spiral_timeline_inward.gif (animated)\n")
    
    # 3. 3D time surface
    print("3️⃣  Creating 3D time surface: OUTWARD spiral through time")
    img_3d_out = draw_spiral_3d_time_surface(spiral_type='outward')
    img_3d_out.save('spiral_3d_time_outward.png')
    print("   ✓ Saved: spiral_3d_time_outward.png\n")
    
    print("4️⃣  Creating 3D time surface: INWARD spiral through time")
    img_3d_in = draw_spiral_3d_time_surface(spiral_type='inward')
    img_3d_in.save('spiral_3d_time_inward.png')
    print("   ✓ Saved: spiral_3d_time_inward.png\n")
    
    # 4. State evolution diagrams
    print("5️⃣  Creating state diagram: OUTWARD spiral as state evolution")
    img_state_out = draw_spiral_state_diagram(spiral_type='outward')
    img_state_out.save('spiral_state_outward.png')
    print("   ✓ Saved: spiral_state_outward.png\n")
    
    print("6️⃣  Creating state diagram: INWARD spiral as state evolution")
    img_state_in = draw_spiral_state_diagram(spiral_type='inward')
    img_state_in.save('spiral_state_inward.png')
    print("   ✓ Saved: spiral_state_inward.png\n")
    
    print("✨ All spiral-through-time visualizations complete:\n")
    print("   Timeline GIFs show:")
    print("   - How spiral advances through moments")
    print("   - Trail of previous positions (memory)")
    print("   - Current position in the spiral (now)")
    print()
    print("   3D Time Surfaces show:")
    print("   - Spiral unfolds from past (dim) → present (bright)")
    print("   - TIME AXIS = progression through moments")
    print("   - Density = how long system stays in state region")
    print()
    print("   State Diagrams show:")
    print("   - Each point on spiral = system state at that moment")
    print("   - Spiral path = state trajectory over time")
    print("   - Direction = causality (inward attracts, outward repels)")
