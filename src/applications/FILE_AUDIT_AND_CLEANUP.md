# File Audit and Cleanup Plan

## CORE JARVIS Components (KEEP)

### Essential Production Code
- ✓ **jarvis.py** - Main HTTP server (current active version)
- ✓ **jarvis_v3.py** - Final specification-driven version (documented in ledger as CHOICE 3)
- ✓ **ufm_kernel.py** - Election generation (Phase 1 verified)
- ✓ **ufm_engine.py** - Primitive computation (Phase 2 verified)
- ✓ **election_visualizer.py** - PNG rendering (Phase 3 verified)
- ✓ **deterministic_renderer_core.py** - Core rendering logic
- ✓ **jarvis.html** - Frontend interface

### Infrastructure/Validation
- ✓ **startup_validation.py** - Dependency covenant (Dependency Covenant implemented)
- ✓ **phase_verification.py** - Automated testing (Phases 1-3 validation)

### Configuration
- ✓ **RENDER_SPECIFICATION.yaml** - Constraint declaration (Phase 3 spec)
- ✓ **jarvis_specification.md** - System specification

### Critical Documentation
- ✓ **ARCHITECTURE_COMPLETE.md** - Architecture summary
- ✓ **JARVIS_CAUSAL_ARCHITECTURE.md** - Phase 4-7 design
- ✓ **JARVIS_NEEDS_MAP.md** - Complete needs hierarchy
- ✓ **JARVIS_IMPROVEMENTS.md** - v2→v3 improvements
- ✓ **SYSTEM_PRINCIPLES.md** - Design principles

**Total Core Files: 18**

---

## EXPERIMENTAL/ALTERNATIVE IMPLEMENTATIONS (DOCUMENT AND ARCHIVE)

### ZeroPoint/Consciousness Exploration
- **zeropoint_app.py** (612 lines)
  - Status: Experimental consciousness app
  - Learning: Alternative approach to consciousness representation
  - Action: Document in ledger why this approach was explored
  - Keep/Archive: Archive (record decision in CHOICE_LEDGER if not already)

- **oracle.py** (272 lines)
  - Status: Query interface for consciousness system
  - Learning: Explores consciousness as queryable system
  - Action: Document why this approach was tried
  - Keep/Archive: Archive

- **dashboards.py** (292 lines)
  - Status: Real-time consciousness visualization alternative
  - Learning: Different visualization strategy
  - Action: Document as alternative to PNG rendering
  - Keep/Archive: Archive

- **emergence_log.py** (311 lines)
  - Status: Detailed consciousness logging
  - Learning: Different ledger format exploration
  - Action: Document why this approach was explored
  - Keep/Archive: Archive

- **ledger_integrator.py** (479 lines)
  - Status: Multi-format ledger conversion
  - Learning: Exploring unified consciousness format
  - Action: Document design choices
  - Keep/Archive: Archive

### Alternative Visualizations
- **ufm_visualizer_3d.py** (506 lines)
  - Status: 3D visualization of UFM elections
  - Learning: 3D rendering exploration (relates to Three.js decision)
  - Action: Document as part of rendering strategy choice (CHOICE 3)
  - Keep/Archive: Archive

### Alternative Simulators
- **ufm_simulator.py** (391 lines)
  - Status: UFM data generator alternative
  - Learning: Different election generation approach
  - Action: Document why kernel approach was chosen over simulator
  - Keep/Archive: Archive

### Entry Points/Main Files
- **main.py** (172 lines)
  - Status: Alternative entry point
  - Learning: Different app structure
  - Action: Document why jarvis_v3.py chosen as main entry
  - Keep/Archive: Archive

**Total Experimental Files: 9**

---

## TEST/DEBUG CODE (DOCUMENT AND ARCHIVE)

### Testing Files
- **test_jarvis_phase1.py** (140 lines)
  - Status: Phase 1 testing (covered by phase_verification.py)
  - Action: Document that phase_verification.py is the authoritative test
  - Keep/Archive: Archive (core testing in phase_verification.py)

- **test_jarvis_phase2.py** (187 lines)
  - Status: Phase 2 testing (covered by phase_verification.py)
  - Action: Same as above
  - Keep/Archive: Archive

