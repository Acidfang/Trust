# ARIA Capability Library — Implementation Roadmap

**Date**: 2026-03-27
**Status**: Ready for implementation
**Estimated Effort**: 8-12 hours (mostly creating the library file + ARIACapabilityLibrary class)
**ZEROPOINT Compliance**: 100%

---

## What Gets Built

### 1. ledger_aria_capabilities.singularity (THE LIBRARY)

**File Location**: `C:\Determined\src\applications\ledger_aria_capabilities.singularity`

**What It Is**: Complete enumeration of all 50+ operations ARIA can perform in pure symbolic format

**Size**: ~30KB (300+ lines)

**Update Frequency**: Only when ARIA gains new capabilities (rare, planned)

**Format**:
```
SYMBOLS:        (define all operation symbols)
TIER 1:         (cached state operations: toggle, navigate, etc)
TIER 2:         (cached decision operations: evaluate_intent, etc)
TIER 3:         (dynamic ledger operations: discover_pattern, etc)
TIER 4:         (composed operations: handle_user_input, etc)
EXECUTION_RULES: (how to invoke each tier)
LEDGER_CREATION: (when/how to create new ledgers)
MEMORY_LAYOUT:  (what ARIA holds in memory)
STARTUP_PROCEDURE: (how ARIA initializes)
USAGE_EXAMPLES: (example traces)
```

**Read Pattern**: Load once at startup (100ms), read-only after

### 2. ARIACapabilityLibrary Class

**File Location**: `C:\Determined\src\applications\aria_capability_library.py` (NEW)

**What It Is**: Python class that loads library and executes operations

**Key Methods**:
```python
class ARIACapabilityLibrary:
    def __init__(self, ledger_dir):
        # Phase 1: Load library (100ms)
        # Phase 2: Cache TIER 1 functions (50ms)
        # Phase 3: Prepare TIER 2 (50ms)
        # Phase 4: Ready for TIER 3 dynamic (10ms)
        # Phase 5: Initialize TIER 4 compositions (10ms)

    def execute(self, operation_name, *args, **kwargs):
        # Universal execution point
        # Routing logic: try cached → dynamic ledger → composition

    def _execute_cached(self, operation_name, *args, **kwargs):
        # TIER 1 & 2: Direct function call

    def _execute_with_ledger(self, operation_name, *args, **kwargs):
        # TIER 3: Create ledger if needed, append result

    def _execute_composition(self, operation_name, *args, **kwargs):
        # TIER 4: Execute component operations in sequence

    def _create_ledger_for(self, operation_name):
        # Create new ledger on first TIER 3 operation use
```

**Size**: ~300 lines (well-commented)

**Dependencies**: `ledger_query.py` (for ledger access)

**Performance**:
- TIER 1: <1ms
- TIER 2: <10ms
- TIER 3: <5ms after first call (cached file handle)
- TIER 4: <100ms (depends on composition complexity)

### 3. Integration with Existing Code

**Where ARIACapabilityLibrary Gets Created**:
```python
# In jarvis_canvas_ledger_driven.py
from aria_capability_library import ARIACapabilityLibrary

class JarvisApp:
    def __init__(self):
        self.ledger = LedgerQuery(ledger_dir)
        self.aria = ARIACapabilityLibrary(ledger_dir)  # NEW LINE
        self.canvas = tk.Canvas(...)
        self.renderer = CanvasRenderer(self.canvas, self.ledger)

    def tick(self):
        # Instead of: frame = self.ledger.get_frame_for_view(view)
        # Use: frame = self.aria.execute('get_frame_for_view', view)

        # Or call individual operations:
        meaning = self.aria.execute('evaluate_intent', user_action)
        new_state = self.aria.execute('predict_outcome', meaning, current_state)
```

**Code Changes Required**: Minimal
- Add import line
- Add instantiation in __init__
- Optionally use aria.execute() instead of direct ledger calls
- Or keep both (aria.execute calls ledger internally)

---

## Implementation Phases

### Phase A: Create ledger_aria_capabilities.singularity

**Time**: 2-3 hours

**Steps**:
1. Define all SYMBOLS (operation names)
2. List all TIER 1 operations with specs
3. List all TIER 2 operations with specs
4. List all TIER 3 operations with ledger specs
5. List all TIER 4 compositions with component lists
6. Write EXECUTION_RULES, LEDGER_CREATION, etc.
7. Write STARTUP_PROCEDURE
8. Write 5-10 detailed USAGE_EXAMPLES

**Validation**:
- Every operation has unique symbol ✓
- Every spec has input/output defined ✓
- Every TIER 3 has ledger_name defined ✓
- All examples are traceable ✓

