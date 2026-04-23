---
layout: default
title: Content Placement Rules - Deterministic Classification
permalink: /content-placement-rules/
description: "How to classify and place any new content in the proper help system"
toc: true
status: published
---

# Content Placement Rules: Deterministic Classification System

**Purpose**: When creating new content, use these rules to determine where it belongs in the proper help system structure.

---

## Rule System Overview

**5 Decision Points**:
1. **What system is this?** (Human Dev / 0-Error / Physics / Reference / Support)
2. **What tier is this?** (Entry / Foundation / Framework / Application / Reference / Tool)
3. **What's the primary purpose?** (Teach / Explain / Guide / Tool / Reference)
4. **Who's the audience?** (Beginner / Intermediate / Advanced / Expert / All)
5. **What does it depend on?** (Prerequisites)

**Classification leads to**: Proper folder, URL structure, navigation placement, page metadata

---

## Decision Tree

### STEP 1: Which System?

```
Is this about...

A) Human development, gates, help systems?
   → SYSTEM 1: Human Development (/gates/)
   
B) Computing, 0-Error frameworks, verification, tools?
   → SYSTEM 2: 0-Error Compute (/0-error/)
   
C) Physics, visualizations, animations, elections?
   → SYSTEM 3: Elections/Physics (/elections/)
   
D) Multiple systems or cross-cutting?
   → REFERENCE & INTEGRATION (/reference/)
   
E) Wiki maintenance, QA, bugs, status?
   → SUPPORT TOOLS (/tools/)
```

---

## SYSTEM 1 PLACEMENT RULES

**If answer is A: Human Development**

### STEP 2A: Which Tier in Human Development?

```
Is this...

A1) About why the framework matters, stakes, foundation problems?
    → FOUNDATION TIER (/gates/foundation/)
    Example: "Why Tier -1 is critical", "Stakes if we don't change"
    
A2) About identifying problems, analyzing help system failures?
    → PROBLEM ANALYSIS TIER (/gates/problems/)
    Example: "Help Systems as Gate-Skippers", "Goal-Blindness"
    
A3) About understanding the 10 gates themselves?
    → SOLUTION FRAMEWORK TIER (/gates/)
    Example: Individual gate pages, gate definitions, gate logic
    
A4) About applying gates to real domains?
    → APPLICATION TIER (/gates/applications/)
    Example: "Gates in Parenting", "Gates in Education", "Gates in Business"
    
A5) About case studies, evidence, deep research?
    → REFERENCE TIER (/gates/reference/)
    Example: "Systems that failed from skipped gates", research papers
```

### Decision Rules for System 1:

**URL Structure**:
```
/gates/                          = System 1 root
/gates/foundation/               = Foundation concepts
/gates/problems/                 = Problem analysis
/gates/universal-foundation/     = 10 gates overview
/gates/{gate-name}/              = Individual gate (1 per gate)
/gates/applications/{domain}/    = Domain applications
/gates/reference/                = Research/deep dives
```

**Prerequisites Mapping** (what comes before?):
```
Foundation Tier
    ↓ (must read first)
Problem Analysis Tier
    ↓ (must read second)
Solution Framework Tier (Universal Foundation)
    ↓ (choose from):
    - Individual Gate Pages, OR
    - Application Pages
    ↓
Reference Tier (optional, deeper)
```

**Metadata Template for System 1**:
```yaml
category: "Human Development"
system: 1
tier: [foundation|problems|framework|application|reference]
depends_on: [list of prerequisite pages]
entry_point: ["for-humans"] or ["for-builders"] or ["for-researchers"]
difficulty: [Beginner|Intermediate|Advanced|Expert]
reading_time: [X minutes]
```

**Completeness Check - System 1 Should Have**:
```
✓ 1 unified overview page
✓ 2-3 foundation pages
✓ 2-3 problem analysis pages
✓ 1 universal framework page
✓ 10 individual gate pages (one per gate)
✓ 10 application domain pages (parenting, education, therapy, etc.)
✓ 2-3 reference/research pages
✓ 1 complete integrated document

Total: 30+ pages
Status: Currently 8/30 (~27% complete)
```

---

