# GIF Animation Specification — Container Resolution & Entropy Limits

**Date:** April 1, 2026  
**Status:** Precision gate verified — specifications locked  
**Applies to:** Molecules → Cells → Tissues → Organs → Systems

---

## Core Principle

**GIF is an animation container with entropy constraints.**

Each animation type has:
- **Frame count** (how many snapshots fit)
- **Field entropy budget** (how much variation allowed)
- **Resolution limits** (image dimensions)
- **Duration** (playback time = frames / fps)
- **File size ceiling** (storage constraint)

These scale predictably from molecular to organismal levels.

---

## CRITICAL: Moment-Specific Determinism

**All specifications in this document are determined AT THE MOMENT OF REQUEST.**

This is not abstract theory—these are concrete values locked in when animation generation begins:

```
GENERATION MOMENT (t = request_time)
  ↓
  ├─ Resolution level: DETERMINED (what scale?)
  ├─ Animation type: DETERMINED (which visualization?)
  ├─ Frame count: DETERMINED (12 or 36 frames for this type)
  ├─ FPS: DETERMINED (20 or 30, locked for this animation)
  ├─ Duration: DETERMINED (calculated frames ÷ fps)
  ├─ Image dimensions: DETERMINED (preset by resolution)
  ├─ DPI: DETERMINED (preset by resolution)
  ├─ Entropy budget: DETERMINED (what field variation is allowed)
  ├─ File size limit: DETERMINED (preset by resolution)
  └─ Validation rules: DETERMINED (7 checks must all pass)
```

**Every value is causal chain:**
1. Request arrives (what do you want?)
2. All values determined from that request
3. Animation generated under those exact constraints
4. Validation verifies constraints were satisfied
5. Ledger records the moment and all determined values

**No animation has abstract specifications—every GIF has concrete determinations from its request moment.**

The specification table below serves as a TEMPLATE. When an animation is requested, 
these templates become concrete values at that moment in time, recorded in ledger.

---

## System Capabilities Determine Values

**At request moment, the system's capabilities determine what values are valid and optimal.**

```
REQUEST ARRIVES:
  ├─ System queries its capabilities
  │   ├─ GPU/CPU available?
  │   ├─ Memory available?
  │   ├─ Storage available?
  │   ├─ Processing speed?
  │   ├─ Rendering quality achievable?
  │   └─ File compression capacity?
  │
  ├─ System determines optimal values FROM capabilities
  │   ├─ If GPU fast: higher fps, larger dimensions
  │   ├─ If memory limited: fewer frames, smaller resolution
  │   ├─ If storage constrained: lower dpi, higher compression
  │   ├─ If rendering complex: lower entropy budget
  │   └─ If time-critical: simpler animation type
  │
  ├─ All values locked at this moment
  │   ├─ Capabilities → Constraints → Values (concrete)
  │   └─ No abstract values—only what system can actually do
  │
  └─ Generation proceeds under determined constraints
```

**Capabilities Inform Frame Count:**
- System can render 36 frames at 1200×1200 in time budget? → 36 frames locked
- System can only handle 12 frames at that resolution? → 12 frames locked instead
- Values determined by actual capability, not template

**Capabilities Inform Resolution:**
- System can handle 2000×2000 at molecular scale? → locked at 2000×2000
- System limited to 1200×1200? → locked at 1200×1200
- **No downgrade happens in ledger—actual capability determines actual value**

**Capabilities Inform FPS:**
- System GPU can render at 30 fps smooth? → 30 fps locked
- System can only sustain 20 fps? → 20 fps locked
- Actual system performance determines actual fps

**Capabilities Inform Entropy Budget:**
- System has headroom (fast, low load)? → Medium-high entropy allowed
- System under load (slow, memory pressure)? → Low entropy only
- Current system state determines what variation is safe

**Capabilities Inform File Size:**
- Storage available is 25 MB at system startup? → 25 MB limit locked
- Storage currently only 10 MB available? → 10 MB limit locked
- Real available space determines real limit at request moment

