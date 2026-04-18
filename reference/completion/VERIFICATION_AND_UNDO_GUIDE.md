# Verification & Undo Protocol - Practical Implementation Guide

**Date**: April 3, 2026  
**Status**: Mandatory for all actions

---

## Executive Summary

The operating instructions have been updated with a **critical requirement**: 

**Every action must have BOTH:**
1. **Verification**: Proof it worked (tests, checks, measurements)
2. **Undo**: Ability to completely reverse it (rollback, revert, restore)

**Both must be planned BEFORE action, tested BEFORE executing, and verified AFTER.**

This is NOT optional. This is NOT "just for safety". This is fundamental to the decision-making framework.

---

## The Three-State Model

Every action moves through three states that must all be verifiable:

```
[BEFORE STATE] 
      ↓
   [ACTION]
      ↓
[AFTER STATE] ← must verify [AFTER] == expected
      ↓
   [UNDO]
      ↓
[BEFORE STATE] ← must verify [BEFORE] == original
```

If you cannot verify all three states, you cannot execute the action.

---

## Practical Application Examples

### Example 1: Create a New Python File

**Action**: Create `election_ledger_engine.py`

**BEFORE Planning Phase:**

1. **Define Success Criteria (Verification Plan)**
   - File exists at `c:\Determined\election_ledger_engine.py`
   - File contains expected content (check first 100 lines)
   - File is importable: `from election_ledger_engine import ElectionLedger`
   - No syntax errors: `python -m py_compile election_ledger_engine.py` succeeds

2. **Define Undo Mechanism (Undo Plan)**
   - Mechanism: Delete file
   - Exact command: `rm c:\Determined\election_ledger_engine.py` (PowerShell: `Remove-Item c:\Determined\election_ledger_engine.py`)
   - Undo state requirement: File must not exist after undo
   - Undo verification: `Test-Path c:\Determined\election_ledger_engine.py` returns False

3. **Test Undo Mechanism BEFORE Creating File**
   ```powershell
   # Create a marker file
   New-Item -Path "c:\Determined\test_marker.txt" -ItemType File
   # Verify it exists
   Test-Path c:\Determined\test_marker.txt  # Returns True
   # Delete it
   Remove-Item c:\Determined\test_marker.txt
   # Verify it's gone
   Test-Path c:\Determined\test_marker.txt  # Returns False
   # ✓ Undo mechanism verified
   ```

4. **Record the Plan**
   - BEFORE state: No file at `c:\Determined\election_ledger_engine.py`
   - ACTION: Create file with 1000+ lines of code
   - Verification plan documented ✓
   - Undo plan documented ✓
   - Undo mechanism tested ✓

**Execution Phase:**

5. **Execute the Action**
   - Create the file with full content

6. **Verify (MANDATORY - Action not complete without this)**
   ```powershell
   # Check existence
   Test-Path c:\Determined\election_ledger_engine.py  # Must be True ✓
   
   # Check content
   (Get-Content c:\Determined\election_ledger_engine.py | Select-Object -First 1)  
   # Must contain: """ELECTION LEDGER ENGINE... ✓
   
   # Check syntax
   python -m py_compile c:\Determined\election_ledger_engine.py  # Must succeed ✓
   
   # Check importability
   python -c "from election_ledger_engine import ElectionLedger; print('OK')"  # Must work ✓
   ```
   - **Result**: VERIFIED ✓ - File created successfully

7. **Test Undo (Proof of Reversibility)**
   ```powershell
   # Before undo:
   Test-Path c:\Determined\election_ledger_engine.py  # True
   
   # Execute undo
   Remove-Item c:\Determined\election_ledger_engine.py
   
   # After undo:
   Test-Path c:\Determined\election_ledger_engine.py  # Must be False ✓
   
   # Verify [BEFORE] state restored
   ```
   - **Result**: REVERSIBLE ✓ - Can fully undo

8. **Document in Ledger**
   - Action: Successful ✓
   - Verification: Passed all 4 checks ✓
   - Undo tested: Works ✓
   - Timestamp: [when completed]

---

### Example 2: Modify Configuration File

**Action**: Update `settings.py` to change `DEBUG = True`

**BEFORE Planning Phase:**

