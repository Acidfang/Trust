---
layout: default
title: 0-Error Compute - Duplicate Detector
permalink: /zero-error/detector/
toc: true
category: 0-Error Computing
tier: Tool
difficulty: Intermediate
reading_time: 10
entry_point: Tool users
status: published
---

# Duplicate Detector: Find and Eliminate Code Redundancy

## What This Is

A tool that automatically finds duplicate code, repeated functions, redundant imports, and other forms of code duplication.

## Why It Matters

Code duplication:
- **Increases bugs** — Fix bug in one place, not the other
- **Increases maintenance** — Change logic, need to change multiple places
- **Hides intent** — Similar code might have different purposes
- **Wastes space** — Literal code size increases
- **Confuses developers** — Which version is the "real" one?

## What It Detects

### Type 1: Duplicate Functions
```python
def calculate_state_A():
    states = []
    for item in input:
        states.append(item.state)
    return states

def calculate_state_B():  # DUPLICATE!
    states = []
    for item in input:
        states.append(item.state)
    return states
```

**Fix**: Merge into single function, call from both places

### Type 2: Duplicate Logic Blocks
```python
if state == 0:
    x = value * 2
    y = value + 1
    result = x + y
    
if state == 1:
    x = value * 2
    y = value + 1      # DUPLICATE LOGIC!
    result = x + y
```

**Fix**: Extract to shared function

### Type 3: Duplicate Imports
```python
from utils import helper
...
from utils import helper  # DUPLICATE IMPORT!
```

**Fix**: Single import, use throughout

### Type 4: Duplicate YAML Keys
```yaml
config:
  database:
    host: localhost
  database:           # DUPLICATE KEY!
    port: 5432
```

**Fix**: Merge into single database section

### Type 5: Similar Constants
```python
MAX_RETRIES = 3
MAX_ATTEMPTS = 3      # DUPLICATE VALUE!
```

**Fix**: Define once, reference both places

## How to Use

### Run Detection
```bash
python duplicate_detector.py
```

### Get Report
Output shows:
- Exact duplicates (100% match)
- Similar blocks (90%+ match)
- Duplicate imports
- YAML key conflicts
- Constant duplication

### Review Results
Each duplicate shows:
- Files where it occurs
- Lines of code
- Similarity percentage
- Suggested fix

### Apply Fix
For each duplicate:
1. Decide which version is correct
2. Merge or deduplicate
3. Remove redundant copies
4. Test that it works
5. Run detector again

## Example Report

```
DUPLICATE DETECTOR REPORT
Generated: 2026-04-19

========================================
EXACT DUPLICATES (100% match)
========================================

[DUP-001] Function: validate_state
  File: validators.py (lines 10-25)
  File: checker.py (lines 45-60)
  Type: Exact function duplicate
  Fix: Merge into one, reference from both

[DUP-002] Import statement
  File: main.py (line 1)
  File: main.py (line 5)
  Type: Duplicate import (same file)
  Fix: Remove line 5

========================================
SIMILAR BLOCKS (85-99% match)
========================================

[SIM-001] Logic block: state update
  File: manager.py (lines 30-40)
  File: service.py (lines 55-65)
  Similarity: 92%
  Difference: Variable names slightly different
  Fix: Check if should be exactly identical

========================================
SUMMARY
========================================
- Exact duplicates: 2
- Similar duplicates: 4
- Total redundancy: ~150 lines of code
Recommendation: Fix 2-3 highest-impact duplicates first
```

## Workflow

1. **Run detector** → Get full report
2. **Identify high-impact** → Start with most expensive duplicates
3. **Fix critical duplicates** → Those affecting multiple modules
4. **Re-test** → Verify fixes work correctly
5. **Run detector again** → Verify no new duplicates introduced
6. **Document fix** → Log why duplicate existed and how fixed

## Prevention

To avoid duplicates:

- **Extract functions** — Common code goes to single function
- **Use imports** — Don't copy-paste, import instead
- **Single definition** — Define constants once
- **Code review** — Spot duplicates in PR review
- **Regular detection** — Run detector often

---

**Complete 0-Error Compute:** [Introduction](/Trust/zero-error/intro/)

