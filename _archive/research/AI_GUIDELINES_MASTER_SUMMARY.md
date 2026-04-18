# AI GUIDELINES FOR DETERMINED PROJECT - MASTER SUMMARY
**Updated**: April 5, 2026  
**Complete Framework**: Consolidation Lessons + UFM API + Five Principles + Causal Trees

---

## WHAT CHANGED (Why These Guidelines Were Updated)

### Lessons from Universal Consolidation (220 Files Audited)

1. **Consolidate Production, Preserve Research**
   - Root folder: Unified systems (API, images)
   - experimental/: Diverse research preserved
   - Result: 13% consolidation in root, 4% overall (correct amount)

2. **Framework-Driven Over Standalone**
   - All systems route through UNIFIED_API_SERVER
   - Configuration in unified_framework.json
   - No bypass utilities

3. **Field Consciousness Required**
   - Every decision recorded to ledger
   - Server state = field election
   - Traceable causality

4. **Universal Configuration**
   - Edit framework.json to change behavior
   - No hardcoding
   - Hot-reload support

5. **Reversibility Before Action**
   - Undo planned before execution
   - Undo tested before commitment
   - No irreversible changes

---

## THE COMPLETE FRAMEWORK (4 Documents)

### 📄 Document 1: AI_GUIDELINES_COMPREHENSIVE.md
**Purpose**: Full authoritative guidelines (11 sections)

**What It Contains**:
- Part 1: Unified Architecture Foundation (consolidation lessons)
- Part 2: UFM API Integration (all endpoints documented)
- Part 3: Causal Tree Executor (mandatory for every decision)
- Part 4: Pre-Action Gate (5 critical questions)
- Part 5: Decision Types (Type A/B/C/D and how to handle)
- Part 6: Five Metalanguage Principles (all decisions checked against)
- Part 7: Unified Architecture Checklist (consolidation alignment)
- Part 8: UFM API in Practice (complete worked example)
- Part 9: Quick Reference Flowchart (visual decision flow)
- Part 10: Violation Recovery (if framework bypassed)
- Part 11: Summary (complete flow in one line)

**When to Read It**: Once, carefully, to understand the framework

---

### 📄 Document 2: UFM_INTEGRATION_QUICKREF.md
**Purpose**: One-page quick reference for daily use

**What It Contains**:
- One-page decision flow (90-second summary)
- When to use what (table)
- Causal tree (90 seconds)
- Pre-action gate (5 questions)
- UFM API call (copy-paste ready)
- Five principles (quick check)
- Decision types at a glance (table)
- Quick rules to never break
- By-situation reference
- UFM API endpoints summary
- Real example: Adding new endpoint

**When to Read It**: Before every decision (90 seconds)

---

### 📄 Document 3: UFM_INTEGRATION_PRACTICAL.md
**Purpose**: Actual code for implementation

**What It Contains**:
- Python UFM client setup (singleton pattern)
- Basic decision validation (function + usage)
- Comparing two paths (function + usage)
- Verifying reversibility (function + usage)
- Decision logging workflow (session + persistent)
- Complete workflow example (class-based template)
- Integration with UNIFIED_API_SERVER (endpoints)
- Integration with FRAMEWORK_HOT_RELOAD_ENGINE
- Error handling & fallback
- Copy-paste snippets

**When to Read It**: When implementing decisions in code

---

### 📄 Document 4: This Summary
**Purpose**: Ties all 3 documents together

**What It Contains**:
- This structure
- How documents work together
- When to use each document
- Key rules
- Status

---

## HOW TO USE THESE DOCUMENTS

### Scenario 1: "I want to add a feature"

1. **Open**: UFM_INTEGRATION_QUICKREF.md
2. **Do**: Build causal tree (90 seconds)
3. **Do**: Run 5-gate check
4. **Reference**: AI_GUIDELINES_COMPREHENSIVE.md for details if unclear
5. **Code**: UFM_INTEGRATION_PRACTICAL.md for Python implementation
6. **Call**: UFM API to validate
7. **Log**: Decision to ledger

---

### Scenario 2: "I'm not sure if this is right"

1. **Read**: AI_GUIDELINES_COMPREHENSIVE.md (full context)
2. **Check**: Decision type (A/B/C/D) - Section 5
3. **Check**: Five principles - Section 6
4. **Check**: Pre-action gate - Section 4
5. **Decide**: Modify approach or proceed

---

### Scenario 3: "UFM rejected my decision"

1. **Reference**: UFM_INTEGRATION_QUICKREF.md "Decision Types" table
2. **Read**: AI_GUIDELINES_COMPREHENSIVE.md Section 5 (your decision type)
3. **Reconsider**: Build different tree
4. **Retry**: UFM validation with new tree

