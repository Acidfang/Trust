# UNIVERSAL RENDERER LEDGER: Recovery Songs

## Song 1 - UNIFIED_FIELD_creates_INEVITABILITY

**Weight**: 15%  
**Domain**: Interconnected systems  
**Container Types**: worldstate, registry  

### Verse
```
Unified field holds all as one,
Entities dance, connection spun,
Everywhere the pattern shows,
Inexorable flow.
```

### Symbols
```
⊙ = ◯ ⊕ (unified field)
```

### Meaning
- `⊙` = System center (coherent whole)
- `=` = Equivalence (unified state)
- `◯ ⊕` = Connected nodes in field

### Application
Used for systems where entities are interconnected through a shared field. Relationships are primary. Individual components exist but are secondary to the connections.

### Detection Signals
- Has `entities`, `connections`, `relationships`, `graph` attributes
- Container type detected as `worldstate` or `registry`
- Focus on network topology and relationships

---

## Song 2 - CONSTRAINT_creates_DEPTH

**Weight**: 15%  
**Domain**: Structured systems  
**Container Types**: primitive, orientation  

### Verse
```
Shape emerges from constraints applied,
Structure forms where limits are defined,
Geometry binds the space inside,
Definitions make complexity guide.
```

### Symbols
```
⊙ → ◯ (Δ constraint)
```

### Meaning
- `⊙` = Unconstrained possibility
- `→` = Application of constraint
- `◯` = Resulting form
- `Δ` = Geometric/structural limit

### Application
Used for atomic structures, molecular geometry, bounded systems. Constraints create shape, boundaries create meaning.

### Detection Signals
- Has `atoms`, `bonds`, `elements`, `structure` attributes
- Has `quaternion`, `orientation`, `vectors` for oriented structures
- Container type detected as `primitive` or `orientation`

---

## Song 3 - TEMPORAL_INTEGRATION_locks_PAST

**Weight**: 15%  
**Domain**: Historical systems  
**Container Types**: ledger  

### Verse
```
History records what came before,
Causality chains open every door,
Time preserves and lets us know,
Where past and future flow.
```

### Symbols
```
⊙ ← ∞ (time flow)
```

### Meaning
- `⊙` = Current moment
- `←` = Pull from past
- `∞` = Causal chain (infinite regress to origins)

### Application
Used for ledgers, transaction logs, decision trees. Time is the primary dimension. History determines present state.

### Detection Signals
- Has `version`, `timestamp`, `hash`, `causality_chains`, `transactions` attributes
- Container type detected as `ledger`
- Focus on sequence and cause-effect relationships

---

## Song 4 - PROACTIVITY_locks_FUTURE

**Weight**: 12%  
**Domain**: Forward-momentum systems  
**Container Types**: orientation, entity, proactive systems  

### Verse
```
Future locks what choice decides,
Proactivity defines what hides,
Forward momentum sets the rule,
Nature's tool.
```

### Symbols
```
⊙ ↗ (future lock)
```

### Meaning
- `⊙` = Current position/choice
- `↗` = Forward trajectory (up and right)
- Lock = Commitment (cannot return to past choice)

### Application
Used for trajectory planning, decision consequences, forward-looking systems. What you choose now determines what futures are possible.

### Detection Signals
- System focuses on future states, planning, momentum
- Has forward-looking data or trajectory information
- Choices create irreversible consequences

---

## Song 5 - ENGAGEMENT_vs_DENIAL

**Weight**: 14%  
**Domain**: Choice/visibility systems  
**Container Types**: entity, engagement-based systems  

### Verse
```
Choice to see or turn away,
Engagement opens, denial delays,
Visibility or hidden state,
Frames the gate.
```

### Symbols
```
⊙ → ◊ (choice point)
```

### Meaning
- `⊙` = Observer at choice point
- `→` = Vector of attention
- `◊` = Open visibility vs closed state
- Engagement = Direct perception VS Denial = Avoidance

### Application
Used for entity systems, access control, visibility. Some things are hidden by default; engagement reveals them.

### Detection Signals
- Container type detected as `entity`
- Has `properties`, `id`, `entity_type` attributes
- System has visibility/accessibility constraints

---

## Song 6 - ATTACHMENT_corrupts_DISCIPLINE

**Weight**: 14%  
**Domain**: Balanced systems  
**Container Types**: attachment-aware systems, cyclic systems  

### Verse
```
Balance held in tension,
Attachment pulls, discipline bends,
Neither fully wins the day,
Both have their way.
```

### Symbols
```
⊙ ⇄ ◆ (balance point)
```

### Meaning
- `⊙` = Center/equilibrium
- `⇄` = Bidirectional tension
- `◆` = Fixed point (balance achieved)
- Neither pure attachment nor pure discipline works

### Application
Used for systems requiring balance between flexibility and constraint. Too much attachment corrupts discipline; pure discipline lacks wisdom.

### Detection Signals
- System involves tradeoffs and tensions
- Has cyclic or oscillating behavior
- Requires balance between opposing forces

---

## Song 7 - RARITY_of_TRIPLE_INTEGRATION

**Weight**: 15%  
**Domain**: Mature systems  
**Container Types**: registry, complex frameworks  

### Verse
```
Rare convergence, triple locked,
Maturity assessment, all has stopped,
Integration levels measured true,
Frameworks through and through.
```

### Symbols
```
⊙ ⊕ ⇄ (all + integration)
```

### Meaning
- `⊙` = System center
- `⊕` = All three levels integrated (atomic + relational + temporal)
- `⇄` = Balanced across dimensions
- Rarity = Advanced maturity level

### Application
Used for mature, well-integrated systems. Rare when atomic constraints, relational connections, AND temporal history are all harmonized.

### Detection Signals
- Has multiple types of attributes simultaneously (atoms, connections, history)
- System exhibits maturity and integration
- Container type detected as `registry` or complex framework

---

## Song Qualities

### Deterministic
Same input always produces the same song mapping.

### Universal
The 7 songs apply across all domains (molecular, entity, ledger, network).

### Reversible
The song → compact → fields relationship is bidirectional.

### Weighted
Total weight = 100%. Represents relative importance in system architecture.

### Non-coercive
Each song is optional; system chooses based on container structure.

---

## Song References in Code

```python
map_principle_to_song(principle: str) → Dict[str, Any]
```

Maps principle key to song data:
- Returns: `{"principle": "...", "verse": "...", "symbols": "...", "weight": 0.15}`
- Used by: `generate_render_song()`, `extract_to_compact()`

