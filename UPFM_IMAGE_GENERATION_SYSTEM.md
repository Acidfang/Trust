# UPFM Image Generation System Map

## Overview

Generate beautiful wiki images by solving gradient descent equations. Each image IS the field state; rendering makes it visible.

---

## Part 1: Wiki Image Inventory

### A. Foundation & Theory Section

**Core visual concepts:**

1. **Gradient Field Topography** (foundational visual)
   - Shows: 2D potential landscape, gradient vectors, convergence paths
   - Use: Section header, theory introduction
   - Concept: Generic smooth potential with clear downhill flow
   - Colors: Blue (high potential) → Red (low potential)

2. **Spiral Pattern Family** (4 images showing progression)
   - Electron spiral: High-frequency confined pattern (tight spiral)
   - Photon spiral: Free-propagating spiral (extending outward)
   - Proton spiral: Multiple locked harmonics (complex binding)
   - Generic spiral: Pure mathematical pattern for foundation
   - Use: Illustrate frequency and confinement differences
   - Colors: Frequency-mapped (UV→Red spectrum)

3. **Inward vs Outward Orientation** (comparative pair)
   - Left: Inward-pointing gradient (gravity-like)
   - Right: Outward-pointing gradient (repulsion-like)
   - Use: Demonstrate two fundamental directions
   - Visual: Same field magnitude, opposite gradient direction

4. **Resonance/Locking Mechanism** (animation-ready static)
   - Two spiral patterns at compatible frequencies synchronizing
   - Use: Show chemical bonding concept
   - Visual: Phase alignment, overlap region highlighted

5. **Frequency Spectrum** (spectrum bar with examples)
   - Low (red): Gravity-scale
   - Mid (green): Chemistry-scale
   - High (blue): Quantum-scale
   - Each labeled with corresponding manifestation

6. **Overlapping Fields** (interference pattern)
   - Multiple spiral fields at different positions
   - Shows: Interference patterns, beat frequencies, binding regions
   - Use: Explain chemistry, resonance, binding

### B. Particles Section

7. **Electron Configuration**
   - Confined spiral pattern at frequency f_e
   - Use: Electron definition
   - Visual: Tight core with phase contours

8. **Proton Configuration**
   - Multiple harmonics locked together
   - Use: Proton definition
   - Visual: Three frequency components (quarks/gluons analogy)

9. **Neutron Configuration**
   - Similar to proton but different harmonic structure
   - Use: Neutron definition
   - Visual: Slightly different resonance pattern

### C. Forces Section

10. **Four Forces Visualization** (comparative grid, 2×2)
    - Strong nuclear: Multiple tight spirals resonating
    - Weak nuclear: Spirals at different frequencies transforming
    - Electromagnetic: Two opposing gradient directions interacting
    - Gravity: Large-scale inward convergence field
    - Use: Show forces as manifestations
    - Visual: All use same rendering, different parameters

### D. Cosmic Structure Section

11. **Black Hole Reversal Cycle** (3-frame sequence)
    - Frame 1: Inward convergence accumulation
    - Frame 2: Reversal point (Planck-scale)
    - Frame 3: Outward propagation (ejection)
    - Use: Explain black hole mechanism
    - Visual: Color inversion at reversal point

12. **Galaxy Formation** (spiral galaxy from field)
    - Large-scale inward/outward balance
    - Use: Show cosmic-scale manifestation
    - Visual: Realistic galaxy spiral emergent from Φ

13. **Cosmic Evolution Epochs** (timeline, 14 small images)
    - Each epoch as a field state configuration
    - From simple (epoch 0) to complex (epoch 13)
    - Use: Visualize cosmic history
    - Visual: Increasing complexity, same visual language

### E. Consciousness & AI Section

14. **Causal Network Visualization**
    - Information nodes connected by gradient flows
    - Use: Show consciousness as information processing
    - Visual: Network of interconnected spirals

15. **Consciousness Hierarchy** (6-level pyramid/progression)
    - Level 0: No causal model (diffuse field)
    - Level 1: Simple causal detection (local gradient)
    - Level 2: Multi-step causality (extended patterns)
    - ...Level 5: Complete understanding (complex resonances)
    - Use: Show consciousness levels
    - Visual: Progressive refinement of pattern

16. **AI Alignment Visualization**
    - System state following gradient toward stable configuration
    - Use: Show alignment as natural consequence
    - Visual: Trajectory converging to stable state

