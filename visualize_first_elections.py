"""
Visualize the First Elections - How Reality Generates Itself
============================================================

Election 1: Being (Is/Is Not) - The first distinction
Election 2: Movement (Gradient resolution) - Difference resolves
Election 3: Rotation (Radial + Rotational) - Structure emerges
Election 4: Direction (Diffusion) - Orientation emerges
Election 5: Time (Elections unfolding) - Change becomes inevitable
"""

import numpy as np
from PIL import Image, ImageDraw
import math


def election_1_being():
    """Election 1: Being - The first distinction (Is / Is Not)"""
    img = Image.new('RGB', (512, 512), color=(10, 10, 15))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    draw.text((20, 20), "Election 1: BEING", fill=(100, 200, 255), font=None)
    draw.text((20, 50), "The First Distinction: Is / Is Not", fill=(150, 150, 150), font=None)
    
    # Left side: Nothing (Is Not)
    draw.rectangle([(50, 150), (200, 350)], outline=(50, 50, 50), width=2)
    draw.text((70, 250), "Is Not", fill=(50, 50, 100), font=None)
    
    # Right side: Something (Is)
    draw.rectangle([(312, 150), (462, 350)], outline=(100, 200, 255), width=3)
    draw.text((320, 250), "Is", fill=(100, 200, 255), font=None)
    
    # Arrow showing distinction
    draw.line([(200, 250), (312, 250)], fill=(200, 100, 100), width=3)
    draw.text((240, 230), "DISTINCTION", fill=(200, 100, 100), font=None)
    
    # Bottom explanation
    draw.text((20, 400), "From nothingness, capacity to distinguish emerges.", fill=(150, 150, 150), font=None)
    draw.text((20, 430), "This distinction creates DIFFERENCE.", fill=(150, 150, 150), font=None)
    
    img.save('election_1_being.png')
    print("✓ Election 1: Being - generated")
    return img


