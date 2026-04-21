"""
Wiki Animation Framework - Convert Static to Temporal
======================================================

Core Principle:
Everything in the wiki describes a PROCESS through time.

Static wiki should become:
- Animated GIFs/MP4s showing evolution
- Interactive HTML5 canvas showing real-time progression
- Time slider to scrub through moments
- Phase indicators showing where in cycle we are

This framework automates conversion of static visuals to animated ones.
"""

import numpy as np
from PIL import Image, ImageDraw
import math
import json

# ═══════════════════════════════════════════════════════════════════════════
# ANIMATION TEMPLATES FOR UFM CONCEPTS
# ═══════════════════════════════════════════════════════════════════════════

class AnimationTemplate:
    """Base class for all wiki concept animations"""
    
    def __init__(self, name, description, num_frames=24):
        self.name = name
        self.description = description
        self.num_frames = num_frames
        self.frames = []
    
    def generate_frames(self, t):
        """Override: Generate single frame at time t (0-1)"""
        raise NotImplementedError
    
    def create_animation(self):
        """Generate all frames"""
        for frame_num in range(self.num_frames):
            t = frame_num / self.num_frames
            frame = self.generate_frames(t)
            self.frames.append(frame)
        return self.frames
    
    def save_gif(self, filename):
        """Save as animated GIF"""
        if not self.frames:
            self.create_animation()
        
        self.frames[0].save(
            filename,
            save_all=True,
            append_images=self.frames[1:],
            duration=100,
            loop=0
        )


class ElectronOrbitalAnimation(AnimationTemplate):
    """
    Animate electron orbital probability density.
    Shows how electron probability cloud cycles through quantum states.
    """
    
    def __init__(self):
        super().__init__(
            "Electron Orbital",
            "Hydrogen-like electron showing s, p, d orbital transitions"
        )
    
    def generate_frames(self, t):
        img = Image.new('RGB', (256, 256), color=(20, 20, 25))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Cycle through s → p → d orbitals
        orbital_cycle = (t * 3) % 3
        
        if orbital_cycle < 1:
            # S-ORBITAL (spherical)
            phase = orbital_cycle
            draw.text((10, 10), "1s Orbital (spherical)", fill=(100, 200, 255))
            
            # Draw expanding/contracting sphere
            radius = 50 + 30 * math.sin(phase * math.pi)
            draw.ellipse(
                [(128 - radius, 128 - radius), (128 + radius, 128 + radius)],
                outline=(100, 200, 255),
                width=2
            )
            
            # Probability density at current time
            brightness = int(200 * (0.5 + 0.5 * math.sin(phase * math.pi)))
            for angle in np.linspace(0, 2*math.pi, 20):
                x = 128 + radius * math.cos(angle)
                y = 128 + radius * math.sin(angle)
                draw.ellipse([(x-2, y-2), (x+2, y+2)], fill=(100, brightness, 255))
        
        elif orbital_cycle < 2:
            # P-ORBITAL (dumbbell)
            phase = orbital_cycle - 1
            draw.text((10, 10), "2p Orbital (dumbbell)", fill=(150, 200, 100))
            
            # Two lobes
            lobe_y = 80 + 50 * math.sin(phase * math.pi)
            
            # Upper lobe
            draw.ellipse(
                [(100, 128 - lobe_y - 30), (156, 128 - lobe_y + 30)],
                outline=(150, 200, 100),
                width=2
            )
            
            # Lower lobe
            draw.ellipse(
                [(100, 128 + lobe_y - 30), (156, 128 + lobe_y + 30)],
                outline=(150, 200, 100),
                width=2
            )
            
            # Nodal plane at center
            draw.line([(80, 128), (176, 128)], fill=(200, 100, 100), width=1)
        
        else:
            # D-ORBITAL (cloverleaf)
            phase = orbital_cycle - 2
            draw.text((10, 10), "3d Orbital (cloverleaf)", fill=(200, 150, 100))
            
            # Four lobes in cloverleaf pattern
            lobes = [
                (100, 80),   # top
                (156, 100),  # right
                (156, 156),  # bottom
                (100, 156)   # left
            ]
            
            size = 25 + 15 * math.sin(phase * math.pi)
            for lobe_x, lobe_y in lobes:
                draw.ellipse(
                    [(lobe_x - size, lobe_y - size), (lobe_x + size, lobe_y + size)],
                    outline=(200, 150, 100),
                    width=2
                )
        
        # Radial decay envelope (all orbitals)
        decay_line = f"Radial decay: e^(-αr)"
        draw.text((10, 230), decay_line, fill=(150, 150, 150))
        
        # Phase indicator
        phase_pct = int(t * 100)
        draw.text((200, 230), f"Phase: {phase_pct}%", fill=(100, 200, 255))
        
        return img


