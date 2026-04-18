# Rotating/Animated Patterns in Unified Container

## Every Technique That Can Animate

**Principle**: Any visualization parameter that can vary over frames can become an animation

```python
# Current architecture
renderer.render_field_2d(grid, 
                        technique="hybrid",      # Can we vary this?
                        isovalue=0.5,           # Can we vary this?
                        azimuth_angle=45,       # Can we vary this?
                        threshold_focus=None,   # NEW: can we vary?
                        output="gif",           # NEW: output type
                        num_frames=36)          # rotation frames
```

**Pattern**: Any parameter that varies → animation frame chain

---

## 7 Animation Patterns (Same Container)

### 1. **AZIMUTH ROTATION** (Already Implemented)
**Parameter varies**: `azimuth_angle`: 0° → 360°

```python
# 36 frames, each frame:
azimuth = frame_idx * (360 / 36)  # 0°, 10°, 20°, ..., 350°

# Works for:
- 3d_surface ✓ (3D elevation rotating)
- 3d_isometric (static—no benefit)
- 3d_depth (static—no benefit)

# Result GIF: 1.2s rotation at 30fps
```

---

### 2. **THRESHOLD ANIMATION** (Reveal/Collapse)
**Parameter varies**: `isovalue`: 0.9 → 0.1 → 0.9

Shows field structure progressively

```python
# 36 frames across threshold range
frame_threshold = 0.1 + abs(frame_idx - 18) / 18 * 0.8
# Frame 0: high threshold (tight core)
# Frame 18: low threshold (loose periphery)
# Frame 36: high threshold again (loop)

# Visual: Molecular core "pulses" in/out
# Like watching field density build from core outward

# Works for:
- isosurface (core explodes outward)
- hybrid (core/halo pulse)
- multi_layer (layers appear/disappear)
- gaussian (density waves)

# Result GIF: "breathing" molecule effect
```

**Decision**: Show spatial extent of field (how far does influence reach?)

---

### 3. **ELEMENT FOCUS CYCLING** (Highlight Rotation)
**Parameter varies**: `element_focus`: O → H → C → N → O

For multi-element grids, emphasize one element at a time

```python
elements = ["O", "H", "C", "N"]
frame_element_idx = frame_idx % len(elements)
focus_element = elements[frame_element_idx]

# Rendering logic:
for element, grid in grid_dict.items():
    if element == focus_element:
        intensity = 1.0  # Bright
    else:
        intensity = 0.2  # Dimmed

# Visual: Each element "pulses" in sequence
# Viewer sees: "O is here, now H is here, now C..."

# Works for:
- hybrid (element by element)
- multi_layer (highlight each layer)
- isosurface (element contribution visible)

# Result GIF: Elements take turns showing up
```

**Decision**: Show spatial separation of element types (where is each atom?)

---

### 4. **LAYER CYCLING** (Multi-Layer Animation)
**Parameter varies**: `active_layer`: 0 → 1 → 2 → 3 → 0

For multi-layer technique, show one layer at a time

```python
layers = [0, 1, 2, 3]  # For layer_count=4
frame_active_layer = frame_idx % len(layers)

# Rendering: only show specified layer, rest transparent

# Visual: Like peeling an onion
# "Core is here" → "first ring here" → "second ring here" → "outer shell"

# Works for:
- multi_layer (designed for this)
- hybrid (core vs halo)

# Result GIF: "Onion peeling" effect
```

**Decision**: Show layer structure (how many density shells?)

---

### 5. **ROTATION + SCALE** (Spinning + Zoom)
**Parameter varies**: `azimuth_angle` AND `view_scale`

Combine two parameters: rotate + zoom in/out

```python
# Each frame:
azimuth = (frame_idx / num_frames) * 360
scale = 0.5 + 0.5 * abs(np.sin(frame_idx / num_frames * np.pi))
# Scale: 0.5x (zoomed out) → 1.0x (normal) → 0.5x (round trip)

# Visual: Spinning molecule grows/shrinks
# Like watching a molecular orbit

# Works for:
- 3d_surface (rotate + scale together)
- 3d_isometric (scale only, no rotation)
- All 2D techniques (scale via crop/window)

# Result GIF: "Orbital dance" animation
```

**Decision**: Show scale/context (how big is this structure?)

---

### 6. **TIMING/EVOLUTION** (Field Evolution)
**Parameter varies**: `time_step`: 0 → T

Simulate time-dependent behavior (e.g., oscillation, diffusion)

