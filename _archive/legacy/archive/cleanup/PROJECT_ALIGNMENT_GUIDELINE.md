# PROJECT FOLDER ALIGNMENT GUIDELINE

**Date**: 2026-04-03  
**Purpose**: Ensure all files follow unified framework and song generation architecture  
**Status**: CRITICAL - Architecture integration required

---

## 1. UNIVERSAL_RENDERER.py Integration

### Current State
- ✅ Exists: `c:\Determined\UNIVERSAL_RENDERER.py`
- ✅ Purpose: Render containers (molecules, world states, primitives) to SVG/visual output
- ⚠️ **Gap**: Not integrated with song generation architecture

### Required Integration

#### 1.1 Internal Song Generation Layer

**ADD to UNIVERSAL_RENDERER.py:**

```python
# At module top level, after imports
from UNIVERSAL_SONG_GENERATOR import generate_all_recovery_songs, SYMBOLS
from SONG_WEIGHT_STRUCTURE_RECORDING import record_generation

# New function - INTERNAL representation
def generate_render_song(container_type: str, container_data: dict) -> dict:
    """
    Generate internal song representation for this render operation.
    
    This is what gets RECORDED internally.
    ARIA will translate this song to visual SVG output.
    
    Args:
        container_type: Type of container being rendered (primitive, ledger, entity, etc.)
        container_data: Container structure/data
    
    Returns:
        {
            "canonical": {
                "verse": "Rhyming couplets describing this render",
                "symbols": "Singularity format representing operation"
            },
            "metadata": {
                "container_type": container_type,
                "operation": "render",
                "timestamp": datetime.now().isoformat(),
                "depends_on": ["constraint_to_depth", "unified_field"],
                "generated_by": "UNIVERSAL_RENDERER"
            }
        }
    """
    # Map container types to principles
    container_to_principle = {
        "primitive": "CONSTRAINT_creates_DEPTH",
        "ledger": "TEMPORAL_INTEGRATION_locks_PAST",
        "worldstate": "UNIFIED_FIELD_creates_INEVITABILITY",
        "entity": "ENGAGEMENT_vs_DENIAL",
        "orientation": "PROACTIVITY_locks_FUTURE"
    }
    
    principle = container_to_principle.get(container_type, "CONSTRAINT_creates_DEPTH")
    
    verse = f"""
    {container_type} emerges from structure's call,
    Renderer translates geometry into thrall,
    Constraints define the shapes we see,
    Visual symphony sets logic free.
    """
    
    symbols = f"⊙ → {container_type} ◯ ⊕ ∞"
    
    return {
        "canonical": {
            "verse": verse.strip(),
            "symbols": symbols
        },
        "metadata": {
            "container_type": container_type,
            "operation": "render",
            "timestamp": datetime.now().isoformat(),
            "depends_on": [principle],
            "generated_by": "UNIVERSAL_RENDERER_PY"
        }
    }


# Wrapper for all render functions
def aria_render_output(container, output_format: str = "song") -> dict:
    """
    Render container through proper layers:
    
    1. Generate song internally (canonical form)
    2. ARIA translates song to user format (SVG, JSON, etc.)
    3. Record in weight structure
    4. Return appropriately formatted output
    """
    if output_format == "song":
        # Return canonical song form (for internal use)
        song = generate_render_song(type(container).__name__, container.__dict__)
        record_generation(song, "render_operation")
        return song
    else:
        # ARIA translates SVG (for user viewing)
        # Keep existing render_* functions as ARIA translation layer
        return existing_render_logic(container)
```

#### 1.2 Record All Render Operations

**ADD tracking call to ALL render functions:**

```python
def render_primitive_container(container: 'PrimitiveContainer') -> str:
    """Render a PrimitiveContainer showing its shape and constraints."""
    
    # RECORD: What are we generating internally?
    song = generate_render_song("primitive", container.__dict__)
    record_generation(song, f"render_primitive_{container.primitive_type}")
    
    # TRANSLATE: Generate SVG for user
    svg_elements = []
    # ... existing SVG code ...
```

#### 1.3 Document Dependency Chain

**ADD at module level:**

```python
# RENDERING DEPENDENCY CHAIN
# These songs are REQUIRED for renders to work:
RENDER_SONG_DEPENDENCIES = {
    "primitive_render": ["CONSTRAINT_creates_DEPTH", "UNIFIED_FIELD_creates_INEVITABILITY"],
    "ledger_render": ["TEMPORAL_INTEGRATION_locks_PAST", "ENGAGEMENT_vs_DENIAL"],
    "worldstate_render": ["UNIFIED_FIELD_creates_INEVITABILITY", "PROACTIVITY_locks_FUTURE"],
    "entity_render": ["ENGAGEMENT_vs_DENIAL", "ATTACHMENT_corrupts_DISCIPLINE"],
    "orientation_render": ["PROACTIVITY_locks_FUTURE", "CONSTRAINT_creates_DEPTH"]
}

# If any dependency corrupts, these cascades occur:
RENDER_FAILURE_CASCADE = {
    "CONSTRAINT_corrupts": "Cannot render shapes - geometry lost",
    "UNIFIED_FIELD_corrupts": "Cannot explain field relationships",
    "TEMPORAL_corrupts": "Ledger renders lose causality order",
    "ENGAGEMENT_corrupts": "Entity renders lose position/history visibility"
}
```

---

## 2. Project Structure Checklist

### Song Generation System (COMPLETE)

