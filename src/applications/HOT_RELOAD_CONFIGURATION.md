# Hot-Reload Configuration System

## ⚡ No Restart Required

The canvas app now supports **live configuration reloading**. Change ledger files and see results immediately.

---

## How It Works

### Architecture

```
Edit ledger_config.jsonl
            ↓
App running (10Hz tick loop)
            ↓
Every 3 seconds: Hot-reload check
            ↓
If config changed: Reload fonts/colors
            ↓
Next frame renders with new config
```

### The Process

1. **Ledger files are monitored** - Every 3 seconds the app checks `ledger_config.jsonl`
2. **Config reloads automatically** - If file changed, config is reloaded into memory
3. **Next frame reflects changes** - On next render tick, new config is used
4. **No app restart needed** - Everything stays running

---

## Quick Start

### 1. Start the App

```bash
python jarvis_canvas_ledger_driven.py
```

You'll see:
```
[JARVIS] Starting Pure Ledger-Driven Canvas App
[JARVIS] Configuration hot-reload enabled (every 3 seconds)
```

### 2. Make a Change

Edit `ledger_config.jsonl` while app is running:

**Change this:**
```json
{"type": "COLOR_DEFINITION", "id": "bg", "hex": "#1a1a1a"}
```

**To this:**
```json
{"type": "COLOR_DEFINITION", "id": "bg", "hex": "#000000"}
```

Save the file.

### 3. Wait 3 Seconds

The app automatically detects the change:
```
[HOT-RELOAD] Config reloaded: 5 fonts, 10 colors
```

### 4. See Changes

Next render cycle shows the new background color. **No restart needed.**

---

## Supported Hot-Reload Changes

### ✅ Change Colors
```json
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#ff0000"}
```
Changes apply in next render cycle (~100ms).

### ✅ Change Fonts
```json
{"type": "FONT_DEFINITION", "id": "header", "family": "Arial", "size": 18, "weight": "bold"}
```
Changes apply in next render cycle.

### ✅ Add New Colors
```json
{"type": "COLOR_DEFINITION", "id": "my_color", "hex": "#00ff00"}
```
New color available immediately, renders on next use.

### ✅ Add New Fonts
```json
{"type": "FONT_DEFINITION", "id": "my_font", "family": "Courier", "size": 14, "weight": "bold"}
```
New font available immediately.

### ✅ Modify Layouts
```json
{"type": "LAYOUT_DEFINITION", "id": "header_height", "pixels": 60}
```
New layout values available on next reference.

### ✅ Change View Configs
```json
{"type": "VIEW_CONFIG", "view_id": "menu", "enable_sidebar": false}
```
Configuration changes detected on next view render.

---

## Reload Behavior

### Automatic (Default)

Hot-reload runs automatically every 3 seconds (30 ticks at 10Hz).

**Console output:**
```
[HOT-RELOAD] Config reloaded: 5 fonts, 10 colors
```

This appears periodically even if nothing changed (reload still runs, config stays same).

### What Gets Reloaded?

1. **Fonts** - All font definitions
2. **Colors** - All color definitions
3. **Layouts** - All layout specifications
4. **View Configs** - All view configurations

### What Doesn't Require Reload?

- **Button positions** - In `ledger_buttons.jsonl` (already queried per frame)
- **Current view** - In `ledger_app_state.jsonl` (queried per frame)
- **Frame content** - In `ledger_dashboards.jsonl` (queried per frame)

These are already dynamic and don't need reloading.

---

## Example Workflow: Live Theme Testing

### Step 1: Start App

```bash
python jarvis_canvas_ledger_driven.py
```

App running with default blue theme.

### Step 2: Edit ledger_config.jsonl (While App Running)

Change all blues to greens:

```json
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#00aa00"}
{"type": "COLOR_DEFINITION", "id": "header", "hex": "#006600"}
{"type": "COLOR_DEFINITION", "id": "accent", "hex": "#00ff00"}
```

Save file.

### Step 3: Wait 3 Seconds

Console shows:
```
[HOT-RELOAD] Config reloaded: 5 fonts, 10 colors
```

### Step 4: Observe

App now renders with green theme. Try more changes!

### Step 5: Iterate

Edit again:
```json
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#ff6600"}
```

Wait 3 seconds → Orange buttons appear.

No restart needed. Ever.

---

## Advanced: Manual Reload

If you want to reload NOW instead of waiting 3 seconds:

```python
# In custom code that has access to renderer:
result = renderer.reload_fonts_and_colors()
print(result)
# Output: {'status': 'success', 'fonts': 5, 'colors': 10, 'ledger_config': {...}}
```

---

## Configuration Files (All Live-Hot-Reloadable)

| File | What Changes | When Applied |
|------|--------------|--------------|
| `ledger_config.jsonl` | Fonts, colors, layouts | Every 3 seconds |
| `ledger_app_state.jsonl` | Current view | Every frame |
| `ledger_dashboards.jsonl` | View content | Every frame |
| `ledger_buttons.jsonl` | Button specs | Every frame |

**Key Point:** The ones that need reload (config) reload every 3s. The ones that don't (state, content) are queried every frame.

---

## Performance Impact

- **Minimal** - Reload only happens once every 3 seconds
- **Fast** - File read + JSON parse takes <1ms
- **Non-blocking** - Reload happens in main tick loop, doesn't freeze UI
- **Memory efficient** - Old fonts/colors cleaned up before reload

---

## Troubleshooting

### "No hot-reload messages in console"

**Check:**
1. App is actually running
2. Not seeing messages because they're printed every 3 seconds

**Solution:** Make a change to `ledger_config.jsonl` and you'll see the reload message and the change applied.

### "Changed file but nothing happened"

**Check:**
1. Did you save the file?
2. Is JSON syntax valid? (missing commas, quotes?)
3. Waited at least 3 seconds?

**Solution:**
- Save explicitly
- Validate JSON (check for syntax errors)
- Wait full 3 seconds for next reload cycle

### "Colors changed but fonts didn't"

**Possible:**
- You edited a font but need to use it somewhere
- Fonts reload but aren't used until referenced

**Solution:**
- Make sure elements actually use the font you changed
- Check `ledger_buttons.jsonl` references the font ID

---

## Implementation Details

### How Hot-Reload Works

1. **Tick counter** - Increments each app tick (every 100ms)
2. **Every 30 ticks** (3 seconds) - Calls `reload_fonts_and_colors()`
3. **Reload method** - Clears old config, calls `ledger.reload_config()`
4. **Ledger re-reads** - `ledger_config.jsonl` parsed again
5. **New fonts created** - Tkinter Font objects recreated with new specs
6. **Old fonts cleaned** - Previous Font objects deleted to free memory
7. **Next render** - Uses new config automatically

### Why No Restart?

- **Stateless config** - Configuration is independent data, not baked into code
- **Queryable** - App queries config every time it needs it
- **Replaceable** - Old fonts/colors deleted and recreated without stopping app
- **Frame-based** - Each render cycle checks what config it needs

---

## Comparison: Before vs. After

### Before (Old Way)
```
Edit Python code → Restart app → Load config → See changes
[5 minutes]
```

### After (Hot-Reload)
```
Edit JSON file → Wait 3 seconds → See changes
[~5 seconds]
```

---

## Summary

✅ **No restarts needed**  
✅ **Changes apply automatically**  
✅ **Every 3 seconds checked**  
✅ **All config types supported**  
✅ **Zero downtime**  
✅ **Live testing workflow**  

**Edit → Wait 3 seconds → See changes.**

The app never stops. The config never requires restart.
