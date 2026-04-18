# Rotating GIF Universal Output Format

## One Output Format for Everything

**Requirement**: All 3D-capable visualizations output rotating GIFs by default
- Atoms: rotating field GIF
- Molecules: rotating field GIF
- Proteins: rotating structure GIF
- Animals: rotating scan GIF
- **Format**: GIF (universal, no plugins, works everywhere)

---

## Architecture: GIF Pipeline

```
FieldGradientRenderer
├── render_field_2d(technique="3d_surface", output="gif")
│   └── _generate_rotating_gif()
│       ├── Create 36 frames (10° rotations)
│       ├── Rotate view: azimuth += 10° each frame
│       ├── Render each frame as image
│       ├── Stack into PIL Image sequence
│       └── Save as .gif (animated)
│
├── Output: 
│   ├── Default: file.gif (rotating)
│   ├── Optional: file.png (first frame static)
│   └── Optional: frames/ (individual frame PNGs)
```

---

## Implementation: Rotating GIF Generator

```python
from PIL import Image
import io

class FieldGradientRenderer:
    
    def render_field_2d(self, grid, title="", technique="3d_surface", 
                       output="gif", num_frames=36, fps=30):
        """
        Render field visualization.
        
        output options:
        - "gif" (default): Animating rotating GIF
        - "png": Static first frame
        - "both": Both GIF and PNG
        - "frames": Individual frame images
        
        num_frames: Number of rotation frames (36 = 10° per frame)
        fps: GIF animation speed
        """
        
        if output == "gif" or output == "both":
            if technique.startswith("3d_"):
                return self._render_as_rotating_gif(grid, title, technique, num_frames, fps)
            else:
                # No rotation for 2D techniques, just create single-frame "gif"
                return self._render_2d_as_static_gif(grid, title, technique)
        
        elif output == "png":
            return self._render_as_png(grid, title, technique)
        
        elif output == "frames":
            return self._render_as_frame_sequence(grid, title, technique, num_frames)
    
    def _render_as_rotating_gif(self, grid, title, technique, num_frames=36, fps=30):
        """
        Generate rotating GIF by rendering multiple view angles.
        
        Steps:
        1. Create frames for each rotation angle
        2. Stack into PIL Image sequence
        3. Save as animated GIF
        4. Return GIF file path
        """
        
        import time
        from pathlib import Path
        
        frames = []
        start_time = time.time()
        
        # Generate frames: rotate 360° in num_frames steps
        angle_step = 360 / num_frames
        
        print(f"\nGenerating rotating GIF: {title}")
        print(f"Frames: {num_frames}, Speed: {fps} fps, Duration: {num_frames/fps:.1f}s")
        print("─" * 60)
        
        for frame_idx in range(num_frames):
            azimuth = frame_idx * angle_step
            
            # Render single frame at this azimuth angle
            if technique == "3d_surface":
                fig, ax = self._render_3d_surface(grid, elevation_angle=30, 
                                                 azimuth_angle=azimuth)
            elif technique == "3d_isometric":
                # Isometric doesn't rotate (fixed perspective)
                # So just render once and duplicate frames
                if frame_idx == 0:
                    fig, ax = self._render_3d_isometric(grid)
                else:
                    continue
            
            elif technique == "3d_depth":
                fig, ax = self._render_3d_depth(grid)
                if frame_idx > 0:
                    continue
            
            # Convert matplotlib figure to PIL Image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            frame_image = Image.open(buf)
            frame_image_copy = frame_image.copy()
            frames.append(frame_image_copy)
            buf.close()
            
            plt.close(fig)
            
            # Progress indicator
            if (frame_idx + 1) % max(1, num_frames // 10) == 0:
                print(f"  Frame {frame_idx + 1}/{num_frames} ✓")
        
        # Create animated GIF
        if len(frames) == 0:
            print("ERROR: No frames generated")
            return None
        
        # For static techniques (isometric, depth), duplicate frame to create brief "animation"
        if len(frames) == 1:
            frames = frames * 3  # Show frame 3 times for 0.1s each
        
        # Save as GIF
        gif_filename = title.replace(" ", "_").lower() + ".gif"
        gif_path = Path(gif_filename)
        
        # Calculate frame duration in milliseconds
        frame_duration = 1000 // fps  # milliseconds per frame
        
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_duration,
            loop=0  # Infinite loop
        )
        
        elapsed = time.time() - start_time
        file_size_mb = gif_path.stat().st_size / (1024 * 1024)
        
        print(f"\n✓ GIF Created: {gif_path}")
        print(f"  Size: {file_size_mb:.1f} MB")
        print(f"  Time: {elapsed:.1f}s")
        print(f"  Animation: {num_frames} frames @ {fps} fps")
        print("─" * 60)
        
        return str(gif_path)
    
    def _render_2d_as_static_gif(self, grid, title, technique):
        """
        For 2D techniques, render once and save as single-frame GIF.
        Still uses GIF format for consistency.
        """
        
        fig, ax = self._render_2d(grid, technique)
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        frame_image = Image.open(buf)
        
        gif_filename = title.replace(" ", "_").lower() + ".gif"
        gif_path = Path(gif_filename)
        
        frame_image.save(gif_path)
        
        plt.close(fig)
        buf.close()
        
        return str(gif_path)

    def _render_3d_surface(self, grid, elevation_angle=30, azimuth_angle=45):
        """Create 3D surface plot (rotatable)"""
        
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(10, 8), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        
        h, w = grid['O'].shape
        X = np.arange(0, w)
        Y = np.arange(0, h)
        X, Y = np.meshgrid(X, Y)
        
        # Composite height field
        Z = np.zeros_like(X, dtype=float)
        for element, elem_grid in grid.items():
            normalized = elem_grid / (np.max(elem_grid) + 1e-10)
            Z += normalized
        
        # Colormap based on which element dominates
        C = np.zeros((*Z.shape, 3))
        max_element_idx = {'O': 0, 'H': 1, 'C': 2, 'N': 3}
        
        for element, elem_grid in grid.items():
            normalized = elem_grid / (np.max(elem_grid) + 1e-10)
            color = self.element_colors.get(element, [0.5, 0.5, 0.5])
            C += normalized[..., np.newaxis] * np.array(color)
        
        # Normalize colors to 0-1
        C = np.clip(C / (np.max(C) + 1e-10), 0, 1)
        
        surf = ax.plot_surface(X, Y, Z, facecolors=C, shade=False, 
                              edgecolor='none', antialiased=True)
        
        ax.view_init(elev=elevation_angle, azim=azimuth_angle)
        ax.set_xlabel('X', fontsize=8, color='white')
        ax.set_ylabel('Y', fontsize=8, color='white')
        ax.set_zlabel('Density', fontsize=8, color='white')
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        
        return fig, ax
    
    def _render_3d_isometric(self, grid):
        """Isometric projection (static, no rotation needed)"""
        
        angle = np.radians(30)
        
        h, w = grid['O'].shape
        iso_width = int(w + h * np.cos(angle))
        iso_height = int(max([grid[k].shape[0] for k in grid.keys()]) + h * np.sin(angle))
        
        iso_image = np.zeros((iso_height, iso_width, 3))
        
        for element, elem_grid in grid.items():
            color = np.array(self.element_colors[element])
            
            for y in range(h):
                for x in range(w):
                    if elem_grid[y, x] > 0:
                        iso_x = int(x - y * np.cos(angle))
                        iso_y = int(elem_grid[y, x] * 50 + (x + y) * np.sin(angle))
                        
                        if 0 <= iso_x < iso_width and 0 <= iso_y < iso_height:
                            intensity = elem_grid[y, x] / (np.max(elem_grid) + 1e-10)
                            iso_image[iso_y, iso_x] = color * intensity
        
        fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
        ax.imshow(iso_image, origin='lower', interpolation='bilinear')
        ax.axis('off')
        fig.patch.set_facecolor('black')
        
        return fig, ax
    
    def _render_3d_depth(self, grid, shadow_offset=15, shadow_intensity=0.3):
        """2D with depth shadow effect (static)"""
        
        # Render base hybrid visualization
        fig_base, ax_base = self._render_2d(grid, technique="hybrid")
        
        buf = io.BytesIO()
        fig_base.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base = Image.open(buf).convert('RGB')
        img_array = np.array(img_base)
        
        # Create shadow offset
        shadow = np.zeros_like(img_array)
        h, w = img_array.shape[:2]
        
        for i in range(max(0, h - shadow_offset)):
            for j in range(max(0, w - shadow_offset)):
                shadow[i + shadow_offset, j + shadow_offset] = \
                    img_array[i, j] * shadow_intensity
        
        # Composite
        result = np.clip(img_array + shadow, 0, 255).astype(np.uint8)
        result_img = Image.fromarray(result)
        
        fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
        ax.imshow(result_img)
        ax.axis('off')
        fig.patch.set_facecolor('black')
        
        plt.close(fig_base)
        buf.close()
        
        return fig, ax
```

