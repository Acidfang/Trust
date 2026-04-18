# Ledger-Driven Deterministic Shell

## Design Principle

**Field → Selection → Record**

- **Field:** Intent posted to `/api/intent`
- **Selection:** Deterministic execution (no randomness, no decisions)
- **Record:** Result appended immutably to `ledger.json`

No state outside the ledger. Full replay reconstructs exact system state.

## Architecture

```
Frontend (Browser)
    ↓ POST intent
Backend API (FastAPI)
    ↓ validate → execute → append
Ledger (JSON)
    ↓ derive state
Frontend (render)
```

## System State

State is **never** stored in memory. It is **always** computed from the ledger.

```python
def compute_state_from_ledger():
    state = {}  # Start empty
    for entry in ledger:
        apply(entry, state)  # Replay each action
    return state
```

This means:
- Refresh browser → same state (it's reading the ledger)
- Restart backend → no data loss (ledger is persistent)
- Full transparency → audit trail is the system

## Quick Start

### 1. Install Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Backend

**Windows:**
```
start_backend.bat
```

**Linux/macOS:**
```bash
cd backend
python app.py
```

Server runs on `http://127.0.0.1:8000`

### 3. Open Frontend

In browser, go to: `http://127.0.0.1:8000`

Or run:
```
open_browser.bat
```

## API

### GET `/api/state`
Returns current state (computed from ledger)

```json
{
  "view": "init",
  "position": [100, 200],
  "objects": [],
  "log": []
}
```

### GET `/api/ledger`
Returns entire ledger (audit trail)

```json
{
  "entries": [
    {
      "id": 0,
      "timestamp": "2026-03-28T00:00:00",
      "intent": {"action": "system_boot", "params": {}},
      "output": {"status": "success"},
      "valid": true,
      "hash": "abc123..."
    }
  ]
}
```

### POST `/api/intent`
Append intent, execute, record result

```bash
curl -X POST http://127.0.0.1:8000/api/intent \
  -H "Content-Type: application/json" \
  -d '{"action": "create_object", "params": {"id": "obj_1", "x": 100, "y": 200}}'
```

Supported actions:
- `create_object` - Create point on canvas
- `move_object` - Move existing object
- `render_text` - Add text to log
- `set_view` - Change current view

### GET `/api/replay`
Verify system by full replay

```json
{
  "ledger_entries": 5,
  "replayed_state": {...},
  "verification": "state derived completely from ledger"
}
```

## Frontend

**Canvas Section:**
- Visualizes objects from ledger
- Click objects to select them

**Control Panel:**
- Create, move, render objects
- View current state (JSON)
- See ledger entry count

**Log:**
- Timeline of all actions
- Errors and status messages

## Key Design Principles

### 1. No State Outside Ledger
Memory is not authoritative. Ledger is.

### 2. Every Action Recorded
```
POST /api/intent → execute → append ledger → return result
```

### 3. Deterministic Execution
Same intent + same ledger = same result. Always.

### 4. Immutable History
Past ledger entries never change. New corrections are new entries.

### 5. Full Replay
Recompute state from scratch every time = transparency + verification

## Testing

### Full Replay Test
```bash
curl http://127.0.0.1:8000/api/replay
```

Should show that replayed state matches current state.

### Ledger Integrity
```bash
curl http://127.0.0.1:8000/api/ledger | jq '.entries | length'
```

Should match entry count in UI.

### Persistence Test
1. Create object (POST to `/api/intent`)
2. Restart backend
3. GET `/api/state`

State should be identical (loaded from ledger).

## Project Structure

```
ledger-shell/
├── backend/
│   ├── app.py           # FastAPI server
│   ├── ledger.json      # Append-only ledger
│   └── requirements.txt
├── frontend/
│   └── index.html       # React-like pure JS UI
├── start_backend.bat    # Windows startup
├── open_browser.bat     # Open frontend
└── README.md
```

## Zeropoint Principles Applied

✓ **One-sentence intent:** Deterministic shell that reads intent, executes, records.

✓ **Spec before code:** Structure defined before any implementation.

✓ **Five gates:** Aligns with primitive, eliminates ambiguity, visible reasoning, kind, scalable.

✓ **No state outside ledger:** Field → Selection → Record strictly enforced.

✓ **Perfect foresight:** Every action path works; no dead branches.

✓ **Intent before code:** Every component has explicit purpose.

## What This Proves

This system demonstrates:
- **Transparency** — Every action is visible and traceable
- **Determinism** — Same inputs always produce same outputs
- **Immutability** — History cannot be rewritten
- **Auditability** — Full replay verifies correctness
- **Scalability** — Works with 1 action or 10,000

The ledger is the only source of truth. The system is its history.
