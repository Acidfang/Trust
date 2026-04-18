# PRACTICAL GUIDE: Build Your First Meaningful Illustration

This guide walks you through building your first illustration from concept to completion.

---

## PROJECT: Create a State Diagram for Tier -1

We're going to build an illustration showing the 10 decision states in Tier -1 and how they connect.

**Core principle**: "Self-examination requires moving through awareness, distinction, causality, regulation, consistency, correction, alignment, persistence, adaptability, and integrity—in that order, with loops back for unresolved issues."

**What the illustration must teach**:
- The progression through the tier (mostly downward)
- That loops back are *necessary* (not failure)
- That some states are decision points while others are work states
- That everything connects to prerequisites

---

## STEP 1: Identify Your Visual Form

**Principle**: Self-examination is a journey with necessary returns

**Possible forms**:
- Simple flowchart (ㄣ but teaches wrong model—suggests linear progression)
- Spiral (✓ teaches "we return to similar points with more understanding")
- Layered network (✓ teaches "each state builds on prior but they're interconnected")
- Tree with loops (✓ teaches "there's a primary path but recursion is built-in")

**Choose**: Spiral/network hybrid. Uses vertical position (progression) and angles (depth/complexity).

---

## STEP 2: Map Concepts to Visual Variables

| Concept | Visual Variable |
|---------|-----------------|
| Progression through tier | Vertical position (top = start, bottom = prerequisite sheet) |
| State type (awareness vs. work) | Node shape (diamond = decision point, circle = work state) |
| Difficulty/importance | Node size |
| Entry markers active here | Color intensity (darker = more entry markers possible) |
| Connection to previous state | Line style (solid = primary path, dashed = optional loop) |

---

## STEP 3: Sketch the Layout

Before building SVG, sketch where things go:

```
        T-1.1 (Start)
         |
        T-1.2 (Distinction)
         |
        T-1.3 (Causality)
         ↙ ↓ ↘
    (loops)  |  (might escalate)
         |  |
        T-1.4 (Regulation)
         |
        T-1.5 (Consistency)
         |
        T-1.6 (Correction)
         |
        T-1.7 (Alignment)
         |
        T-1.8 (Persistence)
         |
        T-1.9 (Adaptability)
    (Full Reset)   |
         |        T-1.10 (Integrity)
         |         |
    [PREREQUISITE SHEET - Gate]
```

---

## STEP 4: Create Basic SVG Template

