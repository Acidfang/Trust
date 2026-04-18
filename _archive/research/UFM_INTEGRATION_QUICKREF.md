# UFM API INTEGRATION QUICK REFERENCE
**For Developers Making Decisions in Determined Project**

---

## ONE-PAGE DECISION FLOW

### Every Decision Follows This Path:
```
1. Parse Intent → 2. Build Tree → 3. Classify → 4. Gate Check
↓
5. Encode → 6. Call UFM → 7. Log → 8. Execute
```

---

## WHEN TO USE WHAT

| Situation | Use This | Endpoint |
|-----------|----------|----------|
| I'm about to change something | Build causal tree | (local first) |
| I want to verify tree is good | Pre-action gate 5-check | (local) |
| I want UFM to validate decision | Process Universal | `/v1/process/universal` |
| I want to compare two paths | Compare endpoint | `/v1/compare` |
| I want to verify reversibility | Reconstruct endpoint | `/v1/reconstruct` |

---

## CAUSAL TREE (90 SECONDS)

### Just Answer These:
1. **What am I choosing?** (Be specific)
2. **What are ALL paths?** (List at least A1, A2, B1, C1)
3. **Which is best?** (Why this one?)
4. **Why NOT the others?** (Rejection reasons)
5. **How will I know it worked?** (Success criteria)
6. **How do I undo it?** (Reversal steps)

That's your tree. Document it.

---

## PRE-ACTION GATE (5 QUESTIONS)

### Before You Code Anything:

☐ **Question 1: Framework?**  
Is this a framework pattern? YES → Continue

☐ **Question 2: Danger Patterns?**  
Does it have: standalone code, parallel infrastructure, bypass framework?  
YES → STOP. NO → Continue

☐ **Question 3: Reversible?**  
Can you define AND test undo?  
YES → Continue

☐ **Question 4: Clear?**  
Can you answer: What? Why? How? Undo?  
YES → Continue

☐ **Question 5: Aligned?**  
Does it follow consolidation principles (unify production, preserve research)?  
YES → Continue

**All 5 YES? → Run UFM validation**  
**Any NO? → Reconsider tree, try different path**

---

## UFM API CALL (Copy-Paste Ready)

```python
import json
import base64
import urllib.request

# Your decision (complete this)
decision = {
    "timestamp": "2026-04-05T10:30:00Z",
    "choice": "YOUR CHOICE HERE",
    "framework_alignment": "YES",  # YES/PARTIAL/NO
    "risk_score": 0.15,  # 0.0-1.0 (higher=riskier)
    "five_principles": {
        "identity": "Is it unambiguous?",
        "state": "Can we measure it?",
        "causality": "Input→output chain?",
        "coherence": "No contradictions?",
        "determinism": "Verifiable/reproducible?"
    },
    "causal_tree_path": "A1",  # A1/A2/B1/C1/D1
    "verification_plan": "HOW TO TEST",
    "undo_plan": "HOW TO REVERSE",
    "classification": "Type A"  # A/B/C/D
}

# Encode
b64 = base64.b64encode(json.dumps(decision).encode()).decode()

# Call UFM
url = "https://ufm-engine.onrender.com/v1/process/universal"
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "ufm_live_8f430fc7.Psl_W4LR5Y_4C1EVmdIgQWrtoNyv65Rx4jvmYW2H2DA"
}
payload = json.dumps({"data_b64": b64, "verify": True})

req = urllib.request.Request(url, data=payload.encode(), headers=headers, method="POST")
with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode())

# Check result
quality_score = result.get("quality_score", 0)
is_valid = result.get("is_valid", False)

if quality_score > 0.75 and is_valid:
    print("✓ UFM APPROVED - Proceed with execution")
else:
    print(f"✗ UFM REJECTED - quality_score={quality_score}, reconsider tree")
```

---

## FIVE PRINCIPLES (QUICK CHECK)

| Principle | Question | Pass Criteria |
|-----------|----------|---------------|
| **Identity** | Is it uniquely identifiable? | YES - someone else can identify exactly what decided |
| **State** | Can we measure before/after? | YES - success criteria defined + measurable |
| **Causality** | Input→output chain traceable? | YES - continuous chain, no gaps, each step verifiable |
| **Coherence** | No contradictions? | YES - consistent with framework + previous decisions |
| **Determinism** | Outcome reproducible? | YES - same inputs = same output always |

