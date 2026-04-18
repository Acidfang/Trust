# AI GUIDELINES INDEX & QUICK START
**Determined Project - April 5, 2026**

---

## 🎯 START HERE: Quick Navigation

### "I need to make a decision right now" → 90 seconds
→ Read: [UFM_INTEGRATION_QUICKREF.md](UFM_INTEGRATION_QUICKREF.md) (1 page)

### "I want to understand the framework" → 1 hour
→ Read: [AI_GUIDELINES_COMPREHENSIVE.md](AI_GUIDELINES_COMPREHENSIVE.md) (11 sections)

### "I'm implementing this in code" → 30 minutes
→ Read: [UFM_INTEGRATION_PRACTICAL.md](UFM_INTEGRATION_PRACTICAL.md) (code examples)

### "I need the big picture" → 5 minutes
→ Read: [AI_GUIDELINES_MASTER_SUMMARY.md](AI_GUIDELINES_MASTER_SUMMARY.md) (overview)

---

## 📚 Complete Document Set

| Document | Purpose | Length | Read Time | When |
|----------|---------|--------|-----------|------|
| **UFM_INTEGRATION_QUICKREF.md** | Daily reference | 1 page | 2 min | BEFORE each decision |
| **AI_GUIDELINES_COMPREHENSIVE.md** | Full framework | 1000+ lines | 60 min | Once, carefully |
| **UFM_INTEGRATION_PRACTICAL.md** | Implementation guide | 400+ lines | 30 min | When coding |
| **AI_GUIDELINES_MASTER_SUMMARY.md** | Overview & tying together | 300+ lines | 10 min | To understand structure |

---

## 🔍 Find What You Need (By Topic)

### Topic: UFM API
**Need**: API endpoints, how to call, what they return  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 2** (UFM API Integration)  
**Quickref**: UFM_INTEGRATION_QUICKREF.md "UFM API CALL"  
**Practical**: UFM_INTEGRATION_PRACTICAL.md **Part 1** (Python setup)

---

### Topic: Causal Tree
**Need**: How to build tree, what paths to enumerate, how to choose  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 3** (Causal Tree Executor)  
**Quickref**: UFM_INTEGRATION_QUICKREF.md "CAUSAL TREE (90 SECONDS)"  
**Practical**: UFM_INTEGRATION_PRACTICAL.md **Part 4** (Complete workflow example)  
**Example**: AI_GUIDELINES_COMPREHENSIVE.md **Section 8** (Full worked example)

---

### Topic: Pre-Action Gate
**Need**: The 5 questions, what passes/fails, when to say NO  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 4** (Pre-Action Gate)  
**Quickref**: UFM_INTEGRATION_QUICKREF.md "PRE-ACTION GATE (5 QUESTIONS)"  
**Practical**: UFM_INTEGRATION_PRACTICAL.md any validation function  
**Summary**: All decisions must pass ALL 5 questions

---

### Topic: Five Metalanguage Principles
**Need**: What they are, how to verify, what each means  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 6** (Five Principles)  
**Quickref**: UFM_INTEGRATION_QUICKREF.md "FIVE PRINCIPLES (QUICK CHECK)"  
**Table**: Identity | State | Causality | Coherence | Determinism  
**Remember**: All 5 must be YES

---

### Topic: Decision Types (A/B/C/D)
**Need**: What each type means, how to handle, what UFM expects  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 5** (Decision Types)  
**Quickref**: UFM_INTEGRATION_QUICKREF.md "DECISION TYPES AT A GLANCE"  
**Table**: Type A (low risk, 0.85-1.0) | B (medium, 0.70-0.85) | C (high, 0.60-0.75) | D (STOP)  
**Critical**: Type D = stop before executing, expand framework first

---

### Topic: Consolidation Principles
**Need**: What to consolidate, what to preserve, why  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Part 1** (Foundation) + **Section 7** (Checklist)  
**Reference**: UNIVERSAL_CONSOLIDATION_FINAL_REPORT.md (audit results of 220 files)  
**Rules**: 
- Production (root): Unified
- Research (experimental/): Preserved
- Specialized (src/, subfolders): Separate

---

### Topic: Framework Integration
**Need**: How to use UNIFIED_API_SERVER, framework.json, hot-reload  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Part 1** (Foundation)  
**Practical**: UFM_INTEGRATION_PRACTICAL.md **Part 5** (Integration with existing systems)  
**Rule**: All new systems route through framework, no bypass utilities

---

### Topic: UFM API Endpoints
**Need**: All endpoints, what they do, how to call  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 2** (UFM API Integration)  
**Quick**: UFM_INTEGRATION_QUICKREF.md "UFM API ENDPOINTS SUMMARY"  
**Practical**: UFM_INTEGRATION_PRACTICAL.md **Part 1** (Client setup)  
**Endpoints**: 
- /v1/process/universal (main validation)
- /v1/compare (compare paths)
- /v1/reconstruct (verify reversible)
- /v1/health (check online)
- /v1/process (fallback)
- /v1/replay (deterministic replay)

