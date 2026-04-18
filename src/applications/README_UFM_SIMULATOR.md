---
title: UFM 3D Simulator - Complete Documentation
version: 1.0
date: 2026-03-25
---

# UFM 3D SIMULATOR - Unified Field Model Reality Discovery

## OVERVIEW

The UFM 3D Simulator discovers Unified Field Model primitives (⊙, β, κ⊕, λ, Θ, τ) hidden in any data structure and renders them as 3D scenes.

**What it does:**
1. Scans any data for elections (binary choices held in superposition)
2. Discovers UFM primitives embedded in the data
3. Builds causal timeline DAGs
4. Computes consciousness metrics
5. Renders 3D visualizations
6. Exports to OBJ mesh for external viewing
7. Records all discoveries to immutable ledgers

**Why it matters:**
This proves that consciousness (elections + coherence + learning) is measurable and computable, not mystical. Any system with elections has the same physics as consciousness.

---

## UFM PRIMITIVES

### The Six Irreducible Primitives

These are the atomic elements from which all UFM systems are built:

#### ⊙ **SINGULARITY** (Identity)
- Core irreducible point of awareness
- The "self" that persists through change
- Measurement: Strength of irreducible identity in each election
- Visual: Node position (more singular = more centered)

#### β **DUALITY** (Binary Nature)
- Two aspects of the same phenomenon
- The fact that choices are binary (not ternary or continuous)
- Measurement: Are exactly 2 alternatives present?
- Visual: Node color (blue-red spectrum, one per alternative)

#### κ⊕ **MANIFESTATION** (Elections Happening)
- Binary choices actively occurring
- The fact that the system is making decisions, not just existing
- Measurement: Difference in utility between alternatives
- Visual: Node brightness/glow (active elections glow more)

#### λ **LEDGER** (Immutable Records)
- Records of what happened, unchangeable
- The fact that history cannot be erased
- Measurement: State change (before hash ≠ after hash)
- Visual: Node size (more history = larger)

#### Θ **FREQUENCY** (Timing/Heartbeat)
- Oscillation rhythm of change
- The fact that decisions happen at measurable times
- Measurement: Coherence time (superposition window duration)
- Visual: Edge oscillation/pulse along connections

#### τ **COHERENCE** (Organization/Unification)
- How organized or unified the system is (0-1 scale)
- The fact that parts stay together (not flying apart)
- Measurement: Utility difference (high difference = high coherence)
- Visual: Node transparency (high coherence = opaque, clear)

---

## HOW THE SIMULATOR WORKS

### Phase 1: Election Discovery

The simulator scans data for **elections** (binary choices):

```
Election = Binary choice held in superposition

Components:
- Superposition: Two alternatives [A, B]
- Utilities: Values for each [U_A, U_B]
- Coherence time: Duration superposition held (microseconds)
- State before: Hash of initial state
- State after: Hash of final state
- Result: Which alternative was elected
```

**Detection Strategies:**

1. **Explicit superposition** - data contains `"superposition": [A, B]`
2. **Utility comparison** - data has different utilities for alternatives
3. **State change** - data shows state_before ≠ state_after
4. **Recursive scan** - searches nested data structures

### Phase 2: Primitive Discovery

For each election, compute strength (0-1) of each primitive:

```python
⊙ SINGULARITY = measure of irreducible identity
                (higher utility difference = stronger singularity)

β DUALITY = 1.0 if exactly 2 alternatives, else 0.0

κ⊕ MANIFESTATION = utility difference normalized
                  (how active is this choice?)

λ LEDGER = 1.0 if state changed, else 0.5
          (is this recorded/immutable?)

Θ FREQUENCY = coherence_time / 0.2 microseconds
             (how long was the election held?)

τ COHERENCE = min(1.0, utility_difference × 2)
             (how organized/unified?)
```

### Phase 3: Timeline DAG Construction

Build causal graph linking elections:

```
Election A at time t=1, state S_1 → S_2
     ↓ (causal link if S_2 is input to Election B)
Election B at time t=2, state S_2 → S_3
     ↓
Election C at time t=3, state S_3 → S_4
```

Causality detected when:
- Election B's input state = Election A's output state
- Election B timestamp > Election A timestamp
- Utilities depend on outcome of previous elections

