#!/usr/bin/env python3
"""
Verify what SHOULD appear on the canvas by tracing through the render logic
Check key points in each potential function
"""

import numpy as np
import math

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB"""
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
        round((r + m) * 255),
        round((g + m) * 255),
        round((b + m) * 255)
    )

# Test points for electron spiral
print("=" * 60)
print("ELECTRON SPIRAL - Key test points")
print("=" * 60)

test_points = [
    (0, 0, "Center"),
    (0.1, 0, "Right from center"),
    (0, 0.1, "Up from center"),
    (0.1, 0.1, "Diagonal"),
    (0.5, 0, "Far right"),
    (0, 0.5, "Far up"),
    (0.5, 0.5, "Far diagonal"),
]

for x, y, desc in test_points:
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    sigma = 0.5
    
    spiral = 12 * theta
    envelope = math.exp(-(r**2) / (2 * sigma**2))
    pot = spiral * envelope
    
    # What color should this be?
    hue = ((pot % (2 * math.pi)) / (2 * math.pi)) * 360
    
    print(f"\n{desc} ({x:+.1f}, {y:+.1f}):")
    print(f"  r={r:.3f}, θ={theta:.3f} rad")
    print(f"  spiral={spiral:.2f}, envelope={envelope:.3f}")
    print(f"  potential={pot:.3f}")
    print(f"  hue={hue:.1f}°")

print("\n" + "=" * 60)
print("PHOTON PROPAGATING - Key test points")
print("=" * 60)

for x, y, desc in test_points:
    kx = 8 * math.cos(0.5)
    ky = 8 * math.sin(0.5)
    
    wave = math.sin(kx * x + ky * y)
    decay = math.exp(-0.1 * (x**2 + y**2))
    pot = wave * decay
    
    hue = ((pot % (2 * math.pi)) / (2 * math.pi)) * 360
    
    print(f"\n{desc} ({x:+.1f}, {y:+.1f}):")
    print(f"  wave={wave:.3f}, decay={decay:.3f}")
    print(f"  potential={pot:.3f}")
    print(f"  hue={hue:.1f}°")

print("\n" + "=" * 60)
print("GALAXY SPIRAL - Key test points")
print("=" * 60)

for x, y, desc in test_points:
    r = math.sqrt(x**2 + y**2) + 0.1
    theta = math.atan2(y, x)
    
    spiral = 2 * (theta - math.log(r + 1))
    intensity = math.exp(-(r**2) / 2)
    pot = spiral * intensity
    
    hue = ((pot % (2 * math.pi)) / (2 * math.pi)) * 360
    
    print(f"\n{desc} ({x:+.1f}, {y:+.1f}):")
    print(f"  r={r:.3f}, spiral={spiral:.3f}, intensity={intensity:.3f}")
    print(f"  potential={pot:.3f}")
    print(f"  hue={hue:.1f}°")

print("\n" + "=" * 60)
print("CONSCIOUSNESS NETWORK - Key test points")
print("=" * 60)

nodes = 7
for x, y, desc in test_points:
    field = 0
    for n in range(nodes):
        angle = (2 * math.pi * n) / nodes
        cx = 0.6 * math.cos(angle)
        cy = 0.6 * math.sin(angle)
        dist = math.sqrt((x - cx)**2 + (y - cy)**2)
        
        field += 2 * math.exp(-dist**2 / 0.3)
        field += 0.3 * math.sin(n * math.atan2(y - cy, x - cx))
    
    hue = ((field % (2 * math.pi)) / (2 * math.pi)) * 360
    
    print(f"\n{desc} ({x:+.1f}, {y:+.1f}):")
    print(f"  field={field:.3f}")
    print(f"  hue={hue:.1f}°")

# Now verify the FULL grid rendering
print("\n" + "=" * 60)
print("FULL GRID VERIFICATION - Sample 8x8 grid")
print("=" * 60)

def render_grid_sample(pot_func, name, size=8, domain=[-2, 2]):
    """Render a small grid and show it"""
    dx = (domain[1] - domain[0]) / size
    print(f"\n{name} (8x8 sample):")
    
    potentials = []
    for i in range(size * size):
        y = i // size
        x = i % size
        px = domain[0] + x * dx
        py = domain[0] + y * dx
        pot = pot_func(px, py)
        potentials.append(pot)
    
    pot_min = min(potentials)
    pot_max = max(potentials)
    pot_range = pot_max - pot_min + 1e-6
    
    print(f"Potential range: [{pot_min:.3f}, {pot_max:.3f}]")
    
    # Show hue pattern
    print("\nHue pattern (degrees):")
    for i in range(size * size):
        y = i // size
        x = i % size
        if x == 0 and y > 0:
            print()
        
        pot = potentials[i]
        hue = ((pot % (2 * math.pi)) / (2 * math.pi)) * 360
        value = (pot - pot_min) / pot_range
        
        print(f"{hue:3.0f}°", end=" ")
    print()

# Test each potential
def electron_spiral(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    spiral = 12 * theta
    envelope = math.exp(-(r**2) / 0.5)
    return spiral * envelope

def photon_wave(x, y):
    kx = 8 * math.cos(0.5)
    ky = 8 * math.sin(0.5)
    wave = math.sin(kx * x + ky * y)
    decay = math.exp(-0.1 * (x**2 + y**2))
    return wave * decay

def galaxy_spiral(x, y):
    r = math.sqrt(x**2 + y**2) + 0.1
    theta = math.atan2(y, x)
    spiral = 2 * (theta - math.log(r + 1))
    intensity = math.exp(-(r**2) / 2)
    return spiral * intensity

render_grid_sample(electron_spiral, "Electron Spiral")
render_grid_sample(photon_wave, "Photon Wave")
render_grid_sample(galaxy_spiral, "Galaxy Spiral")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
print("\nExpected visual patterns:")
print("✓ Electron Spiral: Concentric rings with rotating hue going counterclockwise")
print("✓ Photon Wave: Diagonal stripes from lower-left to upper-right, fading outward")
print("✓ Galaxy Spiral: Logarithmic spiral arms, fading from center")
print("✓ Consciousness: 7 bright spots in heptagon, oscillating between them")
