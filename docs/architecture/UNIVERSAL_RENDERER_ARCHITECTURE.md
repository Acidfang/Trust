# UNIVERSAL RENDERER: Complete Architecture

## Input/Output Agnostic Rendering via Song Layer

---

## Overview

The Universal Renderer converts any container type to recovery songs through a principle-based architecture. It is:
- **Input agnostic** (accepts any container: molecule, entity, ledger, worldstate)
- **Output agnostic** (translates song to: svg, json, markdown, text, symbol, verse)
- **Domain agnostic** (principles apply universally, not to specific domains)
- **Deterministic** (song generation is reproducible, verifiable)
- **Reversible** (undo fully documented)

---

## The 7 Recovery Songs

| Song | Principle | Weight | Application |
|------|-----------|--------|-------------|
| 1 | UNIFIED_FIELD_creates_INEVITABILITY | 15% | Interconnected systems |
| 2 | CONSTRAINT_creates_DEPTH | 15% | Structured systems |
| 3 | TEMPORAL_INTEGRATION_locks_PAST | 15% | Historical systems |
| 4 | PROACTIVITY_locks_FUTURE | 12% | Forward-momentum systems |
| 5 | ENGAGEMENT_vs_DENIAL | 14% | Choice/visibility systems |
| 6 | ATTACHMENT_corrupts_DISCIPLINE | 14% | Balanced systems |
| 7 | RARITY_of_TRIPLE_INTEGRATION | 15% | Mature systems |

