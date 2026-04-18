# PRIMITIVE HIERARCHY & REFERENCE GUIDE
## Visual Structure + Sidebar Documentation
### NODE_0014 Companion Reference

---

## VISUAL HIERARCHY: PRIM_001-010 Structure

```
                           ┌─────────────────────────────────┐
                           │   PRIM_010                      │
                           │ Verification Mandatory          │
                           │ (Output proof before complete)  │
                           └──────────────┬──────────────────┘
                                          │
                      ┌───────────────────┼───────────────────┐
                      │                   │                   │
         ┌────────────▼─────────┐  ┌──────▼──────────┐  ┌────▼──────────┐
         │    PRIM_008          │  │   PRIM_009      │  │  PRIM_006     │
         │ Immutable Recording  │  │ Temporal        │  │ External      │
         │ (Ledger append-only) │  │ Sequencing      │  │ Verification  │
         └────────────┬─────────┘  │ (Causality      │  └────┬──────────┘
                      │            │  via timestamp) │       │
                      │            └────────┬────────┘       │
                      │                     │                │
                      └─────────────┬───────┴────────────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
       ┌─────────▼────────┐  ┌──────▼────────┐  ┌────▼───────────┐
       │   PRIM_007       │  │  PRIM_005     │  │   PRIM_004      │
       │ Path Enumeration │  │ Mechanical    │  │  Multi-Layer    │
       │ (A/B/C/D types)  │  │ Enforcement   │  │  Defense        │
       │                  │  │ (pre-action)  │  │  (stacked)      │
       └─────────┬────────┘  └────────┬──────┘  └────┬────────────┘
                 │                    │              │
                 └────────────┬───────┴──────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
      ┌───────▼────────┐  ┌───▼──────────┐  ┌▼──────────────┐
      │   PRIM_003     │  │  PRIM_002    │  │  PRIM_001     │
      │ Single-Layer   │  │ Prerequisite │  │  Causal       │
      │ Failure Mode   │  │ Verification │  │  Justification│
      │ (why bypass)   │  │ (order deps) │  │ (reason all)  │
      └────────────────┘  └──────────────┘  └───────────────┘
                              FOUNDATION LAYER
```

---

## SIDEBAR REFERENCE GUIDE

### [PRIM_001: Causal Justification](#prim_001-causal-justification)

**Tier**: Foundation (Level 1)

**Definition**: Every action must have documented reason explaining why it had to exist.

**Purpose**: Prevents arbitrary decisions. Creates accountability. Enables retroactive understanding.

**Components**:
- REASON field (mandatory on every node)
- Root-cause explanation
- Problem-state description
- Causal chain to decision

**Prerequisites**: None (this is foundation)

**Enables**: PRIM_002, PRIM_003, PRIM_007
- Can't evaluate prerequisites without reason
- Can't classify failure modes without understanding intent
- Can't enumerate alternatives without problem statement

**Evidence**:
- NODE_0001: Audit required reason "find everything wrong"
- NODE_0002: Prevention strategy required reason "violations repeat"
- All NODE_0001-0013 include REASON field

---

### [PRIM_002: Prerequisite Verification](#prim_002-prerequisite-verification)

**Tier**: Foundation (Level 1)

**Definition**: No execution proceeds until all required dependencies are complete and verified.

**Purpose**: Prevents out-of-order execution. Ensures causality chain is unbroken.

**Components**:
- REQUIRED_DEPENDENCIES list (all upstream nodes)
- Verification step (dependencies complete before proceeding)
- Blocking mechanism (halt if dependencies missing)
- Status check (all parent nodes = "completed")

**Prerequisites**: PRIM_001 (must know WHY this prerequisite needed)