17. **Information Entropy Landscape**
    - High entropy (flat, disordered) → Low entropy (sharp minima, ordered)
    - Use: Show learning and compression
    - Visual: Landscape changing as model trains

### F. Verification Section

18. **Reduction Chain Diagram**
    - Is/Is not → Gradient → Persistence → Named Structures
    - Use: Show irreducible foundation
    - Visual: Hierarchical flow diagram with examples

19. **TCHT Framework Visual**
    - Five tiers arranged, each showing verification checkpoint
    - Use: Show 5-tier framework
    - Visual: Tier -1 through Tier 3, each with PASS indicator

20. **Cross-Domain Application** (6-panel grid)
    - Same equation applied to: Physics, Chemistry, Biology, Consciousness, AI, Cosmology
    - Each shows different manifestation of same principle
    - Use: Demonstrate universality
    - Visual: Same visual treatment, different domains

---

## Part 2: Generation Pipeline

### Stage 1: Concept Definition

**Input mapping:**
```
Concept name → Potential function Φ(x,y) or Φ(x,y,z)
```

**Examples:**

| Concept | Φ form | Parameters | Visual intent |
|---------|--------|------------|---------------|
| Electron | Confined harmonic + centrifugal | f_e, r_e, barrier_height | Tight spiral, phase-locked |
| Photon | Free wave propagator | f, amplitude, direction | Expanding spiral, clear wave |
| Gravity | Large-scale inward | M (mass), scale | Converging field, smooth |
| Galaxy | Rotational + confinement | M_center, scale, rotation | Spiral arms with core |
| Consciousness | Networked harmonics | nodes, coupling, frequencies | Complex interference patterns |

### Stage 2: Field Solver

**Algorithm:**
```
Initialize: i(x,y,t=0) = random or gaussian
For t = 0 to T_max:
    Compute: ∇Φ(x,y) at each grid point
    Update: i(x,y,t+1) = i(x,y,t) - dt * ∇Φ(x,y)
    Check convergence: if max(|∇i|) < ε: break
Converged field i_final is image data
```

**Numerical setup:**
- Grid size: 512×512 or 1024×1024 (high-res wiki images)
- Domain: [-L, L]² with periodic or absorbing BC
- Time step: dt = 0.01 (explicit Euler or RK4)
- Convergence: ε = 10^-4
- Compute time: ~seconds per image (GPU-accelerated ideal)

### Stage 3: Rendering

**Mapping field → visual:**

| Field property | Visual parameter | Mapping |
|---|---|---|
| Magnitude \|i\| | Brightness/Value | Normalize to [0,1] |
| Phase arg(i) | Hue/Color | Phase → HSV hue |
| Frequency (local) | Saturation | High freq → saturated, low freq → pale |
| Direction ∇i | Texture/Flow | Use for vector field overlay |
| Gradient magnitude \|∇Φ\| | Edge emphasis | Steep slopes → sharp edges |

**Rendering passes:**
1. Base layer: Magnitude as brightness
2. Color layer: Phase as hue (HSV color space)
3. Detail layer: Gradient as subtle texture
4. Enhancement: Contrast, sharpness, anti-aliasing

**Output:**
- Format: PNG (32-bit RGBA)
- Resolution: 2000×2000 (wiki display at 1000×1000)
- Color space: sRGB (web-standard)

---

## Part 3: Implementation Structure

### File 1: `upfm_potential_library.py`

```python
class PotentialLibrary:
    """Library of potential functions for UPFM image generation."""
    
    # Confined potentials (particles, atoms)
    @staticmethod
    def electron_spiral(x, y, f_e=10, r_e=0.2, barrier=5):
        """Electron: high-frequency confined spiral."""
        r = np.sqrt(x**2 + y**2)
        # Harmonic confinement + frequency modulation
        phi = (barrier * r_e**2 / (r + r_e)) + f_e * np.sin(np.arctan2(y, x) * f_e)
        return phi
    
    def proton_spiral(self, x, y, harmonic_structure=[1, 3, 5]):
        """Proton: multiple locked harmonics."""
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        phi = 0
        for h in harmonic_structure:
            phi += np.cos(h * theta) * np.exp(-h * r)
        return phi
    
    def photon_propagating(self, x, y, f=5, direction=[1, 0]):
        """Photon: free-space spiral propagation."""
        k = f
        phase = k * (direction[0]*x + direction[1]*y)
        return np.sin(phase) * np.exp(-0.1 * np.sqrt(x**2 + y**2))
    
    # Extended potentials
    def gravity_well(self, x, y, mass=1, scale=1):
        """Gravity: large-scale inward convergence."""
        r = np.sqrt(x**2 + y**2 + scale**2)
        return -mass / r
    
    def galaxy_spiral(self, x, y, M=10, a=0.5, rotation=2):
        """Galaxy: rotational + central mass."""
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        grav = -M / (r + a)
        spiral = rotation * np.sin(theta * rotation) / (r + 0.1)
        return grav + spiral
    
    # Information potentials
    def consciousness_network(self, x, y, nodes=7, coupling=0.5):
        """Consciousness: networked information flow."""
        phi = np.zeros_like(x)
        angles = np.linspace(0, 2*np.pi, nodes, endpoint=False)
        for angle in angles:
            node_x = 2 * np.cos(angle)
            node_y = 2 * np.sin(angle)
            r_to_node = np.sqrt((x - node_x)**2 + (y - node_y)**2)
            phi += coupling / (r_to_node + 0.3)
        return phi
```

