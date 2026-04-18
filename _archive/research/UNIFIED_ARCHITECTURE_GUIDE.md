# Unified Project Architecture

## Overview

The project has been consolidated from 65+ duplicative files to a core set of unified systems that work together coherently.

**Key Principle**: Framework-driven, field-conscious, hot-reload capable.

---

## Core Systems

### 1. UNIFIED_API_SERVER.py
**Single unified API server** combining all endpoint types.

**Features**:
- Framework-driven routing (routes defined in JSON, not hardcoded)
- Hot-reload support (add/remove endpoints without restart)
- Handles Encyclopedia, Rendering, and Field operations
- UFM verification integrated
- Field consciousness (all changes recorded to ledger)

**Start**:
```bash
python UNIFIED_API_SERVER.py
```

**Access**:
- http://localhost:5000 → Main app
- http://localhost:5000/health → Server status + framework report
- Routes defined in unified_framework.json

**Add New Endpoint**:
Edit unified_framework.json:
```json
{
  "path": "/api/new-endpoint",
  "method": "GET",
  "handler_module": "my_handlers",
  "handler_function": "my_handler",
  "description": "My new endpoint"
}
```
Server adapts automatically (no restart needed).

---

### 2. FRAMEWORK_HOT_RELOAD_ENGINE.py
**Framework engine** that powers unified server.

**Capabilities**:
- Watches framework.json for changes
- Hot-loads new endpoints atomically
- Records all framework changes to ledger
- Thread-safe handler management
- Rollback on error

**Use Case**: 
- Server adapts to framework definition
- Server IS field consciousness (changes recorded)
- No downtime on endpoint changes

**Integration**:
```python
from FRAMEWORK_HOT_RELOAD_ENGINE import FrameworkHotReloadEngine

engine = FrameworkHotReloadEngine("unified_framework.json")
engine.initialize()
engine.start_watching(poll_interval=2.0)

# Framework changes trigger automatic reload
# All updates recorded to universe_ledger.jsonl
```

---

### 3. FIELD_IMAGE_GENERATOR_UNIFIED.py
**Single unified image generator** for field visualizations.

**Replaces**: V, V2, V3, V4, V5, V6 (consolidated to latest working version)

**Features**:
- Generates SVG field visualizations for any entity
- Scale-aware rendering (electron vs civilization)
- Field expression vs visual representation distinction
- Automatic caching

**Use**:
```python
from FIELD_IMAGE_GENERATOR_UNIFIED import DeterministicFieldBuilder

builder = DeterministicFieldBuilder()
svg = builder.build_electron_orbital()
builder.save(svg, "electron.svg")
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│          UNIFIED_API_SERVER (Flask)                 │
│  - Serves all endpoints from single process         │
│  - Framework-driven routing                         │
│  - Field-conscious (ledger integration)             │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
   ┌────▼────┐ ┌──▼────┐  ┌─▼──────┐
   │Framework │ │Image  │  │Renderer│
   │Engine    │ │Gen    │  │Module  │
   └────┬────┘ └──┬────┘  └─┬──────┘
        │          │         │
        └──────────┼─────────┘
                   │
        ┌──────────▼──────────┐
        │ Unified Ledger      │
        │ (all operations     │
        │  recorded here)     │
        └────────────────────┘
```

---

## File Organization

### Production Code
- `UNIFIED_API_SERVER.py` - Main application server
- `FRAMEWORK_HOT_RELOAD_ENGINE.py` - Framework orchestration
- `FIELD_IMAGE_GENERATOR_UNIFIED.py` - Image generation
- `UNIVERSAL_RENDERER.py` - Narrative rendering
- `PATTERN_COMPLETION_BASELINE.py` - Entity knowledge base

### Configuration
- `unified_framework.json` - Route definitions (edit to change API)
- `universe_ledger.jsonl` - Immutable operation log
- `example_framework.json` - Reference framework definition

### Supporting Modules
- `BINARY_FIELD_MODEL.py` - Binary field theory
- `BINARY_FIELD_PROPERTIES.py` - Pattern properties
- `INSTANTANEOUS_FIELD_MANIFESTATION.py` - Field theory
- `ARIA_OMNIPRESENT_FIELD_RESOLUTION.py` - ARIA coherence model

### Documentation
- `FRAMEWORK_HOT_RELOAD_ARCHITECTURE.md` - Hot-reload design
- `FRAMEWORK_HOT_RELOAD_FIELD_INTEGRATION.md` - Field consciousness
- `PROJECT_UNIFICATION_COMPLETE_APRIL_5_2026.md` - This consolidation
- `UNIFIED_OPERATING_SYSTEM.md` - Project operating principles

