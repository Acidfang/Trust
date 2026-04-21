#!/usr/bin/env python3
"""
Analyze the FULL image - not just test points
Check if spiral is complete across entire domain
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Load the actual rendered image
img = Image.open('c:/Determined/electron_spiral_direct.png')
img_array = np.array(img)

print("="*70)
print("FULL IMAGE ANALYSIS - Electron Spiral")
print("="*70)
print(f"Image shape: {img_array.shape}")
print(f"Image size: {img.size}")

# Convert RGB to grayscale to see intensity structure
gray = np.mean(img_array, axis=2)

print(f"\nGrayscale intensity range: [{gray.min():.1f}, {gray.max():.1f}]")

# Look at specific scanlines to see patterns
print("\nHorizontal scanline (middle, y=128):")
scanline_h = img_array[128, :, :]
print(f"  R values (first 20): {scanline_h[:20, 0]}")
print(f"  G values (first 20): {scanline_h[:20, 1]}")
print(f"  B values (first 20): {scanline_h[:20, 2]}")

print("\nVertical scanline (middle, x=128):")
scanline_v = img_array[:, 128, :]
print(f"  R values (first 20): {scanline_v[:20, 0]}")
print(f"  G values (first 20): {scanline_v[:20, 1]}")
print(f"  B values (first 20): {scanline_v[:20, 2]}")

# Check what's in different regions
print("\n" + "="*70)
print("REGIONAL ANALYSIS")
print("="*70)

regions = {
    "Top-left corner [0:10, 0:10]": (slice(0, 10), slice(0, 10)),
    "Center [120:136, 120:136]": (slice(120, 136), slice(120, 136)),
    "Top-right corner [0:10, 245:256]": (slice(0, 10), slice(245, 256)),
    "Bottom-left corner [245:256, 0:10]": (slice(245, 256), slice(0, 10)),
    "Bottom-right corner [245:256, 245:256]": (slice(245, 256), slice(245, 256)),
}

for name, (y_slice, x_slice) in regions.items():
    region = img_array[y_slice, x_slice, :]
    print(f"\n{name}:")
    print(f"  Shape: {region.shape}")
    print(f"  Color (mean): R={region[:,:,0].mean():.0f}, G={region[:,:,1].mean():.0f}, B={region[:,:,2].mean():.0f}")
    print(f"  Intensity range: [{region.mean(axis=2).min():.0f}, {region.mean(axis=2).max():.0f}]")
    
    # Check if all pixels are same color (suggesting missing computation)
    unique_colors = len(np.unique(region.reshape(-1, 3), axis=0))
    print(f"  Unique colors in region: {unique_colors}")

# Visual inspection - check if the spiral actually extends to edges
print("\n" + "="*70)
print("SPIRAL EXTENT CHECK")
print("="*70)

# Check intensity at different radii
center = 128
radii = [10, 20, 50, 100, 120, 127]

for r in radii:
    # Sample at cardinal directions from center
    samples = [
        (center, center + r, "right"),
        (center, center - r, "left"),
        (center + r, center, "down"),
        (center - r, center, "up"),
    ]
    
    print(f"\nRadius {r} from center:")
    for y, x, direction in samples:
        if 0 <= x < 256 and 0 <= y < 256:
            rgb = img_array[y, x, :]
            intensity = rgb.mean()
            print(f"  {direction:5s} ({x:3d},{y:3d}): RGB={tuple(rgb)}, intensity={intensity:.0f}")

# Check if image is all uniform color (would indicate error)
unique_pixels = len(np.unique(img_array.reshape(-1, 3), axis=0))
print(f"\n{'='*70}")
print(f"Total unique colors in image: {unique_pixels}")
if unique_pixels < 100:
    print("⚠️  WARNING: Very few unique colors - may indicate rendering error!")
else:
    print(f"✓ Good color variation ({unique_pixels} unique colors)")

# Create a visual comparison showing what regions have data
print("\n" + "="*70)
print("CREATING DIAGNOSTIC VISUALIZATION")
print("="*70)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))

# Original image
axes[0,0].imshow(img_array)
axes[0,0].set_title('Original Render')
axes[0,0].grid(True, alpha=0.3)

# Intensity map
axes[0,1].imshow(gray, cmap='gray')
axes[0,1].set_title('Intensity (grayscale)')
axes[0,1].grid(True, alpha=0.3)

# Hue map (from RGB)
hsv_array = np.zeros((256, 256, 3))
for y in range(256):
    for x in range(256):
        r, g, b = img_array[y, x, :] / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c
        
        if delta == 0:
            h = 0
        elif max_c == r:
            h = 60 * (((g - b) / delta) % 6)
        elif max_c == g:
            h = 60 * ((b - r) / delta + 2)
        else:
            h = 60 * ((r - g) / delta + 4)
        
        h = h / 360.0
        hsv_array[y, x, 0] = h

axes[1,0].imshow(hsv_array[:,:,0], cmap='hsv')
axes[1,0].set_title('Hue Map')
axes[1,0].grid(True, alpha=0.3)

# Saturation of colors
sat_array = np.zeros((256, 256))
for y in range(256):
    for x in range(256):
        r, g, b = img_array[y, x, :] / 255.0
        max_c = max(r, g, b)
        if max_c == 0:
            sat = 0
        else:
            sat = (max_c - min(r, g, b)) / max_c
        sat_array[y, x] = sat

axes[1,1].imshow(sat_array, cmap='viridis')
axes[1,1].set_title('Color Saturation')
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('c:/Determined/electron_spiral_diagnostics.png', dpi=100)
print("✓ Saved: electron_spiral_diagnostics.png")

# Check the outer edges specifically
print("\n" + "="*70)
print("EDGE ANALYSIS")
print("="*70)

edge_corners = {
    "TL": img_array[0:1, 0:1, :][0,0],
    "TR": img_array[0:1, 255:256, :][0,0],
    "BL": img_array[255:256, 0:1, :][0,0],
    "BR": img_array[255:256, 255:256, :][0,0],
}

for corner, rgb in edge_corners.items():
    print(f"{corner}: RGB={tuple(rgb)}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("Check the diagnostic image to see if spiral extends fully.")
print("If outer regions are all same color, spiral doesn't reach edges.")
