# 🔴 RCA-FIRST PROTOCOL (Root Cause Analysis)

**Document ID**: RCA-FIRST-2026-03-29
**Status**: MANDATORY ENFORCEMENT
**Effective**: All operations on Determined project

---

## WHEN TO RUN RCA

**Trigger Conditions (ANY of these = RCA required):**
- Unexpected behavior occurs
- Error message doesn't match documentation
- Feature stops working without code changes
- Same error occurs across multiple attempts
- "This worked yesterday but not today"
- Any behavior that contradicts the spec
- Any discrepancy between EXPECTED and ACTUAL

**Critical:** If you're tempted to "try one more thing" → STOP and RCA first.

---

## PROTOCOL EXECUTION (Step by Step)

### **STEP 1: STOP IMMEDIATELY**

❌ **DO NOT:**
- Continue debugging
- Try another variation
- Make guesses
- Ignore the discrepancy
- Assume it's transient

✅ **DO THIS:**
- Stop what you're doing
- Document what happened
- Recognize the unexpected behavior

---

### **STEP 2: DOCUMENT THE DISCREPANCY**

Write down exactly what you expected vs. what actually happened:

```
EXPECTED OUTPUT/BEHAVIOR:
[Describe what you expected based on documentation or prior behavior]

ACTUAL OUTPUT/BEHAVIOR:
[Describe exactly what happened instead]

THE DELTA (Difference):
[What is the gap between expected and actual?]

EVIDENCE:
[Console output, error messages, ledger entries, affected files]
```

**Example:**
```
EXPECTED: jarvis_v3.py starts on port 8081
ACTUAL: Error "Address already in use"
DELTA: Port is occupied by another process
EVIDENCE: Error message, no process visible in task list
```

---

### **STEP 3: IDENTIFY THE WRONG ASSUMPTION**

Ask yourself: **"What assumption did I make that was proven wrong?"**