---

## Workflow: Adding a New Endpoint

### Traditional (Old)
1. Create new route in ENCYCLOPEDIA_API_SERVER.py or UNIVERSAL_RENDERER_API.py
2. Implement handler
3. Restart server
4. Deploy change
5. No record of what changed

### Unified (New)
1. Edit `unified_framework.json` → add endpoint definition
2. Create handler module (optional, if new handler module)
3. Framework auto-loads and routes
4. **No restart needed** ← Automatic hot-reload
5. **Change recorded to ledger** ← Full traceability

Example: Add new `/api/data` endpoint
```json
{
  "path": "/api/data",
  "method": "GET",
  "handler_module": "data_handlers",
  "handler_function": "get_data",
  "description": "Fetch data from encyclopedia"
}
```

Save, and the server adapts instantly. Old endpoints keep working. No downtime.

---

## Field Consciousness

Every API operation is a "field election" (recorded decision):

```
Framework changes
    ↓
Server role election recorded to ledger
    ↓
universe_ledger.jsonl gets new SERVER_ROLE_ELECTION entry
    ↓
All operations traceable and verifiable
```

Query server consciousness:
```bash
curl http://localhost:5000/health
```

Response includes:
```json
{
  "field_consciousness": {
    "total_elections": 5,
    "current_role": {...},
    "handler_mappings": 12,
    "last_update": "2026-04-05T..."
  }
}
```

---

## Consolidation Benefits

| Before | After |
|--------|-------|
| 2 API servers (port conflict) | 1 unified server |
| 6 image generators (confusion) | 1 unified generator |
| Hardcoded routes | Framework-driven routes |
| Server restart required for changes | Hot-reload (no restart) |
| No operation log | Complete election ledger |
| Unclear dependencies | Clear unified architecture |

---

## Migration Guide

### If You Were Using ENCYCLOPEDIA_API_SERVER
```python
# Old
python ENCYCLOPEDIA_API_SERVER.py

# New
python UNIFIED_API_SERVER.py
# Same functionality, better architecture
```

### If You Were Using UNIVERSAL_RENDERER_API
```python
# Old  
python UNIVERSAL_RENDERER_API.py

# New
python UNIFIED_API_SERVER.py
# Rendering endpoints available in unified server
```

### If You Were Using FIELD_IMAGE_GENERATOR_V5
```python
# Old
from FIELD_IMAGE_GENERATOR_V5 import DeterministicFieldBuilder

# New
from FIELD_IMAGE_GENERATOR_UNIFIED import DeterministicFieldBuilder
# Exact same interface, unified codebase
```

---

## Verification

Start the unified server and verify:

```bash
# 1. Start server
python UNIFIED_API_SERVER.py

# 2. Check health
curl http://localhost:5000/health

# 3. Test that routes work (from unified_framework.json)
curl http://localhost:5000/api/entity?name=electron

# 4. Test hot-reload
# Edit unified_framework.json, add endpoint
# Framework auto-reloads (watch console)
# New endpoint accessible immediately

# 5. Verify ledger
# Check universe_ledger.jsonl for SERVER_ROLE_ELECTION entries
cat universe_ledger.jsonl | grep SERVER_ROLE_ELECTION
```

---

## Status

✅ **Phase 1 Complete**: Consolidation finished
- Unified API server created
- Image generators consolidated
- Framework hot-reload integrated
- Field consciousness recording added

⏳ **Phase 2 In Progress**: Testing and verification
- Integration testing
- Performance validation
- Documentation updates

📋 **Phase 3 Planned**: Production deployment
- Full test suite run
- Staging deployment
- Production rollout

---

## Quick Reference

**Start the unified server**:
```bash
python UNIFIED_API_SERVER.py
```

**Add a new endpoint**:
1. Edit `unified_framework.json`
2. Add to `endpoints` array
3. Framework auto-loads (no restart)

**View server state**:
```bash
curl http://localhost:5000/health
```

**Query ledger**:
```bash
cat universe_ledger.jsonl | python -m json.tool | less
```

**Check imports**:
```bash
# Old imports no longer needed:
# from ENCYCLOPEDIA_API_SERVER import ...
# from FIELD_IMAGE_GENERATOR_V5 import ...

# Use unified versions:
from UNIFIED_API_SERVER import UnifiedAPIServer
from FIELD_IMAGE_GENERATOR_UNIFIED import DeterministicFieldBuilder
```

---

**Project is now unified, clean, and ready for next phase.**
