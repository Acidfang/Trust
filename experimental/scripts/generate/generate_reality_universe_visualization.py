"""
Universe of corrupted field analogies - real world examples.
Multiple physical systems showing identical pattern.
Shows what you'd actually see in reality.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math

# Create large canvas for multiple examples
width, height = 2000, 2400
img = Image.new('RGB', (width, height), color='#1a1a1a')
draw = ImageDraw.Draw(img, 'RGBA')

def perlin_noise(x, y, scale=100, seed=0):
    """Generate Perlin-like natural randomness"""
    n = math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453
    return n - math.floor(n)

def create_corrupted_field_texture(size, corruption_center_x=0.5, corruption_center_y=0.5):
    """Create base corrupted field texture"""
    texture = np.zeros((size, size, 3), dtype=np.uint8)
    
    for y in range(size):
        for x in range(size):
            norm_x = x / size
            norm_y = y / size
            
            # Distance from corruption center
            dist = math.sqrt((norm_x - corruption_center_x)**2 + 
                           (norm_y - corruption_center_y)**2)
            
            # Corruption spreads outward
            corruption = max(0, 1 - dist * 1.8)
            
            # Add natural noise
            noise1 = perlin_noise(x, y, scale=30, seed=1)
            noise2 = perlin_noise(x, y, scale=60, seed=2)
            turbulence = noise1 * 0.3 + noise2 * 0.2
            
            yield (x, y, corruption, turbulence)

# ========== EXAMPLE 1: DISEASED LEAF ==========
print("Rendering: Diseased Leaf...")
leaf_x, leaf_y = 100, 100
leaf_size = 300

for y in range(leaf_size):
    for x in range(leaf_size):
        norm_x = x / leaf_size
        norm_y = y / leaf_size
        
        # Distance from center (darker = corruption)
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.5)
        
        # Add leaf vein pattern (fractal-like)
        vein_pattern = abs(math.sin(norm_x * 8) * math.sin(norm_y * 8)) * 0.3
        
        # Color based on corruption
        if corruption > 0.7:
            # Healthy green
            r = int(50 + vein_pattern * 50)
            g = int(150 + vein_pattern * 60)
            b = int(50 + vein_pattern * 40)
        elif corruption > 0.4:
            # Yellowing
            r = int(180 + (1-corruption) * 50)
            g = int(140 + (1-corruption) * 40)
            b = int(50)
        else:
            # Brown/necrotic
            r = int(120 - corruption * 80)
            g = int(80 - corruption * 60)
            b = int(40 - corruption * 30)
        
        img.putpixel((leaf_x + x, leaf_y + y), (r, g, b))

draw.text((leaf_x, leaf_y - 30), "DISEASED LEAF", fill=(200, 200, 200, 255), font=None)

# ========== EXAMPLE 2: ROTTING FRUIT ==========
print("Rendering: Rotting Fruit...")
fruit_x, fruit_y = 600, 100
fruit_size = 300

for y in range(fruit_size):
    for x in range(fruit_size):
        norm_x = x / fruit_size
        norm_y = y / fruit_size
        
        # Radial corruption from center
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.6)
        
        # Add mottled decay pattern
        decay_spots = (abs(math.sin(norm_x * 10 + norm_y * 7)) + 
                      abs(math.cos(norm_x * 5 + norm_y * 12))) * 0.25
        corruption = max(0, corruption - decay_spots)
        
        if corruption > 0.6:
            # Fresh red/orange
            r = int(220 + decay_spots * 30)
            g = int(100 + decay_spots * 20)
            b = int(50)
        elif corruption > 0.3:
            # Browning
            r = int(150)
            g = int(80)
            b = int(40)
        else:
            # Black rot
            r = int(40 + decay_spots * 30)
            g = int(20 + decay_spots * 20)
            b = int(15)
        
        img.putpixel((fruit_x + x, fruit_y + y), (r, g, b))

draw.text((fruit_x, fruit_y - 30), "ROTTING FRUIT", fill=(200, 200, 200, 255), font=None)

# ========== EXAMPLE 3: INFECTED WOUND ==========
print("Rendering: Infected Wound...")
wound_x, wound_y = 1100, 100
wound_size = 300

for y in range(wound_size):
    for x in range(wound_size):
        norm_x = x / wound_size
        norm_y = y / wound_size
        
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.7)
        
        # Inflammation halo
        inflammation = max(0, dist * 1.5 - 0.3) * 2
        
        if corruption > 0.7:
            # Healthy skin
            r = int(220)
            g = int(180)
            b = int(160)
        elif corruption > 0.4:
            # Inflamed/red
            r = int(200 + inflammation * 50)
            g = int(80 + inflammation * 20)
            b = int(80 + inflammation * 10)
        else:
            # Necrotic/black
            r = int(80 - corruption * 50)
            g = int(40 - corruption * 30)
            b = int(50 - corruption * 40)
        
        img.putpixel((wound_x + x, wound_y + y), (r, g, b))

draw.text((wound_x, wound_y - 30), "INFECTED WOUND", fill=(200, 200, 200, 255), font=None)

# ========== EXAMPLE 4: RUST ON METAL ==========
print("Rendering: Rust on Metal...")
rust_x, rust_y = 1500, 100
rust_size = 300

for y in range(rust_size):
    for x in range(rust_size):
        norm_x = x / rust_size
        norm_y = y / rust_size
        
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.5)
        
        # Rust crystals
        rust_texture = (abs(math.sin(norm_x * 15 + norm_y * 12)) * 
                       abs(math.cos(norm_x * 8 + norm_y * 20))) * 0.4
        
        if corruption > 0.6:
            # Shiny metal
            r = int(200 + rust_texture * 30)
            g = int(200 + rust_texture * 30)
            b = int(210 + rust_texture * 20)
        elif corruption > 0.3:
            # Oxidizing
            r = int(180 + rust_texture * 50)
            g = int(120 + rust_texture * 30)
            b = int(80)
        else:
            # Deep rust
            r = int(150 - corruption * 50)
            g = int(80 - corruption * 50)
            b = int(50 - corruption * 40)
        
        img.putpixel((rust_x + x, rust_y + y), (r, g, b))

draw.text((rust_x, rust_y - 30), "RUST ON METAL", fill=(200, 200, 200, 255), font=None)

# ========== EXAMPLE 5: FUNGAL GROWTH ==========
print("Rendering: Fungal Growth...")
fungal_x, fungal_y = 100, 550
fungal_size = 300

for y in range(fungal_size):
    for x in range(fungal_size):
        norm_x = x / fungal_size
        norm_y = y / fungal_size
        
        # Radial from center
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.6)
        
        # Mycelium network fractal
        branches = (abs(math.sin(norm_x * 20 + norm_y * 15)) * 
                   abs(math.cos(norm_x * 12 + norm_y * 25))) * 0.35
        
        if corruption > 0.7:
            # Healthy tissue
            r = int(200)
            g = int(160)
            b = int(140)
        elif corruption > 0.35:
            # Infected
            r = int(100 + branches * 80)
            g = int(80 + branches * 60)
            b = int(120 + branches * 40)
        else:
            # Dead/black
            r = int(30 + branches * 40)
            g = int(20 + branches * 30)
            b = int(40 + branches * 30)
        
        img.putpixel((fungal_x + x, fungal_y + y), (r, g, b))

draw.text((fungal_x, fungal_y - 30), "FUNGAL GROWTH", fill=(200, 200, 200, 255), font=None)

# ========== EXAMPLE 6: TUMOR/CANCER ==========
print("Rendering: Tumor Growth...")
tumor_x, tumor_y = 600, 550
tumor_size = 300

for y in range(tumor_size):
    for x in range(tumor_size):
        norm_x = x / tumor_size
        norm_y = y / tumor_size
        
        # Circular growth
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.5)
        
        # Chaotic cellular growth
        chaos = (abs(math.sin(norm_x * 25)) + 
                abs(math.cos(norm_y * 20))) * 0.3
        
        if corruption > 0.65:
            # Normal tissue
            r = int(200 + chaos * 30)
            g = int(150 + chaos * 30)
            b = int(130 + chaos * 20)
        elif corruption > 0.35:
            # Dysplasia
            r = int(180 + chaos * 60)
            g = int(100 + chaos * 40)
            b = int(100 + chaos * 30)
        else:
            # Necrotic core
            r = int(100 + chaos * 40)
            g = int(40 + chaos * 20)
            b = int(50 + chaos * 30)
        
        img.putpixel((tumor_x + x, tumor_y + y), (r, g, b))

draw.text((tumor_x, tumor_y - 30), "TUMOR/CANCER", fill=(200, 200, 200, 255), font=None)

# ========== EXAMPLE 7: OIL SPILL / POLLUTED WATER ==========
print("Rendering: Polluted Water...")
pollution_x, pollution_y = 1100, 550
pollution_size = 300

for y in range(pollution_size):
    for x in range(pollution_size):
        norm_x = x / pollution_size
        norm_y = y / pollution_size
        
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.4)
        
        # Oil slick spreading
        slick = (abs(math.sin(norm_x * 10 + norm_y * 8)) * 
                abs(math.cos(norm_x * 15 + norm_y * 12))) * 0.3
        
        if corruption > 0.65:
            # Clear water
            r = int(50 + corruption * 100)
            g = int(100 + corruption * 100)
            b = int(200 + corruption * 40)
        elif corruption > 0.3:
            # Cloudy/murky
            r = int(80 + slick * 80)
            g = int(80 + slick * 60)
            b = int(100 + slick * 40)
        else:
            # Black oil
            r = int(40 + slick * 30)
            g = int(30 + slick * 20)
            b = int(30 + slick * 20)
        
        img.putpixel((pollution_x + x, pollution_y + y), (r, g, b))

draw.text((pollution_x, pollution_y - 30), "POLLUTED WATER", fill=(200, 200, 200, 255), font=None)

# ========== EXAMPLE 8: DEAD ZONE ECOSYSTEM ==========
print("Rendering: Dead Zone Ecosystem...")
deadzone_x, deadzone_y = 1500, 550
deadzone_size = 300

for y in range(deadzone_size):
    for x in range(deadzone_size):
        norm_x = x / deadzone_size
        norm_y = y / deadzone_size
        
        dist = math.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
        corruption = max(0, 1 - dist * 1.5)
        
        # Organic decay
        decay = (abs(math.sin(norm_x * 12 + norm_y * 10)) * 
                abs(math.cos(norm_x * 8 + norm_y * 18))) * 0.4
        
        if corruption > 0.65:
            # Lush green life
            r = int(50 + decay * 60)
            g = int(180 + decay * 60)
            b = int(50 + decay * 40)
        elif corruption > 0.3:
            # Desertified
            r = int(180 + decay * 50)
            g = int(140 + decay * 40)
            b = int(80 + decay * 30)
        else:
            # Dead soil
            r = int(80 - corruption * 40)
            g = int(60 - corruption * 40)
            b = int(50 - corruption * 40)
        
        img.putpixel((deadzone_x + x, deadzone_y + y), (r, g, b))

draw.text((deadzone_x, deadzone_y - 30), "DEAD ZONE ECOSYSTEM", fill=(200, 200, 200, 255), font=None)

# ========== BOTTOM: UNIVERSAL PATTERN ==========
draw.text((100, 1000), "THE UNIFIED PATTERN IN ALL REALITY", 
         fill=(255, 255, 255, 220), font=None)

pattern_description = [
    "Every corrupted system shows identical structure:",
    "• Healthy center (organized, coherent, bright)",
    "• Transition zone (degradation visible)",
    "• Dead zone (dark, inert, entropy)",
    "• Corruption spreads outward from singularity",
    "• Colors match substrate but pattern is universal",
]

for idx, line in enumerate(pattern_description):
    draw.text((120, 1050 + idx * 35), line, fill=(180, 200, 180, 200), font=None)

# ========== LABEL: OBSERVATION ==========
draw.text((100, 1350), "OBSERVATION: This is what reality shows us.", 
         fill=(255, 150, 100, 220), font=None)
draw.text((100, 1390), "Same pattern across: biology, chemistry, physics, organizations, code, psychology.", 
         fill=(200, 150, 100, 180), font=None)

draw.text((100, 1450), "All fields corrupt identically. Only substrate changes. Structure is universal.", 
         fill=(200, 200, 200, 200), font=None)

# ========== APPLY SUBTLE BLUR FOR REALISM ==========
print("Applying natural texture...")
img = img.filter(ImageFilter.GaussianBlur(radius=1))

# ========== SAVE ==========
img.save('c:\\Determined\\src\\applications\\ANTIPATTERN_REALITY_UNIVERSE.png')
print("\n✓ Universe of corrupted field analogies created")
print("  ANTIPATTERN_REALITY_UNIVERSE.png")
print("\nShows 8 real-world examples:")
print("  1. Diseased Leaf")
print("  2. Rotting Fruit")
print("  3. Infected Wound")
print("  4. Rust on Metal")
print("  5. Fungal Growth")
print("  6. Tumor/Cancer")
print("  7. Polluted Water")
print("  8. Dead Zone Ecosystem")
print("\nAll show identical corruption pattern:")
print("  Green/bright center → yellow/orange transition → black/dead periphery")