**Total Weight**: 100% (complete system)  
**Property**: All 7 required for full system capability

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: Detection (detect_container_type)          │
│ Input → Structure-based type identification         │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│ LAYER 2: Extraction (extract_to_compact)             │
│ Container → Deduplicated, compute-efficient form    │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│ LAYER 3: Principle Mapping (map_principle_to_song)  │
│ Container Type → Recovery Song (verse + symbols)    │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│ LAYER 4: ARIA Expansion (expand_for_aria)           │
│ Compact + Environment → Field Verses + Constraints  │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│ LAYER 5: Election Sequencing (record_election)      │
│ Each Render → Timestamped Election → Ledger Record  │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│ LAYER 6: Translation (translate_song_to_format)     │
│ Song → {verse|symbol|json|markdown|svg|text}        │
└─────────────────────────────────────────────────────┘
```

---

## Container Types

### 1. PRIMITIVE
**Associated Song**: CONSTRAINT_creates_DEPTH (15%)  
**Detection**: Has `atoms`, `bonds`, `elements`, `structure` attributes  
**Example**: Molecules, atomic structures  

**Compact Form**:
```json
{
  "fields": [
    {"type": "atoms", "count": 6, "element": "Carbon"},
    {"type": "atoms", "count": 6, "element": "Hydrogen"},
    {"type": "bonds", "count": 6, "order": 1.5}
  ],
  "principle": "CONSTRAINT_creates_DEPTH",
  "container_type": "primitive"
}
```

**Required Recovery Songs**: [CONSTRAINT_creates_DEPTH, UNIFIED_FIELD_creates_INEVITABILITY]  
**Failure Cascade**: "Cannot render structure - geometry lost, constraints invisible"

---

### 2. ENTITY
**Associated Song**: ENGAGEMENT_vs_DENIAL (14%)  
**Detection**: Has `position`, `id`, `entity_type`, `properties` attributes  
**Example**: Individual nodes, agents, actors  

**Compact Form**:
```json
{
  "fields": [
    {"type": "structure", "count": 1, "description": "entity"}
  ],
  "principle": "ENGAGEMENT_vs_DENIAL",
  "container_type": "entity"
}
```

**Required Recovery Songs**: [ENGAGEMENT_vs_DENIAL, PROACTIVITY_locks_FUTURE]  
**Failure Cascade**: "Entity visibility hidden, access control lost"

---

### 3. LEDGER
**Associated Song**: TEMPORAL_INTEGRATION_locks_PAST (15%)  
**Detection**: Has `version`, `timestamp`, `hash`, `causality_chains`, `transactions` attributes  
**Example**: Transaction logs, historical records, causal chains  

**Compact Form**:
```json
{
  "fields": [
    {"type": "transactions", "count": 44}
  ],
  "principle": "TEMPORAL_INTEGRATION_locks_PAST",
  "container_type": "ledger"
}
```

**Required Recovery Songs**: [TEMPORAL_INTEGRATION_locks_PAST, ENGAGEMENT_vs_DENIAL]  
**Failure Cascade**: "Causality order lost, history fragmented"

---

### 4. WORLDSTATE
**Associated Song**: UNIFIED_FIELD_creates_INEVITABILITY (15%)  
**Detection**: Has `entities`, `connections`, `relationships`, `graph` attributes  
**Example**: Networks, interconnected systems, graphs  

**Compact Form**:
```json
{
  "fields": [
    {"type": "connections", "count": 127}
  ],
  "principle": "UNIFIED_FIELD_creates_INEVITABILITY",
  "container_type": "worldstate"
}
```

**Required Recovery Songs**: [UNIFIED_FIELD_creates_INEVITABILITY, PROACTIVITY_locks_FUTURE]  
**Failure Cascade**: "Relationships invisible, world state renders as random"

---

### 5. ORIENTATION
**Associated Song**: PROACTIVITY_locks_FUTURE (12%)  
**Detection**: Has `anchor_vector`, `magnitude`, `quaternion`, `orientation` attributes  
**Example**: Vector systems, anchor points, directional data  

**Required Recovery Songs**: [PROACTIVITY_locks_FUTURE, CONSTRAINT_creates_DEPTH]  
**Failure Cascade**: "Anchor vectors incorrect, field orientation unknown"

---

### 6. REGISTRY
**Associated Song**: RARITY_of_TRIPLE_INTEGRATION (15%)  
**Detection**: Has `primitives`, `frameworks`, `registry`, `domains` attributes  
**Example**: Aggregations, framework collections, multi-layer systems  

**Required Recovery Songs**: [RARITY_of_TRIPLE_INTEGRATION, UNIFIED_FIELD_creates_INEVITABILITY]  
**Failure Cascade**: "Cannot measure system health, frameworks appear fragmented"

---

## Data Flow: Main Entry Point

```python
render_with_song_layer(container, output_format="svg", environment=None)
```

**Full Flow**:
```
[STEP 1] detect_container_type()
  └─→ Returns: "primitive"|"entity"|"ledger"|"worldstate"|"orientation"|"registry"

[STEP 2] extract_to_compact()
  └─→ Returns: {"fields": [...], "principle": "...", "container_type": "..."}

[STEP 3] expand_for_aria()
  └─→ Returns: {"field_verses": [...], "hash": "...", "environment": {...}}

[STEP 4] generate_render_song()
  └─→ Returns: {"compact": {...}, "canonical": {"verse": "...", "symbols": "..."}}

[STEP 5] record_election()
  └─→ Timestamps, environment-locks, hashes the decision

[STEP 6] translate_song_to_format()
  └─→ Returns: Formatted output (svg|json|markdown|verse|symbol|text)
