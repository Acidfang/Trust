# UNIVERSAL RENDERER LEDGER: ARIA Expansion

## ARIA Expansion Phase (Step 3)

**Purpose**: Convert compact form to semantic expansion with environment context  
**Function**: `expand_for_aria(compact: Dict, environment: Optional[Dict], timestamp: Optional[str]) → Dict[str, Any]`  
**Input**: Compact form from extraction  
**Output**: Fully expanded form with field constraints and hashing  

---

## ARIA Expansion Structure

```json
{
  "timestamp": "2026-04-03T14:24:48.123456",
  "environment": {
    "solvent": "none_assumed|water|organic|vacuum",
    "temperature": "298K",
    "pressure": "1atm",
    "external_forces": "none|gravity|magnetic_field|..."
  },
  "source_compact": {
    ... (original compact form)
  },
  "field_verses": [
    {
      "field": "atoms",
      "count": 6,
      "element": "Carbon",
      "constraints": "sp2 hybridized, planarity constraint, 120° bond angles"
    },
    {
      "field": "atoms",
      "count": 6,
      "element": "Hydrogen",
      "constraints": "Terminal hydrogen, single bond only, no branching, H-count=6"
    },
    {
      "field": "bonds",
      "count": 6,
      "order": 1.5,
      "constraints": "Aromatic resonance, delocalized electrons, stability requirement"
    }
  ],
  "principle": "CONSTRAINT_creates_DEPTH",
  "container_type": "primitive",
  "hash": "abc123def456..."
}
```

---

## Environment Context

### Default Environment (if not provided)
```json
{
  "solvent": "none_assumed",
  "temperature": "298K",
  "pressure": "1atm",
  "external_forces": "none"
}
```

### Environment Variables

#### solvent
Values: `none_assumed`, `water`, `organic`, `vacuum`, `buffer`, `gas`, etc.

**Impact on constraints**:
- If water: Adds hydration layer, polarization effects, solvation constraints
- If organic: Adds non-polar interaction effects
- If vacuum: Removes solvation, simplifies constraints

Example:
```
Carbon in water → "solvated, hydration layer, polarization effects"
Carbon in none → "sp2 hybridized, planarity constraint, 120° angles"
```

#### temperature
Values: "0K", "298K", "373K", etc.

**Impact on constraints**:
- Higher temperature: Increased molecular motion, stability concerns
- Lower temperature: Reduced motion, frozen-state assumptions
- Room temperature (298K): Standard assumptions

#### pressure
Values: "1atm", "0.1atm", "10atm", etc.

**Impact on constraints**:
- Higher pressure: Compression effects, density changes
- Lower pressure: Expansion assumptions
- Standard (1atm): Baseline

#### external_forces
Values: `none`, `gravity`, `magnetic`, `electric`, `shear`, etc.

**Impact on constraints**:
- Gravity: Directionality bias (down)
- Magnetic: Alignment constraints
- Electric: Polarization effects

---

## Constraint Generation Algorithm

```python
def _generate_field_constraints(field, environment):
  
  field_type = field["type"]
  element = field.get("element", "")
  count = field.get("count", 1)
  order = field.get("order", 1.0)
  
  solvent = environment.get("solvent", "none_assumed")
  temp = environment.get("temperature", "298K")
  pressure = environment.get("pressure", "1atm")
  forces = environment.get("external_forces", "none")
  
  # Generate constraints based on field type + environment
  
  IF field_type == "atoms":
    IF element == "Carbon":
      base = "Carbon center"
      IF solvent == "water":
        return f"{base}, solvated, hydration layer, polarization effects"
      ELIF solvent == "organic":
        return f"{base}, lipophilic, van der Waals interactions"
      ELSE:
        return f"{base}, sp2 hybridized, planarity constraint, 120° bond angles"
    
    ELIF element == "Hydrogen":
      constraints = f"Terminal hydrogen, single bond only, no branching, H-count={count}"
      IF forces.contains("magnetic"):
        constraints += ", hydrogen bonding constraints"
      return constraints
    
    ELSE:
      return f"{count}× {element} atoms, standard bonding"
  
  ELIF field_type == "bonds":
    IF order == 1.5:
      constraints = "Aromatic resonance, delocalized electrons, stability requirement"
    ELIF order == 1.0:
      constraints = "Single bond, localized electron pair, standard bond length"
    ELIF order == 2.0:
      constraints = "Double bond, restricted rotation, reactivity core"
    ELSE:
      constraints = f"Bond order {order}, standard constraints"
    
    IF temp > 373:
      constraints += ", thermal motion increases"
    
    return constraints
  
  ELIF field_type == "connections":
    constraints = f"Network connectivity, {count} connections, graph topology"
    IF forces.contains("gravity"):
      constraints += ", downward bias"
    return constraints
  
  ELSE:
    return f"{field_type} constraint, count={count}"
```