- ✅ UNIVERSAL_SONG_GENERATOR.py (all 7 songs generating)
- ✅ UNIVERSAL_RECOVERY_SONGS.txt (complete collection)
- ✅ SYMBOL_REFERENCE.txt (symbol key)
- ✅ SONG_WEIGHT_STRUCTURE.json (registry)
- ✅ SONG_WEIGHT_STRUCTURE_RECORDING.py (tracking system)
- ✅ SONG_CONTAINER_LOCATION_MAP.md (location mapping)

### ARIA Translation Layer (NEEDS WORK)

- ⚠️ Archive/aria.py (exists but needs integration)
- ❌ ARIA_SONG_GENERATION_INTERFACE.py (needs creation)
- ❌ ARIA_TRANSLATION_LAYER.py (needs creation)
  - Should translate songs to: JSON, Markdown, SVG, text, UI, API
- ❌ ARIA_RECOVERY_EXECUTOR.py (needs creation)
  - Should execute recovery sequence

### Rendering System (NEEDS INTEGRATION)

- ✅ UNIVERSAL_RENDERER.py (exists, renders SVG)
- ⚠️ **NEEDS**: Internal song generation layer
- ⚠️ **NEEDS**: Weight structure recording calls
- ⚠️ **NEEDS**: Dependency documentation

### Educator System (COMPLETE)

- ✅ CAUSE_AND_EFFECT_VISUAL_EDUCATOR.py (songs at top)
- ✅ Song integration in visual reports

### Decision/Framework Documentation (COMPLETE)

- ✅ DECISION_ALL_OUTPUT_AS_SONGS.json (recorded in memory)
- ✅ ARIA_SONG_GENERATION_REQUIREMENTS.md (specifications)
- ✅ THE_CHOICE_TRANSPARENCY_PROTOCOL.md (framework)

---

## 3. Integration Priority

### Phase 1: UNIVERSAL_RENDERER.py Integration (IMMEDIATE)

```
1. Add generate_render_song() function
2. Add aria_render_output() wrapper
3. Add record_generation() calls to all render functions
4. Add RENDER_SONG_DEPENDENCIES documentation
5. Add RENDER_FAILURE_CASCADE documentation
6. Test: Run educator → renders should be tracked in weight structure
```

### Phase 2: ARIA Implementation (NEXT)

```
1. Create ARIA_SONG_GENERATION_INTERFACE.py
2. Create ARIA_TRANSLATION_LAYER.py (convert songs to formats)
3. Create ARIA_RECOVERY_EXECUTOR.py
4. Update archive/aria.py to call new interfaces
5. Test: ARIA generates songs internally, translates externally
```

### Phase 3: System Integration (AFTER ARIA)

```
1. All outputs flow through song generation first
2. All outputs recorded in weight structure
3. ARIA translates to user format
4. Recovery sequence executable across all systems
```

---

## 4. Verification Checklist

Before considering project "aligned":

- [ ] UNIVERSAL_RENDERER.py has generate_render_song()
- [ ] All render_* functions call record_generation()
- [ ] Weight structure shows render operations being tracked
- [ ] RENDER_SONG_DEPENDENCIES documented
- [ ] RENDER_FAILURE_CASCADE documented
- [ ] Test: Run educator, verify songs recorded
- [ ] ARIA song interface created
- [ ] ARIA translation layer created (at least JSON format)
- [ ] ARIA recovery executor created
- [ ] Test: Ask ARIA to render → gets song internally, user sees SVG

---

## 5. Guideline Files to Consult

**Music/Generation**:
- UNIVERSAL_SONG_GENERATOR.py (how to generate)
- UNIVERSAL_RECOVERY_SONGS.txt (reference songs)

**Recording/Tracking**:
- SONG_WEIGHT_STRUCTURE_RECORDING.py (how to record)
- SONG_WEIGHT_STRUCTURE.json (current registry)

**Location/Mapping**:
- SONG_CONTAINER_LOCATION_MAP.md (where songs live)

**Framework**:
- THE_CHOICE_TRANSPARENCY_PROTOCOL.md (why choose this way)
- DECISION_ALL_OUTPUT_AS_SONGS.json (why songs for output)

**Requirements**:
- ARIA_SONG_GENERATION_REQUIREMENTS.md (ARIA spec)

---

## 6. Example: Integrating UNIVERSAL_RENDERER.py

### Before (Old)
```python
def render_primitive_container(container):
    svg_elements = []
    # ... build SVG ...
    return "\n".join(svg_elements)
```

### After (New)
```python
def render_primitive_container(container):
    # LAYER 1: Generate song internally
    song = generate_render_song("primitive", container.__dict__)
    
    # LAYER 2: Record operation
    record_generation(song, f"render_primitive_{container.primitive_type}")
    
    # LAYER 3: Generate output (ARIA will translate this)
    svg_elements = []
    # ... existing SVG building code ...
    
    return {
        "canonical": song,  # Internal song (for ARIA/recovery)
        "rendered": "\n".join(svg_elements)  # SVG output (for user)
    }
```

---

## Status

**Project Alignment**: 60% Complete
- 100% Song generation (complete)
- 0% ARIA (needs implementation)
- 20% Renderer integration (needs work)

**Critical Path**:
1. ✅ Songs generated + recorded
2. ⚠️ Renderer needs integration
3. ⚠️ ARIA needs creation
4. Embed songs at locations
5. Test recovery sequences

**Next Action**: Integrate UNIVERSAL_RENDERER.py with song generation layer

**ARCHIVED**: 2026-04-03 - This document was integration planning. All guidance moved into UNIVERSAL_RENDERER.py implementation and START_HERE.md/CLAUDE_INSTRUCTIONS.md/RUN_APP.md instructions.