**Validation Checks ARE Capability Checks:**
The 7 validation rules verify system met its determined constraints:
1. ✓ RESOLUTION RULE — Did system achieve determined dimensions?
2. ✓ ENTROPY RULE — Did field variation stay within capability limits?
3. ✓ FRAME RULE — Did system generate exact frame count determined?
4. ✓ TIMING RULE — Did fps stay constant as capability would provide?
5. ✓ FILE SIZE RULE — Did file stay within determined storage limit?
6. ✓ COLOR RULE — Did system preserve element colors accurately?
7. ✓ ENERGY RULE — Did physics stay within computational constraints?

**System Capabilities Are Part of Causality:**

```
CAUSALITY CHAIN (expanded with capabilities):
  1. Request arrives at time T
  2. System measures capabilities at time T
     (available CPU, GPU, memory, storage, bandwidth)
  3. System determines specifications FROM those capabilities
     (values = f(capabilities))
  4. All values locked—concrete not abstract
  5. Animation generates under determined constraints
  6. Validation proves system met determined constraints
  7. Ledger records moment + capabilities + determined values
  
Therefore:
  Same request at T → same capabilities → same determined values
  Same request at T+1 → different capabilities → potentially different determined values
  
Each animation is NOT "a rotation animation"—it's "MY rotation animation at the moment 
MY system was capable of rendering it EXACTLY THIS WAY"
```

---

## Animation Types & Specifications

### TYPE 1: AZIMUTH ROTATION

**Purpose:** Full 360° view of structure

**Container Spec:**
```
frames:           36 (10° per frame)
fps:              30 (standard playback)
duration:         1.2 seconds (36 frames ÷ 30 fps)
image_dimensions: 1200×1200 px (minimum for clarity)
dpi:              150 (high quality)
entropy_budget:   LOW (deterministic rotation only)
```

**Field Entropy Allowed:**
- Must be static field rotating 360°
- Field values DO NOT CHANGE between frames
- Only rotation parameter varies (angle)
- Entropy = 0 (completely deterministic)

**File Size:**
- Per frame: ~40-60 KB (high quality PNG)
- Total: ~1.5-2.2 MB (36 frames)
- Compression: GIF palette optimization

**Scaling Rule:**
- Molecular scale: 1200×1200 (single molecule + context)
- Cell scale: 2000×2000 (organelles visible)
- Tissue scale: 2400×2400 (cell arrangement)
- Organ scale: 3000×3000 (tissue networks)
- System scale: 3600×3600 (organ interactions)

**Resolution locked:** Highest clarity for structure visualization

---

### TYPE 2: THRESHOLD ANIMATION (Breathing Core)

**Purpose:** Show field spatial extent (core → periphery)

**Container Spec:**
```
frames:           36 (smooth progression)
fps:              20 (slower for clarity)
duration:         1.8 seconds (36 frames ÷ 20 fps)
image_dimensions: 1200×1200 px
dpi:              150
entropy_budget:   LOW-MEDIUM (threshold varies, field static)
threshold_range:  (0.2, 0.8) [20% core to 80% sparse]
```

**Field Entropy Allowed:**
- Field values CONSTANT
- Threshold parameter varies smoothly: 0.9 → 0.1 → 0.9
- Creates effect of core pulsing outward, then collapsing
- Entropy ≈ Low (single parameter varies)

**Animation Pattern:**
```
Frame 1:  threshold=0.9  (tight core only)
Frame 18: threshold=0.1  (loose periphery)
Frame 36: threshold=0.9  (tight core again)
```

**File Size:** ~1.8-2.5 MB (36 frames)

**Scaling Rule:** Same as azimuth (dimensions scale with resolution level)

**Resolution locked:** Threshold range {0.2, 0.8} must hold through all scales

---

### TYPE 3: ELEMENT FOCUS CYCLING

**Purpose:** Highlight each element in sequence

