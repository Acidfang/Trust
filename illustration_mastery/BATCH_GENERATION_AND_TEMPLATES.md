# Build Any Tier Illustration Using Templates

You now have three ways to create illustrations:

1. **Manual SVG** - Handcraft the SVG directly (complete control)
2. **Python Generator** - Use the template class to generate (repeatable, scalable)
3. **Hybrid** - Generate base, then hand-edit specific elements

---

## APPROACH 1: Adapt the Python Generator

The `generate_tier_minus1.py` is a template. Adapt it for other tiers:

### For Tier 0 (States T0.1 through T0.?)

```python
# Change the class name and states list

class TierZeroIllustrator(TierMinusOneIllustrator):
    def __init__(self):
        super().__init__()
        
        # Replace states with Tier 0 states
        self.states = [
            {'id': 'T0.1', 'name': 'Acceptance', 'y': 100, 'type': 'decision', 'size': 30},
            {'id': 'T0.2', 'name': 'Recognition', 'y': 200, 'type': 'work', 'size': 31},
            # ... continue with all Tier 0 states
        ]
        
        # Update entry markers and loops for Tier 0
        self.loop_backs = [
            {'from': 3, 'to': 1, 'marker': 'resistance', 'style': 'loop-back'},
            # ... your Tier 0 loops
        ]
```

### For Tier 1, 2, 3 (Same pattern)

Just change:
- Class name: `TierOneIllustrator`, `TierTwoIllustrator`, `TierThreeIllustrator`
- Title in `build_header()`
- States list
- Loop backs list
- Output filename

---

## APPROACH 2: Minimal Generator Template

If you want simpler code for quick illustrations:

```python
from pathlib import Path

def create_state_illustration(tier_name, states, loops, output_file):
    """Generate any tier illustration from state definitions"""
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="{200 + len(states) * 100}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .decision-point {{ fill: #8B0000; }}
      .work-state {{ fill: #006400; }}
      .primary-path {{ stroke: #333; stroke-width: 2; }}
      .loop-back {{ stroke: #cc6666; stroke-width: 2; stroke-dasharray: 5,5; }}
    </style>
  </defs>
  
  <text x="500" y="30" text-anchor="middle" font-size="24" font-weight="bold">
    {tier_name}
  </text>
'''
    
    # Add states
    cx = 500
    for i, state in enumerate(states):
        state_class = 'decision-point' if state['type'] == 'decision' else 'work-state'
        y = 100 + (i * 100)
        
        svg += f'''
  <g transform="translate({cx}, {y})">
    <circle r="30" class="{state_class}" />
    <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" font-weight="bold">
      {state['id']}
    </text>
    <text x="0" y="50" text-anchor="middle" font-size="10">
      {state['name']}
    </text>
  </g>
'''
        
        # Add path to next state
        if i < len(states) - 1:
            svg += f'<path d="M {cx},{y + 30} L {cx},{y + 70}" class="primary-path" />\n'
    
    svg += '\n</svg>'
    
    Path(output_file).write_text(svg, encoding='utf-8')
    print(f"✓ Illustration saved: {output_file}")


# Usage:
tier_zero_states = [
    {'id': 'T0.1', 'name': 'Acceptance', 'type': 'decision'},
    {'id': 'T0.2', 'name': 'Recognition', 'type': 'work'},
    {'id': 'T0.3', 'name': 'Stabilization', 'type': 'work'},
    # ... etc
]

create_state_illustration(
    "TIER 0: Acceptance (Identity)",
    tier_zero_states,
    loops=[],  
    output_file='tier_0_simple.svg'
)
```

---

## APPROACH 3: Copy-Paste SVG Template