**Common wrong assumptions:**
- "The code hasn't changed" (but it was modified)
- "The system is deterministic" (but it has timing issues)
- "The error message tells me the cause" (error shows symptom, not root)
- "This is a one-time glitch" (it's systematic)
- "The spec covers this" (the spec has a gap)
- "I understand this component" (I actually don't know all its behaviors)

**Write it as a statement:**
```
I assumed: "Port 8081 would be free"
Wrong because: "The previous instance didn't shut down cleanly"
Evidence: "Process still visible in lsof output"
```

---

### **STEP 4: READ COMPLETE ENUMERATION**

For the **domain where the assumption was wrong**, find and read the **complete enumeration file**.

**Enumeration files exist for:**
- **Graphics/Rendering** → Color, layout, widget rendering enumerations
- **Networking** → Port management, process lifecycle enumerations
- **Data Storage** → Ledger operations, persistence enumerations
- **Architecture** → Framework choices, abstraction level enumerations
- **Memory** → State management, cleanup enumerations

**When reading enumeration:**
- Read ALL branches, not just first few
- Identify which branch you're currently in
- Check if there are edge cases documented
- Note any warnings or cautions
- Record what you learn

---

### **STEP 5: MAP COMPLETE DECISION SPACE**

Create a complete map of all possible approaches to this problem:

```
⊙ DECISION_SPACE_FOR_[YOUR_PROBLEM]

├─ Approach A: [Description]
│  ├─ Sub-option A1: [How it works, constraints]
│  ├─ Sub-option A2: [How it works, constraints]
│  └─ Sub-option A3: [How it works, constraints]
│
├─ Approach B: [Description]
│  ├─ Sub-option B1: [How it works, constraints]
│  └─ Sub-option B2: [How it works, constraints]
│
└─ Approach C: [Different abstraction level]
   └─ [How it works, constraints]
```

**For port conflict example:**
```
⊙ DECISION_SPACE_FOR_PORT_CONFLICTS

├─ Approach A: Kill existing process
│  ├─ Sub A1: Use lsof/netstat to find PID
│  ├─ Sub A2: Use taskkill /F to terminate
│  └─ Sub A3: Manual process termination
│
├─ Approach B: Use different port
│  ├─ Sub B1: 8082
│  ├─ Sub B2: 9000
│  └─ Sub B3: Dynamic port selection
│
└─ Approach C: Implement graceful restart
   └─ Detect stale process and auto-cleanup
```

---

### **STEP 6: TEST TOP BRANCHES MINIMALLY**

For the 2-3 most promising branches:

**Test Branch A:**
1. Implement minimal working version
2. Run it
3. Does it solve the problem? 
4. Record: **WORKS** or **FAILS** (and why)
5. **Time**: _____ (record how long)

**Test Branch B:**
1. Implement minimal working version
2. Run it
3. Does it solve the problem?
4. Record: **WORKS** or **FAILS** (and why)
5. **Time**: _____ (record how long)

**Test Branch C (if needed):**
1. Implement minimal working version
2. Run it
3. Does it solve the problem?
4. Record: **WORKS** or **FAILS** (and why)
5. **Time**: _____ (record how long)

**Critical Rule:** Let branches fail naturally. Do NOT debug a failing branch—switch to a different branch instead.

---

### **STEP 7: VERIFY AGAINST LEDGER**

Consult the authority sources:

- [ ] Does this decision appear in COMPLETE_CHOICE_LEDGER.md?
- [ ] What was the documented outcome?
- [ ] Are there known trade-offs?
- [ ] Why was THIS branch chosen before?
- [ ] Is there a documented reason why other branches were rejected?

**If you find a ledger entry:**
- Read it completely
- Understand the full context
- Apply the documented lessons
- Avoid repeating past mistakes

---

### **STEP 8: RECORD TO LEDGER**

Create an immutable record of your investigation:

```json
{
  "type": "rca_investigation",
  "timestamp": "2026-03-29T14:30:45.123456Z",
  "investigator": "Claude",
  
  "unexpected_behavior": "jarvis_v3.py fails to start",
  "error_message": "Address already in use on port 8081",
  
  "expected_vs_actual": {
    "expected": "Server binds to port 8081 immediately",
    "actual": "OSError: Address already in use",
    "delta": "Port is occupied"
  },
  
  "wrong_assumption_identified": "I assumed the previous instance shut down cleanly",
  "assumption_evidence": "Process still present in lsof with PID 2847",
  
  "enumeration_consulted": "NETWORK_PROCESS_LIFECYCLE_ENUMERATION.md",
  "enumeration_branches_read": [
    "Branch 1: Clean shutdown process",
    "Branch 2: Unclean termination recovery",
    "Branch 3: Port reuse strategies"
  ],
  
  "decision_space_mapped": true,
  "branches_in_space": ["Kill existing process", "Use different port", "Graceful restart"],
  
  "branches_tested": {
    "A_kill_process": {
      "attempt": "taskkill /F /PID 2847",
      "result": "WORKS",
      "time_minutes": 0.2
    },
    "B_different_port": {
      "attempt": "Use port 8082 instead",
      "result": "WORKS (but wrong port)",
      "time_minutes": 0.1
    },
    "C_graceful_restart": {
      "attempt": "Health check before bind",
      "result": "NOT_TESTED",
      "time_minutes": 0.0
    }
  },
  
  "ledger_consulted": true,
  "ledger_entries_found": 1,
  "ledger_recommendation": "Use health check before bind to prevent port conflicts",
  
  "chosen_solution": "Implement health check + auto-kill stale process",
  "reason": "Prevents future occurrences, aligns with existing patterns",
  "implementation_status": "IN_PROGRESS",
  
  "next_action": "Modify jarvis_v3.py to check port before binding",
  "prevention": "Added health check endpoint to detect running instances"
}
```

---

### **STEP 9: ONLY AFTER COMPLETE RCA**

Do NOT proceed until ALL of these are checked:

- [ ] Unexpected behavior fully documented
- [ ] Wrong assumption clearly identified
- [ ] Complete enumeration read (all branches)
- [ ] Decision space completely mapped
- [ ] Top 2-3 branches tested minimally
- [ ] Test results recorded (WORKS or FAILS)
- [ ] Ledger consulted for prior decisions
- [ ] RCA findings recorded to ledger
- [ ] Solution chosen with documented reason
- [ ] Root cause understood (not just "fixed the error")

**If any box is unchecked, go back to that step.**

---

## CRITICAL RULES

### Rule 1: Stop the Debugging Death Spiral

**If you're still debugging after 15 minutes with the same error:**
```
This means:
- The branch itself is wrong (not the implementation)
- You're in an impossible sub-space
- Switch branches completely, don't debug deeper
```

**Example from HTTPServer lesson:**
- HTTPServer + BaseHTTPRequestHandler was the WRONG branch
- Raw socket HTTP was the RIGHT branch at a different abstraction level
- Debugging within wrong branch was infinite loop
- Switching branches solved immediately

### Rule 2: Error Messages Show Symptoms, Not Causes

```
ERROR: "Address already in use"
  ↑ Symptom
  
ROOT CAUSE: "Previous instance didn't terminate cleanly
                due to unhandled exception in shutdown handler"
  ↑ Actual cause (requires enumeration + testing)
```

**Don't trust the error message to tell you the real problem.**

### Rule 3: Dead-End Branches Are Architectural

When same approach fails identically across multiple variations:
- The entire branch is wrong (not any single implementation)
- Go back to decision space
- Pick a DIFFERENT branch at a DIFFERENT abstraction level
- Do NOT keep trying harder in the same branch

### Rule 4: Every RCA Discovery Must Be Recorded

```
❌ FORBIDDEN:
  "I figured out the issue, moving on..."
  
✅ REQUIRED:
  "I figured out the issue, recording to ledger:
   _____________________________________________"
```

Unrecorded discoveries mean the next Claude instance starts blind.

---

## QUICK REFERENCE CHECKLIST

**When you encounter unexpected behavior:**

- [ ] **STOP** — Stop debugging immediately
- [ ] **DOCUMENT** — Write EXPECTED vs ACTUAL
- [ ] **IDENTIFY** — What assumption was wrong?
- [ ] **ENUMERATE** — Find complete enumeration for this domain
- [ ] **MAP** — Draw decision space with all branches
- [ ] **TEST** — Try top 2-3 branches minimally
- [ ] **VERIFY** — Check ledger for prior decisions
- [ ] **RECORD** — Write findings to ledger
- [ ] **CHOOSE** — Select branch with documented reason
- [ ] **PROCEED** — Only AFTER all steps complete

---

## WHAT NOT TO DO

| ❌ DO NOT | ✅ DO THIS INSTEAD |
|-----------|-------------------|
| "I'll try one more thing" | Stop and run RCA |
| "It's probably just a timing issue" | Test all branches, verify assumptions |
| "The error message says X" | Read enumeration to find root cause |
| "Let me debug this deeper" | Recognize dead-end branch, switch branches |
| Make decisions without enumeration | Map ALL branches before deciding |
| Leave discoveries unrecorded | Record to ledger immediately |
| Guess the root cause | Test, verify, document |
| Continue with same failing approach | Switch to completely different branch |

---

## SUMMARY

The RCA-FIRST protocol prevents the exact problems that plagued this project before:

1. **Debugging dead-end branches** → Stop at 15min, switch branches
2. **Missing complete enumeration** → READ EVERYTHING FIRST
3. **Unrecorded discoveries** → Record all findings to ledger
4. **Assuming error messages** → Use enumeration to find root cause
5. **Guessing solutions** → Test branches, document results

**This project works because we stopped guessing and started investigating.**

Keep it that way.

---

## ESCALATION

**If after complete RCA you still cannot find root cause:**
1. Document everything you've tried
2. Record all findings to ledger
3. Escalate to project maintainer
4. Include: EXPECTED, ACTUAL, DELTA, branches tested, ledger entries consulted

**Do not proceed blindly. Do not guess. Escalate.**
