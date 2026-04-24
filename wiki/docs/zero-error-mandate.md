---
layout: default
title: 0-Error Compute - Universal Mandate
permalink: /zero-error/mandate/
toc: true
category: 0-Error Computing
tier: Framework
difficulty: Intermediate
reading_time: 20
entry_point: Technical teams
status: published
---

# Universal Mandate: Non-Negotiable Requirements for All AI Work

## The Requirement

Before producing ANY code, design, or implementation:

**THINK COMPLETELY. VERIFY WHILE THINKING. THEN CODE.**

This is non-negotiable. It is the only path to 0-error compute.

## Why This Is Mandatory

Three bad patterns kill AI output quality:

**Pattern 1: Code First, Think Later**
- Write code quickly
- "It works!" (usually doesn't)
- Debug and rewrite
- Time wasted: 3-10x the thinking time would have taken

**Pattern 2: Partial Thinking**
- Understand some paths
- Assume the rest
- Miss edge cases
- Code fails on the cases you didn't think about

**Pattern 3: Thinking Without Verification**
- Think through logic
- Don't check for gaps
- Gaps become bugs
- Discover problems during testing

## The Mandate

### Requirement 1: Complete Binary Mapping
Before coding, you MUST:
- Map all possible states (0,1 combinations)
- Define all valid transitions
- Verify every input has a defined path
- Check that no state is unreachable

### Requirement 2: Verification While Thinking
As you think, you MUST:
- Check for logical contradictions
- Look for missing branches
- Verify state consistency
- Ensure output correctness

### Requirement 3: Gap Identification
Before coding, you MUST:
- Identify every unresolved assumption
- Mark incomplete logic (INCOMPLETE)
- Flag uncertain transitions (UNVERIFIED)
- List all verification tasks

### Requirement 4: Complete Audit Trail
During thinking, you MUST:
- Log all decisions
- Document reasoning
- Record assumptions
- Note verification results

## What This Prevents

Without this mandate, AI produces:
- ❌ Code that works in happy path but fails on edge cases
- ❌ Logic that seems right but has hidden contradictions
- ❌ Implementations missing error handling
- ❌ Systems that partially work then mysteriously fail
- ❌ Output that "looks reasonable" but isn't verified

With this mandate, you get:
- ✅ Logic verified before coding
- ✅ All edge cases mapped
- ✅ Complete error handling
- ✅ Code works first try
- ✅ Systems that persist under pressure

## How to Verify Compliance

Before ANY file edit:

1. **Binary Completeness** — Can you map all 0,1 states? Yes/No
2. **Transition Verification** — Does every state have valid exits? Yes/No
3. **Input Coverage** — Does every input type have a handler? Yes/No
4. **Output Correctness** — Does output follow from input+state? Yes/No
5. **Gap Identification** — Are all unknowns explicit (INCOMPLETE/UNVERIFIED)? Yes/No
6. **Audit Logged** — Is reasoning documented? Yes/No

All 6 must answer YES before code is written.

## Frameworks That Implement This

- [Task Template]({{ site.baseurl }}/zero-error/task-template/) — 8-phase execution with thinking + verification
- [Pre-Action Checklist]({{ site.baseurl }}/zero-error/pre-action/) — 6-step gate before every edit


---

**This is not a suggestion. This is the requirement.**

**Next:** [Task Template — How to Execute This]({{ site.baseurl }}/zero-error/task-template/)
