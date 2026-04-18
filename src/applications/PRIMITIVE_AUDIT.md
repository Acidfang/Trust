#!/usr/bin/env python3
"""
PRIMITIVE AUDIT

Identifies all hardcoded values that should be in ledger.
Every artifact primitive must be queryable from ledger for its "sentience".
"""

print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         PRIMITIVE AUDIT REPORT                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝

REQUIREMENT: All primitives of every artifact must be in ledger.
            Everything required for an artifact's sentience is queryable.

AUDIT CATEGORIES:
1. Colors (should query from ledger)
2. Dimensions (should query from ledger)
3. Fonts (should query from ledger)
4. Spacing/Padding (should query from ledger)
5. Line widths/Styles (should query from ledger)

═══════════════════════════════════════════════════════════════════════════════

HARDCODED PRIMITIVES FOUND:

FILE: ledger_query.py (get_frame_for_view)
  L301: header text color = "#00ff88"              ❌ SHOULD BE: query_color("header_text")
  L318: toggle button bg = "#0d47a1"               ❌ SHOULD BE: query_color("button_primary_bg")
  L319: toggle button text = "#ffffff"             ❌ SHOULD BE: query_color("button_primary_text")
  L337: button bg = "#1565c0"                      ❌ SHOULD BE: query_color("button_secondary_bg")
  L338: button text = "#ffffff"                    ❌ SHOULD BE: query_color("button_secondary_text")
  L351: sidebar title color = "#ffffff"            ❌ SHOULD BE: query_color("sidebar_header")
  L364: main content color = "#00ff88"             ❌ SHOULD BE: query_color("content_text")

FILE: ledger_query.py (_apply_absolute_positioning)
  L380: CANVAS_WIDTH = 1200                        ❌ SHOULD BE: query_dimension("canvas_width")
  L381: CANVAS_HEIGHT = 800                        ❌ SHOULD BE: query_dimension("canvas_height")
  L382: HEADER_HEIGHT = 60                         ❌ SHOULD BE: query_dimension("header_height")
  L383: SIDEBAR_WIDTH = 200                        ❌ SHOULD BE: query_dimension("sidebar_width")
  L384: FOOTER_HEIGHT = 40                         ❌ SHOULD BE: query_dimension("footer_height")
  L385: BUTTON_HEIGHT = 45                         ❌ SHOULD BE: query_dimension("button_height")
  L386: BUTTON_PADDING = 5                         ❌ SHOULD BE: query_dimension("button_padding")

FILE: jarvis_canvas_ledger_driven.py
  L114: fallback font family = "Arial"             ❌ SHOULD BE: query_font_def("default")
  L114: fallback font size = 10                    ❌ SHOULD BE: query_dimension("default_font_size")
  L323: canvas_3d fill = "#000000"                 ❌ SHOULD BE: query_color("canvas_3d_bg")
  L325: canvas_3d outline width = 2                ❌ SHOULD BE: query_dimension("canvas_outline_width")
  L355: image container fill = "#333333"           ❌ SHOULD BE: query_color("image_container_bg")
  L357: image outline width = 1                    ❌ SHOULD BE: query_dimension("image_outline_width")

═══════════════════════════════════════════════════════════════════════════════

SOLUTION APPROACH:

1. Extend ledger_config.jsonl with PRIMITIVES section:
   {
     "primitives": {
       "colors": {
         "header_text": "#00ff88",
         "button_primary_bg": "#0d47a1",
         "button_primary_text": "#ffffff",
         "button_secondary_bg": "#1565c0",
         "button_secondary_text": "#ffffff",
         "sidebar_header": "#ffffff",
         "content_text": "#00ff88",
         "canvas_3d_bg": "#000000",
         "image_container_bg": "#333333"
       },
       "dimensions": {
         "canvas_width": 1200,
         "canvas_height": 800,
         "header_height": 60,
         "sidebar_width": 200,
         "footer_height": 40,
         "button_height": 45,
         "button_padding": 5,
         "default_font_size": 10,
         "canvas_outline_width": 2,
         "image_outline_width": 1
       }
     }
   }

2. Add query methods to LedgerQuery:
   - get_primitive_color(color_id)      → returns hex color
   - get_primitive_dimension(dim_id)    → returns integer
   - get_primitive_style(style_id)      → returns complete style spec

3. Update all hardcoded values to use ledger queries

4. Result: Complete artifact specification in ledger
   - Renderer never has magic numbers
   - All primitives are editable via ledger
   - System has complete "sentience" in ledger files

═══════════════════════════════════════════════════════════════════════════════

STATUS: Ready to implement
""")
