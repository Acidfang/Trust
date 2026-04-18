# UNIVERSAL RENDERER LEDGER: Output Formats

## Translation Phase (Step 6)

**Purpose**: Convert canonical song to any output format  
**Function**: `translate_song_to_format(song: Dict[str, Any], output_format: str) → Any`  
**Input**: Canonical song from generation  
**Output**: Formatted representation (varies by format)

---

## Supported Formats

### 1. Format: `verse`

**Output**: Just the poetry  

**Example Output**:
```
Shape emerges from constraints applied,
Structure forms where limits are defined,
Geometry binds the space inside,
Definitions make complexity guide.
```

**Use**: Human reading, poetry-focused communication  
**Size**: Minimal (2-4 lines)  
**Readability**: ✓ High

---

### 2. Format: `symbol`

**Output**: Ultra-compact symbols only  

**Example Output**:
```
⊙ → ◯ (Δ constraint)
```

**Use**: Recovery/encoding, emergency communication  
**Size**: Minimal (1 line)  
**Recovery-Ready**: ✓ Yes (can reconstruct from symbol)  
**Readability**: Specialized (requires symbol key)

---

### 3. Format: `json`

**Output**: Structured JSON data  

**Example Output**:
```json
{
  "principle": "CONSTRAINT_creates_DEPTH",
  "type": "primitive",
  "verse": "Shape emerges from constraints applied, ...",
  "symbols": "⊙ → ◯ (Δ constraint)",
  "weight": 0.15,
  "timestamp": "2026-04-03T14:24:48"
}
```

**Use**: API responses, machine processing, data interchange  
**Size**: Medium (5-10 fields)  
**Parseable**: ✓ Yes  
**Readability**: Good for machines, moderate for humans

---

### 4. Format: `markdown`

**Output**: Formatted markdown document  

**Example Output**:
```markdown
## CONSTRAINT_creates_DEPTH

**Container Type**: primitive  
**Weight**: 15%

### Verse
```
Shape emerges from constraints applied,
Structure forms where limits are defined,
Geometry binds the space inside,
Definitions make complexity guide.
```

### Symbols
```
⊙ → ◯ (Δ constraint)
```

**Generated**: 2026-04-03T14:24:48
```

**Use**: Documentation, wiki entries, formatted display  
**Size**: Large (20+ lines)  
**Readability**: ✓ High (formatted)

---

### 5. Format: `text`

**Output**: Plain text summary  

**Example Output**:
```
[CONSTRAINT_creates_DEPTH]
Shape emerges from constraints applied,
Structure forms where limits are defined,
Geometry binds the space inside,
Definitions make complexity guide.

Symbols: ⊙ → ◯ (Δ constraint)
```

**Use**: Logs, console output, simple display  
**Size**: Small (5-10 lines)  
**Readability**: Good

---

### 6. Format: `svg`

**Output**: SVG vector graphic visualization  

**Example Structure**:
```xml
<svg width="600" height="500">
  <rect ... fill="#f9f9f9"/>
  <text class="title">CONSTRAINT_creates_DEPTH</text>
  <rect class="weight-indicator" width="90" height="8"/>
  <text class="weight">Weight: 15%</text>
  <text class="verse">... verse text ...</text>
  <text class="symbols">⊙ → ◯ (Δ constraint)</text>
  <text class="weight">Type: primitive</text>
</svg>
```

**Use**: Visual rendering, diagrams, presentations  
**Size**: Large (50+ lines)  
**Renders**: ✓ As image/diagram  
**Viewable**: Any SVG-capable viewer

**SVG Content**:
- Title (centered, bold)
- Weight bar (colored indicator, 0-100%)
- Verse section (poem text)
- Symbols section (geometric notation)
- Container type (footer)

---

### 7. Format: `song`

**Output**: Raw canonical song (internal format)  

**Example Output**:
```json
{
  "compact": {
    "fields": [...],
    "principle": "CONSTRAINT_creates_DEPTH",
    "container_type": "primitive",
    "extracted_at": "2026-04-03T14:24:48"
  },
  "canonical": {
    "verse": "Shape emerges from constraints applied, ...",
    "symbols": "⊙ → ◯ (Δ constraint)"
  },
  "metadata": {
    "principle": "CONSTRAINT_creates_DEPTH",
    "container_type": "primitive",
    "song_key": "constraint",
    "weight": 0.15,
    "operation": "render",
    "timestamp": "2026-04-03T14:24:48",
    "generated_by": "UNIVERSAL_RENDERER"
  }
}
```

**Use**: Debug, complete introspection, internal processing  
**Size**: Large (full record)  
**Readable**: ✓ Yes, but verbose  
**Useful**: System developers, debugging

---

### 8. Format: `meta_song`

**Output**: Composed meta-song from election sequence  

