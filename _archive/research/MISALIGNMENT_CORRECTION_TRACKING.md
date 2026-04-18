# MISALIGNMENT CORRECTION CHECKLIST
**Date**: April 3, 2026  
**Purpose**: Track all files containing outdated coherence values  
**Status**: Critical vs. Contextual

---

## 🔴 CRITICAL: Entity Coherence Values (Must Update)

These represent coherence values for the 8 entity scales and directly violate verified framework.

### ENCYCLOPEDIA_README.md
**Source of Original Error**
- Line 325: `τ ≈ 0.85`: Human consciousness → **Should be: τ ≈ 0.45**
- Line 326: `τ ≈ 0.65`: Ecosystems → **Should be: τ ≈ 0.40**
- Line 327: `τ ≈ 0.55`: Civilizations → **Should be: τ ≈ 0.32**
- **Status**: ⏳ NEEDS UPDATE
- **Impact**: This is the authoritative documentation. When developers look for coherence values, they find these wrong ones.

### FIELD_IMAGE_GENERATOR.py  
**Copies from README**
- Line 329: `τ ≈ 0.85 | Unified field perception + Agency` (Human visualization)
- **Status**: ⏳ NEEDS UPDATE
- **Impact**: SVG visualizations show incorrect coherence label

### FIELD_IMAGE_GENERATOR_V2.py
**Old Version (May Be Archived)**
- Line 86: `'coherence': 0.85,` (Human entity)
- **Status**: 🟡 CHECK IF ARCHIVED (if active, needs update)
- **Impact**: If used, propagates error

---

## 🟡 CONTEXTUAL: System Coherence Values (Different Context)

These represent ARIA's internal coherence state (heartbeat, processing), NOT entity scales. **May not need updating** - verify context.

### generate_aria_books.py
- Multiple lines with `"coherence": 0.85`
- **Question**: Is this ARIA's system coherence or entity coherence?
- **If system coherence**: May be correct (unrelated to entity scales)
- **If entity coherence**: Needs review
- **Status**: NEEDS CONTEXT CHECK

### PATTERN_COMPLETION_BASELINE.py
- Lines 435, 620: `'system_coherence': 0.85`
- **Question**: Is this ARIA's processing coherence or entity measurement?
- **Status**: NEEDS CONTEXT CHECK (likely different domain)

### Other System-Level Uses
- `expression_election_engine.py` line 409: Appears to be processing coherence
- `test_consciousness_ledger.py` lines 60, 77: Test data (may be fixture/placeholder)
- **Status**: NEEDS CONTEXT CHECK

---

## ✅ ALREADY CORRECTED

### ENCYCLOPEDIA_API_SERVER.py
- ✅ Cell: 0.82 → 0.60 (DONE)
- ✅ Human: 0.85 → 0.45 (DONE)  
- ✅ Ecosystem: 0.65 → 0.40 (DONE)
- ✅ Civilization: 0.55 → 0.32 (DONE)

---

## 📋 ACTION ITEMS

### Priority 1 (Entity Scale Alignment)
- [ ] **ENCYCLOPEDIA_README.md** - Update lines 325-327 with correct values
  - Human: 0.85 → 0.45
  - Ecosystem: 0.65 → 0.40
  - Civilization: 0.55 → 0.32

- [ ] **FIELD_IMAGE_GENERATOR.py** - Update line 329 with correct human coherence
  - Change: `τ ≈ 0.85` to `τ ≈ 0.45`
  - Update description to reflect lower coherence

### Priority 2 (Version Control)
- [ ] **FIELD_IMAGE_GENERATOR_V2.py** - Check if archived or active
  - If active: Update line 86
  - If archived: Mark as legacy

### Priority 3 (Context Verification)
- [ ] **generate_aria_books.py** - Verify context of 0.85 values
  - Are these entity coherence or system coherence?
  - If entity: update to framework values
  - If system: may leave as-is

- [ ] **PATTERN_COMPLETION_BASELINE.py** - Verify system coherence context
  - If system-specific: leave as-is
  - If entity-related: align with framework

- [ ] **Other files** - Audit for entity vs. system coherence usage

---

## VERIFICATION RULES (To Prevent Recurrence)

Add to development guidelines:

1. **Entity Coherence Values**
   - Must come from COHERENCE_FIELD_MODEL_GUIDE.md (authoritative source)
   - Must satisfy: τ = 1 - H(ΔS) / H_max
   - Must be monotonically decreasing: Electron (0.99) > Atom (0.75) > ... > Civilization (0.32)

2. **System Coherence Values** (ARIA internal)
   - Different namespace from entity scales
   - Should be clearly labeled as "system_coherence" or "processing_coherence"
   - Not constrained by entity gradient rules

3. **Test Cases**
   ```python
   def test_entity_coherence_gradient():
       """Verify entity coherence values follow verified framework"""
       entities = ["Electron", "Atom", "Carbon", "Water", "Cell", "Human", "Ecosystem", "Civilization"]
       coherence_values = [0.99, 0.75, 0.78, 0.72, 0.60, 0.45, 0.40, 0.32]
       
       # Verify monotonic decrease (mostly)
       for i in range(len(coherence_values)-1):
           assert coherence_values[i] >= coherence_values[i+1], \
               f"Gradient violation: {entities[i]} ({coherence_values[i]}) " \
               f"> {entities[i+1]} ({coherence_values[i+1]})"
   ```

---

## COMPLETION STATUS

| File | Type | Status | Priority |
|------|------|--------|----------|
| ENCYCLOPEDIA_API_SERVER.py | Entity | ✅ CORRECTED | - |
| ENCYCLOPEDIA_README.md | Entity (Doc) | ⏳ PENDING | 1 |
| FIELD_IMAGE_GENERATOR.py | Entity (Visual) | ⏳ PENDING | 1 |
| FIELD_IMAGE_GENERATOR_V2.py | Entity (Archive?) | 🟡 CHECK | 2 |
| generate_aria_books.py | System? | 🟡 VERIFY | 3 |
| PATTERN_COMPLETION_BASELINE.py | System? | 🟡 VERIFY | 3 |

**Overall Progress**: 1/8 corrected. 2 critical pending. 5 requiring context verification.
