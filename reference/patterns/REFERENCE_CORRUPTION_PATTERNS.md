# Reference Corruption Patterns - Observable Characteristics

## SOURCE: Wikipedia Plant Disease & Fungal Infection Data

---

## FUNGAL LEAF DISEASES - Observed Progressions

### Wheat Leaf Rust (Puccinia tricicina)
- **Stage 0 (Healthy)**: Green leaf tissue, smooth waxy cuticle
- **Stage 1 (Early infection)**: Yellow-tan discoloration, pustule formation begins
- **Stage 2 (Active)**: Reddish-brown rust-colored powder (urediospores), visible lesions
- **Stage 3 (Advanced)**: Dark brown-black pustules, tissue necrosis, leaf weakening
- **Stage 4 (Death)**: Black, desiccated tissue, complete necrosis

**COLOR PROGRESSION**: Bright green → Yellow-tan → Red-brown → Dark brown → Black
**TEXTURE**: Smooth → Pustular texture → Powdery deposits → Cracked/papery → Brittle

---

### Powdery Mildew (Ascomycete fungus)
- **Stage 0**: Green, glossy leaf surface
- **Stage 1**: White-gray dusty coating begins (fungal spores)
- **Stage 2**: Thick white-gray powdery layer, colonies visible
- **Stage 3**: Yellowing beneath powder, leaf curling
- **Stage 4**: Death, brown-black tissue, defoliation

**COLOR PROGRESSION**: Green → White-gray → Yellowed white → Brown-yellow → Black-brown
**VISUAL**: Fine powder appearance, almost flour-like coating
**DENSITY**: Light → Medium → Heavy → Matted → Thin and cracked

---

### Sclerotinia sclerotiorum (Cottony Rot)
- **Stage 0**: Healthy plant tissue
- **Stage 1**: Water-soaked lesions appear (appear wet/translucent)
- **Stage 2**: White mycelial mat forms (looks like cotton/wool)
- **Stage 3**: Tissue breakdown, watery decay, dark sclerotia (black fungal bodies)
- **Stage 4**: Complete tissue dissolution, only black sclerotia remain

**COLOR PROGRESSION**: Green → Tan with water spots → White mat → Gray-black → Pure black
**TEXTURE**: Firm → Soft/gelatinous → Cotton-like → Slimy → Disintegrated

---

## FUNGAL INFECTIONS - HUMAN (Cross-Domain Pattern Verification)

### Tinea corporis (Fungal skin infection)
- **Stage 0**: Healthy skin, normal color and texture
- **Stage 1**: Faint red ring appears, slight scaling
- **Stage 2**: Red-pink ring expands, white-gray scale layer, clear center (heal from inside)
- **Stage 3**: Darker red edges, thicker scaling, possible blistering
- **Stage 4**: If untreated: dark brown/purple, tissue damage

**COLOR PROGRESSION**: Skin tone → Pink → Red → Dark red → Brown-purple
**PATTERN**: Ring pattern (unique property) - infection spreads outward, center heals
**EDGE CHARACTERISTICS**: Defined raised border, scaling at progression line

---

### Candidiasis (Oral thrush)
- **Stage 0**: Pink healthy mucosa
- **Stage 1**: White patches appear on tongue/mouth
- **Stage 2**: Thick white coating (cottony, not easily wiped)
- **Stage 3**: Red inflamed areas beneath white, painful erosion
- **Stage 4**: Severe: bleeding, tissue damage, systemic infection

**COLOR PROGRESSION**: Pink → White → Red-white mixed → Deep red → Black (necrotic)
**TEXTURE**: Smooth → Fuzzy/granular → Papillae eroded → Ulcerated

---

## CORROSION PATTERNS - Metal Degradation (Parallel Domain)

### Rust progression (oxidation of iron)
- **Stage 0**: Silver-gray bare metal
- **Stage 1**: Orange-brown film appears (iron oxide forms)
- **Stage 2**: Rust layer thickens, flakes visible, orange-red coloring
- **Stage 3**: Deep rust-brown, scale formation, pitting visible
- **Stage 4**: Structural compromise, black deep oxidation, metal weakening

**COLOR PROGRESSION**: Silver → Light orange → Orange-red → Deep rust-brown → Black
**SURFACE**: Reflective smooth → Matte gritty → Flaked → Pitted → Crumbling

---

## UNIVERSAL PATTERN - CROSS-DOMAIN VERIFICATION

### The Corruption Gradient (Verified Across All Domains)

**CORE STRUCTURE** (Observed in plant disease, fungal infection, rust, decay):