1. **Define Success Criteria (Verification Plan)**
   - File modified successfully
   - Line change: `DEBUG = False` (was `DEBUG = True`)
   - All other content unchanged
   - Python syntax still valid
   - Import works: `from settings import DEBUG` returns False
   - Test verification: Run existing unit tests that depend on DEBUG setting

2. **Define Undo Mechanism (Undo Plan)**
   - Mechanism: Git revert
   - Save current git hash: `git rev-parse HEAD` = `abc123def456...`
   - Undo command: `git revert abc123def456...` OR `git checkout HEAD -- settings.py`
   - Undo verification: `grep "DEBUG = True" settings.py` returns match

3. **Test Undo Mechanism BEFORE Modifying**
   ```powershell
   # In a test file, make a change, then revert it:
   Add-Content c:\Determined\test_config.py -Value "TEST_VAR = 1"
   # Verify change
   Select-String "TEST_VAR" c:\Determined\test_config.py  # Found ✓
   # Revert (simulate undo)
   git checkout HEAD -- c:\Determined\test_config.py
   # Verify revert
   Select-String "TEST_VAR" c:\Determined\test_config.py  # Not found ✓
   # Undo mechanism works ✓
   ```

4. **Record the Plan - BEFORE State**
   ```powershell
   # Capture BEFORE state
   Get-Content c:\Determined\settings.py | Select-String "DEBUG"
   # Output: DEBUG = True ✓ captured
   ```

**Execution Phase:**

5. **Execute the Action**
   - Modify settings.py: `DEBUG = True` → `DEBUG = False`

6. **Verify (MANDATORY)**
   ```powershell
   # Verify change made
   Get-Content c:\Determined\settings.py | Select-String "DEBUG"
   # Must show: DEBUG = False ✓
   
   # Verify syntax valid
   python -m py_compile c:\Determined\settings.py  # Must succeed ✓
   
   # Verify import works
   python -c "from settings import DEBUG; print(DEBUG)"  # Must print False ✓
   
   # Run unit tests
   python -m pytest tests/ -k "settings"  # Must pass ✓
   ```
   - **Result**: VERIFIED ✓ - Change successful and correct

7. **Test Undo (Proof of Reversibility)**
   ```powershell
   # Before undo:
   Get-Content c:\Determined\settings.py | Select-String "DEBUG"
   # Shows: DEBUG = False ✓
   
   # Execute undo
   git revert abc123def456...
   
   # After undo:
   Get-Content c:\Determined\settings.py | Select-String "DEBUG"
   # Must show: DEBUG = True ✓
   
   # Verify return to BEFORE state
   ```
   - **Result**: REVERSIBLE ✓ - Perfectly reversible

8. **Document in Ledger**
   - Action: Completed ✓
   - Before state: DEBUG = True (captured)
   - After state: DEBUG = False (verified)
   - Undo capability: git revert (tested ✓)
   - Verified: All unit tests pass ✓

---

### Example 3: Database Operation

**Action**: Insert 100 new records into election ledger

**BEFORE Planning Phase:**

1. **Define Success Criteria (Verification Plan)**
   - 100 records inserted
   - Row count increased by 100
   - No duplicate IDs
   - All required fields populated
   - Query returns correct data

2. **Define Undo Mechanism (Undo Plan)**
   - Mechanism: Database transaction rollback
   - Start transaction: `BEGIN TRANSACTION`
   - Undo command: `ROLLBACK` (if within transaction) OR restore from backup snapshot
   - Undo verification: Row count returns to original

3. **Test Undo Mechanism BEFORE Inserting Real Data**
   ```sql
   -- Test transaction
   BEGIN TRANSACTION;
   INSERT INTO test_ledger VALUES (1, 'test', ...);
   SELECT COUNT(*) FROM test_ledger;  -- Should show +1 row
   ROLLBACK;
   SELECT COUNT(*) FROM test_ledger;  -- Should show original count
   -- Undo mechanism verified ✓
   ```

4. **Record BEFORE State**
   ```sql
   SELECT COUNT(*) FROM election_ledger;  -- Current: 150 rows
   SELECT MAX(id) FROM election_ledger;   -- Current: ID 150
   ```

**Execution Phase:**

5. **Execute the Action (within transaction)**
   ```sql
   BEGIN TRANSACTION;
   INSERT INTO election_ledger (id, title, ...) VALUES (151, 'Decision 1', ...), ... (250, 'Decision 100', ...);
   ```

