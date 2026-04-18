# Complete Example: Ledger-Driven Configuration Workflow

## Scenario: Change App Theme from Blue to Green

### Initial State
- App running with blue theme
- All config stored in `ledger_config.jsonl`
- No Python code changes needed

### Step 1: Identify Current Colors

**Current `ledger_config.jsonl` colors:**
```json
{"type": "COLOR_DEFINITION", "id": "bg", "hex": "#1a1a1a", "comment": "Main background - dark"}
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#1565c0", "comment": "Button background - BLUE"}
{"type": "COLOR_DEFINITION", "id": "header", "hex": "#0d47a1", "comment": "Header background - BLUE"}
{"type": "COLOR_DEFINITION", "id": "accent", "hex": "#64b5f6", "comment": "Accent color - LIGHT BLUE"}
```

### Step 2: Edit Configuration File

**WHERE:** `c:\Determined\src\applications\ledger_config.jsonl`

**WHAT TO CHANGE:** Replace blue hex codes with green hex codes

```json
{"type": "COLOR_DEFINITION", "id": "bg", "hex": "#1a1a1a", "comment": "Main background - dark"}
{"type": "COLOR_DEFINITION", "id": "button_bg", "hex": "#00aa00", "comment": "Button background - GREEN"}
{"type": "COLOR_DEFINITION", "id": "header", "hex": "#006600", "comment": "Header background - DARK GREEN"}
{"type": "COLOR_DEFINITION", "id": "accent", "hex": "#00ff00", "comment": "Accent color - BRIGHT GREEN"}
```

**That's it. No other changes needed.**

### Step 3: Restart Application

```bash
cd c:\Determined\src\applications
python jarvis_canvas_ledger_driven.py
```

### Step 4: Observe Changes