**Container Spec:**
```
frames:           12 (4 elements × 3 frames each)
fps:              30
duration:         0.4 seconds (12 frames ÷ 30 fps)
image_dimensions: Same as parent scale
dpi:              150
entropy_budget:   MEDIUM (intensity color channel varies)
elements:         O, H, C, N (up to 4 types)
focus_intensity:  1.0 (highlighted) / 0.2 (dimmed)
```

**Field Entropy Allowed:**
- Base field CONSTANT
- Only color intensity changes per element
- Cycling: O → H → C → N → O (repeating)
- Entropy = Modest (intensity modulation only)

**Animation Pattern:**
```
Frames 1-3:   Oxygen (red) bright, others dim
Frames 4-6:   Hydrogen (cyan) bright, others dim
Frames 7-9:   Carbon (yellow) bright, others dim
Frames 10-12: Nitrogen (blue) bright, others dim
```

**File Size:** ~0.5-0.8 MB (12 frames, simpler)

**Resolution locked:** Exactly 4 elements, cycling order fixed

---

### TYPE 4: LAYER CYCLING (Onion Peeling)

**Purpose:** Show internal density structure

**Container Spec:**
```
frames:           12 (4 layers × 3 frames each)
fps:              20
duration:         0.6 seconds (12 frames ÷ 20 fps)
image_dimensions: Same as parent scale
dpi:              150
entropy_budget:   MEDIUM (layer selection varies)
layer_count:      4 (tight core to loose periphery)
layer_thresholds: [0.9, 0.7, 0.5, 0.3]
opacity_per_layer: [1.0, 0.7, 0.5, 0.2]
```

**Field Entropy Allowed:**
- Base field CONSTANT
- Each frame shows only 1 layer visible
- Layers are pre-computed threshold bands
- Entropy = Modest (layer selector only)

**Animation Pattern:**
```
Frames 1-3:  Layer 0 (threshold ≥ 0.9, full opacity)
Frames 4-6:  Layer 1 (threshold ≥ 0.7, 70% opacity)
Frames 7-9:  Layer 2 (threshold ≥ 0.5, 50% opacity)
Frames 10-12: Layer 3 (threshold ≥ 0.3, 20% opacity)
```

**File Size:** ~0.6-0.9 MB (12 frames)

**Resolution locked:** Exactly 4 layers, thresholds {0.9, 0.7, 0.5, 0.3} fixed

---

### TYPE 5: EVOLUTION (Temporal Dynamics)

**Purpose:** Show time-based field behavior

**Container Spec:**
```
frames:           36 (smooth time progression)
fps:              30
duration:         1.2 seconds (36 frames ÷ 30 fps)
image_dimensions: Same as parent scale
dpi:              150
entropy_budget:   MEDIUM-HIGH (field values vary in time)
time_range:       [0, T] (complete cycle)
variation_type:   oscillation, breathing, pulsing
```

**Field Entropy Allowed:**
- Field values CHANGE over time (physics-based)
- Time parameter: t = 0 → 2π (one complete oscillation)
- Field intensity modulates: concentration × (1 + α·sin(ωt))
- Entropy = Moderate (temporal dynamics)

**Animation Pattern:**
```
Frame 1:  t=0,    intensity×1.0 (baseline)
Frame 18: t=π,    intensity×1.3 (peak)
Frame 36: t=2π,   intensity×1.0 (back to baseline)
```

**Physics Constraint:**
```
ρ(t) = ρ₀ × (1 + amplitude × sin(phase + frequency × t))
```

**File Size:** ~1.5-2.2 MB (36 frames)

**Resolution locked:** Must follow realistic oscillation physics

---

### TYPE 6: ROTATION + SCALE (Orbital Motion)

**Purpose:** Spinning + zoom for spatial context

**Container Spec:**
```
frames:           36 (combined variation)
fps:              30
duration:         1.2 seconds
image_dimensions: Same as parent scale
dpi:              150
entropy_budget:   MEDIUM (two parameters vary)
azimuth_angle:    0° → 360°
scale_factor:     0.5× → 1.0× → 0.5× (zoom out/in/out)
```

