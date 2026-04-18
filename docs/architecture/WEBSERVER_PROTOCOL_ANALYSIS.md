# WEBSERVER PROTOCOL ANALYSIS
## Transparent Format for Webserver Existence

**Date**: March 29, 2026  
**Status**: CRITICAL - System has two competing backends with no clear ownership or transparency  
**Priority**: HIGHEST - Must establish single clear webserver with visible state reporting

---

## PROBLEM STATEMENT

### Current State
The system has **TWO independent webservers** attempting to start:

1. **jarvis_v3.py** (HTTP JSON API) 
   - Location: `c:\Determined\src\applications\jarvis_v3.py`
   - Port: 8081
   - Dependency: `LedgerQuery` class (imports 25+ ledger files at startup)
   - Status: **FAILING** (Exit Code 1 - no error output)

2. **app.py** (FastAPI)
   - Location: `c:\Determined\ledger-shell\backend\app.py`
   - Port: 8000
   - Framework: FastAPI
   - Status: **FAILING** (Exit Code 1 - no error output)

### Root Cause
Both backends fail silently with **zero diagnostic output**. No `try/except`, no error messages, no logging that persists.

**Impact**: User cannot tell if:
- Import failed
- File not found
- JSON parse error
- Port already bound
- Database connection failed
- Syntax error in code

This has caused **"too many instances"** of debugging frustration.

---

## REQUIREMENT SPECIFICATION

### What "Transparent Format" Means
```
Transparent Format = System MUST:
1. Print startup sequence (what's loading in order)
2. Report success/failure for each component
3. Log all exceptions with full traceback (never silently die)
4. Report final state: READY, DEGRADED, or FAILED
5. Provide health check endpoint that reports actual truth
6. Write all diagnostics to persistent log file (not just stdout)
7. Make it OBVIOUS to user what is/isn't working
```

---

## WEBSERVER ARCHITECTURE - DECISION REQUIRED

### Option A: Single Backend (RECOMMENDED)
**Use jarvis_v3.py as THE webserver**, remove app.py duplication
- ✅ Single source of truth
- ✅ Eliminates port conflicts
- ✅ Clearer ownership
- ✅ Easier to maintain transparency

**Effort**: 
- Add error handling to LedgerQuery (wrap all _load_* methods)
- Add startup diagnostics to jarvis_v3.py
- Remove/archive app.py (ledger-shell/backend)

### Option B: Dual Stack with Health Checks
**Keep both, but make each report its status clearly**
- Complexity: HIGH
- Benefit: None (they serve same purpose)
- Risk: Port binding conflicts, confusion

**Decision**: **OPTION A IS CORRECT** - Single backend with full transparency

---

## JARVIS_V3.PY PROTOCOL SPECIFICATION

### Startup Sequence (Must be Visible)
```
[BOOT  0.0s] Python interpreter initialized
[LOAD  0.1s] Import FastAPI libraries... ✓
[LOAD  0.2s] Import LedgerQuery class... ✓
[INIT  0.3s] LedgerQuery() instantiated...
  [LOAD  0.4s] ledger_buttons.jsonl (127 buttons)... ✓
  [LOAD  0.5s] ledger_dashboards.jsonl (8 dashboards)... ✓
  [LOAD  0.6s] ledger_actions.jsonl (45 actions)... ✓
  [LOAD  0.7s] ledger_elections.jsonl (1023 elections)... ✓
  ... (continue for all 25+ ledgers)
  [LOAD  1.2s] ALL LEDGERS LOADED ✓
[INIT  1.3s] Frame cache initialized... ✓
[PORT  1.4s] HTTP server binding to 127.0.0.1:8081... ✓
[READY 1.5s] ════════════════════════════════════════════
          JARVIS v3 WEBSERVER READY
          Port:     8081
          Ledgers:  25 files loaded
          Buttons:  127
          Dashboards: 8
          ════════════════════════════════════════════
[RUN   1.6s] Waiting for connections...
```

### Health Check Endpoint
**Endpoint**: `GET /api/health`

**Response (when healthy)**:
```json
{
  "status": "healthy",
  "timestamp": "2026-03-29T10:15:30Z",
  "uptime_seconds": 245,
  "boot_sequence": "complete",
  "components": {
    "ledger_query": "loaded",
    "frame_cache": "operational",
    "http_server": "listening",
    "port_8081": "bound"
  },
  "ledgers_loaded": 25,
  "buttons_count": 127,
  "dashboards_count": 8,
  "errors": []
}
```