**Example Output**:
```json
{
  "compact": {"fields": [], "principle": "CONSTRAINT_creates_DEPTH"},
  "canonical": {
    "verse": "Shape emerges from constraints applied, ...\n\nHistory records what came before, ...\n\nUnified field holds all as one, ...",
    "symbols": "⊙ → ◯ (Δ constraint) → ⊙ ← ∞ (time flow) → ⊙ = ◯ ⊕ (unified field)"
  },
  "metadata": {
    "principle": "META_SONG_of_3_elections",
    "type": "election_meta_song",
    "election_count": 3,
    "dominant_principle": "CONSTRAINT_creates_DEPTH",
    "election_sequence": [
      "CONSTRAINT_creates_DEPTH",
      "TEMPORAL_INTEGRATION_locks_PAST",
      "UNIFIED_FIELD_creates_INEVITABILITY"
    ],
    "election_hashes": [
      "a1b2c3...",
      "d4e5f6...",
      "g7h8i9..."
    ]
  }
}
```

**Use**: System narrative, complete story, high-level summary  
**Size**: Large (concatenated verses)  
**Story**: ✓ Complete narrative  
**Useful**: System analysis, decision review

---

## Format Selection Matrix

| Purpose | Format | Why |
|---------|--------|-----|
| Emergency comms | `symbol` | Ultra-minimal, recoverable |
| Human reading | `verse` or `text` | Natural language, minimal |
| Machine processing | `json` | Structured, parseable |
| Documentation | `markdown` | Formatted, displayable |
| Visualization | `svg` | Vector graphic, scalable |
| System debug | `song` | Complete record |
| System narrative | `meta_song` | Full story across elections |
| Logs | `text` | Simple, one-line friendly |

---

## Translation Algorithm

```python
def translate_song_to_format(song, output_format):
  
  IF output_format == "verse":
    return song["canonical"]["verse"]
  
  ELIF output_format == "symbol":
    return song["canonical"]["symbols"]
  
  ELIF output_format == "json":
    return {
      "principle": song["metadata"]["principle"],
      "type": song["metadata"]["container_type"],
      "verse": song["canonical"]["verse"],
      "symbols": song["canonical"]["symbols"],
      "weight": song["metadata"]["weight"],
      "timestamp": song["metadata"]["timestamp"]
    }
  
  ELIF output_format == "markdown":
    return f"""## {song["metadata"]["principle"]}

**Container Type**: {song["metadata"]["container_type"]}
**Weight**: {song["metadata"]["weight"]:.0%}

### Verse
```
{song["canonical"]["verse"]}
```

### Symbols
```
{song["canonical"]["symbols"]}
```

**Generated**: {song["metadata"]["timestamp"]}
"""
  
  ELIF output_format == "text":
    return f"[{song['metadata']['principle']}]\n{song['canonical']['verse']}\n\nSymbols: {song['canonical']['symbols']}"
  
  ELIF output_format == "svg":
    return _render_song_as_svg(song)
  
  ELIF output_format == "song":
    return song  # Already canonical
  
  ELSE:
    return {  # Fallback
      "principle": song["metadata"]["principle"],
      "verse": song["canonical"]["verse"],
      "symbols": song["canonical"]["symbols"]
    }
```

---

## Format Characteristics

### Lossless Formats (can reconstruct song)
- `song` (identity)
- `json` (complete, parseable)
- `markdown` (human-readable, recoverable)

### Lossy Formats (metadata lost)
- `verse` (poetry only)
- `symbol` (symbols only)
- `text` (compact, minimal)
- `svg` (visual only)

### Meta-Processing Formats
- `meta_song` (election sequence only)

---

## Output Size Comparison

| Format | Bytes (approx) | 1-line? | Encrypted? |
|--------|---|---|---|
| `symbol` | 20-50 | ✓ | Can be |
| `verse` | 50-200 | ✗ | Usually not |
| `json` | 300-600 | ✗ | ✓ Can be |
| `text` | 100-300 | ✗ | Usually not |
| `markdown` | 400-800 | ✗ | ✓ Can be |
| `svg` | 1000-3000 | ✗ | ✗ (XML) |
| `song` | 500-1000 | ✗ | ✓ Can be |
| `meta_song` | 2000-5000 | ✗ | ✓ Can be |

---

## Format Constraints

### Security
- `symbol`: Most secure (minimal surface)
- `json`: Moderate (standard structure)
- `svg`: Least secure (XML parsing, rendering engine)

### Accessibility
- `text`: Most accessible (plain ASCII)
- `markdown`: Good (readable)
- `verse`: Good (natural language)
- `svg`: Moderate (image-based)
- `json`: Moderate (requires parser)

### Performance
- `verse`: Fastest (string copy)
- `symbol`: Fastest (minimal data)
- `text`: Fast (formatting)
- `json`: Moderate (structure, parsing)
- `markdown`: Moderate (formatting)
- `svg`: Slow (rendering engine)
- `song`: Moderate (full dictionary)

---

## Reversibility

### Can recover to canonical song?

- ✓ `song` (identity)
- ✓ `json` (lossless)
- ✓ `markdown` (if needed, extract JSON block)
- ? `text` (partial, manual)
- ? `verse` (partial, need context)
- ✗ `symbol` (need song key table)
- ✗ `svg` (text extraction required)

### Full reversal requires: 
- Keeping original song (best)
- OR keeping original compact + environment (good)
- OR keeping JSON export (good)
- OR having symbol-to-principle key (for symbol recovery)