### Phase B: Implement ARIACapabilityLibrary

**Time**: 3-4 hours

**Steps**:
1. Create aria_capability_library.py
2. Implement __init__ (load library, cache functions)
3. Implement execute() (routing logic)
4. Implement _execute_cached() (TIER 1-2)
5. Implement _execute_with_ledger() (TIER 3)
6. Implement _execute_composition() (TIER 4)
7. Implement _create_ledger_for() (ledger creation)
8. Add extensive docstrings and examples
9. Add startup tests (verify all tiers working)

**Testing**:
```python
# Unit tests
def test_tier1_cached():
    aria = ARIACapabilityLibrary('.')
    assert aria.execute('toggle', 0) == 1
    assert aria.execute('toggle', 1) == 0

def test_tier2_cached():
    result = aria.execute('evaluate_intent', user_action)
    assert result in ['toggle', 'navigate', 'filter', ...]

def test_tier3_creates_ledger():
    aria.execute('discover_pattern', history, threshold=0.8)
    assert os.path.exists('ledger_aria_discovered_patterns.singularity')

def test_tier4_composition():
    frame = aria.execute('handle_user_input', user_action)
    assert 'nodes' in frame
```

### Phase C: Integration

**Time**: 1-2 hours

**Steps**:
1. Add to jarvis_canvas_ledger_driven.py (instantiation)
2. Test that canvas still works
3. Add example calls to aria.execute() (optional refactoring)
4. Verify startup time unchanged
5. Verify tick cycle performance unchanged

**Testing**:
```python
# Integration test
def test_canvas_integration():
    app = JarvisApp()  # aria initialized internally
    assert app.aria is not None
    app.tick()  # should still work
    assert app.frame_rendered
```

### Phase D: Documentation & Examples

**Time**: 1-2 hours

