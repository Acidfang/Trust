# UNIVERSAL RENDERER LEDGER: Data Extraction & Compact Form

## Extraction Phase (Step 2)

**Purpose**: Convert any container to deduplicated, compute-efficient compact form  
**Function**: `extract_to_compact(container: Any) → Dict[str, Any]`  
**Output Format**: Compact form (source of truth for all rendering)

---

## Compact Form Structure

```json
{
  "fields": [
    {
      "type": "atoms|bonds|connections|structure",
      "count": <integer>,
      "element": "<optional: element name>",
      "order": "<optional: bond order>"
    }
  ],
  "principle": "PRINCIPLE_NAME",
  "container_type": "primitive|entity|ledger|worldstate|orientation|registry|generic",
  "extracted_at": "2026-04-03T14:24:48.123456"
}
```

### Field Types

#### atoms
```json
{"type": "atoms", "count": 6, "element": "Carbon"}
```
- Used for: Molecular/primitive containers
- Deduplication: Grouped by element symbol
- Example: 6 Carbon atoms + 6 Hydrogen atoms = 2 deduplicated entries

#### bonds
```json
{"type": "bonds", "count": 6, "order": 1.5}
```
- Used for: Molecular/primitive containers
- Deduplication: Grouped by bond order (1.0, 1.5, 2.0, 3.0, etc.)
- Example: 6 aromatic bonds (order 1.5) = 1 deduplicated entry

#### connections
```json
{"type": "connections", "count": 127}
```
- Used for: Worldstate/network containers
- Aggregates all edges in the graph
- Count = total number of relationships

#### structure
```json
{"type": "structure", "count": 1, "description": "entity|ledger|generic"}
```
- Used for: Fallback when no specific fields detected
- Carries container type information

---

## Extraction Algorithm

```python
extract_to_compact(container):
  
  [STEP 1] Detect container type
    └─→ detect_container_type(container) → "primitive|entity|ledger|..."
  
  [STEP 2] Scan container attributes
    
    IF has 'atoms':
      For each atom in atoms_list:
        element = atom.element
        element_counts[element] += 1
      FOR each deduplicated element:
        fields.append({
          "type": "atoms",
          "count": count,
          "element": element
        })
    
    IF has 'bonds':
      For each bond in bonds_list:
        order = bond.order
        bond_counts[order] += 1
      FOR each deduplicated order:
        fields.append({
          "type": "bonds",
          "count": count,
          "order": order
        })
    
    IF has 'connections':
      fields.append({
        "type": "connections",
        "count": len(connections_list)
      })
  
  [STEP 3] Map container type to principle
    principle_categories = {
      "primitive": "constraint",
      "entity": "engagement",
      "ledger": "temporal",
      "worldstate": "unified_field",
      "orientation": "proactive",
      "registry": "rarity",
      "generic": "constraint"
    }
    principle_key = principle_categories[container_type]
  
  [STEP 4] Look up song for principle
    song_data = map_principle_to_song(principle_key)
  
  [STEP 5] Return compact form
    return {
      "fields": fields,
      "principle": song_data["principle"],
      "container_type": container_type,
      "extracted_at": now()
    }
```

---

## Deduplication Rules

### For Atoms
**Deduplication Key**: Element symbol  
**Grouping**: All atoms with element="C" → count  
**Example**:
```
Input atoms: [C, H, C, H, C, H, C, H, C, H, C, H]
Output fields: [
  {"type": "atoms", "count": 6, "element": "C"},
  {"type": "atoms", "count": 6, "element": "H"}
]
```

### For Bonds
**Deduplication Key**: Bond order (1.0, 1.5, 2.0, 3.0, etc.)  
**Grouping**: All bonds with order=1.5 → count  
**Example**:
```
Input bonds: [order=1.5, order=1.5, order=1.5, order=1.5, order=1.5, order=1.5]
Output fields: [
  {"type": "bonds", "count": 6, "order": 1.5}
]
```

### For Connections
**No deduplication**: Total count of all edges  
**Example**:
```
Input connections: [127 distinct edges]
Output fields: [
  {"type": "connections", "count": 127}
]
```