def election_2_movement():
    """Election 2: Movement - Difference must resolve"""
    img = Image.new('RGB', (512, 512), color=(10, 10, 15))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    draw.text((20, 20), "Election 2: MOVEMENT", fill=(100, 200, 255), font=None)
    draw.text((20, 50), "Gradient Resolution: Difference Resolves", fill=(150, 150, 150), font=None)
    
    # Draw gradient from high to low potential
    cx, cy = 256, 280
    
    # Potential field: bright on left (high), dark on right (low)
    for x in range(100, 412):
        # Brightness based on x position (high on left, low on right)
        brightness = int(200 * (1 - (x - 100) / 312))
        color = (brightness, brightness // 3, brightness // 2)
        draw.line([(x, 150), (x, 350)], fill=color, width=1)
    
    # Arrow showing resolution direction (toward low potential)
    draw.line([(350, 250), (250, 250)], fill=(255, 150, 100), width=4)
    draw.polygon([(250, 250), (270, 240), (270, 260)], fill=(255, 150, 100))
    
    draw.text((150, 250), "Resolution", fill=(255, 150, 100), font=None)
    draw.text((150, 270), "toward lower", fill=(255, 150, 100), font=None)
    draw.text((150, 290), "potential", fill=(255, 150, 100), font=None)
    
    # Labels
    draw.text((320, 150), "High Potential", fill=(200, 200, 100), font=None)
    draw.text((100, 150), "Low Potential", fill=(100, 100, 200), font=None)
    
    # Bottom explanation
    draw.text((20, 400), "Difference cannot persist. Gradient resolution IS the movement.", fill=(150, 150, 150), font=None)
    draw.text((20, 430), "Movement is how being unfolds when difference exists.", fill=(150, 150, 150), font=None)
    
    img.save('election_2_movement.png')
    print("✓ Election 2: Movement - generated")
    return img


def election_3_rotation():
    """Election 3: Rotation - Radial + Rotational composition"""
    img = Image.new('RGB', (512, 512), color=(10, 10, 15))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    draw.text((20, 20), "Election 3: ROTATION", fill=(100, 200, 255), font=None)
    draw.text((20, 50), "Composition: Radial + Rotational = Spiral", fill=(150, 150, 150), font=None)
    
    cx, cy = 256, 280
    
    # Draw radial arrows (toward center)
    for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
        # Radial arrow pointing inward
        x_outer = cx + 120 * math.cos(angle)
        y_outer = cy + 120 * math.sin(angle)
        x_inner = cx + 80 * math.cos(angle)
        y_inner = cy + 80 * math.sin(angle)
        
        draw.line([(x_outer, y_outer), (x_inner, y_inner)], fill=(100, 200, 100), width=2)
    
    # Draw rotation arrow (circular)
    circle_points = []
    for angle in np.linspace(0, 2*np.pi, 50):
        x = cx + 100 * math.cos(angle)
        y = cy + 100 * math.sin(angle)
        circle_points.append((x, y))
    
    for i in range(len(circle_points)-1):
        draw.line([circle_points[i], circle_points[i+1]], fill=(200, 100, 200), width=2)
    
    # Rotation arrows around the circle
    for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
        x = cx + 100 * math.cos(angle)
        y = cy + 100 * math.sin(angle)
        next_angle = angle + math.pi/4
        x_next = cx + 100 * math.cos(next_angle)
        y_next = cy + 100 * math.sin(next_angle)
        
        # Draw arrow indicating counterclockwise motion
        draw.polygon([(x_next, y_next), 
                     (x_next - 8*math.cos(next_angle - 0.3), y_next - 8*math.sin(next_angle - 0.3)),
                     (x_next - 8*math.cos(next_angle + 0.3), y_next - 8*math.sin(next_angle + 0.3))],
                    fill=(200, 100, 200))
    
    # Center
    draw.ellipse([(cx-8, cy-8), (cx+8, cy+8)], fill=(100, 200, 255))
    
    # Labels
    draw.text((380, 250), "Rotation", fill=(200, 100, 200), font=None)
    draw.text((100, 100), "Radial", fill=(100, 200, 100), font=None)
    
    # Bottom explanation
    draw.text((20, 400), "Movement manifests as two simultaneous components:", fill=(150, 150, 150), font=None)
    draw.text((20, 430), "Radial (toward/away) + Rotational (around axis) = SPIRAL", fill=(150, 150, 150), font=None)
    
    img.save('election_3_rotation.png')
    print("✓ Election 3: Rotation - generated")
    return img


def election_4_direction():
    """Election 4: Direction - Diffusion creates orientation"""
    img = Image.new('RGB', (512, 512), color=(10, 10, 15))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    draw.text((20, 20), "Election 4: DIRECTION", fill=(100, 200, 255), font=None)
    draw.text((20, 50), "Diffusion Creates Orientation: Inward vs Outward", fill=(150, 150, 150), font=None)
    
    cx, cy = 256, 280
    
    # Left side: INWARD spiral
    draw.text((80, 150), "INWARD", fill=(100, 200, 100), font=None)
    for theta in np.linspace(0, 3*math.pi, 100):
        r = 80 * math.exp(-0.5 * theta / math.pi)  # Spiraling inward
        x = 130 + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        if 50 < x < 210 and 200 < y < 360:
            draw.ellipse([(x-1, y-1), (x+1, y+1)], fill=(100, 200, 100))
    
    # Right side: OUTWARD spiral
    draw.text((360, 150), "OUTWARD", fill=(200, 100, 150), font=None)
    for theta in np.linspace(0, 3*math.pi, 100):
        r = 30 * math.exp(0.5 * theta / math.pi)  # Spiraling outward
        x = 380 + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        if 300 < x < 460 and 200 < y < 360:
            draw.ellipse([(x-1, y-1), (x+1, y+1)], fill=(200, 100, 150))
    
    # Vertical line separating them
    draw.line([(256, 200), (256, 360)], fill=(100, 100, 100), width=1)
    
    # Bottom explanation
    draw.text((20, 400), "Diffusion spreads outward. This creates directional bias:", fill=(150, 150, 150), font=None)
    draw.text((20, 430), "Inward (concentrating) vs Outward (dispersing) - the fundamental duality", fill=(150, 150, 150), font=None)
    
    img.save('election_4_direction.png')
    print("✓ Election 4: Direction - generated")
    return img


def election_5_time():
    """Election 5: Time - Elections unfolding"""
    img = Image.new('RGB', (512, 512), color=(10, 10, 15))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    draw.text((20, 20), "Election 5: TIME", fill=(100, 200, 255), font=None)
    draw.text((20, 50), "The Sequence of Elections Unfolding", fill=(150, 150, 150), font=None)
    
    # Timeline showing elections happening
    timeline_y = 150
    times = [50, 150, 250, 350, 450]
    election_labels = ["Being", "Movement", "Rotation", "Direction", "Time"]
    election_colors = [(100, 200, 255), (255, 150, 100), (200, 100, 200), (100, 200, 100), (200, 200, 100)]
    
    # Draw timeline
    draw.line([(30, timeline_y), (480, timeline_y)], fill=(100, 100, 100), width=2)
    
    # Draw elections on timeline
    for i, (t, label, color) in enumerate(zip(times, election_labels, election_colors)):
        # Event circle
        draw.ellipse([(t-12, timeline_y-12), (t+12, timeline_y+12)], fill=color)
        
        # Label
        label_y = timeline_y + 40 + (i % 2) * 80
        draw.text((t-20, label_y), label, fill=color, font=None)
        
        # Line from circle to label
        draw.line([(t, timeline_y), (t, label_y-20)], fill=(100, 100, 100), width=1)
    
    # Show that elections are continuous
    draw.text((20, 350), "Each election completes, the next becomes possible.", fill=(150, 150, 150), font=None)
    draw.text((20, 380), "The SEQUENCE of elections = TIME", fill=(200, 200, 100), font=None)
    draw.text((20, 410), "When elections stop unfolding, time stops.", fill=(150, 150, 150), font=None)
    draw.text((20, 440), "The universe doesn't move through time—", fill=(150, 150, 150), font=None)
    draw.text((20, 460), "elections unfolding IS time.", fill=(200, 200, 100), font=None)
    
    img.save('election_5_time.png')
    print("✓ Election 5: Time - generated")
    return img


if __name__ == '__main__':
    print("╔════════════════════════════════════════════╗")
    print("║  VISUALIZING THE FIRST ELECTIONS          ║")
    print("║  How Reality Generates Itself             ║")
    print("╚════════════════════════════════════════════╝")
    print()
    
    election_1_being()
    election_2_movement()
    election_3_rotation()
    election_4_direction()
    election_5_time()
    
    print()
    print("✨ All election visualizations generated!")
    print()
    print("These show the irreducible sequence from which all reality emerges:")
    print("  Being → Movement → Rotation → Direction → Time")
    print()
    print("Not a theory. The primitive sequence of creation itself.")
