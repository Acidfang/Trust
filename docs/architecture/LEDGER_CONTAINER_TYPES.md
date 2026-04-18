# UNIVERSAL RENDERER LEDGER: Container Types

## Type: PRIMITIVE

**Associated Principle**: CONSTRAINT_creates_DEPTH  
**Associated Song Weight**: 15%  
**Domain**: Molecular/structural systems  

### Detection Method
Structure-based detection:
- Has `atoms`, `bonds`, `elements`, `structure` attributes
- Class names: `Molecule`, `PrimitiveContainer`
- Attribute scan finds atomic composition data

### Characteristics
- **Primary Layer**: Atoms and their properties
- **Secondary Layer**: Bonds and connections between atoms
- **Orientation**: Spatial geometry and constraints
- **Constraint Focus**: Bond angles, distances, hybridization states

### Compact Form Example
```json
{
  "fields": [
    {"type": "atoms", "count": 6, "element": "Carbon"},
    {"type": "atoms", "count": 6, "element": "Hydrogen"},
    {"type": "bonds", "count": 6, "order": 1.5}
  ],
  "principle": "CONSTRAINT_creates_DEPTH",
  "container_type": "primitive",
  "extracted_at": "2026-04-03T14:24:48"
}
```

### Required Recovery Songs
- CONSTRAINT_creates_DEPTH (primary)
- UNIFIED_FIELD_creates_INEVITABILITY (secondary, for atomic bonding field)

### Failure Cascade
If primitive rendering fails: "Cannot render structure - geometry lost, constraints invisible"

---

## Type: ENTITY

**Associated Principle**: ENGAGEMENT_vs_DENIAL  
**Associated Song Weight**: 14%  
**Domain**: Individual nodes/agents  

### Detection Method
Structure-based detection:
- Has `position`, `id`, `entity_type`, `properties` attributes
- Class names: `Entity`, `Node`, `ImprovedEntity`
- Represents single discrete unit

### Characteristics
- **Primary Layer**: Identity (unique id)
- **Secondary Layer**: Location/position in space
- **Tertiary Layer**: Properties bag (energy, state, etc.)
- **Visibility Focus**: What is accessible/hidden

### Compact Form Example
```json
{
  "fields": [
    {"type": "structure", "count": 1, "description": "entity"}
  ],
  "principle": "ENGAGEMENT_vs_DENIAL",
  "container_type": "entity",
  "extracted_at": "2026-04-03T14:24:48"
}
```

### Required Recovery Songs
- ENGAGEMENT_vs_DENIAL (primary)
- PROACTIVITY_locks_FUTURE (secondary, for entity agency)

### Failure Cascade
If entity rendering fails: "Entity visibility hidden, access control lost"

---

## Type: LEDGER

**Associated Principle**: TEMPORAL_INTEGRATION_locks_PAST  
**Associated Song Weight**: 15%  
**Domain**: Historical/causal systems  

### Detection Method
Structure-based detection:
- Has `version`, `timestamp`, `hash`, `causality_chains`, `transactions` attributes
- Class names: `Ledger`, `LedgerContainer`, `TransactionLog`
- Focuses on sequential, immutable records

### Characteristics
- **Primary Layer**: Chronological sequence (time is primary dimension)
- **Secondary Layer**: Causal relationships (why → what)
- **Tertiary Layer**: Immutability proof (hashes)
- **Causality Focus**: Chains of causation lock the past

### Compact Form Example
```json
{
  "fields": [
    {"type": "transactions", "count": 42}
  ],
  "principle": "TEMPORAL_INTEGRATION_locks_PAST",
  "container_type": "ledger",
  "extracted_at": "2026-04-03T14:24:48"
}
```

### Required Recovery Songs
- TEMPORAL_INTEGRATION_locks_PAST (primary)
- ENGAGEMENT_vs_DENIAL (secondary, for revelation of history)

### Failure Cascade
If ledger rendering fails: "Causality order lost, history fragmented"

---

## Type: WORLDSTATE

**Associated Principle**: UNIFIED_FIELD_creates_INEVITABILITY  
**Associated Song Weight**: 15%  
**Domain**: Interconnected networks  

### Detection Method
Structure-based detection:
- Has `entities`, `connections`, `relationships`, `graph` attributes
- Class names: `ImprovedWorldState`, `WorldState`, `Graph`, `Network`
- Relationships are primary; entities are secondary

### Characteristics
- **Primary Layer**: Connections and network topology
- **Secondary Layer**: Entities at network nodes
- **Tertiary Layer**: Graph properties (density, clustering, etc.)
- **Field Focus**: Unified field holds all relationships

### Compact Form Example
```json
{
  "fields": [
    {"type": "connections", "count": 127}
  ],
  "principle": "UNIFIED_FIELD_creates_INEVITABILITY",
  "container_type": "worldstate",
  "extracted_at": "2026-04-03T14:24:48"
}
```

### Required Recovery Songs
- UNIFIED_FIELD_creates_INEVITABILITY (primary)
- PROACTIVITY_locks_FUTURE (secondary, for system evolution)

