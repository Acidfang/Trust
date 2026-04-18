# PROJECT REFACTORING PLAN
## Aligning Determined Project Structure with Intent

**Status**: Planning phase  
**Date**: April 18, 2026  
**Purpose**: Reorganize project to reflect 4-tier architecture and enforcement system

---

## CURRENT STATE ANALYSIS

The project has grown to include:
1. **Original Singularity Format proof** (4 concepts)
2. **Data archives** (156,445 messages)
3. **Implementation code** (4 Python scripts)
4. **Documentation** (6 specification files)
5. **NEW: Enforcement system** (Trinity verification, auto-rollback)

**Problem**: Files are mixing across categories. New enforcement system not integrated into main architecture.

---

## IDEAL STRUCTURE (POST-REFACTOR)

```
c:\Determined\

├── 📚 DOCUMENTATION/
│   ├── 00_START_HERE.md                    (← Entry point)
│   ├── PROJECT_INTENT.md                   (← Why this exists)
│   ├── QUICKSTART.md                       (← How to start)
│   │
│   ├── SPECIFICATION/
│   │   ├── SINGULARITY_FORMAT_SPECIFICATION.md
│   │   ├── ARCHITECTURE.md
│   │   └── COMPLIANCE_CHECKLIST.md
│   │
│   ├── IMPLEMENTATION/
│   │   ├── IMPLEMENTATION_GUIDE.md
│   │   └── CODE_WALKTHROUGH.md (NEW)
│   │
│   ├── Trinity_ENFORCEMENT/
│   │   ├── MANDATORY_AI_ENFORCEMENT_GATE.md
│   │   ├── README_MANDATORY_START_HERE.md
│   │   ├── INESCAPABLE_ENFORCEMENT_MANIFEST.md
│   │   └── PROJECT_ENFORCEMENT_INITIALIZATION.md
│   │
│   └── VALIDATION/
│       ├── VALIDATION_REPORT.md
│       └── CASE_STUDIES.md (NEW)
│
├── 🔒 PROOF/                               (Real data in singularity format)
│   ├── VALIDATED_KNOWLEDGE_SINGULARITY.json
│   ├── validated_explanations.json
│   ├── DISCOVERED_KNOWLEDGE_SINGULARITY.json (NEW)
│   └── singularity_format_basis_validated.md
│
├── 💻 CODE/
│   ├── CORE/
│   │   ├── singularity_storage.py            (50+ methods)
│   │   ├── singularity_core.py (NEW)         (Refactored imports)
│   │   └── __init__.py (NEW)
│   │
│   ├── ENFORCEMENT/
│   │   ├── PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py
│   │   ├── project_coherence_integration.py (NEW - bridges to core)
│   │   └── __init__.py (NEW)
│   │
│   ├── UTILITIES/
│   │   ├── extract_validated_pairs.py
│   │   ├── convert_to_singularity_format.py
│   │   ├── show_singularity_proof.py
│   │   └── __init__.py (NEW)
│   │
│   ├── TESTS/
│   │   ├── test_accountability_audit.py
│   │   ├── test_singularity_format.py (NEW)
│   │   └── __init__.py (NEW)
│   │
│   └── main.py (NEW - unified entry point)
│
├── 📊 DATA/
│   ├── SOURCES/
│   │   ├── UNIFIED_MASTER_TIMELINE.json
│   │   ├── technical_definitions.json
│   │   ├── technical_basis_extracted.json
│   │   ├── unified_discoveries_integrated.json
│   │   └── accountability_unified_fast.json
│   │
│   └── EXTRACTED/
│       ├── extracted_meanings.json (NEW)
│       └── extracted_patterns.json (NEW)
│
├── 🔐 .claude/
│   ├── CLAUDE.md
│   ├── MANDATORY_AI_ENFORCEMENT_GATE.md
│   ├── PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py
│   └── COHERENCE_CHECKPOINTS.json (ledger)
│
├── 📦 ARCHIVE/
│   ├── LEGACY_FILES/
│   │   ├── (old organization files)
│   │   └── (reference for historical context)
│   │
│   └── MIGRATION_LOG.md
│
├── 🎯 PROJECT_MANIFEST.md (REFACTORED - master index)
├── 📖 README.md (REFACTORED - top-level guide)
└── 📋 INDEX.md (NEW - complete file inventory)
```

---

## REFACTORING PHASES

### PHASE 1: Create Folder Structure
- Create all directories
- Document purpose of each
- Create __init__.py files for Python packages

### PHASE 2: Move Files to Appropriate Locations
- Documentation files → DOCUMENTATION/
- Proof files → PROOF/
- Code files → CODE/ (with subcategories)
- Data files → DATA/
- Enforcement files → Both .claude/ and DOCUMENTATION/TRINITY_ENFORCEMENT/
- Legacy files → ARCHIVE/

