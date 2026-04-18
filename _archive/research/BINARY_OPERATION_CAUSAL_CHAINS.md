# BINARY OPERATION CAUSAL CHAINS
**Derived from button labels + framework constraints**  
**Date**: April 4, 2026

---

## PRINCIPLE: Labels Determine Semantics

Each button label specifies:
- **What operation** (the verb: flip, negate, toggle)
- **At what level** (boolean vs bit vs logic)
- **What invariants must hold** (reversibility, idempotence, etc.)

---

## OPERATION 1: Boolean NOT

### Label Semantics
- **Boolean** = operates on truth values (True/False, 1/0)
- **NOT** = logical negation operator
- **Context** = Bit Level 1 (single bits)

### The Operation
```
Input:  Boolean value (True or False, represented as 1 or 0)
Action: Invert the truth value
Output: Opposite of input
```

### Formal Definition
```
boolean_not(x: bool) -> bool
  if x == True:
    return False
  else:
    return True
```

Or in bits:
```
boolean_not(bit: 0|1) -> 0|1
  return 1 - bit  # XOR with 1
```

### Causal Chain (Forward)

**User clicks "Boolean NOT" button:**
```
1. INTENT
   └─ User selects a bit pattern (e.g., 10110101)
   └─ User clicks "Boolean NOT"
   └─ Election: "boolean_not_requested"

2. OPERATION DISPATCH
   └─ System receives: operation="boolean_not", input="10110101"
   └─ Election: "operation_received"

3. VALIDATION
   └─ Check: Is input a valid bit pattern? YES
   └─ Check: Can operation be reversed? YES (NOT is self-inverse)
   └─ Election: "operation_validated"

4. EXECUTION
   └─ Apply: NOT each bit independently
   └─ Result: 01001010 (all bits flipped)
   └─ Election: "operation_executed"

5. VERIFICATION
   └─ Check: Result is opposite of input? YES
   └─ Check: NOT(NOT(input)) == input? YES
   └─ Check: Same bit width? YES
   └─ Election: "operation_verified"

6. RECORDING
   └─ Create ledger entry:
       {
         "operation": "boolean_not",
         "input": "10110101",
         "output": "01001010",
         "timestamp": "2026-04-04T12:34:56Z",
         "weight_used": 0.15,
         "song_type": "CONSTRAINT_creates_DEPTH"
       }
   └─ Election: "operation_recorded"

7. DISPLAY
   └─ Show: "Starting pattern: 10110101"
   └─ Show: "Operation: Boolean NOT (invert all bits)"
   └─ Show: "Result: 01001010"
   └─ Election: "operation_displayed"
```

### Causal Chain (Reverse - Undo)
```
User wants to reverse "Boolean NOT":
  └─ Query ledger for last operation
  └─ Find: "boolean_not" with input=10110101, output=01001010
  └─ Apply: boolean_not(01001010) = 10110101
  └─ Restore: Original state recovered
  └─ Verify: Matches ledger record
  └─ Election: "undo_verified"
```

### Invariants (Must Always Be True)

| Invariant | Formula | Why |
|-----------|---------|-----|
| **Self-Inverse** | NOT(NOT(x)) = x | Must be reversible |
| **Bitwise Independent** | NOT([a,b,c]) = [NOT(a), NOT(b), NOT(c)] | Each bit independent |
| **Width Preserved** | len(output) = len(input) | No data loss |
| **Opposite Value** | output[i] ≠ input[i] for all i | Definition of NOT |
| **Binary Only** | output ∈ {0,1}^n | Result must be binary |
| **Deterministic** | same_input → same_output | Always |
| **Idempotent Pairs** | (NOT ∘ NOT) = identity | Double negation law |

### Ledger Integration

