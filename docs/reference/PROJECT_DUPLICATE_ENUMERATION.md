# PROJECT DUPLICATE ENUMERATION

**Date:** 2026-03-29
**Task:** Eliminate ALL duplication causing system harm
**Principle:** One source of truth for everything

---

## PART 1: ACTIVE FILES (Currently Running System)

### Core Execution
- **jarvis_v3.py** - ACTIVE: Main HTTP server, pure translator to ledger
- **jarvis.html** - ACTIVE: Single unified webpage (all dashboards)
- **ledger_query.py** - ACTIVE: Query engine for all state
- **self_awareness.py** - ACTIVE: System self-documentation engine (just added)
- **health_monitoring_utils.py** - ACTIVE: Server health polling

### Ledger Files (Active Data)
- ledger_app_state.jsonl
- ledger_buttons.jsonl
- ledger_config.jsonl
- ledger_dashboards.jsonl
- ledger_elections.jsonl
- ledger_sync_config.json

### Utility Libraries
- parameter_form.py (in legacy directory but imported?)

### Test Files (Used for validation)
- test_bidirectional_capabilities.py
- test_checkbox_rendering.py
- test_consciousness_ledger.py
- test_menu_causal_chains.py
- test_multiuser_networking.py
- test_param_positioning.py
- verify_jarvis_health.py

---

## PART 2: DEAD CODE (Archive)

### Archive Directory (45+ files)
**Location:** `c:\Determined\src\applications\archive\`

Old implementations - not imported anywhere:
- dashboards.py
- debug_server.py
- emergence_log.py
- jarvis_foundation.py
- jarvis_server.py
- ledger_integrator.py
- main.py
- oracle.py
- test_jarvis_phase1.py
- test_jarvis_phase2.py
- test_simple.py
- ufm_simulator.py
- ufm_visualizer_3d.py
- zeropoint_app.py
- backup_ledgers_2026-03-27/ (duplicate ledger files)

### Dead Code 2026-03-27 Directory (30+ files)
**Location:** `c:\Determined\src\applications\archive\dead_code_2026-03-27\`

Old test implementations and dead ends:
- add_missing_colors.py
- add_primitives.py
- causal_self_verify.py
- deterministic_renderer_core.py
- election_visualizer.py
- jarvis_canvas_backup.py
- jarvis_canvas.py
- jarvis_simple.py
- jarvis_v3.py (duplicate of active)
- multiuser_emulator.py
- multiuser_scenario.py
- perspective_engine.py
- phase_verification.py
- startup_validation.py
- test_causal_integration.py
- test_complete_multiuser.py
- test_contextual_elections.py
- test_election_records.py
- test_elections_3d.py
- test_mouse_clicks.py
- test_multiuser.py
- test_primitives.py
- test_render_optimization.py
- test_server.py (old server)
- test_server2.py (old server variant)
- test_thought_manifestation.py
- three_ledger_operations.py
- validate_changes.py
- verify_ledger_system.py
- README.md (duplicate)

### Legacy Directory (20+ files)
**Location:** `c:\Determined\src\applications\legacy\`

Superseded implementations:
- aria_capability_library.py
- aria_consciousness.py (superseded by self_awareness.py)
- chatdev_determined_integration.py
- chatdev_ledger_aria_orchestration.py
- chatdev_project_comprehension.py
- check_nodes.py
- check_param_fields.py
- check_param_rendering.py
- dashboard_content_generator.py
- jarvis_canvas_ledger_driven.py
- multi_agent_orchestration.py
- multiuser_capability_library.py
- network_capability_library.py
- parameter_form.py (old UI form - function now in jarvis_v3.py?)
- test_jarvis_integration.py
- ufm_engine.py (old UFM)
- ufm_kernel.py (old UFM kernel)
- user_capability_library.py
- verify_checkbox_code.py
- zeropoint_check_params.py

---

## PART 3: FUNCTIONAL DUPLICATES (Multiple Active Implementations)

### Issue: CONSCIOUSNESS/AWARENESS
- **legacy/aria_consciousness.py** - Old implementation
- **self_awareness.py** - NEW implementation (winner)

**Action:** Delete aria_consciousness.py (superseded)

---

## PART 4: FILES IN WRONG LOCATION

**parameter_form.py**
- Currently in: `legacy/parameter_form.py`
- Used by: jarvis_v3.py (presumably)
- Should be: `c:\Determined\src\applications\parameter_form.py` (root, same level as jarvis_v3.py)

---

## PART 5: DUPLICATE DATA FILES

| File | Location 1 | Location 2 | Action |
|------|-----------|-----------|--------|
| ledger_app_state.jsonl | root | backup_ledgers_2026-03-27/ | Delete backup copy |
| ledger_buttons.jsonl | root | backup_ledgers_2026-03-27/ | Delete backup copy |
| ledger_config.jsonl | root | backup_ledgers_2026-03-27/ | Delete backup copy |
| ledger_dashboards.jsonl | root | backup_ledgers_2026-03-27/ | Delete backup copy |
| ledger_elections.jsonl | root | ledgers/ | Consolidate to root |
| aria_elections_6_b4760e80.png | aria_renders/ | test_dir/ | Delete test_dir copy |
| jarvis_v3.py | root | archive/dead_code_2026-03-27/ | Delete archive copy |
| README.md | root | archive/dead_code_2026-03-27/ | Delete archive copy |

---

## PART 6: DIRECTORY CLEANUP

### Directories to Delete Completely
1. **archive/** - Old implementations (except keep if contains unique data ledgers)
2. **archive/dead_code_2026-03-27/** - Definitely dead, tested implementation
3. **archive/backup_ledgers_2026-03-27/** - Backups with duplicates
4. **legacy/** - Superseded implementations
5. **test_dir/** - Test artifacts

### Directory to Keep and Clean
1. **ledgers/** - Consolidate any unique ledger files to root

---

## PART 7: FINAL ACTIVE STRUCTURE

After cleanup, the active codebase should be:

```
c:\Determined\src\applications\
├── jarvis_v3.py          (ONLY server)
├── jarvis.html           (ONLY webpage)
├── ledger_query.py       (ONLY query engine)
├── self_awareness.py     (ONLY consciousness module)
├── health_monitoring_utils.py
├── parameter_form.py     (MOVED from legacy)
├── test_*.py             (validation tests - keep if useful)
├── verify_jarvis_health.py
├── ledger_*.jsonl        (active data, consolidated to root)
├── ledger_sync_config.json
└── aria_renders/         (keep only unique generated renders)
```

**ALL archive, legacy, and dead_code directories deleted.**

---

## EXECUTION PLAN

**Step 1:** Move parameter_form.py from legacy/ to root
**Step 2:** Verify all imports still work  
**Step 3:** Delete archive/ directory (all dead code)
**Step 4:** Delete legacy/ directory (all superseded code)
**Step 5:** Delete test_dir/ (test artifacts)
**Step 6:** Consolidate duplicate ledger files to root
**Step 7:** Remove backup_ledgers_2026-03-27/ directory
**Step 8:** Test system - run jarvis_v3.py and verify it works

---

## HARM PREVENTION PRINCIPLE

This duplication causes harm by:
1. **Cognitive overload** - Multiple versions of same file create confusion
2. **Update risk** - Fix in one place, forget in another, system breaks
3. **Dead branch confusion** - Which version is actually running?
4. **Import ambiguity** - Multiple old implementations can be accidentally imported
5. **Data inconsistency** - Duplicate ledger files can diverge

**Single source of truth** for each function eliminates all these harms.
