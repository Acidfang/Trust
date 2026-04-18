"""
ANIMATION VERIFICATION - Extract frame and check electron positions
"""

from PIL import Image
import numpy as np

# Open animation GIF
gif_path = 'electron_growth_animation.gif'
img = Image.open(gif_path)

# Get a middle frame (Phosphorus P at Z=15)
frame_num = 14  # 0-indexed, so frame 14 = element 15 (P)
img.seek(frame_num)
frame = img.convert('RGB')

# Convert to array
frame_array = np.array(frame)
height, width = frame_array.shape[:2]

print(f"""
================================================================================
ANIMATION FRAME VERIFICATION
================================================================================
Total frames: {img.n_frames}
Frame dimensions: {width}x{height}

Analyzing frame {frame_num} (Element Z={frame_num + 1})
""")

# Define color ranges for orbital types in RGB
color_ranges = {
    's': {
        'name': 's-orbital',
        'expected_rgb': (255, 107, 107),  # #FF6B6B = (255, 107, 107)
        'tolerance': 30,
        'expected_quadrant': 'TOP'
    },
    'p': {
        'name': 'p-orbital',
        'expected_rgb': (78, 205, 196),   # #4ECDC4 = (78, 205, 196)
        'tolerance': 30,
        'expected_quadrant': 'RIGHT'
    },
    'd': {
        'name': 'd-orbital',
        'expected_rgb': (69, 183, 209),   # #45B7D1 = (69, 183, 209)
        'tolerance': 30,
        'expected_quadrant': 'BOTTOM'
    },
    'f': {
        'name': 'f-orbital',
        'expected_rgb': (255, 160, 122),  # #FFA07A = (255, 160, 122)
        'tolerance': 30,
        'expected_quadrant': 'LEFT'
    }
}

# Find center of frame
center_x = width / 2
center_y = height / 2

print(f"Frame center: ({center_x:.0f}, {center_y:.0f})")
print()

# Find all colored electron dots
found_electrons = {
    's': [],
    'p': [],
    'd': [],
    'f': []
}

# Scan for colored pixels (electrons should be ~30-40px diameter)
pixel_map = {}

for orbital_type, color_info in color_ranges.items():
    target_rgb = np.array(color_info['expected_rgb'])
    tolerance = color_info['tolerance']
    
    print(f"Searching for {orbital_type}-orbitals ({color_info['name']})")
    print(f"  Target RGB: {target_rgb}, Tolerance: ±{tolerance}")
    
    # Find pixels matching this color
    frame_rgb = frame_array[:, :, :3]
    distance = np.linalg.norm(frame_rgb.astype(float) - target_rgb, axis=2)
    matches = np.where(distance < tolerance)
    
    if len(matches[0]) > 0:
        # Cluster nearby pixels to find electron centers
        y_pixels, x_pixels = matches
        
        # Simple clustering: find dense regions
        found_positions = []
        visited = set()
        
        for idx in range(len(y_pixels)):
            if idx in visited:
                continue
            
            # Start a cluster
            cluster_x = [x_pixels[idx]]
            cluster_y = [y_pixels[idx]]
            visited.add(idx)
            
            # Find nearby pixels
            for idx2 in range(len(y_pixels)):
                if idx2 in visited:
                    continue
                dist = np.sqrt((x_pixels[idx2] - x_pixels[idx])**2 + 
                             (y_pixels[idx2] - y_pixels[idx])**2)
                if dist < 20:  # Pixels within 20px are part of same electron
                    cluster_x.append(x_pixels[idx2])
                    cluster_y.append(y_pixels[idx2])
                    visited.add(idx2)
            
            # Get cluster center
            avg_x = np.mean(cluster_x)
            avg_y = np.mean(cluster_y)
            found_positions.append((avg_x, avg_y))
        
        # Calculate angle from center for each electron
        print(f"  Found {len(found_positions)} electrons:")
        for px, py in found_positions:
            # Calculate angle from center
            dx = px - center_x
            dy = py - center_y
            angle_rad = np.arctan2(dy, dx)
            angle_deg = np.degrees(angle_rad)
            if angle_deg < 0:
                angle_deg += 360
            
            quadrant = None
            if 0 <= angle_deg <= 45 or 315 <= angle_deg <= 360:
                quadrant = 'TOP'
            elif 45 < angle_deg <= 135:
                quadrant = 'RIGHT'
            elif 135 < angle_deg <= 225:
                quadrant = 'BOTTOM'
            elif 225 < angle_deg < 315:
                quadrant = 'LEFT'
            
            print(f"    Angle: {angle_deg:6.1f}° -> Quadrant: {quadrant}")
            found_electrons[orbital_type].append((px, py, angle_deg, quadrant))
    else:
        print(f"  No pixels found")
    print()

print("=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

for orbital_type, color_info in color_ranges.items():
    expected_quad = color_info['expected_quadrant']
    electrons = found_electrons[orbital_type]
    
    if electrons:
        quadrants = [e[3] for e in electrons]
        in_expected = sum(1 for q in quadrants if q == expected_quad)
        
        print(f"\n{orbital_type}-orbitals (expected: {expected_quad}):")
        print(f"  Found: {len(electrons)} electrons")
        print(f"  In correct quadrant ({expected_quad}): {in_expected}/{len(electrons)}")
        
        if in_expected == len(electrons):
            print(f"  [OK] ALL CORRECT - Electrons properly grouped")
        else:
            print(f"  [ERR] INCORRECT - Electrons scattered across quadrants")
            for e in electrons:
                print(f"      {e[3]} quadrant (angle: {e[2]:.1f}°)")
    else:
        print(f"{orbital_type}-orbitals: [NO DATA] NO ELECTRONS FOUND")

print("\n" + "=" * 80)
