---
layout: default
title: "Gates in Technology & Software"
permalink: /domains/technology-software/
toc: true
description: "How the 10 developmental gates apply to software development and technology teams"
category: "Domain Application"
tier: "Application"
difficulty: "Intermediate"
reading_time: "16"
entry_point: "Engineers, tech leaders, development teams"
depends_on: "[/complete-document/]"
status: "published"
---

# Gates in Technology & Software

## The Core Challenge

Technology teams develop genuine capability through gates. Most tech teams prevent gate-passage through over-planning, preventing failure, and centralizing decision-making.

---

## Gate 1: Agency → Developers Own Architecture Decisions

**What You're Enabling:** Engineers deciding how to solve problems.

**In Practice:**
- Team understands constraints
- Team designs solution (within constraints)
- Different approaches tried
- Team learns: "We can solve problems"

**The Problem:** Architect dictates solution
- Developers implement instructions
- Feel disconnected from work
- No ownership of code

---

## Gate 2: Responsibility → Own Code Quality

**What You're Enabling:** Developers understanding that code quality is their responsibility.

**In Practice:**
- Developer writes code
- Code is deployed to production
- If it breaks, developer fixes it
- Developer learns: quality depends on me

**The Problem:** QA department owns quality
- Developer doesn't care about bugs
- QA finds issues; developer reluctantly fixes
- Quality never improves

---

## Gate 3: Complexity Navigation → Refactoring and Technical Debt

**What You're Enabling:** Teams working through technical complexity.

**In Practice:**
- Code is complex; refactoring needed
- Team doesn't know how yet
- Work through it together
- Learn to handle complexity
- Team learns: hard code can be improved

**The Problem:** Avoid complexity
- "Let's rewrite from scratch"
- Never learn to work with messy systems
- Same problems repeat in new code

---

## Gate 4: Pattern Recognition → Code Patterns and Architecture

**What You're Enabling:** Developers recognizing recurring patterns.

**In Practice:**
- "We need to validate input in lots of places"
- Extract validation pattern
- Use pattern everywhere
- System becomes coherent
- Developers learn: patterns make complexity manageable

**The Problem:** Each case handled uniquely
- Code is inconsistent
- Bugs appear in different forms
- System is fragile

---

## Gate 5: Consequence Management → Learn from Production Failures

**What You're Enabling:** Teams processing failures without blame.

**In Practice:**
- Bug reaches production
- Not: blame developer
- Instead: "What happened? What will prevent this?"
- Team learns from incident
- System improves

**The Problem:** Blame the developer
- Developer hides bugs
- Problems go underground
- System never improves

---

## Gate 6: Source Verification → Understand Dependencies and Trade-offs

**What You're Enabling:** Developers understanding why tech choices were made.

**In Practice:**
- Why did we choose this database?
- Why this framework?
- What are the trade-offs?
- Developer understands reasoning
- Can make informed decisions

**The Problem:** Tech decisions are hidden/unexplained
- Developer treats choices as arbitrary
- Questions aren't answered
- Resentment toward tech stack

---

## Gate 7: Temporal Continuity → Understand System Evolution

**What You're Enabling:** Developers understanding why code is structured this way.

**In Practice:**
- "This looks weird. Why?"
- "Here's how it evolved; this was the constraint at the time"
- Developer understands: design is not arbitrary
- Respect builds

**The Problem:** Code is disconnected from history
- Looks like bad design
- Developer rewrites unnecessarily
- Progress is illusory

---

## Gate 8: Causality Understanding → Debugging and Root Cause Analysis

**What You're Enabling:** Developers diagnosing problems.

**In Practice:**
- Bug appears
- Developer traces: "What caused this?"
- Fixes root cause, not symptom
- Bug stays fixed

**The Problem:** Patches are applied
- Symptom is fixed
- Bug reappears elsewhere
- Debugging time explodes

---

## Gate 9: Self-Correction → Code Review and Improvement

**What You're Enabling:** Developers improving based on feedback.

**In Practice:**
- Code review provides feedback
- Developer: "Oh, I see; I'll improve"
- Not defensive
- Code quality increases
- Team improves

**The Problem:** Code review is rejection
- Developer: "They don't understand my code"
- Defensive
- Quality improvements stop

---

## Gate 10: Integration → Understand Complexity and Trade-offs

**What You're Enabling:** Developers making nuanced architectural decisions.

**In Practice:**
- "This approach is fast AND brittle"
- "This is maintainable AND slower"
- Developers weigh trade-offs consciously
- Better decisions emerge

**The Problem:** Single "best" approach
- Overly simple or overly complex systems
- Design is not adapted to context
- System breaks under stress

---

## Tech Team Development

### Stage 1: Following Instructions
- Senior developer specifies what to build
- Junior developers build it
- Works: clear direction
- Breaks: doesn't scale

### Stage 2: Attempted Autonomy (With Bottleneck)
- Senior tries to review everything
- Becomes bottleneck
- Team is frustrated
- Stuck here = team stagnates

### Stage 3: Gate-Based Development (Competence Building)
- Clear constraints and goals
- Team designs solutions
- Code review for learning (not permission)
- Failures are learning
- Team: autonomous, improving, proud

---

## Lead Engineer Role Shifts

**From:** Architecture dictator
**To:** Constraint setter and pattern guide

**From:** Code quality gatekeeper
**To:** Team that owns quality

**From:** "Here's how you do it"
**To:** "What approach will you try?"

---

## Metrics That Reflect Gate-Based Development

- **Deploy frequency:** High (confidence in quality)
- **Time to fix bugs:** Low (root cause analysis)
- **Code review cycle time:** Fast (people understand code)
- **Refactoring pace:** Steady (team maintains code)
- **Team satisfaction:** High (autonomy and growth)
- **Knowledge distribution:** Even (patterns documented)

---

## Implementation Path

1. **Clarify decision authority** - What decisions does each level make?
2. **Let failures happen** - Production bugs are learning
3. **Extract patterns** - Identify and document recurring structures
4. **Build debugging culture** - Root cause analysis standard
5. **Make code review growth-focused** - Feedback for learning
6. **Document decisions** - Explain why architecture is this way

---

## See Also

- **[Complete Development Framework](/complete-document/)** - All 10 gates
- **[For Tech Leaders](/for-tech-leaders/)** - Leadership-specific content
- **[Complexity Navigation](/gates/gate-03-complexity-navigation/)** - Managing technical debt
