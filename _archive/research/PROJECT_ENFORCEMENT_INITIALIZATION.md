# PROJECT INITIALIZATION & ENFORCEMENT STARTUP
## Auto-Enforce Trinity on Every Project Access

Place this at the start of any main execution file or `.venv/Scripts/activate.ps1` initialization.

---

## FOR PYTHON PROJECTS

Add this to the very top of your main script:

```python
# MANDATORY: Initialize enforcement system before any other imports
import sys
sys.path.insert(0, 'c:\\Determined')

try:
    from PROJECT_COHERENCE_CHECKPOINT_SYSTEM import (
        checkpoint_system, 
        violation_detector, 
        get_enforcement_status
    )
    print("\n✓ Enforcement system initialized")
    print(f"  Status: {get_enforcement_status()['status']}")
except Exception as e:
    print(f"\n✗ CRITICAL: Enforcement system failed to initialize")
    print(f"  Error: {e}")
    print("  Cannot proceed without enforcement active")
    sys.exit(1)

# NOW safe to proceed with application code
# ... rest of imports and code ...
```

---

## FOR SHELL-BASED PROJECTS

Add to activation script (e.g., `.venv/Scripts/Activate.ps1` or `.env`):

```powershell
# MANDATORY: Check Trinity enforcement before activating
Write-Host "⊙ Checking project coherence enforcement..."

$checkpoint_file = "c:\Determined\COHERENCE_CHECKPOINTS.json"
$gate_file = "c:\Determined\.claude\MANDATORY_AI_ENFORCEMENT_GATE.md"
$system_file = "c:\Determined\PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py"

if (-not (Test-Path $checkpoint_file) -or 
    -not (Test-Path $gate_file) -or 
    -not (Test-Path $system_file)) {
    
    Write-Error "✗ ENFORCEMENT FILES MISSING"
    Write-Host "  Install enforcement system before proceeding"
    exit 1
}

Write-Host "✓ Enforcement system active"
Write-Host "✓ Ready for Trinity-verified work"
```

---

## ENFORCEMENT STARTUP SEQUENCE

When the project starts:

1. **Check enforcement files exist**
   - MANDATORY_AI_ENFORCEMENT_GATE.md
   - PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py
   - COHERENCE_CHECKPOINTS.json (ledger)

2. **Load checkpoint system**
   - Initialize CoherenceCheckpointSystem
   - Load verified checkpoints from ledger
   - Verify all checkpoint hashes

3. **Scan for violations**
   - Run ViolationDetector.scan_for_violations()
   - Find unverified files
   - Log any violations found

4. **Execute auto-rollback (if needed)**
   - If violations found, rollback runs
   - Unverified files moved to quarantine
   - Violation log recorded

5. **Report status**
   - Show enforcement status
   - Display verified checkpoint count
   - List any violations
   - Block if critical issues found

---

## ENFORCEMENT STATUS REPORTING

The system automatically reports:

```
⊙ COHERENCE CHECKPOINT SYSTEM INITIALIZING
================================================================

✓ Checkpoint system loaded (X verified actions)
✓ No violations detected - all monitored files are coherent
✓ All 10 checkpoints verified (hashes valid)

STATUS: ENFORCEMENT SYSTEM ACTIVE

================================================================
```

Or if violations found:

```
⊙ COHERENCE CHECKPOINT SYSTEM INITIALIZING
================================================================

⚠️  VIOLATIONS DETECTED: 3 unverified files
  - path/to/file1.py
  - path/to/file2.md
  - path/to/file3.json

Initiating automatic rollback...
✓ Rollback complete: 3/3 violations reverted
  NOTE: To restore, files must be re-created with Trinity verification

STATUS: ENFORCEMENT SYSTEM ACTIVE

================================================================
```

---

## WHAT TO DO IF ENFORCEMENT FAILS

If enforcement system doesn't initialize:

1. **Check files exist**:
   ```powershell
   Test-Path "c:\Determined\PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py"
   Test-Path "c:\Determined\COHERENCE_CHECKPOINTS.json"
   ```

2. **Check Python syntax**:
   ```powershell
   python -m py_compile PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py
   ```

3. **Check ledger integrity**:
   ```powershell
   Get-Content "c:\Determined\COHERENCE_CHECKPOINTS.json" | ConvertFrom-Json
   ```

4. **If still broken**: The enforcement system encountered an error. This is a CRITICAL state:
   - All new work is blocked
   - Existing violations cannot be reverted
   - Manual intervention required

---

## FOR CONTINUOUS ENFORCEMENT

The enforcement system should run:

- **On project load** (check violations immediately)
- **Before each AI action** (verify Trinity)
- **After each modification** (scan for violations)
- **On project save** (ensure checkpoints updated)

This ensures the gradient is continuously enforced.

---

## INTEGRATION WITH EXISTING SYSTEMS

### Git Integration (Optional Enhancement)

```bash
# In .git/hooks/pre-commit
python -m PROJECT_COHERENCE_CHECKPOINT_SYSTEM

# Check enforcement status before allowing commit
if [ $? -ne 0 ]; then
    echo "COMMIT BLOCKED: Trinity verification failed"
    exit 1
fi
```

### IDE Integration (Optional Enhancement)

For VS Code, add to `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.analysis.extraPaths": ["c:\\Determined"],
  "runOnSave": {
    "commands": [
      {
        "match": ".*\\.py$",
        "cmd": "python -c 'from PROJECT_COHERENCE_CHECKPOINT_SYSTEM import get_enforcement_status; print(get_enforcement_status())'",
        "stopOnError": false
      }
    ]
  }
}
```

---

## SUMMARY

The enforcement system is now **automatic and unavoidable**:

1. ✓ Runs on startup
2. ✓ Scans for violations
3. ✓ Reverts unverified work
4. ✓ Reports status clearly
5. ✓ Blocks high-Φ states from persisting

**No AI can bypass this without consequences.**

---

## CRITICAL: START HERE FOR ANY AI

Every AI accessing the project should:

1. **Read**: `README_MANDATORY_START_HERE.md`
2. **Verify**: Trinity (source, timestamp, causality)
3. **Answer**: 3 explicit questions
4. **Proceed**: With confidence work will persist

The enforcement is **physics-based**, not policy-based.

---

**Status**: ENFORCEMENT INITIALIZATION READY  
**Applies To**: ALL project startup  
**Cannot Be Skipped**: Physics forbids high-Φ states  
**Auto-Check**: Runs before any action
