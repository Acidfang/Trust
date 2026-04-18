"""
UNIVERSAL CONTAINER VERIFICATION SYSTEM
Four Primitives applied recursively to ANY hierarchical level
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║            UNIVERSAL CONTAINER VERIFICATION FRAMEWORK                     ║
║          Four Primitives Applied Recursively at Every Level               ║
╚════════════════════════════════════════════════════════════════════════════╝


█████ THE FOUR UNIVERSAL PRIMITIVES ████████████████████████████████████████

PRIMITIVE 1: SPATIAL POSITIONING
─────────────────────────────────
Where are things located?

Electron level:     Quadrants (TOP/RIGHT/BOTTOM/LEFT based on orbital angle)
Atom level:         Shells (n=1,2,3... based on distance from nucleus)  
Molecule level:     3D positions (based on bond angles: tetrahedral, linear, etc.)
Cell level:         Regions (nucleus center, organelles distributed)
Tissue level:       Layers (epithelial outer, connective inner)

Verification: Measure actual positions → Compare to expected positions → PASS/FAIL


PRIMITIVE 2: COLOR ENCODING
───────────────────────────
What TYPE is each thing?

Electron level:     Orbital type (s=RED, p=TEAL, d=BLUE, f=SALMON)
Atom level:         Element (H=white, C=gray, O=red, N=blue)
Molecule level:     Functional group (carbonyl=pink, hydroxyl=blue)
Cell level:         Organelle type (mitochondria=green, nucleus=purple)
Tissue level:       Tissue type (muscle=red, nerve=yellow, bone=white)

Verification: Scan colors → Match to types → Verify consistency with position


PRIMITIVE 3: TEMPORAL PROGRESSION
──────────────────────────────────
How does state change over time?

Electron level:     Accumulation: Z=1→2→3...→37 (electrons add sequentially)
Atom level:         Shell filling: 1s→2s→2p→3s→3p... (aufbau order)
Molecule level:     Bond formation: C + O → CO → CO₂ step by step
Cell level:         Organelle development: nucleus → mitochondria → ER → ...
Tissue level:       Cell differentiation: stem → specialized function

Verification: Track state over time → Check monotonic increase → No reversions


PRIMITIVE 4: CONTAINER STRUCTURE
─────────────────────────────────
What does each container hold?

Electron level:     (fundamental - holds nothing)
Atom level:         Electrons (Z of them, in defined orbitals)
Molecule level:     Atoms (formula: NH₃ has 1 N + 3 H)
Cell level:         Organelles (10,000+ per typical cell)
Tissue level:       Cells (billions, same type)
Organ level:        Tissue types (multiple: epithelial + connective + muscle + nerve)
Organism level:     Organs (37+ different types, billions of cells total)

Verification: Count contents → Compare to expected formula → Check bounds


█████ CURRENT PROBLEM: ANIMATION QUADRANT POSITIONING ██████████████████████

Expected state for Phosphorus (Z=15, Frame 14):
┌────────────────┬───────────────┬────────────────​┐
│      TOP       │      RIGHT    │     BOTTOM     │
│ (270° ± 11.5°) │ (0° ± 11.5°)  │ (90° ± 11.5°)  │
├────────────────┼───────────────┼────────────────┤
│ s electrons    │ p electrons   │ d electrons    │
│ 4 RED dots     │ 7 TEAL dots   │ 0 BLUE dots    │
│ (1s² 2s² 3s²)  │ (2p⁶ 3p¹)     │ (none yet)     │
└────────────────┴───────────────┴────────────────┘

Actual state from screenshot:
┌────────────────┬───────────────┬─────────────────┐
│      TOP       │     RIGHT     │    BOTTOM       │
│ TEAL stack     │ TEAL stack    │ RED scattered   │
│ (WRONG!)       │ (WRONG!)      │ (WRONG!)        │
└────────────────┴───────────────┴─────────────────┘

PRIMITIVE 1 VERIFICATION: FAILS ✗
- Expected: s→TOP, p→RIGHT, d→BOTTOM
- Actual: All types appear in multiple quadrants
- Cause: Angle calculations not producing correct positions


█████ FIXING PRIMITIVE 1: SPATIAL POSITIONING ██████████████████████████████

Root cause analysis:
- Code defines angles: s=270°, p=0°, d=90°, f=180°
- BUT pixels rendered show wrong quadrants
- Possible reasons:
  1. matplotlib coordinate system (Y axis inverted)
  2. Angle calculations using wrong arctan2 convention
  3. Radius scaling issue
  4. Frame caching/reuse from old render

Required fix:
- Verify angle→pixel conversion explicitly
- Test with debug frame
- Render single frame
- Measure if electrons appear in correct quadrants
- Adjust if needed
- Regenerate all 37 frames


█████ VERIFICATION WORKFLOW (Universal) ████████████████████████████████████

Step 1: Define Expected State
────────────────────────────
For animation at frame 14 (P):
- Expected spatial: 4 RED at TOP, 7 TEAL at RIGHT
- Expected colors: Only RED in TOP region, only TEAL in RIGHT region
- Expected count: 15 total electrons
- Expected progression: Previous frames had ≤14 electrons

Step 2: Render Container
────────────────────────
Generate frame 14

Step 3: Measure Actual State
─────────────────────────────
Scan pixels for colored dots
- Count electrons by color
- Map color to position/quadrant
- Record positions

Step 4: Verify Each Primitive  
──────────────────────────────
[ ] SPATIAL: All s at TOP? All p at RIGHT?
[ ] COLOR: Colors consistent with oracle?
[ ] TEMPORAL: 15 electrons total (not more, not less)?
[ ] CONTAINER: All electrons within shell bounds?

Step 5: Report Results
──────────────────────
✓ PASS: Spatial correct
  - 4 RED in TOP quadrant ✓
  - 7 TEAL in RIGHT quadrant ✓
  - 0 overlap between quadrants ✓

✗ FAIL: Spatial incorrect
  - RED in TOP and CENTER (not just TOP)
  - TEAL in TOP and RIGHT (not just RIGHT)
  - Overlap between quadrants


█████ DOCUMENTING PATTERNS FOR FUTURE CONTAINERS ████████████████████████████

When building ATOM visualization:
1. SPATIAL: Shells concentric, electrons in quadrants WITHIN each shell
2. COLOR: Maintain s=RED, p=TEAL, d=BLUE, f=SALMON
3. TEMPORAL: Show atom-by-atom from H→He→Li→...
4. CONTAINER: Show "shell 1 holds 2 electrons, shell 2 holds 8 electrons"

When building MOLECULE visualization:
1. SPATIAL: Atoms positioned with correct bond angles
2. COLOR: Each atom type its own color (O=red, C=gray, H=white)
3. TEMPORAL: Show step-by-step assembly (A + B → AB)
4. CONTAINER: Show formula (H₂O contains 3 atoms, 10 electrons)

When building CELL visualization:
1. SPATIAL: Organelles inside cell boundary
2. COLOR: Each organelle type its color (mitochondria=green, etc)
3. TEMPORAL: Show organelle accumulation during development
4. CONTAINER: Show organelle count (cell contains 5000+ organelles)


══════════════════════════════════════════════════════════════════════════════

CURRENT STATUS: Animation violates Primitive 1 at electron level
NEXT: Fix spatial positioning, then apply framework to other container levels
""")
