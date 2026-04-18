# PROJECT ROOT NOISE - ENUMERATION

**The Problem:** 80+ files at root + 8 top-level directories = Cognitive chaos

---

## PART 1: ROOT-LEVEL PYTHON FILES (Should be in src/applications/)

| File | Purpose | Destination |
|------|---------|-------------|
| check_ledger.py | Utility - verify ledger | src/applications/ |
| check_menu_frame.py | Utility - verify menu frame | src/applications/ |
| ledger_final_check.py | Utility - final verification | src/applications/ |
| test_server_health_polling.py | Test - health polling | src/applications/ |
| verify_ledger.py | Utility - ledger verification | src/applications/ |

**Fix:** Move all 5 to `src/applications/` (keep with other utilities/tests)

---

## PART 2: ROOT-LEVEL MARKDOWN FILES (Should be in docs/)

**80+ markdown files at root:**

### Status/Session Documents (Archive/Historical)
- SESSION_2026-03-27_*.md (3 files)
- SESSION_COMPLETE_SUMMARY.md
- SESSION_SUMMARY_*.md (2 files)
- CHECKPOINT_SESSION_*.md
- HARM_REMEDIATION_*.md (3 files)
- IMPLEMENTATION_STATUS.md
- PHASE_1_STATUS.md
- CLEANUP_COMPLETE.md
- CLEANUP_AND_ORGANIZATION_GUIDE.md

**Action:** Keep most recent in `/docs/` → Archive old ones → Delete duplicates

### Architecture/Design Docs
- ARIA_OS_SPECIFICATION.md
- ARIA_OS_DEPLOYMENT_GUIDE.md
- ARIA_CAPABILITY_*.md (5 files)
- BIDIRECTIONAL_*.md (2 files)
- CANVAS_WEBSERVER_MANAGER_*.md
- CAUSAL_CHAIN_RESONANCE_VERIFICATION.md
- CHANGE_DETECTION_OPTIMIZATION.md
- etc. (30+ architecture files)

**Action:** Move to `/docs/architecture/`

### Index/Reference Docs
- JARVIS_FILES_INDEX.md
- IMPLEMENTATION_INDEX_2026-03-27.md
- COMPLETE_FILE_INDEX.md
- MULTIUSER_NETWORKING_INDEX.md
- JARIVS_QUICK_START.md
- RUN_APP.md
- PROJECT_STRUCTURE_GUIDE.md
- QUICK_REFERENCE_CARD.md
- START_HERE.md

**Action:** Keep **only** RUN_APP.md and START_HERE.md at root → Move rest to `/docs/`

### Protocol/Guide Docs (For Future Sessions)
- CLAUDE_INSTRUCTIONS.md (KEEP AT ROOT)
- CLAUDE_*.md (10+ files)
- CODE_MODIFICATION_PROTOCOL.md
- CONTINUATION_PROTOCOL.md
- etc.

**Action:** Keep in `/docs/protocols/` (important for next session)

### Text Files (Should be organized)
- app_output.txt → Delete (likely stale)
- MULTIUSER_NETWORKING_SUMMARY.txt → Move to docs/
- README_CLAUDE_INTEGRATION.txt → Move to docs/
- SYSTEM_COMPLETE.txt → Archive or delete
- UFM_SIMULATOR_DEPLOYMENT_COMPLETE.txt → Archive

---

## PART 3: ROOT-LEVEL DIRECTORIES (Map their purposes)

| Directory | Purpose | Status | Action |
|-----------|---------|--------|--------|
| `archive/` | Old code (already cleaned in src/applications/) | Redundant | Check contents, decide keep/delete |
| `aria_renders/` | Generated render files | Active | Keep at root (assets) |
| `ChatDev/` | ChatDev integration? | Unclear | Identify purpose |
| `ledger-shell/` | Old ledger shell? | Likely old | Check if still used |
| `ledger-system/` | Old ledger system? | Likely old | Check if still used |
| `src/` | Active codebase | ACTIVE | Keep |
| `zeropoint-system/` | Old zeropoint? | Likely old | Check if still used |

**Issue:** Have NO IDEA what ChatDev, ledger-shell, ledger-system, or zeropoint-system do. Are they active or obsolete?

---

## PROPOSED FINAL STRUCTURE

```
c:\Determined\
├── RUN_APP.md                    (ONE line: how to run the system)
├── START_HERE.md                 (ONE line: orientation)
├── CLAUDE_INSTRUCTIONS.md        (Keep - for next session)
├── docs/
│   ├── README.md                 (What docs are where)
│   ├── QUICK_START.md            (Condensed start guide)
│   ├── architecture/             (All architecture docs)
│   ├── protocols/                (All protocol/guide docs)
│   ├── sessions/                 (Session summaries, archived)
│   ├── reference/                (Index and reference docs)
│   └── archive/                  (Old docs for historical reference)
├── src/
│   └── applications/
│       ├── jarvis_v3.py
│       ├── jarvis.html
│       ├── ledger_query.py
│       ├── self_awareness.py
│       ├── health_monitoring_utils.py
│       ├── parameter_form.py
│       ├── check_ledger.py       (MOVED from root)
│       ├── check_menu_frame.py   (MOVED from root)
│       ├── ledger_final_check.py (MOVED from root)
│       ├── verify_ledger.py      (MOVED from root)
│       ├── test_*.py
│       ├── aria_renders/         (or keep at root?)
│       └── ledger_*.jsonl
├── aria_renders/                 (OR HERE?)
├── .claude/
├── .venv/
└── [DECIDE: ChatDev, ledger-shell, ledger-system, zeropoint-system]
```

---

## QUESTIONS NEEDING ANSWERS

1. **ChatDev/** - Is this active or obsolete?
2. **ledger-shell/** - Is this active or obsolete?
3. **ledger-system/** - Is this active or obsolete?
4. **zeropoint-system/** - Is this active or obsolete?
5. **archive/** at root - Different from src/applications/archive (already deleted)?
6. **aria_renders/** - Should this be in src/applications/ or at root?

---

## CLEANUP PHASE 1: DEFINITE MOVES

### Move Python files to src/applications/
- check_ledger.py
- check_menu_frame.py
- ledger_final_check.py
- test_server_health_polling.py
- verify_ledger.py

### Keep at Root (ONLY)
- RUN_APP.md
- START_HERE.md
- CLAUDE_INSTRUCTIONS.md

### Create docs/ folder and move documentation
- Move 80+ .md files to organized structure
- Move .txt files to docs/ or delete
- Archive old session files

---

## HARM FROM CURRENT NOISE

1. **80+ files at root** → User can't see what matters
2. **5 Python files at root** → Unclear if they're part of active system
3. **Multiple system directories** → Unclear which are active vs old
4. **80+ documentation files** → No organization, can't find anything
5. **No clear "START HERE"** → New developer lost immediately

**One principle:** Active system visible = easy. Everything else archived = clear.

