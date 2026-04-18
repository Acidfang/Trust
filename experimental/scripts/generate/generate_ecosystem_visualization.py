"""
Generate realistic nature visualization of antipattern chains.
Shows entire ecosystem degradation: soil, atmosphere, water, life.
Field effects as a whole - corruption spreads through environment.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math

# Create high-res image
width, height = 1920, 1080
img = Image.new('RGB', (width, height))
pixels = img.load()

# ========== PERLIN NOISE GENERATION ==========
def perlin_noise_2d(x, y, seed=0):
    """Simple Perlin-like noise for natural randomness"""
    np.random.seed(int((x + y + seed) * 1000) % (2**32))
    n = np.sin(x * 12.9898 + y * 78.233) * 43758.5453
    return n - math.floor(n)

def smooth_interpolation(t):
    """Smooth Hermite interpolation"""
    return t * t * (3.0 - 2.0 * t)

def perlin_blend(x, y, scale=100, seed=0):
    """Multi-octave Perlin noise"""
    value = 0
    amplitude = 1
    frequency = 1
    max_value = 0
    
    for i in range(5):  # 5 octaves
        sample_x = x * frequency / scale
        sample_y = y * frequency / scale
        
        xi = int(sample_x) % 1000
        yi = int(sample_y) % 1000
        xf = sample_x - xi
        yf = sample_y - yi
        
        u = smooth_interpolation(xf)
        v = smooth_interpolation(yf)
        
        n00 = perlin_noise_2d(xi, yi, seed + i)
        n10 = perlin_noise_2d(xi + 1, yi, seed + i)
        n01 = perlin_noise_2d(xi, yi + 1, seed + i)
        n11 = perlin_noise_2d(xi + 1, yi + 1, seed + i)
        
        nx0 = n00 * (1 - u) + n10 * u
        nx1 = n01 * (1 - u) + n11 * u
        n = nx0 * (1 - v) + nx1 * v
        
        value += n * amplitude
        max_value += amplitude
        
        amplitude *= 0.5
        frequency *= 2
    
    return value / max_value

# ========== ENVIRONMENT STATE BASED ON CORRUPTION LEVEL ==========
def get_environment_state(x_progress, corruption_level):
    """
    Returns environment parameters based on distance from corruption center.
    corruption_level: 0 (healthy) to 1 (completely dead)
    """
    return {
        'soil_richness': 1 - corruption_level,  # Brown/healthy → gray dead
        'vegetation_density': 1 - corruption_level,  # Full trees → bare ground
        'water_clarity': 1 - corruption_level,  # Clear → murky
        'sky_clarity': 1 - corruption_level,  # Bright → dark/hazy
        'air_particles': corruption_level,  # Clean → polluted/smoky
        'wildlife_presence': 1 - corruption_level,  # Animals present → empty
        'growth_vigor': 1 - corruption_level,  # Vibrant colors → gray
    }

# ========== BUILD ENVIRONMENT LAYER BY LAYER ==========

# For each pixel
for pixel_x in range(width):
    for pixel_y in range(height):
        # Normalize coordinates
        norm_x = pixel_x / width  # 0 to 1 (left to right)
        norm_y = pixel_y / height  # 0 to 1 (top to bottom)
        
        # Distance from corruption center (middle of image, slightly right)
        center_x = 0.65
        center_y = 0.5
        dist_to_center = math.sqrt((norm_x - center_x)**2 + (norm_y - center_y)**2)
        
        # Corruption spreads outward
        corruption_level = max(0, 1 - dist_to_center * 2.5)
        
        env = get_environment_state(norm_x, corruption_level)
        
        # ========== SKY LAYER ==========
        if pixel_y < height * 0.4:
            # Left side: clear blue sky
            if norm_x < 0.3:
                sky_r = int(135 + perlin_blend(pixel_x, pixel_y, scale=200) * 20)
                sky_g = int(206 + perlin_blend(pixel_x, pixel_y, scale=200, seed=1) * 20)
                sky_b = int(235 + perlin_blend(pixel_x, pixel_y, scale=200, seed=2) * 20)
            # Middle: transitional
            elif norm_x < 0.6:
                transition = (norm_x - 0.3) / 0.3
                corruption_sky = corruption_level
                
                # Blue sky fading to gray-brown haze
                base_r = int(135 * (1 - corruption_sky) + 100 * corruption_sky)
                base_g = int(206 * (1 - corruption_sky) + 90 * corruption_sky)
                base_b = int(235 * (1 - corruption_sky) + 70 * corruption_sky)
                
                # Add haze particles
                haze = perlin_blend(pixel_x, pixel_y, scale=150, seed=3) * corruption_sky * 40
                
                sky_r = int(base_r + haze)
                sky_g = int(base_g + haze * 0.8)
                sky_b = int(base_b + haze * 0.6)
            # Right side: dark, polluted
            else:
                sky_r = int(80 + perlin_blend(pixel_x, pixel_y, scale=300) * 30)
                sky_g = int(60 + perlin_blend(pixel_x, pixel_y, scale=300, seed=1) * 20)
                sky_b = int(40 + perlin_blend(pixel_x, pixel_y, scale=300, seed=2) * 15)
            
            sky_r = max(0, min(255, sky_r))
            sky_g = max(0, min(255, sky_g))
            sky_b = max(0, min(255, sky_b))
            
            pixels[pixel_x, pixel_y] = (sky_r, sky_g, sky_b)
        
        # ========== GROUND/VEGETATION LAYER ==========
        else:
            # Determine vertical strip we're in
            ground_height = pixel_y - int(height * 0.4)
            
            # Left side: Healthy ecosystem
            if norm_x < 0.3:
                # Soil: rich brown
                soil_r = int(101 + perlin_blend(pixel_x, pixel_y, scale=100) * 40)
                soil_g = int(67 + perlin_blend(pixel_x, pixel_y, scale=100, seed=1) * 30)
                soil_b = int(33 + perlin_blend(pixel_x, pixel_y, scale=100, seed=2) * 20)
                
                # Vegetation overlay (trees, grass)
                veg_noise = perlin_blend(pixel_x, pixel_y, scale=80, seed=4)
                if veg_noise > 0.4 and ground_height < 200:  # Trees in upper ground
                    soil_r = int(34 + veg_noise * 50)
                    soil_g = int(87 + veg_noise * 60)
                    soil_b = int(34 + veg_noise * 40)
                
                pixels[pixel_x, pixel_y] = (soil_r, soil_g, soil_b)
            
            # Middle: Degradation layers
            elif norm_x < 0.7:
                corruption_percentage = (norm_x - 0.3) / 0.4
                
                # Layer-by-layer corruption
                layer_corruption = corruption_level * 5  # 5 corruption layers
                
                if layer_corruption < 1:
                    # Layer 1: Soil compaction (darker, less rich)
                    soil_r = int(101 - 20 * layer_corruption)
                    soil_g = int(67 - 15 * layer_corruption)
                    soil_b = int(33 - 10 * layer_corruption)
                    
                    # Sparse vegetation
                    veg_noise = perlin_blend(pixel_x, pixel_y, scale=60, seed=4)
                    if veg_noise > 0.6 and ground_height < 150:
                        soil_r = int(34 + veg_noise * 40)
                        soil_g = int(87 + veg_noise * 40)
                        soil_b = int(34 + veg_noise * 30)
                
                elif layer_corruption < 2:
                    # Layer 2: Erosion begins (gray/exposed rock)
                    erosion_amt = (layer_corruption - 1)
                    soil_r = int(100 - 20 - 40 * erosion_amt)
                    soil_g = int(100 - 20 - 30 * erosion_amt)
                    soil_b = int(100 - 20 - 20 * erosion_amt)
                
                elif layer_corruption < 3:
                    # Layer 3: Heavy erosion (dead gray)
                    soil_r = int(70)
                    soil_g = int(70)
                    soil_b = int(70)
                
                elif layer_corruption < 4:
                    # Layer 4: Toxic exposure (sickly yellow-gray)
                    toxic_amt = (layer_corruption - 3)
                    soil_r = int(70 + 50 * toxic_amt)
                    soil_g = int(70 + 30 * toxic_amt)
                    soil_b = int(70 - 30 * toxic_amt)
                
                else:
                    # Layer 5: Complete corruption (dark toxic)
                    soil_r = int(120)
                    soil_g = int(100)
                    soil_b = int(40)
                
                pixels[pixel_x, pixel_y] = (soil_r, soil_g, soil_b)
            
            # Right side: Dead ecosystem
            else:
                # Sterile, lifeless ground
                soil_r = int(60 + perlin_blend(pixel_x, pixel_y, scale=150, seed=5) * 30)
                soil_g = int(60 + perlin_blend(pixel_x, pixel_y, scale=150, seed=6) * 20)
                soil_b = int(50 + perlin_blend(pixel_x, pixel_y, scale=150, seed=7) * 15)
                
                # Occasional toxic discoloration
                toxic_noise = perlin_blend(pixel_x, pixel_y, scale=200, seed=8)
                if toxic_noise > 0.7:
                    soil_r = int(soil_r + 40)
                    soil_b = int(soil_b - 20)
                
                pixels[pixel_x, pixel_y] = (soil_r, soil_g, soil_b)

# ========== POST-PROCESSING: ADD FIELD EFFECTS ==========

# Apply Gaussian blur to create atmospheric haze effect
img = img.filter(ImageFilter.GaussianBlur(radius=2))

# Add infection/corruption tendrils
draw = ImageDraw.Draw(img, 'RGBA')

# Draw corruption spreading from center
center_px_x = int(width * 0.65)
center_px_y = int(height * 0.5)

for tendril in range(20):
    angle = (tendril / 20) * 2 * math.pi
    for distance in range(0, int(width * 0.5), 10):
        x = center_px_x + distance * math.cos(angle)
        y = center_px_y + distance * math.sin(angle)
        
        # Tendrils get darker toward center
        opacity = int(100 * (1 - distance / (width * 0.5)))
        
        # Draw corruption tendrils
        draw.ellipse([x-5, y-5, x+5, y+5], fill=(150, 100, 30, opacity))

# Add atmospheric particles (pollution/haze)
particle_density = perlin_blend(width//2, height//2, scale=500, seed=100)
for _ in range(int(500 * (0.5 + particle_density))):
    particle_x = np.random.randint(0, width)
    particle_y = np.random.randint(0, int(height * 0.4))
    
    # More particles on right (corrupted) side
    if particle_x > width * 0.5:
        opacity = int(50 * (1 - (particle_x - width * 0.5) / (width * 0.5)))
        draw.ellipse([particle_x-2, particle_y-2, particle_x+2, particle_y+2], 
                    fill=(200, 180, 150, opacity))

# Add water element showing corruption (if present)
water_y = int(height * 0.7)
for x in range(width):
    norm_x = x / width
    
    # Water quality degrades left to right
    health = 1 - norm_x
    
    # Left: clear water
    if norm_x < 0.3:
        for y in range(water_y, water_y + 50):
            if y < height:
                r, g, b = pixels[x, y]
                # Add water reflection
                r = int(r * 0.8 + 100 * 0.2)
                g = int(g * 0.8 + 150 * 0.2)
                b = int(b * 0.8 + 200 * 0.2)
                pixels[x, y] = (r, g, b)
    
    # Middle: murky
    elif norm_x < 0.7:
        murk = (norm_x - 0.3) * 1.25
        for y in range(water_y, water_y + 50):
            if y < height:
                r, g, b = pixels[x, y]
                r = int(r * (1 - murk) + 80 * murk)
                g = int(g * (1 - murk) + 100 * murk)
                b = int(b * (1 - murk) + 60 * murk)
                pixels[x, y] = (r, g, b)
    
    # Right: toxic/dead
    else:
        for y in range(water_y, water_y + 50):
            if y < height:
                r, g, b = pixels[x, y]
                r = int(r * 0.5 + 100 * 0.5)
                g = int(g * 0.5 + 60 * 0.5)
                b = int(b * 0.5 + 40 * 0.5)
                pixels[x, y] = (r, g, b)

# ========== ADD TEXT LABELS ==========
draw.text((50, 50), 'HEALTHY ECOSYSTEM', fill=(34, 139, 34, 200), font=None)
draw.text((width//2 - 100, 50), 'CORRUPTION SPREADING', fill=(255, 165, 0, 200), font=None)
draw.text((width - 300, 50), 'DEAD SYSTEM', fill=(80, 0, 0, 200), font=None)

draw.text((50, height - 100), 
         'Field Effect: Corruption spreads through entire environment\n' +
         '5 layers of degradation from healthy soil to toxic waste\n' +
         'Atmosphere darkens, water pollutes, life disappears',
         fill=(200, 200, 200, 180), font=None)

# ========== SAVE ==========
img.save('c:\\Determined\\src\\applications\\ANTIPATTERN_ECOSYSTEM_VISUALIZATION.png')
print("✓ Ecosystem visualization generated: ANTIPATTERN_ECOSYSTEM_VISUALIZATION.png")

# Save high-res
img_hd = Image.new('RGB', (3840, 2160))
img_hd.paste(img.resize((3840, 2160), Image.LANCZOS))
img_hd.save('c:\\Determined\\src\\applications\\ANTIPATTERN_ECOSYSTEM_VISUALIZATION_HD.png')
print("✓ High-res ecosystem visualization: ANTIPATTERN_ECOSYSTEM_VISUALIZATION_HD.png")

print("\nVisualization shows:")
print("  • Left: Healthy ecosystem (vibrant soil, rich vegetation, clear water, bright sky)")
print("  • Middle: 5 degradation layers (compaction → erosion → exposure → toxicity → corruption)")
print("  • Right: Dead system (lifeless, gray, polluted, dark)")
print("  • Field effects: Corruption tendrils, atmospheric haze, spreading pollution")
