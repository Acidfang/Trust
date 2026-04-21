#!/usr/bin/env python3
"""
Compare Python rendering with JavaScript simulation
Verify they produce IDENTICAL pixel values
"""

import numpy as np
import math
from PIL import Image, ImageDraw

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB (Python version)"""
    h = h % 360
    c = v * s
    x = c * (1 - abs(((h / 60) % 2) - 1))
    m = v - c
    
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (
        int((r + m) * 255),
        int((g + m) * 255),
        int((b + m) * 255)
    )

def electron_spiral(x, y):
    r = math.sqrt(x * x + y * y)
    theta = math.atan2(y, x)
    
    # Correct formula: spiral with radial decay
    spiral_phase = 12 * theta - 8 * r
    magnitude = math.exp(-(r * r) / (2 * 0.5 * 0.5))
    return spiral_phase * magnitude

def render_javascript_logic(potentialFunc, grid_size=256, domain=[-2, 2], name=""):
    """
    Simulate EXACTLY what JavaScript does
    """
    print(f"\n{'='*70}")
    print(f"Rendering: {name}")
    print(f"{'='*70}")
    
    domain_min = domain[0]
    domain_max = domain[1]
    dx = (domain_max - domain_min) / grid_size
    
    print(f"Grid: {grid_size}x{grid_size}")
    print(f"Domain: [{domain_min}, {domain_max}]")
    print(f"dx: {dx}")
    
    # Step 1: Compute potentials (JavaScript: first loop)
    potentials = []
    pot_min = float('inf')
    pot_max = float('-inf')
    
    for i in range(grid_size * grid_size):
        y = i // grid_size
        x = i % grid_size
        px = domain_min + x * dx
        py = domain_min + y * dx
        
        pot = potentialFunc(px, py)
        potentials.append(pot)
        pot_min = min(pot_min, pot)
        pot_max = max(pot_max, pot)
    
    print(f"Potential range: [{pot_min:.3f}, {pot_max:.3f}]")
    
    pot_range = pot_max - pot_min + 1e-6
    
    # Step 2: Render to RGB (JavaScript: second loop)
    image_data = Image.new('RGB', (grid_size, grid_size))
    pixels = image_data.load()
    
    sample_indices = [0, 1, grid_size, grid_size + 1]  # Four corners of top-left pixel block
    
    for idx, i in enumerate(sample_indices):
        pot = potentials[i]
        y = i // grid_size
        x = i % grid_size
        
        hue = ((pot % (2 * math.pi)) / (2 * math.pi)) * 360
        value = (pot - pot_min) / pot_range
        rgb = hsv_to_rgb(hue, 1.0, value)
        
        print(f"\nPixel [{x},{y}] (index {i}):")
        print(f"  x,y coords: ({domain_min + x*dx:.4f}, {domain_min + y*dx:.4f})")
        print(f"  potential: {pot:.4f}")
        print(f"  hue: {hue:.1f}°, value: {value:.3f}")
        print(f"  RGB: {rgb}")
    
    # Render full image
    for i in range(len(potentials)):
        y = i // grid_size
        x = i % grid_size
        
        pot = potentials[i]
        hue = ((pot % (2 * math.pi)) / (2 * math.pi)) * 360
        value = (pot - pot_min) / pot_range
        rgb = hsv_to_rgb(hue, 1.0, value)
        
        pixels[x, y] = rgb
    
    return image_data

# Render with detailed trace
electron_img = render_javascript_logic(
    electron_spiral, 
    grid_size=256,
    domain=[-2, 2],
    name="Electron Spiral"
)

print("\n" + "="*70)
print("COMPARISON WITH EXISTING RENDERS")
print("="*70)

# Load the existing Python render
existing = Image.open('c:/Determined/electron_spiral_direct.png')
print(f"Existing image size: {existing.size}")
print(f"New simulation size: {electron_img.size}")

# Compare pixel values at key points
print("\nComparing pixel values at corners:")
for y, x in [(0, 0), (0, 255), (255, 0), (255, 255)]:
    existing_pix = existing.getpixel((x, y))
    new_pix = electron_img.getpixel((x, y))
    
    match = "✓ MATCH" if existing_pix == new_pix else "✗ MISMATCH"
    print(f"[{x},{y}]: Existing={existing_pix}, New={new_pix} {match}")

# Save comparison
electron_img.save('c:/Determined/electron_spiral_javascript_simulation.png')
print("\n✓ Saved simulation: electron_spiral_javascript_simulation.png")

# Now check full image comparison
print("\n" + "="*70)
print("PIXEL-BY-PIXEL COMPARISON")
print("="*70)

existing_array = np.array(existing)
new_array = np.array(electron_img)

diff = np.abs(existing_array.astype(int) - new_array.astype(int))
max_diff = np.max(diff)
mean_diff = np.mean(diff)

print(f"Max pixel difference: {max_diff}")
print(f"Mean pixel difference: {mean_diff}")
print(f"Pixels with diff > 1: {np.sum(diff > 1)}")

if max_diff == 0:
    print("\n✓✓✓ PERFECT MATCH - JavaScript and Python produce identical output")
elif max_diff <= 1:
    print("\n✓✓ NEAR PERFECT - Only rounding differences (±1 on RGB)")
else:
    print(f"\n✗ SIGNIFICANT DIFFERENCE - Max diff {max_diff} suggests a logic error")
    
    # Show where the biggest differences are
    diff_indices = np.argwhere(diff > 10)
    if len(diff_indices) > 0:
        print(f"\nShowing differences > 10 at these pixels:")
        for idx in diff_indices[:5]:
            y, x, c = idx
            print(f"  [{x},{y}] channel {c}: {existing_array[y,x,c]} vs {new_array[y,x,c]}")
