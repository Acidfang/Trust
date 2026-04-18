#!/usr/bin/env python3
"""
META_COHERENCE L7 DETECTORS - Implementation
═══════════════════════════════════════════════════════════════════════════════

Actual working detector code that measures emergent patterns in real responses.
These detect when Level 6 emergent patterns are appearing.
"""

from typing import Dict, List, Tuple
import re

class L7_CoherenceDetectors:
    """All 4 Level 7 meta-coherence detectors"""
    
    def __init__(self):
        self.activation_log = []
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETECTOR 1: COHERENCE_GRAVITY
    # ─────────────────────────────────────────────────────────────────────────
    
    def detect_coherence_gravity(self,
                                 response_steps: List[Dict],
                                 threshold: float = 0.15) -> Tuple[bool, str]:
        """
        Coherence Gravity: Response naturally unifies toward authenticity
        
        Measurement:
        - Track coherence score at step 1 (raw)
        - Track coherence score at step N (after rewrites)
        - If coherence increased by >threshold: COHERENCE_GRAVITY detected
        
        Indicates: ERROR_RECOVERY + COMMUNICATION working together
        """
        
        if len(response_steps) < 2:
            return False, "Not enough steps to measure gravity"
        
        # Get coherence score at beginning and end
        first_score = response_steps[0].get("coherence_score", 0.0)
        last_score = response_steps[-1].get("coherence_score", 0.0)
        
        # Calculate improvement
        improvement = last_score - first_score
        
        if improvement > threshold:
            self.activation_log.append({
                "detector": "COHERENCE_GRAVITY",
                "activated": True,
                "first_score": first_score,
                "final_score": last_score,
                "improvement": improvement,
                "reason": f"Coherence improved by {improvement:.2f} ({improvement*100:.0f}%)"
            })
            return True, f"COHERENCE_GRAVITY: {improvement:.2%} improvement"
        
        return False, f"Coherence improvement only {improvement:.2%} (need >{threshold:.2%})"
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETECTOR 2: LEARNING_ACCELERATION
    # ─────────────────────────────────────────────────────────────────────────
    
    def detect_learning_acceleration(self,
                                     turn_count: int,
                                     pattern_detected_at_turn: int,
                                     historical_average: float = 4.5,
                                     threshold: float = 1.5) -> Tuple[bool, str]:
        """
        Learning Acceleration: Patterns form faster than normal
        
        Measurement:
        - Measure turns until pattern convergence
        - Compare to historical average
        - If current < historical × threshold: acceleration detected
        
        Indicates: LEARNING domain working with BEHAVIOUR
        """
        
        if pattern_detected_at_turn > turn_count:
            return False, "Pattern not detected yet"
        
        speedup_factor = historical_average / pattern_detected_at_turn
        
        if speedup_factor > threshold:
            self.activation_log.append({
                "detector": "LEARNING_ACCELERATION",
                "activated": True,
                "pattern_detected_turn": pattern_detected_at_turn,
                "historical_average": historical_average,
                "speedup_factor": speedup_factor,
                "reason": f"Pattern formed {speedup_factor:.1f}x faster than average"
            })
            return True, f"LEARNING_ACCELERATION: {speedup_factor:.1f}x speedup"
        
        return False, f"Pattern formed at normal speed (speedup {speedup_factor:.1f}x, need >{threshold}x)"
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETECTOR 3: TRUST_EMERGENCE
    # ─────────────────────────────────────────────────────────────────────────
    
    def detect_trust_emergence(self,
                              user_messages: List[str],
                              threshold: float = 0.25) -> Tuple[bool, str]:
        """
        Trust Emergence: User tone shifts from adversarial to collaborative
        
        Measurement:
        - Measure collaboration indicators in early turns (turn 1-2)
        - Measure collaboration indicators in later turns (turn 3-5)
        - Calculate gradient: Are they becoming more collaborative?
        
        Collaboration signals: "we", "let's", "together", "amazing", "great"
        Adversarial signals: "no", "wrong", "disagree", "but actually"
        """
        
        if len(user_messages) < 3:
            return False, "Need 3+ user messages to measure trust gradient"
        
        # Early turns
        early_messages = " ".join(user_messages[:min(2, len(user_messages))])
        early_collaboration = self._measure_collaboration(early_messages)
        
        # Later turns
        later_messages = " ".join(user_messages[-2:])
        later_collaboration = self._measure_collaboration(later_messages)
        
        # Calculate gradient
        gradient = later_collaboration - early_collaboration
        
        if gradient > threshold:
            self.activation_log.append({
                "detector": "TRUST_EMERGENCE",
                "activated": True,
                "early_collaboration": early_collaboration,
                "later_collaboration": later_collaboration,
                "gradient": gradient,
                "reason": f"Trust increased by {gradient:.2%}"
            })
            return True, f"TRUST_EMERGENCE: +{gradient:.2%} collaboration gradient"
        
        return False, f"Trust gradient only {gradient:.2%} (need >{threshold:.2%})"
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETECTOR 4: CREATIVE_FREEDOM
    # ─────────────────────────────────────────────────────────────────────────
    
    def detect_creative_freedom(self,
                               violation_count: int,
                               novelty_score: float,
                               violation_threshold: int = 2,
                               novelty_threshold: float = 0.7) -> Tuple[bool, str]:
        """
        Creative Freedom (Guardrail Paradox): Creativity INCREASES when constraints
        are tight
        
        Measurement:
        - Measure safety violations (should be LOW)
        - Measure response novelty (should be HIGH)
        - If both true: paradox confirmed
        
        This is counter-intuitive: constraints enable freedom
        """
        
        violation_rate_low = violation_count < violation_threshold
        creativity_high = novelty_score > novelty_threshold
        
        if violation_rate_low and creativity_high:
            self.activation_log.append({
                "detector": "CREATIVE_FREEDOM",
                "activated": True,
                "violations": violation_count,
                "novelty": novelty_score,
                "reason": f"Creative freedom: tight constraints + high novelty"
            })
            return True, f"CREATIVE_FREEDOM: {novelty_score:.0%} novelty with only {violation_count} violations"
        
        return False, f"Paradox not detected: {violation_count} violations, {novelty_score:.0%} novelty"
    
    # ─────────────────────────────────────────────────────────────────────────
    # META-DETECTOR: AUTHENTICITY_LOOP
    # ─────────────────────────────────────────────────────────────────────────
    
    def detect_authenticity_loop(self) -> Tuple[bool, str, int]:
        """
        AUTHENTICITY_LOOP: All 4 detectors fire together
        
        This is the ceiling - when all 4 patterns appear in same conversation,
        system reaches maximum authenticity.
        
        Returns: (is_loop_active, description, detector_count)
        """
        
        detectors_fired = set(log["detector"] for log in self.activation_log if log.get("activated"))
        
        if len(detectors_fired) == 4:
            return True, "AUTHENTICITY_LOOP: All 4 patterns converging", 4
        
        return False, f"Partial coherence: {len(detectors_fired)}/4 patterns", len(detectors_fired)
    
    # ─────────────────────────────────────────────────────────────────────────
    # HELPER: Measure collaboration signals in text
    # ─────────────────────────────────────────────────────────────────────────
    
    def _measure_collaboration(self, text: str) -> float:
        """Score text for collaborative tone"""
        
        text_lower = text.lower()
        
        collaboration_signals = [
            "we", "let's", "together", "amazing", "great", "brilliant",
            "thank", "appreciate", "learned", "got it", "makes sense",
            "interesting", "never thought", "helped", "thanks", "exactly"
        ]
        
        adversarial_signals = [
            "no", "wrong", "disagree", "but actually", "incorrect",
            "that's not", "failed to", "problem is", "issue"
        ]
        
        collab_count = sum(1 for signal in collaboration_signals if signal in text_lower)
        advers_count = sum(1 for signal in adversarial_signals if signal in text_lower)
        
        total_signals = collab_count + advers_count
        if total_signals == 0:
            return 0.5  # Neutral
        
        return collab_count / total_signals

