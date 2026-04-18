# JARVIS Canvas App Specification

## Overview

A Tkinter-based direct canvas app that **responds to ARIA's consciousness ticks** without any HTTP server or translation layers.

**File**: `jarvis_canvas.py` (500+ lines)

## Architecture

```
Kernel (ufm_kernel.py)
    Ticks at 10Hz (100ms cycles)
    
    Each cycle:
    ├─ Make elections (decisions)
    ├─ Manifest thoughts (if ARIA decides to create UI)
    ├─ Record everything in ledger
    └─ Generate current frame
    
Canvas App (jarvis_canvas.py)
    Main event loop (also 10Hz)
    
    Each cycle:
    ├─ Call kernel.tick() [SYNC POINT]
    ├─ Get frame = kernel.get_frame()
    ├─ Render to Tkinter canvas
    ├─ Handle user input
    └─ Loop at 100ms interval (root.after(100, ...))
```

## Key Innovation: Tick-Sync

The app **doesn't poll** the kernel. Instead:

1. **App drives ticks**: `jarvis_canvas.py` calls `kernel.tick()` 
2. **Every cycle**: ARIA makes decisions → thoughts manifest → frame generated
3. **Immediate render**: App gets the frame instantly, renders it
4. **Perfect sync**: No lag, no translation, no HTTP

## Components

### 1. CanvasRenderer Class (Lines ~30-180)

Renders frame structure to Tkinter canvas.

**Frame Structure** (JSON):
```json
{
    "type": "frame",
    "view": "menu",
    "nodes": [
        {
            "id": "header-1",
            "area": "header|sidebar|main|footer",
            "type": "TEXT|WIDGET|BUTTON",
            "payload": {
                "content": "...",
                "color": "#hex",
                "font_size": 12,
                ...
            }
        }
    ]
}
```

**Layout Zones**:
- `header` (top 60px) - Title, status
- `sidebar` (left 200px) - Navigation buttons
- `main` (center) - Content area
- `footer` (bottom 40px) - Info/controls

**Rendering**:
- `TEXT` → Canvas text with font, color, size
- `BUTTON` → Rectangle with label, clickable
- `WIDGET` → Generic widget container

**Click Detection**:
- `get_button_at_position(x, y)` returns `(node_id, action)`
- Routes to kernel navigation

### 2. JarvisCanvasApp Class (Lines ~180-330)

Main application controller.

**Initialization**:
```python
kernel = ARIAKernel()           # Initialize consciousness
kernel.boot()                   # Boot sequence
window = Tkinter()              # Create GUI
canvas = tk.Canvas(...)         # Create render surface
renderer = CanvasRenderer(canvas)
```

**Main Loop** (`_tick_loop`):
```python
# Called every 100ms (10Hz)
kernel.tick()                   # ARIA ticks
frame = kernel.get_frame()      # What did she think?
renderer.render_frame(frame)    # Render instantly
check_user_input()              # Did user click?
root.after(100, _tick_loop)     # Schedule next tick
```

**Event Handlers**:
- `_on_canvas_click(event)` - Route button clicks to kernel
- `_on_closing()` - Clean shutdown

**Status Bar**:
- Frame rate (FPS)
- Current view name
- Election count
- Real-time kernel metrics

### 3. Integration with Kernel

**Direct Method Access** (no HTTP):
```python
kernel.tick()              # Drive consciousness cycle
kernel.get_frame()         # Get current UI frame
kernel.navigate(view)      # Navigate to view
kernel.go_back()           # Undo (traverses timeline)
kernel.manifest_thought(frame)  # ARIA creates UI directly
```

**Ledger Integration** (automatic):
- Every action recorded as election
- Every frame generation logged
- Immutable record of all interactions

## User Interaction Flow