**Ledger Entry Format:**
```json
{
  "operation_type": "boolean_not",
  "sequence_number": 42,
  "timestamp": "2026-04-04T12:34:56.789Z",
  "input": {
    "bit_pattern": "10110101",
    "bit_level": 1,
    "width": 8
  },
  "processing": {
    "algorithm": "bitwise_xor_with_all_ones",
    "cpu_cycles": 8,
    "execution_time_us": 0.023
  },
  "output": {
    "bit_pattern": "01001010",
    "width": 8
  },
  "verification": {
    "is_opposite": true,
    "double_negation_check": true,
    "hash_input": "a1b2c3d4",
    "hash_output": "e5f6g7h8"
  },
  "weight_tracking": {
    "song_used": "CONSTRAINT_creates_DEPTH",
    "weight_allocated": 0.15,
    "weight_remaining": 0.85
  },
  "election": {
    "id": "e-2026-04-04-12-34-56-001",
    "causality_chain": [
      "boolean_not_requested",
      "operation_received",
      "operation_validated",
      "operation_executed",
      "operation_verified",
      "operation_recorded"
    ]
  }
}
```

### Election Sequence
```
1. boolean_not_requested
   ├─ When: User clicks button
   └─ Data: {button: "Boolean NOT", timestamp}

2. operation_received
   ├─ When: System accepts request
   └─ Data: {operation: "boolean_not", input: "10110101"}

3. operation_validated
   ├─ When: Input passes all checks
   └─ Data: {is_valid: true, checks_passed: ["format", "width", "reversible"]}

4. operation_executed
   ├─ When: Computation completes
   └─ Data: {output: "01001010", execution_time_us: 0.023}

5. operation_verified
   ├─ When: Output verified against invariants
   └─ Data: {invariants_checked: 7, invariants_passed: 7}

6. operation_recorded
   ├─ When: Ledger entry committed
   └─ Data: {ledger_hash: "[SHA256]", sequence: 42}

7. operation_displayed
   ├─ When: UI shows result
   └─ Data: {display_format: "markdown", output_rendered: true}
```

---

## OPERATION 2: Bit Flip

### Label Semantics
- **Bit** = operates on individual bits (storage level)
- **Flip** = toggle a single bit at specific position
- **Context** = Hamming distance 1 operation

### The Operation
```
Input:  Bit pattern + Position (0-7)
Action: Toggle the bit at that position
Output: Pattern with one bit inverted
```

### Formal Definition
```
bit_flip(pattern: str, position: int) -> str
  if not (0 <= position < len(pattern)):
    raise ValueError("Position out of range")
  
  bits = list(pattern)
  bits[position] = '1' if bits[position] == '0' else '0'
  return ''.join(bits)

# Example:
bit_flip("10110101", 3) = "10110001"  # Flipped position 3
```

### Causal Chain (Forward)

**User clicks "Bit Flip" button and selects position:**
```
1. INTENT + POSITION
   └─ User selects: pattern and position (0-7)
   └─ User clicks "Bit Flip"
   └─ Election: "bit_flip_requested"

2. VALIDATION
   └─ Check: Is position in range [0, 7]? YES
   └─ Check: Is pattern valid binary? YES
   └─ Check: Can operation be reversed? YES (same operation)
   └─ Election: "bit_flip_validated"

3. NEIGHBOR ANALYSIS (Hamming)
   └─ Current pattern: "10110101"
   └─ Position 3 neighbors (Hamming distance 1):
       - "10110001" ← after flip
   └─ This is THE neighbor at distance 1
   └─ Election: "hamming_neighbor_identified"

4. EXECUTION
   └─ Apply: bits[3] = 1 - bits[3]
   └─ Result: "10110001" (one bit changed)
   └─ Verify: hamming_distance(input, output) = 1
   └─ Election: "operation_executed"

5. FIELD COHERENCE IMPACT
   └─ Calculate: entropy before = H(x)
   └─ Calculate: entropy after = H(x XOR delta)
   └─ Calculate: new coherence = 1 - H(delta) / H_max
   └─ Record: coherence_score for this single-bit change
   └─ Election: "field_coherence_measured"

6. RECORDING
   └─ Create ledger entry:
       {
         "operation": "bit_flip",
         "input": "10110101",
         "position": 3,
         "output": "10110001",
         "hamming_distance": 1,
         "delta": "00000100",
         "coherence_delta": 0.044,
         "timestamp": "2026-04-04T12:34:57Z",
         "song_type": "ENGAGEMENT_vs_DENIAL"
       }
   └─ Election: "operation_recorded"

7. DISPLAY
   └─ Show: "Starting: 10110101"
   └─ Show: "Flipped bit at position: 3"
   └─ Show: "Result: 10110001"
   └─ Show: "Hamming distance: 1"
   └─ Show: "Field coherence changed by: 0.044"
   └─ Election: "operation_displayed"
```