**Field Entropy Allowed:**
- Base field CONSTANT
- Rotation + scale vary synchronously
- Creates orbital/dance effect
- Entropy = Low-Medium (2 geometric parameters)

**Animation Pattern:**
```
Frame 1:  angle=0°,    scale=0.5× (zoomed out)
Frame 18: angle=180°,  scale=1.0× (zoomed in, opposite side)
Frame 36: angle=360°,  scale=0.5× (return, zoomed out)
```

**File Size:** ~1.5-2.2 MB (36 frames)

**Resolution locked:** Scale range must be {0.5×, 1.0×}

---

### TYPE 7: TECHNIQUE MORPHING (Style Transition)

**Purpose:** Compare rendering methods

**Container Spec:**
```
frames:           12 (3 techniques × 4 frames transition each)
fps:              20
duration:         0.6 seconds
image_dimensions: Same as parent scale
dpi:              150
entropy_budget:   HIGH (rendering algorithm varies)
techniques:       [hybrid, multi_layer, isosurface]
transition_frames_per_technique: 4
```

**Field Entropy Allowed:**
- Base field CONSTANT
- Rendering algorithm CHANGES
- Each technique applied to same field
- Shows how algorithm choice affects visualization
- Entropy = Highest (algorithm selection)

**Animation Pattern:**
```
Frames 1-4:   Hybrid rendering (sharp core + halo)
Frames 5-8:   Multi-layer rendering (4 threshold bands)
Frames 9-12:  Isosurface rendering (single sharp boundary)
```

**File Size:** ~0.7-1.0 MB (12 frames, algorithm overhead)

**Resolution locked:** Exactly 3 techniques, order fixed

---

## Entropy Budget Summary

| Type | Frames | Duration | Entropy | File Size | Primary Variation |
|------|--------|----------|---------|-----------|------------------|
| Azimuth | 36 | 1.2s | None (0) | 1.5-2.2 MB | Rotation angle |
| Threshold | 36 | 1.8s | Low | 1.8-2.5 MB | Threshold value |
| Element | 12 | 0.4s | Medium | 0.5-0.8 MB | Element selection |
| Layer | 12 | 0.6s | Medium | 0.6-0.9 MB | Layer selection |
| Evolution | 36 | 1.2s | Medium-High | 1.5-2.2 MB | Time parameter |
| Rotate+Scale | 36 | 1.2s | Medium | 1.5-2.2 MB | Angle + scale |
| Morph | 12 | 0.6s | High | 0.7-1.0 MB | Algorithm |

---

## Scaling Across Resolutions

### Resolution Levels

```
MOLECULAR:
  - Dimensions: 1200×1200 px
  - DPI: 150
  - File budget: 2.5 MB per GIF
  - Typical frames: 12-36

CELLULAR:
  - Dimensions: 2000×2000 px
  - DPI: 150
  - File budget: 5-7 MB per GIF
  - Typical frames: 12-36

TISSUE:
  - Dimensions: 2400×2400 px
  - DPI: 120 (slightly lower for speed)
  - File budget: 8-12 MB per GIF
  - Typical frames: 12-36

ORGAN:
  - Dimensions: 3000×3000 px
  - DPI: 100 (optimized for size)
  - File budget: 12-18 MB per GIF
  - Typical frames: 12-36

SYSTEM:
  - Dimensions: 3600×3600 px
  - DPI: 100
  - File budget: 15-25 MB per GIF
  - Typical frames: 12-36
```

### Scaling Rule for Parameters

**Field Entropy Budgets Scale Inversely with Resolution:**

```
Higher resolution → MORE detailed field complexity possible
Lower entropy required at baseline as resolution increases

Example:
  Molecular (simple O+H): entropy ≈ 0 (rotation only)
  Cellular (organelles): entropy ≈ low (element cycling)
  Tissue (cell patterns): entropy ≈ medium (layer cycling)
  Organ (tissue networks): entropy ≈ medium-high (evolution)
  System (consciousness): entropy ≈ high (all patterns)
```

---

## Container Constraints (Hard Limits)

