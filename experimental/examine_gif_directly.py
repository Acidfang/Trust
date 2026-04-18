"""
Direct GIF examination - check actual frame properties
"""
from PIL import Image
import json

gif_path = 'electron_growth_animation.gif'
img = Image.open(gif_path)

print("""
================================================================================
DETAILED GIF ANALYSIS
================================================================================

""")

print(f"Total frames: {img.n_frames}")
print(f"Format: {img.format}")
print(f"Mode: {img.mode}")

# Get frame dimensions
print(f"\nFrame info for first 5 frames:")
print(f"{'Frame':<8} {'Size':<15} {'Duration':<12} {'Disposal':<12}")
print("─" * 50)

for frame_idx in range(min(5, img.n_frames)):
    img.seek(frame_idx)
    duration = img.info.get('duration', 'N/A')
    disposal = img.info.get('disposal', 'N/A')
    print(f"{frame_idx:<8} {str(img.size):<15} {str(duration):<12} {str(disposal):<12}")

# Check frame 14 (Phosphorus, Z=15) in detail
print(f"\n{'='*80}")
print(f"FRAME 14 ANALYSIS (Element Z=15 - Phosphorus)")
print(f"{'='*80}\n")

img.seek(14)
print(f"Size: {img.size}")
print(f"Mode: {img.mode}")
print(f"Duration: {img.info.get('duration', 'N/A')}ms")
print(f"Disposal: {img.info.get('disposal', 'N/A')}")

# Convert to RGB
frame = img.convert('RGB')
frame_array = frame.tobytes()
print(f"Frame data size: {len(frame_array)} bytes")
print(f"Expected size (1400x1000x3): {1400*1000*3} bytes")

# Check if frame looks corrupted
unique_bytes = len(set(frame_array[:10000]))  # Sample first 10KB
print(f"Unique byte values in first 10KB: {unique_bytes}")

# Check actual pixel values at known positions
pixels = frame.load()
width, height = frame.size
center_x, center_y = width // 2, height // 2

print(f"\nSample pixels:")
print(f"  Center ({center_x}, {center_y}): RGB{pixels[center_x, center_y]}")
print(f"  Left ({center_x-100}, {center_y}): RGB{pixels[center_x-100, center_y]}")
print(f"  Right ({center_x+100}, {center_y}): RGB{pixels[center_x+100, center_y]}")
print(f"  Top ({center_x}, {center_y-100}): RGB{pixels[center_x, center_y-100]}")
print(f"  Bottom ({center_x}, {center_y+100}): RGB{pixels[center_x, center_y+100]}")

# Check for colored pixels (should be electrons)
print(f"\nLooking for red pixels (s-orbital = #FF6B6B ≈ (255, 107, 107))...")
red_target = (255, 107, 107)
red_count = 0
red_samples = []

for x in range(0, width, 20):
    for y in range(0, height, 20):
        r, g, b = pixels[x, y]
        # Check if close to red target
        if abs(r - 255) < 50 and abs(g - 107) < 50 and abs(b - 107) < 50:
            red_count += 1
            if len(red_samples) < 5:
                red_samples.append(((x, y), (r, g, b)))

print(f"Found approximately {red_count*25} red-ish pixels (sampled every 20px)")
print(f"Sample positions/colors: {red_samples}")

print(f"\nLooking for teal pixels (p-orbital = #4ECDC4 ≈ (78, 205, 196))...")
teal_target = (78, 205, 196)
teal_count = 0
teal_samples = []

for x in range(0, width, 20):
    for y in range(0, height, 20):
        r, g, b = pixels[x, y]
        # Check if close to teal target
        if abs(r - 78) < 50 and abs(g - 205) < 50 and abs(b - 196) < 50:
            teal_count += 1
            if len(teal_samples) < 5:
                teal_samples.append(((x, y), (r, g, b)))

print(f"Found approximately {teal_count*25} teal-ish pixels (sampled every 20px)")
print(f"Sample positions/colors: {teal_samples}")

print(f"\n{'='*80}")
print("QUESTION: Is the animation actually rendering the quadrant positioning?")
print("Or is it using old/cached frame data?")
print(f"{'='*80}")
