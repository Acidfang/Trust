# 🚀 RUN THE APPLICATION

**Updated**: April 3, 2026 - Now with song generation architecture

---

## ⚠️ PROTOCOL COMPLIANCE REQUIRED

**Before running ANY operation on this application:**

1. **Verify you read CLAUDE_INSTRUCTIONS.md** - **NOW INCLUDES SONGS ARCHITECTURE**
2. **Your output goes through songs first** - Not direct to user format
3. **ARIA translates songs to user format** - That's how user sees results
4. **Review MANDATORY_PRE_WORK_PROTOCOL.md** - Still applies
5. **If ANY unexpected behavior occurs, use the diagnostic framework** (not just RCA)

---

## 🎵 SONGS FIRST, THEN TRANSLATION

**All output through this pipeline:**
```
Your Code
   ↓
Generate Song (internal canonical format)
   ↓
Record in SONG_WEIGHT_STRUCTURE (tracked)
   ↓
ARIA translates song to user format (JSON/SVG/Markdown/etc.)
   ↓
User sees output (context-appropriate)
```

**Never generate directly to user format. Always song first.**

---

## 🔴 IF SOMETHING BREAKS

**DO NOT just try the same approach again.**

**Instead:**

1. **Document what happened** - Exact error, conditions, expectations vs. reality
2. **Read CLAUDE_INSTRUCTIONS.md** - "If You're Not Following Instructions" section
3. **Apply Decision Elections Ledger** - Classify the decision
4. **Run Universal Equilibration Protocol** - Find the correct branch
5. **Record the learning** - Add to /memories/repo/ for future systems
6. **Fix root cause** - Not symptom

**Example**:
- **Symptom**: Render not being tracked
- **Root cause**: ARIA not calling render_with_song_layer()
- **Fix**: Update archive/aria.py to use unified router
- **Record**: Why this happened, what was learned

---

## 🔌 THE UNIVERSAL RENDERER

**Location**: [UNIVERSAL_RENDERER.py](./UNIVERSAL_RENDERER.py)

**Contains:**
- Song generation (generate_render_song)
- Translation to formats (translate_song_to_format)
- Recording (record_render_operation)
- Recovery queries (query_render_dependencies)
- Unified router (render_with_song_layer)

**This is where ALL rendering happens now** - One universal container, not scattered across files.

---

## 📊 BEFORE YOU RUN ANYTHING

Verify these 7 songs are working:

```
1. ENGAGEMENT vs DENIAL ✓ (weight 15%)
2. CONSTRAINT creates DEPTH ✓ (weight 15%)
3. ATTACHMENT corrupts DISCIPLINE ✓ (weight 15%)
4. RARITY of TRIPLE INTEGRATION ✓ (weight 12%)
5. TEMPORAL INTEGRATION locks PAST ✓ (weight 14%)
6. PROACTIVITY locks FUTURE ✓ (weight 14%)
7. UNIFIED FIELD creates INEVITABILITY ✓ (weight 15%)
```

**Test**: Run [UNIVERSAL_SONG_GENERATOR.py](./UNIVERSAL_SONG_GENERATOR.py)
```powershell
python UNIVERSAL_SONG_GENERATOR.py
```

Should output:
- UNIVERSAL_RECOVERY_SONGS.txt (17 KB+)
- SYMBOL_REFERENCE.txt (2 KB+)

---

## 🚀 The One File That Matters (Unchanged)

```
c:\Determined\src\applications\jarvis_v3.py
```

**But now**: When it generates output, it goes through:
1. Song generation (UNIVERSAL_RENDERER.py)
2. ARIA translation (archive/aria.py - **VERIFY THIS IS UPDATED**)
3. User format

**That file itself hasn't changed. The rendering chain has.**

---

## Setup (One Time)

```powershell
cd c:\Determined

# Activate virtual environment
& .venv\Scripts\Activate.ps1

# Go to the code
cd src\applications
```

---

## Run It

```powershell
python jarvis_v3.py
```

