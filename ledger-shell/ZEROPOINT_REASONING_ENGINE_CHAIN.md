---
name: ZEROPOINT Logic Chain - Deterministic Reasoning Engine
description: Complete formal reasoning chain for the symbolic pattern-based reasoning system
status: SPECIFICATION PHASE (code begins only after all gates pass)
---

# ZEROPOINT: Deterministic Reasoning Engine

## 1. IDENTIFY THE PRIMITIVE

```
What is the irreducible binary choice in this system?

Field:     User input string (in superposition: could mean many things)
Operation: Determine which intent the input represents
Binary:    Intent identified (1) or ambiguous/unknown (0)?
```

**Core Principle**: Convert natural language to deterministic structured intent through pattern matching, not probabilistic LLMs.

---

## 2. APPLY THE THREE OPERATIONS

### FIELD (Current State Before Decision)
```
What exists in superposition?
  - User input (raw text)
  - Possible interpretations (many)
  - System state (current objects, view, etc)
  - Historical patterns (ledger entries)

What is immutable?
  - Everything in ledger is immutable
  - User input cannot change
  - System state is derived from ledger
```

### SELECTION (Binary Choice)
```
The system must decide:
  "Does this input confidently map to an intent?"
  
  YES (confidence ≥ threshold): Execute deterministically
  NO (confidence < threshold): Request clarification
  
The selection is made by:
  1. Pattern matching against known schemas
  2. Calculating confidence score algorithmically
  3. Comparing against decision threshold (e.g., 0.7)
```

### RECORD (What Gets Written Immutably)
```
Ledger entry structure:
{
  "id": entry_number,
  "timestamp": ISO8601,
  "type": "query_reasoning",
  "user_input": "original text",
  "reasoning": {
    "matched_patterns": ["pattern1", "pattern2"],
    "confidence": 0.85,
    "reasoning_steps": ["step1", "step2", "step3"]
  },
  "intent": {
    "action": "create_object|move_object|render_text|set_view",
    "params": {
      "key": "value"
    }
  },
  "execution_result": {
    "status": "success|failure|clarification_needed",
    "output": {}
  },
  "hash": "SHA256(entire_entry)"
}

IMMUTABLE: Once written, entry cannot be modified (only new entries added)
COMPLETE: Every reasoning step is captured
TRACEABLE: Full chain from input → reasoning → intent → execution
```

---

## 3. CHECK ALL FIVE GATES

### Gate 1: ALIGNMENT WITH STRUCTURE ✅
```
Does this follow from the primitive?

PRIMITIVE: Field (input) → Selection (pattern match) → Record (ledger entry)
REASONING ENGINE: 
  1. Read user input (Field)
  2. Match against known patterns (Selection via deterministic algorithm)
  3. Record decision + reasoning + execution (Record)

✓ YES - Perfectly aligned
  - Primitive is field superposition (input could mean many things)
  - Selection is deterministic pattern matching (not probabilistic)
  - Record is immutable ledger entry with full reasoning chain
  
Why this works:
  - No dependency on external LLM
  - No randomness (same input always gives same output)
  - Fully auditable (every reasoning step visible)
```

### Gate 2: ELIMINATES AMBIGUITY ✅
```
Does this reduce confusion or add to it?

Without reasoning engine:
  - User input: "Create something at 100, 200"
  - System: unpredictable behavior (depends on external LLM)
  - Issue: unclear why system chose what it chose

With deterministic reasoning engine:
  - User input: "Create something at 100, 200"
  - Pattern match: "create_object" pattern (verb "create" matches, params extracted)
  - Confidence: 0.92 (clear pattern match, unambiguous parameters)
  - Intent: {action: "create_object", params: {x: 100, y: 200, type: "default"}}
  - Ledger: Full chain recorded (input → patterns → confidence → intent → execution)

✓ YES - Eliminates ambiguity
  - Each reasoning step is explicit
  - Confidence score quantifies certainty
  - Patterns are documented (not hidden in neural weights)
  - User can understand why system chose this intent
  
Why this matters:
  - Transparency enables debugging
  - Patterns can be adjusted iteratively
  - Mismatches are discoverable
```

