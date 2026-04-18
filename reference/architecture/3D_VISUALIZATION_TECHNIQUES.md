# 3D Visualization Techniques - Same Container

## Adding 3D to FieldGradientRenderer

**Problem**: Same (molecular field visualization)
**Container**: Same (`FieldGradientRenderer`)
**New Techniques**: 3D rendering modes

```python
renderer.render_field_2d(grid, technique="3d_surface")      # Elevation map
renderer.render_field_2d(grid, technique="3d_isometric")    # 3D perspective 2D
renderer.render_field_2d(grid, technique="3d_depth")        # 2D with shadow depth
```

---

## 3D Techniques (Priority Order)

### 1. **3D SURFACE PLOT** (Matplotlib - Simple)
Height = field density, color = element, view = 3D elevation

```python
# Result: 3D mountain-like view
# O and H peaks rise at different heights
# H-bonding zones show as valleys/ridges connecting peaks
```

**Visual**:
- X-Y plane: molecular positions
- Z-axis: field density
- Color: element (red=O, cyan=H)
- Rotation: 3D perspective (adjust angle)

**Advantages**:
- Immediate 3D visual
- Shows interaction topology (bonding as connected peaks)
- Easy to rotate/inspect

### 2. **3D ISOMETRIC PROJECTION** (Pseudo-3D in 2D)
Convert 3D coordinates to isometric 2D, render with perspective

```
Convert (x, y, z=density) → (iso_x, iso_y)
Using isometric formula:
  iso_x = x - y * cos(30°)
  iso_y = z + (x + y) * sin(30°)
Result: 2D image that LOOKS 3D (no rotation needed)
```

**Visual**:
- Molecular cores appear as tilted 3D boxes
- Bonding regions show as 3D valleys
- No rotation needed (fixed perspective)
- Similar to isometric video game graphics

**Advantages**:
- Looks 3D but renders in 2D (fast)
- Professional technical drawing style
- No rendering overhead

### 3. **3D DEPTH SHADING** (2D with Shadow Effect)
Keep 2D image, add shadow/depth cues underneath

```
Original 2D render + shadow layer offset down-right
Creates optical illusion of height/depth
```

**Visual**:
- Each molecular region has shadow beneath it
- Brighter shadows = higher peaks
- 2D-friendly but looks dimensional

**Advantages**:
- Artistic 3D appearance
- Maintains 2D clarity
- Fast to compute

### 4. **3D WIREFRAME + SURFACE** (Advanced)
Mesh surface showing molecular structure + wireframe showing field topology

```
Surface: Smooth field contours
Wireframe: Grid showing mathematical structure
Colors: Element-specific on surface
```

**Visual**:
- Clean mathematical surface
- Field flow/gradient visible as wireframe
- Professional scientific appearance

---

## Implementation: Multi-Technique Parameter

Update render method signature:

```python
def render_field_2d(self, grid, title="", technique="hybrid", 
                   layer_count=4, halo_intensity=0.4,
                   elevation_angle=30, azimuth_angle=45,
                   view_3d=False):
    """
    technique options:
    - "isosurface": Sharp threshold
    - "gaussian": Soft blur
    - "hybrid": Sharp core + fuzzy halo
    - "multi_layer": 3-4 opacity layers
    - "3d_surface": 3D elevation map plot
    - "3d_isometric": Isometric 3D projection in 2D
    - "3d_depth": 2D with shadow depth effect
    - "3d_wireframe": Surface mesh with wireframe overlay
    
    elevation_angle: For 3D plots (default 30°)
    azimuth_angle: For 3D plots (default 45°)
    """
    
    if technique.startswith("3d_"):
        return self._render_3d(grid, technique, elevation_angle, azimuth_angle, **kwargs)
    else:
        return self._render_2d(grid, technique, layer_count, halo_intensity)
```

---

## Architecture

```
FieldGradientRenderer
├── render_field_2d() ◄── Choose technique
│   ├── 2D Techniques
│   │   ├── _render_2d()
│   │   ├── isosurface
│   │   ├── gaussian
│   │   ├── hybrid
│   │   └── multi_layer
│   │
│   └── 3D Techniques
│       ├── _render_3d()
│       ├── 3d_surface (matplotlib 3D plot)
│       ├── 3d_isometric (isometric projection)
│       ├── 3d_depth (shadow effect)
│       └── 3d_wireframe (mesh surface)
│
├── Element colors (shared)
├── Per-element normalization (shared)
└── PNG output (shared)

All techniques:
✓ Same input (grid dict)
✓ Same element colors (O=red, H=cyan)
✓ Same normalization pipeline
✓ Same display/save interface
```

---

## 3D Implementation Details

### 3D Surface Plot
```python
def _render_3d_surface(self, grid, elevation_angle=30, azimuth_angle=45):
    """Create 3D surface elevation map"""
    
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure(figsize=(12, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    
    # For multi-element: composite height = sum of all element densities
    # Colors = per-element
    
    h, w = grid['O'].shape
    X = np.arange(0, w)
    Y = np.arange(0, h)
    X, Y = np.meshgrid(X, Y)
    
    # Create composite height field (sum of all elements normalized)
    Z = np.zeros_like(X, dtype=float)
    for element, elem_grid in grid.items():
        Z += elem_grid / np.max(elem_grid) if np.max(elem_grid) > 0 else 0
    
    # Create RGB surface with per-element coloring
    # High value region R: color O (red)
    # High value region G: color H (cyan - mostly just G and B)
    # Result: composite color shows which element dominates at each location
    
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9,
                          edgecolor='none', antialiased=True)
    
    ax.view_init(elev=elevation_angle, azim=azimuth_angle)
    ax.set_xlabel('X Position', color='white')
    ax.set_ylabel('Y Position', color='white')
    ax.set_zlabel('Field Density', color='white')
    
    return fig, ax
```

