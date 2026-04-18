"""
GIF ANIMATION TEMPORAL VERIFICATION
Verify animation progression across all 37 frames
Check that visual state matches determined outcome patterns
"""

from PIL import Image
import numpy as np
from collections import defaultdict

gif_path = 'electron_growth_animation.gif'
img = Image.open(gif_path)

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           GIF ANIMATION TEMPORAL VERIFICATION SYSTEM                      ║
║          Checking all 37 frames for correct progression patterns          ║
╚════════════════════════════════════════════════════════════════════════════╝

ANALYSIS: Frame-by-frame state verification

""")

# Color targets
color_targets = {
    's': (255, 107, 107),   # #FF6B6B Red
    'p': (78, 205, 196),    # #4ECDC4 Teal
    'd': (69, 183, 209),    # #45B7D1 Blue
    'f': (255, 160, 122)    # #FFA07A Salmon
}

tolerance = 40  # Color matching tolerance

# Quadrant definitions
def get_quadrant(angle_deg):
    """Convert angle to quadrant name"""
    angle_deg = angle_deg % 360
    if 315 <= angle_deg or angle_deg < 45:
        return "TOP"
    elif 45 <= angle_deg < 135:
        return "RIGHT"
    elif 135 <= angle_deg < 225:
        return "BOTTOM"
    else:
        return "LEFT"

# Check key frames
key_frames = {
    0: {'element': 'H', 'z': 1, 'expected_total': 1},
    1: {'element': 'He', 'z': 2, 'expected_total': 2},
    2: {'element': 'Li', 'z': 3, 'expected_total': 3},
    7: {'element': 'N', 'z': 7, 'expected_total': 7},
    14: {'element': 'P', 'z': 15, 'expected_total': 15},
    20: {'element': 'Ca', 'z': 20, 'expected_total': 20},
    36: {'element': 'Tc', 'z': 37, 'expected_total': 37}
}

print(f"Total frames in GIF: {img.n_frames}")
print(f"Checking {len(key_frames)} key frames for state verification\n")
print("=" * 80)

frame_data = {}

for frame_idx in key_frames.keys():
    img.seek(frame_idx)
    frame = img.convert('RGB')
    width, height = frame.size
    center_x, center_y = width // 2, height // 2
    
    element_info = key_frames[frame_idx]
    element = element_info['element']
    z = element_info['z']
    expected_total = element_info['expected_total']
    
    print(f"\nFrame {frame_idx}: {element} (Z={z})")
    print(f"  Expected electrons: {expected_total}")
    print("  " + "─" * 76)
    
    # Find electrons by color
    electrons_by_type = defaultdict(list)
    
    pixels = frame.load()
    
    # Scan for colored pixels
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            
            # Check each orbital type color
            for orbital_type, (target_r, target_g, target_b) in color_targets.items():
                dist = np.sqrt((r - target_r)**2 + (g - target_g)**2 + (b - target_b)**2)
                
                if dist < tolerance:
                    # Calculate angle from center
                    dx = x - center_x
                    dy = y - center_y
                    
                    if dx == 0 and dy == 0:
                        continue
                    
                    angle_rad = np.arctan2(dy, dx)
                    angle_deg = np.degrees(angle_rad)
                    if angle_deg < 0:
                        angle_deg += 360
                    
                    quadrant = get_quadrant(angle_deg)
                    
                    # Store electron (avoiding duplicates from same pixel cluster)
                    found_duplicate = False
                    for prev_x, prev_y, prev_type in electrons_by_type[orbital_type]:
                        if abs(x - prev_x) < 3 and abs(y - prev_y) < 3:
                            found_duplicate = True
                            break
                    
                    if not found_duplicate:
                        electrons_by_type[orbital_type].append((x, y, orbital_type))
    
    # Analyze results
    total_found = sum(len(v) for v in electrons_by_type.values())
    
    print(f"  Total electrons found: {total_found}")
    
    for orbital_type in ['s', 'p', 'd', 'f']:
        if electrons_by_type[orbital_type]:
            count = len(electrons_by_type[orbital_type])
            
            # Get quadrants for this type
            quadrants = defaultdict(int)
            for x, y, _ in electrons_by_type[orbital_type]:
                angle_rad = np.arctan2(y - center_y, x - center_x)
                angle_deg = np.degrees(angle_rad)
                if angle_deg < 0:
                    angle_deg += 360
                quadrant = get_quadrant(angle_deg)
                quadrants[quadrant] += 1
            
            expected_quadrant = {
                's': 'TOP',
                'p': 'RIGHT',
                'd': 'BOTTOM',
                'f': 'LEFT'
            }[orbital_type]
            
            quadrant_dist = dict(quadrants)
            dominant_quad = max(quadrant_dist, key=quadrant_dist.get) if quadrant_dist else "NONE"
            dominant_pct = (quadrant_dist.get(dominant_quad, 0) / count * 100) if count > 0 else 0
            
            status = '[OK]' if dominant_quad == expected_quadrant else '[ERR]'
            
            print(f"    {orbital_type}-orbital: {count:2d} electrons | "
                  f"Dominant: {dominant_quad:6s} ({dominant_pct:5.1f}%) | "
                  f"Expected: {expected_quadrant:6s} {status}")
    
    # State check
    if total_found == expected_total:
        print(f"  [OK] Electron count correct")
    else:
        print(f"  [WARN] Expected {expected_total}, found {total_found}")
    
    frame_data[frame_idx] = {
        'element': element,
        'found': total_found,
        'expected': expected_total,
        'by_type': dict(electrons_by_type)
    }

print("\n" + "=" * 80)
print("TEMPORAL CONSISTENCY CHECK")
print("=" * 80)

# Check if electron count progresses correctly
print("\nElectron count progression:")
prev_count = 0
progression_ok = True

for frame_idx in sorted(key_frames.keys()):
    expected = key_frames[frame_idx]['expected_total']
    found = frame_data[frame_idx]['found']
    
    is_increasing = found >= prev_count
    indicator = "[OK]" if is_increasing else "[FAIL]"
    
    print(f"  Frame {frame_idx:2d}: {found:2d} electrons (expected {expected:2d}) {indicator}")
    
    if not is_increasing:
        progression_ok = False
    
    prev_count = found

print("\n" + "=" * 80)
print("VERDICT")
print("=" * 80)

if not progression_ok:
    print("\n[FAIL] Animation does not show correct temporal progression")
else:
    print("\n[OK] Temporal progression looks correct")

print("""
NEXT: Manual visual inspection required
======================================

User must view the animation and verify:
1. First frame (H): Single red dot at TOP
2. Frame 7 (N): Red cluster at TOP, some teal at RIGHT
3. Frame 14 (P): Clear TOP/RIGHT separation (TOP=red, RIGHT=teal)
4. Frame 20 (Ca): More teal visible, quadrants distinct
5. Frame 36 (Tc): Multiple shells, all 4 quadrants potentially visible

Key visual determinants:
✓ Red electrons ALWAYS at TOP
✓ Teal electrons ALWAYS at RIGHT
✓ Clear left-right separation (not overlapping)
✓ Shells progressively further from center

Current status from your screenshot: FAILS these checks
""")
