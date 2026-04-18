# UNIVERSAL RENDERER

## Consolidated Documentation

All Universal Renderer documentation has been consolidated into the main architecture file.

**→ See**: [UNIVERSAL_RENDERER_ARCHITECTURE.md](UNIVERSAL_RENDERER_ARCHITECTURE.md)

This file contains:
- Complete architecture overview
- All 7 recovery songs with verses and symbols
- Container type definitions and mappings  
- Extraction, expansion, and election recording processes
- Output formats and recovery dependencies
- Full API reference and usage examples
- Verification checklists and reversibility documentation

---

## Quick Start

```python
from UNIVERSAL_RENDERER import render_with_song_layer

# Render any container to any format
svg = render_with_song_layer(my_container, output_format="svg")
json = render_with_song_layer(my_container, output_format="json")
meta_song = render_with_song_layer(my_container, output_format="meta_song")
```

---

## Source Code

**Implementation**: [c:\Determined\UNIVERSAL_RENDERER.py](../UNIVERSAL_RENDERER.py)