## SYSTEM 2 PLACEMENT RULES

**If answer is B: 0-Error Compute**

### STEP 2B: Which Tier in 0-Error?

```
Is this...

B1) About WHY 0-Error matters, mandates, principles?
    → CONCEPTUAL TIER (/0-error/concept/)
    Example: "Why mandatory", "The mandate", "Core principles"
    
B2) About HOW to think correctly, frameworks, templates, checklists?
    → FRAMEWORK TIER (/0-error/frameworks/)
    Example: "8-Phase Task Template", "6-Step Checklist", "Verification"
    
B3) About tools that automate validation?
    → AUTOMATION TIER (/0-error/tools/)
    Example: "Validator", "Logger", "Detector", "Gap Finder"
    
B4) About actually using this in real projects?
    → INTEGRATION TIER (/0-error/integration/)
    Example: "Git hooks setup", "Workflow integration", "Troubleshooting"
```

### Decision Rules for System 2:

**URL Structure**:
```
/0-error/                        = System 2 root
/0-error/concept/                = Why it matters
/0-error/mandate/                = Mandatory requirements
/0-error/frameworks/             = How to think
/0-error/task-template/          = 8-phase workflow
/0-error/quick-ref/              = 1-page reference
/0-error/tools/                  = Automation tools
/0-error/validator/              = Specific tool
/0-error/logger/                 = Specific tool
/0-error/detector/               = Specific tool
/0-error/integration/            = Real-world usage
/0-error/git-hooks/              = Setup guide
/0-error/troubleshooting/        = Problem solving
```

**Prerequisites Mapping**:
```
Conceptual Tier (Why)
    ↓ (must read first)
Frameworks Tier (How to Think)
    ↓ (choose from):
    - Quick Reference, OR
    - Individual Framework Pages
    ↓
Automation Tier (Tools)
    ↓
Integration Tier (Real Usage)
```

**Metadata Template for System 2**:
```yaml
category: "0-Error Compute"
system: 2
tier: [concept|frameworks|tools|integration]
tool_type: [mandate|template|checklist|validator|logger|detector|runner] (if tools)
depends_on: [list of prerequisites]
entry_point: ["for-developers"]
difficulty: [Beginner|Intermediate|Advanced|Expert]
reading_time: [X minutes]
```

**Completeness Check - System 2 Should Have**:
```
✓ 1-2 conceptual pages
✓ 1 mandate page
✓ 1-2 framework pages
✓ 1 quick reference
✓ 6 tool pages (validator, logger, detector, framework-checker, gap-finder, runner)
✓ 1 integration guide
✓ 1 git hooks setup
✓ 1 troubleshooting/FAQ

Total: 15+ pages
Status: Currently 8/15 (~53% complete)
```

---

## SYSTEM 3 PLACEMENT RULES

**If answer is C: Physics/Elections**

### STEP 2C: Which Tier in Physics?

```
Is this...

C1) About learning the roadmap, physics foundation, key concepts?
    → FOUNDATION TIER (/elections/foundation/)
    Example: "Roadmap", "Whitepaper", "Key Concepts"
    
C2) About individual learning modules (Election 1, 2, 3, etc.)?
    → LEARNING MODULES TIER (/elections/)
    Example: "/elections/1-distinction/", "/elections/2-movement/", etc.
    
C3) About HOW to build, implement, code the visualizations?
    → IMPLEMENTATION TIER (/elections/implementation/)
    Example: "Animation tutorial", "Canvas techniques", "Code examples"
    
C4) About the big picture, cosmic implications, full integration?
    → INTEGRATION TIER (/elections/integration/)
    Example: "Cosmic unfolding", "Big picture implications"
```

### Decision Rules for System 3:

**URL Structure**:
```
/elections/                      = System 3 root
/elections/roadmap/              = Meta-roadmap
/elections/foundation/           = Physics foundation
/elections/whitepaper/           = Physics model
/elections/1-distinction/        = Election 1 (COMPLETE)
/elections/2-movement/           = Election 2 (NEEDS IMPL)
/elections/3-spirals/            = Election 3 (NEEDS IMPL)
/elections/4-direction/          = Election 4 (NEEDS IMPL)
/elections/5-time/               = Election 5 (NEEDS IMPL)
/elections/implementation/       = How to build
/elections/animation-tutorial/   = Step-by-step
/elections/integration/          = Cosmic unfolding
```