---

## Hashing for Determinism

**Purpose**: Prove that the expansion is deterministic and immutable  
**Method**: SHA-256 hash of expansion (without hash field)

```python
hash_input = json.dumps({
  "timestamp": "...",
  "environment": {...},
  "source_compact": {...},
  "field_verses": [...],
  "principle": "...",
  "container_type": "..."
}, sort_keys=True, default=str)

expansion_hash = hashlib.sha256(hash_input.encode()).hexdigest()
```

**Hash Properties**:
- **Deterministic**: Same input → same hash always
- **Immutable**: Changing any field changes hash
- **Auditable**: Can verify expansion hasn't been modified
- **Unique**: Collision probability negligible

---

## ARIA Expansion Examples

### Example 1: Benzene Expanded

**Input Compact**:
```json
{
  "fields": [
    {"type": "atoms", "count": 6, "element": "C"},
    {"type": "atoms", "count": 6, "element": "H"},
    {"type": "bonds", "count": 6, "order": 1.5},
    {"type": "bonds", "count": 6, "order": 1.0}
  ],
  "principle": "CONSTRAINT_creates_DEPTH"
}
```

**Expansion (solvent=water, T=298K)**:
```json
{
  "timestamp": "2026-04-03T14:24:48",
  "environment": {
    "solvent": "water",
    "temperature": "298K",
    "pressure": "1atm",
    "external_forces": "none"
  },
  "field_verses": [
    {
      "field": "atoms",
      "count": 6,
      "element": "C",
      "constraints": "Carbon center, solvated, hydration layer, polarization effects"
    },
    {
      "field": "atoms",
      "count": 6,
      "element": "H",
      "constraints": "Terminal hydrogen, single bond only, no branching, H-count=6"
    },
    {
      "field": "bonds",
      "count": 6,
      "order": 1.5,
      "constraints": "Aromatic resonance, delocalized electrons, stability requirement"
    },
    {
      "field": "bonds",
      "count": 6,
      "order": 1.0,
      "constraints": "Single bond, localized electron pair, standard bond length"
    }
  ],
  "principle": "CONSTRAINT_creates_DEPTH",
  "hash": "2c26b46911185131006ba849b2e2daed29f97fa1f9be30d7b67a1cd491fe3d6f"
}
```

---

### Example 2: Entity Expanded

**Input Compact**:
```json
{
  "fields": [
    {"type": "structure", "count": 1, "description": "entity"}
  ],
  "principle": "ENGAGEMENT_vs_DENIAL"
}
```

**Expansion (T=298K)**:
```json
{
  "timestamp": "2026-04-03T14:24:48",
  "environment": {
    "solvent": "none_assumed",
    "temperature": "298K",
    "pressure": "1atm",
    "external_forces": "none"
  },
  "field_verses": [
    {
      "field": "structure",
      "count": 1,
      "constraints": "Entity structure constraint, count=1"
    }
  ],
  "principle": "ENGAGEMENT_vs_DENIAL",
  "hash": "3f0d6e2edc088c308ec7b8c8f88a8f5a9f1c8e0d9f8c7b6a5f4e3d2c1b0a9f8"
}
```

---

## ARIA Usage in Reasoning

ARIA system uses expanded form to:

1. **Understand Constraints**
   - Field verses explain what restrictions apply
   - Environment context shows baseline assumptions
   - Can reason about feasibility

2. **Trace Environmental Dependencies**
   - Timestamp shows when expansion occurred
   - Environment shows exact conditions
   - Can replay with different environments

3. **Verify Determinism**
   - Hash proves expansion matches input
   - Can re-expand and verify hash matches
   - Guarantees reproducibility

4. **Audit Reasoning Chain**
   - Full record of what ARIA saw
   - When it was observed
   - Under what environmental conditions

---

## Reversibility

**Expansion is reversible if you keep**:
- Compact form (can re-expand with same environment)
- Environment context (needed to match constraints)
- Timestamp (marks decision moment)

**Full replay requires**: Compact + Environment + Timestamp  
**Verification requires**: Hash (ensures accuracy)

---

## Verification Checklist

Before using expanded form:

- [ ] Timestamp present (or generated)
- [ ] Environment at least has defaults
- [ ] Field verses count matches source compact field count
- [ ] All constraints generated successfully
- [ ] Hash computes deterministically
- [ ] Hash matches re-computed hash (for verification)
- [ ] Principle and container_type preserved from source

