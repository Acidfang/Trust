#!/usr/bin/env python3
"""
Debug: Find the exact difference between matplotlib HSV and custom HSV
"""

import numpy as np
from matplotlib.colors import hsv_to_rgb as mpl_hsv2rgb

def custom_hsv_to_rgb(h, s, v):
    """My implementation"""
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
    
    return (r + m, g + m, b + m)

# Test at the exact potentials from the image
test_potentials = [
    -39.095,  # Min
    37.572,   # Max
    0.0,      # Middle
    10.0,     # Positive
    -10.0,    # Negative
]

print("="*70)
print("HSV IMPLEMENTATION COMPARISON")
print("="*70)

for pot in test_potentials:
    # Normalize like the render does
    pot_min = -39.095
    pot_max = 37.572
    pot_range = pot_max - pot_min
    v = (pot - pot_min) / pot_range  # Value
    
    # Hue from potential
    h_deg = ((pot % (2 * np.pi)) / (2 * np.pi)) * 360
    h_norm = h_deg / 360.0  # For matplotlib
    
    # Custom formula (expects degrees)
    custom_rgb = custom_hsv_to_rgb(h_deg, 1.0, v)
    custom_rgb_int = tuple(int(c * 255) for c in custom_rgb)
    
    # Matplotlib (expects normalized [0,1])
    mpl_rgb = mpl_hsv2rgb([h_norm, 1.0, v])
    mpl_rgb_int = tuple(int(c * 255) for c in mpl_rgb)
    
    # Difference
    diff = tuple(abs(a - b) for a, b in zip(custom_rgb_int, mpl_rgb_int))
    max_diff = max(diff)
    
    match = "✓" if max_diff <= 1 else "✗"
    
    print(f"\nPotential: {pot:.2f}")
    print(f"  Hue: {h_deg:.1f}°, Value: {v:.3f}")
    print(f"  Custom:     {custom_rgb_int}")
    print(f"  Matplotlib: {mpl_rgb_int}")
    print(f"  Difference: {diff} {match}")

# The key difference might be in boundary cases
print("\n" + "="*70)
print("BOUNDARY CASE ANALYSIS")
print("="*70)

boundary_hues = [0, 60, 120, 180, 240, 300, 359.9]

for h_deg in boundary_hues:
    h_norm = h_deg / 360.0
    s = 1.0
    v = 0.5
    
    custom_rgb = custom_hsv_to_rgb(h_deg, s, v)
    custom_rgb_int = tuple(int(c * 255) for c in custom_rgb)
    
    mpl_rgb = mpl_hsv2rgb([h_norm, s, v])
    mpl_rgb_int = tuple(int(c * 255) for c in mpl_rgb)
    
    diff = max(abs(a - b) for a, b in zip(custom_rgb_int, mpl_rgb_int))
    match = "✓" if diff <= 1 else "✗"
    
    print(f"H={h_deg:6.1f}°: Custom={custom_rgb_int}, Mpl={mpl_rgb_int}, Diff={diff} {match}")

print("\n" + "="*70)
print("RECOMMENDATION")
print("="*70)
print("Use matplotlib.colors.hsv_to_rgb formula in JavaScript, OR")
print("Ensure floating-point math matches exactly")
