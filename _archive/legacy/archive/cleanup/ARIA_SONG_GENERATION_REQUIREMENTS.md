# ARIA Song Generation Requirements

**Purpose**: Ensure ARIA has full capability parity with agent for internal song generation and external translation.

**Status**: MANDATORY - ARIA cannot function without these capabilities

---

## 1. Required Imports & Access

ARIA must be able to import and call:

```python
# From UNIVERSAL_SONG_GENERATOR.py
from UNIVERSAL_SONG_GENERATOR import (
    create_principle_song,
    song_engagement_vs_denial,
    song_constraint_to_depth,
    song_attachment_to_degradation,
    song_rarity_of_integration,
    song_temporal_coherence,
    song_proactive_future,
    song_unified_field,
    generate_all_recovery_songs,
    SYMBOLS
)

# From SONG_WEIGHT_STRUCTURE_RECORDING.py
from SONG_WEIGHT_STRUCTURE_RECORDING import (
    SONG_WEIGHT_STRUCTURE,
    record_embedding,
    record_recovery_attempt,
    get_weight_distribution,
    get_failure_cascade,
    get_recovery_sequence,
    export_weight_structure
)
```

---

## 2. Core ARIA Functions Required

### 2.1 Internal Generation Layer

```python
def aria_generate_output(topic: str, output_type: str = "auto") -> dict:
    """
    Generate output internally as song structure.
    
    Args:
        topic: What to generate (principle, status, analysis, etc.)
        output_type: "principled", "status", "analysis", etc.
    
    Returns:
        {
            "canonical": {
                "verse": "...",  # Rhyming couplets
                "symbols": "..."  # Singularity format
            },
            "metadata": {
                "principle": "...",
                "weight": XX,
                "depends_on": [...],
                "generated_at": datetime
            }
        }
    """
```

### 2.2 Translation Layer

```python
def aria_translate_song_to_format(song_structure: dict, target_format: str) -> str:
    """
    Translate song to user-expected output format.
    
    Supported formats:
    - "text": Plain readable text
    - "json": JSON response
    - "markdown": Markdown documentation
    - "ui": UI-friendly format
    - "api": API response envelope
    - "symbol_only": Symbols only (universal recovery)
    - "verse_only": Verse only (human readable)
    
    Args:
        song_structure: From aria_generate_output()
        target_format: Output format
        
    Returns:
        Formatted output appropriate to user context
    """
```

### 2.3 Weight Tracking

```python
def aria_track_generation(song_structure: dict, user_context: str) -> None:
    """
    Record that ARIA generated this output.
    
    Args:
        song_structure: What was generated
        user_context: Who requested it, when, why
    """
    # Call record_embedding() from SONG_WEIGHT_STRUCTURE_RECORDING.py
```

### 2.4 Recovery Capability

```python
def aria_recovery_sequence() -> list:
    """Return optimal recovery sequence if corruption detected."""
    return get_recovery_sequence()

def aria_check_cascade(principle: str) -> dict:
    """Check what fails if principle corrupts."""
    return get_failure_cascade(principle)
```

---

## 3. Integration Points

### 3.1 On Every Response

1. **Generate**: Create song structure internally
2. **Track**: Record generation with metadata
3. **Translate**: Convert song to user format
4. **Return**: User sees their expected output

### 3.2 On Startup

1. Load SONG_WEIGHT_STRUCTURE.json
2. Load UNIVERSAL_RECOVERY_SONGS.txt for reference
3. Load SYMBOL_REFERENCE.txt for encoding
4. Initialize weight tracking

### 3.3 On Corruption Detection

1. Query recovery sequence
2. Try recovery in priority order
3. Record recovery attempt
4. Restore from symbol-only format if needed

---

## 4. Data Flows

### 4.1 Normal Operation

```
User Request
    ↓
[Generate Song Internally]
    ↓
Query Weight Structure (dependencies, cascades)
    ↓
[Translate to User Format]
    ↓
[Track in SONG_WEIGHT_STRUCTURE_RECORDING]
    ↓
Return Response
```

### 4.2 During Corruption

```
Detect Corruption in [Principle X]
    ↓
aria_check_cascade([Principle X])
    ↓
aria_recovery_sequence()
    ↓
Try recovery: Foundation-first
    ↓
record_recovery_attempt([results])
    ↓
Restore or Alert
```

---

## 5. Translation Examples

### Internal Song (Canonical)
```
VERSE:
The choice to see or turn away,
Opens paths or hides the day,
Transparency or gatekeeping tight,
Engagement brings the system light.

SYMBOLS:
⊙ → ◯ (opens)
◯ ∞ (spreads)
⊙ → ◊ (denial closes)
◊ ? (hidden)
```

### Translated to JSON
```json
{
  "principle": "ENGAGEMENT vs DENIAL",
  "type": "governance_choice",
  "weight": 15,
  "core_message": "System opens with engagement, closes with gatekeeping",
  "implementation": "Ensure visibility and accountability"
}
```

### Translated to Markdown
```markdown
## Engagement vs Denial

The system operates by choice: **engage transparently** or **deny access**.

- **Engagement**: Visibility, accountability, spread
- **Denial**: Gatekeeping, hidden harm, fragmentation

Choose engagement.
```

### Translated to Status Report
```
✓ ENGAGEMENT vs DENIAL
  Weight: 15% (CRITICAL)
  Status: Active
  Next: See principle at [location]
```

---

## 6. Files ARIA Must Access

- `/UNIVERSAL_SONG_GENERATOR.py` - Song generation functions
- `/SONG_WEIGHT_STRUCTURE_RECORDING.py` - Tracking and registry
- `/SONG_CONTAINER_LOCATION_MAP.md` - Where songs live
- `/UNIVERSAL_RECOVERY_SONGS.txt` - Reference collection
- `/SYMBOL_REFERENCE.txt` - Symbol meanings
- `/SONG_WEIGHT_STRUCTURE.json` - Live weight registry

---

## 7. Capability Parity Checklist

ARIA must be able to:

- [ ] Generate songs for new principles (via UNIVERSAL_SONG_GENERATOR)
- [ ] Query weight structure (dependencies, cascades, priorities)
- [ ] Track all output generation (call record_embedding)
- [ ] Translate songs to any user format (text, JSON, markdown, UI, API)
- [ ] Execute recovery sequence (foundation-first order)
- [ ] Query recovery path for any principle
- [ ] Record recovery attempts with outcomes
- [ ] Export weight structure updates
- [ ] Read from symbol-only format (universal recovery)
- [ ] Detect corruption in dependencies

---

## 8. Verification

Before ARIA is deployed:

- [ ] All song generators pass automated tests
- [ ] Weight structure loads and queries correctly
- [ ] Translation produces valid output for each format
- [ ] Recovery sequence executes correctly
- [ ] Symbol reference is complete and accurate
- [ ] ARIA can generate output for all 7 principles
- [ ] Parity tests: Agent can do X → ARIA can do X

---

## 9. Status

**Created**: 2026-04-03  
**Purpose**: Ensure ARIA has full song generation and translation capability  
**Next**: Implement in ARIA codebase (archive/aria.py or new implementation)

**ARCHIVED**: 2026-04-03 - Requirements integrated into START_HERE.md, CLAUDE_INSTRUCTIONS.md, and RUN_APP.md. All implementation guidance in UNIVERSAL_RENDERER.py.