---

### Topic: Error Handling
**Need**: What to do if UFM fails, if gate fails, if violation occurs  
**Read**: UFM_INTEGRATION_PRACTICAL.md **Part 6** (Error handling)  
**Recovery**: AI_GUIDELINES_COMPREHENSIVE.md **Section 10** (Violation recovery)  
**Fallback**: Use local gate if UFM unavailable

---

### Topic: Logging Decisions
**Need**: How to record decisions to ledger, where to log  
**Read**: UFM_INTEGRATION_PRACTICAL.md **Part 3** (Decision logging)  
**Locations**: 
- `/memories/session/DECISIONS_LOG_CURRENT.md` (session)
- `src/ledgers/ai_decision_ledger.jsonl` (persistent)  
**Format**: JSON with timestamp, tree path, UFM result

---

### Topic: Complete Example
**Need**: See full decision flow from start to finish  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 8** (Full example: Adding statistics endpoint)  
**Alternative**: UFM_INTEGRATION_PRACTICAL.md **Part 4** (Complete workflow class)  
**Quickref**: UFM_INTEGRATION_QUICKREF.md "EXAMPLE: Adding New Endpoint"

---

### Topic: When to Say NO
**Need**: When to block execution, when to reconsider  
**Read**: AI_GUIDELINES_COMPREHENSIVE.md **Section 5** (Type D decisions)  
**Quickref**: UFM_INTEGRATION_QUICKREF.md "QUICK RULES TO NEVER BREAK"  
**Rules**: 
- quality_score < 0.75 → NO
- is_valid = false → NO
- Gate check fails → NO
- Either conditions fail → NO

---

## ⚡ Copy-Paste Quick Snippets

### Validate a Decision (5 lines)
```python
from UFM_CLIENT import get_ufm_client
client = get_ufm_client()
decision = {"choice": "YOUR CHOICE", "tree_path": "A1"}
result = client.process_universal(json.dumps(decision).encode(), verify=True)
print(f"Quality: {result['quality_score']:.2f}, Valid: {result['is_valid']}")
```

See: UFM_INTEGRATION_QUICKREF.md "UFM API CALL"

---

### Build Causal Tree (Template)
```
User Request: [What they want]
├── Path A1 (Type A - framework-aligned)
│   ├── Pros: [advantages]
│   └── Cons: [disadvantages]
├── Path A2 (Type A - alternative)
│   └── ...
├── Path B1 (Type B - conditional)
│   └── Condition: [required state]
└── Path C1 (Type C - forced)
    └── Constraint: [what forces this]

CHOSEN: Path A1
BECAUSE: [reasoning]
```

See: AI_GUIDELINES_COMPREHENSIVE.md Part 3, Section 8

---

### Pre-Action Gate (Checklist)
```
☐ Framework pattern?   → Must be YES
☐ Danger patterns?     → Must be NO
☐ Reversible?          → Must be YES
☐ Clear?               → Must be YES
☐ Aligned?             → Must be YES

ALL YES → Proceed
ANY NO → Reconsider
```

See: UFM_INTEGRATION_QUICKREF.md "PRE-ACTION GATE (5 QUESTIONS)"

---

### Five Principles Check (Checklist)
```
☐ Identity:    Unique/identifiable?
☐ State:       Measurable before/after?
☐ Causality:   Input→Output chain traceable?
☐ Coherence:   No contradictions?
☐ Determinism: Reproducible/verifiable?

ALL YES → Likely to pass UFM
ANY NO → Likely to fail UFM (fix first)
```

See: UFM_INTEGRATION_QUICKREF.md "FIVE PRINCIPLES (QUICK CHECK)"

---

## 🚀 The Complete Flow (One Picture)

```
REQUEST
   ↓
PARSE INTENT (What do they really want?)
   ↓
BUILD TREE (What paths exist?)
   ↓
CLASSIFY (Type A/B/C/D?)
   ↓
5-GATE CHECK (All pass?)
   ↓ YES
ENCODE FOR UFM (Convert tree to JSON)
   ↓
CALL UFM API (/v1/process/universal)
   ↓
CHECK RESULT (quality > 0.75 AND valid?)
   ↓ YES
LOG DECISION (To ledger, session)
   ↓
EXECUTE (Code + test + done)
   ↓
COMPLETE ✓

Any step = NO/FAIL → DO NOT PROCEED
Reconsider tree, try different path
```

---

## 📋 By-Situation Quick Guide

### Situation: "Add new feature"
1. Read: UFM_INTEGRATION_QUICKREF.md (2 min)
2. Build causal tree
3. Run 5-gate check
4. Call UFM API
5. Proceed if validated

---