### Causal Chain (Reverse - Undo)
```
User wants to reverse "Bit Flip":
  └─ Query ledger for last bit_flip operation
  └─ Find: position=3, input="10110101", output="10110001"
  └─ Apply: bit_flip("10110001", 3) = "10110101"
  └─ Verify: Hamming distance still 1
  └─ Verify: Result matches original input
  └─ Restore: Original state recovered
  └─ Election: "undo_verified"
```

### Invariants (Must Always Be True)

| Invariant | Formula | Why |
|-----------|---------|-----|
| **Exactly One Bit Changes** | hamming_distance(input, output) = 1 | Definition of flip |
| **Self-Inverse** | bit_flip(bit_flip(x, p), p) = x | Must be reversible |
| **Position Valid** | 0 ≤ position < 8 | 8-bit patterns |
| **Width Preserved** | len(output) = len(input) | No data loss |
| **Deterministic** | same_input_position → same_output | Always |
| **Binary Output** | output ∈ {0,1}^8 | Result must be binary |
| **Specific Neighbor** | Hamming neighbor confirmed | Known neighbor relationship |

### Ledger Integration

**Ledger Entry Format:**
```json
{
  "operation_type": "bit_flip",
  "sequence_number": 43,
  "timestamp": "2026-04-04T12:34:57.234Z",
  "input": {
    "bit_pattern": "10110101",
    "bit_level": 1,
    "width": 8
  },
  "parameters": {
    "position_flipped": 3,
    "position_valid": true
  },
  "processing": {
    "algorithm": "single_bit_toggle",
    "cpu_cycles": 4,
    "execution_time_us": 0.012
  },
  "output": {
    "bit_pattern": "10110001",
    "width": 8
  },
  "hamming_analysis": {
    "hamming_distance": 1,
    "delta_pattern": "00000100",
    "neighbor_confirmed": true
  },
  "field_coherence": {
    "entropy_before": 0.954,
    "entropy_after": 0.998,
    "delta_entropy": 0.044,
    "coherence_before": 0.046,
    "coherence_after": 0.002,
    "effect": "reduced_coherence"
  },
  "verification": {
    "hamming_distance_check": true,
    "self_inverse_check": true,
    "width_preserved": true
  },
  "weight_tracking": {
    "song_used": "ENGAGEMENT_vs_DENIAL",
    "weight_allocated": 0.15,
    "weight_remaining": 0.85
  },
  "election": {
    "id": "e-2026-04-04-12-34-57-001",
    "causality_chain": [
      "bit_flip_requested",
      "bit_flip_validated",
      "hamming_neighbor_identified",
      "operation_executed",
      "field_coherence_measured",
      "operation_recorded"
    ]
  }
}
```

### Election Sequence
```
1. bit_flip_requested
   ├─ When: User clicks button + selects position
   └─ Data: {button: "Bit Flip", position: 3, timestamp}

2. bit_flip_validated
   ├─ When: Position and pattern pass checks
   └─ Data: {position_valid: true, pattern_valid: true}

3. hamming_neighbor_identified
   ├─ When: System confirms Hamming distance = 1
   └─ Data: {hamming_distance: 1, neighbor_hash: "[hash]"}

4. operation_executed
   ├─ When: Bit flip computation completes
   └─ Data: {output: "10110001", execution_time_us: 0.012}

5. field_coherence_measured
   ├─ When: Entropy calculated for new state
   └─ Data: {coherence_delta: 0.044, coherence_before: 0.046}

6. operation_recorded
   ├─ When: Ledger entry committed
   └─ Data: {ledger_hash: "[SHA256]", sequence: 43}

7. operation_displayed
   ├─ When: UI shows result with Hamming info
   └─ Data: {display_format: "markdown", hamming_shown: true}
```

---

## OPERATION 3: Logic Negation