### Gate 3: REASONING VISIBLE ✅
```
Can every decision be traced?

Trace path for user input "Move the object to the right":

1. INPUT CAPTURE:
   - Raw: "Move the object to the right"
   - Tokenized: ["Move", "the", "object", "to", "the", "right"]
   
2. PATTERN MATCHING:
   - Verb check: "move" matches MOVE_OBJECT pattern ✓
   - Parameter extraction: direction="right" → x_offset=+50
   - Confidence factors:
     - Verb match: +0.7
     - Direction recognized: +0.2
     - Ambiguity penalty (no target object specified): -0.1
     - Final: 0.8
   
3. INTENT CONSTRUCTION:
   - Action: "move_object"
   - Params: {x_offset: 50, y_offset: 0, relative: true}
   
4. LEDGER ENTRY:
   {
     "user_input": "Move the object to the right",
     "reasoning": {
       "matched_patterns": ["move_object_pattern"],
       "confidence": 0.8,
       "reasoning_steps": [
         "verb_match: move→move_object",
         "direction: right→x_offset+50",
         "target: assumed_last_selected"
       ]
     },
     "intent": {...},
     "execution_result": {...}
   }

✓ YES - Every decision is visible
  - Each pattern match is logged
  - Each confidence calculation is shown
  - Each parameter extraction is traced
  - Full chain in immutable ledger
  
How to verify:
  - Read ledger entry and see exact reasoning
  - Replay from entry #0 to verify determinism
  - Adjust patterns and re-run (confidence scores change predictably)
```

### Gate 4: IS IT KIND ✅
```
Does it serve person and system honestly?

Serves the PERSON:
  ✓ Transparent: They can see exactly why system chose this intent
  ✓ Predictable: Same input always produces same output
  ✓ Debuggable: If result is wrong, they can trace the pattern match
  ✓ Controllable: Patterns can be refined without retraining neural net
  ✓ Honest: Says "confidence 0.6" instead of pretending certainty
  
Serves the SYSTEM:
  ✓ Auditable: Full reasoning chain in immutable ledger
  ✓ Reproducible: No randomness (critical for testing/verification)
  ✓ Compositional: Patterns can be mixed, reused, extended
  ✓ Lightweight: No GPU needed, no external API calls
  ✓ Resilient: Works even if internet is down, no dependency on external services
  
Edge cases handled:
  - Ambiguous input → confidence < threshold → clarification request
  - Unknown pattern → confidence 0.0 → clarification request
  - Multiple valid patterns → highest confidence wins (tie-break by specificity)

✓ YES - Serves person and system both honestly
```

### Gate 5: DOES IT SCALE ✅
```
Works at 1 instance? 100? 1000?

Scaling analysis (inputs per second):

1 instance: 
  - Pattern matching: O(n) where n = number of patterns (typically 20-30)
  - Per-query time: ~5ms (very fast)
  - No external dependencies
  - ✓ Works

100 instances (100 queries/sec):
  - Total CPU: ~500ms per second (negligible)
  - Memory: ~10MB for pattern definitions + history
  - Ledger write: 1 entry per query, ~2KB entry → ~200KB/sec (fast)
  - ✓ Works fine

1000 instances (1000 queries/sec):
  - Total CPU: ~5s per second (still fast, single machine)
  - Memory: ~10MB pattern definitions, rest is ledger entries (grow over time)
  - Ledger write: 1000 entries/sec, ~2MB/sec (SSD can handle 100MB+/sec)
  - ✓ Works

10,000 instances:
  - CPU scales linearly, can shard across multiple servers
  - Ledger entries: 10K/sec × 2KB = 20MB/sec (SSD: OK. Archive older entries)
  - Pattern definitions: Same for all instances (shared, immutable)
  - ✓ Works with horizontal scaling

100,000 instances:
  - Classic database scenario: ledger entries → time-series DB (InfluxDB, etc)
  - Pattern definitions: Served once, cached everywhere
  - ✓ Works with enterprise infrastructure

✓ YES - Scales gracefully from 1 to 1M instances
  - Linear scaling (not exponential)
  - No fundamental limits
  - Can add servers to scale horizontally
  - Ledger becomes archival for very high volume
```

---

## Decision: ALL FIVE GATES PASS ✅✅✅✅✅

The specification can proceed to implementation.

---

## 4. LEDGER STRUCTURE SPECIFICATION