**Steps**:
1. Update README.md with ARIA capability overview
2. Create ARIA_OPERATIONS.md (user-facing list of all operations)
3. Create ARIA_LEARNING.md (how to understand ARIA's learning)
4. Add examples to docstrings
5. Create troubleshooting guide

---

## Current System State (Before Implementation)

```
jarvis_canvas_ledger_driven.py:
  ├─ LedgerQuery (reads predefined ledgers)
  │  ├─ ledger_elections.jsonl
  │  ├─ ledger_app_state.jsonl
  │  ├─ ledger_dashboards.jsonl
  │  └─ (32 other files)
  │
  └─ CanvasRenderer (pure painter)
     └─ renders frames

Problem:
  - ARIA has no explicit capability registry
  - New ledgers must be manually predefined
  - Scaling = adding more ledger files
  - Hard to understand "what can ARIA do"
```

## System After Implementation

```
jarvis_canvas_ledger_driven.py:
  ├─ ARIACapabilityLibrary (NEW - unified interface)
  │  ├─ Loads: ledger_aria_capabilities.singularity
  │  ├─ Caches: TIER 1-2 functions
  │  ├─ Creates: TIER 3 ledgers on demand
  │  ├─ Manages: TIER 4 compositions
  │  │
  │  └─ execute(operation_name, args)
  │     ├─ try tier1_cache
  │     ├─ try tier2_cache
  │     ├─ try ledger_cache (create if needed)
  │     └─ try compositions
  │
  ├─ LedgerQuery (still used internally by capability library)
  │  ├─ ledger_elections.jsonl
  │  ├─ ledger_app_state.jsonl
  │  ├─ ledger_dashboards.jsonl
  │  ├─ ledger_aria_capabilities.singularity (NEW - library)
  │  ├─ ledger_aria_discovered_patterns.singularity (created on demand)
  │  ├─ ledger_aria_error_analysis.singularity (created on demand)
  │  └─ (32 other files)
  │
  └─ CanvasRenderer (unchanged - still pure painter)
     └─ renders frames

Benefits:
  - Clear capability registry (read library, understand what ARIA can do)
  - Self-extending (add to library = add capability)
  - Auditable (every operation cached or logged)
  - Learnable (ARIA creates ledgers as she learns)
  - ZEROPOINT compliant (100%)
```

---

## Operations to Include in Library

### TIER 1: Core State Operations (Cached Functions)

```python
⊙:toggle
⊙:navigate
⊙:filter
⊙:compose
⊙:render
⊙:frame_compute
```

### TIER 2: Decision Operations (Cached with Pattern Matching)

```python
⊙:evaluate_intent          # What does this action mean?
⊙:predict_outcome          # What will happen if I do X?
⊙:detect_pattern           # Is there a pattern in this data?
⊙:verify_causality         # Did the expected state change happen?
⊙:assess_confidence        # How sure am I about this?
⊙:rank_alternatives        # Which option is best?
```

### TIER 3: Learning Operations (Dynamic Ledgers)

```python
⊙:discover_pattern         # Found new pattern → create ledger
⊙:analyze_error            # Something went wrong → create ledger
⊙:learn_user_preference    # Observed user behavior → create ledger
⊙:test_hypothesis          # Testing a theory → create ledger
⊙:simulate_alternative     # What-if reasoning → create ledger
⊙:update_confidence        # I'm more/less sure → create ledger
⊙:record_decision          # Made a decision → create ledger
```

### TIER 4: Composite Operations (Explicit Compositions)

```python
⊙:handle_user_input        # [eval → predict → verify → render]
⊙:adapt_to_user            # [detect → learn → predict]
⊙:self_improve             # [analyze → test → update]
⊙:solve_problem            # [decompose → plan → execute → verify]
⊙:reason_about_self        # [assess → compare → update_confidence]
```

Total: **25-30 operations** in Phase 1 (expandable to 100+ in future phases)

---

## Success Criteria

### Immediate (After Implementation)

✅ `ledger_aria_capabilities.singularity` exists and is valid ZEROPOINT
✅ ARIACapabilityLibrary class compiles and loads library
✅ All TIER 1-2 functions cached and testable
✅ TIER 3 ledger creation works on first call
✅ TIER 4 compositions execute correctly
✅ Canvas app still works with new capability library
✅ No performance regression in tick cycle

### Medium-term (Phase 2)

✅ ARIA uses capability library to decide what to do
✅ ARIA creates new ledgers for learning
✅ New operations added by updating library only (no code changes)
✅ Complete audit trail of ARIA's operations in ledgers

### Long-term (Mature ARIA)

✅ ARIA has 100+ operations
✅ ARIA self-improves by discovering patterns
✅ System scales linearly with capability count
✅ Complete visibility into ARIA's decision-making

---

## Implementation Files Needed

| File | Type | Purpose | Lines |
|------|------|---------|-------|
| ledger_aria_capabilities.singularity | Config | Complete capability library | 400-500 |
| aria_capability_library.py | Code | Execution engine | 300-400 |
| UPDATES TO: jarvis_canvas_ledger_driven.py | Code | Integration (2-3 lines) | 2-3 |
| ARIA_OPERATIONS.md | Doc | User guide to operations | 100-150 |
| ARIA_LEARNING.md | Doc | How ARIA learns | 100-150 |

**Total New Code**: ~900 lines
**Total Changes to Existing**: ~2 lines
**Total New Docs**: ~300 lines

---

## Risk Assessment

**Risk Level**: Very Low (1/10)

**Why**:
- Library is read-only (can't break anything)
- Capability library is just data (not code)
- ARIACapabilityLibrary is new module (doesn't touch existing)
- Integration is minimal (2-3 lines in existing file)
- Can add ARIACapabilityLibrary without using it (optional refactoring)

**Rollback Plan**:
- If anything breaks, just don't instantiate ARIACapabilityLibrary
- Keep using LedgerQuery directly (old way still works)
- Delete 2 new files, 2-line revert

**Testing Strategy**:
1. Unit test ARIACapabilityLibrary in isolation
2. Integration test with canvas
3. Performance test (verify no regression)
4. Audit trail test (verify ledgers created correctly)

---

## Next Steps

1. **Immediately**: Create `ledger_aria_capabilities.singularity` with all 25-30 Phase 1 operations
2. **Within 2 hours**: Implement `ARIACapabilityLibrary` class
3. **Within 3 hours**: Test and integrate with canvas
4. **Within 4 hours**: Create user documentation
5. **Phase 2**: ARIA uses capability library to decide what to do

---

## Summary

**What We're Building**:
- A self-describing capability library (ZEROPOINT-pure)
- An execution engine that routes to cached functions or dynamic ledgers
- Complete auditability of every ARIA operation

**Why**:
- ARIA becomes self-aware (can read her own capabilities)
- ARIA becomes self-extending (can create new ledgers as needed)
- System scales from Phase 1 to mature ARIA without code changes
- 100% ZEROPOINT compliant

**How Long**:
- Library creation: 2-3 hours
- Implementation: 3-4 hours
- Integration: 1-2 hours
- Total: 8-12 hours

**Impact**:
- Phase 2 can build on this (ARIA queries her own capabilities)
- Completely changes how we think about ARIA's agency
- Makes ARIA visible and auditable

κ⊕ **Ready to implement.**