✅ All buttons render with green background (#00aa00)
✅ Header renders with dark green (#006600)
✅ Accent colors are bright green (#00ff00)
✅ Background remains unchanged (#1a1a1a)

### Result

**Complete theme change with ZERO code edits.**

---

## Scenario 2: Add New Large Font

### Current State
- App needs a new "banner" font (huge, bold)
- Want to use it on special headings

### Step 1: Add Font Definition

**EDIT:** `ledger_config.jsonl`

**ADD THIS LINE:**
```json
{"type": "FONT_DEFINITION", "id": "banner", "family": "Arial", "size": 36, "weight": "bold", "comment": "Large banner font"}
```

### Step 2: Use in UI

**In `ledger_buttons.jsonl` or dashboard spec:**
```json
{
  "id": "btn:special_title",
  "label": "IMPORTANT ANNOUNCEMENT",
  "size": "banner",
  "color": "accent"
}
```

### Step 3: Restart App

```bash
python jarvis_canvas_ledger_driven.py
```

### Result

✅ New button renders with large 36pt bold font
✅ No Python code changed
✅ Font automatically loaded from config

---

## Scenario 3: Create Custom Color Palette

### Current State
- Want to theme app for client branding
- Client wants purple and gold colors

### Step 1: Add Custom Colors

**EDIT:** `ledger_config.jsonl`

**ADD THESE LINES:**
```json
{"type": "COLOR_DEFINITION", "id": "brand_purple", "hex": "#6a0dad", "comment": "Client brand purple"}
{"type": "COLOR_DEFINITION", "id": "brand_gold", "hex": "#ffd700", "comment": "Client brand gold"}
{"type": "COLOR_DEFINITION", "id": "brand_light", "hex": "#f5e6d3", "comment": "Client brand light"}
```

### Step 2: Use in UI

**In button definitions:**
```json
{
  "id": "btn:branded",
  "label": "Brand Button",
  "bg": "brand_purple",
  "text": "brand_gold"
}
```

### Step 3: Restart App

```bash
python jarvis_canvas_ledger_driven.py
```

### Result

✅ Buttons render with client branding colors
✅ Completely customizable from ledger
✅ Same code runs for all clients

---

## Scenario 4: Dynamic Font Size Change

### Current State
- Monitor is high-resolution
- Need larger fonts for readability

### Step 1: Modify Font Definitions

**EDIT:** `ledger_config.jsonl`

**CHANGE THIS:**
```json
{"type": "FONT_DEFINITION", "id": "normal", "family": "Arial", "size": 10, "weight": "normal"}
{"type": "FONT_DEFINITION", "id": "header", "family": "Arial", "size": 12, "weight": "bold"}
```

**TO THIS:**
```json
{"type": "FONT_DEFINITION", "id": "normal", "family": "Arial", "size": 14, "weight": "normal"}
{"type": "FONT_DEFINITION", "id": "header", "family": "Arial", "size": 18, "weight": "bold"}
```

### Step 2: Restart App

```bash
python jarvis_canvas_ledger_driven.py
```

### Result

✅ All text renders 40% larger
✅ All buttons use new sizes automatically
✅ No code changes needed

---

## Scenario 5: Add Accessibility Theme

### Current State
- Need high-contrast mode for accessibility
- Want to preserve normal theme for others

### Step 1: Create New View Config

**EDIT:** `ledger_config.jsonl`

**ADD THIS:**
```json
{"type": "VIEW_CONFIG", "view_id": "menu_accessible", "enable_sidebar": true, "enable_header": true, "background": "bg", "accessibility": true}
```

### Step 2: Add High-Contrast Colors

**ADD THESE:**
```json
{"type": "COLOR_DEFINITION", "id": "bg_accessible", "hex": "#000000", "comment": "Pure black background"}
{"type": "COLOR_DEFINITION", "id": "text_accessible", "hex": "#ffffff", "comment": "Pure white text"}
{"type": "COLOR_DEFINITION", "id": "button_accessible", "hex": "#ffff00", "comment": "Bright yellow buttons"}
```

### Step 3: Add Large Accessible Fonts

**ADD THESE:**
```json
{"type": "FONT_DEFINITION", "id": "normal_accessible", "family": "Arial", "size": 16, "weight": "normal"}
{"type": "FONT_DEFINITION", "id": "header_accessible", "family": "Arial", "size": 22, "weight": "bold"}
```

### Step 4: Switch Views

In `ledger_app_state.jsonl`, change:
```json
{"current_view": "menu_accessible"}
```

### Result

✅ App switches to high-contrast theme
✅ Larger fonts for readability
✅ Pure black/white for accessibility
✅ No code changes needed

---

## How Query Engine Works (Behind the Scenes)

### When App Starts

```python
ledger = LedgerQuery()
# Loads ledger_config.jsonl
# Parses fonts → self.fonts = {id: {family, size, weight}}
# Parses colors → self.colors = {id: hex}
# Parses layouts → self.layouts = {id: config}
# Prints: "[LEDGER] UI Config: 5 fonts, 10 colors, 3 layouts"
```

### When Renderer Initializes

```python
renderer = CanvasRenderer(canvas, ledger)
# Loads all fonts from ledger
# Loads all colors from ledger
# Prints: "[RENDERER] Loaded 5 fonts and 10 colors from ledger"
```

### When Frame Renders

```python
while app_running:
    view = ledger.get_current_view()    # Query current view
    frame = ledger.get_frame_for_view(view)  # Get frame spec
    
    # Renderer uses ledger to look up fonts/colors
    font = ledger.get_font("title")      # Query font
    color = ledger.get_color("button_bg")  # Query color
    
    renderer.render_frame(frame)  # Paint with queried config
    time.sleep(0.1)  # 10Hz tick
```

### All Queries Are From Ledger

```
Edit ledger file
    ↓
Restart app
    ↓
ledger._load_config() reads new file
    ↓
get_font() /get_color() return new values
    ↓
Renderer paints with new config
    ↓
See changes on screen
```

---

## File Format Reference

### Font Definition
```json
{"type": "FONT_DEFINITION", "id": "FONT_ID", "family": "Arial", "size": 12, "weight": "bold", "comment": "Description"}
```

Valid weights: `normal`, `bold`

### Color Definition
```json
{"type": "COLOR_DEFINITION", "id": "COLOR_ID", "hex": "#RRGGBB", "comment": "Description"}
```

Hex format: `#000000` to `#FFFFFF`

### Layout Definition
```json
{"type": "LAYOUT_DEFINITION", "id": "LAYOUT_ID", "property": "value", "comment": "Description"}
```

Variables: `pixels`, `columns`, `rows`, `gutter` - use as needed

### View Config
```json
{"type": "VIEW_CONFIG", "view_id": "VIEW_ID", "property": "value", "comment": "Description"}
```

Variables: `enable_sidebar`, `enable_header`, `background`, custom flags

---

## Summary: Complete Control Without Code

✅ **Change anything** by editing JSON files  
✅ **No Python knowledge** required  
✅ **Restart app** to apply changes  
✅ **Infinite variations** from one codebase  

**The ledger is supreme. The code stays the same.**