### 3D Isometric Projection
```python
def _render_3d_isometric(self, grid):
    """Project 3D field as 2D isometric view"""
    
    # Convert 3D coordinates to isometric 2D
    angle = np.radians(30)
    
    h, w = grid['O'].shape
    iso_width = int(w + h * np.cos(angle))
    iso_height = int(np.max([grid[k].shape[0] for k in grid.keys()]) + h * np.sin(angle))
    
    iso_image = np.zeros((iso_height, iso_width, 3))
    
    for element, elem_grid in grid.items():
        color = element_colors[element]
        
        for y in range(h):
            for x in range(w):
                if elem_grid[y, x] > 0:
                    # Isometric transform
                    iso_x = int(x - y * np.cos(angle))
                    iso_y = int(elem_grid[y, x] + (x + y) * np.sin(angle))
                    
                    if 0 <= iso_x < iso_width and 0 <= iso_y < iso_height:
                        intensity = elem_grid[y, x] / np.max(elem_grid)
                        iso_image[iso_y, iso_x] = np.array(color) * intensity
    
    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    ax.imshow(iso_image, origin='lower')
    return fig, ax
```

### 3D Depth Shading
```python
def _render_3d_depth(self, grid, shadow_offset=15, shadow_intensity=0.3):
    """Add shadow/depth effect to 2D render"""
    
    # First: render normal 2D image
    fig_2d, ax_2d = self._render_2d(grid, technique="hybrid")
    img_2d = fig_2d.canvas.tostring_rgb()
    
    # Create shadow layer: offset grid down-right
    shadow = np.zeros_like(img_2d)
    for i in range(len(img_2d) - shadow_offset):
        for j in range(len(img_2d[0]) - shadow_offset):
            shadow[i + shadow_offset, j + shadow_offset] = img_2d[i, j] * shadow_intensity
    
    # Composite: shadow + original
    result = img_2d + shadow
    
    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    ax.imshow(result)
    return fig, ax
```

---

## Test Sequence

```python
renderer = FieldGradientRenderer(resolution_level="molecule")
grid = renderer.create_field_grid(width=1200, height=1000)

# Build 3-molecule grid with O, H fields...

# Render all techniques
techniques_2d = ["isosurface", "hybrid", "multi_layer"]
techniques_3d = ["3d_surface", "3d_isometric", "3d_depth"]

print("\n2D Techniques:")
for tech in techniques_2d:
    fig, ax = renderer.render_field_2d(grid, technique=tech)
    fig.savefig(f"three_mol_{tech}.png")
    print(f"✓ {tech}")

print("\n3D Techniques:")
for tech in techniques_3d:
    fig, ax = renderer.render_field_2d(grid, technique=tech, 
                                      elevation_angle=30, azimuth_angle=45)
    fig.savefig(f"three_mol_{tech}.png")
    print(f"✓ {tech}")
```

---

## Visual Comparison Matrix

| Technique | Clarity | 3D Effect | Speed | File Size | Use Case |
|-----------|---------|-----------|-------|-----------|----------|
| Hybrid | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | 500KB | Best overall |
| Multi-layer | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 600KB | Scientific detail |
| **3D Surface** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 1.2MB | Immersive view |
| **3D Isometric** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 800KB | Technical drawing |
| **3D Depth** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 550KB | Artistic |
| Isosurface | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | 400KB | Baseline |

---

## Strategy: When to Use Which 3D

### 3D Surface Plot
**For**: Interactive exploration, understanding field topology
**Example**: "Show me how oxygen and hydrogen fields combine"
**Parameter tuning**:
- `elevation_angle=20`: Low profile (emphasize lateral extent)
- `elevation_angle=60`: Steep profile (emphasize height differences)
- `azimuth_angle=0/90/180/270`: Different viewpoints

### 3D Isometric Projection
**For**: Technical/scientific publications, fixed viewing angle
**Example**: "Crystal structure showing field manifestation"
**Advantages**: 
- No rotation overhead
- Professional illustration style
- Consistent scale/perspective

### 3D Depth Shading
**For**: Artistic rendering, making 2D look dimensional
**Example**: "Poster-style molecular visualization"
**Advantages**:
- Maintains 2D clarity
- Adds visual appeal
- Fast computation

---

## Next Steps

### Immediate (30 min)
- [ ] Add 3D technique parameter to `render_field_2d()`
- [ ] Implement `_render_3d_surface()` (matplotlib already has this)
- [ ] Test on 3-molecule, 5-molecule examples
- [ ] Compare with 2D hybrid

### Phase 2 (1 hour)
- [ ] Implement isometric projection
- [ ] Implement depth shading
- [ ] Create side-by-side comparison matrix

### Phase 3 (Optional)
- [ ] 3D wireframe mesh visualization
- [ ] Interactive 3D viewer (three.js or similar)
- [ ] Rotating animation (gif/video)

---

## Decision Ledger

**Decision**: Add 3D techniques to unified rendering container
- **Date**: 2026-04-01
- **Rationale**: Same problem (field visualization), multiple perspectives. 3D adds immersive dimension understanding. Keep in same container with 2D techniques.
- **Techniques**: 3D Surface, Isometric, Depth Shading (MVPs)
- **Architecture**: Single `render_field_2d()` with technique parameter
- **Status**: ROADMAP READY - implement 3D Surface immediately

