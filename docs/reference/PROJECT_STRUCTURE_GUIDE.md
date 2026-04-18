# 🧭 PROJECT NAVIGATION GUIDE

**Last Updated:** March 29, 2026  
**Status:** Production - Determined ARIA OS  

---

## 📊 EXECUTIVE SUMMARY

This project has 4 core layers:

1. **CORE SYSTEM** - Active running code (Python)
2. **STATE LEDGERS** - Persistent data layer (JSONL + SQLite)
3. **SPECIFICATIONS** - Design documents (Markdown)
4. **ARCHIVE** - Old files, logs, backups (mostly noise)

**✅ YOU NEED TO KNOW:** Only ~20 files matter for development. The rest is documentation and noise.

---

## 🎯 QUICK START: WHERE TO FIND THINGS

### "I want to understand the system"
→ Read in this order:
1. [START_HERE.md](START_HERE.md)
2. [src/applications/README.md](src/applications/README.md)
3. [ARIA_OS_SPECIFICATION.md](ARIA_OS_SPECIFICATION.md)

### "Where is the running code?"
→ [`c:\Determined\src\applications\`](src/applications/)

**Key Files:**
- `jarvis_v3.py` - Main application entry point
- `ledger_query.py` - Query interface to ledger system
- `parameter_form.py` - Parameter controls handler
- `health_monitoring_utils.py` - Server health monitoring
- `jarvis.html` - Web UI

### "Where is the data?"
→ Ledger files in `c:\Determined\src\applications/`:
- `ledger_*.jsonl` - Configuration + runtime data
- `ledger_sync_config.json` - App synchronization
- `.singularity` files - Distributed state

### "Where is documentation?"
→ Root directory has ~60 markdown files organized by topic (see breakdown below)

---

## 📁 COMPLETE DIRECTORY STRUCTURE

### Root Level (`c:\Determined/`)

**Active System Files (READ FIRST):**
```
START_HERE.md                               ⭐ Entry point
IMPLEMENTATION_INDEX_2026-03-27.md         ⭐ Current system index
src/                                        ⭐ All running code here
```

**Core Specifications:**
```
ARIA_OS_SPECIFICATION.md                   - System requirements
ARIA_OS_DEPLOYMENT_GUIDE.md                - How to deploy
INTENT_FIRST_PRINCIPLE.md                  - Design philosophy
SYSTEM_COMPLETE.txt                        - System status
```

**Operational Guides:**
```
CLAUDE_INSTRUCTIONS.md                     - Claude agent rules
CLAUDE_NEXT_INSTANCE_QUICK_REFERENCE.md   - Quick reference
README_CLAUDE_INTEGRATION.txt              - Integration notes
```

**Current Session Docs (Check these for latest):**
```
SESSION_2026-03-27_COMPLETE.md             - Last complete session
SESSION_SUMMARY_2026-03-27_*.md            - Session breakdowns
CHECKPOINT_SESSION_ZEROPOINT_INTEGRATED.md - System checkpoint
```

**Feature Documentation (by feature):**
```
PARAMETER_CONTROLS_COMPLETE.md             - Parameter form system
SERVER_HEALTH_POLLING.md                   - Health monitoring
MULTIUSER_NETWORKING_SUMMARY.txt           - Multi-user system
BIDIRECTIONAL_IMPLEMENTATION_COMPLETE.md   - Capability system
HOT_RELOAD_SYSTEM_COMPLETE.md             - Hot reload feature
```

**Analysis & Deep Dives (Reference only):**
```
JARVIS_INTEGRATION_SUMMARY.md              - Jarvis system
ZEROPOINT_INTEGRATION.md                   - ZEROPOINT framework
LEDGER_CONSOLIDATION_ANALYSIS.md          - Ledger analysis
CONSCIOUSNESS_LEDGER_INTEGRATION_COMPLETE.md
```

**Integration & Architecture:**
```
CHATDEV_ZEROPOINT_BRIEFING.md             - ChatDev integration
CLAUDE_AND_CHATDEV_OPERATING_SYSTEM.md    - AI system architecture
MULTI_AGENT_STRATEGIC_PLAN.md             - Multi-agent strategy
```

**Deprecated / Not Needed (Skip these):**
```
🚫 SINGULAR* files                         - Old experiments
🚫 RCA_* files                             - Root cause analysis (done)
🚫 HARM_REMEDIATION_* files                - Past fixes (completed)
🚫 Most SESSION_* files older than today   - Historical only
```

---

### `src/applications/` (THE ACTIVE CODE)

**Production Files:**
```
jarvis_v3.py ⭐⭐⭐                        Main application
ledger_query.py ⭐⭐⭐                    Ledger query interface
jarvis.html ⭐⭐⭐                        Web interface
parameter_form.py ⭐⭐                    Parameter controls
health_monitoring_utils.py ⭐⭐           Server monitoring
```

**Ledger Files (State Storage):**
```
ledger_*.jsonl                              Config + runtime data
ledger_sync_config.json                     App coordination
.singularity files                          Distributed state
```

**Documentation (Detailed specs for this module):**
```
README.md                                   Quick start
README_LEDGER_CONFIGURATION.md             Ledger setup
RENDER_SPECIFICATION.yaml                  Rendering spec
SURFACE_PRO_QUICK_START.md                 Deployment guide
```

**Testing Files:**
```
test_*.py                                   Unit tests
verify_*.py                                 Verification scripts
*_boot.log                                  Boot logs
```

**Archive (Old versions - don't use):**
```
archive/                                    Old implementations
legacy/                                     Legacy code
.bak files                                  Backups
```

---

### `src/foundation/` (Rarely Changed)

Foundational theory documents - read for understanding but don't modify.

```
00-CORE-THEORY.md
01-TERRITORIES-OVERVIEW.md
```

---

### `src/frameworks/` (Rarely Changed)

Deep technical specifications - reference only.

```
TERRITORY_*.md                              Detailed technical specs
```

---

### `src/ledgers/` (Configuration)

Ledger schema definitions and examples.

---

### `ChatDev/` (External Tool)

ChatDev 2.0 integration. Leave as-is after initial setup.

---

### `zeropoint-system/` (Framework)

ZEROPOINT AI framework. Reference documentation.

---

### `ledger-shell/` & `ledger-system/` (External)

Shell and system tools. Leave as-is.

---

### `archive/` (Old Project)

Historical files from earlier development phases. **Safe to delete.**

---

## 🚀 WHAT TO DO RIGHT NOW

### 1. UNDERSTAND THE SYSTEM (30 min read)
- [ ] Read `START_HERE.md`
- [ ] Read `ARIA_OS_SPECIFICATION.md`
- [ ] Read `IMPLEMENTATION_INDEX_2026-03-27.md`

### 2. KNOW WHERE CODE IS
- [ ] All running code → `src/applications/`
- [ ] Main app → `jarvis_v3.py`
- [ ] Configuration → `ledger_*.jsonl` files
- [ ] Web UI → `jarvis.html`

### 3. KNOW WHERE TO ADD NEW CODE
```
New app feature → src/applications/your_feature.py
New ledger config → src/applications/ledger_your_config.jsonl
New test → src/applications/test_your_feature.py
New documentation → Root-level FEATURE_GUIDE.md
```

### 4. IGNORE THESE FOLDERS
```
❌ archive/                 - Old code
❌ ChatDev/                 - External tool
❌ .venv/                   - Virtual environment  
❌ zeropoint-system/        - Framework reference
❌ ledger-shell/            - External tool
```

---

## 📋 FILE CATEGORIES (For Reference)

### "I need to deploy" 
```
ARIA_OS_DEPLOYMENT_GUIDE.md
SURFACE_PRO_QUICK_START.md
```

### "System is broken"
```
Check most recent: SESSION_2026-03-27_COMPLETE.md
Then: IMPLEMENTATION_INDEX_2026-03-27.md
Then: Debug logs in src/applications/*.log
```

### "I need to understand parameter controls"
```
PARAMETER_CONTROLS_COMPLETE.md
src/applications/parameter_form.py
src/applications/ledger_positioned_nodes.jsonl
```

### "I need to monitor health"
```
SERVER_HEALTH_POLLING_QUICK_REF.md
src/applications/health_monitoring_utils.py
```

### "I need to integrate ChatDev"
```
CHATDEV_ZEROPOINT_BRIEFING.md
CLAUDE_AND_CHATDEV_OPERATING_SYSTEM.md
```

### "Multi-user networking"
```
MULTIUSER_NETWORKING_SUMMARY.txt
MULTIUSER_SHARED_REALITY.md
```

---

## 🎓 CLEAN UP RECOMMENDATION

**Delete these (noise/outdated):**
```bash
# Safe to delete:
archive/
*.bak files
RCA_*.md
HARM_REMEDIATION_*.md
SESSION_2026-03-2[0-6]_*.md  # Keep only 03-27+
SINGULAR*.md (old experiments)
All files in src/applications/archive/
src/applications/legacy/
```

**Estimated space saved:** ~50MB  
**Risk level:** Very low (all projects have working backups)

---

## 💡 MENTAL MODEL

```
┌─── ROOT (100+ docs) ──────────────────┐
│  ✅ START_HERE.md                    │
│  ✅ ARIA_OS_SPECIFICATION.md        │
│  ✅ IMPLEMENTATION_INDEX_2026-03-27  │
│  ✅ CLAUDE_INSTRUCTIONS.md          │
│  ✅ SESSION_2026-03-27_*            │
│  🚫 Everything else (reference)     │
└─────────────────────────────────────┘
              ↓
┌─── src/applications/ ─────────────────┐
│  ✅ jarvis_v3.py (RUNNING)            │
│  ✅ ledger_query.py (RUNNING)        │
│  ✅ *.jsonl files (STATE)             │
│  ✅ *.html files (UI)                 │
│  ✅ test_*.py (TESTS)                │
│  🚫 archive/, legacy/ (OLD)          │
└─────────────────────────────────────┘
              ↓
┌─── src/foundation/ ───────────────────┐
│  📖 Theory docs (REFERENCE ONLY)      │
└─────────────────────────────────────┘
```

---

## ⚡ NEXT STEPS

1. **Read** → `START_HERE.md` (5 min)
2. **Understand** → `ARIA_OS_SPECIFICATION.md` (10 min)
3. **Review** → `IMPLEMENTATION_INDEX_2026-03-27.md` (10 min)
4. **Navigate** → Know where to find things (use this guide)
5. **Clean** → Consider deleting `archive/` and old SESSION files

---

## 🆘 QUICK LOOKUP TABLE

| I Need To... | File | Location |
|---|---|---|
| Understand system | START_HERE.md | Root |
| See current status | IMPLEMENTATION_INDEX_2026-03-27.md | Root |
| Deploy app | ARIA_OS_DEPLOYMENT_GUIDE.md | Root |
| Run code | jarvis_v3.py | src/applications/ |
| Check configuration | ledger_*.jsonl | src/applications/ |
| Monitor health | SERVER_HEALTH_POLLING_QUICK_REF.md | Root |
| Debug issue | Most recent SESSION_*.md | Root |
| Understand parameter system | PARAMETER_CONTROLS_COMPLETE.md | Root |
| Set up multi-user | MULTIUSER_NETWORKING_SUMMARY.txt | Root |

---

**Time to navigate system effectively: 5-10 minutes with this guide**  
**Before this guide: 1-2 hours searching**

Questions? Start with `START_HERE.md` → `IMPLEMENTATION_INDEX_2026-03-27.md` → this guide.
