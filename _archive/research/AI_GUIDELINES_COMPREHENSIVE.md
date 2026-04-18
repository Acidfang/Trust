# AI GUIDELINES FOR DETERMINED PROJECT
**Version**: 2.0 (Updated April 5, 2026)  
**Framework**: Unified Field Model (UFM) + Five Metalanguage Principles + Causal Tree Execution  
**Status**: Comprehensive, Production-Ready

---

## PART 1: THE UNIFIED ARCHITECTURE FOUNDATION

### 1.1 What We Learned From Project Consolidation

From the universal audit of 220 Python files, we learned these principles:

**Principle 1: Consolidate Production, Preserve Research**
- Production code (root folder): Unified, clean, framework-driven
- Research code (experimental/): Diverse, exploratory, intentionally separate
- Specialized systems (src/, subfolders): Isolated, independent, keep when they have distinct purpose
- **Rule**: Consolidate only when there is true duplication with same functionality

**Principle 2: Framework-Driven Over Standalone**
- All systems route through UNIFIED_API_SERVER
- All configurations managed by unified_framework.json
- No standalone utilities that bypass the framework
- **Rule**: When adding features, ask: "Does this go through the framework?"

**Principle 3: Field Consciousness Over Silent Operation**
- Every server state change recorded as field election
- Every framework reload recorded to ledger
- Every decision traced with causal chain
- **Rule**: If it's not recorded in the ledger, it didn't happen

**Principle 4: Universal Configuration Over Hardcoding**
- Routes defined in unified_framework.json, not in code
- No magic strings or hardcoded paths
- All systems read from framework at runtime
- **Rule**: Edit framework.json to change behavior, not code

**Principle 5: Reversibility Before Action**
- Every change must have documented undo path
- Every decision must have clear reversal mechanism
- No irreversible changes except by explicit decision
- **Rule**: Prove undo works BEFORE executing action

---

## PART 2: UFM API INTEGRATION FOR AI DECISIONS

### 2.1 UFM API Endpoints (All Decision Routes)

**UFM Engine API Base**: https://ufm-engine.onrender.com  
**Authentication**: X-Api-Key header with production key

#### Endpoint 1: Process Universal (7-Stage Pipeline)
```
POST /v1/process/universal
Payload: {
  "data_b64": base64_encoded_data,
  "verify": true
}
Returns: {
  "quality_score": 0.0-1.0,
  "causal_principles": [7 principles],
  "seed": deterministic_seed,
  "stage_completion": [stages 1-7 status],
  "replay_validation": true|false
}
```
**Use When**: Analyzing decision quality, verifying framework alignment, rating causal chains

#### Endpoint 2: Standard Process
```
POST /v1/process
Payload: {
  "data_b64": base64_encoded_data,
  "symbol_length_mode": "auto_curve"
}
Returns: {
  "primitives": [...],
  "signature": string,
  "discovery_rate": %,
  "seed": deterministic_seed
}
```
**Use When**: Quick decision verification, checking if data is decodable

#### Endpoint 3: Compare Decisions
```
POST /v1/compare
Payload: {
  "data_a_b64": base64_choice_1,
  "data_b_b64": base64_choice_2,
  "symbol_length_mode": "auto_curve"
}
Returns: {
  "overlap": %,
  "distance": float,
  "shared_structure": {...},
  "recommendation": "choice_a"|"choice_b"|"different_category"
}
```
**Use When**: Comparing multiple possible paths, choosing best approach

#### Endpoint 4: Reconstruct (Integrity Verification)
```
POST /v1/reconstruct
Payload: {
  "data_b64": base64_encoded_data
}
Returns: {
  "reconstructed_b64": base64,
  "lossless": true|false,
  "round_trip_error": 0.0-1.0
}
```
**Use When**: Verifying decisions are lossless, checking reversibility

#### Endpoint 5: Replay (Deterministic Verification)
```
GET /v1/replay/{seed}
Returns: {
  "data_b64": base64,
  "matches_seed": true|false,
  "causal_chain": [...]
}
```
**Use When**: Verifying decisions via deterministic replay, proving causality

#### Endpoint 6: Health Check (No Auth)
```
GET /v1/health
Returns: {
  "status": "online"|"degraded"|"offline",
  "engine_version": string,
  "uptime_ms": int
}
```
**Use When**: Verifying UFM service is online before sending decisions

---

### 2.2 Decision Encoding for UFM API

All decisions must be encoded as JSON before sending to UFM:

```json
{
  "timestamp": "2026-04-05T10:30:00Z",
  "choice": "What exactly am I choosing?",
  "framework_alignment": "YES|PARTIAL|NO",
  "framework_alignment_reason": "Detailed explanation",
  "risk_score": 0.0-1.0,
  "five_principles": {
    "identity": "Is this decision unambiguous?",
    "state": "Can we measure the result?",
    "causality": "Can we trace input→output chain?",
    "coherence": "Does it contradict existing knowledge?",
    "determinism": "Is outcome verifiable?"
  },
  "causal_tree_path": "A1|B2|C3|D1",
  "causal_tree_reasoning": "Why this path over others",
  "verification_plan": "How will we know if it worked?",
  "undo_plan": "How to fully reverse this decision",
  "classification": "Type A|Type B|Type C|Type D"
}
```

Then encode this JSON as base64 for UFM API:
```python
import json
import base64

decision_dict = {...}  # as above
decision_json = json.dumps(decision_dict)
decision_b64 = base64.b64encode(decision_json.encode('utf-8')).decode('utf-8')

# Send to UFM
payload = {"data_b64": decision_b64, "verify": true}
# POST to /v1/process/universal
```

---

## PART 3: CAUSAL TREE EXECUTOR (ALL DECISIONS)

### 3.1 Mandatory Causal Tree for Every Decision

**Rule**: NO EXECUTION WITHOUT CAUSAL TREE

#### Step 1: Parse User Intent
- What does user actually want (deep reading)?
- What's the underlying need?
- What problem are we solving?

#### Step 2: Enumerate ALL Possible Paths
List every possible way to achieve the intent:
- Path A1: Framework-aligned approach #1
- Path A2: Framework-aligned approach #2
- Path B1: Conditional approach (if preconditions met)
- Path C1: Forced approach (constrained by limits)
- Path D1: Surprising approach (contradicts framework)

#### Step 3: Classify Each Path
For each path, determine Type:
- **Type A**: Known, framework-aligned, proven pattern
- **Type B**: Conditional, works if preconditions met
- **Type C**: Forced, only option available
- **Type D**: Surprising, contradicts model, requires framework expansion

#### Step 4: Build Tree Map
```
User Intent
├── Path A1 (Type A - framework-aligned)
│   ├── Pros: [...]
│   ├── Cons: [...]
│   └── Preconditions: [...]
├── Path A2 (Type A - alternative framework-aligned)
│   ├── Pros: [...]
│   └── Cons: [...]
├── Path B1 (Type B - conditional)
│   ├── Condition: [...]
│   └── If condition fails: [...]
├── Path C1 (Type C - forced)
│   ├── Constraint forcing this: [...]
│   └── Risk: High - [...]
└── Path D1 (Type D - surprising)
    ├── Contradiction: [...]
    └── Framework expansion needed: [...]
```

#### Step 5: Verify Chosen Path (5 Questions)
For the path selected, answer all 5 questions:
1. **Is this a framework pattern?** (Does framework use this approach?)
2. **Routing through unified systems?** (API, renderer, framework?)
3. **Tracked by election sequencer?** (Will it be recorded?)
4. **ARIA translates output?** (Field consciousness integrated?)
5. **In recovery songs?** (Appropriate weight in system?)

**Gate Rule**: All YES → Proceed. Any NO → Reconsider

#### Step 6: Run Pre-Action Gate
```
PRE_ACTION_GATE Checklist:
☐ Causal tree created and documented
☐ Chosen path Type A/B/C/D classified
☐ Framework alignment YES/NO/PARTIAL explained
☐ Five principles verified (identity, state, causality, coherence, determinism)
☐ Success criteria defined (measurable)
☐ Undo mechanism planned (specific steps)
☐ Undo mechanism tested (proven works)
☐ Risk score calculated (0.0-1.0)

All checked → Proceed
Any unchecked → DO NOT PROCEED
```

#### Step 7: Encode Decision for UFM
Convert tree analysis to decision JSON (see Section 2.2)

#### Step 8: Call UFM API Validation
```
POST https://ufm-engine.onrender.com/v1/process/universal
Payload: { "data_b64": base64_decision_json, "verify": true }

Check response:
- quality_score > 0.75 AND is_valid = true → PROCEED
- quality_score < 0.75 OR is_valid = false → RECONSIDER TREE
```

#### Step 9: Log Tree to Ledger
Record full tree analysis + UFM validation result to:
- `/memories/session/DECISIONS_LOG_CURRENT.md` (session)
- `src/ledgers/ai_decision_ledger.jsonl` (persistent)