```python
# Each frame represents different time state
# For molecule: simulate H-bonding oscillation

time_param = (frame_idx / num_frames) * 2 * np.pi

# Adjust grid values based on time (physics simulation)
for element in grid:
    grid[element] *= (1.0 + 0.3 * np.sin(time_param))
    # Intensity oscillates: 0.7x → 1.3x

# Visual: Molecular field "breathes" in realistic way
# Like watching electrons orbit, or bonds vibrate

# Works for:
- Any technique (apply time-dependent modulation)
- hybrid (core/halo oscillation)
- multi_layer (layers pulsing)
- gaussian (smooth breathing motion)

# Result GIF: "Living" molecule animation
```

**Decision**: Show temporal dynamics (how does this system change?)

---

### 7. **TECHNIQUE MORPHING** (Style Transition)
**Parameter varies**: `technique`: hybrid → isosurface → multi_layer → hybrid

Smoothly transition between rendering styles

```python
techniques = ["hybrid", "multi_layer", "isosurface"]
frame_technique_idx = frame_idx % len(techniques)

# Interpolate between techniques over multiple frames
# e.g., frames 0-11: fade from hybrid → multi_layer
#       frames 12-23: fade from multi_layer → isosurface
#       frames 24-35: fade from isosurface → hybrid

# Visual: See same field rendered 3 different ways
# "Here's the sharp version, now the layered version, now the threshold version"

# Works for:
- All techniques (as long as output is viewable)
- Especially: hybrid, multi_layer, isosurface (visually distinct)

# Result GIF: Technique comparison carousel
```

**Decision**: Show rendering method impact (which style best reveals structure?)

---

## Implementation Matrix

| Pattern | Parameter | Frames | Rotation | Zoom | Color | Layer | Works Dir? | Visual Purpose |
|---------|-----------|--------|----------|------|-------|-------|-----------|-----------------|
| Azimuth | azimuth_angle | 36 | ✓ | ✗ | ✗ | ✗ | All 3D | Full 360° view |
| Threshold | isovalue | 36 | ✗ | ✗ | ✗ | ✗ | isosurface, hybrid, multi_layer | "Breathing" core |
| Element | element_focus | 12 (3-4 elements) | ✗ | ✗ | ✓ | ✗ | Multi-element | Element location |
| Layer | active_layer | 12 (4 layers) | ✗ | ✗ | ✗ | ✓ | multi_layer, hybrid | Onion peeling |
| Rotate+Scale | azimuth + view_scale | 36 | ✓ | ✓ | ✗ | ✗ | 3D | Orbital motion |
| Evolution | time_param | 36 | ✗ | ✗ | ✗ | ✗ | All | Living system |
| Morph | technique | 12 (techniques) | ✗ | ✗ | ✗ | ✗ | All | Technique compare |

---

## Unified Parameter Extension

Add to `render_field_2d()` signature:

```python
def render_field_2d(self, grid, title="", technique="hybrid",
                   output="gif", num_frames=36, fps=30,
                   # Existing
                   isovalue=0.5, halo_intensity=0.4, layer_count=4,
                   # NEW Animation parameters
                   animation_type="azimuth",      # Which pattern to animate
                   animation_param_range=(None, None),  # Min/max for param variation
                   element_focus=None,             # For element cycling
                   morphing_techniques=None):      # List of techniques to morph
    
    if output in ["gif", "gif_only"]:
        if animation_type == "azimuth":
            return self._animate_azimuth(grid, title, technique, num_frames, fps)
        elif animation_type == "threshold":
            return self._animate_threshold(grid, title, technique, num_frames, fps, animation_param_range)
        elif animation_type == "element":
            return self._animate_element_focus(grid, title, technique, num_frames, fps)
        elif animation_type == "layer":
            return self._animate_layer_cycling(grid, title, technique, num_frames, fps)
        elif animation_type == "rotate_scale":
            return self._animate_rotate_scale(grid, title, technique, num_frames, fps)
        elif animation_type == "evolution":
            return self._animate_evolution(grid, title, technique, num_frames, fps, animation_param_range)
        elif animation_type == "morph":
            return self._animate_technique_morph(grid, title, morphing_techniques, num_frames, fps)
```

---

## Usage Examples

### Example 1: Rotating 3D
```python
renderer.render_field_2d(grid, title="Water Molecule",
                        technique="3d_surface",
                        output="gif",
                        animation_type="azimuth",
                        num_frames=36, fps=30)
# Result: three_water_molecules.gif (spinning molecule)
```

### Example 2: Breathing Threshold
```python
renderer.render_field_2d(grid, title="Field Pulsing",
                        technique="hybrid",
                        output="gif",
                        animation_type="threshold",
                        animation_param_range=(0.2, 0.8),
                        num_frames=36, fps=20)
# Result: field_pulsing.gif (core expands/contracts)
```

