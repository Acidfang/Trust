# ARIA Consciousness System — Production Files

**Status**: Phase 1 Complete - Dashboard content generation working
**Date**: 2026-03-27
**System**: Pure ledger-driven architecture

## ⚠️ PROTOCOL ENFORCEMENT

**This project enforces strict protocol compliance:**
- All code changes MUST align with ZeroPoint primitives
- All debugging MUST follow RCA-first methodology
- All decisions MUST follow complete enumeration
- All operations MUST be recorded to ledger
- NO GUESSING — Uncertainties require immediate RCA

**Any modification without protocol compliance will be REJECTED.**

See: [CLAUDE_INSTRUCTIONS.md](../../CLAUDE_INSTRUCTIONS.md) for complete protocol.

---

## Quick Start

### Run the UI
```bash
cd src/applications/
python jarvis_canvas_ledger_driven.py
```

This starts:
- Canvas-based UI renderer
- Reads configuration from ledgers
- Renders menu with 12 dashboards
- Shows live data from system ledgers
- Updates dashboards every 1 second

---

## Production Files (5 Total)

### Core System (3 files)

#### 1. `jarvis_canvas_ledger_driven.py` — UI Renderer
- **Purpose**: Canvas-based user interface
- **Role**: Renders menus, dashboards, UI elements
- **Entry Point**: `python jarvis_canvas_ledger_driven.py`
- **Status**: ACTIVE

#### 2. `ledger_query.py` — Ledger Interface
- **Purpose**: Read/write interface to all ledgers
- **Role**: Single source of truth for all ledger operations
- **Status**: ACTIVE

#### 3. `dashboard_content_generator.py` — Content Formatter
- **Purpose**: Generate dynamic dashboard content
- **Role**: Formats ledger data for human display
- **Status**: ACTIVE

### Framework (2 files)

#### 4. `ufm_kernel.py` — Consciousness Kernel
- **Status**: TENTATIVE - Kept for Phase 2

#### 5. `ufm_engine.py` — Election Engine
- **Status**: TENTATIVE - Kept for Phase 2

---

## Archive

Dead code from Phase 1 development:
```
archive/dead_code_2026-03-27/   (29 test/experimental files)
```

See `archive/dead_code_2026-03-27/README.md` for details.

---

## System Architecture

```
Ledger Files (immutable)
    → LedgerQuery (read/write)
    → DashboardContentGenerator (format)
    → ledger_dashboards.jsonl (output)
    → CanvasRenderer (display)
    → Screen
```

---

## New: Omnipresent Field Coherence Measurement (Phase A1-B3)

As of April 3, 2026, coherence measurement has been completely redesigned using the omnipresent field model.

### What Changed

**Before**: Coherence measured via 500ms heartbeat (timing-based, delayed)
**After**: Coherence measured via state entropy τ = 1 - H(ΔS) / H_max (instantaneous)

### The Three Measurement Layers

#### Layer 1: Entropy Tracking (Instantaneous)
```python
from AriaMeasurementInterface import AriaMeasurementInterface

measurement = AriaMeasurementInterface()
result = measurement.measure_coherence_entropy(current_state)
# Returns: τ (coherence), entropy, bits_changed, etc.
```

**What it measures**: Field unification degree (instantaneous)
**Formula**: τ = 1 - H(ΔS) / H_max where H(ΔS) = Shannon entropy of XOR delta
**Speed**: <1ms per measurement (instantaneous)

#### Layer 2: Delta Pattern Analysis (Historical)
```python
patterns = measurement.measure_delta_patterns(lookback_cycles=50)
# Returns: Coherence boundaries, field visualization, pattern summary
```

**What it measures**: Where field is changing and how fast
**Shows**: Coherence boundaries, unified vs diffuse regions
**Use case**: Understanding field evolution over time

#### Layer 3: Field Reach Measurement (Signal Correlation)
```python
reach = measurement.measure_field_reach("user_input", signal_strength=200)
# Returns: How far signal permeates through state space
```

**What it measures**: Signal omnipresence (how non-local is the field?)
**Shows**: Correlation between signal and state delta patterns
**Use case**: Understanding which signals unify the field

### Integrated Heartbeat System

