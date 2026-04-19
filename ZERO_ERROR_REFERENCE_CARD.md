# 0-ERROR COMPUTE REFERENCE CARD

**Print this. Keep it visible. Follow it precisely.**

---

## BEFORE EVERY WORK SESSION

```bash
cd c:\Determined
python project_orientation.py          # Verify frameworks loaded
python pre_edit_verification.py        # Load complete context
```

---

## THE 6-STEP PRE-EDIT CHECKLIST

Apply this BEFORE editing EVERY file (4-14 minutes total):

```
[ ] STEP 1: Read Complete Context (2 min)
    What: Entire file you're editing
    Look for: Structure, patterns, dependencies
    Action: Understand before changing

[ ] STEP 2: Check for Existing Content (30 sec)
    Search: grep_search for similar patterns
    Verify: Not already implemented elsewhere
    Action: Avoid duplicates

[ ] STEP 3: Make Comprehensive Edit (3-5 min)
    Include: 3-5 lines BEFORE target
    Include: 3-5 lines AFTER target
    Match: Indentation exactly
    Use: multi_replace for parallel edits

[ ] STEP 4: Validate Syntax (30 sec)
    Python: No syntax errors, no bare except
    YAML: No duplicate keys
    JSON: Valid format
    Markdown: Complete markup
    Action: Run pre_commit_validator.py

[ ] STEP 5: Test If Applicable (1-5 min)
    Code: Run it, check for errors
    Config: Validate structure
    Docs: Check for broken references
    Action: Verify output is correct

[ ] STEP 6: Verify Git State (30 sec)
    Command: git status
    Verify: Only intended files changed
    Command: git diff (review changes)
    Command: pre_commit_validator.py (must pass)
    Action: Ready to commit
```

**Total: 4-14 minutes prevents debugging for HOURS.**

---

## THE DETERMINISTIC ENGINE (Your Reasoning Format)

When thinking through any problem:

```
STATE [unique_id]:
  OBSERVED: Facts directly stated/verified
  UNRESOLVED: Gaps or ambiguous elements (marked explicitly)
  TENSION: Explicit contradictions from OBSERVED facts only

CHOICES: Always exactly three
  A) MAINTAIN current behavior
  B) CHANGE to resolve tension
  C) AVOID (suppress) tension

TRANSITIONS: What happens next
  → Observable outcomes only
  → Direction of change (stability ↑ or ↓)
  → No explanation beyond observable facts

PARENT: Previous state_id
  Ensures full traceability
  No broken chains
  Fully auditable
```

**Key Rule**: Cannot resolve what's marked UNRESOLVED. Mark it and propagate.

---

## ERROR PREVENTION RULES (7 Systematic)

Before EVERY action:

1. **READ COMPLETE CONTEXT** — Understand structure before changing it
2. **CHECK FOR EXISTING CONTENT** — Avoid duplicates, verify not done
3. **MAKE COMPREHENSIVE EDIT** — 3-5 lines context before/after
4. **VALIDATE SYNTAX** — No Python/YAML/JSON/Markdown errors
5. **TEST IF APPLICABLE** — Code runs, config validates, output correct
6. **USE ALL TOOLS** — Validator, compliance checker, gate discovery
7. **VERIFY GIT STATE** — Clean, reviewed, safe to commit

---

## YOUR TOOLS (15 Total)

**Context/Framework:**
- read_file: Read file content
- grep_search: Search workspace
- semantic_search: Find conceptual matches
- memory: Persistent notes

**File Ops:**
- create_file: New file
- replace_string_in_file: Edit existing
- multi_replace_string_in_file: Parallel edits
- create_directory: Create folders

**Execution:**
- run_in_terminal: Execute commands
- get_errors: Check for syntax/lint errors
- file_search: Find files by pattern
- list_dir: List directory contents

**Code Analysis:**
- vscode_listCodeUsages: Find symbol references
- vscode_renameSymbol: Rename symbols precisely
- get_changed_files: View git changes

**Know your tools. Use before making assumptions.**

---

## DECISION LOGGING

Every decision logged to DECISION_LOG.jsonl:

```json
{
  "timestamp": "ISO-8601",
  "decision": "What was decided",
  "type": "Framework|FileAction|Error|Scope|Testing",
  "why": "Reasoning",
  "alternatives": ["opt1", "opt2"],
  "verification": "How verified",
  "tags": ["keywords"]
}
```

**All work is auditable. Opacity is threat. Transparency is safety.**

---

## AUTOMATION SUITE (Run Before Committing)

```bash
python automation_runner.py              # Full health check
python pre_commit_validator.py           # Syntax validation (must pass)
python duplicate_detector.py             # Find redundancy (optional)
python framework_compliance_checker.py   # Verify frameworks (must pass)
python gate_discovery_system.py          # Find gaps
python decision_logger.py                # Review decisions
```

---

## GIT WORKFLOW

```bash
# Check status
git status                  # What changed?
git diff                    # Review changes

# Stage and commit
git add -A                  # Stage all
git commit -m "..."        # Pre-commit hook runs validation
                            # Must pass all checks

# If validation fails
[Fix the issues noted]
git add -A
git commit -m "..."        # Retry commit
```

---

## QUICK REFERENCE (When Stuck)

**"How do I think about this?"**
→ Use the DETERMINISTIC ENGINE (STATE/CHOICE/TRANSITION)

**"What frameworks apply?"**
→ Check CRITICAL_THINKING_MASTER_INDEX.md

**"What tools do I have?"**
→ See AI_ENVIRONMENT_SELF_KNOWLEDGE.md

**"What do I do before editing?"**
→ The 6-STEP PRE-EDIT CHECKLIST (above)

**"Why does this matter?"**
→ Read PROJECT_ENTRY_GATE.md

**"How do I use all this?"**
→ See AI_PRE_EDIT_INTEGRATION_GUIDE.md

---

## TO REMEMBER

### What This Prevents
```
BEFORE: Think vaguely → Code → Errors → Debug
AFTER: Think completely → Verify → Code → Works
```

### The Single Error
I misclassified a sophisticated framework as a threat because I skipped context reading.

**This system makes that impossible.**

### Sophistication ≠ Threat
The frameworks are human-level reasoning formaliz.

Transparency is safety. Opacity is threat.

---

## STATUS CHECK

If you can answer these, you're ready:

1. [ ] What are the 7 error prevention rules?
2. [ ] Can you explain the 6-step pre-edit checklist?
3. [ ] What does UNRESOLVED mean in the deterministic engine?
4. [ ] How many tools do you have and what's their purpose?
5. [ ] What happens if pre-commit validation fails?

**If you can't answer all 5: Re-read the frameworks first.**

---

**Keep this visible. Use it every session. Follow it precisely.**

**Last Updated**: April 19, 2026  
**Valid**: Until frameworks change, then update immediately
