# UNIFIED ARCHITECTURE: Dual-Frontend, Single Backend

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    UNIFIED BACKEND                           │
│                    ledger_query.py                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Core Methods:                                         │   │
│  │ • get_frame_for_view(view_name)                      │   │
│  │ • record_button_click(button_id)                     │   │
│  │ • get_current_view()                                 │   │
│  │ • _apply_absolute_positioning(nodes)                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  Ledger Data Sources (JSON):                                 │
│  • ledger_buttons.jsonl          (button specs)              │
│  • ledger_dashboards.jsonl       (view content)              │
│  • ledger_positioned_nodes.jsonl (pixel coordinates)         │
│  • ledger_state.json             (application state)         │
└─────────────────────────────────────────────────────────────┘
         ▲                                      ▲
         │                                      │
    ┌────┴────────────────────┐    ┌──────────┴────────┐
    │                         │    │                   │
    │  HTTP Frontend          │    │  Tkinter Frontend │
    │  jarvis_v3.py           │    │  jarvis_canvas_   │
    │                         │    │  ledger_driven.py │
    │  • GET /api/frame       │    │                   │
    │  • POST /api/interaction│    │  • Incremental    │
    │  • GET /api/state       │    │    rendering      │
    │                         │    │  • Frame change   │
    │  Translation Layer:     │    │    detection      │
    │  HTTP ↔ Ledger Queries  │    │  • Node tracking  │
    └────────────────────────┘    └─────────────────────┘
           Port 8000                  Tkinter Window
```

## Backend Unification Checklist

✅ **Both apps import:**
- `from ledger_query import LedgerQuery`
- Line 25: jarvis_canvas_ledger_driven.py
- Line 30: jarvis_v3.py

✅ **Both apps initialize identically:**
- `ledger = LedgerQuery(script_dir)`
- Canvas: Line 327 (in init)
- HTTP: Line 36 (module level)

✅ **Button interaction unified:**
- Both call `ledger.record_button_click(button_id)`
- Canvas: Line 406 (on_canvas_click handler)
- HTTP: Line 134 (POST /api/interaction handler)

✅ **Frame rendering uses same backend:**
- Canvas: `ledger.get_frame_for_view(ledger.get_current_view())`
- HTTP: `ledger.get_frame_for_view(ledger.get_current_view())`

✅ **State access unified:**
- Canvas: `ledger.get_current_view()`, `ledger.buttons`, `ledger.dashboards`
- HTTP: Same methods via `/api/state` endpoint

## Frontend Roles

### HTTP Server (jarvis_v3.py)
**Purpose:** Pure HTTP-to-Ledger translator

**Request Handlers:**
1. **GET /api/frame** → Returns frame JSON for current view
   - Calls: `ledger.get_frame_for_view(ledger.get_current_view())`
   - Returns: Frame dict with nodes, colors, dimensions

2. **POST /api/interaction** → Handles button clicks
   - Expects: JSON with `button_id`
   - Calls: `ledger.record_button_click(button_id)`
   - Returns: Result of button action

3. **GET /api/state** → Returns application state
   - Returns: Current view, button count, dashboard count, frame

**Key Characteristic:** 
- Stateless translator
- No business logic (all in ledger_query)
- Every request queries current state fresh

### Tkinter Canvas (jarvis_canvas_ledger_driven.py)
**Purpose:** Pure painter with intelligent incremental rendering

**Rendering Pipeline:**
1. **Frame Change Detection** (`_has_frame_changed()`)
   - Compares new frame spec vs last rendered frame
   - JSON serialization comparison
   - Skips rendering if unchanged

2. **Incremental Rendering** (`render_frame()`)
   - Tracks canvas items by node ID: `node_items[node_id] = [item_ids]`
   - Detects removed nodes → delete their canvas items
   - Detects changed nodes → redraw only those nodes
   - Leaves unchanged nodes untouched on canvas

3. **Node Rendering** (`_render_*_and_return_items()`)
   - Each render method returns list of created canvas item IDs
   - Methods: text, button, rectangle, 3d_object, image, and fallback
   - Items tracked by node ID for future updates

4. **Interaction** (`on_canvas_click()`)
   - Detects which button was clicked via coordinates
   - Calls: `ledger.record_button_click(clicked_button_id)`
   - Triggers frame refresh on next render cycle

**Key Characteristic:**
- Stateful view (tracks node items on canvas)
- Incremental updates only (no full redraws)
- Frame change detection prevents redundant work

## Data Flow Examples

### User Clicks "Dashboard 1" Button

**HTTP Flow:**
```
1. Frontend JS: POST /api/interaction {button_id: "dashboard_1"}
2. jarvis_v3.py:  Receives POST, extracts button_id
3. ledger_query:  record_button_click("dashboard_1")
   ├─ Queries ledger_buttons.jsonl for button spec
   ├─ Executes on_click action (e.g., view change)
   ├─ Updates ledger_state.json (current_view = "dashboard_1")
   └─ Returns result