6. **Verify (MANDATORY - while still in transaction)**
   ```sql
   SELECT COUNT(*) FROM election_ledger WHERE id >= 151;
   -- Must show: 100 ✓
   
   SELECT COUNT(*) FROM election_ledger;
   -- Must show: 250 ✓
   
   SELECT * FROM election_ledger WHERE id = 151;
   -- Must show: first inserted record ✓
   
   SELECT * FROM election_ledger WHERE id = 250;
   -- Must show: last inserted record ✓
   ```
   - **Result**: VERIFIED ✓ - All 100 records inserted correctly

7. **Commit (now that verification passed)**
   ```sql
   COMMIT;
   ```

8. **Test Undo (if needed later)**
   ```sql
   -- Full reversal demonstration
   BEGIN TRANSACTION;
   DELETE FROM election_ledger WHERE id >= 151;
   SELECT COUNT(*) FROM election_ledger;
   -- Should show: 150 (back to BEFORE) ✓
   ROLLBACK;  -- Don't actually delete, just prove we can
   ```

9. **Document in Ledger**
   - Action: Committed ✓
   - Before: 150 records
   - After: 250 records (100 new)
   - Verification: All fields valid ✓
   - Undo: DELETE WHERE id >= 151 (tested ✓)

---

## Blocked Actions (Cannot Execute)

### ❌ Action Without Verification
```
"I'll create a new feature and we can test it later"
BLOCKED: Cannot execute without verification plan
Must have: How will we TEST it? When? What metrics?
```

### ❌ Action Without Undo Planning
```
"I'll modify the production database"
BLOCKED: Cannot execute without undo plan
Must have: How will we REVERSE this? What's the rollback procedure?
```

### ❌ Action With Untested Undo
```
"I've planned to restore from backup if something goes wrong"
BLOCKED: Undo plan not tested
Must have: Actually test the restore procedure BEFORE making changes
```

### ❌ Action Without Verification Execution
```
"I created the file, but I didn't check if it worked"
BLOCKED: Action incomplete
Must have: Run verification checks. Did it actually work?
```

---

## Decision Ledger Entry Template

Every action must create a ledger entry following this structure:

```markdown
## Action: [Brief Title]
**Date**: [Date]
**Status**: VERIFIED ✓ / FAILED ✗

### BEFORE State
- Condition: [measurable state before action]
- Count: [quantitative measure]
- State: [exact snapshot]

### Action Taken
- Command: [exact command executed]
- Time: [when executed]
- Parameters: [what changed]

### Verification Results
- Criterion 1: ✓ PASS [evidence]
- Criterion 2: ✓ PASS [evidence]
- Criterion 3: ✓ PASS [evidence]

### Undo Capability
- Mechanism: [how to reverse]
- Tested: ✓ YES / ✗ NO [when tested]
- Rollback time: [how long to undo]

### AFTER State
- Condition: [measurable state after action]
- Count: [quantitative measure]
- State: [exact snapshot]

### Undo Reverification (if executed)
- Before Undo: [state at reversal]
- After Undo: [state after reversal]
- Back to BEFORE: ✓ YES / ✗ NO
```

---

## Why This Matters

**Without verification**: You don't know if action actually worked  
**Without undo planning**: You're trapped if something goes wrong  
**Without testing undo**: You can't trust it will work when needed  
**Without all three**: You're operating blind and unable to recover

This protocol ensures:
1. ✓ Actions actually succeed (verification)
2. ✓ Failures can be recovered from (undo capability)
3. ✓ Recovery mechanism is proven to work (tested undo)
4. ✓ Complete transparency of what happened (documentation)

---

## Updated Framework

**The One Rule:**
> Whatever you do: Document it. **Verify it. Make it undoable.**

**The Decision Method:**
1. Plan verification (what success looks like)
2. Plan undo (how to reverse)
3. Test undo mechanism
4. Execute action
5. **Verify execution**
6. **Test undo reverification**
7. Document result

This is universal. This applies to every action, without exception.

---

## Status

**Implemented**: April 3, 2026  
**Requirement Level**: MANDATORY  
**Applies To**: Every action, without exception  
**Enforcement**: Actions without verification & tested undo are blocked
