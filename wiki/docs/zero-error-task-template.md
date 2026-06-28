---
layout: default
title: 0-Error Compute - Task Template
permalink: /zero-error/task-template/
toc: true
category: 0-Error Computing
tier: Application
difficulty: Intermediate
reading_time: 15
entry_point: Implementers
status: published
---

# 0-Error Task Template: 8-Phase Execution Framework

## The 8 Phases (In Order)

### PHASE 1: Understand (5-10 min)
**Goal**: Know exactly what you're building

What to do:
- Read the requirement completely
- Identify inputs and outputs
- Know what success looks like
- Note any unknowns

Verify:
- ✅ Can you explain requirement in 2 sentences?
- ✅ Do you know ALL inputs?
- ✅ Do you know ALL outputs?
- ✅ Do you know success criteria?

### PHASE 2: Context (5-10 min)
**Goal**: Load all relevant frameworks

What to do:
- Read [Universal Mandate](/Trust/zero-error/mandate/)
- Read [Pre-Action Checklist](/Trust/zero-error/pre-action/)
- Review [Quick Reference](/Trust/zero-error/quick-ref/) 
- Know your tools

Verify:
- ✅ Have you read current frameworks?
- ✅ Do you know your error prevention rules?
- ✅ Are you aware of similar past tasks?

### PHASE 3: Think (15-45 min)
**Goal**: Complete binary logic mapping

What to do:
- Map all possible states (0,1 combinations)
- Define all state transitions
- Verify every input path
- Check for contradictions
- Identify gaps (mark INCOMPLETE)
- Document assumptions

Verify While Thinking:
- ✅ Can you enumerate all states? 
- ✅ Does every transition exist?
- ✅ Are all inputs handled?
- ✅ Are there contradictions?
- ✅ Is logic coherent?

### PHASE 4: Verify (10-20 min)
**Goal**: Find verification gaps BEFORE coding

Verification Checklist:
- ✅ Binary Completeness — All 0,1 states mapped?
- ✅ Transition Coverage — Every state has valid exits?
- ✅ Input Handling — All input types covered?
- ✅ Output Correctness — Does output follow from input+state?
- ✅ Gap Identification — All unknowns marked?
- ✅ Assumption Logging — All decisions documented?

If ANY answer is NO:
- ❌ STOP — Do not proceed to coding
- ❌ Return to thinking phase
- ❌ Complete the gap
- ❌ Re-verify

### PHASE 5: Plan (5-10 min)
**Goal**: Know exactly what code to write

What to do:
- List files to create/modify
- Define functions/classes needed
- Identify integration points
- Plan testing approach

Verify:
- ✅ Can you list every code change?
- ✅ Do you know what each change does?
- ✅ Have you planned error handling?

### PHASE 6: Execute (10-30 min)
**Goal**: Write the code (should be trivial)

What to do:
- Create/modify files per plan
- Implement verified logic
- Add error handling
- Add logging/tracing

Verify During Coding:
- ✅ Does code match thinking?
- ✅ Are all branches implemented?
- ✅ Is error handling complete?
- ✅ Are comments clear?

### PHASE 7: Test (10-20 min)
**Goal**: Verify code matches logic

What to test:
- Happy path (normal inputs)
- Edge cases (boundary values)
- Error paths (invalid inputs)
- Integration (all components together)

Verify:
- ✅ Did happy path work?
- ✅ Did all edge cases work?
- ✅ Did error paths work?
- ✅ Did integration work?

### PHASE 8: Document (5-10 min)
**Goal**: Record what was built and why

What to do:
- Write/update README
- Document design decisions
- Log assumptions for future
- Note any known limitations
- Record verification results

## Total Time

- Thinking-heavy tasks: 1-2 hours (long Phase 3)
- Implementation-heavy tasks: 2-4 hours (long Phase 6)
- Simple tasks: 30 minutes (all phases)

**The longer you think, the faster coding goes.**

## What This Prevents

- ❌ Half-thinking before coding
- ❌ Unverified assumptions
- ❌ Skipped error handling
- ❌ Missing edge cases
- ❌ Code that doesn't match requirements

## Success Criteria

✅ All 8 phases completed  
✅ All verification checkpoints passed  
✅ Code works first try  
✅ No debugging needed  
✅ All requirements met  
✅ Documentation complete  

---

**Next:** [Quick Reference — Keep This Visible](/Trust/zero-error/quick-ref/)