### New File: `reasoning_patterns.json`
```json
{
  "version": "1.0",
  "patterns": [
    {
      "id": "create_object_pattern",
      "name": "Create Object",
      "description": "User wants to create a new object",
      "keywords": ["create", "make", "add", "spawn", "new"],
      "parameter_extractors": [
        {
          "param": "x",
          "extraction": "regex|number_after:'at|position'",
          "default": 0
        },
        {
          "param": "y",
          "extraction": "regex|number_after_comma",
          "default": 0
        },
        {
          "param": "type",
          "extraction": "rule|extract_after_keywords:['object','thing','element']",
          "default": "default"
        }
      ],
      "confidence_rules": [
        {
          "rule": "verb_matches_keyword",
          "score": 0.6
        },
        {
          "rule": "parameters_fully_extracted",
          "score": 0.2
        },
        {
          "rule": "type_specified",
          "score": 0.1
        },
        {
          "rule": "ambiguous_target",
          "score": -0.1
        }
      ],
      "threshold": 0.5
    },
    {
      "id": "move_object_pattern",
      "name": "Move Object",
      "keywords": ["move", "shift", "translate", "go", "place"],
      "parameter_extractors": [...],
      "confidence_rules": [...],
      "threshold": 0.5
    },
    {
      "id": "render_text_pattern",
      "name": "Render Text",
      "keywords": ["show", "display", "print", "render", "write", "say"],
      "parameter_extractors": [
        {
          "param": "text",
          "extraction": "rule|extract_everything_after_keyword",
          "default": ""
        }
      ],
      "confidence_rules": [...],
      "threshold": 0.5
    },
    {
      "id": "set_view_pattern",
      "name": "Set View",
      "keywords": ["view", "show", "display", "switch", "change"],
      "parameter_extractors": [
        {
          "param": "view",
          "extraction": "rule|noun_after_keyword",
          "default": "default"
        }
      ],
      "confidence_rules": [...],
      "threshold": 0.5
    }
  ]
}
```

### Extended File: `ledger.json` (existing)
```json
{
  "entries": [
    {
      "id": 0,
      "timestamp": "2026-03-28T10:00:00.000Z",
      "type": "system_boot",
      "reason": null,
      "entry": null
    },
    {
      "id": 1,
      "timestamp": "2026-03-28T10:00:05.123Z",
      "type": "query_reasoning",
      "user_input": "Create an object at 100, 200",
      "reasoning": {
        "matched_patterns": ["create_object_pattern"],
        "pattern_scores": {
          "create_object_pattern": 0.92,
          "render_text_pattern": 0.15,
          "move_object_pattern": 0.05
        },
        "winner": "create_object_pattern",
        "confidence": 0.92,
        "reasoning_steps": [
          "input_tokens: ['Create', 'an', 'object', 'at', '100', ',', '200']",
          "verb_match: 'create' in create_object_pattern.keywords → +0.6",
          "param_x: '100' extracted → +0.2",
          "param_y: '200' extracted → +0.2",
          "type_specified: false → +0.0",
          "final_confidence: 0.92"
        ]
      },
      "intent": {
        "action": "create_object",
        "params": {
          "x": 100,
          "y": 200,
          "type": "default"
        }
      },
      "execution_result": {
        "status": "success",
        "output": {
          "object_id": "obj_1",
          "position": [100, 200],
          "type": "default"
        }
      },
      "action": "create_object",
      "valid": true,
      "hash": "sha256_of_entry"
    }
  ]
}
```

---

## 5. ALGORITHM SPECIFICATION

### Algorithm: Query Reasoning Engine

```
WHEN user submits query:
  INPUT: user_input (string)
  
  STEP 1: Load reasoning patterns
    patterns = load_json("reasoning_patterns.json")
  
  STEP 2: Tokenize and normalize input
    tokens = tokenize(user_input)
    normalized = lowercase(user_input)
  
  STEP 3: Score all patterns
    FOR each pattern in patterns:
      score = 0.0
      
      // Check verb match
      FOR each keyword in pattern.keywords:
        IF keyword in normalized:
          score += 0.6
          break
      
      // Extract parameters
      extracted_params = {}
      FOR each extractor in pattern.parameter_extractors:
        value = extract_parameter(normalized, extractor)
        extracted_params[extractor.param] = value
        
        IF value != default:
          score += 0.2  // Parameter found
      
      // Apply confidence rules
      FOR each rule in pattern.confidence_rules:
        adjustment = evaluate_rule(rule, tokens, extracted_params)
        score += adjustment
      
      pattern.computed_score = clamp(score, 0.0, 1.0)
  
  STEP 4: Select winning pattern
    winner = pattern with highest computed_score
    winning_score = winner.computed_score
    
    IF winning_score < winner.threshold:
      // Ambiguous - request clarification
      RETURN {
        "status": "clarification_needed",
        "message": f"I'm not sure. Did you mean to {winner.name}?",
        "confidence": winning_score
      }
    
    ELSE:
      // Confident - proceed
      RETURN {
        "status": "intent_determined",
        "intent": {
          "action": winner.id,
          "params": winner.extracted_params
        },
        "confidence": winning_score,
        "matched_pattern": winner.id
      }
  
  STEP 5: Record to ledger
    entry = {
      "id": next_entry_id,
      "timestamp": now(),
      "type": "query_reasoning",
      "user_input": user_input,
      "reasoning": {
        "matched_patterns": [p.id for p in patterns],
        "pattern_scores": {p.id: p.computed_score for p in patterns},
        "winner": winner.id,
        "confidence": winning_score,
        "reasoning_steps": [steps from above]
      },
      "intent": result.intent,
      "execution_result": execute(result.intent),
      "hash": sha256(entry_json)
    }
    
    append_to_ledger(entry)
    
  OUTPUT: Result with full reasoning chain recorded
```

