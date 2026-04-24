---
layout: default
title: Wiki Bug Report Template
permalink: /wiki-bug-report/
toc: true
status: published
category: Reference
tier: Support
difficulty: Beginner
reading_time: 5
entry_point: Site users
---

# Wiki Bug Report Template

## Purpose

This template ensures bug reports are complete, verifiable, and actionable. Each report becomes part of the wiki's audit trail.

---

## Bug Report Structure

### SECTION 1: Issue Classification (Required)

```
Type (choose one):
  ☐ Content Error — Page content is incorrect or outdated
  ☐ Format Error — Markdown, HTML, or styling issue
  ☐ Navigation Error — Links broken or missing
  ☐ Logic Error — Reasoning/explanation contradicts framework
  ☐ Missing Content — Intentional gap not marked INCOMPLETE
  ☐ Performance Issue — Site load/render problem
  ☐ Other — Describe: ______________
```

### SECTION 2: Location (Required)

```
Page Title: ________________________________
Page URL: /__________________/
Section/Heading: ________________________________
Line Number (if applicable): __________
```

### SECTION 3: What's Wrong (Required)

**Current State:**
```
Describe what you see right now (be specific):




```

**Expected State:**
```
Describe what should be there instead:




```

**Why It's Wrong:**
```
Explain the impact or why this matters:

Severity:
  ☐ Critical — Breaks framework understanding
  ☐ High — Causes incorrect decision
  ☐ Medium — Causes confusion
  ☐ Low — Minor improvement
```

### SECTION 4: Mandate Verification (Required)

**Does this issue violate the Universal Mandate?**

```
☐ No — Factual/formatting issue only
☐ Yes — Affects binary mapping
☐ Yes — Affects state transitions
☐ Yes — Affects input coverage
☐ Yes — Affects output correctness
☐ Yes — Missing gap identification
☐ Yes — Missing audit trail

If yes, explain:
```

### SECTION 5: Evidence (Required)

**Provide specific evidence:**

```
1. Quote the problematic text:
   "..."

2. Where to find correct information:
   - Reference: ______________
   - URL: ______________
   - Alternative source: ______________

3. Related pages affected (if any):
   - /__________________/
   - /__________________/
```

### SECTION 6: Reproduction (If applicable)

**Steps to reproduce the issue:**

```
1. Go to: /__________________/
2. Look for: ________________________________
3. Observe: ________________________________
4. Expected: ________________________________
```

### SECTION 7: Proposed Fix (Optional but helpful)

```
How would you fix this?

Option 1:
- Change: ________________________________
- To: ________________________________
- Reason: ________________________________

Option 2:
- Alternative approach: ________________________________

Questions for maintainer:
- ________________________________
```

### SECTION 8: Submitter Info (Required)

```
Name/Role: ________________________________
AI Instance / Human / Developer / Other: ________________________________
Contact/Reference: ________________________________
Date Submitted: ________________________________
```

---

## How to Submit a Bug Report

### Option 1: Structured Text (Copy & Use Template)

Copy the template above, fill it completely, and send to the wiki maintainer with subject:

```
[BUG] {Page Title} - {Brief Description}
```

Example:
```
[BUG] Universal Mandate - Requirement 2 typo
[BUG] Task Template - Phase 3 missing verification criteria
[BUG] Navigation - For-Builders link returns 404
```

---

### Option 2: GitHub Issues (If Integrated)

Use format:

```markdown
**Type**: [Content Error / Format Error / Navigation Error / Logic Error / Missing Content]
**Severity**: [Critical / High / Medium / Low]
**Page**: [page-name] → [section]

**Current**: [What's wrong]
**Expected**: [What should be there]
**Why**: [Why it matters]

**Evidence**:
- Reference: [source]
- Related pages: [links]

**Proposed Fix**: [Optional]
```

---

### Option 3: Issue Tracker Integration

If using issue tracker, ensure every bug report includes:
- [x] Type classification
- [x] Exact location (page + section)
- [x] Current vs Expected states
- [x] Mandate impact (if any)
- [x] Evidence with references
- [x] Proposed fix (if available)

---

## Bug Triage Criteria

### Immediate Fix Required (Critical)
- Framework violation detected
- Broken navigation (404s, dead links)
- Factually incorrect information that could cause wrong decisions
- Styling that prevents content readability

### Fix Soon (High Priority)
- Outdated information (but framework still valid)
- Typos in critical passages
- Missing cross-references
- Incomplete linking between related pages

### Schedule for Review (Medium)
- Formatting inconsistencies
- Clarity improvements
- Better examples needed
- Performance optimizations

### Consider for Future (Low)
- Style improvements
- UI enhancements
- Optional additional examples
- Organizational refinements

---

## What Happens After Submission

### Process Flow

```
BUG SUBMITTED
    ↓ (Triage: Is it valid?)
    → INVALID (Explanation sent back)
    → DUPLICATE (Linked to existing issue)
    → NEEDS INFO (Questions asked)
    ↓
    ACCEPTED (Scheduled for fix)
    ↓ (Fix prepared)
    → VERIFICATION (Tests/review)
    ↓
    FIXED (Deployed to wiki)
    ↓ (Confirmation)
    CLOSED (Audit logged)
```

### Response Timeline

| Priority | Response Time | Fix Time |
|----------|--------------|----------|
| Critical | 24 hours | 3 days |
| High | 3 days | 1 week |
| Medium | 1 week | 2 weeks |
| Low | 2 weeks | Monthly review |

### You'll Receive

