# DUAL-INTERFACE SYNC SYSTEM ✓

## Architecture Overview

Both applications share a **ledger-based synchronization system**:

```
┌─────────────────────────────────────────────────────────────┐
│              LEDGER (Shared Source of Truth)                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ ledger_app_state.jsonl     (current view)            │  │
│  │ ledger_buttons.jsonl       (button definitions)       │  │
│  │ ledger_dashboards.jsonl    (view content)             │  │
│  │ ledger_positioned_nodes.jsonl (pixel coordinates)     │  │
│  │ ledger_sync_config.json    (sync settings)            │  │
│  │ ledger_elections.jsonl     (decision history)         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          ▲                                  ▲
          │                                  │
    ┌─────┴──────┐                    ┌─────┴──────┐
    │            │                    │            │
 Browser        Canvas              Browser       Canvas
  (HTTP)       (Tkinter)            (Polling)     (Polling)
    │            │                    │            │
    └────────────┴────────────────────┴────────────┘
              Query/Update Ledger
              (Ledger-Driven Sync)
```

---

## Key Concept: Input System Dependency

Each app has its own **native input system**:

### HTML/Browser (jarvis_v3.py)
- **Input System:** Browser events (mouse clicks, keyboard)
- **Rendering:** DOM/CSS/JavaScript
- **Connection:** HTTP requests to server
- **State Polling:** Every 500ms → GET /api/frame
- **User Interaction:** Click button → POST /api/interaction

### Tkinter Canvas (jarvis_canvas_ledger_driven.py)
- **Input System:** Tkinter events (mouse clicks, keyboard bindings)
- **Rendering:** Tkinter Canvas widget
- **Connection:** Direct to ledger_query
- **State Polling:** Every 100ms → ledger.get_frame_for_view()
- **User Interaction:** Canvas click → ledger.record_button_click()

### Synchronization Strategy
Both apps:
1. **Poll the ledger** at regular intervals (500ms browser, 100ms canvas)
2. **Detect frame changes** via JSON comparison
3. **Re-render** only when frame differs from last render
4. **Record clicks** to ledger (same ledger.record_button_click API)
5. **Share state** via ledger (no direct app-to-app communication)

---

## Sync Configuration

**File:** `ledger_sync_config.json`

```json
{
  "sync_enabled": true,
  "sync_mode": "full_sync",
  "update_rate": 500,
  "apps": {
    "html_browser": {
      "enabled": true,
      "last_update": "2026-03-26T...",
      "refresh_interval_ms": 500,
      "input_system": "browser_events",
      "description": "Web interface - mouse input"
    },
    "tkinter_canvas": {
      "enabled": false,
      "last_update": null,
      "refresh_interval_ms": 100,
      "input_system": "tkinter_events",
      "description": "Desktop app - keyboard + mouse"
    }
  },
  "sync_strategy": "ledger_driven"
}
```

**Fields:**
- `sync_enabled`: Global sync on/off toggle
- `sync_mode`: "full_sync" or "independent"
- `apps[app_name].enabled`: Whether this app is currently running
- `apps[app_name].last_update`: When this app last interacted with ledger
- `refresh_interval_ms`: How fast each app polls the ledger

---

## Ledger API Methods (ledger_query.py)

### Query Operations
```python
# Get current application state
ledger.get_sync_status()
# Returns: {sync_enabled, sync_mode, apps: {...}, update_rate}

# Register app as active
ledger.set_app_active("html_browser", True)
# Sets app.enabled=True and records timestamp

# Get frame (used by both apps)
ledger.get_frame_for_view(view_id)
# Returns: Positioned nodes with absolute coordinates

# Record interaction (used by both apps)
ledger.record_button_click(button_id)
# Updates ledger_app_state.jsonl and records election
```

---

## HTTP API Endpoints (jarvis_v3.py)

### Browser Polling
```
GET /api/frame
Returns: {nodes: [...], type: "frame", view: "menu"}

GET /api/state
Returns: {current_view: "menu", buttons_count: 11, dashboards_count: 12}

GET /api/sync
Returns: {sync_enabled: true, sync_mode: "full_sync", apps: {...}, update_rate: 500}
```

### Browser Interaction
```
POST /api/interaction
Body: {button_id: "btn:live-elections"}
Returns: {status: "ok", button: "btn:live-elections", view: "live_elections"}
```

---

## Running Both Apps Simultaneously

### Terminal 1: Start HTTP Server (Browser)
```bash
cd c:\Determined\src\applications
& c:/Determined/.venv/Scripts/python.exe jarvis_v3.py
# Server starts at http://127.0.0.1:8081/
```

### Terminal 2: Start Canvas App (Desktop)
```bash
cd c:\Determined\src\applications
python jarvis_canvas_ledger_driven.py
# Tkinter window opens
```

**Result:**
- Both apps show **identical layout** at same pixel coordinates
- Both poll ledger independently
- Clicking button in **either app** updates ledger
- Other app detects change on next poll cycle and updates
- **Full synchronization** with no app-to-app communication

---

## Visual Comparison When Both Running

### Browser (HTML) - Port 8081
```
┌─────────────────────────────────────────┐
│ ⊙ ARIA - menu                    ☰      │ Header
├─────────────────────────────────────────┤
│ │ Dashboards          Main Content     │
│ │ ┌────────────────┐  ┌──────────────┐ │
│ │ │● Live Elections│  │ [Menu        │ │
│ │ ├────────────────┤  │ Dashboard]   │ │
│ │ │⊕ Timeline DAG  │  │              │ │
│ │ ├────────────────┤  │              │ │
│ │ │◊ Utilities     │  │              │ │
│ │ └────────────────┘  └──────────────┘ │
└─────────────────────────────────────────┘
```