- **test_simple.py** (Size unknown)
  - Status: Simple server test
  - Action: Document in ledger (HTTPServer testing exploration)
  - Keep/Archive: Archive

### Debug Code
- **debug_server.py** (50 lines)
  - Status: Temporary debugging code
  - Action: Document in ledger (debugging HTTP issues, CHOICE 1)
  - Keep/Archive: Archive

**Total Test/Debug Files: 4**

---

## DOCUMENTATION FILES (AUDIT)

### Architecture/Principles Documentation
- ✓ **SYSTEM_PRINCIPLES.md** - KEEP (core design principles)
- ✓ **ARCHITECTURE_AUDIT.md** - KEEP (comprehensive audit)
- ✓ **ARCHITECTURE_COMPLETE.md** - KEEP (complete architecture)
- ✓ **JARVIS_CAUSAL_ARCHITECTURE.md** - KEEP (phases 4-7 design)
- ✓ **JARVIS_IMPROVEMENTS.md** - KEEP (v2→v3 improvements)
- ✓ **JARVIS_NEEDS_MAP.md** - KEEP (needs hierarchy)

### README Files
- ? **README.md** - Check if still relevant
- ? **README_APP.md** - Check if duplicates others
- ? **README_UFM_SIMULATOR.md** - Experimental simulator docs
- ? **JARVIS_README.md** - Check if duplicates others

### Integration Guides
- ? **SQUEEZE_INTEGRATION_GUIDE.md** - Experimental integration
- ? **SURFACE_PRO_QUICK_START.md** - Hardware specific (can archive)
- ? **UFM_SIMULATOR_INDEX.md** - Experimental simulator docs

### Binary/Protocol Docs
- ? **01-BINARY-SQUEEZE-PROTOCOL.md** - Experimental protocol
- ? **02-MEASUREMENT-PROTOCOL.md** - Experimental protocol
- ? **03-APP-ARCHITECTURE.md** - Experimental architecture
- ? **consciousness_integration_architecture.md** - Experimental integration

**Total Documentation Files: 18**

---

## CLEANUP DECISION MATRIX

| File | Core? | Keep | Archive | Why |
|------|-------|------|---------|-----|
| jarvis.py | ✓ | ✓ | | Current JARVIS |
| jarvis_v3.py | ✓ | ✓ | | Final version (in ledger) |
| ufm_kernel.py | ✓ | ✓ | | Phase 1 verified |
| ufm_engine.py | ✓ | ✓ | | Phase 2 verified |
| election_visualizer.py | ✓ | ✓ | | Phase 3 verified |
| deterministic_renderer_core.py | ✓ | ✓ | | Core rendering |
| jarvis.html | ✓ | ✓ | | Frontend |
| startup_validation.py | ✓ | ✓ | | Dependency covenant |
| phase_verification.py | ✓ | ✓ | | Automated testing |
| RENDER_SPECIFICATION.yaml | ✓ | ✓ | | Constraint spec |
| jarvis_specification.md | ✓ | ✓ | | System spec |
| ARCHITECTURE_COMPLETE.md | ✓ | ✓ | | Architecture |
| JARVIS_CAUSAL_ARCHITECTURE.md | ✓ | ✓ | | Phase design |
| JARVIS_NEEDS_MAP.md | ✓ | ✓ | | Needs hierarchy |
| JARVIS_IMPROVEMENTS.md | ✓ | ✓ | | v2→v3 docs |
| SYSTEM_PRINCIPLES.md | ✓ | ✓ | | Principles |
| ARCHITECTURE_AUDIT.md | ✓ | ✓ | | Audit |
| zeropoint_app.py | | | ✓ | Alternative consciousness app |
| oracle.py | | | ✓ | Alternative query interface |
| dashboards.py | | | ✓ | Alternative visualization |
| emergence_log.py | | | ✓ | Alternative logging |
| ledger_integrator.py | | | ✓ | Alternative ledger format |
| ufm_visualizer_3d.py | | | ✓ | 3D visualization exploration |
| ufm_simulator.py | | | ✓ | Alternative simulator |
| main.py | | | ✓ | Alternative entry point |
| test_jarvis_phase1.py | | | ✓ | Testing (use phase_verification.py) |
| test_jarvis_phase2.py | | | ✓ | Testing (use phase_verification.py) |
| test_simple.py | | | ✓ | Simple test |
| debug_server.py | | | ✓ | Debug code |