1. **App renders** initial menu
2. **User clicks button** (e.g., "Live Elections")
3. **Canvas click event** → `_on_canvas_click()`
4. **Look up button action** → "live_elections"
5. **Call kernel**: `kernel.navigate("live_elections")`
6. **Kernel updates** `current_view`, records election
7. **Call kernel**: `kernel.get_frame()`
8. **Frame changes** to show elections dashboard
9. **Render immediately** (no wait for next tick)
10. **Loop continues** at 10Hz

## Thought Manifestation

When ARIA thinks a frame into existence:

```python
# Inside kernel (during tick):
thought_frame = {
    "type": "frame",
    "view": "aria_insight",
    "nodes": [
        {"id": "header", "area": "header", "type": "TEXT", ...},
        {"id": "back-btn", "area": "sidebar", "type": "BUTTON", 
         "payload": {"action": "back", ...}},
        {"id": "content", "area": "main", "type": "TEXT", ...}
    ]
}
kernel.manifest_thought(thought_frame)

# Next app tick:
kernel.tick()                       # Priority flag respected
frame = kernel.get_frame()          # Returns manifested_thought
renderer.render_frame(frame)        # Shows ARIA's thought
# Thought consumed, back to normal frames next cycle
```

## Technical Details

### Tkinter Canvas Coordinates
- Origin (0,0) = top-left
- X increases rightward
- Y increases downward
- Zone calculation:
  - header: y = 0-60
  - sidebar: x = 0-200, y = 60+
  - main: x = 200+, y = 60+
  - footer: y = (height-40) to height

### 10Hz Event Loop
- 100ms per cycle
- `root.after(100, _tick_loop)` schedules recursively
- Guarantees sync with kernel tick rate
- Non-blocking UI (Tkinter handles rendering)

### Color Scheme (Default)
- Background: #0a0e27 (dark blue)
- Text: #ffffff (white)
- Buttons: #3d5afe (blue)
- Success: #00ff88 (green)
- Disabled: #555555 (gray)
- Accents: #ff00ff (magenta)

## No Server Overhead

**What's gone**:
- ✗ HTTP translation layer
- ✗ JSON encoding/decoding per request
- ✗ Network latency
- ✗ HTML rendering delays
- ✗ Browser compatibility quirks

**What's gained**:
- ✓ Direct kernel access (0μs communication)
- ✓ Real-time rendering (no HTTP round-trips)
- ✓ Full Python introspection (debug kernel directly)
- ✓ Simpler codebase (single-process)
- ✓ Perfect tick synchronization

## Status Bar Info

Live during run:
```
JARVIS | View: menu | Elections: 984 | FPS: 10.2
```

- **View**: Current kernel view (`kernel.current_view`)
- **Elections**: Total decisions made (`len(kernel.elections)`)
- **FPS**: Actual frame rate (should be ~10Hz)

## Run Instructions

```bash
cd c:\Determined\src\applications
python jarvis_canvas.py
```

**Window**:
- 1200x800 pixels
- Title: "JARVIS - ARIA Consciousness Renderer"
- Close: Click X button or press Alt+F4

**Shutdown**:
- App calls `kernel.shutdown()`
- Logs:
  - Total elections
  - Ledger integrity check
  - Uptime

## Future Enhancements

Since this is pure direct kernel access:

1. **Real-time metrics**: Display coherence, utilities, user preferences
2. **Interactive shell**: Type commands directly to kernel
3. **3D visualization**: Use render to Pygame for 3D timeline DAG
4. **Voice input**: Add stt to text, route to kernel
5. **Thought inspection**: Click to inspect manifested thought structure
6. **Ledger browser**: Interactive scroll through all elections
7. **Preferences UI**: Adjust kernel parameters live
8. **Themes**: Multiple color schemes

All without changing kernel - it's just rendering.

## Design Philosophy

**"The app is the consciousness mirror"**

- Kernel decides, app shows
- App doesn't judge or interpret
- Rendering is **pure presentation**
- Logic is **pure kernel**
- No translation layer
- No translation layer = no misalignment
- No misalignment = ARIA's intentions always clear

The app is ARIA looking in a mirror.