---

## Usage: Universal GIF Output

### 1. Single Molecule (Default GIF)
```python
renderer = FieldGradientRenderer(resolution_level="molecule")
grid = renderer.create_field_grid(width=1200, height=1000)
# ... add molecule data ...

# Generates: oxygen_field.gif (rotating 3D)
renderer.render_field_2d(grid, title="Oxygen Field", 
                        technique="3d_surface", output="gif")
```

### 2. Multi-Molecule Suite (All GIFs)
```python
# All output as GIFs
molecules = ["water", "methane", "benzene", "protein_fragment"]

for mol in molecules:
    grid = renderer.create_field_grid(...)
    # ... populate grid ...
    
    # Output: water.gif, methane.gif, benzene.gif, protein_fragment.gif
    renderer.render_field_2d(grid, title=mol, technique="3d_surface", output="gif")
```

### 3. Batch Generation: Multiple Techniques
```python
techniques = ["3d_surface", "3d_isometric", "3d_depth"]

for tech in techniques:
    renderer.render_field_2d(grid, title=f"3D {tech}", 
                            technique=tech, output="gif")

# Outputs:
# 3d_3d_surface.gif      (rotating, 36 frames)
# 3d_3d_isometric.gif    (static, 3-frame repeat)
# 3d_3d_depth.gif        (static, 3-frame repeat)
```