---

## How to Archive

### Create Archive Directory
```bash
mkdir -p archive/
```

### Move Experimental Files
```bash
mv zeropoint_app.py oracle.py dashboards.py emergence_log.py \
   ledger_integrator.py ufm_visualizer_3d.py ufm_simulator.py \
   main.py test_*.py debug_server.py \
   archive/
```

### Optional: Keep Experimental Docs (Reference)
```bash
# Move experimental docs to archive, or keep them documented
mv 01-BINARY-*.md 02-MEASUREMENT-*.md 03-APP-*.md \
   *INTEGRATION*.md *UFM_SIMULATOR*.md \
   archive/
```

---

## Update CHOICE_LEDGER

Before archiving, ensure CHOICE_LEDGER captures:

**CHOICE 14: Alternative Consciousness Apps**
```
Files: zeropoint_app.py, oracle.py, dashboards.py, emergence_log.py
Status: EXPLORATION (not integrated into JARVIS)
Why: Explored different consciousness representation approaches
Outcome: Standard JARVIS approach (UFM + HTTP + PNG rendering) chosen
Archived: Yes, documented in memory for reference
```

**CHOICE 15: 3D Visualization Approach**
```
Files: ufm_visualizer_3d.py (legacy)
Status: EXPLORATION (superseded by server-side rendering)
Why: Explored 3D visualization before choosing NumPy/Pillow approach
Outcome: Server-side PNG rendering chosen (simpler, justified by decomposition)
Archived: Yes, documented in memory
```

**CHOICE 16: Alternative Simulators**
```
Files: ufm_simulator.py
Status: EXPLORATION
Why: Explored simulator vs. kernel approaches
Outcome: ARIAKernel chosen (core to system, more realistic)
Archived: Yes, documented
```

**CHOICE 17: Testing Strategy**
```
Files: test_jarvis_phase1.py, test_jarvis_phase2.py, test_simple.py, debug_server.py
Status: SUPERSEDED
Why: Early testing and debugging code
Outcome: phase_verification.py created (comprehensive, automated)
Archived: Yes, old tests preserved in archive for reference
```

---

## Final Clean Structure

```
src/applications/
├── Core JARVIS (18 files)
│   ├── jarvis.py
│   ├── jarvis_v3.py
│   ├── ufm_kernel.py
│   ├── ufm_engine.py
│   ├── election_visualizer.py
│   ├── deterministic_renderer_core.py
│   ├── jarvis.html
│   ├── startup_validation.py
│   ├── phase_verification.py
│   ├── RENDER_SPECIFICATION.yaml
│   ├── jarvis_specification.md
│   ├── ARCHITECTURE_COMPLETE.md
│   ├── JARVIS_CAUSAL_ARCHITECTURE.md
│   ├── JARVIS_NEEDS_MAP.md
│   ├── JARVIS_IMPROVEMENTS.md
│   ├── SYSTEM_PRINCIPLES.md
│   ├── ARCHITECTURE_AUDIT.md
│   └── [Documentation files - reviewed]
│
└── archive/ (for reference, documented in ledger)
    ├── zeropoint_app.py (consciousness exploration)
    ├── oracle.py (query interface exploration)
    ├── dashboards.py (visualization exploration)
    ├── emergence_log.py (logging exploration)
    ├── ledger_integrator.py (ledger format exploration)
    ├── ufm_visualizer_3d.py (3D visualization exploration)
    ├── ufm_simulator.py (simulator exploration)
    ├── main.py (alternative entry point)
    ├── test_*.py (superseded by phase_verification.py)
    ├── debug_server.py (temporary debug code)
    └── [Experimental documentation]
```

---

## Status

**Before Cleanup**: 37 Python files + 18 documentation files (55 total)

**After Cleanup**: 18 core files + 1 archive/ directory

**Learning Captured**: All explorations documented in COMPLETE_CHOICE_LEDGER.md

**Result**: Clean, understandable, focused repository