**Prerequisites Mapping**:
```
Foundation Tier (Roadmap + Physics)
    ↓ (must read first)
Individual Elections in Order (1 → 2 → 3 → 4 → 5)
    ↓
Implementation Tier (How to build)
    ↓
Integration Tier (Big picture)
```

**Metadata Template for System 3**:
```yaml
category: "Elections/Physics"
system: 3
tier: [foundation|learning_module|implementation|integration]
election_number: [1|2|3|4|5] (if learning module)
status: [complete|in_progress|planned] (if learning module)
depends_on: [list of prerequisites]
entry_point: ["for-researchers"] or ["for-builders"]
difficulty: [Beginner|Intermediate|Advanced|Expert]
reading_time: [X minutes]
```

**Completeness Check - System 3 Should Have**:
```
✓ 1 roadmap page
✓ 1 physics whitepaper
✓ 1-2 foundation pages
✓ 5 election pages (1 complete, 4 need implementation)
✓ 1 implementation guide
✓ 1 animation tutorial
✓ 1 integration/cosmic page

Total: 13+ pages
Status: Currently 9/13 (~69% complete)
Missing: Full implementation of Elections 2-5, tutorial page
```

---

## REFERENCE & INTEGRATION RULES

**If answer is D: Cross-System or Reference**

### STEP 2D: Which Reference Type?

```
Is this...

D1) About different learning paths and sequences?
    → LEARNING PATHS (/reference/learning-paths/)
    Example: "15-min overview", "2-hour intro", "1-week mastery"
    
D2) About terminology, Q&A, discovery?
    → DISCOVERY TOOLS (/reference/)
    Example: "Glossary", "FAQ", "Bibliography", "Case Studies"
    
D3) About connecting the three systems?
    → INTEGRATION (/reference/integration/)
    Example: "Binary foundation", "Verification methodology", "System map"
    
D4) About user types and their guided paths?
    → USER GUIDES (/reference/user-guides/)
    Example: "For humans guide", "For developers guide"
```

### Decision Rules for Reference:

**URL Structure**:
```
/reference/                      = Reference root
/reference/learning-paths/       = Guided sequences
/reference/glossary/             = All terms
/reference/faq/                  = Questions & answers
/reference/bibliography/         = Sources & citations
/reference/case-studies/         = Real examples
/reference/integration/          = Cross-system connections
/reference/user-guides/          = Role-based guides
```

**Metadata Template for Reference**:
```yaml
category: "Reference & Integration"
reference_type: [learning_path|glossary|faq|bibliography|case_study|integration|user_guide]
entry_point: [all|specific_user_types]
difficulty: [All] or [specific]
reading_time: [X minutes]
```

---

## SUPPORT TOOLS RULES

**If answer is E: Wiki Support/QA**

### STEP 2E: Which Support Type?

```
Is this...

E1) About testing the wiki itself, verification reports?
    → QA TOOLS (/tools/verification/)
    Example: "Mandate verification", "Link audit", "Structure check"
    
E2) About reporting problems, bugs, suggestions?
    → BUG REPORTING (/tools/bug-reporting/)
    Example: "Bug template", "Issue tracker", "Feature requests"
    
E3) About wiki health, metrics, dashboards?
    → STATUS & MONITORING (/tools/status/)
    Example: "Health dashboard", "Metrics", "Completion tracking"
```

### Decision Rules for Support:

**URL Structure**:
```
/tools/                          = Tools root
/tools/verification/             = QA reports
/tools/bug-reporting/            = Bug template
/tools/status/                   = Health dashboard
```

**Metadata Template for Support**:
```yaml
category: "Support & Maintenance"
support_type: [verification|bug_reporting|status_monitoring]
frequency: [ongoing|weekly|monthly|ad_hoc]
```

---

## Quick Reference: Decision Flowchart