### PHASE 3: Update Import Paths in Code
- Fix all relative imports
- Update file path references
- Ensure circular dependencies are eliminated

### PHASE 4: Create Integration Bridges
- Create project_coherence_integration.py to connect enforcement with core
- Create main.py as unified entry point
- Ensure enforcement system hooks into initialization

### PHASE 5: Update Documentation
- Create 00_START_HERE.md (true entry point)
- Create PROJECT_INTENT.md (explain the 4 concepts)
- Create CODE_WALKTHROUGH.md (guide through code structure)
- Update INDEX.md with file locations
- Refactor PROJECT_MANIFEST.md for new structure

### PHASE 6: Verification & Testing
- Verify all imports work
- Run test suite
- Check Trinity verification on all modified files
- Validate coherence of new structure

---

## KEY CHANGES TO CODE

### singularity_storage.py
**Current**: Imports from same directory  
**After**: Located in CODE/CORE/singularity_storage.py
- All method signatures unchanged
- Import paths updated if needed
- Can be imported as: `from CODE.CORE.singularity_storage import SingularityStore`

### PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py
**Current**: Root level  
**After**: CODE/ENFORCEMENT/ + .claude/ (dual location for global access)
- Core logic in CODE/ENFORCEMENT/
- Symlink/reference in .claude/ for enforcement gate
- Create integration bridge in CODE/ENFORCEMENT/project_coherence_integration.py

### Extract/Convert/Show Scripts
**Current**: Root level  
**After**: CODE/UTILITIES/
- update_relative_imports.py (NEW - handles path updates)
- All maintain API compatibility

### Test Files
**Current**: Root level  
**After**: CODE/TESTS/
- test_accountability_audit.py → CODE/TESTS/
- test_singularity_format.py (NEW)
- CI/CD integration ready

---

## INTEGRATION POINTS

### Trinity Enforcement Integration
The enforcement system should:
1. Load all project tasks in context
2. Verify Trinity on all modified files
3. Record checkpoint for refactoring as single action
4. Ensure no violation detection on moved files

**Implementation**:
```python
# CODE/ENFORCEMENT/project_coherence_integration.py
from CODE.CORE.singularity_storage import SingularityStore
from CODE.ENFORCEMENT.PROJECT_COHERENCE_CHECKPOINT_SYSTEM import create_verified_action

# On startup, verify project coherence
# Register refactoring as single Trinity-verified action
```

### Unified Entry Point
```python
# CODE/main.py
"""
Unified entry point for Determined project
- Initialize enforc system
- Load SingularityStore
- Verify project coherence
- Provide CLI for all utilities
"""
```

---

## MIGRATION STRATEGY

### Step-by-Step Execution
1. Create all folders (non-destructive)
2. Copy (not move) files to new locations
3. Update imports in code
4. Test that imports work
5. Register refactoring in enforcement system
6. Move original files to ARCHIVE/
7. Update documentation
8. Verify everything works

### Rollback Safety
- Original files preserved in ARCHIVE/
- Git history maintained (if using version control)
- MIGRATION_LOG.md documents every change
- Can revert by moving files back if needed

---

## SUCCESS CRITERIA

✓ All files organized by tier/category  
✓ All imports updated and working  
✓ Enforcement system integrated  
✓ NEW: unified entry point (main.py)  
✓ NEW: comprehensive navigation (00_START_HERE.md)  
✓ NEW: project intent clarity (PROJECT_INTENT.md)  
✓ Documentation navigable from any point  
✓ Trinity verified on all changes  
✓ Code passes all tests  

---

## BENEFITS AFTER REFACTORING

| Aspect | Before | After |
|--------|--------|-------|
| **Clarity** | 200+ files in root | Organized by 5 tiers |
| **Navigation** | Confusing | 00_START_HERE → clear path |
| **Intent** | Implicit | Explicit (PROJECT_INTENT.md) |
| **Enforcement** | Added separately | Integrated into architecture |
| **Extensibility** | Hard to add new | Easy (folder structure ready) |
| **Trinity** | Checkpoint system exists | Fully integrated in workflow |
| **Entry Point** | No clear start | main.py unified entry |
| **Documentation** | 6 files scattered | Organized in DOCUMENTATION/ |

---

## REFACTORING COSTS & BENEFITS

**Time**: ~2-3 hours to execute (now that plan is clear)  
**Risk**: Low (files preserved, reversible)  
**Benefit**: High (project becomes navigable, maintainable, extensible)  

**For Next AI**: Will be able to:
- Read 00_START_HERE.md and understand project immediately
- Navigate to any component via clear folder structure
- Run `main.py` to start using the system
- Understand intent from PROJECT_INTENT.md
- Follow Trinity enforcement automatically

---

**Status**: PLAN READY FOR EXECUTION  
**Next**: Begin Phase 1 (Create Folders)