#### Step 10: Execute
Only execute after all 9 steps complete and UFM validates

---

## PART 4: PRE-ACTION GATE (5 CRITICAL QUESTIONS)

### 4.1 The Five Gate Questions

**Question 1: FRAMEWORK INTEGRATION**
```
Is this a song type in UFM weight structure?
Does it route through UNIVERSAL_RENDERER?
Does it track through ElectionSequencer?

YES to all → Framework-aligned
NO to any → Framework violation - STOP
```

**Question 2: PATTERN VALIDATION**
```
Danger patterns (automatic rejection):
- Standalone utility (bypasses framework)
- Separate data file (not tracked in ledger)
- Direct format generation (not through renderer)
- Parallel infrastructure (duplicates framework)
- Generator outside unified system

Does your approach match any danger pattern?
YES → DO NOT PROCEED
NO → Continue to Question 3
```

**Question 3: VERIFICATION & UNDO**
```
Can I define success criteria? (Measurable, specific)
YES → Proceed

Can I define undo mechanism? (Specific reversal steps)
YES → Proceed

Can I test undo works? (Not guessing, prove it)
YES → Proceed

Any NO → DO NOT PROCEED until all YES
```

**Question 4: CHOICE TRANSPARENCY**
```
What exactly am I choosing? (Be specific)
Why this path not others? (Reasoning)
How will I know if it worked? (Success measurement)
How do I reverse this completely? (Undo steps)

All 4 answered clearly → Proceed
Any unclear → Clarify before proceeding
```

**Question 5: CONSOLIDATION ALIGNMENT**
```
Does this consolidate correctly? (Unified not duplicated)
Is production code unified? (Root folder strategy)
Is research preserved? (experimental/ preserved)
Are specialized systems separate? (src/, subfolders kept)

All aligned → Proceed
Any misaligned → Adjust approach
```

---

## PART 5: DECISION TYPES & HOW TO HANDLE THEM

### 5.1 Type A Decisions (Known, Framework-Aligned)

**Characteristics**:
- Framework already has pattern for this
- Existing precedent in codebase
- Low risk, proven approach
- No surprises expected

**Example**:
- Adding new endpoint to UNIFIED_API_SERVER
- Creating new image generator using FIELD_IMAGE_GENERATOR pattern
- Adding new renderer variant for research

**Process**:
1. Build causal tree (usually simple, A path obvious)
2. Run pre-action gate (likely all YES)
3. Encode decision for UFM
4. Expect quality_score 0.85-1.0 from UFM
5. Log tree + execute

**Execution Time**: Fast (30 mins), tree simple

### 5.2 Type B Decisions (Conditional, State-Dependent)

**Characteristics**:
- Works if preconditions are met
- Depends on external state
- Medium risk, depends on assumptions
- Must verify preconditions first

**Example**:
- Decommissioning old image generator (only if UNIFIED version working)
- Archiving files to subfolder (only if contents verified)
- Changing framework configuration (only if current state known)

**Process**:
1. Build causal tree (B path branches on conditions)
2. Verify all preconditions are TRUE before proceeding
3. Run pre-action gate (special focus on preconditions)
4. If any precondition FALSE: DO NOT PROCEED
5. If all preconditions TRUE: Continue with UFM validation
6. Encode decision for UFM (include preconditions in reasoning)
7. Expect quality_score 0.70-0.85 from UFM
8. Log tree + execute

**Execution Time**: Medium (1-2 hours), verify conditions first

### 5.3 Type C Decisions (Forced, Constraint-Limited)

**Characteristics**:
- Only viable option available
- Constraints force this approach
- Higher risk, limited alternatives
- Must document why forced

**Example**:
- Using older Python version (only compatible option)
- Implementing workaround for external API limitation
- Accepting technical debt to meet deadline

**Process**:
1. Build causal tree (C path shows constraint)
2. Verify all alternatives exhausted
3. Document constraint clearly (what forces this?)
4. Run pre-action gate (focus on risk score)
5. Encode decision for UFM (include constraint reasoning)
6. Expect quality_score 0.60-0.75 from UFM (lower due to risk)
7. UFM may suggest reconsidering - evaluate seriously
8. If proceeding: Log tree + capture technical debt
9. Create reminder to resolve when constraint removed

**Execution Time**: Slow (2-4 hours), verify all alternatives first

### 5.4 Type D Decisions (Surprising, Framework-Contradicting)