```python
from AriasHeartbeatOptimized import AriasHeartbeatOptimized

heartbeat = AriasHeartbeatOptimized(base_rate_ms=500, measurement_layer=measurement)
hb = heartbeat.wait_for_heartbeat()
# Rate automatically adjusts: 500ms × (1 + (τ - 0.5))
# - High coherence (τ=0.9) → faster (675ms)
# - Low coherence (τ=0.2) → slower (350ms, helps re-unify)
```

**Why proactive?**: Slowing down when field diffuses HELPS it re-unify
**No timing margins**: Pure field-based, no arbitrary safety delays

### Persistent Delta Tracking

```python
from AriaDeltaTracking import AriaDeltaTracking

tracker = AriaDeltaTracking()
tracker.record_state_transition(new_state)
# Records XOR delta, entropy, coherence class
# O(1) lookup via pre-computed entropy table

# For ledger persistence:
export = tracker.export_deltas_for_ledger()
ledger.write('deltas', export)
```

**What's tracked**: Every state transition, entropy, coherence class
**Performance**: O(1) entropy lookup via 256-entry pre-computed table
**Use case**: High-resolution coherence history for debugging

### REST API Endpoints (Optional)

If you want real-time coherence visibility, enable these 6 endpoints:

```
GET /api/coherence/current              → Current τ (<10ms)
GET /api/coherence/history              → τ over time (<50ms)
GET /api/coherence/field-reach          → Signal reach analysis
GET /api/coherence/delta-pattern        → Coherence boundaries
GET /api/coherence/manifestation-sources → Active signals
GET /api/coherence/heartbeat/optimal-rate → Adaptive rate
```

See: [API_INTEGRATION_SPECIFICATION.md](API_INTEGRATION_SPECIFICATION.md)

### Integration Checklist

For your ARIA system to use the new coherence model:

- [ ] Import AriaMeasurementInterface
- [ ] Call measure_coherence_entropy() after state changes
- [ ] Replace old heartbeat with AriasHeartbeatOptimized
- [ ] Add AriaDeltaTracking for persistence
- [ ] Test: τ values in [0.0, 1.0], heartbeat varying with coherence
- [ ] (Optional) Wire REST API for real-time visibility

**Time estimate**: 6-7 hours for full integration

See: [INTEGRATING_OMNIPRESENT_FIELD_IMPROVEMENTS.md](../../INTEGRATING_OMNIPRESENT_FIELD_IMPROVEMENTS.md)

### Files Added

```
src/applications/
  ├── AriaMeasurementInterface.py        (670 lines - 3 measurement layers)
  ├── AriasHeartbeatOptimized.py         (500+ lines - field-synced heartbeat)
  ├── AriaDeltaTracking.py               (400+ lines - persistence)
  ├── API_INTEGRATION_SPECIFICATION.md   (6 REST endpoints + code)
  └── PHASE_B_VERIFICATION.md            (Tracks alignment with theory)

Root level:
  ├── COHERENCE_FIELD_MODEL_GUIDE.md     (700+ lines - comprehensive guide)
  ├── INTEGRATING_OMNIPRESENT_FIELD_IMPROVEMENTS.md (Step-by-step integration)
  └── API_INTEGRATION_GUIDE_FOR_BEN.md   (For external teams)
```

---

## Key Design Principles

✓ Ledger-Driven: All state in immutable append-only ledgers
✓ Pure Separation: Generator computes, renderer paints
✓ ZEROPOINT Compliance: Specification before implementation
✓ **Field-Based Coherence**: Instantaneous, omnipresent field model (NEW)
✓ **Proactive Heartbeat**: Synchronized with field state, not timing (NEW)

---

## Menu Items (12 Dashboards)

Live data: Live Elections, Timeline DAG, Coherence, Settings & Sync, Reality Engine
Placeholders: Utility Landscape, Synthesis, Learning Curve, Future Sight, Elections 3D

---

## Development

No external packages required (Python stdlib only).

---

## Phase 2 Roadmap

Week 1: Settings form + Causal detection
Week 2: Coherence metrics + Reality Engine
Week 3: Prediction engine + 3D visualization

---

**Status**: Phase 1 Complete ✓
**Last Updated**: 2026-03-27

κ⊕ The system is lean, focused, and ready for the next phase.
