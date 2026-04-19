---
layout: default
title: 0-Error Compute - Pre-Action Checklist
permalink: /zero-error/pre-action/
toc: true
---

# Pre-Action Checklist: 6-Step Gate Before Every File Edit

## Do This Before Editing ANY File

This is not optional. 6 steps. 5 minutes. No exceptions.

---

## STEP 1: Understand The Requirement (2 min)

**What**: Know exactly what you're building.

**How**:
- Read the requirement completely
- Write it down in your own words
- Know what success looks like
- Identify what you don't know

**Pass Criteria**:
- Can you explain requirement in 1-2 sentences?
- Do you know all inputs?
- Do you know all outputs?
- Do you know success criteria?

If NO to any → Stop. Re-read requirement.

---

## STEP 2: Load Framework Context (2 min)

**What**: Get all frameworks loaded in thinking.

**How**:
- Review [Universal Mandate]({{ site.baseurl }}/zero-error/mandate/)
- Scan [Quick Reference]({{ site.baseurl }}/zero-error/quick-ref/)
- Know the 6-step verification checklist
- Know the 7 error prevention rules

**Pass Criteria**:
- Can you list 3 error prevention rules?
- Do you know the verification checklist?
- Are you ready to think?

If NO to any → Stop. Review frameworks again.

---

## STEP 3: Map All States (Binary Completeness) (3-15 min)

**What**: Think through ALL possible states and transitions.

**How**:
- What are all possible states? (list them)
- What are all possible transitions? (state changes)
- Can every input reach an output? (yes/no for each)
- Are there contradictions? (check)

**Pass Criteria**:
- Can you enumerate all states?
- Does every state have valid exits?
- Are all inputs handled?
- Are there contradictions? No.

If NO to any → Stop. Complete the thinking.

---

## STEP 4: Verification While Thinking (3-10 min)

**What**: Check logic coherence while thinking (not after).

**How**:
- Trace through one input completely
- Does it reach output? Yes/No
- Trace through boundary input
- Does it handle correctly? Yes/No
- Trace through invalid input
- Does it error safely? Yes/No

**Pass Criteria**:
- ✅ Happy path works
- ✅ Boundary cases work
- ✅ Error cases work
- ✅ Logic is coherent

If NO to any → Stop. Revise thinking.

---

## STEP 5: Gap Identification (1-5 min)

**What**: Make unknowns explicit before coding.

**How**:
- Are there any unresolved assumptions? (list them)
- Are there uncertain transitions? (mark UNVERIFIED)
- Are there incomplete designs? (mark INCOMPLETE)
- Have you logged all decisions?

**Pass Criteria**:
- All unknowns are explicit
- INCOMPLETE and UNVERIFIED are marked
- Decisions are documented
- Nothing is hidden/assumed

If NO to any → Stop. Make unknowns explicit.

---

## STEP 6: Proceed to Code (1 min)

**What**: You are ready to code.

**How**:
- All 5 steps above are DONE ✅
- Verification checklist is all green
- You can code mechanically
- Output will be correct

**Pass Criteria**:
- Can you answer YES to all 5 steps?
- Do you have complete thinking?
- Are you ready to code?

If YES to all → Proceed to implementation.  
If NO to any → Return to the relevant step.

---

## The Verification Checklist (From Step 4)

Use this before coding:

- ☐ Binary Completeness: All states mapped?
- ☐ Transition Coverage: Every state has valid exits?
- ☐ Input Handling: All input types covered?
- ☐ Output Correctness: Output follows from input+state?
- ☐ Gap Identification: All unknowns marked?
- ☐ Assumption Logging: Decisions documented?

**All 6 must be checked before you write code.**

---

## What This Prevents

- ❌ Half-thinking before coding
- ❌ Unverified assumptions  
- ❌ Missing edge cases
- ❌ Skipped error handling
- ❌ Unresolved contradictions

## What This Enables

- ✅ Complete thinking before code
- ✅ Logic verified while thinking
- ✅ All edge cases mapped
- ✅ Complete error handling
- ✅ Code works first try

---

## Timing

**Total: 5-10 minutes per file edit**

- Step 1: 2 minutes
- Step 2: 2 minutes
- Step 3: 3-15 minutes (varies by complexity)
- Step 4: 3-10 minutes
- Step 5: 1-5 minutes
- Step 6: 1 minute

**The time you spend here saves 10x time in debugging.**

---

**Next:** [Universal Mandate]({{ site.baseurl }}/zero-error/mandate/) → [Full Framework Details]({{ site.baseurl }}/zero-error/intro/)
