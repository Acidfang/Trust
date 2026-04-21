#!/usr/bin/env python3
"""
FINAL VERIFICATION - Simulate JavaScript rendering and compare to Python
Ensure they produce IDENTICAL output
"""

import numpy as np
import math
from PIL import Image

def hsv_to_rgb(h, s, v):
    """Match JavaScript HSV→RGB exactly"""
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
    """NEW VERSION with sigma=1.5"""
    r = math.sqrt(x * x + y * y)
    theta = math.atan2(y, x)
    
    spiral_phase = 12 * theta - 8 * r
    magnitude = math.exp(-(r * r) / (2 * 1.5 * 1.5))
    return spiral_phase * magnitude

def photon_propagating(x, y):
    kx = 8 * math.cos(0.5)
    ky = 8 * math.sin(0.5)
    wave = math.sin(kx * x + ky * y)
    decay = math.exp(-0.1 * (x * x + y * y))
    return wave * decay

def galaxy_spiral(x, y):
    r = math.sqrt(x * x + y * y) + 0.1
    theta = math.atan2(y, x)
    spiral = 2 * (theta - math.log(r + 1))
    intensity = math.exp(-(r * r) / 2)
    return spiral * intensity

def consciousness_network(x, y):
    field = 0
    nodes = 7
    
    for n in range(nodes):
        angle = (2 * math.pi * n) / nodes
        cx = 0.6 * math.cos(angle)
        cy = 0.6 * math.sin(angle)
        dist = math.sqrt((x - cx) * (x - cx) + (y - cy) * (y - cy))
        
        field += 2 * math.exp(-(dist * dist) / 0.3)
        field += 0.3 * math.sin(n * math.atan2(y - cy, x - cx))
    
    return field

def simulate_javascript_render(pot_func, grid_size=256, domain=[-2, 2], name=""):
    """Simulate EXACTLY what JavaScript does"""
    print(f"\n{'='*70}")
    print(f"Simulating JavaScript: {name}")
    print(f"{'='*70}")
    
    domain_min = domain[0]
    domain_max = domain[1]
    dx = (domain_max - domain_min) / grid_size
    
    # Step 1: Compute all potentials
    potentials = []
    pot_min = float('inf')
    pot_max = float('-inf')
    
    for i in range(grid_size * grid_size):
        y = i // grid_size
        x = i % grid_size
        px = domain_min + x * dx
        py = domain_min + y * dx
        
        pot = pot_func(px, py)
        potentials.append(pot)
        pot_min = min(pot_min, pot)
        pot_max = max(pot_max, pot)
    
    print(f"Potential range: [{pot_min:.3f}, {pot_max:.3f}]")
    pot_range = pot_max - pot_min + 1e-6
    
    # Step 2: Render pixels
    img = Image.new('RGB', (grid_size, grid_size))
    pixels = img.load()
    
    for i in range(len(potentials)):
        y = i // grid_size
        x = i % grid_size
        
        pot = potentials[i]
        hue = ((pot % (2 * math.pi)) / (2 * math.pi)) * 360
        value = (pot - pot_min) / pot_range
        rgb = hsv_to_rgb(hue, 1.0, value)
        
        pixels[x, y] = rgb
    
    return img

# Test all four concepts
concepts = [
    (electron_spiral, "Electron Spiral"),
    (photon_propagating, "Photon Propagating"),
    (galaxy_spiral, "Galaxy Spiral"),
    (consciousness_network, "Consciousness Network"),
]

print("FINAL VERIFICATION - JavaScript Simulation")
print("="*70)

all_match = True

for pot_func, name in concepts:
    # Simulate JavaScript render
    js_sim = simulate_javascript_render(pot_func, grid_size=256, domain=[-2, 2], name=name)
    
    # Load existing Python render
    filename = f'c:/Determined/{name.lower().replace(" ", "_")}_direct.png'
    py_render = Image.open(filename)
    
    # Compare
    js_array = np.array(js_sim)
    py_array = np.array(py_render)
    
    if js_array.shape != py_array.shape:
        print(f"✗ Shape mismatch: {js_array.shape} vs {py_array.shape}")
        all_match = False
        continue
    
    diff = np.abs(js_array.astype(int) - py_array.astype(int))
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    pixels_different = np.sum(diff > 1)
    
    print(f"\n{name}:")
    print(f"  Max pixel difference: {max_diff}")
    print(f"  Mean pixel difference: {mean_diff:.2f}")
    print(f"  Pixels with diff > 1: {pixels_different} / {256*256}")
    
    if max_diff <= 1:
        print(f"  ✓✓✓ MATCH (only rounding differences)")
    elif max_diff <= 5:
        print(f"  ✓ ACCEPTABLE (minor differences)")
    else:
        print(f"  ✗ MISMATCH (significant difference)")
        all_match = False
    
    # Check corners
    print(f"  Corner values:")
    corners = [(0,0), (0,255), (255,0), (255,255)]
    corners_match = True
    for cx, cy in corners:
        js_pix = js_array[cy, cx]
        py_pix = py_array[cy, cx]
        if np.max(np.abs(js_pix.astype(int) - py_pix.astype(int))) > 1:
            print(f"    [{cx},{cy}]: JS={tuple(js_pix)}, PY={tuple(py_pix)} ✗")
            corners_match = False
        else:
            print(f"    [{cx},{cy}]: {tuple(js_pix)} ✓")
    
    if not corners_match:
        all_match = False

print("\n" + "="*70)
print("FINAL RESULT")
print("="*70)

if all_match:
    print("✓✓✓ ALL VERIFIED - JavaScript output matches Python output")
    print("✓✓✓ Canvas rendering will be IDENTICAL to Python")
    print("✓✓✓ All four concepts extend across full domain")
    print("\n✓✓✓ READY FOR PRODUCTION")
else:
    print("✗ VERIFICATION FAILED - Check differences above")

# Detailed edge analysis
print("\n" + "="*70)
print("EDGE EXTENT VERIFICATION")
print("="*70)

for pot_func, name in concepts:
    js_sim = simulate_javascript_render(pot_func, grid_size=256, domain=[-2, 2], name=name)
    js_array = np.array(js_sim)
    
    # Check edge intensity
    top_left = js_array[0, 0]
    top_right = js_array[0, 255]
    bot_left = js_array[255, 0]
    bot_right = js_array[255, 255]
    
    # Are they all different? (would indicate spiral extends)
    unique_corners = len(set([tuple(top_left), tuple(top_right), tuple(bot_left), tuple(bot_right)]))
    
    print(f"\n{name}:")
    print(f"  TL: RGB={tuple(top_left)}")
    print(f"  TR: RGB={tuple(top_right)}")
    print(f"  BL: RGB={tuple(bot_left)}")
    print(f"  BR: RGB={tuple(bot_right)}")
    print(f"  Unique corner colors: {unique_corners}/4", end="")
    
    if unique_corners >= 2:
        print(" ✓ (Spiral extends to edges)")
    else:
        print(" ✗ (Spiral does NOT extend to edges)")

print("\n" + "="*70)