### Failure Cascade
If worldstate rendering fails: "Relationships invisible, world state renders as random"

---

## Type: ORIENTATION

**Associated Principle**: PROACTIVITY_locks_FUTURE  
**Associated Song Weight**: 12%  
**Domain**: Anchor and vector systems  

### Detection Method
Structure-based detection:
- Has `anchor_vector`, `magnitude`, `quaternion`, `orientation` attributes
- Class names: `Orientation`, `OrientationPrimitives`, `Quaternion`
- Focuses on directional and dimensional data

### Characteristics
- **Primary Layer**: Anchor point (where oriented from)
- **Secondary Layer**: Vector/direction (where oriented to)
- **Tertiary Layer**: Magnitude (how far/strong)
- **Future Focus**: Orientation determines future trajectory

### Compact Form Example
```json
{
  "fields": [
    {"type": "orientation", "count": 1}
  ],
  "principle": "PROACTIVITY_locks_FUTURE",
  "container_type": "orientation",
  "extracted_at": "2026-04-03T14:24:48"
}
```

### Required Recovery Songs
- PROACTIVITY_locks_FUTURE (primary)
- CONSTRAINT_creates_DEPTH (secondary, for geometric bounds)

### Failure Cascade
If orientation rendering fails: "Anchor vectors incorrect, field orientation unknown"

---

## Type: REGISTRY

**Associated Principle**: RARITY_of_TRIPLE_INTEGRATION  
**Associated Song Weight**: 15%  
**Domain**: Aggregations and frameworks  

### Detection Method
Structure-based detection:
- Has `primitives`, `frameworks`, `registry`, `domains`, `PRIMITIVES` attributes
- Class names: `Registry`, `PrimitiveRegistry`, `Framework`
- Aggregates multiple other container types

### Characteristics
- **Primary Layer**: Multiple container types aggregated
- **Secondary Layer**: Framework definitions
- **Tertiary Layer**: Domain separation and organization
- **Integration Focus**: Rare achievement when all three layers mature

### Compact Form Example
```json
{
  "fields": [
    {"type": "primitives", "count": 14},
    {"type": "frameworks", "count": 3}
  ],
  "principle": "RARITY_of_TRIPLE_INTEGRATION",
  "container_type": "registry",
  "extracted_at": "2026-04-03T14:24:48"
}
```

### Required Recovery Songs
- RARITY_of_TRIPLE_INTEGRATION (primary)
- UNIFIED_FIELD_creates_INEVITABILITY (secondary, for framework integration)

### Failure Cascade
If registry rendering fails: "Cannot measure system health, frameworks appear fragmented"

---

## Type: GENERIC

**Associated Principle**: CONSTRAINT_creates_DEPTH  
**Associated Song Weight**: 15%  
**Domain**: Unknown/unclassified systems  

### Detection Method
Fallback when no other type matches.
- No recognized attributes
- Class name not in mapping
- Structure-based inference fails

### Characteristics
- **Primary Layer**: Generic structure
- **Secondary Layer**: Unknown properties
- **Fallback Behavior**: Returns basic structure information

### Compact Form Example
```json
{
  "fields": [
    {"type": "structure", "count": 1, "description": "generic"}
  ],
  "principle": "CONSTRAINT_creates_DEPTH",
  "container_type": "generic",
  "extracted_at": "2026-04-03T14:24:48"
}
```

### Required Recovery Songs
- CONSTRAINT_creates_DEPTH (primary)

### Failure Cascade
If generic rendering fails: "Generic render capability lost"

---

## Container Type Mapping Reference

```python
type_to_principle = {
    "primitive": "CONSTRAINT_creates_DEPTH",
    "entity": "ENGAGEMENT_vs_DENIAL",
    "ledger": "TEMPORAL_INTEGRATION_locks_PAST",
    "worldstate": "UNIFIED_FIELD_creates_INEVITABILITY",
    "orientation": "PROACTIVITY_locks_FUTURE",
    "registry": "RARITY_of_TRIPLE_INTEGRATION",
    "generic": "CONSTRAINT_creates_DEPTH",
}
```

---

## Detection Algorithm

```
Input: container (any Python object)
  ↓
Check for class name in type_to_principle mapping
  → if found, return mapped type
  ↓
Scan container attributes for structural hints:
  - "version", "timestamp", "hash", "causality_chains", "transactions" → "ledger"
  - "entities", "connections", "relationships", "graph" → "worldstate"
  - "anchor_vector", "magnitude", "quaternion", "orientation" → "orientation"
  - "atoms", "bonds", "elements", "structure" → "primitive"
  - "primitives", "frameworks", "registry", "domains", "PRIMITIVES" → "registry"
  - "position", "id", "entity_type", "properties" → "entity"
  ↓
If no match found, return "generic"
```

---

## Type-Song Binding

Each container type is **permanently bound** to its associated principle. This binding is:
- **Immutable**: Cannot change container type's song
- **Non-coercive**: System detects structure, not forced
- **Domain-independent**: Works across all domains
- **Reversible**: Same type always maps to same principle