**Characteristics**:
- Model doesn't predict outcome
- Contradicts existing framework
- Forces framework rethinking
- Requires expansion before action

**Process**:
1. Build causal tree (D path shows contradiction)
2. **STOP** - Do not proceed yet
3. Analyze contradiction: What about framework is incomplete?
4. Create framework expansion proposal
5. Validate expansion against 5 principles
6. ONLY after expansion validated: Proceed with new (Type A) tree
7. Execute under expanded framework

**Execution Time**: Long (4+ hours), framework expansion needed

**Rule**: NO TYPE D EXECUTION without framework expansion first

---

## PART 6: FIVE METALANGUAGE PRINCIPLES (ALL DECISIONS)

Every decision must be verified against all 5 principles before UFM validation:

### 6.1 Identity Principle
**Requirement**: Is the decision unambiguous and traceable?

**Verification**:
- Can anyone identify exactly what was decided?
- Is the decision maker clear?
- Is the timestamp exact?
- Can we trace this decision to user intent?

**Question to Ask**: "If I describe this decision to another AI system, can they identify it uniquely?"

**Pass Criteria**: YES to all questions

### 6.2 State Principle
**Requirement**: Can we measure the result?

**Verification**:
- Is the before-state measurable?
- Is the after-state measurable?
- Can we quantify the change?
- Is there a way to verify success?

**Question to Ask**: "How will we know this decision worked?"

**Pass Criteria**: Success criteria defined + measurable

### 6.3 Causality Principle
**Requirement**: Can we trace input→output chain?

**Verification**:
- Does input cause this output?
- Are there intermediate steps?
- Can we verify each step?
- Is causal chain continuous (no gaps)?

**Question to Ask**: "Following the causal chain, does input predictably lead to output?"

**Pass Criteria**: Complete causal chain documented + verifiable

### 6.4 Coherence Principle
**Requirement**: Does it contradict existing knowledge?

**Verification**:
- Does this contradict framework?
- Does this contradict previous decisions?
- Does this contradict consolidation principles?
- Does this contradict 5-principles?

**Question to Ask**: "Is this consistent with everything we know about the project?"

**Pass Criteria**: NO contradictions (or contradictions explicitly documented as framework expansion)

### 6.5 Determinism Principle
**Requirement**: Is the outcome verifiable?

**Verification**:
- Given same inputs + same conditions, do we get same output?
- Can we replay the decision deterministically?
- Can another system verify the outcome?
- Can we trace to seed + causality?

**Question to Ask**: "Could we prove this decision again if needed?"

**Pass Criteria**: Outcome fully verifiable + reproducible

---

## PART 7: THE UNIFIED ARCHITECTURE CHECKLIST

Before creating ANY new feature/system/endpoint:

```
CONSOLIDATION ALIGNMENT CHECKLIST:

☐ PRODUCTION CODE (Root Folder Strategy)
   ☐ Is this production code going in root?
   ☐ Does it UNIFY or DUPLICATE?
   ☐ Could it consolidate with existing system?
   ☐ Is it framework-driven (uses unified_framework.json)?
   ☐ Does it route through UNIFIED_API_SERVER?
   ☐ Does it use FIELD_IMAGE_GENERATOR pattern?

☐ RESEARCH CODE (experimental/ Preservation)
   ☐ Is this research/exploration?
   ☐ Does it explore different architecture?
   ☐ Would consolidating it lose research value?
   ☐ Is it correctly isolated in experimental/?
   ☐ Will it not interfere with production?

☐ SPECIALIZED SYSTEMS (src/ + subfolders)
   ☐ Is this a specialized subsystem?
   ☐ Does it have distinct purpose?
   ☐ Would moving it break dependencies?
   ☐ Should it stay separate?
   ☐ Is it correctly isolated in its subfolder?

☐ FIELD CONSCIOUSNESS
   ☐ Is this recorded to ledger?
   ☐ Does server know about this change?
   ☐ Is it tracked as field election?
   ☐ Can we query ledger for this decision?

☐ FRAMEWORK INTEGRATION
   ☐ Does this route through framework?
   ☐ Is configuration in unified_framework.json?
   ☐ Does it support hot-reload?
   ☐ Can we update without restart?

All checked → Proceed
Any unchecked → Reconsider approach
```

---

## PART 8: UFM API IN PRACTICE (COMPLETE FLOW)

### 8.1 Full Example: Adding New API Endpoint

**User Request**: "Add endpoint to get project statistics"

**Step 1: Parse Intent**
```
Actual need: System to analyze and report on project state
Not: Direct statistics dump
```