### Example 3: Element Cycling
```python
renderer.render_field_2d(grid, title="Water Elements",
                        technique="isosurface",
                        output="gif",
                        animation_type="element",
                        num_frames=12)  # 12 frames / 3 elements = 4 frames each
# Result: water_elements.gif (O, H, O, H, O, H...)
```

### Example 4: Technique Carousel
```python
renderer.render_field_2d(grid, title="Rendering Methods",
                        output="gif",
                        animation_type="morph",
                        morphing_techniques=["hybrid", "multi_layer", "isosurface"],
                        num_frames=36, fps=20)
# Result: rendering_methods.gif (see all 3 techniques)
```

### Example 5: Living System
```python
renderer.render_field_2d(grid, title="Molecular Breathing",
                        technique="hybrid",
                        output="gif",
                        animation_type="evolution",
                        animation_param_range=(0.7, 1.3),  # Oscillate intensity
                        num_frames=36, fps=30)
# Result: molecular_breathing.gif (realistic oscillation)
```

---

## Decision Logic: Which Animation For What?

**Question**: What does the viewer need to understand?

1. **"What does it look like from all angles?"**
   - Use: Azimuth rotation
   - Result: GIF showing full 360° view
   - Best for: 3D techniques

2. **"What's the spatial extent of the field?"**
   - Use: Threshold animation
   - Result: GIF showing core → periphery expansion
   - Best for: isosurface, hybrid

3. **"Where is each element located?"**
   - Use: Element focus cycling
   - Result: GIF highlighting each element in turn
   - Best for: Multi-element molecules

4. **"What's the internal structure?"**
   - Use: Layer cycling
   - Result: GIF peeling layers like onion
   - Best for: multi_layer technique

5. **"How does this system behave over time?"**
   - Use: Evolution animation (time-based)
   - Result: GIF showing oscillation/breathing
   - Best for: All techniques (realistic physics)

6. **"Which rendering method is best?"**
   - Use: Technique morphing
   - Result: GIF comparing multiple rendering styles
   - Best for: Methodology comparisons, documentation

---

## Extension: Batch Animation Generation

```python
def render_field_with_all_animations(grid, base_title):
    """Generate all 7 animation styles in one call"""
    
    animations = [
        ("azimuth", {"animation_type": "azimuth"}),
        ("breathing", {"animation_type": "threshold", "animation_param_range": (0.2, 0.8)}),
        ("element", {"animation_type": "element"}),
        ("layer", {"animation_type": "layer"}),
        ("orbital", {"animation_type": "rotate_scale"}),
        ("evolution", {"animation_type": "evolution", "animation_param_range": (0.7, 1.3)}),
        ("techniques", {"animation_type": "morph", "morphing_techniques": ["hybrid", "multi_layer", "isosurface"]})
    ]
    
    results = {}
    for anim_name, anim_params in animations:
        print(f"\nGenerating: {base_title}_{anim_name}.gif")
        
        gif_path = renderer.render_field_2d(
            grid, title=f"{base_title} ({anim_name})",
            output="gif",
            num_frames=36, fps=30,
            **anim_params
        )
        results[anim_name] = gif_path
    
    return results

# Usage
gifs = render_field_with_all_animations(water_grid, "Water Molecule")
# Results:
# - Water Molecule (azimuth).gif
# - Water Molecule (breathing).gif
# - Water Molecule (element).gif
# - Water Molecule (layer).gif
# - Water Molecule (orbital).gif
# - Water Molecule (evolution).gif
# - Water Molecule (techniques).gif
```

---

## Decision Ledger

**Decision**: Identify 7 animation patterns working in unified container
- **Date**: 2026-04-01
- **Rationale**: Same container, different parameters = different animations. Every parameter variation = potential animation. All 7 patterns serve different communication goals.
- **Architecture**: Single `render_field_2d()` with `animation_type` parameter routing to `_animate_*()` methods
- **Status**: PATTERN INVENTORY COMPLETE
- **Next**: Implement highest-value patterns (azimuth✓, threshold, element, layer, evolution)

---

## Priority Implementation (Quick Wins)

**Already Have**:
- ✓ Azimuth (3D rotation) - just implemented

**Quick Add (15 min each)**:
1. Threshold animation - just vary isovalue param in frame loop
2. Element cycling - loop through element colors
3. Layer cycling - render each layer sequentially

**Medium Add (30 min)**:
4. Rotate+scale - combine azimuth with zoom viewport
5. Evolution - add time-based field modulation

**Optional**:
6. Technique morphing - blend between technique outputs (advanced)

