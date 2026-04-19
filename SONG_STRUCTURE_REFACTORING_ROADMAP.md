# Song Structure Refactoring Roadmap (April 19, 2026)

**Objective**: Integrate free/bound photon principle into all code. Every function follows the tier-based rhythm.

**Universal Principle**: Code resonates like a song through alternating BOUND (verification) and FREE (flexibility) states.

---

## Phase 1: Establish the Pattern (TIER -1 BOUND)

### 1.1 Document the Pattern
- **File**: Update `.instructions.md` with "Song-Structured Functions" section
- **Content**: Show function template with explicit tier comments
- **Purpose**: Make the pattern visible and teachable

### 1.2 Create Template
- **File**: Create `SONG_FUNCTION_TEMPLATE.py`
- **Content**: Reference implementation showing rhythm structure
- **Purpose**: Provide copy-paste starting point for all functions

**Status**: 🔄 IN PROGRESS

---

## Phase 2: Update Framework Scripts (TIER 0 FREE → TIER 1 BOUND)

These scripts embody critical thinking. They must exemplify the pattern.

### 2.1 `framework_compliance_checker.py`
- **Current**: Checks if frameworks are referenced, but doesn't embody them
- **Change**: Add tier structure to each method
  - `__init__`: TIER -1 (establish honest constraints)
  - `check_framework_references()`: TIER 1 (root cause: what's missing?)
  - `check_decision_logging()`: TIER 2 (consistency everywhere?)
  - `report()`: TIER 3+ (automatic integration)

### 2.2 `pre_edit_verification.py`
- **Current**: Verifies startup context exists, but linear structure
- **Change**: Tier-structured verification flow
  - TIER -1: What must be true to proceed?
  - TIER 0: What could be wrong?
  - TIER 1: Root cause checks (not surface validation)
  - TIER 2: Consistency across all checks
  - TIER 3+: Make verification automatic

### 2.3 `pre_commit_validator.py`
- **Current**: Validates before commit with linear checks
- **Change**: Tier-structured validation
  - TIER -1: Honest assessment of what was actually verified
  - TIER 0: Surface vs. real validity
  - TIER 1: Root cause failures (not just syntax)
  - TIER 2: Applied uniformly to all changes
  - TIER 3+: Auto-validation as default

### 2.4 `framework_compliance_checker.py` (secondary)
- **Current**: Checks framework references
- **Change**: Embody the frameworks it checks

**Status**: 🔄 NEXT

---

## Phase 3: Apply to Support Scripts (TIER 2 FREE → BOUND)

These should follow the pattern too.

### 3.1 `decision_logger.py`
- Log decisions with tier context
- Show which tier decision belongs to

### 3.2 `duplicate_detector.py`
- Tier-structured detection (root cause, not just duplicates)

### 3.3 `project_startup.py`
- Startup follows tier sequence: honesty → exploration → locking → consistency → automation

### 3.4 `project_orientation.py`
- Tier-structured orientation process

**Status**: 📋 PLANNED

---

## Phase 4: Documentation Updates (TIER 1 BOUND)

Make the pattern teachable and visible.

### 4.1 Update `.instructions.md`
Add section: "How to Code Like a Song (Tier Structure in Functions)"
- Show template
- Show 3 examples
- Show how tiers appear in Python syntax

### 4.2 Create `SONG_FUNCTION_TEMPLATE.py`
Reference implementation with detailed comments showing tier structure

### 4.3 Create `TIER_CODING_PATTERNS.md`
- How to recognize tier structure
- How to spot missing tiers
- How to refactor toward song structure

**Status**: 📋 PLANNED

---

## Phase 5: Verification & Integration (TIER 3+ BOUND)

Ensure refactoring actually improved things.

### 5.1 Test Updated Scripts
- Run each script with tier-structured code
- Verify they work correctly
- Verify they're easier to understand

### 5.2 Apply to All Future Code
- New functions always follow song structure
- Automated checking for missing tiers

### 5.3 Integration Complete
- Song structure is automatic, not manual
- Every function naturally embodies TIER -1 through 3+

**Status**: 📋 FUTURE

---

## Implementation Sequence

**TODAY (April 19, 2026)**:
1. ✅ Create this roadmap
2. 🔄 Update `.instructions.md` with pattern
3. 🔄 Create `SONG_FUNCTION_TEMPLATE.py`
4. 🔄 Refactor `framework_compliance_checker.py`
5. 🔄 Refactor `pre_edit_verification.py`
6. 🔄 Refactor `pre_commit_validator.py`
7. ✅ Commit all changes

**Next Session**:
1. Refactor support scripts (Phase 3)
2. Create documentation (Phase 4)
3. Verify and validate (Phase 5)

---

## Success Criteria

✅ **Phase 1 Complete**: Pattern is documented and visible
✅ **Phase 2 Complete**: Framework scripts embody the principle
✅ **Phase 3 Complete**: All scripts tier-structured
✅ **Phase 4 Complete**: Pattern is teachable
✅ **Phase 5 Complete**: All new code automatically follows pattern

**Final State**: Every function in workspace has explicit tier structure. Code resonates.

---

## Key Insight

The song structure isn't decoration. It's the actual architecture:

```
Function = TIER -1 (BOUND) + TIER 0 (FREE) + TIER 1 (BOUND) + TIER 2 (FREE) + TIER 3+ (BOUND)
```

When code follows this rhythm, it's not just correct—it's **coherent**.