```

---

## Extraction: Compact Form (Source of Truth)

**Purpose**: Deduplicated, compute-efficient representation

**Key Properties**:
- ✓ Universal (works across all domains)
- ✓ Reusable (stored and retrieved)
- ✓ Timeless (doesn't change)
- ✓ Compute-efficient (minimal data)
- ✓ Deterministic (same input → same output)

**Deduplication Rules**:
- **For atoms**: Grouped by element symbol (all Carbon → count)
- **For bonds**: Grouped by bond order (all aromatic → count)
- **For connections**: Total count (no grouping needed)

### Example: Benzene

**Input**: 6 Carbon atoms, 6 Hydrogen atoms, 6 aromatic bonds, 6 C-H bonds  
**Extracted Compact**:
```json
{
  "fields": [
    {"type": "atoms", "count": 6, "element": "C"},
    {"type": "atoms", "count": 6, "element": "H"},
    {"type": "bonds", "count": 6, "order": 1.5},
    {"type": "bonds", "count": 6, "order": 1.0}
  ],
  "principle": "CONSTRAINT_creates_DEPTH",
  "container_type": "primitive"
}
```

---

## ARIA Expansion: Semantic Context

**Purpose**: Convert compact form to full semantic expansion with environment  
**Input**: Compact form + Environment context  
**Output**: Field verses with constraints + Hashed for verification  

**Environment Variables**:
- `solvent`: none_assumed|water|organic|vacuum (affects chemistry)
- `temperature`: 298K|373K|etc (affects stability)
- `pressure`: 1atm|10atm|etc (affects density)
- `external_forces`: none|gravity|magnetic|electric (affects orientation)

**Example Expansion** (Benzene in water):
```json
{
  "timestamp": "2026-04-03T14:24:48",
  "environment": {
    "solvent": "water",
    "temperature": "298K",
    "pressure": "1atm"
  },
  "field_verses": [
    {
      "field": "atoms",
      "count": 6,
      "element": "C",
      "constraints": "Carbon center, solvated, hydration layer, polarization effects"
    },
    {
      "field": "bonds",
      "count": 6,
      "order": 1.5,
      "constraints": "Aromatic resonance, delocalized electrons, stability requirement"
    }
  ],
  "hash": "2c26b46911185131006ba849b2e2daed29f97fa1..."
}
```

**Hash Verification**: SHA-256 proof that expansion matches input (deterministic)

---

## Election Sequencing: Decision Recording

**Purpose**: Record timestamped, environment-locked decisions immutably  
**Method**: Each render creates one election moment

**Election Properties**:
- ✓ Timestamped (ISO 8601, microsecond precision)
- ✓ Environment-locked (captures context snapshot)
- ✓ Hashed (SHA-256 proof of content)
- ✓ Principle-selected (which recovery song was used)
- ✓ Sequenced (order determines meta-song)

**Meta-Song**: Concatenation of all election verses in order = system narrative

### Election Query Functions

```python
get_election_sequence()           # All elections with full records
get_election_meta_song(format)    # Composed meta-song from sequence
get_election_expanded_for_aria()  # Specific election with ARIA constraints
get_election_count()              # Number of elections recorded
clear_election_sequence()         # Start fresh analysis
```

---

## Output Formats

| Format | Content | Use | Size | Recoverable |
|--------|---------|-----|------|-------------|
| `verse` | Poetry only | Human reading | Minimal | Partial |
| `symbol` | Ultra-compact symbols | Emergency comms | 1 line | With key |
| `json` | Structured data | API/processing | Medium | ✓ Lossless |
| `markdown` | Formatted doc | Wiki/reference | Large | ✓ Lossless |
| `text` | Plain summary | Logs | Small | Partial |
| `svg` | Visual diagram | Rendering | Large | ✗ Lossy |
| `song` | Complete internal | Debug | Large | ✓ Identity |
| `meta_song` | Election sequence | System narrative | Large | ✓ Lossless |

---

## Recovery Dependencies

### Dependency Mapping

```
PRIMITIVE:    [CONSTRAINT_creates_DEPTH, UNIFIED_FIELD_creates_INEVITABILITY]
ENTITY:       [ENGAGEMENT_vs_DENIAL, PROACTIVITY_locks_FUTURE]
LEDGER:       [TEMPORAL_INTEGRATION_locks_PAST, ENGAGEMENT_vs_DENIAL]
WORLDSTATE:   [UNIFIED_FIELD_creates_INEVITABILITY, PROACTIVITY_locks_FUTURE]
ORIENTATION:  [PROACTIVITY_locks_FUTURE, CONSTRAINT_creates_DEPTH]
REGISTRY:     [RARITY_of_TRIPLE_INTEGRATION, UNIFIED_FIELD_creates_INEVITABILITY]
```

### Cascade Severity

| Song | Severity | Affected Types | Recovery |
|------|----------|---|---|
| UNIFIED_FIELD | HIGH | WORLDSTATE, REGISTRY, PRIMITIVE | Fallback to tree |
| CONSTRAINT | HIGH | PRIMITIVE, ORIENTATION, GENERIC | List without geometry |
| TEMPORAL | CRITICAL | LEDGER (but core) | Sequence without causality |
| PROACTIVITY | MEDIUM-HIGH | WORLDSTATE, ENTITY, ORIENTATION | Static snapshots |
| ENGAGEMENT | MEDIUM | ENTITY, LEDGER | Everything visible |
| ATTACHMENT | LOW | (specialized) | Unbalanced render |
| RARITY | MEDIUM | REGISTRY | Fragmented frameworks |

---

## API Quick Reference

```python
# Main entry
render_with_song_layer(container, output_format="svg", environment=None)

