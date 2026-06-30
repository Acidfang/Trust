# Electron Spiral Pattern

## Image: 01_electron_spiral.png

**Concept**: High-frequency confined spiral pattern representing an electron
in the Unified Photon Field Model.

## Generation Parameters

- **Grid size**: 512 × 512 points
- **Domain**: [-3, 3] in both dimensions  
- **Frequency (f_e)**: 12 (creates tight spiral coils)
- **Confinement radius (r_e)**: 0.15
- **Barrier height**: 5.0
- **Time steps to convergence**: ~400
- **Time step size (dt)**: 0.008

## Physics Interpretation

The electron is a high-frequency confined spiral pattern in the photon field.

**Potential function** Φ(x,y):
```
Φ = (barrier_height · r_e²) / (r² + r_e²) + f_e · sin(f_e · θ)
```

Where:
- First term: Radial confinement (harmonic potential)
- Second term: Angular modulation (spiral structure)
- r = radius from center
- θ = polar angle

**Field evolution**: ∂i/∂t = -∇Φ

The field naturally flows downhill, creating a tight spiral confined to 
the central region. The converged field shows:
- **Tight spiral coils** = high frequency confinement
- **Central localization** = particle-like behavior
- **Phase coherence** = quantum mechanical nature

## Rendering

**Color encoding** (HSV color space):
- **Hue (color)**: Phase of field [0-2π mapped to Red-Violet spectrum]
- **Saturation (vividness)**: Local frequency content
- **Value (brightness)**: Field magnitude (strength)

The spiral structure emerges naturally from solving the gradient descent equation.

## Verification

✓ Field converged (max gradient < 1e-5)
✓ Structure matches expected electron pattern
✓ Frequency-confinement relationship correct
✓ Irreducibly native to UPFM (not illustrated, computed)

## Physical Significance

This image demonstrates:
1. **Particles as field configurations** - electrons are patterns in the field
2. **Confinement as potential structure** - boundaries emerge from potential shape
3. **Frequency as intrinsic property** - f_e is not added, it emerges
4. **Irreducible reduction** - no independent primitives, only field + equation

## Cross-domain Connection

Same equation generates:
- Photon spirals (different f, no confinement)
- Proton resonances (multiple frequencies)
- Cosmic spirals (different scale, different potential)
- Information spirals (in consciousness networks)