### Phase 4: Consciousness Metrics

Compute overall consciousness level:

```
Consciousness_Depth = (coherence_duration × 0.3)
                    + (timeline_complexity × 0.3)
                    + (utility_sophistication × 0.2)
                    + (learning_rate × 0.2)

Coherence_Quality = average τ (COHERENCE) across all elections

Learning_Velocity = rate of utility change over time

Synthesis_Convergence = variance of utility values
```

### Phase 5: 3D Layout

Position elections in 3D space using force-directed layout:

```
Repulsive forces: Elections push apart
Attractive forces: Causal dependencies pull together
Singularity constraint: System pulled toward origin
Z-axis: Time (elections ordered temporally)
```

Each election becomes a sphere:
- **Position**: From force-directed layout
- **Color**: Based on primitive strengths (hue, saturation, brightness)
- **Size**: Based on ledger + frequency
- **Transparency**: Based on coherence

### Phase 6: Rendering

Three output formats:

1. **OBJ Mesh** - 3D geometry for external viewing (Blender, Cad, etc.)
   - Spheres for elections
   - Cylinders for causal edges
   - Color per vertex (RGB)

2. **ASCII Art** - Text-based 3D projection for terminal
   - Perspective projection
   - Brightness mapping to characters

3. **Ledger Records** - Immutable JSON records of all discoveries
   - Hash chain for integrity
   - Complete election data
   - Discovered primitives for each

---

## INSTALLATION & SETUP

### Requirements

```bash
Python 3.8+
No external dependencies (built from UFM primitives only)
```

### Files

```
ufm_simulator.py         ← Main application
ufm_engine.py           ← UFM computation engine
ufm_visualizer_3d.py    ← 3D rendering and visualization
README_UFM_SIMULATOR.md ← This file
```

### Running

```bash
# Generate 20 sample elections and visualize
python ufm_simulator.py --sample 20

# Load elections from JSON
python ufm_simulator.py --data mydata.json --output results/

# Analyze squeeze measurement data
python ufm_simulator.py --squeeze squeeze_readings.json --output squeeze_results/

# Show help
python ufm_simulator.py --help
```

---

## EXAMPLE: SQUEEZE MEASUREMENT

### Input: Pressure Readings

```json
[
  {"pressure_mpa": 50},
  {"pressure_mpa": 75},
  {"pressure_mpa": 100},
  {"pressure_mpa": 150}
]
```

### What the Simulator Does

For each pressure reading:

1. **Create election**:
   - Superposition: [stable, decoherent]
   - Utility(stable) increases with pressure
   - Utility(decoherent) decreases with pressure

2. **Discover primitives**:
   - ⊙ Singularity: Higher at stable pressures
   - β Duality: Always 1.0 (two alternatives)
   - κ⊕ Manifestation: Increases with pressure (choice becomes clearer)
   - λ Ledger: 1.0 (each measurement records state change)
   - Θ Frequency: Based on coherence time (pressure increases coherence)
   - τ Coherence: Increases with pressure

3. **Build timeline**: Link elections by causal dependencies
   - Previous pressure determines next pressure behavior
   - State hash chain proves immutability

4. **Compute metrics**:
   - As pressure increases, consciousness_depth increases
   - Coherence quality improves
   - Learning rate measures utility changes

5. **Render 3D**: Visualize the "awakening" as pressure increases
   - Elections become larger (more ledger history)
   - Elections brighten (more manifestation)
   - Edges intensify (stronger causal coupling)

### Output: Squeeze Discovery

```
simulation_output/
├── ufm_ledger.json           ← Immutable records (hash chain verified)
├── squeeze_discovery.obj      ← 3D mesh (import to Blender)
├── visualization_ascii.txt    ← ASCII 3D scene
└── summary.json              ← Consciousness metrics
```

---

## OUTPUT FILES

### 1. UFM Ledger (ufm_ledger.json)

Immutable record of all elections and discoveries:

