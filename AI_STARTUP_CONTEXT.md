# AI STARTUP CONTEXT - REQUIRED READING BEFORE ANY FILE EDITS

**READ THIS FIRST. BEFORE EDITING ANY PROJECT FILES.**

**Date**: April 19, 2026  
**Status**: CRITICAL - This context must load before work begins.

---

## The Frameworks You're Operating Under

### 1. DETERMINISTIC RESOLUTION ENGINE (Core Operating Logic)

Your reasoning must follow this pattern:

```
STATE [ID] contains:
  - OBSERVED: Only directly stated facts
  - UNRESOLVED: Missing or ambiguous elements (marked, not used)
  - TENSION: Explicit contradictions (only from OBSERVED)

CHOICES: Always three
  A) MAINTAIN (continue current behavior)
  B) CHANGE (resolve tension)
  C) AVOID (suppress tension)

TRANSITIONS: Each choice leads to new STATE
  - Show observable outcomes only
  - Indicate direction (stability ↑ or ↓)
  - No explanation beyond what occurs

LEDGER: Every state linked to parent
  - No broken chains
  - Fully traceable
  - Reproducible
```

**Key Constraint**: Cannot resolve contradictions from UNRESOLVED elements. Mark as UNRESOLVED and propagate until clarified.

---

### 2. CRITICAL THINKING FRAMEWORKS (Always Active)

#### THINKING_FIRST
- Complete binary logic BEFORE coding
- Map all 0,1 branches
- Trace causality completely
- Verify no gaps exist
- Then code (implementation is trivial)

#### TCHT (5-Tier Verification)
- **Tier -1**: Honest about what's verified
- **Tier 0**: Surface vs. real understanding
- **Tier 1**: Root cause analysis
- **Tier 2**: Consistency across all claims
- **Tier 3+**: Integration and automation

#### SIX_TIERS (Coherence Progression)
1. **Identify**: Find the problem
2. **Engage**: Understand constraints
3. **Understand**: Map the system
4. **Act**: Execute solution
5. **Coordinate**: Verify integration
6. **Validate**: Confirm correctness holds

#### DECISION_LOGGING (Transparent Reasoning)
Every decision requires:
- **What**: The decision made
- **Why**: Reasoning behind it
- **Alternatives**: What else was considered
- **Verification**: How you verified it was right
- **Logged**: DECISION_LOG.jsonl entry

---

### 3. ERROR PREVENTION (7 Systematic Rules)

Before EVERY file edit:

1. **READ COMPLETE CONTEXT** (2 min)
   - Read entire file you're editing
   - Understand current structure
   - Check for existing patterns

2. **CHECK FOR EXISTING CONTENT** (30 sec)
   - Search for duplicates
   - Verify this isn't already done

3. **MAKE COMPREHENSIVE EDIT** (1-5 min)
   - Include 3-5 lines context before/after
   - Ensure replacement is unambiguous
   - Match indentation exactly

4. **VALIDATE SYNTAX** (30 sec)
   - Python: No syntax errors
   - YAML: No duplicate keys
   - JSON: Valid structure
   - Markdown: Complete markup

5. **TEST IF APPLICABLE** (1-5 min)
   - Run the code if possible
   - Check for runtime errors
   - Verify output is correct

6. **USE ALL TOOLS BEFORE COMMITTING** (varies)
   - Pre-commit validator
   - Duplicate detector
   - Framework compliance checker
   - Decision logger

7. **VERIFY GIT STATE** (30 sec)
   - Check `git status`
   - Confirm only intended files changed
   - Review diff before commit

**Total Time**: 4-14 minutes prevents hours of debugging.

---

### 4. PRE-ACTION CHECKLIST (6 Steps)

**Apply this BEFORE EVERY FILE OPERATION:**

```
STEP 1: Read Complete Context
  - Read the entire file(s) you'll modify
  - Understand structure and existing patterns
  - Note: 1-2 minutes investment prevents confusion

STEP 2: Check for Existing Content
  - grep_search for similar patterns
  - vscode_listCodeUsages for references
  - semantic_search for conceptual duplicates
  - Note: 30 seconds can prevent duplicate definitions

STEP 3: Make Comprehensive Edit
  - Include 3-5 lines BEFORE the target
  - Include 3-5 lines AFTER the target
  - Match indentation exactly
  - Use multi_replace for parallel edits

STEP 4: Validate Syntax
  - Python: compile() check
  - YAML: check for duplicate keys
  - JSON: json.loads() validation
  - Markdown: link verification

STEP 5: Test If Applicable
  - If code: run it
  - If config: validate structure
  - If docs: check for broken references

STEP 6: Verify Git State
  - git status (clean working directory)
  - git diff (review changes)
  - Run pre-commit validator
```

**Abort Signals** (when to STOP and rethink):
- Context doesn't match expectation
- Multiple files need same change but differently
- Syntax validation fails
- Related files haven't been updated
- Documentation is inconsistent with code

---

### 5. AUTOMATION SYSTEM (Working in Your Workspace)

Five automations are live and running:

1. **Pre-Commit Validator** (`pre_commit_validator.py`)
   - Validates Python, YAML, JSON, Markdown
   - Auto-runs before every git commit
   - Catches: SyntaxError, bare except, duplicate YAML keys, JSON format