**Response (when degraded/failed)**:
```json
{
  "status": "degraded",
  "timestamp": "2026-03-29T10:15:30Z",
  "boot_sequence": "partial",
  "failed_at": "Loading ledger_dashboards.jsonl",
  "error": "JSON decode error at line 45: expected property name",
  "errors": [
    {
      "component": "ledger_dashboards",
      "error": "JSON decode error at line 45",
      "file": "ledger_dashboards.jsonl",
      "recoverable": false
    }
  ]
}
```

### Persistent Diagnostics Log
**File**: `c:\Determined\src\applications\jarvis_v3_boot.log`

**Format**: System appends every startup event to this log (never cleared):
```
2026-03-29T10:15:22Z [BOOT] Starting jarvis_v3.py
2026-03-29T10:15:22Z [LOAD] Importing libraries...
2026-03-29T10:15:23Z [LOAD] FastAPI imported ✓
2026-03-29T10:15:23Z [LOAD] LedgerQuery.load_all() starting...
2026-03-29T10:15:23Z [LOAD]   ledger_buttons: 127 entries
2026-03-29T10:15:24Z [LOAD]   ledger_dashboards: 8 entries
...
2026-03-29T10:15:25Z [READY] ✓ JARVIS v3 READY on port 8081
```

This log is **PERSISTENT** - user can check it days later to see boot history.

---

## ERROR HANDLING PROTOCOL

### LedgerQuery Class Defensive Loading
```python
class LedgerQuery:
    def __init__(self, ledger_dir: str = "."):
        self.ledger_dir = ledger_dir
        self.errors = []  # Track all errors, don't crash on first
        self.load_all()   # With error collection
        
    def load_all(self):
        """Load all ledgers. Collect errors but proceed."""
        self._try_load("buttons", self._load_buttons)
        self._try_load("dashboards", self._load_dashboards)
        self._try_load("actions", self._load_actions)
        # ... etc
        
    def _try_load(self, name, load_func):
        """Wrap each loader with try/except"""
        try:
            load_func()
            print(f"[LOAD] ✓ {name}")
            return True
        except FileNotFoundError:
            return False  # OK - optional file
        except json.JSONDecodeError as e:
            self.errors.append(f"{name}: JSON error - {e}")
            return False
        except Exception as e:
            self.errors.append(f"{name}: {type(e).__name__} - {e}")
            return False
            
    def _load_buttons(self):
        """Load with error handling"""
        buttons_file = os.path.join(self.ledger_dir, "ledger_buttons.jsonl")
        if not os.path.exists(buttons_file):
            return  # Optional
        
        with open(buttons_file, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    btn = json.loads(line)
                    self.buttons[btn.get("id")] = btn
                except json.JSONDecodeError as e:
                    raise json.JSONDecodeError(
                        f"Line {line_no}: {e.msg}",
                        e.doc, e.pos
                    )
```

### Startup Error Reporting
```python
def startup_diagnostics(ledger):
    """Print diagnostic summary after load"""
    print("\n" + "="*60)
    if ledger.errors:
        print(f"⚠️  BOOT WARNINGS ({len(ledger.errors)} issues):")
        for error in ledger.errors:
            print(f"  - {error}")
        print("\n✓ JARVIS STARTING IN DEGRADED MODE")
    else:
        print("✓ ALL SYSTEMS NOMINAL")
    
    print(f"\nLoaded:")
    print(f"  • {len(ledger.buttons)} buttons")
    print(f"  • {len(ledger.dashboards)} dashboards")
    print(f"  • {len(ledger.elections)} elections")
    print("="*60 + "\n")
```

---

## BIDIRECTIONAL CHAIN REQUIREMENT

This is the CRITICAL missing piece causing "too many instances":

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORWARD CHAIN: User wants to verify server exists
  
  "Is server running?" 
    ↓
  Check /api/health
    ↓
  Response: {"status": "healthy", ...}
    ↓
  ✓ Server confirmed running
  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BACKWARD CHAIN: Before attempting to start server

  Want to start server
    ↓
  First: Check /api/health  ← CRITICAL: Must do this FIRST
    ↓
  If response OK:
    → DON'T start again (already running)
    → Just report "Server healthy"
  
  If no response / error:
    → Server crashed or not running
    → OK to start fresh
  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**The Current Bug**: 
- We check /api/state, /api/frame, /api/interaction
- We DON'T check /api/health
- So we never detect "already running"
- Result: Duplicate processes, port conflicts, Exit Code 1