If you want to edit by hand, use this template:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .decision-point { fill: #8B0000; }
      .work-state { fill: #006400; }
      .primary-path { stroke: #333; stroke-width: 2; fill: none; }
      .loop-back { stroke: #cc6666; stroke-width: 2; stroke-dasharray: 5,5; fill: none; }
      text { font-family: Arial, sans-serif; }
    </style>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333" />
    </marker>
  </defs>
  
  <!-- TITLE -->
  <text x="500" y="30" text-anchor="middle" font-size="24" font-weight="bold">
    [YOUR TIER NAME AND DESCRIPTION]
  </text>
  
  <!-- STATE NODES -->
  <!-- Copy-paste this block for each state: -->
  <g transform="translate(500, [Y_POSITION])">
    <circle r="30" class="[decision-point|work-state]" />
    <text x="0" y="0" text-anchor="middle" dy="0.3em" fill="white" font-weight="bold">
      [STATE_ID]
    </text>
    <text x="0" y="50" text-anchor="middle" font-size="10">
      [STATE_NAME]
    </text>
  </g>
  
  <!-- PRIMARY PATHS -->
  <!-- Copy-paste this for each connection: -->
  <path d="M 500,[Y1] L 500,[Y2]" class="primary-path" marker-end="url(#arrow)" />
  
  <!-- LOOP BACKS (if any) -->
  <path d="M [X_FROM],[Y_FROM] Q [CTL_X],[CTL_Y] [X_TO],[Y_TO]" 
        class="loop-back" marker-end="url(#arrow)" />
  
</svg>
```

---

## ILLUSTRATION CHECKLIST FOR EACH TIER

Use this to verify your illustration is complete:

- [ ] **Title**: Clear tier name + one-sentence core principle
- [ ] **All states**: Every state in tier shown as node
- [ ] **Type encoding**: Decision points (red) vs work states (green) correct
- [ ] **Progression**: Top to bottom shows natural flow
- [ ] **Size variation**: Shows complexity increasing (optional but effective)
- [ ] **Primary paths**: Straight lines connecting consecutive states
- [ ] **Loop backs**: Curved dashed lines showing entry marker loops
- [ ] **Labels**: State IDs and names on every node
- [ ] **Legend**: Shows what colors/styles mean
- [ ] **30-second test**: Can someone unfamiliar understand the flow in 30 seconds?
- [ ] **5-minute test**: After reading state names, does it make conceptual sense?
- [ ] **Teaching integrity**: Does the visual form match the concept?

---

## BATCH GENERATION SCRIPT

Want to generate all tiers at once?

```python
#!/usr/bin/env python3
"""Generate all tier illustrations"""

from pathlib import Path
import sys

# Import all tier illustrators (when you create them)
# from generate_tier_minus1 import TierMinusOneIllustrator
# from generate_tier_0 import TierZeroIllustrator
# ... etc

TIERS = {
    'Tier -1': TierMinusOneIllustrator,
    # 'Tier 0': TierZeroIllustrator,
    # 'Tier 1': TierOneIllustrator,
    # 'Tier 2': TierTwoIllustrator,
    # 'Tier 3': TierThreeIllustrator,
}

output_dir = Path(__file__).parent / 'examples'
output_dir.mkdir(exist_ok=True)

print("Generating all tier illustrations...")
for tier_name, Illustrator in TIERS.items():
    illustrator = Illustrator()
    output_file = output_dir / f"{tier_name.lower().replace(' ', '_')}.svg"
    illustrator.save(output_file)
    print(f"  ✓ {tier_name}")

print(f"✓ All illustrations generated in {output_dir}/")
```

---

## What Each Tier Should Teach

### Tier -1: Self (Coherence)
**Visual**: Spiral/network downward with loops
**Teaching**: "Self-understanding requires moving through awareness, distinction, causality, regulation, consistency, correction, alignment, persistence, adaptability, integrity—with necessary loops back."
**Key visual element**: Two major loop-backs + full reset path

### Tier 0: Identity
**Visual**: Branching tree (choices at each point)
**Teaching**: "Identity emerges through acceptance, recognition, stabilization, definition, communication, boundary-setting, integration, expression, evolution, sovereignty—each a choice point."
**Key visual element**: Clear A/B/C branching at every state

### Tier 1: Competence
**Visual**: Ascending stairs with connection bridges
**Teaching**: "Competence builds through foundation, skill, practice, challenge, failure, learning, adaptation, mastery, teaching, legacy—each builds on prior."
**Key visual element**: Horizontal bridges showing prerequisite relationships

### Tier 2: Contribution
**Visual**: Expanding concentric circles
**Teaching**: "Contribution starts in self, extends to family, community, society, species, life, consciousness—each layer depends on all prior layers."
**Key visual element**: Overlapping circles showing "both" relationships

### Tier 3: Transcendence
**Visual**: Ascending path with illumination
**Teaching**: "Transcendence isn't escape—it's discovering meaning, purpose, connection that integrates all prior tiers."
**Key visual element**: Light/gradient showing integration of all prior work

---

## NEXT STEPS

1. **Tomorrow**: Build Tier 0 illustration (branching structure)
2. **Day 3**: Build Tier 1 illustration (prerequisite structure)
3. **Day 4**: Build Tier 2 illustration (concentric structure)
4. **Day 5**: Build Tier 3 illustration (integration structure)
5. **Day 6**: Create matrix visualization (all states at once)
6. **Day 7**: Create interactive HTML versions

Each new tier teaches you more about visual encoding. By Tier 3, you'll be able to generate illustrations instantly.

---

**Status**: [Illustration Multiplication Strategy Complete ✓]
