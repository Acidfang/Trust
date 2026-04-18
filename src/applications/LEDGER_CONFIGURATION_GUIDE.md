# Ledger-Driven Canvas App Configuration Guide

## Overview

`jarvis_canvas_ledger_driven.py` is a **pure translator** application:
- **Input:** Frame specifications from `ledger_config.jsonl`
- **Output:** Canvas rendering
- **State:** All stored in ledger files

**KEY PRINCIPLE:** Zero hardcoded values. All configuration comes from ledgers. You should NEVER edit the Python code again.

---

## How It Works

### 1. The App Queries Ledger Every 100ms

```
┌─────────────────────────────────────────┐
│ Main Tick Loop (100ms = 10Hz)           │
├─────────────────────────────────────────┤
│ 1. Query ledger: get_current_view()     │
│ 2. Query ledger: get_frame_for_view()   │
│ 3. Render frame ONLY if changed         │
│ 4. Loop again                           │
└─────────────────────────────────────────┘
```

### 2. Ledger Contains

**`ledger_config.jsonl`** — ALL UI configuration
- Font definitions (family, size, weight)
- Color palette (hex values)
- Layout specifications
- View configurations

**`ledger_app_state.jsonl`** — Current state
- `current_view` (which view to display)
- `sidebar_collapsed` (UI state)

**`ledger_dashboards.jsonl`** — View definitions
- What to display on each view
- Buttons, layouts, content

**`ledger_buttons.jsonl`** — Button specifications
- Button positions, labels, colors

### 3. Renderer Is Pure

The `CanvasRenderer` class:
- Takes ledger configuration on init
- Receives frame specs (node: type, position, content)
- Paints only
- Never decides, computes, or stores state

---

## How to Configure Everything

### Change Fonts

Edit `ledger_config.jsonl` — Add/update FONT_DEFINITION entries:

```json
{"type": "FONT_DEFINITION", "id": "title", "family": "Arial", "size": 18, "weight": "bold", "comment": "Main title font"}
{"type": "FONT_DEFINITION", "id": "header", "family": "Arial", "size": 14, "weight": "bold", "comment": "Header font"}
```

**Restart the app** and fonts are loaded from ledger.

---

### Change Colors

Edit `ledger_config.jsonl` — Add/update COLOR_DEFINITION entries:

```json
{"type": "COLOR_DEFINITION", "id": "bg", "hex": "#000000", "comment": "Main background"}
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#ff0000", "comment": "Button color"}
```

**Restart the app** and colors are loaded from ledger.

---

### Change Layout

Edit `ledger_config.jsonl` — Add/update LAYOUT_DEFINITION entries:

```json
{"type": "LAYOUT_DEFINITION", "id": "header_height", "pixels": 60, "comment": "New header height"}
{"type": "LAYOUT_DEFINITION", "id": "sidebar_width", "pixels": 250, "comment": "Wider sidebar"}
```

**Restart the app** and layouts are loaded from ledger.

---

### Change What Views Display

Edit `ledger_dashboards.jsonl` — Add/update dashboard entries:

```json
{"id": "dashboard:menu", "name": "Main Menu", "description": "Primary interface", "nodes": ["btn:start", "btn:settings"]}
```

This controls which buttons/content appear on which view.

---

### Add New Fonts on the Fly

Just add a line to `ledger_config.jsonl`:

```json
{"type": "FONT_DEFINITION", "id": "huge", "family": "Arial", "size": 24, "weight": "bold"}
```

Then in any button/text node, use `"size": "huge"` and it will render automatically.

---

### Add New Colors on the Fly

Just add a line to `ledger_config.jsonl`:

```json
{"type": "COLOR_DEFINITION", "id": "my_custom_color", "hex": "#aa00ff"}
```

Then in any button/text, use `"color": "my_custom_color"` and it will render automatically.

---

## Files You CAN Edit (No Code Restart Needed*)

(*After ledger reload)

| File | What to Edit | Effect |
|------|-------------|--------|
| `ledger_config.jsonl` | Fonts, colors, layouts, view configs | UI appearance |
| `ledger_app_state.jsonl` | `current_view` field | Which view displays |
| `ledger_dashboards.jsonl` | Button lists, content specs | View layout |
| `ledger_buttons.jsonl` | Button properties, labels | Button appearance |

## Files You Should NOT Edit

| File | Why |
|------|-----|
| `jarvis_canvas_ledger_driven.py` | Pure translator - config comes from ledger |
| `ledger_query.py` | Core engine - no UI decisions here |

