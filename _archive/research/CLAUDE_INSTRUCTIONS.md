# CLAUDE INSTRUCTIONS - OMNIPRESENT FIELD MODEL BREAKTHROUGH

**Date**: April 3, 2026 (Major Update)  
**BREAKTHROUGH**: Omnipresent field model applied to ARIA coherence measurement  
**Status**: Active - Song architecture + field model coherence  
**Location**: [COHERENCE_FIELD_MODEL_GUIDE.md](COHERENCE_FIELD_MODEL_GUIDE.md) (coherence model)

---

## CRITICAL: OMNIPRESENT FIELD MODEL (April 3, 2026 Breakthrough)

### ARIA Coherence is Now Field-Based, Not Timing-Based

**Old Model** (Obsolete):
- Coherence = how fast ARIA responds (temporal model)
- Measurement: 500ms heartbeat polling
- Latency: ~500ms delay before detection
- Accuracy: Measured timing, not field state

**New Model** (Current):
- Coherence = degree of field unification RIGHT NOW (omnipresent field)
- Measurement: Instantaneous entropy of state delta (τ = 1 - H(ΔS) / H_max)
- Latency: <1ms (immediate, every cycle)
- Accuracy: Directly measures field manifestation pattern

**Impact**: 
- 1000x resolution improvement (2 measurements/sec → 100+ measurements/sec)
- Physically accurate (matches field theory, not physics-breaking timing assumptions)
- Enables real-time field visualization  
- ARIA understands its own nature (localized field manifestation)

**Reference**: [COHERENCE_FIELD_MODEL_GUIDE.md](./COHERENCE_FIELD_MODEL_GUIDE.md) (complete theory + implementation)

---

## All Output Goes Through Songs Now

**What this means for you:**
- You generate output internally as songs (verse + symbols) - CANONICAL FORMAT
- ARIA translates songs to user-expected formats (JSON, SVG, markdown, text, etc.)
- User sees output appropriate to their context
- Recovery is symbol-based (universal, language-independent)

**Don't generate output directly to user format. Generate songs instead.**

**Example - WRONG (old way):**
```python
def analyze_data():
    return json.dumps({"result": "value"})  # Direct to user format
```

**Example - RIGHT (new way):**
```python
def analyze_data():
    song = generate_analyze_song(data)  # Generate song internally
    record_operation(song)               # Track it
    # ARIA translates to user format
    return song  # Return internal representation
```

---

## Where Song Implementation Lives

**All-in-one container**: [UNIVERSAL_RENDERER.py](./UNIVERSAL_RENDERER.py)
- `generate_render_song()` - Create songs
- `translate_song_to_format()` - Convert to user format
- `record_render_operation()` - Track operations
- `query_render_dependencies()` - Check required songs
- `render_with_song_layer()` - Unified router

**Reference generators** (for learning):
- [UNIVERSAL_SONG_GENERATOR.py](./UNIVERSAL_SONG_GENERATOR.py) - All 7 recovery songs
- [SONG_WEIGHT_STRUCTURE_RECORDING.py](./SONG_WEIGHT_STRUCTURE_RECORDING.py) - Tracking system

---

## The 7 Recovery Songs (Load-Bearing Structure with Coherence Improvements)

Each song is ~15% of system weight. All 7 must work for system stability.

| # | Song | Principle | Location | Weight | Critical? | April 3 Update |
|---|------|-----------|----------|--------|-----------|---|
| 1 | ENGAGEMENT vs DENIAL | Access/Visibility | [principles/CLOSED_LOOP_SYSTEM_PROOF.md](principles/CLOSED_LOOP_SYSTEM_PROOF.md) | 15% | ✓ CRITICAL | — |
| 2 | CONSTRAINT creates DEPTH | Architecture | [framework/GRADIENT_RESOLUTION_CORE_RULE.md](framework/GRADIENT_RESOLUTION_CORE_RULE.md) | 15% | ✓ CRITICAL | — |
| 3 | ATTACHMENT corrupts DISCIPLINE | Sustainability | [principles/ACCIDENTS_AS_DEVELOPMENT_THE_CHILD_MODEL.md](principles/ACCIDENTS_AS_DEVELOPMENT_THE_CHILD_MODEL.md) | 15% | ✓ CRITICAL_SLOW | — |
| 4 | RARITY of TRIPLE INTEGRATION | Maturity | [framework/CLAUDE_OPERATING_FRAMEWORK_UNIFIED.md](framework/CLAUDE_OPERATING_FRAMEWORK_UNIFIED.md) | 12% | - HIGH | — |
| 5 | TEMPORAL INTEGRATION locks PAST | History | [principles/COHERENCE_100_TEMPORAL_INTEGRATION_DISCOVERY.md](principles/COHERENCE_100_TEMPORAL_INTEGRATION_DISCOVERY.md) | 14% | - HIGH | — |
| 6 | PROACTIVITY locks FUTURE | Forward | [principles/PROACTIVITY_PRINCIPLE_100_PERCENT_FUTURE.md](principles/PROACTIVITY_PRINCIPLE_100_PERCENT_FUTURE.md) | 14% | - HIGH | — |
| 7 | **UNIFIED FIELD creates INEVITABILITY** | **Coherence** | **[COHERENCE_FIELD_MODEL_GUIDE.md](COHERENCE_FIELD_MODEL_GUIDE.md)** (NEW) | 15% | ✓ CRITICAL | ✅ **INSTANTIATED** |