### Quick Rule:
- All 5 YES → Likely to pass UFM (quality_score > 0.75)
- Any NO → Likely to fail UFM (fix before calling)

---

## DECISION TYPES AT A GLANCE

| Type | What | Example | Risk | UFM Expect |
|------|------|---------|------|-----------|
| **A** | Framework pattern exists | New endpoint like existing ones | LOW | 0.85-1.0 |
| **B** | Conditional, state-dependent | Archive if tests pass | MEDIUM | 0.70-0.85 |
| **C** | Forced by constraints | Use old tech due to compatibility | HIGH | 0.60-0.75 |
| **D** | Contradicts framework | Bypass framework entirely | CRITICAL | Stop, expand framework first |

---

## QUICK RULES TO NEVER BREAK

```
Rule 1: NO CAUSAL TREE = DO NOT CODE
Rule 2: NO PRE-ACTION GATE = DO NOT EXECUTE
Rule 3: NO UFM VALIDATION = DO NOT COMMIT
Rule 4: NO LEDGER RECORD = UNDO IT

Rule 5: Production code = Unified (consolidate)
Rule 6: Research code = Experimental (preserve)
Rule 7: Specialized code = Subfolders (separate)
Rule 8: Framework use = Always (no bypass)
```

---

## QUICK REFERENCE - BY SITUATION

### "I want to add a new feature"
1. Build tree (what paths exist?)
2. Classify (Type A/B/C/D?)
3. Run 5-gate (framework check)
4. Call UFM (validate)
5. Code + log

### "I want to consolidate files"
1. Build tree (consolidate which ones?)
2. Check consolidation principle (truly duplicate?)
3. Run 5-gate (framework alignment)
4. Call UFM (validate)
5. Consolidate + log

### "I want to fix a bug"
1. Build tree (how to fix?)
2. Verify reversible (can undo fix if needed?)
3. Run 5-gate (risk assessment)
4. Call UFM (validate)
5. Deploy fix + log

### "I want to change framework"
1. Build tree (what changes?)
2. Classify (likely Type D - framework expansion!)
3. If Type D: STOP, create expansion first
4. Create new tree under expanded framework
5. Now tree becomes Type A under new framework
6. Run 5-gate + call UFM (validate) + execute

---

## UFM API ENDPOINTS SUMMARY

```
GET /v1/health
→ Check if UFM online

POST /v1/process/universal
→ Full 7-stage validation of decision (MAIN USE)

POST /v1/process
→ Quick check if data decodable

POST /v1/compare
→ Compare two paths (which is better?)

POST /v1/reconstruct
→ Verify reversibility (round-trip integrity)

GET /v1/replay/{seed}
→ Replay decision deterministically (verify causality)
```

---

## EXAMPLE: Adding New Endpoint

**Request**: "Add /api/status endpoint"

**Tree** (30 seconds):
- A1: Add to UNIFIED_API_SERVER, register in framework.json (BEST)
- A2: Query existing ledger directly (ALTERNATIVE)
- C1: Standalone tool (REJECTED - framework bypass)

**Gate Check** (30 seconds):
- ☐ Framework pattern? YES (follows endpoint pattern)
- ☐ Danger patterns? NO
- ☐ Reversible? YES (undo = remove, revert framework.json)
- ☐ Clear? YES
- ☐ Aligned? YES

**UFM Call** (30 seconds):
```
{
  "choice": "Add /api/status endpoint",
  "framework_alignment": "YES",
  "risk_score": 0.10,
  "classification": "Type A"
  ... (fill in 5 principles) ...
}
→ Encode → Call UFM → quality_score: 0.92 ✓
```

**Execute**: Code + register + test + log

**Total Time**: 5 minutes tree + gate + UFM

---

## REMEMBER

- Every decision goes through: Tree → Gate → UFM → Log → Execute
- UFM quality_score < 0.75? Reconsider tree, don't force it
- If surprised by outcome? That's Type D - stop, expand framework
- No shortcutting: Tree → Gate → UFM ALL REQUIRED
- Violations recover: Delete + revert + document + retry

---

**Questions?** See AI_GUIDELINES_COMPREHENSIVE.md for full details.