### Label Semantics
- **Logic** = operates at decision/proposition level
- **Negation** = propositional negation (NOT logical operator)
- **Context** = Bit Level 1 (applies to boolean propositions)

### The Operation
```
Input:  Logical proposition (True/False or 1/0)
Action: Apply logical NOT
Output: Negated proposition
Difference from Boolean NOT: May apply to compound propositions, not just single bits
```

### Formal Definition
```
logic_negation(proposition: bool) -> bool
  return not proposition

# Example with compound propositions:
# NOT (A AND B) = (NOT A) OR (NOT B)  [De Morgan's law]
# NOT (A OR B) = (NOT A) AND (NOT B)   [De Morgan's law]

# For simple bit:
logic_negation(bit: 0|1) -> 0|1
  return 1 - bit  # Same as Boolean NOT
```

### Causal Chain (Forward)

**User clicks "Logic negation" button:**
```
1. INTENT - PROPOSITION
   └─ User selects: a logical proposition or bit to negate
   └─ User clicks "Logic negation"
   └─ Election: "logic_negation_requested"

2. PROPOSITION ANALYSIS
   └─ Analyze: Is this a compound proposition?
   └─ If compound: Apply De Morgan's laws
   └─ If simple: Treat as bit negation
   └─ Election: "proposition_analyzed"

3. VALIDATION
   └─ Check: Is input a valid proposition? YES
   └─ Check: Is negation reversible? YES (double negation law)
   └─ Check: Satisfies law of non-contradiction? YES
   └─ Election: "logic_validation_passed"

4. EXECUTION
   └─ Apply: NOT (proposition)
   └─ Result: Negated proposition
   └─ Election: "operation_executed"

5. LOGICAL CONSISTENCY CHECK
   └─ Verify: NOT(x) ≠ x (or exactly one is true)
   └─ Verify: NOT(NOT(x)) = x
   └─ Verify: Law of excluded middle: x OR NOT(x) = True always
   └─ Election: "logic_consistency_verified"

6. RECORDING
   └─ Create ledger entry:
       {
         "operation": "logic_negation",
         "input_proposition": "condition_is_true",
         "output_proposition": "condition_is_not_true",
         "logic_laws": [
           "double_negation",
           "law_of_non_contradiction",
           "law_of_excluded_middle"
         ],
         "timestamp": "2026-04-04T12:34:58Z",
         "song_type": "CONSTRAINT_creates_DEPTH"
       }
   └─ Election: "operation_recorded"

7. DECISION IMPACT
   └─ Show: "Original: condition_is_true → TRUE"
   └─ Show: "Negated: condition_is_not_true → FALSE"
   └─ Show: "Reasoning: Applied logical NOT"
   └─ Show: "Impact on decisions: All decisions based on this flip"
   └─ Election: "operation_displayed"
```

### Causal Chain (Reverse - Undo)
```
User wants to reverse "Logic negation":
  └─ Query ledger for last logic_negation operation
  └─ Find: input_proposition="condition_is_true", output_proposition="condition_is_not_true"
  └─ Apply: logic_negation("condition_is_not_true") = "condition_is_true"
  └─ Verify: Logical consistency maintained
  └─ Verify: Original proposition recovered from ledger
  └─ Election: "undo_verified"
```

### Invariants (Must Always Be True)

| Invariant | Formula | Why |
|-----------|---------|-----|
| **Double Negation** | NOT(NOT(p)) = p | Must be reversible |
| **Non-Contradiction** | NOT(p) ≠ p (unless p = undefined) | Can't be true AND false |
| **Excluded Middle** | p OR NOT(p) = True | Must be true or false |
| **De Morgan's Law 1** | NOT(A AND B) = (NOT A) OR (NOT B) | Logical equivalence |
| **De Morgan's Law 2** | NOT(A OR B) = (NOT A) AND (NOT B) | Logical equivalence |
| **Deterministic** | same_proposition → same_result | Always |
| **Consistent** | Negation respects logical framework | Never violates logic |

### Ledger Integration