4. Frontend JS: GET /api/frame
5. jarvis_v3.py:  ledger.get_frame_for_view("dashboard_1")
6. ledger_query:  Returns new frame from ledger_dashboards.jsonl
7. Frontend: Renders new frame
```

**Canvas Flow:**
```
1. User clicks canvas at (x, y)
2. on_canvas_click detects button at coordinates
3. ledger.record_button_click(button_id) [same as HTTP]
4. Next render_frame() call:
   ├─ New frame retrieved from ledger
   ├─ _has_frame_changed() compares vs last frame
   ├─ If changed:
   │  ├─ Detect removed nodes → delete items
   │  ├─ Detect changed nodes → redraw only those
   │  ├─ Leave unchanged nodes untouched
   │  └─ Update node tracking state
   └─ Canvas displays incremental changes
```

## Positioning Data

**ledger_positioned_nodes.jsonl Structure:**
```json
{"id": "header_title", "x": 15, "y": 15, "width": 950, "height": 50}
{"id": "toggle_sidebar", "x": 1150, "y": 15, "width": 35, "height": 35}
{"id": "btn_dashboard_0", "x": 5, "y": 110, "width": 195, "height": 45}
{"id": "btn_dashboard_1", "x": 5, "y": 160, "width": 195, "height": 45}
...14 total nodes...
```

Both apps apply positioning identically via:
- `ledger._apply_absolute_positioning(nodes)`
- Falls back to computed layout if node not in positioned ledger

## Compliance Model

Both frontends implement:
✅ **Pure Pattern:** No business logic, only presentation
✅ **Ledger-Driven:** All state from ledger queries
✅ **Deterministic:** Same input → same output (ledger state)
✅ **Incremental:** Only render/transmit what changed

## Testing the Architecture

### 1. Start HTTP Server
```bash
python jarvis_v3.py
# Listens on port 8000
```

### 2. Start Canvas Server
```bash
python jarvis_canvas_ledger_driven.py
# Opens Tkinter window
```

### 3. Click same button in both interfaces
- Should trigger same backend change
- Both should show same new view
- Canvas should show only incremental changes

### 4. Verify ledger queries
```python
from ledger_query import LedgerQuery
ledger = LedgerQuery(".")
frame = ledger.get_frame_for_view("dashboard_1")
# Same frame in both HTTP and canvas
```

## Summary

**Before:** 
- HTTP used `ufm_kernel` (kernel-based heartbeat architecture)
- Canvas used `ledger_query` (ledger-based queries)
- Different business logic paths

**After:**
- Both use `ledger_query` exclusively
- Both call identical methods: `get_frame_for_view()`, `record_button_click()`
- HTTP: stateless translator (HTTP ↔ Ledger)
- Canvas: stateful renderer (incremental painting)
- Same backend = consistent application behavior
- Different rendering strategies = optimized for each platform
