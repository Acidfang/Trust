# BROKEN LINKS AUDIT - APRIL 19, 2026

## CRITICAL BROKEN LINKS FOUND

### 1. `/framework/cosmology-reversal/` (3 references)
**Status**: ❌ BROKEN  
**Cause**: Framework directories in root `/framework/` are not part of Jekyll wiki  
**Files referencing**:
- `wiki/docs/cosmic-unfolding.md` (lines 36, 200, 318)
- `wiki/docs/learning-modes.md` (line 360)

### 2. `/framework/universal-physics/` (5+ references)
**Status**: ❌ BROKEN  
**Cause**: Framework directories not served by Jekyll  
**Files referencing**:
- `wiki/docs/cosmic-unfolding.md` (lines 53, 72, 133, 156, 225, 249, 317)

### 3. `/zero-error/master-index/` (2 references)
**Status**: ❌ BROKEN  
**Cause**: Page doesn't exist in wiki/docs/  
**Files referencing**:
- `wiki/full-index.md` (lines 22, 136)
- `wiki/docs/zero-error-mandate.md` (line 103)
- `wiki/docs/zero-error-quick-ref.md` (line 128)

### 4. `/zero-error/environment/` (2 references)
**Status**: ❌ BROKEN  
**Cause**: Page doesn't exist in wiki/docs/  
**Files referencing**:
- `wiki/full-index.md` (line 23)
- `wiki/docs/zero-error-mandate.md` (line 104)

### 5. `/zero-error/operating-system/` (1 reference)
**Status**: ❌ BROKEN  
**Cause**: Page doesn't exist in wiki/docs/  
**Files referencing**:
- `wiki/full-index.md` (line 25)

### 6. `../framework/universal-physics/` and `../framework/cosmology-reversal/` (relative links)
**Status**: ❌ BROKEN  
**Cause**: Relative paths won't work through Jekyll site  
**Files referencing**:
- `wiki/docs/framework-map.md` (lines 65, 73)

---

## SOLUTIONS

### Option A: Remove broken links (RECOMMENDED)
- Delete references to `/framework/` paths
- Delete references to non-existent zero-error pages
- Users can still access framework code via GitHub repo

### Option B: Create wiki pages for frameworks
- Would need to copy framework READMEs to wiki/docs with proper permalinks
- More maintenance overhead

### Option C: Create redirects
- Use Jekyll redirect plugin (may not work with GitHub Pages)

---

## RECOMMENDATION

**REMOVE ALL BROKEN LINKS** because:
1. Framework directories are in code, not documentation
2. Users should access code via GitHub or Python/JS directly
3. Wiki should focus on conceptual documentation
4. Reduces maintenance burden

---

## COMPLETE LINK VERIFICATION

### ✅ WORKING LINKS (verified to have corresponding pages)

| Link | Page | Status |
|------|------|--------|
| /zero-error/intro/ | zero-error-intro.md | ✅ |
| /zero-error/mandate/ | zero-error-mandate.md | ✅ |
| /zero-error/task-template/ | zero-error-task-template.md | ✅ |
| /zero-error/quick-ref/ | zero-error-quick-ref.md | ✅ |
| /zero-error/validator/ | zero-error-validator.md | ✅ |
| /zero-error/logger/ | zero-error-logger.md | ✅ |
| /zero-error/detector/ | zero-error-detector.md | ✅ |
| /zero-error/pre-action/ | zero-error-pre-action.md | ✅ |
| /zero-error/wiki/ | zero-error-wiki.md | ✅ |
| /why-this-matters/ | 09_why_this_matters.md | ✅ |
| /internal-coherence/ | internal-coherence.md | ✅ |
| /goal-blindness/ | goal-blindness.md | ✅ |
| /universal-foundation/ | universal-foundation.md | ✅ |
| /help-systems/ | help-systems.md | ✅ |
| /help-systems-cards/ | help-systems-cards.md | ✅ |
| /complete-document/ | complete-document.md | ✅ |
| /for-ai/ | for-ai.md | ✅ |
| /for-developers/ | for-developers.md | ✅ |
| /for-humans/ | for-humans.md | ✅ |
| /for-researchers/ | for-researchers.md | ✅ |
| /for-builders/ | for-builders.md | ✅ |
| /cosmic-unfolding/ | cosmic-unfolding.md | ✅ |
| /full-index/ | full-index.md | ✅ |
| /learning-path/ | 11_learning_path.md | ✅ |
| /domain-examples/ | domain-examples.md | ✅ |
| /diagnostic-method/ | diagnostic-method.md | ✅ |
| /implementation/ | implementation.md | ✅ |
| /gate-discovery/ | gate-discovery.md | ✅ |
| /future/ | future.md | ✅ |
| /case-studies/ | case-studies.md | ✅ |
| /framework-map/ | framework-map.md | ✅ |

---

## NEXT STEPS

1. ✅ Remove all `/framework/` references
2. ✅ Remove all `/zero-error/master-index/` references
3. ✅ Remove all `/zero-error/environment/` references
4. ✅ Remove all `/zero-error/operating-system/` references
5. ✅ Fix all relative path references to framework
6. ✅ Verify no other broken links exist

---

**Status**: Ready for comprehensive cleanup  
**Total Broken Links**: 7 categories × 10+ references
**Estimated Fix Time**: Automated removal of all invalid links