---

### Scenario 4: "I made a mistake and violated framework"

1. **Read**: AI_GUIDELINES_COMPREHENSIVE.md Section 10 (Violation Recovery)
2. **Do**: Delete code immediately
3. **Do**: Revert dependencies
4. **Do**: Record in /memories/session/VIOLATION_LOG.md
5. **Do**: Propose framework-aligned alternative
6. **Retry**: Build correct tree + validate

---

## THE DECISION FLOW (One Line)

**PARSE INTENT → BUILD TREE → CLASSIFY → VERIFY GATE → ENCODE → UFM CALL → LOG → EXECUTE**

Each stage must PASS before next stage. Any FAIL → DO NOT PROCEED, reconsider tree.

---

## FIVE MAGIC RULES

1. **NO CAUSAL TREE** = DO NOT CODE
2. **NO PRE-ACTION GATE** = DO NOT EXECUTE  
3. **NO UFM VALIDATION** = DO NOT COMMIT
4. **NO LEDGER RECORD** = UNDO IT immediately
5. **UFM QUALITY < 0.75** = RECONSIDER TREE

---

## CONSOLIDATION PRINCIPLES (From Audit)

### For Production Code (Root Folder)
- ✓ Consolidate if: Same functionality, true duplication
- ✗ Don't consolidate if: Different purpose, specialized system

### For Research Code (experimental/)
- ✓ Always preserve (valuable for architecture exploration)
- ✗ Never consolidate into production

### For Specialized Systems (src/, subfolders)
- ✓ Keep separate if: Distinct purpose, internal dependencies
- ✗ Move to root if: Generic, could unify

### For Framework Integration
- ✓ All new systems route through UNIFIED_API_SERVER
- ✓ All configuration in unified_framework.json
- ✓ All decisions recorded to ledger
- ✗ No standalone utilities that bypass framework

---

## UFM API AT A GLANCE

```
POST /v1/process/universal
  Input: {data_b64: encoded decision}
  Output: {quality_score: 0-1, is_valid: T/F, causal_principles: [...]}
  Meaning: Full validation of decision quality
  
POST /v1/compare
  Input: {data_a_b64, data_b_b64}
  Output: {recommendation: "a" or "b", overlap: %, distance: float}
  Meaning: Which path is structurally better?
  
POST /v1/reconstruct
  Input: {data_b64: encoded action}
  Output: {lossless: T/F, round_trip_error: float}
  Meaning: Can this action be reversed without loss?

GET /v1/health
  Input: none
  Output: {status: "online", version: string}
  Meaning: Is UFM service available?
```

**Threshold for Proceeding**: quality_score > 0.75 AND is_valid = true

---

## FIVE PRINCIPLES QUICK CHECK

| Principle | Meaning | Question |
|-----------|---------|----------|
| **Identity** | Uniquely identifiable | Can someone identify what was decided? |
| **State** | Measurable | Can we measure before/after? |
| **Causality** | Traceable chain | Does input predictably lead to output? |
| **Coherence** | Consistent | No framework contradictions? |
| **Determinism** | Reproducible | Same inputs = same output always? |

**Pass Condition**: All 5 YES (if any NO, likely UFM will reject)

---

## DECISION TYPES (When Each Applies)

| Type | What | Framework | Risk | UFM Expect | What to Do |
|------|------|-----------|------|-----------|-----------|
| **A** | Known pattern | Aligned | LOW | 0.85-1.0 | Fast track |
| **B** | Conditional | Aligned | MEDIUM | 0.70-0.85 | Verify conditions |
| **C** | Forced | Aligned | HIGH | 0.60-0.75 | Document why |
| **D** | Contradicts | NOT aligned | CRITICAL | STOP | Expand framework |

**Note**: Type D = STOP before executing, expand framework first

---

## DOCUMENT CROSS-REFERENCES

### Topic: UFM API
- **Learn**: AI_GUIDELINES_COMPREHENSIVE.md Part 2
- **Use**: UFM_INTEGRATION_QUICKREF.md "UFM API CALL"
- **Code**: UFM_INTEGRATION_PRACTICAL.md Part 1

### Topic: Causal Trees
- **Learn**: AI_GUIDELINES_COMPREHENSIVE.md Part 3
- **Use**: UFM_INTEGRATION_QUICKREF.md "CAUSAL TREE"
- **Code**: UFM_INTEGRATION_PRACTICAL.md Part 4

