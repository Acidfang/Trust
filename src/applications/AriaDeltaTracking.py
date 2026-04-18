#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARIA Delta Tracking - High-Resolution State Transition Measurement

Status: Phase B3 Implementation
Date: April 3, 2026
Purpose: Track XOR deltas across state transitions for persistent coherence measurement

Features:
  - Records every state→state XOR delta
  - O(1) entropy lookup using pre-computed tables
  - Tracks coherence boundaries in real-time
  - Integrates with ledger system (persistent storage)
  - Enables pattern analysis across long time horizons

Integration: Feeds into ledger_query.py and AriaMeasurementInterface
"""

import json
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class AriaDeltaTracking:
    """
    Track XOR deltas between consecutive ARIA states.
    
    Enables high-resolution coherence measurement across long periods
    by recording and analyzing state transition patterns.
    """
    
    def __init__(self, state_width_bits: int = 256, precompute_entropy: bool = True):
        """
        Initialize delta tracking system.
        
        Args:
            state_width_bits: Width of state space (default 256 bits)
            precompute_entropy: Pre-compute entropy table for O(1) lookup
        """
        self.state_width_bits = state_width_bits
        self.previous_state = 0
        self.delta_sequence: List[Dict] = []  # Persistent delta history
        
        # Pre-computed entropy table (for fast O(1) lookup)
        self.entropy_table: Dict[int, float] = {}
        if precompute_entropy:
            self._precompute_entropy_table()
        
        # Tracking statistics
        self.statistics = {
            "total_transitions": 0,
            "coherence_boundaries_detected": 0,
            "patterns_discovered": [],
            "min_entropy": 1.0,
            "max_entropy": 0.0,
            "avg_entropy": 0.0
        }
    
    # ========================================================================
    # ENTROPY PRE-COMPUTATION (Performance Optimization)
    # ========================================================================
    
    def _precompute_entropy_table(self):
        """
        Pre-compute Shannon entropy for all possible bit patterns.
        
        Instead of computing entropy for each delta on-the-fly,
        build a lookup table with all 256 possible entropy values.
        
        Enables O(1) entropy lookups during delta recording.
        """
        for value in range(256):  # All possible byte values
            ones = bin(value).count('1')
            zeros = 8 - ones
            
            # Shannon entropy: H = -Σ p_i * log2(p_i)
            entropy = 0.0
            if ones > 0:
                p_one = ones / 8
                entropy -= p_one * math.log2(p_one)
            if zeros > 0:
                p_zero = zeros / 8
                entropy -= p_zero * math.log2(p_zero)
            
            self.entropy_table[value] = entropy
    
    def lookup_entropy(self, delta_value: int, use_table: bool = True) -> float:
        """
        Look up entropy of delta value.
        
        With pre-computed table: O(1) lookup
        Without pre-computed table: O(n) calculation
        
        Args:
            delta_value: The delta (XOR result)
            use_table: If True, use pre-computed table (faster)
        
        Returns:
            Shannon entropy of delta value
        """
        if use_table and self.entropy_table:
            # Fast: O(1) table lookup
            # For multi-byte deltas, average entropy of each byte
            entropy_sum = 0.0
            num_bytes = (self.state_width_bits // 8)
            
            for i in range(num_bytes):
                byte_val = (delta_value >> (i * 8)) & 0xFF
                entropy_sum += self.entropy_table.get(byte_val, 0.5)
            
            return entropy_sum / max(1, num_bytes)
        else:
            # Slow: Calculate on-the-fly
            ones = bin(delta_value).count('1')
            zeros = self.state_width_bits - ones
            
            p_one = ones / self.state_width_bits if ones > 0 else 0
            p_zero = zeros / self.state_width_bits if zeros > 0 else 0
            
            entropy = 0.0
            if p_one > 0:
                entropy -= p_one * math.log2(p_one)
            if p_zero > 0:
                entropy -= p_zero * math.log2(p_zero)
            
            return entropy
    
    # ========================================================================
    # DELTA RECORDING
    # ========================================================================
    
    def record_state_transition(self, new_state: int) -> Dict:
        """
        Record a state transition and analyze its delta.
        
        Args:
            new_state: New state value (after transition)
        
        Returns:
            Dict with delta analysis
        """
        # Compute delta
        delta = self.previous_state ^ new_state
        bits_changed = bin(delta).count('1')
        
        # Look up entropy (O(1) with pre-computed table)
        entropy = self.lookup_entropy(delta, use_table=True)
        
        # Compute coherence: τ = 1 - H(ΔS) / H_max
        max_entropy = 1.0
        coherence = max(0.0, 1.0 - (entropy / max_entropy))
        
        # Record transition
        timestamp = datetime.now().isoformat()
        transition_record = {
            "timestamp": timestamp,
            "sequence_number": self.statistics["total_transitions"],
            "previous_state": self.previous_state,
            "new_state": new_state,
            "delta": delta,
            "bits_changed": bits_changed,
            "entropy": round(entropy, 6),
            "coherence": round(coherence, 6),
            "coherence_class": self._classify_coherence(coherence)
        }
        
        self.delta_sequence.append(transition_record)
        
        # Update statistics
        self._update_statistics(entropy, coherence)
        
        # Update state
        self.previous_state = new_state
        self.statistics["total_transitions"] += 1
        
        return transition_record
    
    def record_state_transitions_batch(self, state_sequence: List[int]) -> List[Dict]:
        """
        Record multiple state transitions in sequence.
        
        Useful for batch processing or replaying history.
        
        Args:
            state_sequence: List of state values in order
        
        Returns:
            List of transition records
        """
        results = []
        for state in state_sequence:
            result = self.record_state_transition(state)
            results.append(result)
        
        return results
    
    def _classify_coherence(self, coherence: float) -> str:
        """Classify coherence level."""
        if coherence > 0.8:
            return "highly_coherent"
        elif coherence > 0.6:
            return "moderately_coherent"
        elif coherence > 0.4:
            return "weakly_coherent"
        else:
            return "incoherent"
    
    def _update_statistics(self, entropy: float, coherence: float):
        """Update running statistics."""
        self.statistics["min_entropy"] = min(self.statistics["min_entropy"], entropy)
        self.statistics["max_entropy"] = max(self.statistics["max_entropy"], entropy)
        
        # Update running average
        total = self.statistics["total_transitions"]
        old_avg = self.statistics["avg_entropy"]
        new_avg = (old_avg * total + entropy) / (total + 1)
        self.statistics["avg_entropy"] = new_avg
    
    # ========================================================================
    # BOUNDARY DETECTION
    # ========================================================================
    
    def detect_coherence_boundaries(self, lookback: int = 50) -> List[Dict]:
        """
        Detect transitions between high and low coherence regions.
        
        A "boundary" is where coherence class changes
        (e.g., highly_coherent → weakly_coherent).
        
        Args:
            lookback: Number of recent transitions to analyze
        
        Returns:
            List of detected boundaries with context
        """
        if len(self.delta_sequence) < 2:
            return []
        
        window_start = max(0, len(self.delta_sequence) - lookback)
        window = self.delta_sequence[window_start:]
        
        boundaries = []
        
        for i in range(1, len(window)):
            prev_class = window[i-1]["coherence_class"]
            curr_class = window[i]["coherence_class"]
            
            if prev_class != curr_class:
                boundary = {
                    "sequence_number": window[i]["sequence_number"],
                    "timestamp": window[i]["timestamp"],
                    "transition": f"{prev_class} → {curr_class}",
                    "previous_coherence": window[i-1]["coherence"],
                    "current_coherence": window[i]["coherence"],
                    "delta_entropy": window[i]["entropy"],
                    "bits_changed": window[i]["bits_changed"]
                }
                boundaries.append(boundary)
        
        self.statistics["coherence_boundaries_detected"] = len(boundaries)
        return boundaries
    
    # ========================================================================
    # PATTERN DISCOVERY
    # ========================================================================
    
    def discover_entropy_patterns(self, window_size: int = 10, 
                                 min_occurrences: int = 3) -> List[Dict]:
        """
        Discover repeating entropy patterns in delta sequences.
        
        Looks for recurring patterns like:
          - Low entropy stretches (coherent periods)
          - High entropy bursts (diffuse periods)
          - Entropy oscillations
        
        Args:
            window_size: Size of pattern window to look for
            min_occurrences: Minimum times pattern must repeat
        
        Returns:
            List of discovered patterns
        """
        if len(self.delta_sequence) < window_size * min_occurrences:
            return []
        
        patterns = defaultdict(int)
        discovered = []
        
        # Extract entropy sequences
        entropy_sequence = [round(d["entropy"], 2) for d in self.delta_sequence]
        
        # Find patterns
        for i in range(len(entropy_sequence) - window_size + 1):
            pattern = tuple(entropy_sequence[i:i + window_size])
            patterns[pattern] += 1
        
        # Filter for repeated patterns
        for pattern, count in patterns.items():
            if count >= min_occurrences:
                avg_entropy = sum(pattern) / len(pattern)
                discovered.append({
                    "pattern": list(pattern),
                    "occurrences": count,
                    "avg_entropy": round(avg_entropy, 3),
                    "interpretation": self._interpret_pattern(pattern),
                    "window_size": window_size
                })
        
        # Sort by frequency
        discovered.sort(key=lambda p: p["occurrences"], reverse=True)
        
        self.statistics["patterns_discovered"] = discovered
        return discovered
    
    def _interpret_pattern(self, pattern: Tuple) -> str:
        """Interpret what a pattern means for field coherence."""
        avg = sum(pattern) / len(pattern)
        values = list(pattern)
        
        if all(v < 0.3 for v in values):
            return "Sustained coherent field (low entropy throughout)"
        elif all(v > 0.6 for v in values):
            return "Sustained diffuse field (high entropy throughout)"
        elif max(values) - min(values) > 0.5:
            return "Oscillating field (entropy varying widely)"
        elif any(v > 0.6 for v in values):
            return "Field with occasional diffusion bursts"
        else:
            return "Field transitioning between states"
    
    # ========================================================================
    # EXPORT & PERSISTENCE
    # ========================================================================
    
    def export_deltas_for_ledger(self) -> Dict:
        """
        Export delta records in format suitable for ledger storage.
        
        Returns ledger-compatible JSON structure.
        """
        return {
            "type": "delta_tracking_export",
            "timestamp": datetime.now().isoformat(),
            "total_transitions": self.statistics["total_transitions"],
            "deltas": self.delta_sequence,
            "statistics": {
                "total": self.statistics["total_transitions"],
                "min_entropy": round(self.statistics["min_entropy"], 6),
                "max_entropy": round(self.statistics["max_entropy"], 6),
                "avg_entropy": round(self.statistics["avg_entropy"], 6),
                "boundaries_detected": self.statistics["coherence_boundaries_detected"]
            }
        }
    
    def import_deltas_from_ledger(self, ledger_data: Dict) -> int:
        """
        Import delta records from ledger data.
        
        Rebuilds internal state from exported ledger.
        
        Args:
            ledger_data: Previously exported delta data
        
        Returns:
            Number of deltas imported
        """
        if "deltas" not in ledger_data:
            return 0
        
        imported_count = 0
        for delta_record in ledger_data["deltas"]:
            self.delta_sequence.append(delta_record)
            imported_count += 1
        
        # Rebuild statistics
        if self.delta_sequence:
            last_record = self.delta_sequence[-1]
            self.previous_state = last_record["new_state"]
            self.statistics["total_transitions"] = len(self.delta_sequence)
        
        return imported_count
    
    def get_statistics(self) -> Dict:
        """Get tracking statistics."""
        return self.statistics.copy()


# ============================================================================
# TESTING & VALIDATION
# ============================================================================

def test_delta_tracking():
    """Test delta tracking system."""
    print("\n📊 ARIA DELTA TRACKING TEST")
    print("=" * 70)
    
    tracker = AriaDeltaTracking(state_width_bits=256)
    
    # Test pattern: coherent period → transition → diffuse period → recovery
    print("\n1. STATE TRANSITION RECORDING:")
    print("   Simulating state sequence with pattern changes...")
    
    state_sequence = [
        0b11110000111100001111000011110000111100001111000011110000111100,  # Coherent pattern
        0b11110000111100001111000011110000111100001111000011110000111101,  # Small change
        0b11110000111100001111000011110000111100001111000011110000111111,  # Slightly larger
        0b11110000111100001111000011110000111100001111000011111111111111,  # Transitioning
        0b10101010101010101010101010101010101010101010101010101010101010,  # Complete change
        0b10101010101010101010101010101010101010101010101010101010101011,  # Diffuse pattern
        0b10101010101010101010101010101010101010101010101010101010101001,  # Random changes
        0b11110000111100001111000011110000111100001111000011110000111100,  # Back to coherent
    ]
    
    results = tracker.record_state_transitions_batch(state_sequence)
    
    print(f"\n   Recorded {len(results)} transitions")
    print("\n   Seq | Bits| Entropy | τ      | Class")
    print("   " + "-" * 45)
    for r in results:
        print(f"   {r['sequence_number']:2d}  | {r['bits_changed']:3d}  | "
              f"{r['entropy']:.3f}   | {r['coherence']:.2f}  | {r['coherence_class'][:10]}")
    
    print("\n2. COHERENCE BOUNDARY DETECTION:")
    boundaries = tracker.detect_coherence_boundaries(lookback=20)
    print(f"   Found {len(boundaries)} coherence boundaries:")
    for b in boundaries:
        print(f"     - Seq {b['sequence_number']}: {b['transition']}")
    
    print("\n3. ENTROPY PATTERN DISCOVERY:")
    patterns = tracker.discover_entropy_patterns(window_size=3, min_occurrences=2)
    print(f"   Found {len(patterns)} patterns:")
    for i, p in enumerate(patterns[:3]):  # Show top 3
        print(f"     Pattern {i+1}: {p['pattern']} (occurs {p['occurrences']}x)")
        print(f"       → {p['interpretation']}")
    
    print("\n4. STATISTICS:")
    stats = tracker.get_statistics()
    print(f"   Total transitions: {stats['total_transitions']}")
    print(f"   Entropy range: {stats['min_entropy']:.3f} - {stats['max_entropy']:.3f}")
    print(f"   Average entropy: {stats['avg_entropy']:.3f}")
    print(f"   Boundaries: {stats['coherence_boundaries_detected']}")
    
    print("\n5. ENTROPY TABLE PERFORMANCE:")
    print(f"   Pre-computed table entries: {len(tracker.entropy_table)}")
    print(f"   Lookup time: O(1) per delta")
    print(f"   Saves recomputation of entropy for every transition ✓")
    
    print("\n✅ Delta tracking complete")


if __name__ == "__main__":
    test_delta_tracking()
