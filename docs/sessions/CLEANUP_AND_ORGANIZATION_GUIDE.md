# 🧹 PROJECT CLEANUP & ORGANIZATION GUIDE

**Purpose:** Reduce noise from 100+ files to a manageable set  
**Time to execute:** 15 minutes  
**Risk level:** Very low (fully reversible)

---

## 📊 CURRENT STATE

```
c:\Determined\
├── 60+ markdown files (ROOT NOISE)
├── src/applications/
│   ├── 40+ markdown files (DOCS)
│   ├── 20+ ledger files (ACTIVE DATA)
│   ├── 10+ backup files (OLD)
│   └── archive/ (OLD PROJECT)
└── archive/ (ROOT BACKUP)

TOTAL: ~150 files, 50MB
USEFUL: ~25 files, 10MB
```

---

## ✅ KEEP THESE (Priority Order)

### 🔴 CRITICAL (Must Keep - System Won't Work Without These)

```
src/applications/
  ├── jarvis_v3.py                    ⭐⭐⭐ Main application
  ├── ledger_query.py                 ⭐⭐⭐ Query engine
  ├── jarvis.html                     ⭐⭐⭐ Web UI
  ├── parameter_form.py               ⭐⭐ Parameter controls
  ├── health_monitoring_utils.py      ⭐⭐ Health monitoring
  ├── ledger_*.jsonl                  ⭐⭐ Configuration
  └── ledger_sync_config.json         ⭐⭐ Sync config

Root/
  ├── ARIA_OS_SPECIFICATION.md        ⭐⭐⭐ System spec
  ├── src/                            ⭐⭐⭐ All code
  └── START_HERE.md                   ⭐⭐ Entry point
```

### 🟡 IMPORTANT (Keep - References)

```
Root/
  ├── IMPLEMENTATION_INDEX_2026-03-27.md    - Current status
  ├── PARAMETER_CONTROLS_COMPLETE.md       - Parameter docs
  ├── SERVER_HEALTH_POLLING_QUICK_REF.md  - Health monitoring
  ├── CLAUDE_INSTRUCTIONS.md              - Agent instructions
  ├── SESSION_2026-03-27_COMPLETE.md      - Latest session
  ├── ARIA_OS_DEPLOYMENT_GUIDE.md         - Deploy guide
  ├── MULTIUSER_NETWORKING_SUMMARY.txt    - Multi-user guide
  └── BIDIRECTIONAL_IMPLEMENTATION_COMPLETE.md - Capability docs
```

### 🟡 USEFUL (Keep - Reference)

```
Root/
  ├── INTENT_FIRST_PRINCIPLE.md
  ├── JARVIS_QUICK_START.md
  ├── SURFACE_PRO_QUICK_START.md
  ├── README_CLAUDE_INTEGRATION.txt
  └── COMPLETE_FILE_INDEX.md
```

---

## 🗑️ DELETE THESE (Safe - All Noise or Outdated)

### Tier 1: Definitely Delete

```
🗑️ SAFE TO DELETE IMMEDIATELY

Root/
  ├── archive/                                    # Old project backup
  ├── RCA_*.md                                    # Root cause analysis (completed)
  ├── HARM_REMEDIATION_*.md                       # Harm remediation (completed)
  ├── SESSION_2026-03-2[0-6]_*.md                # Old sessions (keep only 03-27+)
  ├── ARCHITECTURAL_CORRECTION_*.md               # Old architectures
  ├── SINGULAR*_*.md                             # Abandoned experiments
  ├── ZEROPOINT_CODEBASE_AUDIT.md               # Audit (referenced elsewhere)
  ├── VALIDATION_ARCHITECTURE_REFERENCE.md       # Old validation
  ├── INSTANCE_ARIA_*.md                         # Old perspectives
  ├── *.txt files except .instructions           # Log files
  ├── COMPLETE_FILE_INDEX.md                     # Use PROJECT_STRUCTURE_GUIDE.md
  └── check_ledger.py, verify_ledger.py         # Verification scripts (not used)

src/applications/
  ├── archive/                                   # Old code versions
  ├── legacy/                                    # Legacy implementations
  ├── *.bak, *.backup files                      # Backups
  ├── test_dir/                                  # Old test files
  ├── *.singularity files (old ones)             # Keep only active ones
  ├── debug.log                                  # Debug logs
  └── startup.log                                # Startup logs
```

### Tier 2: Can Delete Later

