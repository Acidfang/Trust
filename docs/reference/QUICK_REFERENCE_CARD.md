# ⚡ PROJECT QUICK REFERENCE CARD

**Print this or keep it open while working**

---

## 🎯 THE THREE ESSENTIAL FILES

```
1. START_HERE.md
   → Read first to understand the system
   
2. ARIA_OS_SPECIFICATION.md  
   → The actual system spec - what should it do?
   
3. src/applications/jarvis_v3.py
   → The running code - where it happens
```

---

## 📍 WHERE TO FIND THINGS

| Need... | Location | File |
|---------|----------|------|
| **To run app** | src/applications/ | jarvis_v3.py |
| **Query database** | src/applications/ | ledger_query.py |
| **Web UI** | src/applications/ | jarvis.html |
| **Parameters** | src/applications/ | parameter_form.py |
| **Health monitoring** | src/applications/ | health_monitoring_utils.py |
| **Configuration** | src/applications/ | ledger_*.jsonl |
| **System spec** | Root | ARIA_OS_SPECIFICATION.md |
| **How to deploy** | Root | ARIA_OS_DEPLOYMENT_GUIDE.md |
| **What's working now** | Root | IMPLEMENTATION_INDEX_2026-03-27.md |
| **Multi-user docs** | Root | MULTIUSER_NETWORKING_SUMMARY.txt |
| **Parameter docs** | Root | PARAMETER_CONTROLS_COMPLETE.md |
| **Health monitoring** | Root | SERVER_HEALTH_POLLING_QUICK_REF.md |

---

## 🏗️ SYSTEM ARCHITECTURE (55 Second Version)

```
┌─────────────────────────────┐
│   jarvis_v3.py (Main App)   │
│   Runs Determined ARIA OS   │
└──────────┬──────────────────┘
           │
           ├─→ ledger_query.py
           │   (Reads/writes state)
           │
           ├─→ parameter_form.py
           │   (UI controls)
           │
           ├─→ health_monitoring_utils.py
           │   (System monitoring)
           │
           └─→ jarvis.html
               (Web interface)
               
           All state in:
           ledger_*.jsonl (persisted)
           ledger_sync_config.json (coordination)
```

---

## 🚀 QUICK START (Command Line)

```bash
# 1. Navigate to code
cd c:\Determined\src\applications

# 2. Activate virtual environment
& c:\Determined\.venv\Scripts\Activate.ps1

# 3. Run the app
python jarvis_v3.py

# 4. Open browser to:
http://localhost:8000/jarvis.html
```

---

## 📊 FILE ORGANIZATION (Visual)

```
c:\Determined/
│
├─ 📖 START_HERE.md                    ← Read first!
├─ 📖 ARIA_OS_SPECIFICATION.md         ← What is it?
├─ 📖 IMPLEMENTATION_INDEX_2026-03-27  ← What's done?
├─ 📖 PROJECT_STRUCTURE_GUIDE.md       ← Where's what?
│
├─ 🛠️ src/applications/                ← ALL CODE HERE
│   ├─ 🐍 jarvis_v3.py                ⭐ Main app
│   ├─ 🐍 ledger_query.py             ⭐ Database
│   ├─ 🌐 jarvis.html                 ⭐ Web UI
│   ├─ 🐍 parameter_form.py
│   ├─ 🐍 health_monitoring_utils.py
│   └─ 📊 ledger_*.jsonl               ⭐ Config
│
├─ 📁 src/foundation/                  ← Theory (ref only)
├─ 📁 src/frameworks/                  ← Specs (ref only)
│
├─ 🚫 archive/                         ← Old files (delete)
├─ 🚫 ChatDev/                         ← External tool
└─ 🚫 Everything else                  ← Reference docs
```

---

## 🎓 UNDERSTANDING LEVELS

**Level 1: 5 minutes**
- Read: `START_HERE.md`
- Know: Where to find the running code

**Level 2: 15 minutes**
- Read: `ARIA_OS_SPECIFICATION.md`
- Know: What the system does

**Level 3: 30 minutes**
- Read: `PROJECT_STRUCTURE_GUIDE.md`
- Read: `IMPLEMENTATION_INDEX_2026-03-27.md`
- Know: How everything fits together

**Level 4: 1-2 hours**
- Read: Feature docs (PARAMETER_CONTROLS_COMPLETE.md, etc.)
- Read: Code comments in src/applications/
- Know: How to modify the system

---

## 🔧 COMMON TASKS

### "I want to run the app"
```
cd c:\Determined\src\applications
python jarvis_v3.py
```