**What happens internally now:**
1. jarvis_v3 generates data
2. UNIVERSAL_RENDERER.py creates songs from data
3. ARIA translates songs to user format
4. User sees the result

---

## Access It

Open browser:
```
http://localhost:8000/jarvis.html
```

---

## What It Needs (Already There)

```
c:\Determined\
├── UNIVERSAL_RENDERER.py          ← ALL rendering happens here now
├── UNIVERSAL_SONG_GENERATOR.py    ← Reference for song generation
├── SONG_WEIGHT_STRUCTURE_RECORDING.py ← Tracks all operations
├── archive/aria.py                ← VERIFY: Calls render_with_song_layer()
│
c:\Determined\src\applications\
├── jarvis_v3.py                   ← RUN THIS (unchanged)
├── jarvis.html
├── ledger_query.py
├── parameter_form.py
├── health_monitoring_utils.py
└── ledger_*.jsonl
```

All dependencies already installed.  
All config files already set up.  
**Just run `python jarvis_v3.py`.**

---

## Stop It

```
Ctrl+C in terminal
```

---

## Important: ARIA Update Needed

**archive/aria.py** needs to be updated to call:
```python
from UNIVERSAL_RENDERER import render_with_song_layer

# Instead of direct rendering:
output = render_with_song_layer(container, output_format="svg")
```

**This ensures**:
- Songs generated internally ✓
- Operations recorded ✓  
- User gets correct format ✓
- Recovery possible ✓

**Status**: If renders aren't appearing in SONG_WEIGHT_STRUCTURE.json, ARIA update is probably needed.

---

## Verification Checklist

After running:

- [ ] No errors in console
- [ ] SONG_WEIGHT_STRUCTURE.json file exists
- [ ] Render operations logged in weight structure
- [ ] Can query recovery sequence (should show 7 songs in priority order)
- [ ] Symbol-only recovery format works (⊙ ◯ → ∞ ⊕ ◊ ?)
- [ ] User sees expected output (JSON/SVG/etc. based on format requested)

---

## Troubleshooting

**"Port already in use"** - Kill existing process or use different port

**"render_with_song_layer not found"** - UNIVERSAL_RENDERER.py needs updating or not in path

**"No renders in weight structure"** - ARIA not calling unified router. Update archive/aria.py

**"Songs not generating"** - Run UNIVERSAL_SONG_GENERATOR.py to test independently

**"Recovery sequence error"** - Check SONG_WEIGHT_STRUCTURE.json is valid JSON

---

## Recovery Mode (Manual)

If system corrupts, recover in this order:

```powershell
# 1. Check weight structure
python -c "from SONG_WEIGHT_STRUCTURE_RECORDING import SONG_WEIGHT_STRUCTURE; print(SONG_WEIGHT_STRUCTURE['recovery_priority'])"

# 2. Regenerate if needed
python UNIVERSAL_SONG_GENERATOR.py

# 3. Verify symbols
cat SYMBOL_REFERENCE.txt

# 4. Restart app
python src\applications\jarvis_v3.py
```

Recovery sequence: Foundation-first order (Unified Field → Constraint → Temporal → Proactive → Engagement → Attachment → Rarity)
```powershell
# Kill existing process
Get-Process python | Stop-Process -Force
# Try again: python jarvis_v3.py
```

**"ModuleNotFoundError"**
```powershell
# Reactivate venv
& c:\Determined\.venv\Scripts\Activate.ps1
# Try again: python jarvis_v3.py
```

**"Can't find jarvis.html"**
```powershell
# Make sure you're in the right directory
cd c:\Determined\src\applications
python jarvis_v3.py
```

---

## That's all you need to know.

**File to run:** `jarvis_v3.py`  
**Where:** `c:\Determined\src\applications\`  
**Command:** `python jarvis_v3.py`  
**Access:** `http://localhost:8000/jarvis.html`  
**Stop:** `Ctrl+C`

Everything else is documentation. You don't need it.
