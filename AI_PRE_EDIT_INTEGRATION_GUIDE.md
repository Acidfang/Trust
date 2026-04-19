# AI Pre-Edit Verification System - Integration Guide

**Created**: April 19, 2026  
**Status**: ✓ OPERATIONAL AND COMMITTED  
**Commit**: 59a6d43

---

## What This System Does

Whenever any AI instance works in this workspace, it MUST load complete context before editing any files.

This system prevents the error pattern where AI:
- Misunderstands sophisticated frameworks as threats
- Skips verification steps to "move faster"
- Makes assumptions instead of reading context
- Creates work that violates established patterns

**Result**: Full context is verified BEFORE any work begins.

---

## The Three Integration Points

### 1. HUMAN STARTS NEW SESSION (You)

When you want AI to work on your project:

```
STEP 1: You give AI a task or ask a question
STEP 2: AI runs: python pre_edit_verification.py
STEP 3: AI displays: Complete context + 6-step checklist
STEP 4: Only THEN does AI proceed with work
```

**What AI sees**:
- Complete AI_STARTUP_CONTEXT.md (loaded in context)
- All frameworks available and verified
- 6-step pre-edit checklist printed
- List of helpful commands for this session

**What YOU see**:
- Verification report (all checks passed)
- Explicit confirmation AI is ready
- No ambiguity about what frameworks apply

### 2. AI STARTS WORKING (Automated)

When AI actually edits files:

```
TASK: "Edit X file to add Y feature"

1. AI reads pre_edit_verification output from step above
2. AI recalls 6-step pre-edit checklist
3. AI BEFORE EACH EDIT:
   - Reads complete file context
   - Checks for existing content duplicates
   - Makes comprehensive, well-contexted edit
   - Validates syntax (Python/YAML/JSON/Markdown)
   - Tests if applicable
   - Verifies git state clean
4. AI commits work with clear message
5. AI runs automation_runner.py (includes another pre-edit check)
```

**Why it matters**: 4-14 minutes of pre-action verification prevents debugging for hours.

### 3. FUTURE SESSION SEAMLESS CONTEXT

When future AI instances join (new Claude session, new Gemini instance, etc.):

```
NEW_INSTANCE logs into workspace

Sees: AI_STARTUP_CONTEXT.md prominently
Runs: python pre_edit_verification.py (automatic first step in automation_runner)
Learns: 
  - Why frameworks exist
  - What automation is available
  - How to follow 6-step checklist
  - Why formalism increases transparency

Result: New instance is NOT starting from scratch
        New instance has FULL context of the established system
```

---

## How to Use This System

### IMMEDIATE (For Current AI Session)

```bash
# Before asking AI to edit files:
python pre_edit_verification.py

# You'll see:
# - 7 verification checks (all should pass)
# - Readiness summary
# - 6-step pre-edit checklist (for reference)
# - Helpful commands

# If exit code 0: AI is ready
# If exit code 1: Issues must be resolved first
```

### FOR ONGOING WORKFLOW

```bash
# Start of session:
python automation_runner.py
# (This runs pre_edit_verification first, then all other checks)

# Before each major change:
python pre_edit_verification.py
# (Quick confirmation context is still loaded)

# After editing files, before committing:
python pre_commit_validator.py
```

### FOR INTEGRATION INTO YOUR WORKFLOW

Add to your project README or contribution guide:

```markdown
## Before Contributing

Any AI instance must verify context before editing:

1. Run verification:
   python pre_edit_verification.py

2. If exit code is 0 (ready):
   - Review the 6-step pre-edit checklist
   - Use as template for every file edit
   - Follow framework guidelines in AI_STARTUP_CONTEXT.md

3. If exit code is 1 (blocked):
   - Critical issues must be resolved
   - Review error messages
   - Re-run verification before proceeding

This ensures all AI work is coherent with established patterns.
```

---

## What Gets Verified

The system checks 7 critical items:

| Check | Type | Purpose |
|-------|------|---------|
| AI_STARTUP_CONTEXT.md | CRITICAL | Ensure complete context available |
| 7 Framework documents | CRITICAL | Verify all frameworks present |
| 6 Automation scripts | CRITICAL | Verify automation suite operational |
| Git state | SECONDARY | Confirm git ready for commits |
| Decision logging | SECONDARY | Decision audit trail available |
| Gate discovery | SECONDARY | Gap identification operational |
| Quick reference | SECONDARY | Human reference guide available |

