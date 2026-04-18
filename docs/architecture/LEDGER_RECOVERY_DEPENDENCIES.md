# UNIVERSAL RENDERER LEDGER: Recovery & Dependencies

## Recovery Dependencies

**Purpose**: Define which songs are required for each container type to render correctly  
**Function**: `query_render_dependencies(container_type: str) → Dict[str, Any]`  

---

## Container Type → Required Songs Mapping

### PRIMITIVE
**Primary Songs Required**:
- CONSTRAINT_creates_DEPTH (structure geometry)
- UNIFIED_FIELD_creates_INEVITABILITY (atomic bonding field)

**Failure Cascade**:
> Cannot render structure - geometry lost, constraints invisible

**Why**:
- CONSTRAINT songs define the geometric limits (bond angles, distances)
- UNIFIED_FIELD songs explain how atoms cohere into molecule
- Without both: Structure appears as disconnected list of elements

**Recovery Level**: CRITICAL (2/7 songs)

---

### ENTITY
**Primary Songs Required**:
- ENGAGEMENT_vs_DENIAL (visibility/access)
- PROACTIVITY_locks_FUTURE (entity agency/trajectory)

**Failure Cascade**:
> Entity visibility hidden, access control lost

**Why**:
- ENGAGEMENT song determines if entity is visible or concealed
- PROACTIVITY song determines future possibilities for this entity
- Without both: Entity exists but cannot understand access or consequences

**Recovery Level**: HIGH (2/7 songs)

---

### LEDGER
**Primary Songs Required**:
- TEMPORAL_INTEGRATION_locks_PAST (history preservation)
- ENGAGEMENT_vs_DENIAL (revelation of history)

**Failure Cascade**:
> Causality order lost, history fragmented

**Why**:
- TEMPORAL song is the mechanism that locks history immutable
- ENGAGEMENT song determines what history is revealed/hidden
- Without both: Ledger becomes random chronology, causality invisible

**Recovery Level**: CRITICAL (2/7 songs)

---

### WORLDSTATE
**Primary Songs Required**:
- UNIFIED_FIELD_creates_INEVITABILITY (connections/relationships)
- PROACTIVITY_locks_FUTURE (system evolution)

**Failure Cascade**:
> Relationships invisible, world state renders as random

**Why**:
- UNIFIED_FIELD song is the mechanism connecting entities
- PROACTIVITY song determines how state evolves
- Without both: Entities appear isolated, transitions unpredictable

**Recovery Level**: CRITICAL (2/7 songs)

---

### ORIENTATION
**Primary Songs Required**:
- PROACTIVITY_locks_FUTURE (direction/trajectory)
- CONSTRAINT_creates_DEPTH (geometric bounds)

**Failure Cascade**:
> Anchor vectors incorrect, field orientation unknown

**Why**:
- PROACTIVITY song determines directional bias (forward lock)
- CONSTRAINT song defines the geometric space
- Without both: Orientation has no reference frame or meaning

**Recovery Level**: HIGH (2/7 songs)

---

### REGISTRY
**Primary Songs Required**:
- RARITY_of_TRIPLE_INTEGRATION (maturity assessment)
- UNIFIED_FIELD_creates_INEVITABILITY (framework integration)

**Failure Cascade**:
> Cannot measure system health, frameworks appear fragmented

**Why**:
- RARITY song evaluates if all three abstraction levels are mature
- UNIFIED_FIELD song connects the frameworks together
- Without both: Cannot assess health or understand coherence

**Recovery Level**: MEDIUM (2/7 songs)

---

### GENERIC
**Primary Songs Required**:
- CONSTRAINT_creates_DEPTH (fallback structure)

**Failure Cascade**:
> Generic render capability lost

**Why**:
- CONSTRAINT song is the baseline for any structure
- Generic types have no specific requirements
- Can recover with just structure constraint knowledge

**Recovery Level**: LOW (1/7 songs)

---

## Dependency Graph

```
UNIFIED_FIELD
  ├─ WORLDSTATE
  ├─ REGISTRY
  └─ PRIMITIVE

CONSTRAINT
  ├─ PRIMITIVE
  ├─ ORIENTATION
  ├─ GENERIC
  └─ (fallback)

TEMPORAL
  └─ LEDGER

PROACTIVITY
  ├─ WORLDSTATE
  ├─ ENTITY
  ├─ ORIENTATION
  └─ (future systems)

ENGAGEMENT
  ├─ ENTITY
  └─ LEDGER

ATTACHMENT
  └─ (balance/cyclic systems)

RARITY
  └─ REGISTRY
```

---

## Recovery Strategy by Song