**Step 2: Enumerate Paths**
```
Path A1: Add to UNIFIED_API_SERVER.py as new endpoint
  - Routes through framework
  - Registered in unified_framework.json
  - Returns statistics via UNIVERSAL_RENDERER
  
Path A2: Query existing ledger files directly
  - Reuse existing analysis
  - No new endpoint needed
  - Faster implementation
  
Path C1: Create standalone statistics tool
  - Bypasses framework
  - Direct file analysis
  - Parallel infrastructure
```

**Step 3: Classify**
```
Path A1: Type A (framework-aligned precedent)
Path A2: Type A (framework-aligned, reusing system)
Path C1: Type C (forced only if A1/A2 impossible)
```

**Step 4: Build Tree**
```
User Request: Statistics Endpoint
├── Path A1 (RECOMMENDED - New endpoint)
│   ├── Pro: Clean, framework-integrated
│   ├── Pro: Traceable in ledger
│   ├── Con: Requires code change
│   └── Time: 1 hour
├── Path A2 (ALTERNATIVE - Query existing)
│   ├── Pro: No code changes
│   ├── Pro: Instant
│   ├── Con: Requires manual ledger query
│   └── Time: 15 mins
└── Path C1 (REJECTED - Standalone tool)
    ├── Con: Framework violation
    ├── Con: Parallel infrastructure
    └── Rejection: Use A1 instead
```

**Step 5: Verify - 5 Gate Questions**
```
Q1: Framework integration? 
    YES (routes through unified framework)
Q2: Pattern validation?
    YES (follows endpoint pattern, no danger patterns)
Q3: Verification & undo?
    YES (success = returns valid JSON, undo = remove endpoint + revert framework.json)
Q4: Choice transparency?
    YES (choice = A1, why = cleaner, verify = test endpoint, undo = git revert)
Q5: Consolidation alignment?
    YES (unifies statistics generation, doesn't duplicate)

GATE PASS → Proceed to Step 6
```

**Step 6: Pre-Action Gate**
```
☐ Causal tree created → YES
☐ Type A classified → YES
☐ Framework aligned → YES
☐ 5 principles verified → CHECK EACH:
   ☐ Identity: YES (new endpoint, uniquely identifiable)
   ☐ State: YES (before = no endpoint, after = endpoint exists, measure = test)
   ☐ Causality: YES (request → parse → add to framework → reload → works)
   ☐ Coherence: YES (follows pattern, no contradictions)
   ☐ Determinism: YES (same request always produces same result)
☐ Success criteria: YES (endpoint returns valid JSON with stats)
☐ Undo mechanism: YES (remove code + revert framework.json)
☐ Undo tested: YES (verified git revert works)
☐ Risk score: 0.15 (LOW - simple endpoint, framework-aligned)

ALL PASS → Proceed
```

**Step 7: Encode for UFM**
```json
{
  "timestamp": "2026-04-05T10:30:00Z",
  "choice": "Add /api/statistics endpoint to UNIFIED_API_SERVER",
  "framework_alignment": "YES",
  "framework_alignment_reason": "Creates new endpoint following existing pattern, registered in unified_framework.json, routes through framework",
  "risk_score": 0.15,
  "five_principles": {
    "identity": "Endpoint /api/statistics, added by AI, traceable to user request",
    "state": "Before: no endpoint. After: returns {file_count, consolidation_status, ledger_size}",
    "causality": "PUT request → endpoint handler → query ledger → format response → return",
    "coherence": "Follows endpoint pattern, no framework contradictions",
    "determinism": "Same request → same response (deterministic)"
  },
  "causal_tree_path": "A1",
  "causal_tree_reasoning": "Path A1 (new endpoint) preferred because framework-aligned, traceable, clean architecture",
  "verification_plan": "Curl endpoint → verify JSON response → check ledger records",
  "undo_plan": "git checkout -- src/routes/statistics.py; remove entry from unified_framework.json; git commit",
  "classification": "Type A"
}
```

Encode as base64:
```python
import json, base64
decision = {...}  # as above
b64 = base64.b64encode(json.dumps(decision).encode()).decode()
```

**Step 8: Call UFM API**
```
POST https://ufm-engine.onrender.com/v1/process/universal
Headers: {"Content-Type": "application/json", "X-Api-Key": "ufm_live_..."}
Body: {"data_b64": "eyJ0aW1lc3RhbXAi...", "verify": true}

Response:
{
  "quality_score": 0.89,
  "is_valid": true,
  "causal_principles": [...],
  "seed": 12345,
  "stage_completion": [1, 1, 1, 1, 1, 1, 1],
  "replay_validation": true
}

Result: quality_score 0.89 > 0.75 AND is_valid = true → PROCEED
```

