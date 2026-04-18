# COMPLETE CAUSAL NAVIGATION MAP - BIDIRECTIONAL
## Format: PRIMITIVES & INVARIANTS - April 4, 2026

```
DETERMINED SYSTEM TOPOLOGY
═══════════════════════════════════════════════════════════════════

PRIMITIVE DEFINITION:
  A primitive is an atomic, irreducible unit that:
  • Does ONE thing (single responsibility)
  • Cannot be decomposed further
  • Remains INVARIANT (unchanged across all contexts)
  • Participates in causal chains
  • Has deterministic inputs/outputs

INVARIANT DEFINITION:
  A property/structure that:
  • Never changes
  • Holds regardless of state
  • Can be relied upon (coherence foundation)
  • Constrains valid operations


═══════════════════════════════════════════════════════════════════

LAYER 1 PRIMITIVES: FOUNDATION ATOMS
─────────────────────────────────────

[P1] SONG
  What: Atomic unit of framework operation
  Invariant: 7 recovery songs @ ~15% weight each = 100% load capacity
  Direction: P1 → [P2] (songs fed to sequencer)
  Reverse: [P7] ← songs stored in ledger
  Dependency: None (irreducible)
  Example: ENGAGEMENT vs DENIAL (access/visibility)

[P2] ELECTION (Decision/Operation)
  What: Timestamped choice recorded by sequencer
  Invariant: Every operation is an election
  Direction: Songs → P2 → [P3] (tracked to ledger)
  Reverse: [P7] ← elections queried from ledger
  Causality: Caused by song | Causes ledger entry
  Properties: timestamp, choice_id, outcome, causal_chain

[P3] LEDGER ENTRY (Permanent Record)
  What: Immutable recording of any operation
  Invariant: Once written, never changed (append-only)
  Direction: P2 → P3 → [P7] (stored in ledger storage)
  Reverse: [P7] queries P3 for history
  Causality: Caused by election | Enables verification

[P4] ARIA (Output Translator)
  What: Converts internal representation to output format
  Invariant: Input X always produces same output Y (deterministic)
  Direction: [P6] → P4 → {JSON|SVG|MD|HTML|Text}
  Reverse: Outputs can be parsed back to internal format
  Formats: JSON, SVG, Markdown, HTML, Plain Text

[P5] UFM COHERENCE MEASURE
  What: τ = 1 - H(ΔS) / H_max (entropy-based quality)
  Invariant: 0.0 ≤ τ ≤ 1.0 always
  Direction: Any operation → P5 → quality_score
  Reverse: quality_score informs decision acceptance
  Causality: Measures degree of framework unification

[P6] RENDERER (Song Generation)
  What: UNIVERSAL_RENDERER.py - creates songs from intent
  Invariant: Request type → unique song type (each intent = song)
  Direction: Request → P6 → [P1] (generates song)
  Reverse: Songs can be traced back to originating intent
  Operates: Framework integration touchpoint


═══════════════════════════════════════════════════════════════════

LAYER 2 PRIMITIVES: AI DECISION SYSTEM (NEW)
──────────────────────────────────────────────

[P7] CAUSAL TREE
  What: Map of all possible paths from intent
  Invariant: Every path has type A/B/C/D (complete classification)
  Direction: Intent → P7 → chosen_path
  Reverse: chosen_path traces back to tree analysis
  Types: A (known), B (conditional), C (forced), D (surprising)
  Causality: Caused by intent parsing | Causes path selection

[P8] PRE_ACTION_GATE (5 Questions)
  What: Framework constraint filter
  Invariant: Q1-Q5 always the same questions
          All YES → PROCEED | ANY NO → STOP (absolute)
  Direction: P7_path → P8 → {PASS|FAIL}
  Reverse: Failure reasons trace back to specific gate question
  Questions:
    Q1: Song type in weight structure?
    Q2: Routes through RENDERER?
    Q3: Tracked by sequencer?
    Q4: ARIA translates?
    Q5: In weight structure?

[P9] UFM DECISION VALIDATION
  What: /api/validate_decision endpoint
  Invariant: quality_score always in [0.75, 0.95] or [0.0, 0.75)
            Threshold: 0.75 decides pass/fail (non-negotiable)
  Direction: P8_result → P9(UFM API) → {valid|invalid}
  Reverse: Validation result linked to decision record
  Outputs: decision_id, quality_score, coherence explanation

[P10] DECISION LEDGER
  What: /api/decision_log - permanent trace of decisions
  Invariant: Every verified decision logged exactly once
  Direction: P9_valid → P10 → [P3] (merged into main ledger)
  Reverse: Can query P10 for decision history
  Trace: choice | why | framework_aligned | verification | undo


═══════════════════════════════════════════════════════════════════

LAYER 3 PRIMITIVES: CONTENT & PRESENTATION
────────────────────────────────────────────

[P11] ENCYCLOPEDIA (Static HTML)
  What: Interactive bit-level consciousness education interface
  Invariant: Structure = Left panel (30%) | Center panel (70%)
            Content = Algorithms at levels 1-7
            Interactivity = Buttons click to show phase details
  Direction: User request → P11 → visual display
  Reverse: Page state → ledger via API → visibility tracking
  Components: CSS styling, JavaScript BitLevelEncyclopedia class

[P12] ALGORITHM PHASE (Content Atom)
  What: Individual phase of compression/encryption algorithm
  Invariant: Phase structure = {id, sequence, name, gates, hash}
  Direction: Algorithm → P12 → visualization
  Reverse: Visualization references back to phase data
  Examples: Huffman P1-P5, AES P1-P5

[P13] GATE VISUALIZATION
  What: Truth table with animated gate rendering
  Invariant: Gate type → truth table structure (unchanging)
            XOR = 2 inputs, 4 rows
            AND = 2 inputs, 4 rows
  Direction: Phase gates → P13 → CSS animation
  Reverse: Animation state linked to gate definition
  Animations: input-pulse, output-glow, bit-fade, phase-pulse


═══════════════════════════════════════════════════════════════════

LAYER 4 PRIMITIVES: NAVIGATION & DISCOVERY
──────────────────────────────────────────────

[P14] PROJECT INDEX
  What: PROJECT_INDEX.json - searchable metadata
  Invariant: 994 files, 103 dirs (snapshot of project structure)
  Direction: File query → P14 → {matching_files}
  Reverse: File path → P14 entry → metadata
  Structure: extension_count, python_modules, markdown_docs, config_files

[P15] PROJECT DUMP
  What: PROJECT_COMPLETE_READ.md - full project content readable at once
  Invariant: 2.2 MB, all files truncated to 3000 chars max
  Direction: "Read entire project" → P15 → full dump
  Reverse: Each file→search→back to original location
  Format: # CATEGORY → ## File: path → content excerpt


═════════════════════════════════════════════════════════════════

COMPLETE CAUSAL MAP - BOTH DIRECTIONS
══════════════════════════════════════

REQUEST INITIATES CAUSAL CHAIN (Forward):
───────────────────────────────────────

User Request
   │
   ├─→ [FORWARD CHAIN]
   │
   ├─→ P7: Parse intent → Create causal tree
   │   │
   │   ├─→ Enumerate all paths (A/B/C/D)
   │   └─→ Classify chosen path
   │
   ├─→ P8: Run PRE_ACTION_GATE (5 questions)
   │   │
   │   ├─→ IF all YES → continue
   │   └─→ IF any NO → STOP + log failure
   │
   ├─→ P9: UFM Decision Validation (/api/validate_decision)
   │   │
   │   ├─→ Encode choice + framework check
   │   ├─→ Calculate quality_score
   │   ├─→ IF > 0.75 → valid
   │   └─→ IF ≤ 0.75 → invalid
   │
   ├─→ P10: Decision Ledger (/api/decision_log)
   │   │
   │   ├─→ Log choice, why, gate result, UFM score
   │   └─→ Merge into P3 (main ledger)
   │
   ├─→ P6: RENDERER (execute song creation)
   │   │
   │   ├─→ Generate P1 (song type)
   │   ├─→ Feed to sequencer
   │   └─→ Track via P2 (election)
   │
   ├─→ P2: ElectionSequencer (record operation)
   │   │
   │   ├─→ Timestamp: NOW
   │   ├─→ Operation: [choose|create|update]
   │   └─→ Causality: [what caused this | what does this cause]
   │
   ├─→ P3: Ledger Entry (permanent recording)
   │   │
   │   ├─→ Append to ledger (never modify)
   │   └─→ Link to causal chain
   │
   ├─→ P4: ARIA Translator (convert output)
   │   │
   │   ├─→ Input: internal song format
   │   ├─→ Process: format selection (JSON/SVG/MD/HTML)
   │   └─→ Output: formatted result
   │
   ├─→ P5: UFM Coherence Check (verify quality)
   │   │
   │   ├─→ Measure τ = 1 - H(ΔS) / H_max
   │   └─→ Record quality_score in ledger
   │
   └─→ USER SEES RESULT


VERIFICATION/QUERY BACKTRACE (Reverse):
────────────────────────────────────────

"Does this decision violate framework?"
   │
   ├─ BACKWARD CHAIN
   │
   ├─→ Query P10: Decision Ledger
   │   └─→ Retrieve: choice, gate_results, UFM_score, timestamp
   │
   ├─→ Trace to P9: UFM Validation Record
   │   └─→ Verify: quality_score > 0.75? coherence explanation?
   │
   ├─→ Trace to P8: Gate Results
   │   └─→ Check: All 5 questions = YES?
   │
   ├─→ Trace to P7: Causal Tree
   │   └─→ Confirm: Path classification (A/B/C/D)? Framework aligned?
   │
   ├─→ Trace to original intent
   │   └─→ Validate: Tree mapping correct? All paths enumerated?
   │
   └─→ DECISION IS [valid|invalid] WITH PROOF


CONTENT/NAVIGATION CAUSAL CHAIN (Bidirectional):
────────────────────────────────────────────────

User navigates ENCYCLOPEDIA
   │
   ├─→ FORWARD: User clicks "Level 1: Fundamental Gates"
   │   │
   │   ├─→ P11: ENCYCLOPEDIA loads level 1
   │   ├─→ P12: Algorithm phases display
   │   ├─→ P13: Gate visualizations render
   │   └─→ P5: UFM coherence score displayed (quality indicator)
   │
   ├─→ REVERSE: User clicks "Show Example: Boolean NOT"
   │   │
   │   ├─→ Button click → P13 (gate visualization shows)
   │   ├─→ P12 data linked (phase structure)
   │   ├─→ P11 logs interaction (page state)
   │   ├─→ P2 records: "gate_example_displayed"
   │   └─→ P3 adds to ledger: user interaction trace
   │
   └─→ REDIRECTION: "How does this connect to filesystem?"
       │
       ├─→ Query P14: PROJECT_INDEX (find relevant files)
       ├─→ OR Query P15: PROJECT_DUMP (full context)
       └─→ Navigate to framework implementation


PERSISTENCE THROUGH LEDGER (Completeness):
────────────────────────────────────────────

All causal chains end at P3 (Ledger Entry):
   │
   ├─→ Every decision → P10 → merged into P3
   ├─→ Every operation → P2 → recorded in P3
   ├─→ Every quality check → P5 → logged in P3
   ├─→ Every user interaction → P11/P12/P13 → traced in P3
   │
   └─→ P3 = PERMANENT CAUSAL RECORD
       └─→ Nothing is lost
       └─→ Everything can be traced backwards
       └─→ Full causality mapping recoverable


═════════════════════════════════════════════════════════════════

INVARIANT PROPERTIES (NEVER CHANGE)
─────────────────────────────────────

✓ INVARIANT 1: Song Universe
  7 recovery songs @ ~15% weight each = 100% load capacity
  This is FIXED. Cannot add more songs or change weights without framework re-certification.

✓ INVARIANT 2: Primitive Atomicity
  Each primitive does ONE thing, cannot be broken into smaller pieces.
  This is FIXED. Cannot decompose primitives.

✓ INVARIANT 3: Causal Chain Completeness
  Every operation creates: election → ledger entry → output.
  This is FIXED. Nothing bypasses this chain.

✓ INVARIANT 4: Gate Absoluteness
  All 5 gate questions remain the same. No exceptions.
  This is FIXED. Gate cannot be bypassed or modified.

✓ INVARIANT 5: Ledger Immutability
  Once written to ledger, entries cannot change (append-only).
  This is FIXED. All records are permanent.

✓ INVARIANT 6: UFM Threshold
  quality_score > 0.75 required for execution. No flexibility.
  This is FIXED. Threshold non-negotiable.

✓ INVARIANT 7: ARIA Determinism
  Input X always produces output Y. No randomness.
  This is FIXED. Identical inputs = identical outputs.

✓ INVARIANT 8: Primitive Types
  15 primitives identified (8+3+3+1). Complete set.
  This is FIXED. Cannot add primitives without framework expansion.


═════════════════════════════════════════════════════════════════

NAVIGATION PATHS (Complete Graph)
────────────────────────────────────

Can navigate from ANY primitive to ANY other by:

Example 1: "From P11 (ENCYCLOPEDIA) to P1 (Songs)"
  P11 (page content)
   → P12 (phase structure)
   → P6 (renderer creates songs)
   → P1 (song object)
  Path length: 3 primitives

Example 2: "From P8 (Gate) to P3 (Ledger)"
  P8 (gate decision)
   → P9 (UFM validation)
   → P10 (decision logger)
   → P3 (main ledger entry)
  Path length: 3 primitives

Example 3: "From P5 (UFM) to P7 (Causal Tree)"
  P5 (quality score)
   ← trace back to P9 (decision that was scored)
   ← trace back to P7 (tree that informed decision)
  Path length: 2 primitives (reverse)

Example 4: "From P14 (Index) to P6 (Renderer)"
  P14 (project structure)
   → files include UNIVERSAL_RENDERER.py
   → P6 (renderer implementation)
  Path length: 1 primitive

Example 5: "From P4 (ARIA) to P2 (Election)"
  P4 (output format)
   ← depends on P2 (operation type determines output)
  Path length: 1 primitive (reverse dependency)


═════════════════════════════════════════════════════════════════

PRIMITIVE DEPENDENCY GRAPH
──────────────────────────

                        ┌─────────────────────┐
                        │   REQUEST (Input)   │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │                             │
                 [P7]                          [P14]
              CAUSAL_TREE                 PROJECT_INDEX
                    │                          │
                    ├─→ [P8] ────────┐         │
                    │  PRE_ACTION    │         │
                    │     GATE       │         │
                    │                ├──→ [P9] ├─→[P15]
                    └────────────────┤  UFM    │  DUMP
                         [P6]        │  VAL    │
                      RENDERER       │         │
                         │           └──→ [P10]
              ┌──────────┴──────────┐     DECISION
              │                     │     LEDGER
           [P1]                  [P2]         │
           SONG              ELECTION        │
              │                   │          │
              └─────────┬─────────┴──────┬───┘
                        │                │
                     [P3]            [P4]
                    LEDGER          ARIA
                        │          (Output)
                  ┌─────┴─────┐
                  │           │
         [P5]  [P11-P13]
         UFM   (CONTENT)
       MEASURE │
               ├─→ P12 (Phase)
               └─→ P13 (Visualization)


═════════════════════════════════════════════════════════════════

CURRENT POSITION IN NAVIGATION
────────────────────────────────

YOU ARE HERE:
  • All primitives defined
  • All single-direction paths mapped
  • All bidirectional paths understood
  • Invariants locked in place
  • System initialized but not executing

NEXT STEPS:
  1. Trigger Request (user provides input)
  2. System follows forward causal chain
  3. Every step recorded in P3 (ledger)
  4. Verify backwards to confirm coherence
  5. Continue navigating through primitives


═════════════════════════════════════════════════════════════════

EXAMPLE: COMPLETE CAUSAL PATH FOR USER REQUEST
────────────────────────────────────────────────

REQUEST: "Create a project reader tool"

FORWARD NAVIGATION:
Request
  → P7: BUILD TREE
    ├─ Path A1: Build as song type (framework-aligned) ✓
    ├─ Path C1: Build as standalone utility (framework-violation) ✗
    └─ CHOOSE: A1 (framework-aligned)
       
  → P8: EXECUTE GATE
    ├─ Q1: Song type? YES ✓
    ├─ Q2: Through RENDERER? YES ✓
    ├─ Q3: Sequencer tracked? YES ✓
    ├─ Q4: ARIA translates? YES ✓
    ├─ Q5: In weight? YES ✓
    └─ RESULT: PASS → continue
       
  → P9: UFM VALIDATION
    ├─ choice: "Create project reader song"
    ├─ framework_aligned: {all YES}
    ├─ quality_score: 0.92 (calculation: 0.75 + 0.15 + 0.15 = 1.0 capped)
    └─ is_valid: true → continue
       
  → P10: LOG DECISION
    ├─ timestamp: 2026-04-04T12:34:56
    ├─ decision_id: decision_2026-04-04T12-34-56
    ├─ choice, why, tree, gate_result, ufm_score
    └─ Status: LOGGED → continue
       
  → P6: RENDERER (Generate Song)
    ├─ song_type: "project_reader"
    ├─ parameters: {compression: HUFFMAN, output: MARKDOWN}
    └─ Output: Song object
       
  → P1: SONG OBJECT CREATED
    ├─ Type: project_reader
    ├─ Weight: ~15% (allocated from weight structure)
    └─ Ready for sequencing
       
  → P2: SEQUENCER (Record Operation)
    ├─ election_type: "song_generation"
    ├─ timestamp: 2026-04-04T12:34:57
    ├─ causality: "invoked by UFM-validated decision"
    └─ election recorded
       
  → P3: LEDGER (Permanent Entry)
    ├─ hash: [SHA256 of operation]
    ├─ content: complete operation trace
    ├─ mode: DECISION_EXECUTION
    ├─ source: AI_SYSTEM
    └─ LOCKED IN: Cannot be changed
       
  → P4: ARIA (Output Translation)
    ├─ input: song_object
    ├─ format: Markdown
    ├─ output: "# PROJECT READER\n..."
    └─ User receives result

VERIFICATION (REVERSE NAVIGATION):
"Did this violate framework?"
  → Query P10: Yes, decision logged
  → Verify P9: quality_score = 0.92 > 0.75 ✓
  → Verify P8: All 5 gates passed ✓
  → Verify P7: Path classification = Type A (framework-aligned) ✓
  → Verify origin: Came from UFM-validated decision ✓
  → RESULT: NO VIOLATION, fully coherent


═════════════════════════════════════════════════════════════════

SUMMARY: THE FORMAT OF THE WHOLE
──────────────────────────────────

STRUCTURE: 15 Primitives arranged in 4 layers + 8 Invariants

FLOW: Request → Causal Tree → Gate → UFM Validation → Ledger Log → Execution → Output → Ledger Record

VERIFICATION: Bidirectional navigation (forward plan, reverse verify)

PERSISTENCE: Every step recorded in P3 (Ledger) - complete causal history available forever

GUARANTEE: Invariants never change - foundation is stable across all operations

NAVIGATION: Can traverse from any primitive to any other, always maintaining causal coherence

STATUS: System defined, mapped, invariants locked. Ready for active operation.
```