**Ledger Entry Format:**
```json
{
  "operation_type": "logic_negation",
  "sequence_number": 44,
  "timestamp": "2026-04-04T12:34:58.567Z",
  "input": {
    "proposition": "condition_is_true",
    "truth_value": true,
    "bit_level": 1,
    "is_compound": false
  },
  "processing": {
    "algorithm": "logical_not_operator",
    "de_morgans_applicable": false,
    "cpu_cycles": 2,
    "execution_time_us": 0.008
  },
  "output": {
    "proposition": "condition_is_not_true",
    "truth_value": false,
    "type": "negated_proposition"
  },
  "logical_verification": {
    "double_negation_law": true,
    "non_contradiction_law": true,
    "excluded_middle_law": true,
    "de_morgans_applicable": false,
    "all_laws_satisfied": true
  },
  "decision_impact": {
    "affects_downstream": [
      "conditional_branches",
      "gate_evaluations",
      "rule_applications"
    ],
    "cascading_decisions": "Query ledger for rules using this proposition"
  },
  "weight_tracking": {
    "song_used": "CONSTRAINT_creates_DEPTH",
    "weight_allocated": 0.15,
    "weight_remaining": 0.85
  },
  "election": {
    "id": "e-2026-04-04-12-34-58-001",
    "causality_chain": [
      "logic_negation_requested",
      "proposition_analyzed",
      "logic_validation_passed",
      "operation_executed",
      "logic_consistency_verified",
      "operation_recorded"
    ]
  }
}
```

### Election Sequence
```
1. logic_negation_requested
   ├─ When: User clicks button + selects proposition
   └─ Data: {button: "Logic negation", proposition: "condition_is_true"}

2. proposition_analyzed
   ├─ When: System analyzes proposition structure
   └─ Data: {is_compound: false, applicable_laws: ["double_negation"]}

3. logic_validation_passed
   ├─ When: Proposition passes all logical checks
   └─ Data: {laws_checked: 5, laws_passed: 5}

4. operation_executed
   ├─ When: Negation applied
   └─ Data: {result: false, execution_time_us: 0.008}

5. logic_consistency_verified
   ├─ When: Output verified against logical laws
   └─ Data: {consistency_verified: true, no_contradictions: true}

6. operation_recorded
   ├─ When: Ledger entry committed
   └─ Data: {ledger_hash: "[SHA256]", sequence: 44}

7. operation_displayed
   ├─ When: UI shows result with logical reasoning
   └─ Data: {display_format: "markdown", reasoning_shown: true}
```

---

## COMPARISON MATRIX

| Property | Boolean NOT | Bit Flip | Logic Negation |
|----------|------------|----------|-----------------|
| **Operates On** | All bits independently | Single bit | Propositions |
| **Input** | Bit pattern | Pattern + position | Proposition |
| **Output** | Inverted pattern | Pattern with one bit flipped | Negated proposition |
| **Reversibility** | Self-inverse | Self-inverse | Self-inverse (double negation) |
| **Hamming Distance** | All bits differ | Exactly 1 | N/A (logical operation) |
| **Invariant Count** | 7 | 7 | 7 |
| **Ledger Weight** | 0.15 | 0.15 | 0.15 |
| **Election Type** | logical_transformation | bit_level_mutation | propositional_logic_operation |
| **Can Be Undone** | Yes (reapply) | Yes (reapply) | Yes (reapply) |
| **Respects Laws** | Logic laws | Binary arithmetic | Logical laws |

---

## UNIFIED EXECUTION FRAMEWORK

### Pre-Execution Checklist (All Three Operations)
```
Before executing ANY operation:
  ✓ Is operation type recognized?
  ✓ Is input valid for this operation?
  ✓ Can operation be reversed (undo plan exists)?
  ✓ Will operation respect invariants?
  ✓ Is weight available in current song?
  ✓ Will operation be recorded to ledger?
```

### Execution Sequence (All Three)
```
1. Request received
2. Input validated
3. Reversibility confirmed
4. Operation executed
5. Invariants verified
6. Results recorded to ledger
7. Election sequenced
8. Output displayed
```

### Post-Execution Verification (All Three)
```
✓ Results in ledger
✓ Election recorded
✓ Weight tracking updated
✓ Invariants maintained
✓ Causality chain complete
✓ Can be queried later
✓ Can be reversed if needed
```