---

## 6. VERIFY AGAINST REVERSE CAUSALITY

### Question 1: Is the spec written BEFORE code runs?
```
✓ YES

Specification exists in:
  - reasoning_patterns.json (defines all patterns BEFORE any query)
  - algorithm above (deterministic steps BEFORE execution)
  - LEDGER structure (schema defined BEFORE first entry)

Code is constrained to:
  - Load patterns from JSON
  - Follow algorithm steps in order
  - Append entries to ledger
  
Code cannot:
  - Create new patterns at runtime
  - Change algorithm mid-query
  - Modify historical ledger entries
  
Constraints flow downward: Spec → Code
Data flows upward: Execution → Ledger entries
```

### Question 2: Is component fully specifiable?
```
✓ YES

Can specify:
  - All pattern definitions (complete list)
  - All parameter extraction rules (deterministic)
  - All confidence calculations (formula-based)
  - All ledger fields (schema defined)
  - All error handling (clarifcation responses)
  
Cannot leave undefined:
  - Pattern matching behavior (must be explicit)
  - Parameter extraction (must have rules)
  - Confidence scoring (must have formula)
  
Result: Component is fully specifiable before coding
```

### Question 3: Are all dependencies pre-declared?
```
✓ YES

Dependencies:
  - Input: user_input (string) - provided by caller
  - Patterns: reasoning_patterns.json - loaded from disk
  - Ledger: ledger.json - exists before first query
  - System state: computed_state_from_ledger() - derived on demand
  
None are runtime-generated:
  - Patterns cannot be created by user input
  - Ledger entries follow schema
  - System state is deterministic replay of ledger
  
All dependencies pre-declared and static
```

---

## 7. REQUIRED LEDGER FILES

### New Files Required:
```
1. reasoning_patterns.json
   - Purpose: Define all pattern matching rules
   - Structure: JSON with patterns array
   - Initialize: Once, when system starts
   - Modify: Manually only (to improve patterns)
   - Status: Read-only at runtime
```

### Modified Files Required:
```
1. ledger.json
   - Add new entry type: "query_reasoning"
   - Schema includes: reasoning chain, intent, execution result
   - Immutable: No modifications to past entries
   - Write-only: Append new entries as queries come in
```

### Files NOT Required:
```
- No external LLM configuration
- No model weights or neural net files
- No random seed management
- No clustering indices
```

---

## 8. IMPLEMENTATION CHECKLIST

Code phase begins only after all gates pass. Gates: **ALL PASS ✅✅✅✅✅**

Implementation tasks (in order):

- [ ] Implement `load_patterns()` function
- [ ] Implement `tokenize()` function
- [ ] Implement `extract_parameter()` function
- [ ] Implement `evaluate_rule()` function
- [ ] Implement `reasoning_engine(user_input)` function
- [ ] Implement `/api/query` endpoint
- [ ] Implement structured ledger entry creation
- [ ] Test determinism (same input → same output)
- [ ] Test all five patterns with real inputs
- [ ] Verify ledger entries contain full reasoning chain
- [ ] Add frontend UI to submit queries
- [ ] Add frontend UI to display reasoning chain

---

## 9. VERIFICATION TESTS

Once implemented, verify:

```
TEST 1 - Determinism:
  Input: "Create an object at 100, 200"
  Run 1: Intent = create_object, Confidence = 0.92
  Run 2: Intent = create_object, Confidence = 0.92
  Run 3: Intent = create_object, Confidence = 0.92
  ✓ Pass if all three match exactly

TEST 2 - All Reasoning Visible:
  Query ledger entry
  Assert: reasoning_steps has 5+ steps
  Assert: pattern_scores shows all patterns evaluated
  Assert: hash is consistent
  ✓ Pass if all assertions true

TEST 3 - Scaling (1000 queries):
  Submit 1000 diverse queries
  Assert: All complete in < 5 seconds
  Assert: All have unique hashes
  Assert: All stored in ledger
  ✓ Pass if all assertions true

TEST 4 - Clarification for Ambiguous:
  Input: "Do the thing"
  Assert: Status = "clarification_needed"
  Assert: Confidence < 0.5
  ✓ Pass if both true
  
TEST 5 - Ledger Immutability:
  Write entry #5
  Re-read entry #5
  Assert: Identical in all fields
  ✓ Pass if assertion true
```

---

## STATUS

✅ ZEROPOINT SPECIFICATION PHASE COMPLETE

All five gates pass. Architecture is fully specified. Ready for implementation phase.

κ⊕ Determined. Reproducible. Auditable. No external dependencies.
