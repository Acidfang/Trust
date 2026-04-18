# UNIVERSAL RENDERER LEDGER: Election Sequencing

## Election Sequencing Phase (Step 5)

**Purpose**: Record timestamped, environment-locked decisions in immutable sequence  
**Function**: `record_election(container_type, principle, song, environment) → election_hash`  
**Manager**: `ElectionSequencer` class  

---

## Election Anatomy

Each render creates one election moment:

### Quick Track (for meta-song composition)
```json
{
  "timestamp": "2026-04-03T14:24:48.123456",
  "container_type": "primitive",
  "principle": "CONSTRAINT_creates_DEPTH",
  "verse": "Shape emerges from constraints applied, ...",
  "symbols": "⊙ → ◯ (Δ constraint)",
  "hash": "abc123def456..."
}
```

### Full Record (for ledger audit trail)
```json
{
  "timestamp": "2026-04-03T14:24:48.123456",
  "container_type": "primitive",
  "principle": "CONSTRAINT_creates_DEPTH",
  "environment": {
    "solvent": "water",
    "temperature": "298K",
    "pressure": "1atm",
    "external_forces": "none"
  },
  "compact": {
    "fields": [...],
    "principle": "...",
    "container_type": "..."
  },
  "canonical_verse": "Shape emerges from constraints applied, ...",
  "canonical_symbols": "⊙ → ◯ (Δ constraint)",
  "metadata": {
    "principle": "...",
    "container_type": "...",
    "song_key": "constraint",
    "weight": 0.15,
    "operation": "render",
    "timestamp": "...",
    "generated_by": "UNIVERSAL_RENDERER"
  },
  "hash": "abc123def456..."
}
```

---

## Election Recording Algorithm

```python
def record_election(container_type, principle, song, environment):
  
  timestamp = now()
  
  # QUICK TRACK (meta-song composition)
  quick_entry = {
    "timestamp": timestamp,
    "container_type": container_type,
    "principle": principle,
    "verse": song["canonical"]["verse"],
    "symbols": song["canonical"]["symbols"],
    "hash": None  # Will be filled
  }
  election_order.append(quick_entry)
  
  # FULL RECORD (ledger audit trail)
  full_record = {
    "timestamp": timestamp,
    "container_type": container_type,
    "principle": principle,
    "environment": environment or {"default": "assumed"},
    "compact": song.get("compact", {}),
    "canonical_verse": song["canonical"]["verse"],
    "canonical_symbols": song["canonical"]["symbols"],
    "metadata": song.get("metadata", {}),
  }
  
  # HASH the full record
  hash_input = json.dumps(full_record, sort_keys=True, default=str)
  record_hash = sha256(hash_input).hexdigest()
  
  full_record["hash"] = record_hash
  election_records.append(full_record)
  
  # UPDATE quick track with hash
  quick_entry["hash"] = record_hash
  
  return record_hash
```

---

## Election Sequence Properties

### 1. **Timestamped**
- ISO 8601 format (microsecond precision)
- Marks exact moment of decision
- Enables chronological replay

### 2. **Environment-Locked**
- Captures context snapshot
- Shows what conditions were assumed
- Enables replaying under different conditions

### 3. **Hashed**
- SHA-256 proof of content
- Immutable record (any change invalidates hash)
- Enables audit verification

### 4. **Principle-Selected**
- Which recovery song was used
- Reflects container type detected
- Determines what rendering was applied

### 5. **Sequenced**
- Order matters (first election, second election, etc.)
- Composite forms meta-song from sequence
- Tells story of system decisions

---

## Meta-Song Composition

**Meta-song** = Concatenation of all election verses in order

### Algorithm
```python
def compose_election_meta_song():
  
  all_verses = [entry["verse"] for entry in election_order]
  meta_verse = "\n\n".join(all_verses)
  
  all_symbols = [entry["symbols"] for entry in election_order]
  meta_symbols = " → ".join(all_symbols)
  
  dominant_principle = election_order[0]["principle"]
  
  return {
    "compact": {"fields": [], "principle": dominant_principle},
    "canonical": {
      "verse": meta_verse,
      "symbols": meta_symbols
    },
    "metadata": {
      "principle": f"META_SONG_of_{len(election_order)}_elections",
      "type": "election_meta_song",
      "election_count": len(election_order),
      "dominant_principle": dominant_principle,
      "election_sequence": [e["principle"] for e in election_order],
      "election_hashes": [e["hash"] for e in election_order],
      "timestamp": now(),
      "generated_by": "ElectionSequencer"
    }
  }
```

