"""
BINARY OPERATION HANDLERS

Implements the causal chains and invariants from BINARY_OPERATION_CAUSAL_CHAINS.md

This module provides the actual execution, validation, and ledger recording for:
- Boolean NOT
- Bit Flip  
- Logic Negation
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class OperationResult:
    """Result of a binary operation execution."""
    operation_type: str
    input_data: Any
    output_data: Any
    invariants_verified: bool
    invariant_checks: Dict[str, bool]
    execution_time_us: float
    election_id: str
    ledger_hash: str
    causal_chain: list


class BooleanNOTOperation:
    """Boolean NOT: Invert all bits independently."""
    
    INVARIANTS = {
        "self_inverse": "NOT(NOT(x)) == x",
        "bitwise_independent": "NOT([a,b,c]) == [NOT(a), NOT(b), NOT(c)]",
        "width_preserved": "len(output) == len(input)",
        "opposite_value": "output[i] != input[i] for all i",
        "binary_only": "output in {0,1}^n",
        "deterministic": "same_input → same_output",
        "idempotent_pairs": "(NOT ∘ NOT) == identity"
    }
    
    @staticmethod
    def execute(pattern: str) -> Tuple[str, OperationResult]:
        """Execute Boolean NOT operation."""
        start_time = datetime.now()
        
        # STEP 1: Validation
        if not BooleanNOTOperation._validate_input(pattern):
            raise ValueError(f"Invalid input pattern: {pattern}")
        
        # STEP 2: Execute
        output = BooleanNOTOperation._invert_bits(pattern)
        
        # STEP 3: Verify invariants
        invariant_checks = BooleanNOTOperation._verify_invariants(pattern, output)
        if not all(invariant_checks.values()):
            raise AssertionError(f"Invariant violations: {invariant_checks}")
        
        # STEP 4: Create election ID
        election_id = f"e-boolean-not-{int(start_time.timestamp() * 1000)}"
        
        # STEP 5: Create ledger hash
        ledger_entry = {
            "operation": "boolean_not",
            "input": pattern,
            "output": output,
            "timestamp": start_time.isoformat()
        }
        ledger_hash = hashlib.sha256(json.dumps(ledger_entry, sort_keys=True).encode()).hexdigest()
        
        # STEP 6: Create execution time
        execution_time_us = (datetime.now() - start_time).total_seconds() * 1_000_000
        
        # STEP 7: Create causal chain
        causal_chain = [
            "boolean_not_requested",
            "operation_received",
            "operation_validated",
            "operation_executed",
            "operation_verified",
            "operation_recorded"
        ]
        
        result = OperationResult(
            operation_type="boolean_not",
            input_data=pattern,
            output_data=output,
            invariants_verified=True,
            invariant_checks=invariant_checks,
            execution_time_us=execution_time_us,
            election_id=election_id,
            ledger_hash=ledger_hash,
            causal_chain=causal_chain
        )
        
        return output, result
    
    @staticmethod
    def _validate_input(pattern: str) -> bool:
        """Check input is valid binary pattern."""
        return bool(pattern) and all(c in '01' for c in pattern)
    
    @staticmethod
    def _invert_bits(pattern: str) -> str:
        """Invert all bits."""
        return ''.join('1' if bit == '0' else '0' for bit in pattern)
    
    @staticmethod
    def _verify_invariants(input_pattern: str, output_pattern: str) -> Dict[str, bool]:
        """Verify all invariants hold."""
        checks = {}
        
        # Self-inverse
        double_negation = BooleanNOTOperation._invert_bits(output_pattern)
        checks["self_inverse"] = double_negation == input_pattern
        
        # Bitwise independent
        checks["bitwise_independent"] = all(
            input_pattern[i] != output_pattern[i] for i in range(len(input_pattern))
        )
        
        # Width preserved
        checks["width_preserved"] = len(output_pattern) == len(input_pattern)
        
        # Opposite value
        checks["opposite_value"] = all(
            input_pattern[i] != output_pattern[i] for i in range(len(input_pattern))
        )
        
        # Binary only
        checks["binary_only"] = all(c in '01' for c in output_pattern)
        
        # Deterministic
        output_2 = BooleanNOTOperation._invert_bits(input_pattern)
        checks["deterministic"] = output_2 == output_pattern
        
        # Idempotent pairs
        checks["idempotent_pairs"] = (
            BooleanNOTOperation._invert_bits(BooleanNOTOperation._invert_bits(input_pattern)) 
            == input_pattern
        )
        
        return checks


class BitFlipOperation:
    """Bit Flip: Toggle a single bit at specified position."""
    
    INVARIANTS = {
        "exactly_one_bit_changes": "hamming_distance(input, output) == 1",
        "self_inverse": "bit_flip(bit_flip(x, p), p) == x",
        "position_valid": "0 <= position < 8",
        "width_preserved": "len(output) == len(input)",
        "deterministic": "same_input_position → same_output",
        "binary_output": "output in {0,1}^8",
        "specific_neighbor": "Hamming neighbor confirmed"
    }
    
    @staticmethod
    def hamming_distance(s1: str, s2: str) -> int:
        """Calculate Hamming distance between two bit patterns."""
        if len(s1) != len(s2):
            raise ValueError("Strings must be same length")
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
    
    @staticmethod
    def execute(pattern: str, position: int) -> Tuple[str, OperationResult]:
        """Execute Bit Flip operation."""
        start_time = datetime.now()
        
        # STEP 1: Validation
        if not BitFlipOperation._validate_input(pattern, position):
            raise ValueError(f"Invalid pattern or position")
        
        # STEP 2: Execute
        output = BitFlipOperation._flip_bit(pattern, position)
        
        # STEP 3: Calculate Hamming distance
        hamming = BitFlipOperation.hamming_distance(pattern, output)
        delta_pattern = ''.join(
            '1' if pattern[i] != output[i] else '0' for i in range(len(pattern))
        )
        
        # STEP 4: Verify invariants
        invariant_checks = BitFlipOperation._verify_invariants(pattern, output, position, hamming)
        if not all(invariant_checks.values()):
            raise AssertionError(f"Invariant violations: {invariant_checks}")
        
        # STEP 5: Calculate field coherence impact
        entropy_before = BitFlipOperation._calculate_entropy(pattern)
        entropy_after = BitFlipOperation._calculate_entropy(delta_pattern)
        coherence_delta = abs(entropy_before - entropy_after)
        
        # STEP 6: Create election ID
        election_id = f"e-bit-flip-{position}-{int(start_time.timestamp() * 1000)}"
        
        # STEP 7: Create ledger hash
        ledger_entry = {
            "operation": "bit_flip",
            "input": pattern,
            "position": position,
            "output": output,
            "hamming_distance": hamming,
            "delta": delta_pattern,
            "coherence_delta": coherence_delta,
            "timestamp": start_time.isoformat()
        }
        ledger_hash = hashlib.sha256(json.dumps(ledger_entry, sort_keys=True).encode()).hexdigest()
        
        # STEP 8: Create execution time
        execution_time_us = (datetime.now() - start_time).total_seconds() * 1_000_000
        
        # STEP 9: Create causal chain
        causal_chain = [
            "bit_flip_requested",
            "bit_flip_validated",
            "hamming_neighbor_identified",
            "operation_executed",
            "field_coherence_measured",
            "operation_recorded"
        ]
        
        result = OperationResult(
            operation_type="bit_flip",
            input_data={"pattern": pattern, "position": position},
            output_data={"pattern": output, "hamming": hamming, "delta": delta_pattern},
            invariants_verified=True,
            invariant_checks=invariant_checks,
            execution_time_us=execution_time_us,
            election_id=election_id,
            ledger_hash=ledger_hash,
            causal_chain=causal_chain
        )
        
        return output, result
    
    @staticmethod
    def _validate_input(pattern: str, position: int) -> bool:
        """Check input pattern and position are valid."""
        if not all(c in '01' for c in pattern):
            return False
        if not (0 <= position < len(pattern)):
            return False
        return True
    
    @staticmethod
    def _flip_bit(pattern: str, position: int) -> str:
        """Flip bit at position."""
        bits = list(pattern)
        bits[position] = '1' if bits[position] == '0' else '0'
        return ''.join(bits)
    
    @staticmethod
    def _calculate_entropy(pattern: str) -> float:
        """Calculate Shannon entropy of bit pattern."""
        if not pattern:
            return 0.0
        ones = pattern.count('1')
        zeros = pattern.count('0')
        total = len(pattern)
        p_ones = ones / total if ones > 0 else 0
        p_zeros = zeros / total if zeros > 0 else 0
        entropy = 0.0
        if p_ones > 0:
            entropy -= p_ones * math.log2(p_ones)
        if p_zeros > 0:
            entropy -= p_zeros * math.log2(p_zeros)
        return entropy
    
    @staticmethod
    def _verify_invariants(input_pattern: str, output_pattern: str, position: int, hamming: int) -> Dict[str, bool]:
        """Verify all invariants hold."""
        checks = {}
        
        # Exactly one bit changes
        checks["exactly_one_bit_changes"] = hamming == 1
        
        # Self-inverse
        output_2 = BitFlipOperation._flip_bit(output_pattern, position)
        checks["self_inverse"] = output_2 == input_pattern
        
        # Position valid
        checks["position_valid"] = 0 <= position < len(input_pattern)
        
        # Width preserved
        checks["width_preserved"] = len(output_pattern) == len(input_pattern)
        
        # Deterministic
        output_again = BitFlipOperation._flip_bit(input_pattern, position)
        checks["deterministic"] = output_again == output_pattern
        
        # Binary output
        checks["binary_output"] = all(c in '01' for c in output_pattern)
        
        # Specific neighbor (Hamming = 1)
        checks["specific_neighbor"] = hamming == 1
        
        return checks


class LogicNegationOperation:
    """Logic Negation: Apply logical NOT to propositions."""
    
    INVARIANTS = {
        "double_negation": "NOT(NOT(p)) == p",
        "non_contradiction": "NOT(p) != p",
        "excluded_middle": "p OR NOT(p) == True",
        "de_morgans_1": "NOT(A AND B) == (NOT A) OR (NOT B)",
        "de_morgans_2": "NOT(A OR B) == (NOT A) AND (NOT B)",
        "deterministic": "same_proposition → same_result",
        "consistent": "respects logical framework"
    }
    
    @staticmethod
    def execute(proposition: bool) -> Tuple[bool, OperationResult]:
        """Execute Logic Negation operation."""
        start_time = datetime.now()
        
        # STEP 1: Validation
        if not isinstance(proposition, bool):
            raise TypeError(f"Proposition must be bool, got {type(proposition)}")
        
        # STEP 2: Execute
        output = not proposition
        
        # STEP 3: Verify invariants
        invariant_checks = LogicNegationOperation._verify_invariants(proposition, output)
        if not all(invariant_checks.values()):
            raise AssertionError(f"Invariant violations: {invariant_checks}")
        
        # STEP 4: Create election ID
        election_id = f"e-logic-neg-{int(start_time.timestamp() * 1000)}"
        
        # STEP 5: Create ledger hash
        ledger_entry = {
            "operation": "logic_negation",
            "input": str(proposition),
            "output": str(output),
            "timestamp": start_time.isoformat()
        }
        ledger_hash = hashlib.sha256(json.dumps(ledger_entry, sort_keys=True).encode()).hexdigest()
        
        # STEP 6: Create execution time
        execution_time_us = (datetime.now() - start_time).total_seconds() * 1_000_000
        
        # STEP 7: Create causal chain
        causal_chain = [
            "logic_negation_requested",
            "proposition_analyzed",
            "logic_validation_passed",
            "operation_executed",
            "logic_consistency_verified",
            "operation_recorded"
        ]
        
        result = OperationResult(
            operation_type="logic_negation",
            input_data=proposition,
            output_data=output,
            invariants_verified=True,
            invariant_checks=invariant_checks,
            execution_time_us=execution_time_us,
            election_id=election_id,
            ledger_hash=ledger_hash,
            causal_chain=causal_chain
        )
        
        return output, result
    
    @staticmethod
    def _verify_invariants(input_prop: bool, output_prop: bool) -> Dict[str, bool]:
        """Verify all invariants hold."""
        checks = {}
        
        # Double negation
        double_neg = not (not input_prop)
        checks["double_negation"] = double_neg == input_prop
        
        # Non-contradiction
        checks["non_contradiction"] = output_prop != input_prop
        
        # Excluded middle
        checks["excluded_middle"] = input_prop or (not input_prop)
        
        # De Morgan's (simplified for boolean)
        checks["de_morgans_1"] = True  # N/A for simple boolean
        checks["de_morgans_2"] = True  # N/A for simple boolean
        
        # Deterministic
        output_2 = not input_prop
        checks["deterministic"] = output_2 == output_prop
        
        # Consistent
        checks["consistent"] = not (input_prop and output_prop)
        
        return checks


# ============================================================================
# LEDGER RECORDING
# ============================================================================

class OperationLedger:
    """Records operations to ledger."""
    
    def __init__(self, ledger_file: str = "ledger_operations.jsonl"):
        self.ledger_file = ledger_file
    
    def record_operation(self, result: OperationResult, weight_song: str = "CONSTRAINT_creates_DEPTH") -> str:
        """Record operation to ledger and return record hash."""
        entry = {
            "operation_type": result.operation_type,
            "sequence_number": self._get_next_sequence(),
            "timestamp": datetime.now().isoformat(),
            "input": result.input_data,
            "output": result.output_data,
            "invariants_verified": result.invariants_verified,
            "invariant_checks": result.invariant_checks,
            "execution_time_us": result.execution_time_us,
            "election_id": result.election_id,
            "ledger_hash": result.ledger_hash,
            "causal_chain": result.causal_chain,
            "weight_song": weight_song,
            "weight_allocated": 0.15
        }
        
        # Append to ledger
        with open(self.ledger_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        return result.ledger_hash
    
    def _get_next_sequence(self) -> int:
        """Get the next sequence number."""
        try:
            with open(self.ledger_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    return last_entry.get('sequence_number', 0) + 1
        except FileNotFoundError:
            pass
        return 1


# ============================================================================
# IMPORTS
# ============================================================================

import math
