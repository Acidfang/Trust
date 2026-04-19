---
layout: default
title: 0-Error Compute - Quick Reference
permalink: /zero-error/quick-ref/
toc: false
---

# 0-Error Compute - Quick Reference Card

**Print this. Keep it visible. Use it for every task.**

---

## The Core Rule (5 SECONDS)

**THINK → VERIFY → CODE**

Don't skip steps. Don't think fast. Think completely, verify completely, then code.

---

## Before Every File Edit (6 STEPS - 5 MINUTES)

1. **Read** PRE_ACTION_CHECKLIST.md
2. **Know** what you're building
3. **Map** all 0,1 states
4. **Verify** logic while thinking
5. **Mark** all unknowns (INCOMPLETE/UNVERIFIED)
6. **Code** only after all verified

---

## The 8 Phases (IN ORDER)

| Phase | What | Time | Done? |
|-------|------|------|-------|
| 1 | Understand requirement | 5-10 min | ☐ |
| 2 | Load frameworks | 5-10 min | ☐ |
| 3 | Think + verify logic | 15-45 min | ☐ |
| 4 | Verification checklist | 10-20 min | ☐ |
| 5 | Plan implementation | 5-10 min | ☐ |
| 6 | Execute (write code) | 10-30 min | ☐ |
| 7 | Test all paths | 10-20 min | ☐ |
| 8 | Document | 5-10 min | ☐ |

---

## Verification Checklist (BEFORE CODING)

☐ Binary Completeness — All states mapped?  
☐ Transition Coverage — Every state has exits?  
☐ Input Handling — All inputs covered?  
☐ Output Correctness — Output follows from input+state?  
☐ Gap Identification — Unknowns marked?  
☐ Assumption Logging — Decisions documented?  

**If ANY are unchecked → GO BACK TO PHASE 3**

---

## 7 Error Prevention Rules

1. **Don't skip thinking** — Partial thinking = bugs
2. **Don't assume** — Mark unknowns explicitly
3. **Don't code half-logic** — Complete thinking first
4. **Don't skip verification** — Check while thinking
5. **Don't ignore contradictions** — Resolve them now
6. **Don't test assumptions** — Verify them first
7. **Don't update assumptions later** — Define them upfront

---

## Decision Logging Format

When you make a decision:
```
DECISION: [What decision]
REASON: [Why you chose this]
ALTERNATIVES: [Other options considered]
VERIFIED: [How you verified this works]
TIMESTAMP: [When decided]
```

---

## What to Do If You Get Stuck

**Stuck on thinking?**
1. Return to Phase 1 — Do you understand the requirement?
2. Write down unknowns explicitly
3. Break problem into smaller pieces
4. Start with simplest case first

**Stuck on verification?**
1. Draw a state diagram
2. Trace through one example input completely
3. Check: Did it reach output? Yes/No
4. If no → Missing transition (go back to thinking)

**Code doesn't work?**
1. Reread Phase 3 thinking
2. Compare code to thinking
3. Is there a mismatch? Yes/No
4. If yes → Thinking was incomplete (go back to Phase 3)

---

## Success Criteria

✅ Requirement understood fully  
✅ All 0,1 states mapped  
✅ All transitions verified  
✅ All unknowns marked  
✅ Verification checklist all checked  
✅ Code written per plan  
✅ All tests pass  
✅ Documentation complete  

**If all are checked: TASK COMPLETE**

---

## Links to Full Frameworks

- [Universal Mandate]({{ site.baseurl }}/zero-error/mandate/) — Complete requirements
- [Task Template]({{ site.baseurl }}/zero-error/task-template/) — Full 8-phase details
- [Pre-Action Checklist]({{ site.baseurl }}/zero-error/pre-action/) — 6-step gate details
- [Master Index]({{ site.baseurl }}/zero-error/master-index/) — Navigate all frameworks

---

**Use this card. Every task. No exceptions.**