### If UNIFIED_FIELD Corrupts
**Affects**: WORLDSTATE, REGISTRY, PRIMITIVE  
**Severity**: HIGH (3 container types affected)  
**Recovery**:
1. Try rendering as schema/tree instead of network
2. Fallback to CONSTRAINT song for primitive structure
3. Relationships appear as lists instead of unified field

**Testable**: Can WORLDSTATE render when UNIFIED_FIELD unavailable?

### If CONSTRAINT Corrupts
**Affects**: PRIMITIVE, ORIENTATION, GENERIC, (fallback)  
**Severity**: HIGH (core rendering)  
**Recovery**:
1. All geometric information lost
2. Fallback to list representation (no structure)
3. PRIMITIVE containers render as "atoms + bonds" without geometry
4. GENERIC containers render as "structure" without details

**Testable**: Do atoms render without bond angles?

### If TEMPORAL Corrupts
**Affects**: LEDGER  
**Severity**: CRITICAL (only 1 type, but core function)  
**Recovery**:
1. Ledger becomes random sequence
2. Causality chains appear broken
3. History is readable but causation is unknowable

**Testable**: Can LEDGER show transactions without causal order?

### If PROACTIVITY Corrupts
**Affects**: WORLDSTATE, ENTITY, ORIENTATION, (future systems)  
**Severity**: MEDIUM-HIGH (3 types, but non-critical rendering)  
**Recovery**:
1. Forward trajectory information lost
2. Systems render as static snapshots
3. Evolution/agency information unavailable

**Testable**: Can ENTITY render without future possibilities?

### If ENGAGEMENT Corrupts
**Affects**: ENTITY, LEDGER  
**Severity**: MEDIUM (2 types, access control)  
**Recovery**:
1. Visibility/access information lost
2. Everything renders as visible/accessible
3. Hidden states become revealed

**Testable**: Do all entities render as visible?

### If ATTACHMENT Corrupts
**Affects**: (balance systems only)  
**Severity**: LOW (specialized domain)  
**Recovery**:
1. Balance calculations unavailable
2. Cyclic systems render as pure attachment or pure discipline
3. Tension information lost

**Testable**: Do cyclic systems render unbalanced?

### If RARITY Corrupts
**Affects**: REGISTRY  
**Severity**: MEDIUM (framework assessment)  
**Recovery**:
1. Cannot assess maturity
2. Frameworks appear fragmented
3. Integration level measurement lost

**Testable**: Can REGISTRY render without maturity assessment?

---

## Cascade Severity Levels

| Level | Cascade | Example | Recovery |
|-------|---------|---------|----------|
| CRITICAL | Core rendering breaks | LEDGER (TEMPORAL) | Must restore song |
| HIGH | Multiple types fail | UNIFIED_FIELD (3 types) | Fallback rendering |
| MEDIUM | Some access lost | ENGAGEMENT (2 types) | Partial rendering |
| LOW | Specialized only | ATTACHMENT (1 type) | Graceful degradation |

---

## Dependency Verification

### Check 1: Required Songs Present?
```python
required = query_render_dependencies(container_type)["required"]
songs_available = [s for s in list_all_songs()]
missing = [s for s in required if s not in songs_available]

if missing:
  raise ValueError(f"Missing required songs: {missing}")
```

### Check 2: Can Render with Fallbacks?
```python
cascade = check_render_cascade(container_type)
# If cascade describes graceful fallback, can render
# If cascade describes critical failure, cannot render
```

### Check 3: Recovery Path Available?
```python
# For each missing song, is there a recovery strategy?
recovery_available = all(
  song in RECOVERY_STRATEGIES 
  for song in missing_songs
)
```

---

## Undo/Reversal for Dependencies

**If rendering fails due to missing songs**:

1. **Identify**: Which song is missing?
2. **Restore**: Restore that song from backup
3. **Verify**: Re-render and check success
4. **Document**: Record which song failure occurred

**Full reversal requires**: 
- Backup of all 7 songs (source of truth)
- Versioning of song changes
- Ability to restore to prior state

---

## Cascade Prevention

To avoid cascades:

1. **Always backup all 7 songs**
2. **Version control songs** (track changes)
3. **Verify songs before rendering**
4. **Use fallbacks gracefully**
5. **Log dependency failures**
6. **Test cascade paths** (simulate failures)

---

## Dependency Testing Checklist

- [ ] Can render without each song individually?
- [ ] Cascade messages are accurate?
- [ ] Fallback rendering available?
- [ ] Recovery paths documented?
- [ ] All 7 songs present and valid?
- [ ] Hash verification passes?
- [ ] Container type to principle mapping correct?