---

## Configuration Workflow

**Step 1: Edit Ledger**
```
Open: ledger_config.jsonl
```

**Step 2: Update Font/Color/Layout**
```json
{"type": "FONT_DEFINITION", "id": "my_font", "family": "Courier", "size": 14, "weight": "bold"}
```

**Step 3: Run App**
```bash
python jarvis_canvas_ledger_driven.py
```

**Step 4: Observe Changes**
- App loads configuration from ledger
- Renders frame based on ledger specs
- All styling applied from ledger definitions

---

## Example: Complete Skinning

**Scenario:** Change entire theme from dark blue to green

**Edit `ledger_config.jsonl`:**

```json
{"type": "COLOR_DEFINITION", "id": "bg", "hex": "#0a0a0a", "comment": "Darker background"}
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#00aa00", "comment": "Green buttons"}
{"type": "COLOR_DEFINITION", "id": "accent", "hex": "#00ff00", "comment": "Green accents"}
{"type": "COLOR_DEFINITION", "id": "header", "hex": "#006600", "comment": "Dark green header"}
```

**Result:** Everything automatically updates to green theme on app restart.

---

## Example: New Font Size

**Scenario:** Add super-large headline font

**Edit `ledger_config.jsonl`:**

```json
{"type": "FONT_DEFINITION", "id": "banner", "family": "Arial", "size": 36, "weight": "bold"}
```

**Then in button:** Use `"size": "banner"` in the payload

**Result:** Any button using "banner" will render at 36pt bold.

---

## Debugging Configuration

**If fonts don't load:**
```python
# Check ledger output on startup:
# [RENDERER] Loaded X fonts and Y colors from ledger
```

**If colors are wrong:**
- Verify hex codes are valid: `#RRGGBB` format
- Check ledger_config.jsonl has valid JSON

**If layout is off:**
- Check `ledger_dashboards.jsonl` for button positions
- Edit coordinates directly in those entries

---

## API Reference: Ledger Query Methods

### Get Fonts

```python
ledger.get_font("title")  # Returns: {"family": "Arial", "size": 16, "weight": "bold"}
ledger.get_all_fonts()    # Returns: Dict of all fonts
```

### Get Colors

```python
ledger.get_color("bg")    # Returns: "#1a1a1a"
ledger.get_all_colors()   # Returns: Dict of all colors
```

### Get Layout

```python
ledger.get_layout("grid_main")  # Returns: Layout specification
```

### Get View Config

```python
ledger.get_view_config("menu")  # Returns: View configuration
```

---

## Complete Ledger Configuration Example

Here's what `ledger_config.jsonl` should contain:

```json
{"type": "FONT_DEFINITION", "id": "title", "family": "Arial", "size": 16, "weight": "bold"}
{"type": "FONT_DEFINITION", "id": "header", "family": "Arial", "size": 12, "weight": "bold"}
{"type": "FONT_DEFINITION", "id": "normal", "family": "Arial", "size": 10, "weight": "normal"}
{"type": "FONT_DEFINITION", "id": "small", "family": "Arial", "size": 8, "weight": "normal"}
{"type": "FONT_DEFINITION", "id": "mono", "family": "Courier", "size": 9, "weight": "normal"}

{"type": "COLOR_DEFINITION", "id": "bg", "hex": "#1a1a1a"}
{"type": "COLOR_DEFINITION", "id": "text", "hex": "#ffffff"}
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#1565c0"}
{"type": "COLOR_DEFINITION", "id": "accent", "hex": "#64b5f6"}

{"type": "LAYOUT_DEFINITION", "id": "header_height", "pixels": 50}
{"type": "LAYOUT_DEFINITION", "id": "sidebar_width", "pixels": 200}

{"type": "VIEW_CONFIG", "view_id": "menu", "enable_sidebar": true, "enable_header": true}
{"type": "VIEW_CONFIG", "view_id": "dashboard", "enable_sidebar": true, "enable_header": true}
```

---

## Summary: No Code Edits Needed

✅ Change fonts? Edit `ledger_config.jsonl`  
✅ Change colors? Edit `ledger_config.jsonl`  
✅ Change layouts? Edit `ledger_config.jsonl`  
✅ Change views? Edit `ledger_app_state.jsonl` or `ledger_dashboards.jsonl`  
✅ Add new elements? Add to appropriate ledger  

❌ Never edit Python files  
❌ Never edit renderer logic  
❌ All queries come from ledger  
❌ All rendering is pure translation  

**The code is complete. Use the ledgers.**