class PhotonWaveAnimation(AnimationTemplate):
    """Animate photon as electromagnetic wave propagating through space"""
    
    def __init__(self):
        super().__init__(
            "Photon Wave",
            "Electromagnetic plane wave propagating with wave packet envelope"
        )
    
    def generate_frames(self, t):
        img = Image.new('RGB', (512, 128), color=(20, 20, 25))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Wave parameters
        wavelength = 50
        amplitude = 30
        propagation_speed = 256  # pixels per full cycle
        
        # Wave position (shifting phase with time)
        phase_shift = t * propagation_speed
        
        # Draw wave
        x_points = np.linspace(0, 512, 200)
        for i in range(len(x_points) - 1):
            x1, x2 = x_points[i], x_points[i+1]
            
            # Oscillation
            y1 = 64 + amplitude * math.sin(2 * math.pi * (x1 - phase_shift) / wavelength)
            y2 = 64 + amplitude * math.sin(2 * math.pi * (x2 - phase_shift) / wavelength)
            
            # Wave packet envelope (Gaussian modulation)
            envelope1 = math.exp(-((x1 - 256) ** 2) / (2 * 40**2))
            envelope2 = math.exp(-((x2 - 256) ** 2) / (2 * 40**2))
            
            # Color by phase
            hue_shift = (x1 / 512) * 180 + t * 60
            r = int(150 + 100 * math.sin(hue_shift * math.pi / 180))
            g = int(150 + 100 * math.sin((hue_shift + 120) * math.pi / 180))
            b = int(150 + 100 * math.sin((hue_shift + 240) * math.pi / 180))
            
            color = (r, g, b)
            
            draw.line(
                [(x1, y1 * envelope1 + 64 * (1 - envelope1)),
                 (x2, y2 * envelope2 + 64 * (1 - envelope2))],
                fill=color,
                width=2
            )
        
        draw.text((10, 10), "Photon: Plane Wave + Gaussian Envelope", fill=(100, 200, 255))
        draw.text((10, 110), f"Propagation phase: {int(t*100)}%", fill=(150, 150, 150))
        
        return img


