#!/usr/bin/env python3
"""
Check if the difference is just PIL round-trip precision
Regenerate Python images fresh and compare
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

def electron_spiral_numpy(x, y):
    """Using NumPy (what render_potentials_direct.py uses)"""
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    spiral_phase = 12 * theta - 8 * r
    magnitude = np.exp(-(r**2) / (2 * 1.5**2))
    return spiral_phase * magnitude

def hsv_to_rgb_mpl(h, s, v):
    """Using matplotlib's version"""
    from matplotlib.colors import hsv_to_rgb as mpl_hsv2rgb
    # Convert to [0,1] range for matplotlib
    h_norm = (h % 360) / 360.0
    hsv = np.array([[[h_norm, s, v]]])
    rgb = mpl_hsv2rgb(hsv)
    return tuple(int(c * 255) for c in rgb[0, 0])

# Regenerate using EXACT method from render_potentials_direct.py
grid_size = 256
domain = [-2, 2]
x = np.linspace(domain[0], domain[1], grid_size)
y = np.linspace(domain[0], domain[1], grid_size)
X, Y = np.meshgrid(x, y)

# Compute potential
phi = electron_spiral_numpy(X, Y)

# Normalize
phi_normalized = (phi - np.min(phi)) / (np.max(phi) - np.min(phi) + 1e-6)

# Convert to HSV and RGB (matplotlib method)
from matplotlib.colors import hsv_to_rgb as mpl_hsv2rgb

h = (phi / (2 * np.pi)) % 1.0  # Hue wraps
s = np.ones_like(h)  # Full saturation
v = phi_normalized  # Brightness

hsv = np.stack([h, s, v], axis=-1)
rgb = mpl_hsv2rgb(hsv)
rgb_int = (rgb * 255).astype(np.uint8)

# Convert to PIL image
img_fresh = Image.fromarray(rgb_int)

# Load the existing render
img_existing = Image.open('c:/Determined/electron_spiral_direct.png')

# Compare
fresh_array = np.array(img_fresh)
existing_array = np.array(img_existing)

diff = np.abs(fresh_array.astype(int) - existing_array.astype(int))

print("="*70)
print("PIL ROUND-TRIP VERIFICATION")
print("="*70)
print(f"\nFresh render vs Existing PNG:")
print(f"  Max difference: {np.max(diff)}")
print(f"  Mean difference: {np.mean(diff):.2f}")
print(f"  Pixels with diff > 1: {np.sum(diff > 1)} / {256*256}")

corners = [(0,0), (0,255), (255,0), (255,255)]
print(f"\nCorner comparison:")
for cx, cy in corners:
    f = tuple(fresh_array[cy, cx])
    e = tuple(existing_array[cy, cx])
    d = tuple(abs(a-b) for a,b in zip(f,e))
    match = "✓" if np.max(d) <= 1 else "✗"
    print(f"  [{cx:3d},{cy:3d}]: Fresh={f}, Existing={e}, Diff={d} {match}")

# Save fresh version
img_fresh.save('c:/Determined/electron_spiral_fresh.png')
print(f"\n✓ Saved fresh: electron_spiral_fresh.png")

if np.max(diff) <= 1:
    print("\n✓ PIL is preserving data correctly (±1 rounding)")
elif np.max(diff) <= 5:
    print("\n⚠ Minor PIL/float precision differences (±5 on RGB)")
else:
    print("\n✗ MAJOR difference - something is wrong!")
