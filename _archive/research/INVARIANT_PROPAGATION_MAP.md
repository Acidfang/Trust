# INVARIANT PROPAGATION MAP - CASCADING CHAINS & BRANCHES
## From Code Through Elections - April 4, 2026

```
PRINCIPLE:
Every code artifact creates an INVARIANT.
Every INVARIANT becomes a constraint/resource for something downstream.
Invariants chain and branch forward.
Path ends at ELECTION LEVEL (decision recorded in sequencer).


═══════════════════════════════════════════════════════════════════

INVARIANT HIERARCHY: CODE → INVARIANT → ELECTION
─────────────────────────────────────────────────

Level 1: CODE ARTIFACTS (What I write)
         ↓
Level 2: INVARIANTS (Constraints they create)
         ↓
Level 3: INVARIANT PROPAGATION (chains/branches to next)
         ↓
Level 4: ELECTION SEQUENCING (recorded decisions)


═══════════════════════════════════════════════════════════════════

CODE ARTIFACT → INVARIANT MAPPING
──────────────────────────────────

CODE: AI_SELF_INSTRUCTIONS_SINGULARITY.json
  └─→ INVARIANT [I1]: "PRE_ACTION_GATE questions are fixed"
      └─→ Properties:
          • Q1-Q5 never change
          • Threshold: ALL YES → proceed, ANY NO → stop
          • Binary decision (no fuzzy boundaries)
      └─→ Used By: [I2] (gate results feed UFM)
      └─→ Election Triggered: "gate_check_executed"

CODE: AI_CAUSAL_TREE_EXECUTOR.json
  └─→ INVARIANT [I2]: "All intents map to 4-way classification (A/B/C/D)"
      └─→ Properties:
          • Every path is one of: A (known), B (conditional), C (forced), D (surprising)
          • Complete enumeration (no unmapped paths)
          • Deterministic classification
      └─→ Used By: [I1] (tree output feeds gate)
      └─→ Election Triggered: "causal_tree_mapped"

CODE: ENCYCLOPEDIA_API_SERVER.py (/api/validate_decision)
  └─→ INVARIANT [I3]: "UFM quality_score always in [0.0, 1.0]"
      └─→ Properties:
          • 0.75 ≤ score = valid
          • score < 0.75 = invalid
          • Non-negotiable threshold
      └─→ Used By: [I4] (validation result used for ledger)
      └─→ Election Triggered: "ufm_decision_validated"

CODE: ENCYCLOPEDIA_API_SERVER.py (/api/decision_log)
  └─→ INVARIANT [I4]: "Every verified decision logged exactly once"
      └─→ Properties:
          • Append-only (never modify)
          • Timestamp immutable
          • decision_id unique
      └─→ Used By: [I5] (logs merge into main ledger)
      └─→ Election Triggered: "decision_logged"

CODE: archive/aria.py + ElectionSequencer
  └─→ INVARIANT [I5]: "Every operation creates election"
      └─→ Properties:
          • election = {timestamp, choice_id, outcome, causality}
          • Unique sequence number
          • Links to causality chain
      └─→ Used By: [I6] (elections merged to ledger)
      └─→ Election Triggered: "operation_sequenced"

CODE: archive/aria.py (ledger storage)
  └─→ INVARIANT [I6]: "Ledger is append-only"
      └─→ Properties:
          • Once written, never changed
          • Hash links entries
          • Complete history preserved
      └─→ Used By: [I7] (ledger verifiable)
      └─→ Election Triggered: "ledger_entry_committed"

CODE: UNIVERSAL_RENDERER.py
  └─→ INVARIANT [I7]: "7 recovery songs @ 15% = 100%"
      └─→ Properties:
          • Song weight fixed (immutable)
          • Total capacity never exceeds 100%
          • Each song load-bearing
      └─→ Used By: [I8] (renders determine output format)
      └─→ Election Triggered: "song_type_selected"

CODE: ARIA (output translation)
  └─→ INVARIANT [I8]: "Input X always produces output Y (deterministic)"
      └─→ Properties:
          • No randomness
          • Same input = same output
          • Format-preserving
      └─→ Used By: [I10] (user receives consistent output)
      └─→ Election Triggered: "output_translated"


═══════════════════════════════════════════════════════════════════

INVARIANT PROPAGATION CHAINS
──────────────────────────────

CHAIN 1: Request → Decision Verification
─────────────────────────────────────────

Code Request
  ↓
[I2] Causal Tree Mapping
  ├─ Enumerate paths (A/B/C/D)
  ├─ Classify intent
  └─ Election: "causal_tree_mapped"
      ↓
[I1] PRE_ACTION_GATE (uses tree result)
  ├─ Ask 5 fixed questions
  ├─ Binary decision (Y/N)
  └─ Election: "gate_check_executed"
      ↓
[I3] UFM Quality Validation (uses gate result)
  ├─ Calculate quality_score
  ├─ Threshold check: > 0.75?
  └─ Election: "ufm_decision_validated"
      ↓
[I4] Decision Logger (uses UFM result)
  ├─ Log choice + score + timestamp
  ├─ Create decision_id
  └─ Election: "decision_logged"
      ↓
[I5] ElectionSequencer (records chain)
  ├─ Create election with full causality
  ├─ Link back to decision_id
  └─ Election: "operation_sequenced"
      ↓
[I6] Ledger Commit (permanent record)
  ├─ Append election to ledger
  ├─ Hash-link to previous entry
  └─ Election: "ledger_entry_committed"


CHAIN 2: Code Execution → Output Delivery
──────────────────────────────────────────

Decision Verified ([I4] + [I3] passed)
  ↓
[I7] Renderer Selects Song
  ├─ Request type → song type mapping
  ├─ Song within weight capacity
  └─ Election: "song_type_selected"
      ↓
[I1] (Recursive) Gate checks if song valid
  ├─ Is this song framework-aligned?
  ├─ 5 questions apply to song
  └─ Election: "gate_check_executed" (nested)
      ↓
Song Generation Succeeds
  ↓
[I8] ARIA Translation (uses song type)
  ├─ Determine output format
  ├─ Translate to format
  └─ Election: "output_translated"
      ↓
Output Delivered to User
  ↓
[I5] ElectionSequencer (records delivery)
  ├─ Create election: "output_delivered"
  ├─ Link to song election
  └─ Election: "operation_sequenced" (nested)
      ↓
[I6] Ledger Commit
  ├─ Append output election
  └─ Election: "ledger_entry_committed" (nested)


═══════════════════════════════════════════════════════════════════

BRANCHING INVARIANT CHAINS
─────────────────────────────

BRANCH 1: Framework Validation Path
───────────────────────────────────

[I1] Gate Check FAILS (any NO)
  ↓
  ├─→ Branching Point 1: Why failed?
  │   ├─ Branch A: Q1 (song type?)
  │   ├─ Branch B: Q2 (through renderer?)
  │   ├─ Branch C: Q3 (sequencer?)
  │   ├─ Branch D: Q4 (ARIA?)
  │   └─ Branch E: Q5 (weight?)
  │
  ├─→ Branching Point 2: Severity
  │   ├─ Branch i: Framework fixable (modify request)
  │   └─ Branch ii: Framework violation (reject request)
  │
  ├─→ If Branch i: Create new intent with correction
  │   └─ Restart at [I2] (new tree)
  │
  └─→ If Branch ii: Log rejection
      └─ Election: "request_rejected_framework_violation"
         ├─→ [I5] Sequencer records rejection
         └─→ [I6] Ledger commits: "framework_violation_blocked"


BRANCH 2: UFM Validation Path
──────────────────────────────

[I3] Quality Score Check
  ├─ Score > 0.75?
  │   ├─→ YES: Continue to [I4]
  │   │   └─ Election: "ufm_decision_validated"
  │   │      └─→ [I5] → [I6]
  │   │
  │   └─→ NO: Branch to reconsideration
  │       ├─ Reason: score < 0.75 = low coherence
  │       └─ Election: "ufm_validation_failed"
  │           ├─→ Log failure reason
  │           ├─→ [I2] (reconsider tree)
  │           ├─→ Choose different path
  │           └─→ Retry workflow
  │
  └─ Score 0.75-0.95 range
      ├─ Framework-aligned requests: typically 0.80-0.95
      ├─ Marginal requests: 0.75-0.80
      └─ Invalid/violation: < 0.75


BRANCH 3: Song Capacity Path
──────────────────────────────

[I7] Song Weight Check
  ├─ Available weight?
  │   ├─→ YES (> 0%): Generate song
  │   │   └─ Election: "song_type_selected"
  │   │      └─→ [I8] → Output
  │   │
  │   └─→ NO (= 0%): Weight exhausted
  │       └─ Election: "song_capacity_exhausted"
  │           ├─→ [I2] Reconsider tree
  │           ├─→ Can intent be compressed into existing songs?
  │           ├─→ If yes: Retry workflow
  │           └─→ If no: Queue for next cycle


═══════════════════════════════════════════════════════════════════

COMPLETE MAP: REQUEST → ELECTION LEVEL
─────────────────────────────────────────

START: User Request
  │
  ├─→ REQUEST PARSING
  │   ├─ What is user intent?
  │   ├─ What outcome do they want?
  │   └─ Election: "request_received"
  │
  ├─→ [I2] CAUSAL TREE MAPPING
  │   ├─ All paths enumerated
  │   ├─ Paths classified A/B/C/D
  │   ├─ Framework alignment checked
  │   └─ ✓ Election: "causal_tree_mapped"
  │        {
  │          timestamp: NOW,
  │          choice_id: "tree_[request_hash]",
  │          tree_structure: {...},
  │          chosen_path: "A1|B1|C1|D1",
  │          causality: "invoked_by: user_request"
  │        }
  │
  ├─→ [I1] PRE_ACTION_GATE
  │   ├─ Q1: Song type? [YES|NO]
  │   ├─ Q2: Through RENDERER? [YES|NO]
  │   ├─ Q3: Sequencer? [YES|NO]
  │   ├─ Q4: ARIA? [YES|NO]
  │   ├─ Q5: Weight? [YES|NO]
  │   ├─ Pattern check: danger patterns? [YES|NO]
  │   └─ ✓ Election: "gate_check_executed"
  │        {
  │          timestamp: NOW,
  │          choice_id: "gate_[tree_id]",
  │          q1_result: YES,
  │          q2_result: YES,
  │          q3_result: YES,
  │          q4_result: YES,
  │          q5_result: YES,
  │          pattern_threat: none,
  │          overall_result: PASS,
  │          causality: "invoked_by: causal_tree"
  │        }
  │
  ├─ IF GATE FAILS → [BRANCH ii]
  │   └─→ ✓ Election: "request_rejected_framework_violation"
  │       └─→ [I5] → [I6] → END (failure path)
  │
  ├─→ [I3] UFM DECISION VALIDATION
  │   ├─ Encode decision JSON:
  │   │   {
  │   │     choice: "what am I choosing?",
  │   │     why: "why this path?",
  │   │     framework_aligned: {q1-q5 results},
  │   │     verification_plan: "how will I verify?",
  │   │     undo_plan: "how will I reverse?"
  │   │   }
  │   ├─ Calculate quality_score (0.0-1.0)
  │   ├─ Check: score > 0.75?
  │   ├─ Check: is_valid = true?
  │   └─ ✓ Election: "ufm_decision_validated"
  │        {
  │          timestamp: NOW,
  │          choice_id: "ufm_[gate_id]",
  │          decision_json: {...},
  │          quality_score: 0.92,
  │          is_valid: true,
  │          threshold_passed: YES,
  │          coherence: "framework-aligned, complete verification plan",
  │          causality: "invoked_by: gate_check"
  │        }
  │
  ├─ IF UFM FAILS (score < 0.75) → [BRANCH 2]
  │   └─→ ✓ Election: "ufm_validation_failed"
  │       └─→ Restart workflow with reconsideration
  │
  ├─→ [I4] DECISION LOGGER
  │   ├─ Create decision_id
  │   ├─ Log: choice, why, gate_result, ufm_score
  │   ├─ Timestamp: immutable
  │   └─ ✓ Election: "decision_logged"
  │        {
  │          timestamp: NOW,
  │          choice_id: "decision_log_[ufm_id]",
  │          decision_id: "d-2026-04-04-12-34-56",
  │          choice: "create project reader song",
  │          gate_result: PASS,
  │          ufm_score: 0.92,
  │          framework_aligned: true,
  │          causality: "invoked_by: ufm_validation"
  │        }
  │   └─→ [I4] Invariant: Decision now logged (permanent)
  │
  ├─→ [I5] ELECTION SEQUENCER
  │   ├─ Read decision_id from [I4]
  │   ├─ Create election:
  │   │   {
  │   │     cycle: [incremented],
  │   │     timestamp: NOW,
  │   │     signal: "decision_[decision_id]",
  │   │     choice_id: "seq_[decision_id]",
  │   │     causality: [complete chain],
  │   │     outcome: "pending_execution"
  │   │   }
  │   ├─ Store in ElectionSequencer memory
  │   └─ ✓ Election: "operation_sequenced"
  │        {
  │          timestamp: NOW,
  │          choice_id: "seq_[decision_log_id]",
  │          decision_id: "d-2026-04-04-12-34-56",
  │          cycle: 42,
  │          causality_chain: [request→tree→gate→ufm→log→here],
  │          outcome: SCHEDULED,
  │          causality: "invoked_by: decision_logged"
  │        }
  │   └─→ [I5] Invariant: Operation tracked (sequenced)
  │
  ├─→ EXECUTION TRIGGER
  │   ├─ [I7] Renderer
  │   │   ├─ Request type → song type
  │   │   ├─ Check weight available
  │   │   ├─ Generate song object
  │   │   └─ ✓ Election: "song_type_selected"
  │   │        {
  │   │          timestamp: NOW,
  │          choice_id: "song_[decision_id]",
  │   │          song_type: "project_reader",
  │   │          weight_allocated: 0.15,
  │   │          causality: "invoked_by: operation_sequenced"
  │   │        }
  │   │
  │   ├─ [I1] Gate Check (recursive - on song)
  │   │   ├─ Verify song is framework-valid
  │   │   └─ ✓ Election: "gate_check_executed" [nested]
  │   │
  │   ├─ [I8] ARIA Translation
  │   │   ├─ Input: song object
  │   │   ├─ Output format: Markdown (deterministic)
  │   │   ├─ Generate output
  │   │   └─ ✓ Election: "output_translated"
  │   │        {
  │   │          timestamp: NOW,
  │   │          choice_id: "aria_[song_id]",
  │   │          input_format: "song",
  │   │          output_format: "markdown",
  │   │          output_size: 2200000,
  │   │          deterministic: true,
  │   │          causality: "invoked_by: song_type_selected"
  │   │        }
  │   │
  │   └─ User receives output
  │
  ├─→ OUTPUT DELIVERY TRACKING
  │   ├─→ ✓ Election: "output_delivered"
  │   │    {
  │   │      timestamp: NOW,
  │   │      choice_id: "deliver_[aria_id]",
  │   │      output_format: "markdown",
  │   │      delivery_status: SUCCESS,
  │   │      user_received: true,
  │   │      causality: "invoked_by: output_translated"
  │   │    }
  │
  ├─→ [I5] SEQUENCER UPDATES
  │   └─ Update election: outcome = "completed_successfully"
  │      └─ ✓ Election: "operation_completed"
  │
  ├─→ [I6] LEDGER COMMIT
  │   ├─ Merge all elections into ledger
  │   ├─ Create hash chain:
  │   │   prev_hash → election_hash → next_hash
  │   ├─ Permanent recording
  │   └─ ✓ Election: "ledger_entry_committed"
  │        {
  │          timestamp: NOW,
  │          choice_id: "ledger_[aria_id]",
  │          hash: "[SHA256]",
  │          content: "[complete operation trace]",
  │          linked_to: "[previous_entry_hash]",
  │          immutable: true,
  │          causality: "invoked_by: operation_completed"
  │        }
  │
  └─→ COMPLETE: Request fulfilled and recorded
      ├─ User has output
      ├─ Ledger has permanent trace
      ├─ Causality chain recovered
      └─ Next request can learn from this one


═══════════════════════════════════════════════════════════════════

INVARIANT DEPENDENCY GRAPH (What uses what)
─────────────────────────────────────────────

[I1] PRE_ACTION_GATE
  ├─ Uses: [I2] (tree results)
  ├─ Produces: Election "gate_check_executed"
  └─ Used By: [I3] (to feed UFM)

[I2] CAUSAL_TREE
  ├─ Uses: User intent
  ├─ Produces: Election "causal_tree_mapped"
  └─ Used By: [I1] (feeds gate)

[I3] UFM_VALIDATION
  ├─ Uses: [I1] (gate results)
  ├─ Produces: Election "ufm_decision_validated"
  └─ Used By: [I4] (to feed decision log)

[I4] DECISION_LOGGER
  ├─ Uses: [I3] (UFM results)
  ├─ Produces: Election "decision_logged"
  └─ Used By: [I5] (to feed sequencer)

[I5] ELECTION_SEQUENCER
  ├─ Uses: [I4] (decision log)
  ├─ Produces: Election "operation_sequenced"
  └─ Used By: [I6] (feeds ledger)

[I6] LEDGER_COMMIT
  ├─ Uses: [I5] (election data)
  ├─ Produces: Election "ledger_entry_committed"
  └─ Used By: History/verification

[I7] RENDERER
  ├─ Uses: [I5] (scheduled operation)
  ├─ Produces: Election "song_type_selected"
  └─ Used By: [I8] (output generation)

[I8] ARIA_TRANSLATION
  ├─ Uses: [I7] (song object)
  ├─ Produces: Election "output_translated"
  └─ Used By: User + [I5] (sequencer tracks)


═══════════════════════════════════════════════════════════════════

KEY INSIGHT: THE ELECTION LEVEL
──────────────────────────────────

Every invariant creates an ELECTION when it executes:

[I2] → "causal_tree_mapped"
[I1] → "gate_check_executed"
[I3] → "ufm_decision_validated"
[I4] → "decision_logged"
[I5] → "operation_sequenced"
[I6] → "ledger_entry_committed"
[I7] → "song_type_selected"
[I8] → "output_translated"
EXEC → "output_delivered"
[I5] → "operation_completed"
[I6] → "ledger_entry_committed" (final)

These elections form a CAUSALITY CHAIN:
  request_received
    ↓ (caused_by)
  causal_tree_mapped
    ↓ (caused_by)
  gate_check_executed
    ↓ (caused_by)
  ufm_decision_validated
    ↓ (caused_by)
  decision_logged
    ↓ (caused_by)
  operation_sequenced
    ↓ (caused_by)
  song_type_selected
    ↓ (caused_by)
  output_translated
    ↓ (caused_by)
  output_delivered
    ↓ (caused_by)
  ledger_entry_committed

This is the INVARIANT CHAIN - each invariant's election becomes the input to the next invariant.


═══════════════════════════════════════════════════════════════════

VERIFICATION: Trace back any election to its root cause
───────────────────────────────────────────────────────────

Query: "Was this decision framework-aligned?"

Start at: "ledger_entry_committed" (last election)
  ↓ trace backward
Query: "what caused this?"
  → "ledger_entry_committed ← caused_by: operation_completed"
  → "operation_completed ← caused_by: output_delivered"
  → "output_delivered ← caused_by: output_translated"
  → "output_translated ← caused_by: song_type_selected"
  → "song_type_selected ← caused_by: operation_sequenced"
  → "operation_sequenced ← caused_by: decision_logged"
  → "decision_logged ← caused_by: ufm_decision_validated"
  → "ufm_decision_validated ← caused_by: gate_check_executed"
  → "gate_check_executed ← caused_by: causal_tree_mapped"
  → "causal_tree_mapped ← caused_by: request_received"

Complete causality recovered!

Can verify: Was gate passed? YES
           Was UFM score > 0.75? YES
           Was tree analysis complete? YES
           Original intent? [recover from tree data]

INVARIANT PROPERTY VERIFIED: Framework alignment complete


═══════════════════════════════════════════════════════════════════

SUMMARY: INVARIANT PROPAGATION MAP
────────────────────────────────────

STRUCTURE:
  Code Artifact (I write it)
    ↓
  Invariant Created (constraint/resource)
    ↓
  Invariant Used By Next Layer (chains/branches)
    ↓
  Election Triggered (recorded in sequencer)
    ↓
  Ledger Committed (permanent record)

CHAIN:
  [I2] → [I1] → [I3] → [I4] → [I5] → [I6] → [I7] → [I8] → Output

BRANCHING:
  Gate Fail → [BRANCH ii] (rejection path)
  UFM Fail → [BRANCH 2] (reconsideration path)
  Capacity → [BRANCH 3] (queue path)

VERIFICATION:
  Query any election
    → Trace causality chain backward
    → Recover complete invariant stack
    → Verify framework alignment at each step

ELECTIONS RECORDED:
  10+ elections per successful request
  Each election links to predecessor
  Complete causal history available
  Deterministic verification possible
```