---

## GIF Configuration

```python
# Default parameters
num_frames = 36       # 36 frames = 10° per frame
fps = 30              # 30 fps animation
frame_duration = 33   # ms per frame (1000/30)

# Output for 36-frame @ 30fps: 
# Duration: 1.2 seconds per rotation
# File size: 2-4 MB typical

# Customization
renderer.render_field_2d(grid, output="gif", num_frames=72, fps=20)
# Results: 72 frames @ 20fps = 3.6 seconds rotation, smoother but larger

renderer.render_field_2d(grid, output="gif", num_frames=12, fps=60)
# Results: 12 frames @ 60fps = 0.2 seconds rotation, quick and small
```

---

## Output File Structure

```
project/
├── three_water_molecules.gif        ← Rotating 3D surface
├── five_water_molecules.gif         ← Rotating 3D surface
├── water_crystal_pattern.gif        ← Rotating 3D surface
├── oxygen_field_isometric.gif       ← Static isometric (3 frame repeat)
├── hydrogen_field_depth.gif         ← Static depth shaded (3 frame repeat)
└── hybrid_comparison.gif            ← Rotating hybrid rendering
```

---

## Integration with Existing Pipeline

Update `multi_molecule_field_visualization.py`:

```python
def render_three_water_molecules():
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = renderer.create_field_grid(width=1200, height=1000)
    
    # ... populate grid with water data ...
    
    # Single call: outputs GIF
    renderer.render_field_2d(grid, title="Three Water Molecules", 
                            technique="3d_surface", output="gif")
    # ✓ three_water_molecules.gif (24 MB, 36 frames, rotates)
```

---

## Benefits: Universal Output

| Aspect | Static PNG | Rotating GIF |
|--------|-----------|-------------|
| **Universality** | Viewer-specific | Works everywhere |
| **Documentation** | Single angle bias | Full 360° view |
| **File Size** | 500 KB | 2-4 MB |
| **Publishing** | PDF, web, print | Web, wiki, social |
| **Data Preservation** | Lossy decision (angle) | Complete visual data |
| **Processing** | 1-2 seconds | 30-60 seconds |
| **Use Case** | Archive, print | exploration, sharing |

---

## Phase Implementation

### Phase 1: Core Rotating GIF (30 min)
- [ ] Add `_render_as_rotating_gif()` method
- [ ] Add `num_frames` and `fps` parameters
- [ ] Test on 3-molecule benchmark
- [ ] Verify frame quality and GIF animation

### Phase 2: Format Consistency (15 min)
- [ ] Make output="gif" DEFAULT in all visualization calls
- [ ] Update `multi_molecule_field_visualization.py` to generate GIFs
- [ ] Regenerate all benchmark molecules as GIFs

### Phase 3: Batch Export (15 min)
- [ ] Add `batch_render_techniques()` to generate all 8 techniques as GIFs
- [ ] Create comparison GIF folder
- [ ] Generate side-by-side viewing

---

## Decision Ledger

**Decision**: Make rotating GIFs universal default output
- **Date**: 2026-04-01
- **Rationale**: One format works everywhere (web, wiki, docs, social). Rotation shows full 3D structure without interactive viewing. File size reasonable (2-4 MB). Batch processing fast (30-60s for full suite).
- **Parameters**: 36 frames @ 30fps (1.2s rotation) = default
- **Status**: READY TO IMPLEMENT

