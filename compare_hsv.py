#!/usr/bin/env python3
"""
Check if matplotlib's hsv_to_rgb matches custom formula
"""

import numpy as np
from matplotlib.colors import hsv_to_rgb as mpl_hsv_to_rgb

def custom_hsv_to_rgb(h, s, v):
    """My custom HSV to RGB"""
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

# Test at key hue/saturation/value combos
test_cases = [
    (0, 1.0, 0.482),    # Red at 0°
    (60, 1.0, 0.482),   # Yellow
    (120, 1.0, 0.482),  # Green
    (180, 1.0, 0.482),  # Cyan
    (240, 1.0, 0.482),  # Blue
    (300, 1.0, 0.482),  # Magenta
]

print("Comparing HSV→RGB implementations:")
print("="*70)

for h_deg, s, v in test_cases:
    # Matplotlib expects hue in [0, 1], not [0, 360]
    h_norm = h_deg / 360.0
    
    # Matplotlib
    mpl_rgb = mpl_hsv_to_rgb([h_norm, s, v])
    mpl_rgb_int = tuple(int(c * 255) for c in mpl_rgb)
    
    # Custom (expects degrees)
    custom_rgb = custom_hsv_to_rgb(h_deg, s, v)
    custom_rgb_int = tuple(int(c * 255) for c in custom_rgb)
    
    match = "✓" if mpl_rgb_int == custom_rgb_int else "✗"
    
    print(f"{match} H={h_deg:3.0f}°, S={s:.1f}, V={v:.3f}")
    print(f"  Matplotlib: {mpl_rgb_int}")
    print(f"  Custom:     {custom_rgb_int}")
    
    if mpl_rgb_int != custom_rgb_int:
        print(f"  DIFF: {tuple(a-b for a,b in zip(mpl_rgb_int, custom_rgb_int))}")

print("\n" + "="*70)
print("SOLUTION: Use matplotlib.colors.hsv_to_rgb in JavaScript OR")
print("Make sure custom formula exactly matches matplotlib implementation")