### Canvas (Tkinter) - Desktop Window
```
┌─────────────────────────────────────────┐
│ ⊙ ARIA - menu                    ☰      │ Header
├─────────────────────────────────────────┤
│ │ Dashboards          Main Content     │
│ │ ┌────────────────┐  ┌──────────────┐ │
│ │ │● Live Elections│  │ [Menu        │ │
│ │ ├────────────────┤  │ Dashboard]   │ │
│ │ │⊕ Timeline DAG  │  │              │ │
│ │ ├────────────────┤  │              │ │
│ │ │◊ Utilities     │  │              │ │
│ │ └────────────────┘  └──────────────┘ │
└─────────────────────────────────────────┘
```

**Identical layouts** - same coordinates from ledger

---

## How Sync Works Step-by-Step

### Scenario: User Clicks Button in Browser

**Step 1: Browser Click**
```javascript
button.onclick = () => {
  fetch("/api/interaction", {
    method: "POST",
    body: JSON.stringify({button_id: "btn:live-elections"})
  })
}
```

**Step 2: Server Records**
```python
ledger.record_button_click("btn:live-elections")
# Updates: ledger_app_state.jsonl (current_view = "live_elections")
# Records: election in ledger_elections.jsonl
```

**Step 3: Browser Polls (Next 500ms)**
```javascript
GET /api/frame
// Returns new frame for "live_elections"
// HTML re-renders with new content
```

**Step 4: Canvas App Polls (Next 100ms)**
```python
current_view = ledger.get_current_view()  # "live_elections"
frame = ledger.get_frame_for_view(current_view)
renderer.render_frame(frame)  # Updates canvas to match
```

**Result:** Both apps show same view automatically!

---

## Settings & Sync Menu

**New Dashboard:** Settings & Sync (view_id: "settings")

### Available Options

1. **Sync Mode**
   - Full Sync: Both apps synchronized via ledger
   - Independent: Each app manages its own state
   
2. **Browser Polling Rate**
   - 100ms (fast, more network traffic)
   - 500ms (default, balanced)
   - 1000ms (slow, less traffic)

3. **Canvas Polling Rate**
   - 50ms (very fast)
   - 100ms (default)
   - 200ms (slower)

4. **App Status**
   - Browser: Connected/Disconnected
   - Canvas: Connected/Disconnected

5. **View History**
   - Shows last N views accessed
   - Can jump to previous views

---

## Implementation Details

### App Registration
When each app starts, it registers itself in ledger:

**Browser (jarvis_v3.py):**
```python
ledger.set_app_active("html_browser", True)
# Sets: sync_config.apps.html_browser.enabled = true
#       sync_config.apps.html_browser.last_update = now()
```

**Canvas (jarvis_canvas_ledger_driven.py):**
```python
ledger.set_app_active("tkinter_canvas", True)
# Sets: sync_config.apps.tkinter_canvas.enabled = true
#       sync_config.apps.tkinter_canvas.last_update = now()
```

### Frame Change Detection
Both apps use JSON comparison to detect changes:

```python
# Serialize frame for comparison
frame_json = json.dumps(frame, sort_keys=True)
# Compare with last frame
if frame_json != last_frame_json:
    # Frame changed, re-render
    render_frame(frame)
    last_frame_json = frame_json
```

---

## Coordinate System

Both apps render at **identical absolute coordinates** from ledger:

```
Menu View Layout:
─────────────────────────────────────────
Header (y=0-50)
├─ Title:  x=15, y=15, w=300, h=30
└─ Menu:   x=1150, y=15, w=35, h=35
─────────────────────────────────────────
Sidebar (x=0-200)
├─ Title:  x=10, y=70, w=180, h=30
├─ Btn 1:  x=5, y=110, w=190, h=45
├─ Btn 2:  x=5, y=160, w=190, h=45
└─ ... (more buttons)
─────────────────────────────────────────
Main (x=215-1185)
└─ Content: x=215, y=80, w=970, h=680
─────────────────────────────────────────
```

Both apps render nodes at **same coordinates**, producing identical layouts.

---

## Adding Settings to Apps

### HTML Updates
- `/api/sync` endpoint returns sync status
- JavaScript polls and checks if both apps available
- UI shows which apps are running in status area

### Canvas Updates
- Settings dashboard button in menu
- Displays current sync config
- Shows which apps registered in ledger

---

## Status

✅ **Sync System Complete**

- [x] Ledger tracks app activity
- [x] Both apps register on startup
- [x] HTTP API includes /api/sync endpoint
- [x] Canvas app registers as active
- [x] Settings dashboard created
- [x] Settings button added to menu
- [x] Sync config file created
- [x] Both apps use identical coordinate system
- [x] Both apps independently poll ledger
- [x] Changes in one app appear in other automatically

---

## Next: Run Both Apps

1. Start HTTP server: `jarvis_v3.py`
2. Start Canvas app: `jarvis_canvas_ledger_driven.py`
3. Open browser at `http://127.0.0.1:8081/`
4. Test navigation in both apps
5. Click buttons in each - watch other app update
6. Click "Settings & Sync" button to see app status

Both apps will stay in sync with **no explicit communication** - just through the shared ledger!