### "I want to modify a parameter"
```
Edit: src/applications/ledger_parameters.jsonl
Or:   src/applications/parameter_form.py
Restart: jarvis_v3.py
```

### "I want to check system status"
```
Read: IMPLEMENTATION_INDEX_2026-03-27.md
Or:   src/applications/ledger_app_state.jsonl
```

### "I want to add new feature"
```
1. Create: src/applications/my_feature.py
2. Import: in jarvis_v3.py
3. Test: Create test_my_feature.py
4. Document: Create MY_FEATURE_GUIDE.md in root
```

### "System won't start"
```
1. Check: Most recent error in src/applications/*.log
2. Read: IMPLEMENTATION_INDEX_2026-03-27.md
3. Search: SessionSummary for similar issue
```

### "I need to understand [FEATURE]"
```
Search: Root directory for [FEATURE]_COMPLETE.md
Example: PARAMETER_CONTROLS_COMPLETE.md
         SERVER_HEALTH_POLLING_QUICK_REF.md
         MULTIUSER_NETWORKING_SUMMARY.md
```

---

## 📚 KEY DOCUMENTATION FILES

**Must Read:**
- ✅ START_HERE.md
- ✅ ARIA_OS_SPECIFICATION.md
- ✅ IMPLEMENTATION_INDEX_2026-03-27.md
- ✅ PROJECT_STRUCTURE_GUIDE.md

**Should Read (by feature):**
- 📖 PARAMETER_CONTROLS_COMPLETE.md
- 📖 SERVER_HEALTH_POLLING_QUICK_REF.md
- 📖 MULTIUSER_NETWORKING_SUMMARY.txt
- 📖 ARIA_OS_DEPLOYMENT_GUIDE.md

**For Reference:**
- 📚 INTENT_FIRST_PRINCIPLE.md
- 📚 SURFACE_PRO_QUICK_START.md
- 📚 README_CLAUDE_INTEGRATION.txt

---

## ❌ FILES TO IGNORE

```
Don't waste time reading these:
❌ RCA_*.md (passed, not relevant)
❌ HARM_REMEDIATION_*.md (old fixes)
❌ SESSION_2026-03-2[0-6]_*.md (old sessions)
❌ SINGULAR*.md (experiments)
❌ ARCHITECTURAL_CORRECTION_*.md (old)
❌ archive/* (old code)
❌ ChatDev/* (external tool)
❌ *.bak files (backups)
```

---

## 🎯 MENTAL MODEL

```
Think of it like:

Library Structure:
├─ Entry Hall (START_HERE.md)
├─ System Design (ARIA_OS_SPECIFICATION.md)
├─ Current Status Board (IMPLEMENTATION_INDEX_2026-03-27.md)
├─ Navigation Map (PROJECT_STRUCTURE_GUIDE.md)
│
├─ Operations Center (src/applications/)
│  ├─ Main Control (jarvis_v3.py)
│  ├─ Database (ledger_query.py)
│  ├─ Dashboard (jarvis.html)
│  └─ Data Storage (ledger_*.jsonl)
│
├─ Theory Section (src/foundation/)
└─ Archive (archive/)

Start at: Entry Hall → System Design → Navigation Map
Then: Operations Center for actual work
```

---

## 📞 "I'M STUCK" CHECKLIST

- [ ] Did I read START_HERE.md?
- [ ] Did I read ARIA_OS_SPECIFICATION.md?
- [ ] Did I check IMPLEMENTATION_INDEX_2026-03-27.md?
- [ ] Did I look at project structure? (PROJECT_STRUCTURE_GUIDE.md)
- [ ] Did I find the feature guide? (Search [FEATURE]_COMPLETE.md)
- [ ] Did I check the code? (src/applications/jarvis_v3.py)
- [ ] Did I check recent logs? (src/applications/*.log)

**If still stuck:** All info is in these 4 docs:
1. START_HERE.md
2. ARIA_OS_SPECIFICATION.md
3. IMPLEMENTATION_INDEX_2026-03-27.md
4. PROJECT_STRUCTURE_GUIDE.md

---

## ⏱️ TIME INVESTED → PRODUCTIVITY GAINED

| Time Spent | Competency Level | What You Can Do |
|-----------|------------------|-----------------|
| 5 min | Beginner | Find files, run app |
| 15 min | Intermediate | Understand architecture |
| 30 min | Advanced | Modify configuration |
| 1 hour | Expert | Add new features |

**Recommendation:** Spend 30 minutes reading docs FIRST.  
**Saves:** 5+ hours of confusion later.

---

**Version:** Quick Reference 1.0  
**Last Updated:** March 29, 2026  
**Keep this handy!** →   Bookmark or print