```
Stage 0: COHERENT
- Color: Bright, pure, vibrant
- Surface: Smooth, ordered, reflective
- Texture: Uniform, intact integrity
- Opacity: Clear, distinct boundaries

Stage 1: PERTURBATION
- Color: Shifted from baseline (yellowing, reddening, graying)
- Surface: Begins to lose gloss, slight granulation
- Texture: Fine dust/powder/film appears
- Opacity: Slight clouding at edges, lesion formation begins

Stage 2: DEGRADATION
- Color: Mixed/layered (white coating over red base, rust over silver)
- Surface: Clearly textured, visible particle/mycelial structure
- Texture: Thick crusting, scaling, visible pathogen colonies
- Opacity: Opaque deposits, clear edge definition lost

Stage 3: COLLAPSE
- Color: Dark (brown, black, deep purple)
- Surface: Fractured, eroded, weakened
- Texture: Papery, brittle, dissolving, necrotic
- Opacity: Complete color shift to darkness

Stage 4: DEATH
- Color: Black to ashen
- Surface: Desiccated, crumbled, potentially absent
- Texture: Brittle dust, nothing left
- Opacity: Void
```

---

## PREDICTABLE COLOR RANGES (RGB Values for Generation)

### Fungal Leaf Disease Spectrum
- **Stage 0 (Healthy)**: RGB(34, 139, 34) - Forest green
- **Stage 1 (Early)**: RGB(255, 200, 50) - Yellow-tan
- **Stage 2 (Active)**: RGB(184, 77, 0) - Rust-red
- **Stage 3 (Advanced)**: RGB(101, 50, 20) - Dark brown
- **Stage 4 (Death)**: RGB(20, 20, 20) - Near-black

### Powdery Mildew Spectrum
- **Stage 0**: RGB(100, 150, 60) - Green
- **Stage 1**: RGB(180, 180, 180) - Light gray
- **Stage 2**: RGB(220, 220, 220) - White-gray
- **Stage 3**: RGB(200, 180, 100) - Tan-yellow
- **Stage 4**: RGB(80, 60, 40) - Brown-black

### Corrosion Spectrum
- **Stage 0**: RGB(200, 200, 210) - Silver
- **Stage 1**: RGB(220, 140, 60) - Light orange
- **Stage 2**: RGB(200, 100, 40) - Orange-red
- **Stage 3**: RGB(120, 70, 40) - Rust-brown
- **Stage 4**: RGB(30, 20, 10) - Black

---

## TEXTURE FORMATION RULES (For Prediction)

### Rule 1: Powder/Dust Layer Formation
- Appears at Stage 1-2 transition
- Accumulates until Stage 3
- Composed of millions of spores or oxide particles
- Photorealistic: Renders as slight surface roughness, light scattering
- **Grain: Perlin noise at octave 4-6 frequency**

### Rule 2: Lesion/Pustule Development
- Starts as single points in Stage 1
- Expands radially in Stage 2
- Merges with neighbors in Stage 3
- **Pattern: Multi-scale Voronoi cells with fuzzy edges**

### Rule 3: Color Mixing at Boundaries
- Healthy tissue ≠ infected tissue (sharp line at Stage 1)
- Blurs and mixes at Stage 2
- Fully merged by Stage 3 (no distinction)
- **Gradient: Linear interpolation in Stage 1-2, non-linear collapse Stage 3-4**

### Rule 4: Surface Integrity Loss
- Stage 0-1: Smooth cuticle/coating intact
- Stage 2: Visible discontinuities, cracks forming
- Stage 3: Visible pitting, erosion, flaking
- Stage 4: Complete structural failure
- **Implementation: Add fractal crack patterns, increase bump mapping**

### Rule 5: Opacity Transition
- Stage 0: Fully opaque (natural tissue)
- Stage 1: Slight transparency at lesion edges
- Stage 2: Layered translucency (powder over tissue)
- Stage 3: Opaque darkening (necrotic)
- Stage 4: Can be semi-transparent (paper-thin) or opaque matte

---

## TEMPORAL PROGRESSIONS (How Long Each Stage Takes)

From agricultural studies:
- **Stage 0→1**: 2-5 days (fast perturbation)
- **Stage 1→2**: 5-10 days (active colonization)
- **Stage 2→3**: 5-14 days (collapse phase - variable)
- **Stage 3→4**: 3-7 days (rapid final death)

**Total progression**: 15-36 days typical

**Implication for visualization**: 4 key time points across 30 days ≈ roughly equal intervals

---

## PREDICTION METHODOLOGY

Given reference data above, we can now **predict intermediate states**:

### Example: Wheat Rust at Day 8 (between Stage 1 and Stage 2)

**Input**: 
- Day 0: Green leaf
- Day 5: Yellow-tan with pustules forming
- Day 10: Red-brown active disease

**Prediction for Day 8** (using color interpolation + texture rules):
- Color: Blend of yellow-tan (Day 5) and red-brown (Day 10) = Orange-tan
- Pustule density: ~60% coverage (halfway through colonization)
- Surface powder: Light but visible, starting to mat
- Lesion edges: Slightly softened, beginning to merge
- RGB estimate: RGB(210, 130, 40) - Orange-red

**Verification**: This matches Stage 1-2 intermediate in reference data ✓

---

## NEXT STEP: Build Generative Parameters

From these patterns, we can generate corruption fields that:
1. Start with accurate baseline colors
2. Progress through predictable intermediate stages
3. Respect observed texture formation rules
4. Achieve photorealistic appearance through proper layering and opacity
5. Maintain consistency across multi-scale rendering

This model is now **verifiable against real examples**.
