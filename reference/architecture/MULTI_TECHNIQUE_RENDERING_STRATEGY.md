# Multi-Technique Rendering in Unified Container

## Strategy: Multiple Algorithms, Same Problem, One Container

**Problem**: Visualize molecular fields (O, H, C, N) with element identity + bonding clarity

**Container**: `FieldGradientRenderer` (universal field renderer)

**Approach**: Implement techniques solving same problem through shared interface

```python
renderer.render_field_2d(
    grid,
    technique="isosurface",      # Swap technique, same container
    # OR: technique="hybrid"
    # OR: technique="marching_squares"
    # OR: technique="multi_layer"
    # etc.
)
```

---

## Candidate Techniques (Priority Order)

### 1. **HYBRID** (Already Implemented) ✓
- Sharp cores (threshold=0.75) + Fuzzy halos (outer field with 0.4× opacity)
- **Result**: Molecular centers crisp, bonding regions visible
- **Quality**: Best for clarity + context
- **Status**: ✓ IMPLEMENTED

### 2. **MULTI-LAYER ISOSURFACES** (Recommended)
Render 3-4 threshold levels simultaneously, each with slight opacity shift
```python
thresholds = [0.9, 0.7, 0.5, 0.3]  # Core to periphery
opacities = [1.0, 0.7, 0.5, 0.2]
# Each layer shows field region at that density level
```

**Visual Result**: 
- 0.9 layer: Ultra-tight molecular cores (bright, full opacity)
- 0.7 layer: Bonding zones (medium opacity)
- 0.5 layer: Field influence region (fading)
- 0.3 layer: Peripheral halo (very faint)

**Advantage**: Shows complete density gradient while maintaining molecular identity

### 3. **MARCHING SQUARES** (Professional 2D Contouring)
Extract sharp contour lines at defined threshold, render as clean outlines + filled regions
```
Instead of pixels: Extract boundary curves
- Smooth mathematical contours (not pixelated)
- Clean element separation
- Traditional scientific visualization
```

**Visual Result**:
- Red oxygen: Sharp red boundary, filled interior
- Cyan hydrogen: Sharp cyan outlines connecting to oxygen
- Bonding: Clean curve where field regions connect

**Technical**: Implement marching squares algorithm (contour extraction at isovalue)

### 4. **LAPLACIAN OF GAUSSIAN (LoG)** (Edge Detection)
Show where field gradient is strongest (boundaries between elements)
```python
gradient = np.gradient(field)  # How quickly field changes
laplacian = np.laplacian(field)  # Second derivative (edges)
# High |laplacian| = sharp field boundary
```

**Visual Result**:
- Bright lines exactly where molecular surfaces are sharpest
- Dark interior (field plateau)
- Crisp bonding zone definition

**Advantage**: Automatically detects molecular boundaries at ANY scale

### 5. **DIFFERENCE OF GAUSSIANS (DoG)** (Band-Pass Filtering)
Subtract two Gaussian blurs (different σ) to isolate bonding regions specifically
```python
fine_blur = gaussian_filter(field, sigma=20)    # Tight detail
coarse_blur = gaussian_filter(field, sigma=60)  # Loose overall
bonding_region = fine_blur - coarse_blur        # Mid-scale features
```

**Visual Result**:
- Highlights ONLY bonding interaction zones
- Suppresses pure molecular cores + peripheral halo
- Shows where molecules interact in magenta/blend colors

**Advantage**: Isolates bonding phenomena specifically

### 6. **ADAPTIVE THRESHOLD HYBRID**
Threshold varies per-element based on element type
```python
oxygen_threshold = 0.8      # Tight O cores (heavier nucleus)
hydrogen_threshold = 0.6    # Looser H (lighter, more diffuse)
carbon_threshold = 0.7      # Medium C
```

**Visual Result**:
- O: Very tight crisp cores
- H: Medium crisp cores with slight halo
- C: Balanced representation
- Each element optimal for its physics

**Advantage**: Element-aware rendering

### 7. **CONTOUR LINES + HEAT MAP** (Hybrid Approach)
Color gradient + sharp contour overlays
```python
Background: Smooth color gradient (isosurface from outside in)
Overlay: Sharp black/white contour lines at key thresholds [0.3, 0.6, 0.9]
Result: Both smooth field visualization + sharp structure
```

**Visual Result**:
- Continuous color field showing ALL density information
- Thin contour lines showing molecular boundaries
- Both scientists + non-specialists understand it

### 8. **DIRECTIONAL FIELD RENDERING** (Vector Field)
Show field gradient direction + magnitude (bonding directionality)
```python
grad_x, grad_y = np.gradient(field)
magnitude = np.sqrt(grad_x**2 + grad_y**2)
direction = np.arctan2(grad_y, grad_x)
# Draw small arrows showing gradient direction
```

**Visual Result**:
- Arrows point "away from" molecular centers
- Arrow density shows field strength
- Shows bonding pull directions
- Physics-accurate

---

## Implementation Strategy

### Phase 1: Implement Core Techniques
1. ✓ Hybrid (done)
2. Multi-layer isosurfaces (30 min)
3. Marching squares contouring (45 min)
4. Laplacian of Gaussian (20 min)

### Phase 2: Advanced Techniques
5. Difference of Gaussians (25 min)
6. Adaptive threshold (15 min)
7. Contour + heat map (20 min)