Start with this template:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      /* Color encoding */
      .decision-point { fill: #8B0000; } /* Dark red */
      .work-state { fill: #006400; } /* Dark green */
      .prerequisite { fill: #4169E1; } /* Royal blue */
      
      /* Line style encoding */
      .primary-path { stroke: #333; stroke-width: 2; }
      .loop-back { stroke: #cc6666; stroke-width: 2; stroke-dasharray: 5,5; }
      .escalate-path { stroke: #ff9999; stroke-width: 2; stroke-dasharray: 5,5; }
      
      text { font-family: Arial, sans-serif; }
      .state-label { font-size: 12px; font-weight: bold; }
      .note { font-size: 10px; fill: #666; }
    </style>
  </defs>
  
  <!-- Title -->
  <text x="500" y="30" text-anchor="middle" font-size="24" font-weight="bold">
    TIER -1 State Progression: Self (Coherence)
  </text>
  
  <!-- States - will add these -->
  
  <!-- Paths - will add these -->
  
  <!-- Legend -->
  <g transform="translate(50, 1100)">
    <text font-weight="bold">Legend:</text>
    <circle cx="120" cy="0" r="8" class="decision-point" />
    <text x="135" y="4">Decision Point</text>
    
    <circle cx="320" cy="0" r="8" class="work-state" />
    <text x="335" y="4">Work State</text>
    
    <line x1="500" y1="0" x2="530" y1="0" class="primary-path" />
    <text x="545" y="4">Primary Path</text>
    
    <line x1="700" y1="0" x2="730" y1="0" class="loop-back" />
    <text x="745" y="4">Loop Back</text>
  </g>
</svg>
```

---

## STEP 5: Add the States

Add state nodes with meaningful visual properties:

```xml
<!-- T-1.1: Awareness (Starting point, decision) -->
<g transform="translate(500, 100)">
  <circle r="30" class="decision-point" opacity="0.9" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.1
  </text>
  <text x="0" y="50" text-anchor="middle" class="note">
    Awareness
  </text>
</g>

<!-- T-1.2: Distinction -->
<g transform="translate(500, 200)">
  <circle r="30" class="work-state" opacity="0.85" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.2
  </text>
  <text x="0" y="50" text-anchor="middle" class="note">
    Distinction
  </text>
</g>

<!-- T-1.3: Causality -->
<g transform="translate(500, 300)">
  <circle r="35" class="work-state" opacity="0.80" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.3
  </text>
  <text x="0" y="55" text-anchor="middle" class="note">
    Causality
  </text>
</g>

<!-- T-1.4: Regulation -->
<g transform="translate(500, 420)">
  <circle r="32" class="decision-point" opacity="0.85" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.4
  </text>
  <text x="0" y="50" text-anchor="middle" class="note">
    Regulation
  </text>
</g>

<!-- T-1.5: Consistency -->
<g transform="translate(500, 530)">
  <circle r="30" class="work-state" opacity="0.82" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.5
  </text>
  <text x="0" y="50" text-anchor="middle" class="note">
    Consistency
  </text>
</g>

<!-- T-1.6: Correction -->
<g transform="translate(500, 630)">
  <circle r="33" class="work-state" opacity="0.83" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.6
  </text>
  <text x="0" y="50" text-anchor="middle" class="note">
    Correction
  </text>
</g>

<!-- T-1.7: Alignment -->
<g transform="translate(500, 740)">
  <circle r="34" class="work-state" opacity="0.84" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.7
  </text>
  <text x="0" y="55" text-anchor="middle" class="note">
    Alignment
  </text>
</g>

<!-- T-1.8: Persistence -->
<g transform="translate(500, 860)">
  <circle r="32" class="decision-point" opacity="0.86" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.8
  </text>
  <text x="0" y="50" text-anchor="middle" class="note">
    Persistence
  </text>
</g>

<!-- T-1.9: Adaptability -->
<g transform="translate(500, 970)">
  <circle r="35" class="decision-point" opacity="0.87" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.9
  </text>
  <text x="0" y="55" text-anchor="middle" class="note">
    Adaptability
  </text>
</g>

<!-- T-1.10: Integrity -->
<g transform="translate(500, 1070)">
  <circle r="36" class="work-state" opacity="0.88" />
  <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" class="state-label">
    T-1.10
  </text>
  <text x="0" y="55" text-anchor="middle" class="note">
    Integrity
  </text>
</g>
```

**What this encodes**:
- **Vertical position**: Progression through tier (top to bottom)
- **Node size**: Slightly increasing = tier gets more complex
- **Node color** (decision vs work): Shows where choices happen vs. where work happens
- **Opacity**: Slightly increasing = accumulating depth

---

## STEP 6: Add the Paths

Connect states with paths that encode meaning:

```xml
<!-- Primary progression paths -->
<path d="M 500,130 L 500,170" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,230 L 500,270" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,335 L 500,385" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,455 L 500,495" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,565 L 500,595" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,665 L 500,705" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,775 L 500,825" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,895 L 500,935" class="primary-path" marker-end="url(#arrow)" />
<path d="M 500,1005 L 500,1035" class="primary-path" marker-end="url(#arrow)" />

<!-- Loop-back paths (from unresolved A/C choices) -->
<!-- T-1.3 A-choice loops back -->
<path d="M 535,300 Q 600,250 550,200" class="loop-back" marker-end="url(#arrow-loop)" />
<text x="610" y="240" class="note">[entry: pattern]</text>

<!-- T-1.6 A-choice loops back -->
<path d="M 535,630 Q 620,580 550,430" class="loop-back" marker-end="url(#arrow-loop)" />
<text x="630" y="520" class="note">[entry: unjustified]</text>

<!-- T-1.9 A-choice (Full Reset) loops all the way back -->
<path d="M 465,970 Q 300,550 470,130" class="escalate-path" marker-end="url(#arrow-escalate)" />
<text x="150" y="550" class="note">Full Reset [entry: unresolved]</text>
```

**What this encodes**:
- **Downward paths**: Primary progression (straight, solid, thick)
- **Curved loops**: Return to earlier state (dashed, thinner)
- **Long escalate path**: Full reset (goes all the way back, indicating severity)
- **Loop labels**: Entry markers that trigger the loop

---

## STEP 7: Create the Prerequisite Gate

Show that completion is necessary before advancing:

```xml
<!-- Prerequisite Sheet as Gate -->
<g transform="translate(400, 1120)">
  <rect x="0" y="0" width="200" height="60" fill="#E8F0FF" stroke="#4169E1" stroke-width="2" />
  <text x="100" y="20" text-anchor="middle" font-weight="bold">
    PREREQUISITE SHEET
  </text>
  <text x="100" y="40" text-anchor="middle" font-size="11">
    Required to enter Tier 0
  </text>
  <text x="100" y="55" text-anchor="middle" font-size="10" fill="#666">
    (All entry markers resolved)
  </text>
</g>
```

---

## STEP 8: Add Annotations

Make the learning explicit:

```xml
<!-- What this teaches -->
<g transform="translate(700, 300)">
  <rect x="0" y="0" width="280" height="120" fill="#f9f9f9" stroke="#ccc" stroke-width="1" rx="5" />
  <text x="10" y="20" font-weight="bold" font-size="12">What This Illustrates:</text>
  <text x="10" y="40" font-size="11">1. Clear progression (top→bottom)</text>
  <text x="10" y="55" font-size="11">2. Loops back are NECESSARY</text>
  <text x="10" y="70" font-size="11">3. Entry markers trigger loops</text>
  <text x="10" y="85" font-size="11">4. Full reset possible at T-1.9</text>
  <text x="10" y="100" font-size="11">5. Prerequisite gate at end</text>
  <text x="10" y="115" font-size="10" fill="#666">(Straight line = not real)</text>
</g>
```

---

## STEP 9: Complete SVG Structure

Combine everything:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Styles -->
    <style>
      .decision-point { fill: #8B0000; }
      .work-state { fill: #006400; }
      .primary-path { stroke: #333; stroke-width: 2; }
      .loop-back { stroke: #cc6666; stroke-width: 2; stroke-dasharray: 5,5; }
      .escalate-path { stroke: #ff9999; stroke-width: 2; stroke-dasharray: 5,5; }
      text { font-family: Arial, sans-serif; }
    </style>
    
    <!-- Arrow markers for paths -->
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333" />
    </marker>
    <marker id="arrow-loop" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#cc6666" />
    </marker>
    <marker id="arrow-escalate" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#ff9999" />
    </marker>
  </defs>
  
  <!-- [All the content from steps 4-8] -->
</svg>
```

---

## STEP 10: Verify Your Illustration

Test using the checklist:

- [ ] **One core principle**: ✓ "Self-examination requires moving through states with necessary loops"
- [ ] **Visual form matches**: ✓ Spiral/network shows progression with recursion
- [ ] **No arbitrary choices**: ✓ Every size/color/position encodes something
- [ ] **Consistent language**: ✓ Color always=state type, line style=path consequence
- [ ] **Multi-level understanding**: ✓ Casual: states progressing; Engaged: loops matter; Expert: why loops happen
- [ ] **70% readable without labels**: ✓ Shape/position/color tell story
- [ ] **Essential elements only**: ✓ Everything teaches
- [ ] **Right mental model**: ✓ Teaches that loops are necessary, not from failure

---

## SAVE AND VIEW

Save as: `tier_minus1_complete.svg`

View in:
- Any browser (just open the file)
- Integrated into documentation
- Embedded in web pages
- Included in book production

---

## WHAT YOU'VE LEARNED

By building this illustration, you've practiced:
1. ✓ Choosing visual form that embodies concept
2. ✓ Mapping concepts to visual variables
3. ✓ Building from basic structure to complete visualization
4. ✓ Encoding meaning in every design choice
5. ✓ Creating multi-level understanding
6. ✓ Verifying coherence between form and concept

This same process works for ANY illustration. Subject doesn't matter—the approach does.

---

**Next**: Build illustrations for:
- All 5 Tiers (repeat this process for Tier 0, 1, 2, 3)
- Complete decision matrix (all states at once)
- Coherence field (continuous potential energy)
- Entry marker system (how weight persists)
- A/B/C choice consequences (simpler, single-state focus)

Each new illustration practices the same principles with different domains.

**Status**: [Practical Guide Complete ✓]