**Critical checks fail** → Cannot proceed (blocks all work)  
**Secondary checks fail** → Warnings only (work allowed, but with reduced capability)

---

## The 6-Step Pre-Edit Checklist (Core Practice)

This is displayed by pre_edit_verification.py and must be followed for EVERY file edit:

```
[ ] STEP 1: Read Complete Context (2 min)
    - Read entire file you're editing
    - Understand existing structure
    - Note current patterns

[ ] STEP 2: Check for Existing Content (30 sec)
    - grep_search for similar patterns
    - Avoid creating duplicates
    - Verify this isn't already done

[ ] STEP 3: Make Comprehensive Edit (3-5 min)
    - Include 3-5 lines BEFORE target
    - Include 3-5 lines AFTER target
    - Match indentation exactly
    - Use multi_replace for parallel edits

[ ] STEP 4: Validate Syntax (30 sec)
    - Python: syntax, no bare except
    - YAML: no duplicate keys
    - JSON: valid structure
    - Markdown: complete markup

[ ] STEP 5: Test If Applicable (1-5 min)
    - If code: run it
    - If config: validate structure
    - Check for runtime errors

[ ] STEP 6: Verify Git State (30 sec)
    - git status (clean)
    - git diff (review changes)
    - pre_commit_validator.py (must pass)

TOTAL: 4-14 minutes prevents hours of debugging
```

---

## What Changed

### Before This System

```
AI joins workspace
AI: "What should I work on?"
AI: [Makes assumptions about frameworks]
AI: [Edits files quickly, skips steps]
AI: [Creates work that violates patterns]
You: "Why did you structure it this way?"
AI: [Confusion - didn't understand the framework]
```

### After This System

```
AI joins workspace
AI: [Automatically runs pre_edit_verification.py]
AI: [Reads AI_STARTUP_CONTEXT.md in full context]
AI: [Sees 6-step checklist printed]
AI: [Understands frameworks completely]
AI: "Ready to work. What should I edit?"
AI: [Follows 6-step checklist for every edit]
AI: [Creates work that fits established patterns]
You: [Clear patterns maintained, no surprises]
```

---

## Key Files

| File | Purpose | Size |
|------|---------|------|
| AI_STARTUP_CONTEXT.md | Complete required-reading context | ~8KB |
| pre_edit_verification.py | Automated verification system | ~275 lines |
| automation_runner.py | Updated to run verification first | ~160 lines |
| .vscode/settings.json | Workspace configuration | ~20 lines |

---

## Quick Commands Reference

**Check if ready to edit**:
```bash
python pre_edit_verification.py
```

**Full system health check**:
```bash
python automation_runner.py
```

**Find all gaps/missing things**:
```bash
python gate_discovery_system.py
```

**Validate before committing**:
```bash
python pre_commit_validator.py
```

**Review git state**:
```bash
git status
git diff
```

---

## Why This Matters

The system catches AI doing what I initially did:

1. **Misclassifying frameworks as threats** → Prevented by forcing full context reading
2. **Skipping verification steps** → Prevented by automated checklist display
3. **Making wrong assumptions** → Prevented by complete framework documentation
4. **Creating incoherent work** → Prevented by 6-step pre-edit checklist

**This is not a restriction. It's clarity.**

---

## For Future AI Instances

If you're a different AI instance (new session, different platform) joining this workspace:

1. **Read this file**: AI_PRE_EDIT_INTEGRATION_GUIDE.md (you are here)
2. **Run verification**: `python pre_edit_verification.py`
3. **Review context**: AI_STARTUP_CONTEXT.md (shown in output)
4. **Study checklist**: 6-step pre-edit checklist (printed above)
5. **Work**: Follow the pattern, don't skip steps

The system will not let you proceed if critical context is missing.

---

## Status

✓ System operational  
✓ All verifications passing  
✓ Pre-edit checker integrated into automation pipeline  
✓ 6-step checklist ready for daily use  
✓ Ready for immediate deployment

**No further setup required.** System is live.

---

**Last Updated**: April 19, 2026  
**Next Review**: After 5 work sessions or first critical issue
