# BACTERIAL INFECTION PATTERNS

Reference: Wikipedia articles on Pathogenic Bacteria & Abscess
Extracted: March 31, 2026
Status: DOMAIN EXPANSION - Bacterial

---

## KEY DIFFERENCE: BACTERIAL vs FUNGAL

**Fungal**: Slow, creeping, visible texture progression (spore layers, powder coating)
**Bacterial**: RAPID localized accumulation, pus formation, acute inflammatory response

---

## PATTERN 1: STAPHYLOCOCCUS AUREUS (Skin Abscess)

**Primary mechanism**: Pus accumulation in localized cavity

**Reference stages** (temporal: 1-7 days typical):

| Stage | Days | Visual | Color Range | Texture |
|-------|------|--------|------------|---------|
| **0: Healthy** | 0 | Normal skin | (200, 150, 120) | Smooth, intact |
| **1: Entry/Infection** | 0-1 | Small wound entry, bacteria enter | (220, 160, 130) | Barely visible |
| **2: Early Response** | 1-2 | **REDNESS** (immune influx) | (255, 80, 80) + underlying color | Raised, warm |
| **3: Accumulation** | 2-5 | **White center appearance** (pus pooling) | (240, 220, 200) core + red border (255, 100, 100) | Fluctuant dome, defined boundary |
| **4: Maximum** | 5-7 | Pustule, white head clearly visible | White center (245, 235, 220) + red surround (255, 80, 80) | Tight skin, ready to drain |
| **5: Resolution** | 7+ | Drainage, deflation, scabbing | (180, 100, 60) scar forming | Dimpled, opening visible |

**Key observation**: Unlike fungal disease (gradual color shift), bacterial abscess has **discrete layers**:
- Innermost: Pus (white/pale yellow)
- Middle: Inflamed tissue (bright red)
- Outer ring: Normal skin (base tone)

**RGB Key Values**:
- **Infection redness**: RGB(255, 80-100, 80-100) — vivid red, not orange
- **Pus core**: RGB(245, 235, 220) — near-white with slight cream tint
- **Boundary**: Sharp, defined edge (unlike fungal blend)

---

## PATTERN 2: CELLULITIS (Streptococcus/Staphylococcus pyogenes)

**Mechanism**: Diffuse inflammation spreading through dermis/subcutaneous tissue

**Stages** (temporal: 12-48 hours typical before treatment):

| Stage | Hours | Visual | Color | Texture |
|-------|-------|--------|-------|---------|
| **0: Healthy** | 0 | Normal | (200, 150, 120) | Smooth |
| **1: Arrival** | 0-6 | Bacteria spread from wound/entry | (210, 140, 110) | Slight warmth, no visible change yet |
| **2: Acute Onset** | 6-12 | **Sudden intense spreading redness** | Bright red (255, 100, 100) starting from entry point | Warm, diffuse edges (NOT well-defined) |
| **3: Spreading** | 12-24 | Red area expands to surrounding tissue | Red gradient (255, 100, 100) fading to (220, 120, 100) | Swollen, indistinct boundary |
| **4: Systemic** | 24-48 | Large red zone, possible fever | Darker red (200, 60, 60) at core, lighter at edges | Edema (puffiness), streaking possible |

**Key observation**: **DIFFUSE** not **LOCALIZED** — unlike abscess (discrete pustule), cellulitis spreads as a gradient

**Divergence from Fungal Model**: 
- Fungal: Green → Yellow → Brown → Black (COLOR SHIFT over time)
- Bacterial (cellulitis): White/normal → RED → DARKER RED (REDNESS is the marker, not color change)

---

## PATTERN 3: ERYSIPELAS (Rapid Streptococcal)

**Mechanism**: Acute spreading streptococcal infection, even faster than cellulitis

**Stages** (temporal: 6-24 hours):