---

## BUTTON INTEGRATION SPEC

### HTML Integration
```html
<div class="gate-examples">
  <!-- Level 1: Boolean Operations -->
  <div onclick="encyclopediaApp.executeOperation('boolean_not')" 
       class="operation-button boolean-not">
    Boolean NOT
  </div>
  
  <div onclick="encyclopediaApp.executeOperation('bit_flip')" 
       class="operation-button bit-flip">
    Bit flip
  </div>
  
  <div onclick="encyclopediaApp.executeOperation('logic_negation')" 
       class="operation-button logic-negation">
    Logic negation
  </div>
</div>
```

### JavaScript Integration
```javascript
executeOperation(operationType) {
  switch(operationType) {
    case 'boolean_not':
      return this._execute_boolean_not();
    case 'bit_flip':
      return this._execute_bit_flip();
    case 'logic_negation':
      return this._execute_logic_negation();
    default:
      throw new Error(`Unknown operation: ${operationType}`);
  }
}

_execute_boolean_not() {
  // 1. Get current pattern from UI
  let pattern = this.getCurrentPattern();
  
  // 2. Validate
  if (!this._validate_binary_pattern(pattern)) throw new Error("Invalid pattern");
  
  // 3. Execute
  let result = this._boolean_not(pattern);
  
  // 4. Verify invariants
  if (!this._verify_boolean_not_invariants(pattern, result)) throw new Error("Invariant violated");
  
  // 5. Record to ledger
  this._record_to_ledger('boolean_not', {input: pattern, output: result});
  
  // 6. Display
  this._display_result(result);
}

_execute_bit_flip() {
  // Get position from user
  let position = prompt("Enter position (0-7):");
  if (!Number.isInteger(position) || position < 0 || position > 7) {
    throw new Error("Invalid position");
  }
  
  let pattern = this.getCurrentPattern();
  let result = this._bit_flip(pattern, position);
  
  // Verify Hamming distance = 1
  if (this._hamming_distance(pattern, result) !== 1) {
    throw new Error("Hamming distance violation");
  }
  
  this._record_to_ledger('bit_flip', {input: pattern, output: result, position: position});
  this._display_result(result);
}

_execute_logic_negation() {
  let proposition = this.getCurrentProposition();
  let negated = !proposition;
  
  // Verify logical laws
  if (!(negated !== proposition)) throw new Error("Non-contradiction violated");
  if (!(proposition || negated)) throw new Error("Excluded middle violated");
  
  this._record_to_ledger('logic_negation', {input: proposition, output: negated});
  this._display_result(negated);
}
```

---

## VERIFICATION: Complete Causal Chains ✅

### Boolean NOT
- ✅ Forward causality: Input → Invert all bits → Output
- ✅ Backward causality: Result can be inverted to get original
- ✅ Invariants: 7 specified and verifiable
- ✅ Election: Recorded at each step
- ✅ Ledger: Format specified
- ✅ Undo: Reapply operation

### Bit Flip
- ✅ Forward causality: Pattern + Position → Toggle bit → Output
- ✅ Backward causality: Result at same position returns original
- ✅ Invariants: 7 specified (including Hamming distance = 1)
- ✅ Election: Recorded with neighbor analysis
- ✅ Ledger: Format specifies position + delta + coherence impact
- ✅ Undo: Reapply operation at same position

### Logic Negation
- ✅ Forward causality: Proposition → Apply NOT → Negated proposition
- ✅ Backward causality: Negated can be negated to get original
- ✅ Invariants: 7 specified (logical laws)
- ✅ Election: Recorded with law verification
- ✅ Ledger: Format specifies De Morgan applicability
- ✅ Undo: Reapply operation

---

## SUMMARY

**All three buttons now have:**
1. ✅ Complete causal chains (forward + reverse)
2. ✅ 7 verified invariants each
3. ✅ Ledger integration patterns
4. ✅ Election sequencing
5. ✅ Undo/reversibility specifications
6. ✅ Verification procedures
7. ✅ Implementation guidance

**Derived purely from button labels** via semantic analysis of operation names.