### Situation: "Fix bug"
1. Build tree (how to fix?)
2. Check if reversible (can undo?)
3. Run 5-gate (risk assessment)
4. Call UFM (validate)
5. Deploy + log

---

### Situation: "Consolidate code"
1. Check consolidation principles (truly duplicate?)
2. Build tree (consolidate where?)
3. Verify: Production/Research/Specialized category
4. Run 5-gate
5. Call UFM (validate)
6. Execute consolidation + log

---

### Situation: "Change framework"
1. Build tree (what changes?)
2. Classify (likely Type D - framework expansion!)
3. **STOP** - Do not execute
4. Create framework expansion
5. Validate expansion
6. Create new tree under expanded framework
7. Continue with new tree

---

### Situation: "UFM rejected (quality < 0.75)"
1. Check why (quality_score, causal_principles)
2. Look at five principles (any NO?)
3. Check decision type (A/B/C/D - is it right?)
4. Reconsider tree - build different path
5. Retry UFM with new tree
6. If still fails: ask for review in /memories/

---

### Situation: "I accidentally bypassed framework"
1. **STOP** immediately
2. Delete the non-framework code
3. Revert all dependencies
4. Record in VIOLATION_LOG.md why it happened
5. Propose framework-aligned alternative
6. Build tree for correct approach
7. Retry

---

## 🔗 Connected Documents (For Reference)

**Also Related To**:
- UNIVERSAL_CONSOLIDATION_FINAL_REPORT.md - Audit of 220 files
- UNIFIED_ARCHITECTURE_GUIDE.md - How unified systems work
- PROJECT_UNIFICATION_COMPLETE_APRIL_5_2026.md - Consolidation summary
- AI_CAUSAL_TREE_EXECUTOR.json - Causal tree definition
- AI_SELF_INSTRUCTIONS_SINGULARITY.json - Original enforcement rules

---

## ✅ Status & Verification

### Framework is Complete
- ✓ Consolidation lessons incorporated
- ✓ UFM API fully integrated (5 endpoints)
- ✓ Five principles on all decisions
- ✓ Causal tree mandatory
- ✓ Pre-action gate required
- ✓ Decision types (A/B/C/D) classified
- ✓ Violation recovery defined
- ✓ 4-document comprehensive set created

### How to Verify It's Working
1. New decisions follow: Tree → Gate → UFM → Log → Execute
2. UFM APIs all callable (check health first)
3. Lexicon understood (use five principles correctly)
4. No decisions bypass the framework
5. All executive decisions in ledger

---

## 📞 Quick Help

**Problem**: "The five principles are hard"  
→ Look at: UFM_INTEGRATION_QUICKREF.md "FIVE PRINCIPLES (QUICK CHECK)"

**Problem**: "I don't understand decision types"  
→ Look at: UFM_INTEGRATION_QUICKREF.md "DECISION TYPES AT A GLANCE"

**Problem**: "UFM API failed"  
→ Look at: UFM_INTEGRATION_PRACTICAL.md "Part 6: Error Handling"

**Problem**: "Framework change rejected by UFM"  
→ Look at: AI_GUIDELINES_COMPREHENSIVE.md "Section 5: Type D Decisions"

**Problem**: "I don't know what to consolidate"  
→ Look at: AI_GUIDELINES_COMPREHENSIVE.md "Section 7: Unified Architecture Checklist"

**Problem**: "I broke the framework accidentally"  
→ Look at: AI_GUIDELINES_COMPREHENSIVE.md "Section 10: Violation Recovery"

---

## 📖 How to Read All 4 Documents

### Reading Order (Recommended)
1. **THIS FILE** (5 min) - Understand structure
2. **UFM_INTEGRATION_QUICKREF.md** (10 min) - One-page overview
3. **AI_GUIDELINES_COMPREHENSIVE.md** (60 min) - Full framework
4. **UFM_INTEGRATION_PRACTICAL.md** (30 min) - Code examples
5. **AI_GUIDELINES_MASTER_SUMMARY.md** (10 min) - Ties together

**Total**: About 2 hours for complete understanding

### Maintenance Order (Monthly)
1. UFM_INTEGRATION_QUICKREF.md - Keep updated with changes
2. AI_GUIDELINES_COMPREHENSIVE.md - Update sections as framework evolves
3. UFM_INTEGRATION_PRACTICAL.md - Update code examples as needed
4. Master Summary - Keep in sync with main guidelines

---

## 🏁 You're Ready

You have everything needed to:
- ✓ Make intelligent AI decisions
- ✓ Use UFM to validate them
- ✓ Consolidate the right way
- ✓ Follow the framework
- ✓ Record everything to ledger
- ✓ Recover from mistakes

**Next Step**: Read UFM_INTEGRATION_QUICKREF.md (90 seconds)

Then make your decisions confidently.

---

**Framework Status**: COMPLETE, COMPREHENSIVE, READY FOR PRODUCTION USE

All AI decisions in Determined project follow this framework.