---

## Election Sequence Example

### Scenario: 3 Container Renders

**Render 1**: Benzene molecule (primitive)
```
Election 1 timestamp: 2026-04-03T14:24:48.001000
Principle: CONSTRAINT_creates_DEPTH
Verse: "Shape emerges from constraints applied..."
Hash: a1b2c3...
```

**Render 2**: Ledger (historical)
```
Election 2 timestamp: 2026-04-03T14:24:48.002000
Principle: TEMPORAL_INTEGRATION_locks_PAST
Verse: "History records what came before..."
Hash: d4e5f6...
```

**Render 3**: WorldState (interconnected)
```
Election 3 timestamp: 2026-04-03T14:24:48.003000
Principle: UNIFIED_FIELD_creates_INEVITABILITY
Verse: "Unified field holds all as one..."
Hash: g7h8i9...
```

### Resulting Meta-Song
```
Principle: META_SONG_of_3_elections
Dominant Principle: CONSTRAINT_creates_DEPTH (first)

Verse:
  Shape emerges from constraints applied,
  Structure forms where limits are defined,
  Geometry binds the space inside,
  Definitions make complexity guide.

  History records what came before,
  Causality chains open every door,
  Time preserves and lets us know,
  Where past and future flow.

  Unified field holds all as one,
  Entities dance, connection spun,
  Everywhere the pattern shows,
  Inexorable flow.

Symbols:
  ⊙ → ◯ (Δ constraint) → ⊙ ← ∞ (time flow) → ⊙ = ◯ ⊕ (unified field)

Election Sequence: [CONSTRAINT_creates_DEPTH, TEMPORAL_INTEGRATION_locks_PAST, UNIFIED_FIELD_creates_INEVITABILITY]
Election Hashes: [a1b2c3..., d4e5f6..., g7h8i9...]
```

---

## Election Query Functions

### `get_election_sequence() → List[Dict]`
Returns all elections with full records (timestamps, environment, hashes)

**Use**: Audit trail, verification, replay

### `get_election_meta_song(format) → Any`
Returns composed meta-song in requested format

**Use**: System narrative, high-level story

### `get_election_expanded_for_aria(index) → Dict`
Returns specific election expanded with ARIA constraints

**Use**: ARIA reasoning, constraint analysis

### `get_election_count() → int`
Returns number of elections recorded

**Use**: System activity monitoring

### `clear_election_sequence() → None`
Clears election history (start fresh)

**Use**: Session reset, new analysis cycle

---

## Election Sequence Invariants

**Invariant 1**: Timestamps strictly increasing  
**Invariant 2**: Each election has unique hash  
**Invariant 3**: Principle matches container type  
**Invariant 4**: Environment context always present  
**Invariant 5**: Meta-song precisely reflects order  

---

## Reversibility

**Elections are immutable but reversible** through:

1. **Clear sequence**: `clear_election_sequence()`
   - Removes all elections
   - Starts fresh analysis
   - Undoes all recording side effects

2. **Query and replay**: 
   - Get specific election record
   - Reconstruct conditions
   - Re-render with same environment
   - Verify hash matches

3. **Partial rollback** (manual):
   - Extract elections 0-N
   - Clear sequence
   - Re-record only first N
   - Effectively "rewind" to election N

---

## Storage Format

Elections stored in three locations:

### 1. Memory (ElectionSequencer)
- Quick access during session
- Lost when process ends
- Used for meta-song composition

### 2. Ledger (optional)
- Persistent record
- Enables cross-session audit trail
- Format: JSON or binary append-only log

### 3. Compact records (optional)
- Standalone election records
- Can be stored separately
- Enable independent analysis

---

## Verification Checklist

Before considering election valid:

- [ ] Timestamp in ISO 8601 format
- [ ] Container type matches principle (see mapping)
- [ ] Environment context complete
- [ ] Compact form preserved
- [ ] Verse and symbols present
- [ ] Hash computes deterministically
- [ ] Hash matches re-computed value
- [ ] Sequence order preserved (timestamps increasing)