**The Fix**:
- Add /api/health endpoint (EXISTS check)
- Call health check BEFORE starting (PREVENT duplicate)
- Only start if health check fails
- Report actual status to user

This is not about error handling - this is about **bidirectional causality verification**.

---

## PROTOCOL: WHAT MUST HAPPEN

### Phase 1: Add Transparency Layer to jarvis_v3.py
**Files to modify**:
- `src/applications/jarvis_v3.py` - Add startup diagnostics
- `src/applications/ledger_query.py` - Add error collection to load_all()

**Changes**:
1. Wrap every `_load_*` method with try/except that collects errors
2. Print startup sequence with timestamps
3. Add /api/health endpoint
4. Write boot log to persistent file
5. Never silently exit on error

**Outcome**: jarvis_v3.py starts and reports why (success or failure)

### Phase 2: Test Single Backend
**Command**:
```powershell
cd c:\Determined\src\applications
python jarvis_v3.py
```

**Expected Output**:
```
[BOOT  0.0s] Starting JARVIS v3...
[LOAD  0.1s] Importing libraries... ✓
[INIT  0.2s] LedgerQuery.load_all()...
[LOAD  0.3s]   ✓ ledger_buttons (127 entries)
[LOAD  0.4s]   ✓ ledger_dashboards (8 entries)
... (all ledgers)
[READY 1.2s] ════════════════════════════════════════════
          JARVIS v3 WEBSERVER READY
          Port: 8081
          ════════════════════════════════════════════
```

**Verification**: 
```powershell
curl http://localhost:8081/api/health
# Should return healthy JSON
```

### Phase 3: Archive Duplicate Backend
**Action**: Move `ledger-shell/backend/app.py` to archive

**Reason**: 
- jarvis_v3.py is THE webserver
- FastAPI backend is duplicate/unused
- Having two causes confusion and failure

---

## VERIFICATION PROTOCOL

### Health Check Confirms Working
```powershell
# 1. Server is running
$health = Invoke-WebRequest -Uri 'http://localhost:8081/api/health' -UseBasicParsing
$status = $health.Content | ConvertFrom-Json

if ($status.status -eq "healthy") {
    Write-Host "✓ JARVIS v3 is operational" -ForegroundColor Green
    Write-Host "  Ledgers: $($status.ledgers_loaded)"
    Write-Host "  Buttons: $($status.buttons_count)"
    Write-Host "  Dashboards: $($status.dashboards_count)"
} else {
    Write-Host "⚠️ JARVIS v3 degraded" -ForegroundColor Yellow
    Write-Host "Error: $($status.errors[0])"
}
```

### No More Silent Failures
```powershell
# Before (current): 
# Exit Code 1 with NO OUTPUT = impossible to debug

# After (new):
# Exit Code 1 WITH FULL DIAGNOSTICS
# • stderr prints exception
# • boot log records what failed
# • /api/health reports component status
```

---

## DECISION MATRIX

| Issue | Current | Fixed |
|-------|---------|-------|
| **Server won't start** | Exit Code 1, zero info | Full startup diagnostics |
| **Two competing backends** | App.py + jarvis_v3.py | Only jarvis_v3.py |
| **Error visibility** | None - silent failure | Persistent boot log + /api/health |
| **Port conflicts** | Both try 8081? | Single port 8081 |
| **Debugging** | "too many instances" | Clear diagnostics |
| **User knows status?** | NO - guessing | YES - health endpoint + logs |

---

## NEXT ACTIONS

**IMMEDIATELY**:
1. ✅ Review this protocol
2. 🔄 Implement LedgerQuery error collection
3. 🔄 Add startup diagnostics to jarvis_v3.py
4. 🔄 Add /api/health endpoint
5. 🔄 Add persistent boot logging
6. 🔄 Test startup sequence

**THEN**:
- Archive app.py (ledger-shell/backend)
- Document webserver as single source
- Verify all causal chains still have resonance

**OUTCOME**: 
System startup is transparent, debuggable, and reports accurate status.

---

## SUCCESS CRITERIA

✅ System starts **OR** fails with **clear output**  
✅ `/api/health` endpoint works and reports true status  
✅ Boot diagnostics written to persistent log  
✅ No more "too many instances" of debugging confusion  
✅ User can tell at a glance if system is working  

**Resonance Check**: All modifications preserve causal chain integrity - will verify per CODE_MODIFICATION_PROTOCOL.md