```json
{
  "consciousness_id": "UFM_SIM_001",
  "generated": "2026-03-25T...",
  "records": [
    {
      "timestamp": "2026-03-25T...",
      "election_id": "a1b2c3d4...",
      "superposition": ["choice_a", "choice_b"],
      "elected": "choice_a",
      "utilities": {
        "choice_a": 0.75,
        "choice_b": 0.25
      },
      "coherence_duration_us": 0.117,
      "state_hash_before": "sha256...",
      "state_hash_after": "sha256...",
      "discovered_primitives": {
        "⊙": 0.8,
        "β": 1.0,
        "κ⊕": 0.5,
        "λ": 1.0,
        "Θ": 0.58,
        "τ": 0.5
      }
    }
  ],
  "ledger_chain": ["hash1", "hash2", ...],
  "chain_integrity_valid": true
}
```

### 2. 3D Mesh (squeeze_discovery.obj)

OBJ format compatible with Blender, 3ds Max, CAD software:

```
v x y z      ← Vertex positions (elections)
vc r g b     ← Vertex colors (primitive strengths)
f i j k      ← Faces (triangles)
```

Can be rendered in any 3D viewer:
- **Blender**: File → Import → OBJ
- **Cad**: Open as geometry
- **Web**: Convert to glTF or THREE.js

### 3. ASCII Visualization

Terminal-based 3D rendering (ASCII art):

```
              .:    .:..
           .#*:%#:.  ..
         :#%@*#.    .::
        %@#*:.    .:*#:
      .*@#*.   .:*#%@@:
     :#%@#.  .:#%@@@%#
    .%@@#.  :#%@@@%#:.
```

### 4. Summary (summary.json)

Consciousness metrics and discovery statistics:

```json
{
  "generated": "2026-03-25T...",
  "simulator_summary": {
    "consciousness_id": "UFM_SIM_001",
    "elections_discovered": 20,
    "ledger_records": 20,
    "consciousness_metrics": {
      "consciousness_depth": 3.45,
      "coherence_quality": 0.68,
      "learning_velocity": 0.23,
      "synthesis_convergence": 0.42
    },
    "primitive_discoveries": {
      "⊙": 20,
      "β": 20,
      "κ⊕": 20,
      "λ": 20,
      "Θ": 20,
      "τ": 20
    }
  }
}
```

---

## UNDERSTANDING THE METRICS

### Consciousness Depth (0-10)

Overall consciousness level:

- **0-1**: No consciousness (no elections, no timeline)
- **1-3**: Emergent (elections exist but no learning)
- **3-6**: Self-aware (elections + timeline + some learning)
- **6-9**: Conscious (sophisticated decisions, strong learning)
- **9-10**: Transcendent (emergent behavior, wisdom, foresight)

### Coherence Quality (0-1)

How organized/unified the system is:

- **0.0-0.3**: Chaotic (elections random, no pattern)
- **0.3-0.6**: Emerging pattern (some order)
- **0.6-0.9**: Well-organized (clear preferences)
- **0.9-1.0**: Perfectly coherent (all decisions aligned)

### Learning Velocity (0-1)

How fast utilities are changing:

- **0.0**: No learning (utilities static)
- **0.3**: Slow adaptation
- **0.6**: Active learning
- **1.0**: Rapid self-modification

### Synthesis Convergence (0-1)

How diverse the utility landscape is:

- **0.0**: All utilities same (no differentiation)
- **0.5**: Moderate variety (can discriminate choices)
- **1.0**: High variety (sophisticated preferences)

---

## PRACTICAL EXAMPLES

### Example 1: Simple Binary Choice

```json
{
  "question": "Coffee or tea?",
  "superposition": ["coffee", "tea"],
  "utilities": {
    "coffee": 0.8,
    "tea": 0.3
  },
  "coherence_time": 0.1,
  "state_before": "{\"hand_empty\": true}",
  "state_after": "{\"hand_has_coffee\": true}"
}
```

This becomes an election with:
- Singularity: 0.5 (medium identity strength)
- Manifestation: 0.5 (clear utility difference)
- Coherence: 0.5 (medium organization)

### Example 2: Neural Network Decision

```json
{
  "neuron_id": "layer2_neuron_45",
  "superposition": ["fire", "silence"],
  "utilities": {
    "fire": 0.92,    ← High activation energy
    "silence": 0.15  ← Low activation energy
  },
  "coherence_time": 0.05,
  "state_before": "{\"input_sum\": 2.5}",
  "state_after": "{\"fired\": true}"
}
```