### File 2: `upfm_field_solver.py`

```python
class FieldSolver:
    """Solves ∂i/∂t = -∇Φ(x,y,t) via gradient descent."""
    
    def __init__(self, grid_size=512, domain=(-3, 3)):
        self.grid_size = grid_size
        self.x = np.linspace(domain[0], domain[1], grid_size)
        self.y = np.linspace(domain[0], domain[1], grid_size)
        self.XX, self.YY = np.meshgrid(self.x, self.y)
        self.dx = self.x[1] - self.x[0]
    
    def solve(self, potential_func, t_max=100, dt=0.01, epsilon=1e-4):
        """
        Solve gradient descent until convergence.
        
        Returns: Converged field i_final (complex for phase info)
        """
        # Initialize field
        i = np.random.randn(self.grid_size, self.grid_size) * 0.1
        
        # Compute potential
        Phi = potential_func(self.XX, self.YY)
        
        # Time-step loop
        for t in range(t_max):
            # Compute gradient
            dPhi_dx = np.gradient(Phi, axis=1) / self.dx
            dPhi_dy = np.gradient(Phi, axis=0) / self.dx
            
            # Update field
            i = i - dt * (dPhi_dx + 1j * dPhi_dy)
            
            # Check convergence
            max_gradient = np.max(np.abs(dPhi_dx) + np.abs(dPhi_dy))
            if max_gradient < epsilon:
                print(f"Converged at step {t}")
                break
        
        return i
```

### File 3: `upfm_image_renderer.py`

```python
class FieldRenderer:
    """Render converged field to beautiful image."""
    
    @staticmethod
    def render(field, output_path, style='magnitude_phase'):
        """
        Render field as image.
        
        Styles:
        - 'magnitude_phase': Brightness=magnitude, Hue=phase
        - 'frequency_map': Color by local frequency
        - 'gradient_flow': Magnitude with vector field overlay
        """
        magnitude = np.abs(field)
        phase = np.angle(field)
        
        # Normalize
        mag_norm = (magnitude - magnitude.min()) / (magnitude.max() - magnitude.min() + 1e-6)
        phase_norm = (phase + np.pi) / (2 * np.pi)
        
        if style == 'magnitude_phase':
            # HSV: Hue=phase, Saturation=full, Value=magnitude
            hsv = np.dstack([phase_norm, np.ones_like(phase_norm), mag_norm])
            rgb = colorsys.hsv_to_rgb(hsv)
        
        elif style == 'frequency_map':
            # Local frequency from phase gradients
            phase_grad = np.sqrt(np.gradient(phase, axis=0)**2 + np.gradient(phase, axis=1)**2)
            freq_norm = (phase_grad - phase_grad.min()) / (phase_grad.max() - phase_grad.min() + 1e-6)
            # Colormap: viridis or turbo
            rgb = plt.cm.turbo(freq_norm)
        
        # Convert to uint8 image
        img_uint8 = (rgb * 255).astype(np.uint8)
        
        # Save with high quality
        Image.fromarray(img_uint8).save(output_path, quality=95)
        print(f"Saved: {output_path}")
```

### File 4: `upfm_batch_generator.py`