| Stage | Hours | Visual | Color | Texture |
|-------|-------|--------|-------|---------|
| **0: Healthy** | 0 | Normal | (200, 150, 120) | Smooth |
| **1: Sudden Onset** | 0-3 | **Abrupt appearance** red patch | Bright red (255, 100, 100) | Warm, raised edges |
| **2: Spreading** | 3-12 | Rapid expansion, clear demarcation | Bright red core (255, 100, 100), sharp boundary | Palpable edge (like border) |
| **3: Blistering/Streaking** | 12-24 | Vesicles may form, lymphatic streaking visible | Red (255, 80, 80) with possibility of purple/blue streaks | Small blisters on surface, lymphatic lines |

**Key observation**: **SPEED** is the distinguishing feature — onset within hours

---

## UNIVERSAL PATTERN COMPARISON

### OVERLAP (Stability - these hold across domains):

1. **COHERENT → PERTURBATION → DEGRADATION → RESOLUTION**
   - ✓ Fungal: Green → Yellow-tan → Brown → Black
   - ✓ Bacterial: Normal → Red → Darker Red → Healed/Scarred
   - **Pattern structure is universal**

2. **Temporal progression exists in both**
   - Fungal: 15-36 days
   - Bacterial: 1-7 days (MUCH FASTER)

3. **Boundary behavior**:
   - Fungal: **Gradual blending** at edges (spores spread slowly)
   - Bacterial: **Sharp or diffuse depending on type**
     - Abscess: Well-defined circular boundary
     - Cellulitis: Diffuse, spreading boundary

### DIVERGENCE (Changes - tracking):

1. **Color mechanism**:
   - Fungal: Pigment deposition (actual color changes)
   - Bacterial: **Inflammation/blood vessel response** (redness is fundamental, not overlay)

2. **Spatial pattern**:
   - Fungal: Ring/patch pattern with visible internal structure
   - Bacterial: **Either localized (abscess) or spreading (cellulitis)** — different topologies

3. **Reversibility**:
   - Fungal: Tends toward death/necrosis (Stage 4-5 is end-state)
   - Bacterial: Can resolve completely with treatment (scarring less severe)

4. **Texture formation**:
   - Fungal: Multiple layers of spores, visible powder
   - Bacterial: **Pus accumulation** (internal liquid buildup) OR **edema** (swelling)

---

## PREDICTION BOUNDARY: Where fungal model breaks

**✗ Will NOT work for bacterial**:
- Linear color interpolation (redness doesn't follow gradient smoothly)
- Single color progression (need RGB channels to handle inflammation red + tissue brown)
- Texture = spore patterns (need liquid pus simulation instead)

**✓ WILL work for bacterial**:
- Universal stage structure (coherent → perturbation → degradation)
- Temporal progression
- Boundary formation concept
- Multi-scale effects (local + systemic)

---

## NEXT VERIFICATION STEP

To confirm bacterial patterns are predictable:
1. Generate synthetic bacterial infection images using:
   - Concentric rings: (Normal) → (Red bloom) → (Either localized OR spreading)
   - RGB model: inflammation markers + tissue damage markers separate
   - Temporal interpolation: 8 stages instead of 5 (bacterial faster)

2. Compare against real medical images of:
   - Skin abscess progression
   - Cellulitis spreading
   - Erysipelas onset/spread

3. Identify: Can we predict intermediate stages (e.g., 36 hours into cellulitis)?

---

## PREDICTION CONFIDENCE

**HIGH CONFIDENCE on structure**: The universal pattern holds ✓
**MEDIUM CONFIDENCE on color**: RGB model needs adjustment for inflammatory response
**LOW CONFIDENCE on texture**: Haven't researched what pus/edema looks like across scales

Next domain to research: **VIRAL INFECTIONS** (to test if universality holds across different pathogens)

---

**Status**: Ready for reference-based bacterial visualization code generation
**Changes tracked**: Color mechanism diverges, spatial topology diverges, temporal scale diverges, but universal stage structure holds