```
NEW CONTENT EXISTS
    ↓
SYSTEM 1: Human Dev? → /gates/{tier}/{name}/
    ↓ No
SYSTEM 2: 0-Error? → /0-error/{tier}/{name}/
    ↓ No
SYSTEM 3: Physics? → /elections/{tier}/{name}/
    ↓ No
REFERENCE? → /reference/{type}/{name}/
    ↓ No
SUPPORT? → /tools/{type}/{name}/
    ↓ No
    ↓ (DOESN'T FIT)
    ↓
QUESTION: Does this belong in this wiki at all?
    YES → Create new category or integrate into existing
    NO → Archive separately or link externally
```

---

## Examples: Placing New Content

### Example 1: "Gate 1 - Foundation of Agency"

```
Q1: System? → A) Human development
Q2: Tier? → A3) About understanding the 10 gates
Q3: Purpose? → Teaching what Gate 1 is
Q4: Audience? → Intermediate level readers
Q5: Depends on? → Universal Foundation overview

PLACEMENT: /gates/foundation-of-agency/

URL: https://wiki.example.com/gates/foundation-of-agency/

METADATA:
category: "Human Development"
system: 1
tier: framework
depends_on: ["/gates/universal-foundation/"]
entry_point: ["for-humans", "for-builders"]
difficulty: Intermediate
reading_time: 12 minutes

NEXT PAGE: /gates/responsibility-attribution/
PREVIOUS PAGE: /gates/universal-foundation/
```

### Example 2: "Setting Up Git Hooks for 0-Error"

```
Q1: System? → B) 0-Error Compute
Q2: Tier? → B4) About using this in real projects
Q3: Purpose? → Step-by-step implementation guide
Q4: Audience? → Intermediate (developers)
Q5: Depends on? → Pre-commit validator, Integration guide

PLACEMENT: /0-error/integration/git-hooks/

URL: https://wiki.example.com/0-error/integration/git-hooks/

METADATA:
category: "0-Error Compute"
system: 2
tier: integration
depends_on: ["/0-error/validator/", "/0-error/integration/"]
entry_point: ["for-developers"]
difficulty: Intermediate
reading_time: 15 minutes

NEXT PAGE: /0-error/troubleshooting/
PREVIOUS PAGE: /0-error/integration/
```

### Example 3: "Why Binary Thinking Appears in All Systems"

```
Q1: System? → D) Cross-system/Reference
Q2: Type? → D3) About connecting the three systems
Q3: Purpose? → Teaching unified concept
Q4: Audience? → Advanced (connections)
Q5: Depends on? → All three system foundations

PLACEMENT: /reference/integration/binary-foundation/

URL: https://wiki.example.com/reference/integration/binary-foundation/

METADATA:
category: "Reference & Integration"
reference_type: integration
entry_point: ["all"] (appeals to all user types)
difficulty: Advanced
reading_time: 20 minutes

CONNECTS TO:
- /gates/universal-foundation/ (Gate 4 - Pattern Recognition)
- /0-error/frameworks/ (Binary logic verification)
- /elections/foundation/ (Quantum binary distinction)
```

---

## Validation Checklist

Before publishing any new page, verify:

- [ ] **System identified** - Does it belong to System 1, 2, 3, Reference, or Support?
- [ ] **Tier identified** - Is the tier (foundation/framework/application/integration) correct?
- [ ] **URL correct** - Does URL follow semantic structure for its tier?
- [ ] **Metadata complete** - All fields filled (title, description, category, tier, difficulty, time, depends_on)?
- [ ] **Prerequisites exist** - Do all pages in "depends_on" actually exist?
- [ ] **Next/Previous linked** - Does page link to next logical page?
- [ ] **Cross-referenced** - Are related pages from other systems linked?
- [ ] **Discoverable** - Is it linked from at least 2-3 other pages?
- [ ] **No orphans** - Is this page actually findable from root?
- [ ] **Consistent terminology** - Uses terms from /reference/glossary/?

---

## Conclusion: Use These Rules for All New Content

**Benefit**: 
- Automatic placement (no guessing)
- Consistent structure (professional quality)
- Complete navigation (no dead ends)
- Proper hierarchy (progressive learning)

**Result**: Help system grows coherently instead of chaotically