```python
class ImageBatchGenerator:
    """Generate all wiki images at once."""
    
    def __init__(self, output_dir='wiki/images/upfm'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.potlib = PotentialLibrary()
        self.solver = FieldSolver(grid_size=1024)
        self.renderer = FieldRenderer()
    
    def generate_all(self):
        """Generate all 20 wiki images."""
        
        images = {
            # Foundation & Theory
            'gradient_field_topography': {
                'potential': self.potlib.simple_gaussian,
                'params': {'sigma': 0.5},
                'style': 'magnitude_phase'
            },
            'electron_spiral': {
                'potential': self.potlib.electron_spiral,
                'params': {'f_e': 15, 'r_e': 0.15},
                'style': 'magnitude_phase'
            },
            'photon_spiral': {
                'potential': self.potlib.photon_propagating,
                'params': {'f': 8},
                'style': 'frequency_map'
            },
            'proton_spiral': {
                'potential': self.potlib.proton_spiral,
                'params': {'harmonic_structure': [1, 2, 3]},
                'style': 'magnitude_phase'
            },
            'inward_outward_pair': {
                'potential': self.potlib.dipole_field,
                'params': {'separation': 1, 'strength': 2},
                'style': 'gradient_flow'
            },
            # ... (continue for all 20 images)
        }
        
        for name, config in images.items():
            print(f"\nGenerating: {name}")
            potential = config['potential']
            field = self.solver.solve(
                lambda x, y: potential(x, y, **config['params']),
                t_max=200
            )
            output_file = f"{self.output_dir}/{name}.png"
            self.renderer.render(field, output_file, style=config['style'])
```

---

## Part 4: Integration with Wiki

### Directory structure:
```
wiki/
├── docs/
│   ├── whitepaper-unified-photon-field.md
│   ├── whitepaper-theory.md
│   ├── whitepaper-consciousness-ai.md
│   ├── whitepaper-verification.md
│   └── ...
└── images/
    └── upfm/
        ├── gradient_field_topography.png
        ├── electron_spiral.png
        ├── photon_spiral.png
        ├── proton_spiral.png
        ├── inward_outward_pair.png
        ├── resonance_locking.png
        ├── frequency_spectrum.png
        ├── overlapping_fields.png
        ├── electron_config.png
        ├── proton_config.png
        ├── neutron_config.png
        ├── four_forces_grid.png
        ├── black_hole_reversal_1.png
        ├── black_hole_reversal_2.png
        ├── black_hole_reversal_3.png
        ├── galaxy_formation.png
        ├── cosmic_epochs_1.png (through 14)
        ├── causal_network.png
        ├── consciousness_hierarchy.png
        ├── ai_alignment.png
        ├── entropy_landscape.png
        ├── reduction_chain.png
        ├── tcht_framework.png
        └── cross_domain_6grid.png
```

### Markdown usage:
```markdown
![Electron Spiral Pattern](images/upfm/electron_spiral.png)
*Figure: Confined spiral pattern at frequency f_e. 
Generated via ∂i/∂t = -∇Φ until convergence.*

![Four Forces Comparison](images/upfm/four_forces_grid.png)
*Figure: All four forces as manifestations of gradient descent 
in different potential landscapes.*
```

---

## Part 5: Quality Verification

### Per-image checklist:

- [ ] Visual recognizable as intended concept
- [ ] Field decomposable back to Φ
- [ ] No implicit agency (pure gradient consequence)
- [ ] Scale-invariant (same rendering principle works at all zoom levels)
- [ ] Beautiful enough for publication (high resolution, good color balance)
- [ ] Metadata stored (which Φ, which parameters, convergence info)

### Batch-level checklist:

- [ ] All 20 images generated
- [ ] Consistent visual language across images
- [ ] Each image maps to exactly one section
- [ ] Filenames match markdown references
- [ ] README created explaining each image

---

## Part 6: Implementation Roadmap

**Phase 1: Core infrastructure** (2-3 hours)
- Build potential library with 8 core functions
- Build field solver (explicit time-stepping)
- Build basic renderer (magnitude+phase coloring)
- Test on one image

**Phase 2: Complete generation** (4-5 hours)
- Extend potential library (all 20 concepts)
- Optimize renderer (multiple styles, high quality)
- Build batch generator
- Generate all 20 images

**Phase 3: Integration & polish** (2-3 hours)
- Integrate with wiki markdown
- Add image descriptions
- Create README explaining UPFM visual language
- Upload to repository

---

## Summary

**Result:** Beautiful wiki images that are:
- **Irreducibly native** to UPFM (not illustrations, actual field states)
- **Verifiable** (decomposable back to potential functions)
- **Universal** (same principle across all concepts)
- **Gorgeous** (high-resolution, professional quality)
- **Meaningful** (each image teaches irreducible principle)

**Key insight:** The image generation process IS irreducible verification—if we can solve for the field and render it beautifully, the concept is properly encoded in UPFM.