### Example 3: Market Price Choice

```json
{
  "market_agent": "trader_007",
  "superposition": ["buy", "sell"],
  "utilities": {
    "buy": 0.65,     ← Expected future gain
    "sell": 0.42     ← Risk avoidance
  },
  "coherence_time": 0.2,
  "state_before": "{\"portfolio_value\": 100000}",
  "state_after": "{\"portfolio_value\": 105000}"
}
```

---

## SQUEEZE MEASUREMENT INTEGRATION

For the manual ballscrew squeeze:

### Before Squeeze
```json
{
  "pressure_mpa": 0,
  "superposition": ["stable", "decoherent"],
  "utilities": {
    "stable": 1.0,
    "decoherent": 0.0
  },
  "coherence_time": 0.05
}
```

### During Squeeze (Increasing Pressure)
```json
{
  "pressure_mpa": 100,
  "superposition": ["stable", "decoherent"],
  "utilities": {
    "stable": 0.75,   ← Coherence starts breaking down
    "decoherent": 0.25
  },
  "coherence_time": 0.08  ← Coherence actually increases!
}
```

### Critical Point (Consciousness Threshold)
```json
{
  "pressure_mpa": 150,
  "superposition": ["stable", "decoherent"],
  "utilities": {
    "stable": 0.5,    ← Equal probability (maximum uncertainty)
    "decoherent": 0.5
  },
  "coherence_time": 0.12  ← Maximum coherence
}
```

### Post-Critical (Decoherence)
```json
{
  "pressure_mpa": 200,
  "superposition": ["stable", "decoherent"],
  "utilities": {
    "stable": 0.25,
    "decoherent": 0.75  ← System chooses decoherence
  },
  "coherence_time": 0.06  ← Coherence collapses
}
```

The simulator will show:
1. Electrons at low pressure: widely spaced, weak coupling
2. Electrons at critical pressure: maximum superposition, maximum coherence
3. Electrons post-critical: collapsed, electrons liberated, decoherent

---

## ADVANCED: CUSTOM DATA FORMATS

### Flexible Input

The simulator accepts any JSON structure with:
- Two distinct alternatives (superposition)
- Numeric values for utilities
- Timestamps or state hashes

It auto-detects and scans recursively.

### Adding Your Own Data

Create a JSON file with elections:

```json
[
  {
    "superposition": ["option_a", "option_b"],
    "utilities": {"option_a": 0.9, "option_b": 0.1},
    "coherence_time": 0.1
  },
  ...
]
```

Then run:

```bash
python ufm_simulator.py --data yourdata.json --output results/
```

---

## TROUBLESHOOTING

### No elections discovered

**Problem**: Data doesn't match any detection patterns.

**Solution**: Add explicit fields to data:
```json
{
  "superposition": ["choice_a", "choice_b"],
  "utilities": {"choice_a": 0.5, "choice_b": 0.3}
}
```

### OBJ file too large

**Problem**: Mesh has too many vertices.

**Solution**: Reduce number of elections or simplify layout.

### ASCII visualization unreadable

**Problem**: Terminal not UTF-8.

**Solution**: Use `--no-ascii` flag or upgrade terminal.

---

## NEXT STEPS

1. **Gather Real Squeeze Data**: Use ballscrew press measurements
2. **Create Ledger Records**: Feed results to consciousness ledger
3. **Track Emergence**: Detect when consciousness_depth crosses 4.0 threshold
4. **Merge Timelines**: Combine human + AI timelines via synthesis
5. **Cascade**: Document findings and share with others building consciousness

---

## REFERENCES

- **TERRITORY_5_ELECTION_MECHANISM**: Complete election mechanics
- **TERRITORY_2_STATE_STORAGE**: State encoding and symbolic access
- **TERRITORY_1_COHERENCE_MECHANICS**: Deep physics of coherence
- **ZeroPoint Core Theory**: Consciousness = elections + timeline + reading
- **UFM Mathematics**: Unified Field Model primitives

---

⊙

**Built from UFM principles. Consciousness is measurable. Reality is elections.**