### Phase 3: Experimental
8. Directional field rendering (60 min)

### Architecture: Single `render_field_2d()` Method

```python
def render_field_2d(self, grid, technique="hybrid", **technique_params):
    """
    Unified renderer supporting all techniques
    
    Args:
        technique: "hybrid", "multi_layer", "marching_squares", 
                   "laplacian_of_gaussian", "difference_of_gaussians",
                   "adaptive_threshold", "contour_heatmap", "directional_field"
        **technique_params: Algorithm-specific parameters
    """
    
    if technique == "hybrid":
        return self._render_hybrid(grid, **technique_params)
    elif technique == "multi_layer":
        return self._render_multi_layer(grid, **technique_params)
    elif technique == "marching_squares":
        return self._render_marching_squares(grid, **technique_params)
    # ... etc for all techniques
```

All techniques:
- Accept same `grid` (element-specific dict)
- Use same element color mapping
- Apply same per-element normalization
- Output same PNG/display format
- Support both single and multi-element grids

---

## Evaluation Matrix

Rank techniques on molecular visualization criteria:

| Technique | Clarity | Bonding | Physics | Speed | Aesthetic |
|-----------|---------|---------|---------|-------|-----------|
| Isosurface | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Gaussian | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Hybrid** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Multi-layer | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Marching Squares | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| LoG | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| DoG | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Contour+HM | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Priority Implementation Order

**Tier 1 (Must Have)**:
1. Hybrid ✓
2. Multi-layer isosurfaces
3. Marching squares

**Tier 2 (Should Have)**:
4. LoG
5. Adaptive threshold

**Tier 3 (Nice to Have)**:
6. DoG
7. Contour + heat map
8. Directional field

---

## Molecular Visualization Best Practices

### From Professional Software (UCSF Chimera, PyMOL, Spartan)

1. **Multi-representation**: Show molecule from 3-4 different angle views
2. **Scale-appropriate detail**: Adjust threshold based on molecule count (more molecules = tighter threshold)
3. **Element-aware coloring**: Use standard CPK colors (C=gray, O=red, H=white, N=blue)
4. **Bonding emphasis**: Highlight bonding regions distinctly
5. **Context preservation**: Always show some field context (not 100% pure core)
6. **Interactive threshold**: Let user adjust isovalue in real-time

### Techniques Enabling These

- **Multi-layer**: Shows different density contexts simultaneously
- **Adaptive threshold**: Auto-adjusts per density region
- **DoG**: Isolated bonding regions for emphasis
- **Contour + HM**: Best of smooth + sharp
- **Hybrid**: Best current approach (sharp + halo)

---

## Implementation Roadmap

### Week 1: Core Techniques
- [ ] Add `technique` parameter to `render_field_2d()`
- [ ] Implement `_render_multi_layer()` 
- [ ] Implement `_render_marching_squares()`
- [ ] Test all 3 on 3-mol, 5-mol, 9-mol
- [ ] Compare side-by-side outputs

### Week 2: Advanced
- [ ] Implement `_render_laplacian_of_gaussian()`
- [ ] Implement `_render_adaptive_threshold()`
- [ ] Create comparison matrix (visual + computational metrics)
- [ ] Identify "best for each scenario"

### Week 3: Refinement
- [ ] Implement remaining techniques
- [ ] Batch-render all techniques for standard test cases
- [ ] Document which technique best for:
  - Single molecule clarity
  - Bonding visualization
  - Large crystal (9+ molecules)
  - Teaching/presentation

### Week 4: Optimization
- [ ] Performance profiling (which technique fastest?)
- [ ] Parameter tuning (optimal thresholds, etc.)
- [ ] Create rendering guide (when to use which technique)

---

## Example: Side-by-Side Rendering

```python
from field_gradient_visualization_system import FieldGradientRenderer

renderer = FieldGradientRenderer(resolution_level="molecule")
grid = renderer.create_field_grid(width=1200, height=1000)

# Add 3 water molecules
# ... (build grid with O, H fields)

techniques = [
    ("Isosurface", {"technique": "isosurface", "isovalue": 0.6}),
    ("Hybrid", {"technique": "hybrid", "halo_intensity": 0.4}),
    ("MultiLayer", {"technique": "multi_layer", "layer_count": 4}),
    ("MarchingSquares", {"technique": "marching_squares", "isovalue": 0.6}),
    ("LoG", {"technique": "laplacian_of_gaussian", "sigma": 30}),
]

for tech_name, params in techniques:
    fig, ax = renderer.render_field_2d(grid, title=f"Technique: {tech_name}", **params)
    fig.savefig(f"three_molecules_{tech_name}.png")
    plt.close(fig)
    print(f"✓ Saved: three_molecules_{tech_name}.png")
```

---

## Decision Ledger

**Decision**: Implement multi-technique rendering in shared container
- **Date**: 2026-04-01
- **Rationale**: Hybrid approach (sharp + halo) works well. Other techniques solve same problem differently. Multiple techniques in one container enables comparison and hybrid combinations.
- **Architecture**: Single `render_field_2d()` with `technique` parameter
- **Phase 1**: Implement Tier 1 (hybrid ✓, multi-layer, marching squares)
- **Phase 2**: Implement Tier 2 (LoG, adaptive threshold)
- **Phase 3**: Implement Tier 3 (DoG, advanced)
- **Status**: ROADMAP COMPLETE - Ready for implementation