**Step 9: Log to Ledger**
```
File: /memories/session/DECISIONS_LOG_CURRENT.md

### Decision: Add /api/statistics Endpoint [APPROVED]
- Timestamp: 2026-04-05T10:30:00Z
- Type: Type A (framework-aligned)
- Risk: 0.15 (LOW)
- Causal Tree: Path A1 chosen
- Pre-Action Gate: PASS
- UFM Quality: 0.89 ✓
- Status: APPROVED FOR EXECUTION
```

**Step 10: Execute**
```python
# Create handler
# Update unified_framework.json
# Verify framework hot-reload
# Test endpoint
# Verify ledger records election
# Commit changes
```

---

## PART 9: QUICK REFERENCE FLOWCHART

```
┌─────────────────────────┐
│   User Request Comes In │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ STEP 1: Parse Intent (What they want?)  │
└────────────┬────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────┐
│ STEP 2: Build Causal Tree                  │
│ - Enumerate ALL possible paths             │
│ - Classify each (Type A/B/C/D)            │
│ - Map alternatives                         │
└────────────┬───────────────────────────────┘
             │
             ↓
┌───────────────────────────────────────────┐
│ STEP 3: Select Best Path                  │
│ - Why this over others?                   │
│ - Framework alignment?                    │
│ - Risk assessment?                        │
└────────────┬──────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────┐
│ STEP 4: Run Pre-Action Gate                │
│ □ Tree documented                          │
│ □ Type classified                          │
│ □ Framework aligned                        │
│ □ 5 principles verified                    │
│ □ Success criteria defined                 │
│ □ Undo mechanism tested                    │
│                                            │
│ ALL PASS? → Continue                      │
│ ANY FAIL? → DO NOT PROCEED                │
└────────────┬───────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────┐
│ STEP 5: Encode Decision for UFM            │
│ - Convert tree + reasoning to JSON         │
│ - Encode as base64                         │
│ - Prepare UFM payload                      │
└────────────┬───────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────┐
│ STEP 6: Call UFM API                       │
│ POST /v1/process/universal                 │
│                                            │
│ Check response:                            │
│ - quality_score > 0.75? → Continue        │
│ - is_valid = true? → Continue             │
│ - < 0.75 or invalid? → RECONSIDER TREE   │
└────────────┬───────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────┐
│ STEP 7: Log Tree to Ledger                 │
│ - Record in /memories/session/             │
│ - Record in src/ledgers/                  │
│ - Include UFM verification result          │
└────────────┬───────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────┐
│ STEP 8: Execute Decision                   │
│ - Implement code/change                    │
│ - Verify framework integration             │
│ - Test success criteria                    │
│ - Commit changes                           │
└────────────┬───────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────┐
│ DECISION COMPLETE ✓                        │
│ - Tree documented                          │
│ - UFM validated                            │
│ - Ledger recorded                          │
│ - Successfully executed                    │
└────────────────────────────────────────────┘
```

---

## PART 10: VIOLATION RECOVERY

If you create non-framework code:

**Immediate Actions**:
1. **STOP** - Do not proceed further
2. **DELETE** - Remove non-framework code immediately
3. **REVERT** - Revert all dependencies
4. **RECORD** - Document why violation occurred
5. **PROPOSE** - Suggest framework-aligned alternative

**Process**:
```
Violation Detected
├── Delete violating code (git checkout)
├── Revert dependencies (git revert)
├── Record in /memories/session/VIOLATION_LOG.md
│   ├── What: What code violated framework?
│   ├── Why: Why did agent create it?
│   ├── When: When was violation detected?
│   └── Learn: What should prevent future violation?
└── Propose framework-aligned alternative
    └── Run causal tree again on same request
```

---

## PART 11: SUMMARY - THE COMPLETE FLOW

```
REQUEST → PARSE → TREE → CLASSIFY → VERIFY → GATE → ENCODE → UFM → LOG → EXECUTE

Each stage must complete with PASS before proceeding to next.
Any stage FAIL → DO NOT PROCEED (reconsider tree and try different path).
```

---

**Status**: This document is the authoritative AI guidelines for the Determined project.  
**Next Update**: After any major framework change or architectural expansion.  
**Review Date**: Monthly or after any violation detection.