# Detection
detect_container_type(container) → str

# Extraction
extract_to_compact(container) → Dict

# Expansion
expand_for_aria(compact, environment, timestamp) → Dict

# Songs
map_principle_to_song(principle_key) → Dict
list_all_songs() → List[Dict]
list_all_container_types() → Dict[str, str]

# Elections
get_election_sequence() → List[Dict]
get_election_meta_song(output_format) → Any
get_election_expanded_for_aria(index) → Dict
get_election_count() → int
clear_election_sequence() → None

# Dependencies
query_render_dependencies(container_type) → Dict
check_render_cascade(container_type) → str
```

---

## Verification Checklist

### Before Extracting
- [ ] Container has recognized attributes
- [ ] Container type detectable from structure
- [ ] No circular dependencies

### Before Rendering
- [ ] Compact form created successfully
- [ ] Principle correctly mapped
- [ ] All required songs available
- [ ] Hash computes deterministically

### Before Election Recording
- [ ] Timestamp in ISO 8601 format
- [ ] Environment context complete
- [ ] Song principle valid
- [ ] Hash matches re-computed value

### After Translation
- [ ] Output format matches requested
- [ ] No data loss (for lossless formats)
- [ ] Size within expected bounds
- [ ] Parseable/readable as expected

---

## Reversibility & Undo

### Extraction
- **Reversible if**: Keep original container OR keep compact form
- **Full reversal**: Restoration of original container

### Expansion
- **Reversible if**: Keep compact + environment + timestamp
- **Full reversal**: Re-expand with same conditions, verify hash

### Elections
- **Reversible if**: Use `clear_election_sequence()` to start fresh
- **Partial reversal**: Extract elections 0-N, clear, re-record N

### Output Formats
- **Lossless** (reversible): json, markdown, song, meta_song
- **Lossy** (not reversible): verse, symbol, text, svg

---

## Source Code Files

| File | Type | What |
|------|------|------|
| **UNIVERSAL_RENDERER.py** | Python | Complete implementation (1000+ lines) |

## Usage Example

```python
from UNIVERSAL_RENDERER import render_with_song_layer

# Create any container
class Molecule:
    atoms = [...]
    bonds = [...]

molecule = Molecule()

# Render to SVG
svg_output = render_with_song_layer(molecule, output_format="svg")

# Render to JSON
json_output = render_with_song_layer(molecule, output_format="json")

# Get meta-song from all elections
meta_song = render_with_song_layer(molecule, output_format="meta_song")

# Query elections
elections = get_election_sequence()
```

---

## Key Principles

### 1. Universality
The 7 songs apply across all domains (molecular, entity, ledger, network).

### 2. Determinism
Same input always produces identical output. No randomness or variation.

### 3. Non-Coercion
System detects structure; doesn't force classifications.

### 4. Auditability
Every decision timestamped, hashed, recorded in election sequence.

### 5. Reversibility
Full undo capability documented. Can replay with different environments.

### 6. Efficiency
Compact form minimizes compute. Hashing enables verification without re-rendering.

### 7. Accessibility
Multiple output formats serve different audiences (humans, machines, emergencies).