class GalaxyRotationAnimation(AnimationTemplate):
    """Animate galaxy spiral arms rotating through space"""
    
    def __init__(self):
        super().__init__(
            "Galaxy Rotation",
            "Matter flows inward along spiral direction—that inward flow CREATES the spin"
        )
    
    def generate_frames(self, t):
        img = Image.new('RGB', (256, 256), color=(20, 20, 25))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        cx, cy = 128, 128
        
        # Rotation angle
        rotation = t * 2 * math.pi * 0.5  # 0.5 revolution per cycle
        
        # Fixed pitch angle for stable spiral shape
        pitch_angle = 12
        k = math.tan(math.radians(pitch_angle))
        
        # Draw spiral arms (typically 2 for galaxies)
        num_arms = 2
        
        for arm_num in range(num_arms):
            arm_rotation = rotation + (arm_num * 2 * math.pi / num_arms)
            
            # Generate spiral points
            for theta in np.linspace(0, 3 * math.pi, 100):
                r = 10 * math.exp(k * theta)
                
                # Apply rotation (negate to get counterclockwise in visual space)
                final_angle = theta - arm_rotation
                
                x = cx + r * math.cos(final_angle)
                y = cy + r * math.sin(final_angle)
                
                # Density wave enhancement (brighter on spiral)
                density = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(theta * 4))
                
                color_val = int(200 * density)
                
                if 0 <= x < 256 and 0 <= y < 256:
                    draw.ellipse([(x-1, y-1), (x+1, y+1)], 
                               fill=(color_val, color_val // 2, color_val // 4))
        
        # Galactic center
        draw.ellipse([(cx-5, cy-5), (cx+5, cy+5)], fill=(255, 200, 100))
        
        draw.text((10, 10), "Galaxy: Rotating with Correct Direction", fill=(100, 200, 255))
        draw.text((10, 230), f"Rotation: {int(t*360)}°", fill=(150, 150, 150))
        
        return img


class ConsciousnessNetworkAnimation(AnimationTemplate):
    """Animate consciousness as oscillating neural network activation"""
    
    def __init__(self):
        super().__init__(
            "Consciousness Network",
            "7-node network showing synaptic activation and information flow"
        )
    
    def generate_frames(self, t):
        img = Image.new('RGB', (256, 256), color=(20, 20, 25))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        cx, cy = 128, 128
        node_radius = 60
        num_nodes = 7
        
        # Node positions
        nodes = []
        for i in range(num_nodes):
            angle = (2 * math.pi * i) / num_nodes
            x = cx + node_radius * math.cos(angle)
            y = cy + node_radius * math.sin(angle)
            nodes.append((x, y))
        
        # ━━━ Draw connections with activation flow ━━━
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                x1, y1 = nodes[i]
                x2, y2 = nodes[j]
                
                # Distance between nodes
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # Activation wave traveling along connection
                wave_pos = (t * 2) % 1.0  # 0-1 along the edge
                wave_x = x1 + (x2 - x1) * wave_pos
                wave_y = y1 + (y2 - y1) * wave_pos
                
                # Connection dimness (quiet baseline)
                draw.line([(x1, y1), (x2, y2)], fill=(60, 60, 80), width=1)
                
                # Activation dot
                brightness = int(150 * (0.5 + 0.5 * math.sin(wave_pos * math.pi)))
                draw.ellipse(
                    [(wave_x - 2, wave_y - 2), (wave_x + 2, wave_y + 2)],
                    fill=(100, brightness, 255)
                )
        
        # ━━━ Draw nodes with activation ━━━
        for i, (x, y) in enumerate(nodes):
            # Local activation at this node
            node_activation = 0.5 + 0.5 * math.sin(2 * math.pi * (t + i / num_nodes))
            
            node_brightness = int(100 + 155 * node_activation)
            
            # Node circle
            draw.ellipse(
                [(x - 8, y - 8), (x + 8, y + 8)],
                fill=(100, node_brightness, 255),
                outline=(150, 200, 255)
            )
            
            # Node label
            draw.text((x - 5, y - 15), f"N{i}", fill=(150, 200, 255))
        
        draw.text((10, 10), "Consciousness: Neural Network Activation", fill=(100, 200, 255))
        draw.text((10, 240), f"Synchronization: {int(t*100)}%", fill=(150, 150, 150))
        
        return img


class TimelineAnimation(AnimationTemplate):
    """Animate history unfolding through time"""
    
    def __init__(self):
        super().__init__(
            "Timeline",
            "Historical progression from initial condition through gates"
        )
    
    def generate_frames(self, t):
        img = Image.new('RGB', (512, 128), color=(20, 20, 25))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Timeline stages (simplified)
        stages = [
            ("Initial\nDiffusion", 0, (255, 100, 100)),
            ("Photon\nField", 100, (255, 200, 100)),
            ("Spiral\nFormation", 200, (100, 200, 255)),
            ("Matter\nCrystallizes", 300, (100, 255, 100)),
            ("Life\nEmerges", 400, (200, 100, 255)),
        ]
        
        # Current position in timeline
        current_pos = t * 500
        
        # Draw stages
        for name, x, color in stages:
            # Stage marker
            draw.ellipse([(x-6, 60-6), (x+6, 60+6)], fill=color)
            draw.text((x-20, 75), name, fill=color)
            
            # Progress line from start to current position
            if x <= current_pos:
                progress = min(1.0, (current_pos - x) / 50)
                draw.line([(x, 60), (min(x + 50, current_pos), 60)], 
                         fill=color, width=3)
        
        # Current position marker (bright)
        draw.ellipse(
            [(current_pos - 8, 52), (current_pos + 8, 68)],
            fill=(255, 255, 255),
            outline=(100, 200, 255)
        )
        
        draw.text((10, 10), "Timeline: Reality Unfolding Through Time", fill=(100, 200, 255))
        
        return img


# ═══════════════════════════════════════════════════════════════════════════
# COLLECTION OF ALL WIKI ANIMATIONS
# ═══════════════════════════════════════════════════════════════════════════

class WikiAnimationLibrary:
    """Generate all wiki concept animations"""
    
    templates = [
        ElectronOrbitalAnimation(),
        PhotonWaveAnimation(),
        GalaxyRotationAnimation(),
        ConsciousnessNetworkAnimation(),
        TimelineAnimation(),
    ]
    
    @classmethod
    def generate_all(cls):
        """Generate all animations and save"""
        results = []
        
        for template in cls.templates:
            print(f"📺 Animating: {template.name}")
            print(f"   Description: {template.description}")
            
            # Generate frames
            template.create_animation()
            
            # Save
            filename = f"wiki_animated_{template.name.lower().replace(' ', '_')}.gif"
            template.save_gif(filename)
            
            results.append({
                "name": template.name,
                "description": template.description,
                "filename": filename,
                "frames": len(template.frames),
                "duration_ms": len(template.frames) * 100
            })
            
            print(f"   ✓ Saved: {filename}\n")
        
        return results


# ═══════════════════════════════════════════════════════════════════════════
# HTML5 CANVAS ANIMATION TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════

HTML_CANVAS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>UFM Wiki Animations</title>
    <style>
        body {{
            background: #14141f;
            color: #ccccdd;
            font-family: monospace;
            padding: 20px;
        }}
        .animation-container {{
            margin: 20px 0;
            padding: 15px;
            border-left: 3px solid #2196F3;
            background: rgba(33, 150, 243, 0.05);
        }}
        canvas {{
            border: 1px solid #444;
            background: #14141f;
            display: block;
            margin: 10px 0;
        }}
        .controls {{
            margin: 10px 0;
        }}
        input[type="range"] {{
            width: 300px;
        }}
        .label {{
            font-weight: bold;
            color: #64b5f6;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h1>🌌 UFM Wiki Animations</h1>
    <p>All visualizations show temporal evolution through moments in time</p>
    
    {animation_divs}
    
    <script>
    // Animation framework
    class AnimationController {{
        constructor(canvasId, drawFunction) {{
            this.canvas = document.getElementById(canvasId);
            this.ctx = this.canvas.getContext('2d');
            this.drawFunction = drawFunction;
            this.t = 0;
            this.isPlaying = true;
            this.animate();
        }}
        
        animate() {{
            this.drawFunction(this.ctx, this.t);
            
            if (this.isPlaying) {{
                this.t += 0.01;
                if (this.t > 1) this.t = 0;
            }}
            
            requestAnimationFrame(() => this.animate());
        }}
        
        setTime(t) {{
            this.t = Math.max(0, Math.min(1, t));
        }}
        
        togglePlay() {{
            this.isPlaying = !this.isPlaying;
        }}
    }}
    
    // Initialize all animations
    window.addEventListener('load', () => {{
        // Each animation will be initialized here
        console.log('UFM Wiki Animations Loaded');
    }});
    </script>
</body>
</html>
"""


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  WIKI ANIMATION FRAMEWORK - Generate All Temporal Visuals ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # Generate all animations
    results = WikiAnimationLibrary.generate_all()
    
    # Summary
    print("\n" + "="*60)
    print("✨ WIKI ANIMATION GENERATION COMPLETE")
    print("="*60 + "\n")
    
    print("Generated Animations:")
    for result in results:
        print(f"  • {result['name']}")
        print(f"    → {result['description']}")
        print(f"    → File: {result['filename']}")
        print(f"    → Duration: {result['duration_ms']}ms ({result['frames']} frames)\n")
    
    print("\nNext Steps:")
    print("  1. Replace static wiki images with .gif animations")
    print("  2. Add HTML5 canvas versions for interactive scrubbing")
    print("  3. Create time-slider for each visualization")
    print("  4. Add phase/state indicators")
    print("  5. Document what's happening at each time moment\n")
    
    print("Principle: Everything in wiki is a PROCESS through time")
    print("           Static images hide the temporal dimension")
    print("           Animation reveals the TRUE dynamics")