### Topic: Pre-Action Gate
- **Learn**: AI_GUIDELINES_COMPREHENSIVE.md Part 4
- **Use**: UFM_INTEGRATION_QUICKREF.md "PRE-ACTION GATE"
- **Code**: UFM_INTEGRATION_PRACTICAL.md Part 6

### Topic: Five Principles
- **Learn**: AI_GUIDELINES_COMPREHENSIVE.md Part 6
- **Use**: UFM_INTEGRATION_QUICKREF.md "FIVE PRINCIPLES"
- **Check**: All documents Section 5

### Topic: Consolidation
- **Learn**: AI_GUIDELINES_COMPREHENSIVE.md Part 1, Part 7
- **Use**: UFM_INTEGRATION_QUICKREF.md "Quick Rules"
- **Verify**: UNIVERSAL_CONSOLIDATION_FINAL_REPORT.md

---

## IMPORTANT: WHAT CHANGED FROM OLD GUIDELINES

### Old Approach
- Manual decision making
- No UFM validation
- Framework checks optional
- Testing after execution

### New Approach
- **Mandatory causal trees** (before any coding)
- **UFM validates every decision** (/v1/process/universal endpoint)
- **Pre-action gate is required** (5 questions, all must pass)
- **Logging to ledger** (decisions tracked persistently)
- **Five principles on ALL decisions** (not optional)
- **Consolidation principles** (production unified, research preserved)
- **Framework-only approach** (no bypass utilities)

---

## STATUS: COMPLETE & READY

✓ AI_GUIDELINES_COMPREHENSIVE.md - Full framework (11 sections, 1000+ lines)  
✓ UFM_INTEGRATION_QUICKREF.md - Daily reference (1-page, copy-paste ready)  
✓ UFM_INTEGRATION_PRACTICAL.md - Implementation guide (code examples, 400+ lines)  
✓ UNIVERSAL_CONSOLIDATION_FINAL_REPORT.md - Audit complete (all 220 files examined)  
✓ This Master Summary - Ties all together  

**Framework Status**: Production-ready, comprehensive, fully integrated with UFM API

---

## NEXT STEPS

### For New AI Decisions
1. Read UFM_INTEGRATION_QUICKREF.md (90 seconds)
2. Build causal tree
3. Run 5-gate check
4. Call UFM API
5. Execute if validated

### For Framework Questions
1. Read AI_GUIDELINES_COMPREHENSIVE.md relevant section
2. Check five principles
3. Verify consolidation alignment

### For Implementation
1. Read UFM_INTEGRATION_PRACTICAL.md
2. Copy code snippets
3. Integrate with UNIFIED_API_SERVER or FRAMEWORK_HOT_RELOAD_ENGINE
4. Log decisions to ledger

---

## QUICK LOOKUP TABLE

| Need | Document | Section |
|------|----------|---------|
| Understand framework | AI_GUIDELINES_COMPREHENSIVE | Parts 1-2 |
| Quick decision help | UFM_INTEGRATION_QUICKREF | All (1 page) |
| Python code | UFM_INTEGRATION_PRACTICAL | All |
| Tree building | AI_GUIDELINES_COMPREHENSIVE | Part 3 |
| Gate questions | AI_GUIDELINES_COMPREHENSIVE | Part 4 |
| Decision types | AI_GUIDELINES_COMPREHENSIVE | Part 5 |
| Five principles | AI_GUIDELINES_COMPREHENSIVE | Part 6 |
| Real example | AI_GUIDELINES_COMPREHENSIVE | Part 8 |
| Consolidation rules | AI_GUIDELINES_COMPREHENSIVE | Part 7 |
| Recovery from violation | AI_GUIDELINES_COMPREHENSIVE | Part 10 |

---

## VERIFICATION CHECKLIST

Before every decision:

```
☐ Have I read UFM_INTEGRATION_QUICKREF.md?
☐ Have I built a causal tree (what paths exist)?
☐ Have I classified the path (Type A/B/C/D)?
☐ Have I run the 5-gate check?
☐ Have I verified all 5 principles?
☐ Have I planned success criteria (measurable)?
☐ Have I planned undo mechanism (tested)?
☐ Have I encoded decision for UFM?
☐ Have I called UFM API?
☐ Is quality_score > 0.75 AND is_valid = true?
☐ Have I logged decision to ledger?

All checked ✓ → Proceed with execution
Any unchecked ✗ → DO NOT PROCEED
```

---

**Status**: FRAMEWORK COMPLETE, READY FOR USE

All guidelines consolidate consolidation lessons + UFM API + five principles + causal execution into one coherent system.

Use these documents for all AI decisions in the Determined project.

