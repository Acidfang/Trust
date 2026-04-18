# CLEANUP PROTOCOL - MANDATORY

**Date Established:** 2026-03-29  
**Authority:** User directive + system hygiene principle  
**Scope:** ALL future work on this project  

This protocol is **non-negotiable**. Violating it creates system harm.

---

## THE PROBLEM WE SOLVE

Before this protocol:
- 80+ markdown files at project root
- 5 Python test files scattered at root
- Developers couldn't find anything
- Every new task added MORE noise
- System became unnavigable

**After Protocol:**
- Root has ONLY 3 critical files
- All documentation organized in `/docs/`
- All code in proper location (`src/applications/`)
- Everything discoverable in 2 clicks

---

## ROOT DIRECTORY - ONLY THESE 3 FILES

```
c:\Determined\
├── RUN_APP.md                ← How to run the system (read first)
├── START_HERE.md             ← Project orientation (read second)
├── CLAUDE_INSTRUCTIONS.md    ← Operating rules for next session
└── src/                       ← Active codebase
└── docs/                      ← Everything else
```

**Any other file at root = VIOLATION**

---

## CREATE TEST SCRIPTS - RULES

**When you need to test something:**

### Rule 1: Location
- **ALL** test files go to: `c:\Determined\src\applications/`
- Test files = any file named `test_*.py`, `*_test.py`, `verify_*.py`, `check_*.py`

### Rule 2: Naming
- `test_<feature>.py` for new test
- `verify_<component>.py` for verification utility
- `check_<system>.py` for health check

### Rule 3: Cleanup Responsibility
**BEFORE ENDING YOUR SESSION:**

Every test file YOU created must be handled:
1. If it's useful → Move to `src/applications/`, mark as utility
2. If it's one-off → DELETE IT (don't leave it for someone else)
3. Never commit a test file and abandon it

**Test file at root after session ends = YOUR VIOLATION**

### Rule 4: Documentation Files
**Never create markdown files while testing.**

If you create markdown:
- For session work → Move to `docs/sessions/` at end of session
- For protocols → Move to `docs/protocols/`
- For architecture → Move to `docs/architecture/`
- For reference → Move to `docs/reference/`

**Rule:** End of session = all created docs moved or deleted.

---

## DOCUMENTATION ORGANIZATION

### `docs/protocols/` - Code & Operating Rules
- All `*_PROTOCOL.md` files
- `CLAUDE_*.md` (operating instructions)
- Continuation guides
- Code modification protocols
- System integration guides

### `docs/architecture/` - Design & Implementation
- `ARIA_*.md` - Architecture docs
- `*IMPLEMENTATION*.md` - Feature implementations
- `*ARCHITECTURE*.md` - System design
- `*DESIGN*.md` - Design documents
- Technical specifications

### `docs/sessions/` - Historical Records
- Completed session summaries
- Implementation reports
- Status documents (archived)
- Phase completion records

**These are read-only historical documents.** New sessions don't add here.

### `docs/reference/` - Lookup Materials
- Index files (`*_INDEX.md`)
- Quick reference (`*_QUICK*.md`)
- Guidelines (`*_GUIDE*.md`)
- Audit reports
- Validation records

---

## DIRECTORY STRUCTURE - FINAL

```
c:\Determined/
├── RUN_APP.md
├── START_HERE.md
├── CLAUDE_INSTRUCTIONS.md
│
├── src/applications/          ← ACTIVE CODE ONLY
│   ├── jarvis_v3.py          (server)
│   ├── jarvis.html           (webpage)
│   ├── ledger_query.py       (engine)
│   ├── self_awareness.py     (consciousness)
│   ├── param_form.py         (utilities)
│   ├── ledger_*.jsonl        (data)
│   ├── test_*.py             (any tests - must clean up!)
│   ├── verify_*.py           (utilities)
│   ├── check_*.py            (utilities)
│   └── aria_renders/         (generated files)
│
├── docs/
│   ├── protocols/            (operating rules & guides)
│   ├── architecture/         (design documents)
│   ├── sessions/             (archived session records)
│   └── reference/            (lookup materials)
│
├── .venv/                    (Python environment)
├── .claude/                  (Claude memory)
└── [DECISION PENDING]
    ├── ChatDev/              (active or delete?)
    ├── ledger-shell/         (active or delete?)
    ├── ledger-system/        (active or delete?)
    └── zeropoint-system/     (active or delete?)
```

---

## ENFORCEMENT - END OF SESSION CHECKLIST

Before marking a session complete, verify:

- [ ] **Root check:** Only 3 files at root (RUN_APP.md, START_HERE.md, CLAUDE_INSTRUCTIONS.md)
- [ ] **Test files:** All `test_*.py`, `verify_*.py`, `check_*.py` either in `src/applications/` or DELETED
- [ ] **Markdown files:** All `.md` files either in proper `/docs/` folder or DELETED
- [ ] **Python files:** Only production code at root, everything else in `src/applications/`
- [ ] **Stray files:** No random `.txt` or other files at root
- [ ] **Documentation:** No session notes left at root (move to `/docs/sessions/` or delete)

**If ANY check fails:**
- Session is NOT complete
- Spend 5 minutes cleaning
- Then mark complete

---

## THE PRINCIPLE

**Root directory = What you need to know RIGHT NOW**

Everything else = organized away, but accessible in `/docs/`

This keeps:
- Cognitive load LOW
- Discovery FAST
- Project CLEAN
- Future developers HAPPY

---

## VIOLATIONS & CORRECTIONS

### If you catch yourself creating random files at root:

**STOP IMMEDIATELY.** Ask:
1. Is this critical to run? → Keep at root (only 3 files allowed)
2. Is this code? → Move to `src/applications/`
3. Is this documentation? → Move to `docs/<type>/`
4. Is this temporary? → DELETE IT

**If unsure → DELETE IT.** Anything important will be recreated.

---

## FINAL DIRECTIVE

This protocol is part of the system now. It is not optional.

Every new session requires:
1. Clean root (3 files only)
2. Clean `src/applications/` (no test debris)
3. Organized `/docs/` (everything findable)

**Cleanliness is not a side effect. It is the goal.**

