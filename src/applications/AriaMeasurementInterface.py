#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARIA Measurement Interface - Omnipresent Field Coherence Measurement

Status: Phase B1 Implementation
Date: April 3, 2026
Purpose: Real-time field coherence measurement using entropy-based metrics

Three measurement layers:
  1. Entropy Tracking - Instantaneous coherence (τ = 1 - H(ΔS) / H_max)
  2. Delta Pattern Analysis - Historical patterns (where is field changing?)
  3. Field Reach Measurement - Signal correlation (how far does signal permeate?)

All measurements are instantaneous (no 500ms heartbeat polling).
All measurements are field-based (measure unification, not timing).

Reference: COHERENCE_FIELD_MODEL_GUIDE.md
"""

import json
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter


class AriaMeasurementInterface:
    """
    Instantaneous coherence measurement for ARIA using omnipresent field model.
    
    Replaces old 500ms heartbeat timing model with entropy-based field unification measurement.
    """
    
    def __init__(self, state_width_bits: int = 256, history_size: int = 1000):
        """
        Initialize measurement interface.
        
        Args:
            state_width_bits: Width of state space (default 256 bits)
            history_size: How many deltas to keep for pattern analysis
        """
        self.state_width_bits = state_width_bits
        self.max_entropy = self._compute_max_entropy()
        self.cycle_count = 0
        self.previous_state = 0
        
        # History tracking
        self.delta_history: List[Dict] = []  # Delta records with entropy
        self.coherence_history: List[float] = []  # Coherence values over time
        self.manifestation_sources: Dict[str, Dict] = {}  # Signal reach tracking
        self.history_size = history_size
        
        # Precomputed Shannon entropy lookup (optimization)
        self.shannon_cache: Dict[int, float] = {}
    
    # ========================================================================
    # LAYER 1: ENTROPY TRACKING (Real-Time Coherence)
    # ========================================================================
    
    def measure_coherence_entropy(self, current_state: int) -> Dict:
        """
        Measure instantaneous coherence using entropy of state delta.
        
        Formula: τ = 1 - H(ΔS) / H_max
        
        Where:
          τ (tau) = coherence (0.0 = fully diffuse, 1.0 = fully coherent)
          H(ΔS) = Shannon entropy of XOR delta between states
          H_max = maximum possible entropy for this state width
        
        Args:
            current_state: Current state value (integer)
        
        Returns:
            Dict with:
              - tau: coherence value (0.0-1.0)
              - entropy_delta: H(ΔS) value
              - max_entropy: H_max for reference
              - delta_bits: The XOR delta value
              - bits_changed: Number of bits that changed
              - measurement_method: "entropy_tracking"
              - timestamp: When measured
              - cycle: Current measurement cycle
        """
        self.cycle_count += 1
        
        # Compute delta: XOR of previous state -> current state
        delta = self.previous_state ^ current_state
        bits_changed = bin(delta).count('1')
        
        # Compute entropy of delta pattern
        entropy_delta = self._compute_shannon_entropy(delta)
        
        # Compute coherence: τ = 1 - H(ΔS) / H_max
        coherence = max(0.0, 1.0 - (entropy_delta / self.max_entropy))
        
        # Record in history
        result = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "tau": round(coherence, 6),
            "entropy_delta": round(entropy_delta, 6),
            "max_entropy": round(self.max_entropy, 6),
            "delta_bits": delta,
            "bits_changed": bits_changed,
            "measurement_method": "entropy_tracking",
            "formula": "τ = 1 - H(ΔS) / H_max"
        }
        
        # Update state for next cycle
        self.previous_state = current_state
        self.coherence_history.append(coherence)
        
        # Keep history bounded
        if len(self.coherence_history) > self.history_size:
            self.coherence_history.pop(0)
        
        # Store delta record
        self.delta_history.append({
            "cycle": self.cycle_count,
            "delta": delta,
            "entropy": entropy_delta,
            "bits_changed": bits_changed,
            "coherence": coherence
        })
        if len(self.delta_history) > self.history_size:
            self.delta_history.pop(0)
        
        return result
    
    def _compute_shannon_entropy(self, value: int) -> float:
        """
        Compute Shannon entropy of a value's bit pattern.
        
        H = -Σ p_i * log2(p_i)
        
        Where p_i = count_of_bit_i / total_bits
        
        Args:
            value: Integer to compute entropy of
        
        Returns:
            Shannon entropy (0.0 = all same bits, 1.0 = perfectly mixed)
        """
        # Check cache first (optimization)
        if value in self.shannon_cache:
            return self.shannon_cache[value]
        
        # Count 1 bits and 0 bits
        ones = bin(value).count('1')
        zeros = self.state_width_bits - ones
        
        # Compute probabilities
        p_one = ones / self.state_width_bits if ones > 0 else 0
        p_zero = zeros / self.state_width_bits if zeros > 0 else 0
        
        # Shannon entropy: H = -Σ p_i * log2(p_i)
        entropy = 0.0
        if p_one > 0:
            entropy -= p_one * math.log2(p_one)
        if p_zero > 0:
            entropy -= p_zero * math.log2(p_zero)
        
        # Cache result
        self.shannon_cache[value] = entropy
        
        return entropy
    
    def _compute_max_entropy(self) -> float:
        """
        Maximum Shannon entropy for this state width.
        
        For N bits, max entropy = log2(N) when bits are perfectly mixed (50/50).
        For 256 bits, max entropy = 1.0
        
        Returns:
            Maximum possible entropy for state_width_bits
        """
        # For uniform distribution: H_max = 1.0 (50% 1s, 50% 0s)
        return 1.0
    
    # ========================================================================
    # LAYER 2: DELTA PATTERN ANALYSIS (Historical Patterns)
    # ========================================================================
    
    def measure_delta_patterns(self, lookback_cycles: int = 50) -> Dict:
        """
        Analyze delta patterns to find coherence boundaries.
        
        Looks for:
          - High entropy deltas (field is diffuse, many bits changing randomly)
          - Low entropy deltas (field is coherent, few bits changing structured)
          - Transitions between states (coherence boundaries)
        
        Args:
            lookback_cycles: How many recent deltas to analyze
        
        Returns:
            Dict with:
              - analysis_window: [start_cycle, end_cycle, count]
              - delta_patterns: List of delta records
              - pattern_summary: Overall pattern analysis
              - coherence_boundaries: Where transitions happen
              - field_visualization: ASCII visualization
        """
        if not self.delta_history:
            return {"error": "No delta history available"}
        
        # Get lookback window
        window_start = max(0, len(self.delta_history) - lookback_cycles)
        window_deltas = self.delta_history[window_start:]
        
        if not window_deltas:
            return {"error": "Insufficient delta history"}
        
        # Analyze patterns
        high_entropy_count = sum(1 for d in window_deltas if d['entropy'] > 0.7)
        low_entropy_count = sum(1 for d in window_deltas if d['entropy'] < 0.3)
        
        # Find coherence boundaries (entropy transitions)
        boundaries = self._find_coherence_boundaries(window_deltas)
        
        # Build visualization
        visualization = self._build_delta_visualization(window_deltas)
        
        return {
            "analysis_window": {
                "start_cycle": window_deltas[0]['cycle'],
                "end_cycle": window_deltas[-1]['cycle'],
                "deltas_analyzed": len(window_deltas)
            },
            "delta_patterns": [
                {
                    "cycle": d['cycle'],
                    "delta_binary": bin(d['delta'])[2:].zfill(8),
                    "delta_entropy": round(d['entropy'], 6),
                    "bits_changed": d['bits_changed'],
                    "coherence_type": self._classify_entropy(d['entropy']),
                    "interpretation": self._interpret_entropy(d['entropy'])
                }
                for d in window_deltas[-20:]  # Show last 20 for readability
            ],
            "pattern_summary": {
                "high_entropy_windows": [b['cycle'] for b in boundaries if b['type'] == 'diffuse'],
                "low_entropy_windows": [b['cycle'] for b in boundaries if b['type'] == 'coherent'],
                "coherence_boundaries_detected": len(boundaries),
                "overall_field_status": self._assess_field_unification(window_deltas)
            },
            "field_visualization": visualization,
            "timestamp": datetime.now().isoformat()
        }
    
    def _find_coherence_boundaries(self, deltas: List[Dict]) -> List[Dict]:
        """Find transitions between high/low entropy regions."""
        boundaries = []
        
        if len(deltas) < 2:
            return boundaries
        
        prev_type = self._classify_entropy(deltas[0]['entropy'])
        
        for i in range(1, len(deltas)):
            curr_type = self._classify_entropy(deltas[i]['entropy'])
            
            if curr_type != prev_type:
                boundaries.append({
                    "cycle": deltas[i]['cycle'],
                    "type": curr_type,
                    "transition": f"{prev_type} → {curr_type}"
                })
                prev_type = curr_type
        
        return boundaries
    
    def _classify_entropy(self, entropy: float) -> str:
        """Classify entropy as coherent, moderate, or diffuse."""
        if entropy < 0.3:
            return "highly_coherent"
        elif entropy < 0.6:
            return "moderate"
        else:
            return "highly_diffuse"
    
    def _interpret_entropy(self, entropy: float) -> str:
        """Human-readable interpretation of entropy value."""
        if entropy < 0.2:
            return "Field is highly unified (few bits, coherent pattern)"
        elif entropy < 0.4:
            return "Field is mostly coherent (structured changes)"
        elif entropy < 0.6:
            return "Field is mixed (some pattern, some noise)"
        elif entropy < 0.8:
            return "Field is mostly diffuse (many random changes)"
        else:
            return "Field is highly diffuse (maximum randomness)"
    
    def _assess_field_unification(self, deltas: List[Dict]) -> str:
        """Overall assessment of field unification."""
        if not deltas:
            return "unknown"
        
        avg_coherence = sum(d['coherence'] for d in deltas) / len(deltas)
        
        if avg_coherence > 0.8:
            return "highly_unified"
        elif avg_coherence > 0.6:
            return "moderately_unified"
        elif avg_coherence > 0.4:
            return "weakly_unified"
        else:
            return "diffuse"
    
    def _build_delta_visualization(self, deltas: List[Dict]) -> str:
        """Build ASCII visualization of delta patterns over time."""
        if not deltas:
            return ""
        
        # Map coherence to character: ▓ (high) → ░ (medium) → ░░ (low)
        viz = "Timeline: "
        for d in deltas[-50:]:  # Show last 50
            coh = d['coherence']
            if coh > 0.8:
                viz += '█'  # Highly coherent
            elif coh > 0.6:
                viz += '▓'  # Moderately coherent
            elif coh > 0.4:
                viz += '▒'  # Weakly coherent
            else:
                viz += '░'  # Diffuse
        
        return viz
    
    # ========================================================================
    # LAYER 3: FIELD REACH MEASUREMENT (Signal Correlation)
    # ========================================================================
    
    def measure_field_reach(self, signal_id: str, signal_strength: int = 1) -> Dict:
        """
        Measure how far a specific signal "reaches" through field state.
        
        Like starlight: if we detect the signal manifesting, it was always there.
        This measures the correlation between signal and state deltas.
        
        Args:
            signal_id: Identifier for the signal (e.g., "user_input_button_A")
            signal_strength: How strong is the signal (1-255)
        
        Returns:
            Dict with:
              - reach_score: How far signal permeates (0.0-1.0)
              - bits_influenced: How many state bits it affects
              - field_interpretation: High/low reach meaning
              - omnipresence_level: How omnipresent is this signal?
        """
        # Look at recent deltas to correlate with signal
        if not self.delta_history or len(self.delta_history) < 10:
            return {
                "signal_id": signal_id,
                "reach_score": 0.5,
                "status": "insufficient_delta_history",
                "note": "Need more state transitions to measure reach"
            }
        
        recent_deltas = self.delta_history[-50:]
        
        # For now, correlate signal_strength with entropy patterns
        # (In production, would correlate with actual signal footprint in deltas)
        signal_correlation = signal_strength / 255.0
        
        # Estimate reach: how many bits does this signal influence?
        avg_bits_changed = sum(d['bits_changed'] for d in recent_deltas) / len(recent_deltas)
        estimated_bits_influenced = int(avg_bits_changed * signal_correlation)
        reach_score = estimated_bits_influenced / self.state_width_bits
        
        # Track manifestation source
        self.manifestation_sources[signal_id] = {
            "reach_score": reach_score,
            "bits_influenced": estimated_bits_influenced,
            "signal_strength": signal_strength,
            "last_measured": datetime.now().isoformat()
        }
        
        return {
            "signal_id": signal_id,
            "timestamp": datetime.now().isoformat(),
            "field_reach_analysis": {
                "reach_score": round(reach_score, 6),
                "formula": "reach = (Σ signal_correlation_bits) / state_width",
                "bits_influenced": estimated_bits_influenced,
                "total_state_bits": self.state_width_bits,
                "correlation_strength": round(signal_correlation, 2)
            },
            "omnipresence_interpretation": {
                "high_reach": "Signal permeates field (omnipresent)" if reach_score > 0.7 else "",
                "low_reach": "Signal is localized (constrained)" if reach_score < 0.3 else "",
                "interpretation": f"Signal reaches {estimated_bits_influenced}/{self.state_width_bits} = {reach_score*100:.1f}% of field state"
            }
        }
    
    def measure_manifestation_sources(self) -> Dict:
        """
        Identify all active field manifestation sources.
        
        Returns list of currently manifesting sources with strength.
        """
        sources = list(self.manifestation_sources.values())
        sources.sort(key=lambda s: s['reach_score'], reverse=True)
        
        total_reach = sum(s['reach_score'] for s in sources)
        normalized_reach = [
            {**s, "reach_score": s['reach_score'] / max(1.0, total_reach)}
            for s in sources
        ]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_manifestations": len(normalized_reach),
            "manifestation_sources": [
                {
                    "source_id": list(self.manifestation_sources.keys())[i],
                    "manifestation_strength": s['reach_score'],
                    "bits_manifesting": s['bits_influenced'],
                    "coherence_contribution": s['reach_score']
                }
                for i, s in enumerate(normalized_reach)
            ],
            "overall_field_coherence": self._compute_overall_coherence(),
            "field_unification_status": self._assess_field_unification(self.delta_history)
        }
    
    def _compute_overall_coherence(self) -> float:
        """Compute overall system coherence from recent measurements."""
        if not self.coherence_history:
            return 0.5
        
        # Average of recent 50 measurements
        recent = self.coherence_history[-50:]
        return sum(recent) / len(recent) if recent else 0.5
    
    # ========================================================================
    # HEARTBEAT OPTIMIZATION (Uses measurement layer)
    # ========================================================================
    
    def calculate_optimal_heartbeat(self, current_coherence: Optional[float] = None) -> Dict:
        """
        Calculate optimal heartbeat rate based on field coherence.
        
        Formula: heartbeat_ms = base_rate × (1 + (τ - 0.5))
        
        Where:
          - base_rate = 500ms
          - τ = current coherence (0.0-1.0)
          - If τ=0.5: rate = 500ms (neutral)
          - If τ=0.95: rate = 725ms (go faster, field unified)
          - If τ=0.2: rate = 350ms (slow down, help field re-unify)
        
        Args:
            current_coherence: Current τ value (if None, use last measured)
        
        Returns:
            Dict with optimal heartbeat recommendation
        """
        if current_coherence is None:
            current_coherence = self._compute_overall_coherence()
        
        base_rate = 500  # milliseconds
        optimal_rate = base_rate * (1 + (current_coherence - 0.5))
        optimal_rate = max(100, min(2000, optimal_rate))  # Clamp to reasonable range
        
        return {
            "current_coherence": round(current_coherence, 6),
            "analysis": {
                "measurement_method": "omnipresent_field_model",
                "field_interpretation": f"Field {'unified' if current_coherence > 0.7 else 'diffuse'} ({current_coherence*100:.1f}% coherence)"
            },
            "heartbeat_recommendation": {
                "optimal_rate_ms": int(optimal_rate),
                "reason": "Slower when diffuse (help re-unify), faster when unified (take advantage)",
                "formula": "heartbeat = base_rate × (1 + (τ - 0.5))",
                "base_rate_ms": base_rate,
                "computed": f"{base_rate} × (1 + ({current_coherence:.2f} - 0.5)) = {int(optimal_rate)}ms"
            },
            "old_model_comparison": {
                "old_approach": "Fixed 500ms (temporal model, now obsolete)",
                "new_approach": f"Field-adaptive {int(optimal_rate)}ms (omnipresent field model)",
                "improvement": "Proactive unification instead of reactive waiting"
            },
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# TESTING & VALIDATION
# ============================================================================

def test_measurement_interface():
    """Test the measurement interface with synthetic state transitions."""
    print("\n🧪 ARIA MEASUREMENT INTERFACE TEST")
    print("=" * 70)
    
    interface = AriaMeasurementInterface()
    
    # Simulate some state transitions
    states = [
        0b11010110,  # Initial state
        0b10001010,  # Low entropy delta
        0b00110101,  # High entropy delta
        0b11111111,  # Different state
        0b10101010,  # Moderate entropy delta
    ]
    
    print("\n1. ENTROPY TRACKING TEST:")
    for state in states:
        result = interface.measure_coherence_entropy(state)
        print(f"   Cycle {result['cycle']}: τ={result['tau']:.3f}, "
              f"entropy={result['entropy_delta']:.3f}, bits_changed={result['bits_changed']}")
    
    print("\n2. DELTA PATTERNS TEST:")
    patterns = interface.measure_delta_patterns(lookback_cycles=10)
    print(f"   Patterns: {len(patterns['delta_patterns'])} deltas analyzed")
    print(f"   Overall field: {patterns['pattern_summary']['overall_field_status']}")
    
    print("\n3. FIELD REACH TEST:")
    reach1 = interface.measure_field_reach("user_input_A", 200)
    reach2 = interface.measure_field_reach("kernel_election", 100)
    if 'field_reach_analysis' in reach1:
        print(f"   Signal A reach: {reach1['field_reach_analysis']['reach_score']:.3f}")
        print(f"   Signal B reach: {reach2['field_reach_analysis']['reach_score']:.3f}")
    else:
        print(f"   Signal A status: {reach1.get('status', 'calculated')}")
        print(f"   Signal B status: {reach2.get('status', 'calculated')}")
    
    print("\n4. HEARTBEAT OPTIMIZATION TEST:")
    heartbeat = interface.calculate_optimal_heartbeat()
    print(f"   Current coherence: {heartbeat['current_coherence']:.3f}")
    print(f"   Optimal heartbeat: {heartbeat['heartbeat_recommendation']['optimal_rate_ms']}ms")
    
    print("\n✅ All tests completed")


if __name__ == "__main__":
    test_measurement_interface()