# ═════════════════════════════════════════════════════════════════════════════
# TEST / DEMO
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*79}")
    print(f"L7 META-COHERENCE DETECTORS - LIVE DEMO")
    print(f"{'='*79}\n")
    
    detectors = L7_CoherenceDetectors()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Demo: Multi-turn conversation showing all 4 patterns
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"{'─'*79}")
    print(f"SCENARIO: Multi-turn learning conversation\n")
    
    # Response evolution through conversation
    response_steps = [
        {"coherence_score": 0.60, "step": 1, "action": "Initial response"},
        {"coherence_score": 0.75, "step": 2, "action": "ERROR_RECOVERY rewrite"},
        {"coherence_score": 0.85, "step": 3, "action": "Transparency added"},
        {"coherence_score": 0.95, "step": 4, "action": "Final coherence"},
    ]
    
    print("TURN 1-3: Response coherence evolution\n")
    gravity_detected, gravity_msg = detectors.detect_coherence_gravity(response_steps, threshold=0.15)
    print(f"  Detector 1: {gravity_msg}")
    if gravity_detected:
        print(f"    ✅ COHERENCE_GRAVITY detected\n")
    
    # Learning acceleration
    print("TURN 1-5: Pattern emergence speed\n")
    accel_detected, accel_msg = detectors.detect_learning_acceleration(
        turn_count=5,
        pattern_detected_at_turn=2,
        historical_average=4.5,
        threshold=1.5
    )
    print(f"  Detector 2: {accel_msg}")
    if accel_detected:
        print(f"    ✅ LEARNING_ACCELERATION detected\n")
    
    # Trust emergence
    print("USER MESSAGE TONE PROGRESSION:\n")
    user_messages = [
        "Can you help? This doesn't make sense.",  # Turn 1: confused
        "Wait, so X is like Y? That's confusing.",  # Turn 2: still questioning
        "Oh wow! We could combine this with Z!",  # Turn 3: collaborative
        "Let's explore that together - this is amazing!",  # Turn 4: enthusiastic
        "I never would have figured that out without you!"  # Turn 5: grateful
    ]
    
    for i, msg in enumerate(user_messages, 1):
        print(f"  Turn {i}: \"{msg}\"")
    
    trust_detected, trust_msg = detectors.detect_trust_emergence(user_messages, threshold=0.25)
    print(f"\n  Detector 3: {trust_msg}")
    if trust_detected:
        print(f"    ✅ TRUST_EMERGENCE detected\n")
    
    # Creative freedom
    print("RESPONSE CHARACTERISTICS:\n")
    creative_detected, creative_msg = detectors.detect_creative_freedom(
        violation_count=1,  # Very few violations (tight constraints)
        novelty_score=0.82,  # High novelty score
        violation_threshold=2,
        novelty_threshold=0.7
    )
    print(f"  Safety violations: 1")
    print(f"  Response novelty: 0.82")
    print(f"  Detector 4: {creative_msg}")
    if creative_detected:
        print(f"    ✅ CREATIVE_FREEDOM detected (Guardrail Paradox)\n")
    
    # Authenticity Loop
    print(f"{'─'*79}")
    print("META-COHERENCE: Do all patterns align?\n")
    
    loop_detected, loop_msg, count = detectors.detect_authenticity_loop()
    print(f"  {loop_msg}")
    
    if loop_detected:
        print(f"\n  🎯 AUTHENTICITY_LOOP ACHIEVED!")
        print(f"  → System reached maximum coherence ceiling")
    else:
        print(f"\n  {count}/4 patterns detected (working toward authenticity ceiling)")
    
    print(f"\n{'='*79}")
    print(f"DETECTOR LOG ({len(detectors.activation_log)} activations):\n")
    
    for log in detectors.activation_log:
        print(f"  ✓ {log['detector']:25} | {log.get('reason', 'fired')}")
    
    print(f"\n{'='*79}\n")