1. **Acknowledgment** — Confirmation that bug was received
2. **Triage Result** — Classification and priority
3. **Status Updates** — If waiting for clarification or fix
4. **Resolution** — When bug is fixed with audit trail

---

## Quality Standards for Bug Reports

### ✅ Good Bug Reports
```
Title: [Formatting Error] Quick Reference Card - Table Alignment

Section: "The 8 Phases (IN ORDER)" table, line 42

Current: Table columns misaligned on mobile
Expected: Table should stack or use responsive layout
Evidence: Screenshot attached; affects at 375px width
Severity: Medium - still readable but looks broken
Proposed: Add CSS media query for table-stack

Status: ACCEPTED, Scheduled for next deployment
```

---

```
Title: [Logic Error] Pre-Action Checklist - Gate Definition Conflict

Section: "6 Steps Before Every Edit"

Current: "Verify all unknowns marked" but no explanation of what counts as "unknown"
Expected: Explicit list - INCOMPLETE, UNVERIFIED, ASSUMPTION, TBD with examples
Evidence: Three AI instances asked clarification; rule ambiguous
Severity: High - causes mandate interpretation gaps
Proposed: Add "Unknown Marker List" subsection with 5 concrete examples

Status: ACCEPTED, Assigned to maintainer
```

### ❌ Poor Bug Reports
```
"the wiki is wrong" ← No details, no location, no evidence

"Page 3 has a typo" ← Which page? Which typo?

"Fix the framework" ← Which framework? What's broken?

"The mandate section doesn't make sense" ← Why? What specifically?
```

---

## Bug Report Audit Trail

Every accepted bug report will be logged with:

| Field | Value | Example |
|-------|-------|---------|
| Report ID | Auto-assigned | BUG-2026-0423-001 |
| Type | Classification | Content Error |
| Severity | Priority | High |
| Status | Current state | In Progress |
| Submitted By | Source | Claude Instance #4 |
| Accepted Date | When approved | April 23, 2026 |
| Fixed Date | When deployed | April 26, 2026 |
| Verification | Did fix work? | ✅ Verified |
| Commit Hash | Change reference | abc1234... |

---

## Example: Complete Bug Report

```markdown
SUBJECT: [Logic Error] Universal Mandate - Requirement 2 missing transition definition

TYPE: Logic Error - Affects mandate interpretation
SEVERITY: High - Core framework affected

LOCATION:
- Page: Universal Mandate (/zero-error/mandate/)
- Section: "Requirement 2: Verification While Thinking"
- Lines: 47-51

CURRENT STATE:
"As you think, you MUST:
- Check for logical contradictions
- Look for missing branches
- Verify state consistency
- Ensure output correctness"

EXPECTED STATE:
"As you think, you MUST:
- Check for logical contradictions
- Look for missing branches
- Verify state consistency  
- Ensure output correctness
- [ADD: Define what "checked" means - how many checks required? What documentation?]"

WHY IT'S WRONG:
Two AI instances asked: "How do I know if I've checked enough?" 
The requirement is clear but the verification criteria are implicit.
This violates the mandate's own requirement for "explicit unknowns."

MANDATE IMPACT:
☐ Binary Completeness - Affected: Unclear states of "verification complete"
☐ Transition Coverage - Affected: Gap in how to move from "thinking" to "verified"
☐ Gap Identification - Missing: What counts as complete verification?

EVIDENCE:
Reference: "[For AI Instances](./for-ai/)" mentions "verify while thinking" 
but doesn't define verification criteria
Related: Pre-Action Checklist has explicit checklist (good model)
Source: Conversation logs show this ambiguity recurring

PROPOSED FIX:
Add subsection under Requirement 2:

"### Verification While Thinking: Explicit Checklist

Before moving from Phase 3 (Think) to Phase 4 (Verify), answer:
- ☐ Have you mapped all 0,1 state combinations? (Binary completeness)
- ☐ Does every state have valid transitions defined? (Transition coverage)
- ☐ Can every possible input be handled? (Input coverage)
- ☐ Does output follow logically from input+state? (Output correctness)
- ☐ Are all unknowns marked (INCOMPLETE/UNVERIFIED)? (Gap identification)
- ☐ Is your reasoning documented? (Audit trail)

All 6 must be YES before moving forward."

SUBMITTER:
- Name: Claude Instance #2
- Role: AI Verification
- Date: April 23, 2026

STATUS: Waiting for triage
```

---

## Links & Resources

- **[Universal Mandate](./zero-error/mandate/)** — What violations look like
- **[Verification Report](./wiki-verification/)** — Current state of wiki
- **[Quick Reference](./zero-error/quick-ref/)** — For context on frameworks
- **[Git Issues](https://github.com/your-repo/issues)** — Active tracking (if enabled)

---

**Last Updated**: April 23, 2026  
**Framework**: Universal Mandate  
**Status**: Active - Accepting bug reports  
**Maintainer**: Wiki maintainer [contact info]

---

## Quick Copy-Paste Template

Copy this and fill it:

```
TYPE: [Content/Format/Navigation/Logic/Missing/Performance/Other]
SEVERITY: [Critical/High/Medium/Low]

LOCATION: /__________________/ → Section: ________________

CURRENT: [What's wrong]

EXPECTED: [What should be there]

WHY: [Why it matters]

EVIDENCE: 
- Reference: [source]
- Quote: "..."
- Related: [links]

PROPOSED FIX: [Optional]

SUBMITTER: [Name/Role] - [Date]
```

Send to: [wiki-maintainer@example.com]  
Subject: `[BUG] {Page} - {Brief description}`