```
🗑️ DELETE IF YOU NEED SPACE

Root/
  ├── ChatDev/                        # External tool (keep if using ChatDev)
  ├── zeropoint-system/              # Framework ref (keep if implementing ZEROPOINT)
  └── ledger-shell/, ledger-system/  # External tools (keep if using)

src/applications/
  ├── *.md files in /applications     # Keep README.md, delete the rest
  └── test_*.py except critical ones  # Keep test_bidirectional_capabilities.py
```

---

## 📋 DELETION CHECKLIST

**Before you start:** Create a backup
```bash
# Windows PowerShell
Copy-Item c:\Determined c:\Determined_backup_2026-03-29 -Recurse
```

**Step 1: Delete root-level noise**
```bash
# Run these commands in PowerShell
cd c:\Determined

# Delete old analysis files
Remove-Item RCA_*.md
Remove-Item HARM_REMEDIATION_*.md

# Delete old session files (keep 03-27 and newer)
Remove-Item SESSION_2026-03-2[0-6]_*.md
Remove-Item SINGULAR*_*.md

# Delete redundant files
Remove-Item ARCHITECTURAL_CORRECTION_*.md
Remove-Item check_ledger.py
Remove-Item verify_ledger.py
```

**Step 2: Delete src/applications noise**
```bash
cd c:\Determined\src\applications

# Delete old archive and legacy
Remove-Item archive -Recurse
Remove-Item legacy -Recurse
Remove-Item test_dir -Recurse

# Delete backups
Remove-Item *.bak
Remove-Item *.backup

# Delete old ledger experiments
Remove-Item *.singularity (keep active ones manually)

# Delete logs
Remove-Item *.log
```

**Step 3: Clean root-level archive** (optional - largest cleanup)
```bash
# DELETE IF NOT USED - 20MB saved
Remove-Item c:\Determined\archive -Recurse
```

---

## 📁 RECOMMENDED STRUCTURE (Post-Cleanup)

```
c:\Determined/
│
├── 📄 START_HERE.md                        ⭐ Read first
├── 📄 PROJECT_STRUCTURE_GUIDE.md            ← You are here
├── 📄 ARIA_OS_SPECIFICATION.md             ⭐ System spec
├── 📄 IMPLEMENTATION_INDEX_2026-03-27.md   ⭐ Current index
│
├── 📄 CLAUDE_INSTRUCTIONS.md
├── 📄 INTENT_FIRST_PRINCIPLE.md
├── 📄 ARIA_OS_DEPLOYMENT_GUIDE.md
│
├── 📄 PARAMETER_CONTROLS_COMPLETE.md
├── 📄 SERVER_HEALTH_POLLING_QUICK_REF.md
├── 📄 MULTIUSER_NETWORKING_SUMMARY.txt
├── 📄 BIDIRECTIONAL_IMPLEMENTATION_COMPLETE.md
│
├── 📄 CLAUDE_AND_CHATDEV_OPERATING_SYSTEM.md
├── 📄 CHATDEV_ZEROPOINT_BRIEFING.md
│
├── 📄 SURFACE_PRO_QUICK_START.md
├── 📄 JARVIS_QUICK_START.md
│
├── 📁 src/                                 ⭐ Active code
│   ├── applications/
│   │   ├── 🐍 jarvis_v3.py                ⭐⭐⭐
│   │   ├── 🐍 ledger_query.py             ⭐⭐⭐
│   │   ├── 🐍 parameter_form.py           ⭐⭐
│   │   ├── 🐍 health_monitoring_utils.py  ⭐⭐
│   │   ├── 🌐 jarvis.html                 ⭐⭐⭐
│   │   │
│   │   ├── 📋 README.md
│   │   ├── 📋 RENDER_SPECIFICATION.yaml
│   │   │
│   │   ├── 📊 ledger_*.jsonl              (Config data)
│   │   ├── 📊 ledger_sync_config.json     (Sync data)
│   │   │
│   │   ├── 🧪 test_bidirectional_capabilities.py
│   │   ├── 🧪 test_*.py                   (Other tests)
│   │   │
│   │   └── 📁 ledgers/                    (Schema)
│   │
│   ├── foundation/
│   │   ├── 00-CORE-THEORY.md
│   │   └── 01-TERRITORIES-OVERVIEW.md
│   │
│   └── frameworks/
│       └── TERRITORY_*.md
│
├── 📁 ChatDev/                             (External tool)
├── 📁 zeropoint-system/                    (Framework)
├── 📁 .venv/                               (Virtual env)
│
└── 📁 Recent Backups/
    └── Dated by session          (For recovery if needed)
```

