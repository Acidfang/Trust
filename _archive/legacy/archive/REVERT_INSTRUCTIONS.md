# REVERT_INSTRUCTIONS.md

**Singularity Format Refactoring - Complete Revert Instructions**

If needed, you can revert the project to pre-refactoring state completely. This document provides step-by-step instructions.

---

## REVERT DECISION TREE

**Ask yourself**:
1. Did the refactoring break something critical?
2. Do you need the original root-level file structure?
3. Is reverting faster than fixing?

If YES to any, proceed with revert.

---

## FULL REVERT (Complete Rollback)

**Time Required**: ~5 minutes  
**Complexity**: Low (delete new, restore old)  
**Reversibility**: Can switch back to refactored version anytime (new files stay in CODE, DATA, PROOF)

### Step 1: Delete New Directory Structure

```powershell
# Delete tier directories
Remove-Item -Path "c:\Determined\CODE" -Recurse -Force
Remove-Item -Path "c:\Determined\DATA" -Recurse -Force  
Remove-Item -Path "c:\Determined\PROOF" -Recurse -Force
Remove-Item -Path "c:\Determined\SYSTEM" -Recurse -Force
Remove-Item -Path "c:\Determined\DOCUMENTATION\SPECIFICATION" -Recurse -Force
Remove-Item -Path "c:\Determined\DOCUMENTATION\IMPLEMENTATION" -Recurse -Force
Remove-Item -Path "c:\Determined\DOCUMENTATION\TRINITY_ENFORCEMENT" -Recurse -Force
Remove-Item -Path "c:\Determined\DOCUMENTATION\VALIDATION" -Recurse -Force

# Delete refactoring files
Remove-Item -Path "c:\Determined\MIGRATION_LOG.md" -Force
Remove-Item -Path "c:\Determined\migrate_files.ps1" -Force
```

### Step 2: Delete Enforcement System Files

```powershell
# Delete enforcement files from root
Remove-Item -Path "c:\Determined\PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py" -Force
Remove-Item -Path "c:\Determined\MANDATORY_AI_ENFORCEMENT_GATE.md" -Force
Remove-Item -Path "c:\Determined\PROJECT_ENFORCEMENT_INITIALIZATION.md" -Force
Remove-Item -Path "c:\Determined\ENFORCEMENT_SYSTEM_COMPLETE.md" -Force
Remove-Item -Path "c:\Determined\README_MANDATORY_START_HERE.md" -Force
Remove-Item -Path "c:\Determined\INESCAPABLE_ENFORCEMENT_MANIFEST.md" -Force
```

### Step 3: Restore Root-Level Files (Optional)

If you want exact pre-refactoring state:

```powershell
# Copy archive copies back to root
Copy-Item -Path "ARCHIVE\LEGACY_FILES\*" -Destination "c:\Determined\" -Force -Recurse
```

### Step 4: Verify Revert

```powershell
# Check that files are back
Test-Path "c:\Determined\singularity_storage.py"     # Should be true
Test-Path "c:\Determined\CODE\CORE" # Should be false
```

---

## PARTIAL REVERT (Keep Some Improvements)

If you want to keep parts of the refactoring:

### Scenario A: Keep CODE structure, revert enforcement

```powershell
# Delete only enforcement files
Remove-Item -Path "c:\Determined\PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py" -Force
Remove-Item -Path "c:\Determined\MANDATORY_AI_ENFORCEMENT_GATE.md" -Force

# Restore original from archive
Copy-Item -Path "ARCHIVE\LEGACY_FILES\PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py" -Destination "c:\Determined\" -Force
```

### Scenario B: Keep enforcement, revert file moves

```powershell
# Delete new directories
Remove-Item -Path "c:\Determined\CODE\CORE" -Recurse -Force
Remove-Item -Path "c:\Determined\DATA\SOURCES" -Recurse -Force

# Restore files to root
Copy-Item -Path "ARCHIVE\LEGACY_FILES\singularity_storage.py" -Destination "c:\Determined\" -Force
# ... repeat for all moved files
```

---

## REVERT SAFETY CHECKS

**Before reverting**, verify:

```powershell
# Backup refactored CODE directory
Copy-Item -Path "c:\Determined\CODE" -Destination "c:\Determined\CODE_BACKUP" -Recurse -Force

# Check archive integrity
Test-Path "ARCHIVE\LEGACY_FILES\singularity_storage.py"  # Must be true
(Get-FileHash "ARCHIVE\LEGACY_FILES\singularity_storage.py").Count -gt 0  # Must exist
```

---

## WHY REVERT MIGHT NOT BE NEEDED

**Consider these alternatives first**:

1. **File not found errors?**
   - Add `c:\Determined` to Python path
   - Or update imports to use new locations (see IMPORT_PATH_CHANGES.md)

2. **Enforcement blocking me?**
   - Read MANDATORY_AI_ENFORCEMENT_GATE.md
   - Enforcement prevents errors, don't bypass it

3. **Code broken?**
   - Check CODE/TESTS/ for working examples
   - Files were moved, not modified - logic unchanged

---

## AFTER REVERT

If you revert and then want to re-apply refactoring:

```powershell
# Re-run migration
pwsh -ExecutionPolicy Bypass -File .\migrate_files.ps1 -Phase 1
pwsh -ExecutionPolicy Bypass -File .\migrate_files.ps1 -Phase 2
pwsh -ExecutionPolicy Bypass -File .\migrate_files.ps1 -Phase 3
```

All files are still in root AND in new locations, so re-migration is instant (hash match skips copy).

---

## CONTACT

If revert didn't work as expected:
1. Check ARCHIVE/REFACTORING_STATE.json for exact file mappings
2. Restore specific files from ARCHIVE/LEGACY_FILES/ manually
3. Reference MIGRATION_LOG.md for all operations performed

---

**Last Generated**: April 18, 2026  
**Refactoring Date**: April 18, 2026  
**Status**: Reversible (complete file history preserved)