### GIF Technical Limits
```
Maximum dimensions:    65535×65535 px (GIF format limit, not used)
Practical max:         4000×4000 px (performance/display)
Maximum frame count:   256 colors per frame (palette limit)
Maximum file size:     2 GB (theoretical)
Practical max:         500 MB (browser/viewing)

Recommended constraints:
  - Image dimensions:  ≤ 3600×3600 px
  - Frame count:       12-36 (smooth animation)
  - File size:         ≤ 25 MB
  - Duration:          ≤ 3 seconds (viewer retention)
```

### Animation Frame Rate Ranges

```
Optimal fps by type:
  Rotation (geometric):     30 fps (smooth motion)
  Threshold (reveal):       20 fps (paced reveal)
  Element (sequential):     30 fps (snappy switching)
  Layer (progressive):      20 fps (clear progression)
  Evolution (organic):      30 fps (natural motion)
  Rotate+Scale (combined):  30 fps (coordinated)
  Morph (technique):        20 fps (time to perceive)
```

---

## Validation Rules (Must Pass)

For any GIF animation to be valid:

```
1. RESOLUTION RULE
   ✓ Image dimensions match resolution level spec
   ✓ DPI consistent throughout animation
   
2. ENTROPY RULE
   ✓ Field entropy ≤ spec for animation type
   ✓ Variation parameters within defined ranges
   ✓ No unspecified variations introduced
   
3. FRAME RULE
   ✓ Frame count exactly as specified for type
   ✓ Frames ordered correctly
   ✓ No skipped or duplicate frames
   
4. TIMING RULE
   ✓ FPS constant throughout animation
   ✓ Duration = frames ÷ fps (calculated correctly)
   ✓ No delays or frame drops
   
5. FILE SIZE RULE
   ✓ Final GIF ≤ file size budget for resolution
   ✓ Compression applied (palette optimization)
   ✓ No raw/uncompressed storage
   
6. COLOR RULE
   ✓ Element colors fixed (O=red, H=cyan, C=yellow, N=blue)
   ✓ No desaturation or color averaging
   ✓ Saturation maintained across frames
   
7. ENERGY RULE
   ✓ Animation follows physics (if time-based)
   ✓ Field values consistent with model
   ✓ No illegal state transitions
```

---

## Examples: Locked Specifications

### Example 1: Molecular Azimuth Rotation

```yaml
resolution_level: MOLECULAR
animation_type: AZIMUTH
frames: 36
image_dimensions: 1200×1200 px
dpi: 150
fps: 30
duration: 36 frames ÷ 30 fps = 1.2 seconds
entropy_budget: 0 (field constant, only rotation)
file_size_budget: 2.5 MB max
element_colors: FIXED (O=red, H=cyan)

validation:
  ✓ Each frame rotated 10° from previous (0°, 10°, 20°, ..., 350°)
  ✓ Field values identical in all frames
  ✓ No threshold changes, color shifts, or element additions
  ✓ Final GIF ≤ 2.5 MB
```

### Example 2: Cellular Layer Cycling

```yaml
resolution_level: CELLULAR
animation_type: LAYER
frames: 12
image_dimensions: 2000×2000 px
dpi: 150
fps: 20
duration: 12 frames ÷ 20 fps = 0.6 seconds
entropy_budget: MEDIUM (layer selector only)
layer_thresholds: [0.9, 0.7, 0.5, 0.3] FIXED
file_size_budget: 6 MB max

validation:
  ✓ Frames 1-3: Layer 0 (threshold ≥ 0.9)
  ✓ Frames 4-6: Layer 1 (threshold ≥ 0.7)
  ✓ Frames 7-9: Layer 2 (threshold ≥ 0.5)
  ✓ Frames 10-12: Layer 3 (threshold ≥ 0.3)
  ✓ Thresholds never deviate from locked values
  ✓ No field changes between frames
```

### Example 3: Tissue Evolution (Time-Based)

