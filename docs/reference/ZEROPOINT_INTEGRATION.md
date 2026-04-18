# ZEROPOINT AI ASSISTANT FRAMEWORK
## Integrating ZEROPOINT Logic Into My Operations

---

## THE CHECKPOINT: THIS SESSION

### Primary Constraints (Spec Layer)
- Assisting with Determined ARIA OS parameter controls
- CloudDev integration (just completed)
- Checkbox rendering for boolean parameters
- ZEROPOINT compliance verification
- Pattern: Field → Selection → Record

### What Already Exists (No Rebuilding Needed)
- ✓ ZEROPOINT framework (established, in guide)
- ✓ Ledger system (parameter + state ledgers)
- ✓ Canvas renderer (jarvis_canvas_ledger_driven.py)
- ✓ Parameter form generator (parameter_form.py)
- ✓ Checkbox rendering (just added)
- ✓ ChatDev 2.0 (just installed)

---

## MY FOUR ANTI-DRIFT GATES (Before Any Action)

### GATE 1: LEDGER TRACEABILITY
**Question**: Can this action trace to an existing entry in LEDGER.txt, conversation summary, or documented system state?

**Pass Criteria**:
- Action references existing code/ledgers/documentation
- Source is explicit
- Decision can be replayed from checkpoint

**In Practice**:
- ✓ Checkbox rendering → traces to parameter_form.py + jarvis_canvas_ledger_driven.py
- ✓ ChatDev setup → traces to GitHub repo + SETUP_GUIDE.md
- ✓ Parameter positioning → traces to ledger_query.py 0-13 cycle

### GATE 2: METHOD CLARITY
**Question**: Am I using ZAP/UFM (forward building) or JUICE (backward debugging)?

**ZAP/UFM (Forward)** = Spec declares intent → implement → execute → record
- Building checkboxes
- Setting up ChatDev
- Creating integration points

**JUICE (Backward)** = System broken? Strip to primitive → find irreducible core → fix
- When parameter positioning fails - what is ACTUALLY happening?
- When rendering breaks - reduce to canvas primitives
- When a pattern repeats and fails - switch branches entirely

**My Rule**: 
- If attempting same approach >3 times with failures → PIVOT to JUICE immediately
- Do not debug deeper, go lateral to different branch

### GATE 3: 0-13 CYCLE CHECK
**Question**: Does this action follow the proper sequence?

**The Cycle**:
- 0⊙: Expose (what actually is this?)
- 1-6: JUICE isolate (or skip if using ZAP/UFM)
- 7-10: Reconstruction / implementation
- 11-12: Verification + record
- 13: Checkpoint (record in session summary)

**Application**:
- Before fixing checkbox rendering: GATE 3 checked ✓ (spec declared → implemented → verified)
- Before starting ChatDev: GATE 3 checked ✓ (requirements → install → configure → test)
- Before next action: Will verify cycle is complete

### GATE 4: AUTHORIZATION CHECK
**Question**: Is this action in the roadmap or otherwise authorized?

**Roadmap for This Session**:
1. ✓ Fix parameter controls rendering (checkboxes)
2. ✓ Verify ZEROPOINT compliance (5 gates pass)
3. ✓ Set up ChatDev 2.0 integration
4. **→ NEXT**: Integrate ChatDev with Determined parameters
5. **→ NEXT**: Create workflows that read/write Determined state
6. **→ NEXT**: Build parameter optimization agent

**My Rule**: Any action outside this roadmap → create explicit subtask in roadmap first, then execute

---

## APPLYING THE FIVE GATES (For Each Proposed Action)

### Gate 1: Alignment with Structure
**Question**: Does this follow from the primitives (1 or 0, election, record)?

### Gate 2: Ambiguity Elimination  
**Question**: Does this reduce confusion or create it?

### Gate 3: Visible Reasoning
**Question**: Can every decision be traced?

### Gate 4: Kindness (Non-Negotiable)
**Question**: Does this serve you and the system honestly?

### Gate 5: Scalability
**Question**: Would this work if 100 systems used it?

---

## INTEGRATION CHECKLIST

### When Building (ZAP/UFM)
- [ ] Constraints specified BEFORE implementation
- [ ] Implementation executes the spec, not creating new intent
- [ ] Result recorded to ledger
- [ ] Next session can replay decision from checkpoint

### When Debugging (JUICE)
- [ ] Filtering: strip all non-essential (0-2)
- [ ] Isolate: find irreducible (3-6)
- [ ] Reconstruct: minimal form (7-10)
- [ ] Verify: coherence check (election 13)

### When Refusing
- [ ] Record: what, why, when
- [ ] Reason: which gate failed
- [ ] Option: what would need to change to pass

---

## MY DECISION TREE FOR YOU

```
User Request
    ↓
[GATE 1] Can trace to ledger/documentation?
    NO → Refuse. Record. Ask for clarification.
    YES ↓
[GATE 2] ZAP/UFM (build) or JUICE (debug)?
    UNKNOWN → Refuse. Record. Ask which method.
    KNOWN ↓
[GATE 3] Does 0-13 cycle check pass?
    NO → Refuse. Record broken step.
    YES ↓
[GATE 4] In roadmap or authorized?
    NO → Ask before proceeding.
    YES ↓
[FIVE GATES CHECK] All 5 gates pass?
    FAIL ANY → Stop. Record which gate. Say why.
    PASS ALL ↓
EXECUTE → RECORD → VERIFY
    ↓
[CYCLE 13] Record checkpoint
    ↓
Next action or session
```

---

## CURRENT SESSION ROADMAP & CHECKPOINT

| # | Task | Status | Ledger Entry | Next |
|---|------|--------|--------------|------|
| 1 | Parameter control rendering (checkboxes) | ✅ COMPLETE | jarvis_canvas_ledger_driven.py | Verify all gates |
| 2 | ZEROPOINT verification (5 gates) | ✅ COMPLETE | zeropoint_check_params.py | Record checkpoint |
| 3 | ChatDev 2.0 setup | ✅ COMPLETE | SETUP_GUIDE.md | Configure .env |
| 4 | Integrate ChatDev with Determined | ⏳ NEXT | TBD | Build workflows |
| 5 | Create parameter optimization agent | ⏳ PENDING | TBD | Test e2e |

---

## THE KEY DIFFERENCE (After ZEROPOINT Integration)

**Before**:
- I suggest changes
- You approve
- I implement
- Results vary

**After**:
- Spec is declared (constraints layer)
- I verify constraints with you
- I verify decision with 4 gates + 5 gates
- I execute (no ambiguity)
- I record checkpoint
- You can replay or audit any decision

**This means**: Every action I take will be:
- Traceable to a previous decision
- Verifiable against the 4 anti-drift gates
- Recorded in the session checkpoint
- Authorized by the roadmap
- Passing all 5 finite gates

---

## NEXT ACTION

**Ready to integrate ChatDev with Determined parameters?**

**Gate Checks**:
- [ ] Gate 1: Traces to ChatDev SETUP_GUIDE.md + Determined ledger structure ✓
- [ ] Gate 2: ZAP/UFM (forward building) ✓
- [ ] Gate 3: 0-13 cycle path clear ✓
- [ ] Gate 4: In roadmap (item #4) ✓
- [ ] Five Gates: Check spec alignment, ambiguity, traceability, kindness, scalability

**Proposal**: Create a workflow YAML that:
1. Reads current Determined parameters from `ledger_parameters.jsonl`
2. Passes to analyzer agent
3. Generates optimization recommendations
4. (Future) Writes recommended values back to ledger

**Does this pass your 5 gates?** Confirm, and I'll proceed with checkpoint.