---

## Compact Form Properties

### 1. **Universal**
- Same extraction works across all domains
- Structure matters, not semantics

### 2. **Reusable**
- Can be stored and retrieved
- Input to ARIA expansion
- Basis for election recording

### 3. **Timeless**
- Does not change (source of truth)
- Created once at extraction time
- Referenced by all downstream operations

### 4. **Compute-Efficient**
- Minimal fields (type, count, metadata)
- Deduplicated (no redundant entries)
- Serializable to JSON/binary

### 5. **Deterministic**
- Same container → same compact form
- No randomness or variation
- Reproducible across sessions

---

## Extraction Examples

### Example 1: Benzene Molecule (Primitive)

**Input Container**:
```python
class Molecule:
  atoms = [
    Atom("C", 0, 0, 0),
    Atom("C", 1, 0, 0),
    Atom("C", 1.5, 0.9, 0),
    Atom("C", 1, 1.8, 0),
    Atom("C", 0, 1.8, 0),
    Atom("C", -0.5, 0.9, 0),
    Atom("H", -0.5, -0.9, 0),
    Atom("H", 1.5, -0.9, 0),
    Atom("H", 2.5, 1.8, 0),
    Atom("H", 1.5, 2.7, 0),
    Atom("H", -0.5, 2.7, 0),
    Atom("H", -1.5, 1.8, 0),
  ]
  bonds = [
    Bond(0, 1, order=1.5),
    Bond(1, 2, order=1.5),
    Bond(2, 3, order=1.5),
    Bond(3, 4, order=1.5),
    Bond(4, 5, order=1.5),
    Bond(5, 0, order=1.5),
    Bond(0, 6, order=1.0),    # C-H bonds
    Bond(1, 7, order=1.0),
    Bond(2, 8, order=1.0),
    Bond(3, 9, order=1.0),
    Bond(4, 10, order=1.0),
    Bond(5, 11, order=1.0),
  ]
```

**Extracted Compact Form**:
```json
{
  "fields": [
    {"type": "atoms", "count": 6, "element": "C"},
    {"type": "atoms", "count": 6, "element": "H"},
    {"type": "bonds", "count": 6, "order": 1.5},
    {"type": "bonds", "count": 6, "order": 1.0}
  ],
  "principle": "CONSTRAINT_creates_DEPTH",
  "container_type": "primitive",
  "extracted_at": "2026-04-03T14:24:48"
}
```

---

### Example 2: Simple Entity

**Input Container**:
```python
class Entity:
  position = [5, 5, 5]
  id = "entity_001"
  properties = {"energy": 100, "type": "agent"}
```

**Extracted Compact Form**:
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

---

### Example 3: Ledger with Transactions

**Input Container**:
```python
class Ledger:
  version = 5
  timestamp = "2026-04-03T14:24:00"
  transactions = [
    {"time": "...", "action": "CREATE", "hash": "abc..."},
    {"time": "...", "action": "UPDATE", "hash": "def..."},
    # ... 42 more transactions
  ]
  hash = "master_hash_123"
```

**Extracted Compact Form**:
```json
{
  "fields": [
    {"type": "transactions", "count": 44}
  ],
  "principle": "TEMPORAL_INTEGRATION_locks_PAST",
  "container_type": "ledger",
  "extracted_at": "2026-04-03T14:24:48"
}
```

---

## Verification Checklist

Before calling a compact form valid:

- [ ] Matches container structure (atoms match atom objects, etc.)
- [ ] Deduplication applied (no redundant fields)
- [ ] Principle correctly mapped to container type
- [ ] Container type detected accurately
- [ ] Timestamp present (extraction time recorded)
- [ ] All required fields present (fields, principle, container_type, extracted_at)
- [ ] No excess data (only what's necessary for deterministic rendering)

---

## Undo/Reversibility

**Extraction is reversible** if you keep:
- Original container object (can re-extract)
- Compact form + metadata (can reconstruct approximate source)

**Full reversal requires**: Original container + extraction timestamp