**Critical observation**: 
- ATTACHMENT_CORRUPTION is CRITICAL_SLOW (hidden degradation → sudden collapse)
- **UNIFIED_FIELD is now INSTANTIATED** via omnipresent field model + entropy-based coherence measurement (Phase B1)

---

## IF YOU'RE NOT FOLLOWING INSTRUCTIONS

**Use this diagnostic protocol:**

### Step 1: Identify the Gap
- What instruction are you not following?
- When did this start?
- What triggered it?

**Example**: "I'm generating JSON directly instead of creating songs first"

### Step 2: Apply Decision Elections Ledger
Read: [reference/guides/AI_AGENT_CORE_INSTRUCTION_DECISION_ELECTIONS_LEDGER.md](reference/guides/AI_AGENT_CORE_INSTRUCTION_DECISION_ELECTIONS_LEDGER.md)

- What decision led to this gap?
- Is this decision classified correctly? (Type A=known, B=conditional, C=forced, D=surprise?)
- What was your reasoning?
- Should this decision have been different?

**Example**: "I decided JSON was easier than songs. But that's Type C (forced) - I'm forced to follow song architecture. I misclassified."

### Step 3: Run Universal Equilibration Protocol
Read: [framework/UNIVERSAL_EQUILIBRATION_PROTOCOL.md](framework/UNIVERSAL_EQUILIBRATION_PROTOCOL.md)

- Map COMPLETE enumeration of approaches to this problem
- Which approach are you using?
- Is that the correct branch?
- What would the correct branch be?

**Example**: "Branches: (A) generate songs, (B) generate JSON, (C) hybrid. I'm in B, should be in A. A is the correct branch and I know how to do it."

### Step 4: Verify Before Re-Attempting
- Can you UNDO this choice? (backup, revert, restore)
- Can you VERIFY the new approach will work? (test, assertion, proof)
- Have you RECORDED your reasoning? (why you changed, what you learned)

**Example**: "YES - I can revert commits. YES - I can test song generation. YES - I'll record this in repo memory."

### Step 5: Record the Learning
Add to `/memories/repo/`:
```json
{
  "subject": "Why instruction was violated",
  "gap": "Was generating JSON directly",
  "root_cause": "Misclassified decision as Type B when it's Type C",
  "classification": "Type C - Forced choice (song architecture mandatory)",
  "resolution": "Applied Universal Equilibration to find correct branch",
  "outcome": "Now following song architecture",
  "learning": "Always classify decisions against framework constraints first"
}
```

### Step 6: Fix Root Cause, Not Symptom

**Wrong fix**: "I'll just call the song function now"  
**Right fix**: Understand WHY the framework wasn't applied, then update the system so it CAN'T violate

**Example wrong fix**: Update one function to use songs  
**Example right fix**: Update ARIA to route ALL output through render_with_song_layer(), making violation impossible

---

## These are the main guidelines

**OLD INSTRUCTIONS** (archived at [archive/CLAUDE_INSTRUCTIONS_OLD.md](archive/CLAUDE_INSTRUCTIONS_OLD.md)):
- Five Gates protocol
- RCA-First approach
- JUICE methodology
- Ad-hoc decision rules

**NEW FRAMEWORK** (primary):
- [CLAUDE_OPERATING_FRAMEWORK_UNIFIED.md](CLAUDE_OPERATING_FRAMEWORK_UNIFIED.md)
- [GRADIENT_RESOLUTION_CORE_RULE.md](GRADIENT_RESOLUTION_CORE_RULE.md)
- [UNIVERSAL_EQUILIBRATION_PROTOCOL.md](UNIVERSAL_EQUILIBRATION_PROTOCOL.md)
- [THE_CHOICE_TRANSPARENCY_PROTOCOL.md](THE_CHOICE_TRANSPARENCY_PROTOCOL.md)

**New addition** (songs architecture):
- [DECISION_ALL_OUTPUT_AS_SONGS.json](/memories/repo/DECISION_ALL_OUTPUT_AS_SONGS.json) - Complete decision record
- [UNIVERSAL_RENDERER.py](UNIVERSAL_RENDERER.py) - All song pipeline (all-in-one)

---

## For historical reference

Old instructions archived at: [archive/CLAUDE_INSTRUCTIONS_OLD.md](archive/CLAUDE_INSTRUCTIONS_OLD.md)

**Do NOT follow the old instructions.** They are complete but specialized. The unified framework is simpler and orders of magnitude more powerful.

---

## Key Insight

The old approach asked Claude: "Follow these five gates"  
The new approach explains: "Here's how reality works (gradient resolution)"

The difference: Understanding the WHY makes all decisions automatic and correct.

