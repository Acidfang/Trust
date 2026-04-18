# HUMAN STANDARDS FOR UNIVERSAL CONTAINERS
## Universal Best Practices for Expressing Orientation, Rotation, and Dipole Representation

**Version**: 1.0  
**Date**: April 1, 2026  
**Standards Authority**: Established from scientific consensus (Rotation Formalisms in 3D, Molecular Graphics, Quaternions & Spatial Rotation)  
**Applies to**: ALL containers (molecules, point clouds, vector fields, geometric entities)

---

## CORE PRINCIPLE: ONE TRUTH, MANY EXPRESSIONS

Every container has inherent:
- **Orientation** (how it's rotated relative to reference frame)
- **Dipole/Polarity** (directional property)
- **Field** (local + global spatial influence)

These must be expressed consistently across ALL containers.

---

## 1. ROTATION REPRESENTATION STANDARDS

### 1.1 PRIMARY STANDARD: QUATERNIONS (Hamilton Convention)

All rotations must use **unit quaternions** in **Hamilton convention** (not Shuster):

```
q = (w, x, y, z)  where w is scalar, (x,y,z) is vector part

Unit quaternion constraint: w² + x² + y² + z² = 1

Rotation of angle θ around unit axis u = (ux, uy, uz):
  w = cos(θ/2)
  x = ux * sin(θ/2)
  y = uy * sin(θ/2)
  z = uz * sin(θ/2)
```

**Why Quaternions?**:
- ✓ Most compact (4 numbers vs 9 for matrices)
- ✓ Avoids gimbal lock (unlike Euler angles)
- ✓ Numerically stable after normalization
- ✓ Industry standard in all major frameworks (MATLAB, ROS, Eigen, numpy-quaternion, SymPy)
- ✓ Efficient composition: q3 = q2 ⊗ q1 (quaternion product)
- ✓ Natural interpolation (SLERP - spherical linear interpolation)

**Hamilton vs Shuster Convention**:
- **Hamilton** (standard): ij = k ✓ USE THIS
- **Shuster** (aerospace only): ij = −k ✗ AVOID (causes integration errors)

---

### 1.2 SECONDARY STANDARDS: Conversion Targets

For visualization/debugging, convert quaternions to:

#### **Euler Axis-Angle Representation** (3-1-3 Extrinsic)
Used for human understanding:
```
axis = (qi, qj, qk) / sin(θ/2)   [normalize if needed]
angle θ = 2 * atan2(√(qi²+qj²+qk²), qr)  [numerically stable]
```

**Use case**: Explaining "rotate 45° around Z-axis"

#### **Rotation Matrix** (3×3 Rotation Matrix Form)
Used for transforming vectors when necessary:
```
R = [1-2s(qj²+qk²)    2(qiqj-qkqr)      2(qiqk+qjqr)    ]
    [2(qiqj+qkqr)     1-2s(qi²+qk²)     2(qjqk-qiqr)    ]
    [2(qiqk-qjqr)     2(qjqk+qiqr)      1-2s(qi²+qj²)   ]

where s = 1 for unit quaternions, s = 2/(qi²+qj²+qk²+qr²) for non-unit
```

**Use case**: Matrix multiplication for coordinate transformations

#### **NOT RECOMMENDED**: Euler Angles
- ✗ Suffer from gimbal lock
- ✗ Non-commutative
- ✗ Ambiguous conventions (12 possible orderings)
- ✗ Hard to compose rotations

---

### 1.3 ROTATION COMPOSITION

Composing two rotations R_B then R_A to get R_C:

```python
# Using quaternions (most efficient):
q_C = q_B ⊗ q_A    # quaternion product (not commutative!)

# Result: Direct axis-angle extraction
axis_C = (qc_i, qc_j, qc_k) / sin(θ_C/2)
angle_C = 2 * atan2(√(qc_i²+qc_j²+qc_k²), qc_r)

# This is Rodrigues' Formula for composite rotations (established 1840)
```

**Critical**: Rotation order matters! R_B * R_A ≠ R_A * R_B

---

### 1.4 ROTATION VELOCITY / ANGULAR VELOCITY

If container is rotating, express angular velocity as:

```
ω⃗ = [ωx, ωy, ωz]   [rad/s]

Derivative relationship:
dq/dt = (1/2) * [0, ωx, ωy, ωz] ⊗ q

Rate of rotation matrix change:
d(R)/dt = [ω]× * R   where [ω]× is the skew-symmetric cross-product matrix
```

---

## 2. DIPOLE / POLARITY REPRESENTATION STANDARDS

### 2.1 PRIMARY STANDARD: ARROW VECTORS

Express dipole/polarity as **directional arrow**:

```
Dipole = Vector from NEGATIVE source → POSITIVE source

Visual representation:
  ├─ Arrow tail: Positioned at negative charge center
  ├─ Arrow head: Points toward positive charge
  └─ Arrow length: Proportional to dipole magnitude |μ⃗|
```

**Why this convention?**
- ✓ Matches molecular chemistry (electron clouds flow toward positive)
- ✓ Standard in electromagnetism (field lines point away from +, toward −)
- ✓ Intuitive for visualization
- ✓ Works for point charges, molecular systems, vector fields

### 2.2 COLOR CODING FOR DIPOLE POLARITY

```
Dipole Magnitude Visualization (0-1 scale):
  |μ| = 0.00  →  Gray   (neutral)
  |μ| = 0.33  →  Yellow (moderate)
  |μ| = 0.67  →  Orange (strong)
  |μ| = 1.00  →  Red    (maximum)

Directionality (arrow hue rotation):
  H = base_hue + (angle * 360°/2π)
  S = intensity_scale * |μ|
  L = 50% (constant brightness for readability)
```

### 2.3 MAGNITUDE EXPRESSION

Dipole moment **always expressed in atomic units** for molecular systems:

```
Standard units:
  • Debye (D): 1 D = 3.336 × 10⁻³⁰ C·m (chemistry convention)
  • Atomic units: 1 a.u. = e · a₀ ≈ 2.54 D

UNIVERSAL CONTAINERS convention:
  μ⃗ [atomic units] = [ex, ey, ez]
  
  Where:
    e = elementary charge (normalized to 1 in atomic units)
    a₀ = Bohr radius (normalized to 1 in atomic units)
```

---

## 3. MOLECULAR VISUALIZATION STANDARDS

### 3.1 ATOM TYPE COLOR SCHEME (CPK Standard)

Established by Corey-Pauling-Koltun (1953):

```
Element  │ Color     │ RGB (0-255)
─────────┼───────────┼──────────────
H        │ White     │ (255, 255, 255)
C        │ Black     │ (  0,   0,   0)
N        │ Blue      │ (  0,   0, 255)
O        │ Red       │ (255,   0,   0)
P        │ Orange    │ (255, 127,   0)
S        │ Yellow    │ (255, 255,   0)
F        │ Cyan      │ (  0, 255, 255)
Cl       │ Green     │ (  0, 255,   0)
Br       │ Dark Br   │ (139,  69,  19)
I        │ Purple    │ (128,   0, 128)
other    │ Gray      │ (192, 192, 192)
```

### 3.2 BOND VISUALIZATION STANDARDS

```
Bond Type    │ Style           │ Color
─────────────┼─────────────────┼─────────────
Single       │ Solid line      │ Gray
Double       │ Double line     │ Gray (offset)
Triple       │ Triple line     │ Gray (offset)
Aromatic     │ Dashed circle   │ Gray
Hydrogen B.  │ Dotted line     │ Light gray
Coordinate   │ Arrow line →    │ Blue (points to acceptor)
```

### 3.3 MOLECULAR MODELS BY PURPOSE

```
Model Type          │ Purpose                    │ Best For
────────────────────┼────────────────────────────┼──────────────
Ball-and-stick      │ Structure + connectivity   │ Most molecules
Space-filling       │ Van der Waals surface      │ Size/shape
Ribbon diagram      │ Protein backbone path      │ Proteins
Surface (isosurface)│ Electron density/ESP       │ Properties
Wireframe           │ Speed/clarity              │ Large systems
Spacefilling + ESP  │ Combined property view     │ Reactivity
```

### 3.4 ISOMETRIC PROJECTION (Standard Camera Angle)

```
For all containers, use ISOMETRIC projection:
  Elevation: 35.26° (arctan(√2))
  Azimuth:   45.0°
  Distance:  automated to frame all atoms
  
This shows 3D geometry clearly while maintaining uniformity.
```

---

## 4. FIELD REPRESENTATION STANDARDS

### 4.1 VECTOR FIELD VISUALIZATION

For multi-body systems (all molecules as ONE field):

```
Representation: Arrows at grid points
  Position:  (x, y, z) coordinate
  Direction: Normalized field direction
  Magnitude: Arrow length proportional to |F⃗|
  Color:     Heat map based on magnitude

Magnitude Heatmap (0 to max):
  0.0  →  Blue   (cold, minimal)
  0.25 →  Cyan   
  0.50 →  Green  (medium)
  0.75 →  Yellow
  1.0  →  Red    (hot, maximum)
```

### 4.2 GRADIENT FIELD REPRESENTATION

For energy landscapes:

```
Contour lines (potential):
  • Closed loops show local minima/maxima
  • Density of lines shows steepness
  • Color gradient: Blue (min) → Red (max)

Vector flow:
  • Arrows perpendicular to contours
  • Point in direction of increasing potential
  • Arrow length = magnitude of gradient
```

---

## 5. CONTAINER EXPRESSION STANDARDS

### 5.1 UNIVERSAL CONTAINER DATA SCHEMA

Every container must store:

```json
{
  "container_type": "molecule|field|point_cloud|graph",
  "entity_id": "unique_identifier",
  "entities": [
    {
      "id": "entity_unique_id",
      "type": "atom|point|node",
      "position": [x, y, z],
      "properties": {
        "charge": float,
        "atomic_number": int,
        "radius_van_der_waals": float
      }
    }
  ],
  "orientation": {
    "representation": "quaternion_hamilton",
    "q_w": scalar,
    "q_xyz": [x, y, z],
    "euler_axis_angle_for_reference": {
      "axis": [ux, uy, uz],
      "angle_radians": float
    }
  },
  "dipole": {
    "representation": "arrow_vector",
    "source_negative": [x_neg, y_neg, z_neg],
    "target_positive": [x_pos, y_pos, z_pos],
    "magnitude_debye": float,
    "direction_unit": [ux, uy, uz]
  },
  "field": {
    "type": "gradient|vector|scalar",
    "values": [],
    "units": "atomic_units|SI"
  },
  "rendering": {
    "model_type": "ball_and_stick|space_filling|ribbon|surface",
    "camera": "isometric_35.26_45.0",
    "colormap": "CPK|heat|gradient"
  }
}
```

### 5.2 CONTAINER RENDERING PIPELINE

All containers follow **7-stage universal pipeline**:

```
Stage 1: VALIDATE    ← Input safety (geometry, units, ranges)
         ↓
Stage 2: METRICS     ← Analyze container (size, density, field)
         ↓
Stage 3: STRATEGY    ← Choose rendering approach based on metrics
         ↓
Stage 4: EXECUTE     ← Generate frames (rotation animation)
         ↓
Stage 5: VERIFY      ← Quality check (no overlaps, clear dipoles)
         ↓
Stage 6: ADAPT       ← Fix violations (adjust camera/colors)
         ↓
Stage 7: OUTPUT      ← Encode to GIF/MP4 with metadata
```

---

## 6. IMPLEMENTATION STANDARDS (PYTHON)

### 6.1 QUATERNION OPERATIONS

```python
import numpy as np

class Quaternion:
    def __init__(self, w, x, y, z):
        """Hamilton convention: (w + xi + yj + zk)"""
        self.q = np.array([w, x, y, z])
        self.normalize()
    
    def normalize(self):
        """Ensure unit quaternion"""
        norm = np.linalg.norm(self.q)
        if norm > 1e-10:  # Avoid division by zero
            self.q /= norm
    
    def compose(self, q2):
        """Compose two rotations: self then q2"""
        w1, x1, y1, z1 = self.q
        w2, x2, y2, z2 = q2.q
        
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        
        return Quaternion(w, x, y, z)
    
    def to_matrix(self):
        """Convert to 3x3 rotation matrix"""
        w, x, y, z = self.q
        
        return np.array([
            [1-2*(y**2+z**2), 2*(x*y-w*z), 2*(x*z+w*y)],
            [2*(x*y+w*z), 1-2*(x**2+z**2), 2*(y*z-w*x)],
            [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x**2+y**2)]
        ])
    
    def to_axis_angle(self):
        """Convert to axis-angle for reference"""
        w, x, y, z = self.q
        
        angle = 2 * np.arccos(np.clip(w, -1, 1))
        sin_half = np.sin(angle / 2)
        
        if sin_half < 1e-10:
            axis = np.array([0, 0, 1])  # Undefined
        else:
            axis = np.array([x, y, z]) / sin_half
        
        return {
            'axis': axis,
            'angle_rad': angle,
            'angle_deg': np.degrees(angle)
        }
```

### 6.2 DIPOLE OPERATIONS

```python
class Dipole:
    def __init__(self, source_neg, target_pos, magnitude=None):
        """source_neg: negative charge position (array)
           target_pos: positive charge position (array)
           magnitude: explicit magnitude (optional)
        """
        self.source = np.array(source_neg, dtype=float)
        self.target = np.array(target_pos, dtype=float)
        self.vector = self.target - self.source
        self.magnitude = np.linalg.norm(self.vector)
        self.direction = self.vector / (self.magnitude + 1e-10)
    
    def to_debye(self):
        """Convert magnitude to Debye units (from atomic units)"""
        atomic_to_debye = 2.54  # Conversion factor
        return self.magnitude * atomic_to_debye
    
    def rotate(self, quaternion):
        """Rotate dipole by quaternion"""
        R = quaternion.to_matrix()
        rotated_vec = R @ self.vector
        return Dipole(self.source, self.source + rotated_vec)
    
    def color_code(self):
        """Return RGB color based on magnitude"""
        # Normalize magnitude to 0-1
        norm_mag = np.tanh(self.magnitude / 10.0)  # Smooth saturation
        
        # Hue-saturation-lightness
        if norm_mag < 0.25:
            rgb = (128, 128, 128)  # Gray (neutral)
        elif norm_mag < 0.50:
            rgb = (255, 255, 0)    # Yellow
        elif norm_mag < 0.75:
            rgb = (255, 165, 0)    # Orange
        else:
            rgb = (255, 0, 0)      # Red (maximum)
        
        return rgb
```

---

## 7. METADATA & DOCUMENTATION STANDARDS

Every container rendering must include metadata:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<container_render>
    <metadata>
        <entity_id>molecule_001</entity_id>
        <entity_type>molecule</entity_type>
        <render_date>2026-04-01T12:00:00Z</render_date>
        <renderer>UNIVERSAL_RENDERER_v1.0</renderer>
    </metadata>
    
    <orientation_standard>
        <representation>quaternion_hamilton</representation>
        <q_w>0.7071</q_w>
        <q_vector>0.7071 0.0 0.0</q_vector>
        <euler_reference>
            <axis>0 0 1</axis>
            <angle_rad>1.5708</angle_rad>
            <angle_deg>90.0</angle_deg>
        </euler_reference>
    </orientation_standard>
    
    <dipole_standard>
        <representation>arrow_vector</representation>
        <source_negative>-1.0 0.0 0.0</source_negative>
        <target_positive>1.0 0.0 0.0</target_positive>
        <magnitude_atomic_units>2.0</magnitude_atomic_units>
        <magnitude_debye>5.08</magnitude_debye>
        <color>255 0 0</color>
    </dipole_standard>
    
    <rendering_parameters>
        <model_type>ball_and_stick</model_type>
        <camera>isometric</camera>
        <elevation_deg>35.26</elevation_deg>
        <azimuth_deg>45.0</azimuth_deg>
        <colormap>CPK</colormap>
    </rendering_parameters>
    
    <frame_info>
        <total_frames>360</total_frames>
        <rotation_axis>0 0 1</rotation_axis>
        <rotation_angle_per_frame>1.0</rotation_angle_per_frame>
        <units>degrees</units>
    </frame_info>
</container_render>
```

---

## 8. VALIDATION CHECKLIST FOR ALL CONTAINERS

Before rendering any container:

- [ ] **Orientation** is expressed as unit quaternion (Hamilton convention)
- [ ] **Quaternion normalized**: |q| = 1.000 ± 0.001
- [ ] **Dipole** has clear source (negative) and target (positive)
- [ ] **Dipole magnitude** >= 0 and in known units (atomic units or Debye)
- [ ] **Color scheme** matches CPK standard for atoms (if applicable)
- [ ] **Field visualization** uses consistent heatmap (Blue→Red 0-1 scale)
- [ ] **Camera angle** is isometric (35.26° elevation, 45° azimuth)
- [ ] **Metadata** XML includes all render parameters
- [ ] **No coordinate singularities** (gimbal lock, NaN, Inf)
- [ ] **Rotation composition** verified: q3 = q2 ⊗ q1 (order matters)

---

## 9. REFERENCES & AUTHORITY SOURCES

1. **Rotation Formalisms**:
   - Wikipedia: "Rotation formalisms in three dimensions" (March 2026)
   - Quaternion standard: Hamilton convention (established 1844)
   - Modern references: Shuster (1993), Wertz (1980), Schmidt (2001)

2. **Molecular Graphics**:
   - Wikipedia: "Molecular graphics" (March 2026)
   - CPK coloring: Corey & Pauling (1953), Koltun (1965)
   - Standards: IUPAC compendium (Gold Book)

3. **Molecular Systems**:
   - Dipole representation: Standard in chemistry & physics
   - Vector field visualization: Universal in computational chemistry
   - Units: Atomic units (Hartree-Fock convention)

4. **Software Standards**:
   - Quaternion libraries: Eigen, numpy-quaternion, SciPy, MATLAB, ROS
   - Convention: All use Hamilton convention (Shuster marked "discouraged")
   - Multi-framework consistency: MATLAB Aerospace, ROS, SymPy, Universal Scene Description

---

## 10. FUTURE EXTENSIONS

This standard can be extended to:

- **Quantum systems**: Include wavefunction phases
- **Neural networks**: Node orientations, weight field visualization
- **Crystal structures**: Lattice orientations, defects
- **Force fields**: Electric, magnetic, gravitational fields
- **Protein dynamics**: Multi-frame animations with confidence intervals

All extensions must preserve quaternion + dipole + field core.

---

**END OF STANDARDS DOCUMENT**

Approved for: ALL Universal Containers  
Effective Date: April 1, 2026  
Next Review: April 1, 2027