```yaml
resolution_level: TISSUE
animation_type: EVOLUTION
frames: 36
image_dimensions: 2400×2400 px
dpi: 120
fps: 30
duration: 1.2 seconds
entropy_budget: MEDIUM-HIGH (temporal dynamics)
physics_model: ρ(t) = ρ₀ × (1 + amplitude × sin(frequency × t))
file_size_budget: 10 MB max

validation:
  ✓ Time parameterized: t = 0 → 2π
  ✓ Field varies smoothly per time equation
  ✓ No discontinuities or jumps
  ✓ Physical model followed exactly
  ✓ Entropy documented and justified
```

---

## Ledger Entries Required — Moment-Specific Determinations

**Every GIF animation generates ONE ledger entry capturing all determined values at request time.**

```json
{
  "timestamp": "2026-04-01T14:32:47.123Z",
  "request_moment": {
    "second": "2026-04-01T14:32:47.123Z",
    "timezone": "UTC",
    "causality": "animation requested → specifications determined → generation began"
  },
  "animation_id": "mol_azimuth_001",
  "resolution_level": "MOLECULAR",
  "animation_type": "AZIMUTH",
  "determined_at_request": {
    "frames": 36,
    "fps": 30,
    "duration_seconds": 1.2,
    "image_dimensions_px": "1200×1200",
    "dpi": 150,
    "entropy_budget": "0",
    "entropy_budget_rationale": "field constant, rotation only",
    "file_size_budget_mb": 2.5,
    "specification_source": "GIF_ANIMATION_SPECIFICATION.md"
  },
  "generation_results": {
    "frames_generated": 36,
    "file_size_kb": 2048,
    "entropy_actually_used": 0,
    "entropy_budget_respected": true,
    "validation_checks_passed": 7,
    "element_colors": "O=red(255,0,0), H=cyan(0,255,255)",
    "color_saturation_preserved": true,
    "physics_model": "deterministic_rotation",
    "field_values_constant": true
  },
  "validation_results": {
    "resolution_rule": "✓ PASS",
    "entropy_rule": "✓ PASS",
    "frame_rule": "✓ PASS",
    "timing_rule": "✓ PASS",
    "file_size_rule": "✓ PASS",
    "color_rule": "✓ PASS",
    "energy_rule": "✓ PASS"
  },
  "causality_chain": [
    "request_received",
    "resolution_level_determined",
    "animation_type_determined",
    "all_specifications_locked",
    "animation_generated",
    "validation_performed",
    "all_checks_passed",
    "ledger_recorded"
  ],
  "file_output": "/path/to/animation.gif",
  "hash_sha256": "abc123...",
  "notes": "All specifications determined and locked at request moment. No deviation from template values."
}
```

**Critical Points:**
- `timestamp` = EXACT moment when animation was requested
- `determined_at_request` = All values locked from templates at that moment
- `generation_results` = What actually happened under those locked constraints
- `validation_results` = Proof that all 7 checks passed
- `causality_chain` = Ordered sequence of events from request → ledger record

**No animation is abstract.** Each GIF has a concrete ledger entry capturing:
1. When it was requested (moment)
2. What values were determined (from templates)
3. What was generated (actual results)
4. How it was validated (all 7 rules)
5. Why it matters (causality chain)

---

## Status

**GIF Animation Container: LOCKED WITH MOMENT-SPECIFIC DETERMINISM**

All animation types have specified:
- Frame counts ✓ (determined at request time)
- Field entropy budgets ✓ (determined at request time)
- Resolution parameters ✓ (determined at request time)
- File size ceilings ✓ (determined at request time)
- Validation rules ✓ (7 checks applied at generation)
- Scaling patterns ✓ (molecular → system)

Framework ready to scale from molecular → system levels.

**CRITICAL PRINCIPLE:** Every specification in this document becomes a concrete determination 
at the MOMENT an animation is requested. The values are not abstract—they are locked causal 
consequences of the request. Each animation generates a ledger entry capturing that moment 
and all determined values.

Every GIF generated must satisfy this specification AND provide ledger proof of moment-specific determinations.