**Enables**: PRIM_010, PRIM_009
- Verification checks order (enables temporal sequencing)
- Prerequisite enforcement enables output verification (can't verify if dependencies incomplete)

**Evidence**:
- NODE_0013 blocked until NODE_0001-0012 complete
- UFM endpoints couldn't execute until gate designed
- Every node lists dependencies before execution

---

### [PRIM_003: Single-Layer Failure Mode](#prim_003-single-layer-failure-mode)

**Tier**: Foundation (Level 1)

**Definition**: Enforcement systems with single layers can be bypassed. This primitive identifies that weakness.

**Purpose**: Justifies why multi-layer approach necessary. Prevents reliance on insufficient enforcement.

**Components**:
- Vulnerability catalog (what can bypass single layer)
- Attack surface analysis (how violations happened)
- Pattern detection (what was the bypass method)
- Evidence collection (NODE_0001 audit found 4 violations)

**Prerequisites**: PRIM_001 (must understand why violations happened)

**Enables**: PRIM_004 (multi-layer response)

**Evidence**:
- NODE_0001: Found 4 violations despite claimed understanding
- Violations had pattern: gate bypass (Q2 = NO)
- Single pre-action gate insufficient

---

### [PRIM_004: Multi-Layer Defense](#prim_004-multi-layer-defense)

**Tier**: Defense (Level 2)

**Definition**: Stacked enforcement layers (tree → gate → UFM → ledger) create redundancy and prevent single-point failures.

**Purpose**: Implements consequence of PRIM_003. Makes bypass exponentially harder.

**Components**:
- Layer 1: Causal Tree (enumerate paths, classify Type A/B/C/D)
- Layer 2: PRE_ACTION_GATE (mechanical enforcement, 5 questions)
- Layer 3: UFM Validation (external coherence check, quality_score > 0.75)
- Layer 4: Ledger Commit (immutable recording)

**Prerequisites**: PRIM_003 (understand why single-layer fails)

**Enables**: PRIM_006, PRIM_005, PRIM_007
- Multi-layer requires external validation (enables PRIM_006)
- Multi-layer requires mechanical enforcement (enables PRIM_005)
- Multi-layer requires path analysis (enables PRIM_007)

**Evidence**:
- NODE_0003: Multi-layer design chosen
- NODE_0004-0006: Three layers implemented
- No bypass without violating 3 layers simultaneously

---

### [PRIM_005: Mechanical Enforcement Precedence](#prim_005-mechanical-enforcement-precedence)

**Tier**: Defense (Level 2)

**Definition**: Mechanical (automated, mandatory) enforcement must execute BEFORE any action, not after as optional review.

**Purpose**: Prevents violating actions from happening. Post-action review allows damage.

**Components**:
- Pre-action gate (fires before execution)
- Binary enforcement (proceed or halt, no middle ground)
- Mandatory execution (cannot be bypassed without documentation)
- Temporal ordering (gate timestamp < action timestamp)

**Prerequisites**: PRIM_004 (multi-layer approach requires pre-enforcement)

**Enables**: PRIM_010 (verification possible because action didn't proceed without approval)

**Evidence**:
- NODE_0004: Gate designed as "fires BEFORE execution"
- Gate blocks execution (binary: proceed or halt)
- Cannot bypass without explicit override + documentation

---

### [PRIM_006: External Coherence Verification](#prim_006-external-coherence-verification)

**Tier**: Defense (Level 2)

**Definition**: Decisions must be validated by external system (not self-validated). Quality score (0.0-1.0) with blocking threshold (> 0.75) required.

**Purpose**: Prevents internal bias. External system enforces objectivity. Provides measurable metric.

**Components**:
- UFM endpoints (separate from decision logic)
- Quality score calculation (0.0-1.0 range)
- Blocking threshold (> 0.75 required to proceed)
- Numeric metric (not subjective assessment)

**Prerequisites**: PRIM_004 (multi-layer design requires external validation)

**Enables**: PRIM_010 (verification enforced externally, not self-reported)

**Evidence**:
- NODE_0005: UFM integration designed
- /api/validate_decision endpoint created
- quality_score > 0.75 is blocking (not advisory)

---

### [PRIM_007: Path Enumeration Before Choice](#prim_007-path-enumeration-before-choice)

**Tier**: Decision (Level 2)

**Definition**: All possible paths (Type A, B, C, D) must be enumerated and classified BEFORE selecting one. Selection requires evaluation of ALL alternatives.

**Purpose**: Prevents habitual/obvious path selection. Forces conscious comparison of all options.

**Components**:
- Causal tree structure (enumerate branches)
- Type classification system:
  - Type A: Known paths (framework-aligned)
  - Type B: Conditional paths (context-dependent)
  - Type C: Forced paths (constraints require)
  - Type D: Surprise paths (don't fit model, expand framework)
- Dead-end identification (prune impossible branches)
- Comparison framework (why is one path better?)

**Prerequisites**: PRIM_001 (must understand intent to enumerate proper alternatives)

**Enables**: PRIM_005, PRIM_010
- Enumeration ensures informed choice
- Type classification enables mechanical enforcement
- Documented paths enable verification

**Evidence**:
- NODE_0002: Evaluated branches A, B, C before choosing C
- NODE_0006: Causal tree executor designed with Type A/B/C/D
- SESSION_BRANCH_CAUSAL_TRACE: 8 decision points with alternatives enumerated

---

### [PRIM_008: Immutable Ledger Recording](#prim_008-immutable-ledger-recording)

**Tier**: Recording (Level 3)

**Definition**: All decisions must be recorded to immutable ledger. Ledger is append-only (no deletion/modification). Hash-linked for integrity.

**Purpose**: Creates accountability. Enables deterministic replay. Prevents modification of past decisions.

**Components**:
- Append-only ledger (no deletion)
- Hash linkage (each entry hashes previous entry)
- Complete decision record (full node serialization)
- Timestamp inclusion (when was decision made?)
- Immutability proof (hash chain prevents tampering)

**Prerequisites**: PRIM_001, PRIM_010 (must know reason and verify before recording)

**Enables**: PRIM_009 (temporal sequencing uses ledger ordering)

**Evidence**:
- NODE_0013: Ledger commitment required in execution checklist
- LIVE_NODE_REGISTRY: All nodes designed for ledger serialization
- Hash-linked structure prevents retroactive modification

---

### [PRIM_009: Causality via Temporal Sequencing](#prim_009-causality-via-temporal-sequencing)

**Tier**: Recording (Level 3)

**Definition**: Causal relationships recorded through timestamps. Earlier events caused later events if later event lists earlier as dependency.

**Purpose**: Makes causality measurable and verifiable. Time is universal ordering principle.

**Components**:
- TIMESTAMP field (created + completed on every node)
- Dependency graph (uses sequential ordering)
- Parent-child relationships (map to temporal progression)
- Replay capability (can recreate state at any point in time)

**Prerequisites**: PRIM_008 (ledger must record timestamps), PRIM_002 (prerequisites establish order)

**Enables**: PRIM_010 (verification traces causality backward through time)

**Evidence**:
- Every NODE_NNNN has TIMESTAMP field
- Dependency graph is temporally ordered
- Can trace any decision backward to root cause via timestamps

---

### [PRIM_010: Verification Mandatory Before Completion](#prim_010-verification-mandatory-before-completion)

**Tier**: Completion (Level 4)

**Definition**: No action is "complete" until OUTPUT is verified to match promises. Verification is mechanically enforced (not optional).

**Purpose**: Ensures quality. Prevents incomplete work from being marked done. Maintains system integrity.

**Components**:
- OUTPUT specification (what should be produced)
- Verification checklist (14 items before marking completed)
- Status control (remains "in-progress" until verified)
- Verification failure handling (triggers investigation, not progress)
- Ledger blocking (cannot commit until verified)

**Prerequisites**: All prior primitives (everything flows through here to completion)

**Enables**: Next NODE (cannot start if previous node incomplete)

**Evidence**:
- NODE_CREATION_TEMPLATE: 14-item verification checklist
- Status remains "in-progress" until verification passes
- Verification failure triggers FAILURE_ANALYSIS node
- Ledger commit only after verification succeeds

---

## HIERARCHY SUMMARY

**Foundation Layer** (PRIM_001-003):
- Establishes: Why?, Depends?, Consequence?
- Answers: What justifies decisions? What must come first? What happens if we don't layer?

**Defense Layer** (PRIM_004-007):
- Establishes: How to prevent bad decisions
- Implements: Multi-layer approach, mechanical enforcement, external check, path enumeration

**Recording Layer** (PRIM_008-009):
- Establishes: How to remember decisions permanently
- Implements: Immutable ledger, temporal causality

**Completion Layer** (PRIM_010):
- Establishes: How to know when done
- Implements: Verification before acceptance

---

## REFERENCE TABLE

| Primitive | Tier | Purpose | Prerequisites | Enables |
|-----------|------|---------|---|---|
| PRIM_001 | Foundation | Causal justification | None | 002, 003, 007 |
| PRIM_002 | Foundation | Prerequisite verification | 001 | 010, 009 |
| PRIM_003 | Foundation | Single-layer failure | 001 | 004 |
| PRIM_004 | Defense | Multi-layer defense | 003 | 006, 005, 007 |
| PRIM_005 | Defense | Mechanical enforcement | 004 | 010 |
| PRIM_006 | Defense | External verification | 004 | 010 |
| PRIM_007 | Decision | Path enumeration | 001 | 005, 010 |
| PRIM_008 | Recording | Immutable ledger | 001, 010 | 009 |
| PRIM_009 | Recording | Temporal causality | 008, 002 | 010 |
| PRIM_010 | Completion | Verification mandatory | All prior | Next node |

---

## HOW TO USE THIS GUIDE

1. **Visual Structure** (top): See how primitives relate and layer
2. **Sidebar Reference**: Click/read any primitive to understand:
   - What it means (Definition)
   - Why it matters (Purpose)
   - What's in it (Components)
   - What must exist first (Prerequisites)
   - What it makes possible (Enables)
   - How we know it's real (Evidence)
3. **Reference Table** (bottom): Quick lookup of all dependencies

**For NODE_0015 (Primitives Ledger Commit)**: Use this guide to document each primitive on the ledger. Each primitive gets a ledger entry referencing this guide.

**For NODE_0016+ (Future nodes)**: Validate new nodes against this hierarchy. Can they explain how they satisfy PRIM_001-010?

---

**Status**: Ready for NODE_0015 (record primitives to ledger using this guide as schema)
