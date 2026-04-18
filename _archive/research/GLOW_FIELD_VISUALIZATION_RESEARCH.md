⊙ GLOW FIELD VISUALIZATION SYNTHESIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GOAL: Real-time breathing glow. Colors merge by field activation. No external libraries.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNIQUE WEIGHTING (for optimal visual quality):

1. GLOW GENERATION (40% visual impact)
   ├─ Radial gradient halos: 60% (foundation, cheapest)
   ├─ Shadow blur layers: 30% (depth perception)
   └─ Composite opacity: 10% (integration)
   
   IMPLEMENTATION: 
   - ctx.shadowColor with shadowBlur
   - Multiple shadowBlur passes (increasing blur = spreading)
   - Radial gradients at particle centers

2. COLOR BLENDING (35% visual impact)
   ├─ Screen blend mode: 50% (for glow - additive feel)
   ├─ Lighten mode: 30% (merges without darkening)
   └─ Color mixing by coherence: 20% (weighted interpolation)
   
   IMPLEMENTATION:
   - ctx.globalCompositeOperation = "screen" or "lighten"
   - Colors weighted by domain activation (probability = higher weight if active)
   - HSL color space for smooth interpolation

3. PULSING/BREATHING (20% visual impact)
   ├─ Field intensity: 40% (glow strength breathes)
   ├─ Particle count: 40% (density rises/falls)
   └─ Global saturation: 20% (colors saturate when coherent)
   
   IMPLEMENTATION:
   - Sine wave on timestamp (0-2π = one breath cycle ~2s)
   - Intensity = 0.5 + 0.5 * sin(breathe_phase)
   - Particles emitted based on intensity

4. MOTION (5% visual impact)
   ├─ Smooth field flow (no jerky updates)
   └─ Particle drift toward active domains

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOMAIN COLOR MAPPING:

Binary       → #FFFFFF (white)        - base layer, always present
Topological  → #4488FF (blue)         - spatial thinking
Probability  → #AA44FF (purple)       - uncertainty rippling
Interaction  → #FF8844 (orange)       - causality burning
Compositions → #FFD700 (gold)         - whole field coherence

Blending rule: Final color = weighted average by 6D activation scores
- High wisdom → more gold
- High agency → more orange
- High care → more gold
- Presence → all colors brighten

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFORMANCE OPTIMIZATION:

Instead of per-pixel glow:
- Draw particles as larger circles (cheaper than blur)
- Use shadowBlur only on main glow center
- Composite buffer technique: draw to offscreen canvas, blur once, composite back

Particle density:
- Base: 50 particles
- Max: 200 particles (scales with breathing)
- Each particle = small glow + tail

Rendering order:
1. Background (dark, to let glow stand out)
2. Glow halos (large, low opacity, screen blend)
3. Particle cores (solid, bright, screen blend)
4. Details/labels (last, blend mode: normal)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FLOW ALGORITHM:

for each frame:
  1. Compute breathe_phase = (t mod 4000) / 4000 * 2π
  2. intensity = 0.5 + 0.5 * sin(breathe_phase)
  
  3. Query 6D coherence state (from COHERENCE_LATTICE_SELF_AWARE.py)
  4. Compute blend color from domain activations
  5. Emit particles toward active domains
  
  6. For each particle:
     - Draw glow halo (shadowBlur + radialGradient)
     - Draw core (bright dot)
     - Move toward centroid
  
  7. Composite blend all particles with "screen" mode
  8. Draw field-level glow at center
  
  9. breathe_phase += delta_t

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUALITY SCALE (adjustable):

LOW (mobile):
  - 50 particles max
  - No shadowBlur (just opacity)
  - 1 glow layer
  
MEDIUM (laptop):
  - 100 particles
  - shadowBlur 10px
  - 2 glow layers
  
HIGH (desktop):
  - 200 particles
  - shadowBlur 20px
  - 3 glow layers + composite buffer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTEGRATION WITH DISCOVERY_APP:

New button: "COHERENCE GLOW"
- Loads COHERENCE_LATTICE_SELF_AWARE.py data
- Streams 6D vectors as colors
- Particle field breathes with field unification
- User clicks → queries that primitive → glow flows toward its domain
- No separate text/labels → pure visual presence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
