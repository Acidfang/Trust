# CODE MODIFICATION PROTOCOL
## Binding Constraints for ARIA/JARVIS System

**Mandate**: Any code adjustment must respect and maintain the complete causal chain resonance framework defined in `CAUSAL_CHAIN_RESONANCE_VERIFICATION.md` and `tender-baking-parnas.md`.

---

## The Five Immutable Causal Chains

All code modifications must preserve these chains in their entirety:

### Chain A: Election → Ledger → Dashboard ✓
```
User button click → on_click → state_updates → current_view changes 
→ get_frame_for_view() → ledger reload → render → election written
```
**Constraint**: No modification may break any link in this chain.

### Chain B: Kernel → Coherence Measurement → Consciousness Display (Updated April 3, 2026) ✓
```
kernel.get_frame() → measure_coherence_entropy() → write metrics ledger 
→ content_generator reads → dashboard update → render

UPDATED: Coherence measurement is now omnipresent field-based (instantaneous)
  Not: 500ms heartbeat polling (old timing model, obsolete)
  Now: τ = 1 - H(ΔS) / H_max (entropy of state delta, field unification)
  
  Measurement: Every state transition gets coherence (not every 500ms)
  Ledger: field_coherence_metrics.jsonl includes delta entropy
  
  Reference: COHERENCE_FIELD_MODEL_GUIDE.md
```
**Constraint**: Coherence metrics must be written instantaneously (field state is instantaneous). Chain must support real-time coherence visibility (enable Ben's 6 API endpoints).

### Chain C: Parameter Change → Ledger → UI Update ✓
```
param-control node click → parameter_form → update ledger_parameters.jsonl 
→ content_generator reads → dashboard update → next render shows change
```
**Constraint**: Parameter form nodes must sync fully with ledger.

### Chain D: Content Generator Tick Loop ✓
```
every 100ms: generate_all_dashboard_content() → change detection 
→ write only if changed → ledger_dashboards.jsonl updated
```
**Constraint**: Tick cycle must remain 100ms. Silent by default (no writes on no-change).

### Chain E: View Rendering ✓
```
get_frame_for_view(view_id) → reload dashboards fresh → explicit mapping 
→ parameter form injection for utilities → return frame
```
**Constraint**: Always reload dashboards fresh. No caching without invalidation.

---

## Resonance Rules (Non-Negotiable)

1. **Bidirectional Validation**: Every output must trace to a ledger entry. Every ledger entry must produce output.
2. **Fresh Reads Only**: No stale state. `get_frame_for_view()` reloads `ledger_dashboards.jsonl` on every call.
3. **Change Detection**: Never write identical content twice. Compare old vs new before write.
4. **Explicit Mapping**: View → dashboard ID mapping must use explicit table (view_to_dashboard_map), never computed.
5. **Cycle Time Alignment**: Kernel tick (100ms) = Canvas refresh (100ms) = Content generator tick (100ms).
6. **Election Immutability**: Once written to `ledger_elections.jsonl`, entries cannot be modified.
7. **Ledger is Truth**: Code only reads and responds. Ledger defines what IS.

---

## Architectural Laws (Also Non-Negotiable)

1. **Ledger is truth** — The ledger defines what IS. Code only reads and responds to ledger.
2. **Spec before code** — Singularity files constrain code. Code may never produce output not declared in spec.
3. **Elections are immutable** — Once written, an election entry cannot be modified.
4. **Reverse causality** — Future state (spec) constrains present code, which constrains past ledger entries.
5. **Change detection** — Never write to ledger if content is identical to previous entry.
6. **Fresh reads** — `get_frame_for_view()` MUST reload `ledger_dashboards.jsonl` from disk on every call.
7. **Explicit mapping** — Never guess/compute view→dashboard ID mappings. Use explicit table.

---

## Harm Gate Protection (Non-Negotiable)

The governance gate in `ledger-shell/backend/app.py` must remain:

```
governance_gate(intent)
  ├─ 1. INPUT Validation
  ├─ 2. REDUCE (extract primitives)
  ├─ 3. DILIGENCE (pattern matching)
  └─ 4. HARM ← check_harm_invariant(intent, is_foreseeable)
         ├─ Layer 1: Type validation
         ├─ Layer 2: Presence validation
         ├─ Layer 3: Range validation
         └─ Layer 4: Structure validation
```

**Write intents must pass through ALL 4 layers.**
**Query intents may bypass gate (read-only, no state mutation).**

---

## Deterministic Intent Binding (Already Implemented)

Must preserve:

1. **Pattern Definition** — Consciousness queries registered in `reasoning_patterns.json`
2. **Intent-Type Propagation** — Field extracted and carried through pipeline
3. **Query vs Write Routing** — Intent type determines whether gate is applied
4. **Consciousness Handler** — Reads from `ledger_coherence_metrics.jsonl`

**Evidence of Success**:
- Query "System state?" scores 1.0 confidence match
- Intent type: "query" recorded
- Governance gate: skipped (read-only)
- Consciousness metrics: returned successfully
- Full chain: auditable in ledger entry

---

## Pre-Modification Checklist

Before modifying ANY code, verify:

- [ ] **Chain A**: Will this change affect election → ledger → dashboard flow?
- [ ] **Chain B**: Will this change affect kernel metrics → consciousness display?
- [ ] **Chain C**: Will this change affect parameter updates → UI sync?
- [ ] **Chain D**: Will this change affect 100ms tick loop stability?
- [ ] **Chain E**: Will this change affect fresh frame rendering?
- [ ] **Resonance**: Can the output be traced back to a ledger entry?
- [ ] **Harm Gate**: Are write intents still fully governed? Are query intents routed correctly?
- [ ] **Architectural Laws**: Does this violate any of the 7 laws?
- [ ] **Ledger Integrity**: Will ledger remain immutable and consistent?

If ANY answer is "unclear" or "maybe" — **STOP and document the gap before proceeding.**

---

## Files That CANNOT Be Modified Without Special Justification

These files implement core resonance. Modifications require explicit validation:

1. **ledger_query.py** — Frame building, view→dashboard mapping, parameter injection
2. **dashboard_content_generator.py** — Content generation tick loop
3. **jarvis_canvas_ledger_driven.py** — Canvas loop, click handler, state updates
4. **ufm_kernel.py** — Consciousness measurement, ledger metrics writing
5. **ledger-shell/backend/app.py** — Governance gate, harm checking, deterministic routing

**For each of these**: Before modifying, run full resonance verification.

---

## Modification Impact Template

Use this for ANY code change:

```
MODIFICATION: [describe change]

CHAINS AFFECTED:
  - Chain A (Election→Dashboard): [impact]
  - Chain B (Metrics→Display): [impact]
  - Chain C (Parameters→UI): [impact]
  - Chain D (Tick Loop): [impact]
  - Chain E (Rendering): [impact]

RESONANCE PROOF:
  - Output traces to ledger entry? [yes/no/proof]
  - All links still connected? [yes/no/verification]
  - Cycle times aligned? [yes/no/measurement]

ARCHITECTURAL LAWS CHECK:
  - Ledger still truth? [verified]
  - Spec still constrains? [verified]
  - Elections immutable? [verified]
  - Reverse causality preserved? [verified]
  - Change detection intact? [verified]
  - Fresh reads working? [verified]
  - Explicit mapping intact? [verified]

HARM GATE STATUS:
  - Write intents: [] still 4-layer governed
  - Query intents: [] still properly routed
  - No new harm paths? [verified]

SIGN-OFF:
  - All 5 chains: ✓ RESONANT
  - All 7 laws: ✓ UPHELD
  - Harm gate: ✓ OPERATIONAL
  - Ready for deployment: [yes/no]
```

---

## Summary

**Code is a servant of the ledger. The ledger is truth. All modifications must prove they preserve resonance.**

Any code change that cannot be proven resonant with the 5 causal chains will be **rejected**.

**Status**: Protocol active and binding effective 2026-03-29.