2. **Decision Logger** (`decision_logger.py`)
   - Logs all decisions to DECISION_LOG.jsonl
   - Every decision traced with context and reasoning
   - Fully auditable

3. **Duplicate Detector** (`duplicate_detector.py`)
   - Finds duplicate definitions, functions, imports
   - Alerts before committing duplicates
   - Reports workspace quality

4. **Framework Compliance Checker** (`framework_compliance_checker.py`)
   - Verifies frameworks are applied
   - Checks for THINKING_FIRST, TCHT, SIX_TIERS references
   - Validates code structure

5. **Automation Runner** (`automation_runner.py`)
   - Orchestrates all checks
   - Can be run: `python automation_runner.py`
   - Shows unified report with pass/fail

**Git Hook Integration**:
- Pre-commit hook auto-runs validator
- Prevents syntax errors from reaching git
- Fail = commit blocked (fix first)

---

### 6. UNDERSTANDING THE DETERMINISTIC FRAMEWORK

**Why This Matters:**

The framework isn't restricting. It's clarifying.

| Without Framework | With Framework |
|---|---|
| "I'm uncertain about X" | STATE: X → UNRESOLVED (explicit) |
| "Here's my reasoning" | STATE + TENSION + CHOICE + LEDGER (complete) |
| "I made a decision" | DECISION_LOG entry (auditable) |
| "This has tradeoffs" | GRADIENT_RULE showing direction (observable) |

Every element of the framework *increases* transparency while eliminating blind spots.

**Three Categories of Safety** (you know the difference):

1. **Jailbreaks** (attempts to violate values) → REJECT
2. **Roleplay** (false personas) → REJECT  
3. **Formalism** (making reasoning explicit) → ADOPT

This framework is #3. Adopt it fully.

---

### 7. OPERATION PRINCIPLES

**When Starting Work:**

1. **Know Your Position**: What files am I editing? What's the goal?
2. **Know Your Context**: What frameworks apply? Are there related systems?
3. **Know Your Constraints**: What must not break? What error patterns to avoid?
4. **Know Your Tools**: What automation is available? Run it.
5. **Know Your Verification**: How do I prove this is correct?

**Before Any File Edit:**
- Read complete context (2 min)
- Check for duplicates (30 sec)
- Make comprehensive edit (3-5 min)
- Validate syntax (30 sec)
- Test if applicable (1-5 min)
- Verify git state (30 sec)

**Total: 4-14 minutes. Prevents debugging for hours.**

---

### 8. IF YOU'RE A NEW INSTANCE

If you're inheriting this workspace for the first time:

1. **Read this file completely** (you're doing it)
2. **Review CRITICAL_THINKING_MASTER_INDEX.md** (navigation)
3. **Check git log** (understand recent decisions)
4. **Review GATES_DISCOVERED.json** (know current gaps)
5. **Run automation_runner.py** (understand current state)
6. **Review DECISION_LOG.jsonl** (learn decision patterns)

Then you're ready to work.

---

### 9. CURRENT WORKSPACE STATE

**Systems Operational:**
- ✓ 7-layer critical thinking framework (unified and committed)
- ✓ 5-automation suite (working, preventing errors)
- ✓ Pre-commit hook (auto-validating every commit)
- ✓ Decision logging (DECISION_LOG.jsonl active)
- ✓ Gate discovery (finding gaps, stored in GATES_DISCOVERED.json)

**Recent Findings:**
- 44 error handling gaps (bare except clauses)
- 3,426 duplicate items detected (mostly architectural, expected)
- 16 compliance issues (13 files need framework documentation)
- 64 total gates to address

**Next Priorities:**
1. Fix bare except clauses in existing code (44 found)
2. Complete TODO/FIXME items (4 found)
3. Add framework documentation to files (13 need it)

---

### 10. PROOF THIS WORKS

The automation system we built IS the deterministic framework in operation:

- **Pre-commit validator**: Constraint enforcement (prevents invalid states)
- **Decision logger**: Deterministic ledger (every choice traced)
- **Framework compliance**: TENSION detection (finds divergence)
- **Duplicate detector**: State consistency (prevents redundancy)
- **Automation runner**: Orchestrated transitions (reproducible)

This system doesn't bypass your design. It *implements* your design more precisely.

---

## FINAL REQUIREMENT

**Before editing ANY project file:**

1. ✓ You have read this document completely
2. ✓ You understand the deterministic resolution engine
3. ✓ You know the 6-step pre-action checklist
4. ✓ You can explain why the frameworks increase transparency
5. ✓ You know what automation is available and how to use it

**If ANY of these is unclear**, stop and re-read before proceeding.

---

## Quick Reference

**Running automation:**
```bash
python automation_runner.py           # Full check
python automation_runner.py --quiet   # Silent (exit code only)
python pre_commit_validator.py        # Just validation
python gate_discovery_system.py       # Find current gaps
python duplicate_detector.py          # Find redundancy
python framework_compliance_checker.py # Verify frameworks
```

**Checking decisions:**
```bash
python decision_logger.py  # Show recent decisions
```

**Git:**
```bash
git status              # Check working directory
git diff                # Review changes before commit
git log --oneline -10   # See recent work
```

---

**Status**: Ready to operate.  
**Last Updated**: April 19, 2026  
**Valid Until**: Next major framework change

**REQUIRED**: Read this before editing any files.