**Before:** 150 files, 50MB, confusing  
**After:** 50 files, 20MB, clear structure

---

## 🎯 ORGANIZATION GOING FORWARD

### Documentation Rules

**Root level -  Guideline: 1 markdown per active feature**
```
Format: FEATURE_COMPLETE.md or FEATURE_QUICK_REF.md
Example:
  ✅ PARAMETER_CONTROLS_COMPLETE.md
  ✅ SERVER_HEALTH_POLLING_COMPLETE.md
  ✅ MULTIUSER_NETWORKING_COMPLETE.md
  
Don't create:
  ❌ SESSION_DATE_DESCRIPTIVE_NAME.md (overclutters)
  ❌ RCA_PROBLEM_DATE.md (archive after fixing)
  ❌ Multiple versions of same doc
```

**Code location - Simple rule**
```
All active code → src/applications/*.py
All active configs → src/applications/ledger_*.jsonl
All tests → src/applications/test_*.py
All backups → src/applications/archive/
```

**Session notes - Keep only latest**
```
Keep: SESSION_YYYY-MM-DD_COMPLETE.md (today's)
Delete: Older than 7 days
Archive: Move to archive/ if needed later
```

---

## ✨ BENEFITS OF CLEANUP

| Before | After |
|--------|-------|
| 150 files confusing | 50 files clear |
| Can't find anything | Know exactly where to look |
| 50MB on disk | 20MB on disk |
| 1hr to understand | 5min with guide |
| New team member lost | New team member productive |

---

## 🔄 WHAT TO KEEP IN BACKUP

```
Critical backups to preserve:
✅ src/applications/ledger_*.jsonl          (Current state)
✅ src/applications/jarvis_v3.py            (Working code)
✅ src/applications/*.html                  (UI)
✅ All active feature docs

Old files to move to archive/:
✅ Old .singularity files
✅ Old versions of .py files
✅ Old documentation versions
```

---

## ⚠️ DO NOT DELETE

```
🚫 DO NOT DELETE - CRITICAL
  ├── .venv/ (virtual environment)
  ├── src/ (all code)
  ├── ledger_*.jsonl (configuration)
  ├── jarvis_v3.py (main app)
  ├── ARIA_OS_SPECIFICATION.md (system spec)
  └── START_HERE.md (entry point)

🚫 DO NOT DELETE - Unless you know why
  ├── ChatDev/ (if using ChatDev)
  ├── zeropoint-system/ (if using ZEROPOINT)
  └── .claude/ (if using Claude integration)
```

---

## ✅ CLEANUP VERIFICATION

After cleanup, verify you can still:

```bash
# Test 1: Application runs
cd c:\Determined\src\applications
python jarvis_v3.py
# Should start without errors ✓

# Test 2: Find key files
# Should be able to find in ~10 seconds:
#  - START_HERE.md
#  - ARIA_OS_SPECIFICATION.md
#  - src/applications/jarvis_v3.py
#  - src/applications/ledger_query.py

# Test 3: Documentation clear
# README files explain each section ✓
```

---

## 📊 CLEANUP SCRIPT (Optional)

```powershell
# PowerShell script to automate cleanup
# Save as: cleanup_project.ps1

$rootDir = "c:\Determined"

# Backup first
Copy-Item $rootDir "$($rootDir)_backup_$(Get-Date -Format 'yyyy-MM-dd-HHmmss')" -Recurse

# Delete old analysis files
Remove-Item "$rootDir/RCA_*.md" -Force
Remove-Item "$rootDir/HARM_REMEDIATION_*.md" -Force

# Delete old sessions (keep only latest)
Get-ChildItem "$rootDir/SESSION_2026-03-2[0-6]_*.md" | Remove-Item -Force

# Clean applications directory
Remove-Item "$rootDir/src/applications/archive" -Recurse -Force
Remove-Item "$rootDir/src/applications/legacy" -Recurse -Force
Remove-Item "$rootDir/src/applications/*.bak" -Force
Remove-Item "$rootDir/src/applications/*.log" -Force

# Optional: Delete root archive (frees ~20MB)
# Remove-Item "$rootDir/archive" -Recurse -Force

Write-Host "✓ Cleanup complete"
Write-Host "Space freed: ~30MB"
```

---

**Recommendation:** Execute Tier 1 deletions now. Tier 2 only if you need space.

**Expected result:** Project goes from "what is this?" to "I can navigate this" in 5 minutes.
