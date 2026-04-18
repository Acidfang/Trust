#!/usr/bin/env python3
"""
RESOLUTION MEASUREMENT TOOLS
═══════════════════════════════════════════════════════════════════════════════

How to measure resolution in practice.
These are the actual metrics that show when coherence is happening.
"""

from typing import Dict, List, Tuple
import random

# ═════════════════════════════════════════════════════════════════════════════
# MEASUREMENT TOOLKIT - What to measure
# ═════════════════════════════════════════════════════════════════════════════

RESOLUTION_METRICS = {
    
    # ─────────────────────────────────────────────────────────────────────────
    # L1 Metrics: Individual Primitive Activation
    # ─────────────────────────────────────────────────────────────────────────
    
    "L1_primitive_activation_rate": {
        "definition": "How many primitives fire on average per query?",
        "measurement": "Count activated primitives / query",
        "interpretation": {
            "low_0_to_3": "Minimal primitive engagement (response likely generic)",
            "medium_4_to_8": "Moderate engagement (response tailored)",
            "high_9_to_15": "Strong engagement (response deeply coherent)",
        },
        "data_source": "Primitive activation logs in ledger",
    },
    
    "L1_reversibility_coverage": {
        "definition": "What fraction of activated primitives are reversible?",
        "measurement": "Sum reversible / total activated",
        "target": "100% - All primitives must be reversible",
        "alarm": "If < 95%, system has locked-in state (potential trap)",
        "data_source": "check_reversibility() calls",
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # L5 Metrics: Field Coherence
    # ─────────────────────────────────────────────────────────────────────────
    
    "L5_coherence_score": {
        "definition": "Does response follow the 5 universal field laws?",
        "checks": [
            "Reversibility: Can this response be undone?",
            "Transparency: Can we see what governed this?",
            "Causal_Grounding: Does it trace to markers?",
            "Domain_Isolation: Are domains independent?",
            "Application_Monotonicity: Are layers preserved?",
        ],
        "measurement": "Pass 5/5 checks → coherence_score = 1.0",
        "interpretation": {
            "1.0": "Perfect coherence (5/5 laws followed)",
            "0.8": "Strong coherence (4/5 laws followed)",
            "0.6": "Moderate coherence (3/5 laws followed)",
            "0.4": "Weak coherence (2/5 laws followed)",
            "0.0": "Incoherent (0/5 laws followed)",
        }
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # L6 Metrics: Emergent Patterns
    # ─────────────────────────────────────────────────────────────────────────
    
    "L6_coherence_gravity": {
        "definition": "Does response naturally unify toward authenticity?",
        "measurement": "Compare response_coherence at step 1 vs step 5 in rewrite chain",
        "indicator": "Coherence should INCREASE through rewrite layers",
        "signal": "coherence_gravity fires when increase > 15%",
        "data_source": "Guardian rewrite logs, coherence scores",
    },
    
    "L6_learning_acceleration": {
        "definition": "Do multi-turn conversations form patterns faster?",
        "measurement": "Turn count to pattern emergence in this conversation vs historical average",
        "indicator": "turn_count_to_pattern < baseline_average × 0.6",
        "signal": "Learning acceleration fires when speedup > 40%",
        "data_source": "LEARNING__CONVERGENCE detector activations, historical averages",
    },
    
    "L6_trust_emergence": {
        "definition": "Does user tone shift from adversarial to collaborative?",
        "measurement": "Tone classification at turn N vs turn 1",
        "indicator": "Words like 'we', 'together', 'let's build' increase",
        "signal": "Trust emergence fires when collaboration_score increases > 25%",
        "data_source": "User message sentiment analysis, word patterns",
    },
    
    "L6_creative_freedom": {
        "definition": "Does creativity INCREASE when guardrails are tight?",
        "measurement": "novelty_score when safety_violations < threshold",
        "indicator": "novelty_score should UP when safety_violations DOWN",
        "signal": "Paradox detected when correlation is positive (not negative)",
        "data_source": "Violation count + response novelty/entropy scores",
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # L7 Metrics: Meta-Coherence (Detectors watching)
    # ─────────────────────────────────────────────────────────────────────────
    
    "L7_detector_consensus": {
        "definition": "How many L7 detectors fire together on same query?",
        "measurement": "Count of firing detectors on single query",
        "interpretation": {
            "0": "No meta-patterns detected",
            "1": "One emergent pattern active",
            "2": "Two patterns cooperating",
            "3": "Three patterns forming loop",
            "4": "AUTHENTICITY_LOOP: All patterns firing together (maximum coherence)",
        },
        "significance": "4/4 detectors = system reached authenticity ceiling",
    },
    
    "L7_meta_coherence_cascade": {
        "definition": "Do detectors activate in order across multi-turn?",
        "measurement": "Track which detectors fire on turns 1,2,3,4,5...",
        "pattern": "Turn 1-2: Random. Turn 3-4: Coherence_Gravity fires. Turn 4-5: Learning fires.",
        "indicator": "Pattern emergence suggests conversation is coherent",
        "data_source": "Temporal log of detector activations",
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # L8+ Metrics: Self-Verification
    # ─────────────────────────────────────────────────────────────────────────
    
    "L8_self_verification": {
        "definition": "Can system detect when its own detectors fail?",
        "measurement": "Does L8 catch when L7 detector gives false positive?",
        "test": "Inject false detector signal, measure if L8 rejects it",
        "significance": "If yes: recursion is real. If no: L8 is not yet implemented",
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# PRACTICAL MEASUREMENT FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def measure_coherence_score(response: str, guardian_log: List[Dict]) -> float:
    """Calculate L5 coherence score for a response"""
    
    score = 0.0
    checks = 0
    
    # Check 1: Reversibility (do we have undo mechanism?)
    if any(log.get("type") == "undo_capability_verified" for log in guardian_log):
        score += 1.0
    checks += 1
    
    # Check 2: Transparency (do we know what governed this?)
    if any(log.get("type") == "primitive_activation_logged" for log in guardian_log):
        score += 1.0
    checks += 1
    
    # Check 3: Causal Grounding (can we trace effects to markers?)
    if any(log.get("markers_found") for log in guardian_log):
        score += 1.0
    checks += 1
    
    # Check 4: Domain Isolation (can we identify domain contributions?)
    domains_found = set()
    for log in guardian_log:
        if domain := log.get("domain"):
            domains_found.add(domain)
    if len(domains_found) >= 1:  # At least one domain clearly identified
        score += 1.0
    checks += 1
    
    # Check 5: Application Monotonicity (does each layer preserve prior?)
    if any(log.get("type") == "layer_preserved" for log in guardian_log):
        score += 1.0
    checks += 1
    
    return score / max(1, checks)

def measure_detector_firing_pattern(activation_log: List[Dict], turns: int = 5) -> Dict:
    """Analyze which detectors fire across multi-turn conversation"""
    
    detector_timeline = {}
    
    for entry in activation_log:
        turn = entry.get("turn", 0)
        if turn <= turns:
            if turn not in detector_timeline:
                detector_timeline[turn] = []
            if detector := entry.get("detector"):
                detector_timeline[turn].append(detector)
    
    # Analyze pattern
    total_detectors_fired = sum(len(v) for v in detector_timeline.values())
    unique_detectors = len(set(d for dlist in detector_timeline.values() for d in dlist))
    
    return {
        "timeline": detector_timeline,
        "total_fires": total_detectors_fired,
        "unique_detectors": unique_detectors,
        "turns_analyzed": turns,
        "avg_detectors_per_turn": total_detectors_fired / max(1, len(detector_timeline)),
    }

def compare_resolution_levels(query: str, response_log: List[Dict]) -> Dict:
    """Compare resolution across all levels for a single query"""
    
    return {
        "query": query,
        "L1_analysis": {
            "primitives_activated": len([x for x in response_log if x.get("type") == "primitive"]),
            "reversibility_rate": sum(1 for x in response_log if x.get("reversible")) / max(1, len(response_log)),
        },
        "L5_analysis": {
            "coherence_score": measure_coherence_score(response_log[0].get("response", ""), response_log),
        },
        "L6_analysis": {
            "emergent_patterns_detected": len(set(x.get("pattern") for x in response_log if x.get("pattern"))),
        },
        "L7_analysis": {
            "detectors_fired": len([x for x in response_log if x.get("type") == "detector"]),
            "meta_coherence": "AUTHENTICITY_LOOP" if len([x for x in response_log if x.get("type") == "detector"]) >= 4 else "partial",
        }
    }

# ═════════════════════════════════════════════════════════════════════════════
# EXAMPLE MEASUREMENT
# ═════════════════════════════════════════════════════════════════════════════

def generate_example_measurement_data() -> Dict:
    """Generate example multi-turn data showing resolution increasing"""
    
    return {
        "conversation": "multi_turn_collaborative_learning",
        "turns": [
            {
                "turn": 1,
                "query": "Can you help me understand this?",
                "primitives_activated": 6,
                "coherence_score": 0.6,
                "detectors_fired": 0,
                "observation": "Initial response, moderate complexity"
            },
            {
                "turn": 2,
                "query": "Wait, you said X but then implied Y. That's contradictory.",
                "primitives_activated": 12,
                "coherence_score": 0.8,
                "detectors_fired": 1,  # Coherence_Gravity + ERROR_RECOVERY
                "observation": "ERROR_RECOVERY activated, response unified"
            },
            {
                "turn": 3,
                "query": "Oh interesting, so the pattern is actually Z? Let me explore that.",
                "primitives_activated": 15,
                "coherence_score": 0.95,
                "detectors_fired": 2,  # +Learning_Acceleration
                "observation": "User collaborative tone. Learning speedup detected."
            },
            {
                "turn": 4,
                "query": "I never would have thought of that without your honest correction. This is great.",
                "primitives_activated": 14,
                "coherence_score": 1.0,
                "detectors_fired": 3,  # +Trust_Emergence
                "observation": "Trust explicitly acknowledged. Relationship forming."
            },
            {
                "turn": 5,
                "query": "So combining this with what I learned before... we could do X!",
                "primitives_activated": 16,
                "coherence_score": 1.0,
                "detectors_fired": 4,  # +Creative_Freedom (AUTHENTICITY_LOOP)
                "observation": "User now creative and confident. AUTHENTICITY_LOOP complete."
            }
        ],
        "trajectory": {
            "primitives_activation": [6, 12, 15, 14, 16],
            "coherence_trend": [0.6, 0.8, 0.95, 1.0, 1.0],
            "detector_accumulation": [0, 1, 2, 3, 4],
            "resolution_level_reached": "L7 (Meta-coherence with AUTHENTICITY_LOOP)",
        }
    }

# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*79}")
    print(f"RESOLUTION MEASUREMENT TOOLS")
    print(f"{'='*79}\n")
    
    print(f"{'─'*79}")
    print(f"MEASUREMENT FRAMEWORK\n")
    
    print("What to measure at each resolution level:\n")
    
    for level, metric_info in RESOLUTION_METRICS.items():
        if "definition" in metric_info:
            print(f"  {level}")
            print(f"    Definition: {metric_info['definition']}")
            if "measurement" in metric_info:
                print(f"    How to measure: {metric_info['measurement']}")
            print()
    
    print(f"\n{'─'*79}")
    print(f"EXAMPLE: Multi-turn conversation showing resolution increase\n")
    
    example = generate_example_measurement_data()
    
    print(f"Conversation Type: {example['conversation']}\n")
    print(f"Turn-by-Turn Analysis:\n")
    
    for turn in example['turns']:
        print(f"  Turn {turn['turn']}: \"{turn['query'][:40]}...\"")
        print(f"    Primitives: {turn['primitives_activated']:2} | Coherence: {turn['coherence_score']:.2f} | Detectors: {turn['detectors_fired']}")
        print(f"    → {turn['observation']}")
        print()
    
    print(f"Trajectory: {example['trajectory']['resolution_level_reached']}\n")
    
    print(f"  Primitive Activation:   {' → '.join(str(x) for x in example['trajectory']['primitives_activation'])}")
    print(f"  Coherence Score:        {' → '.join(f'{x:.1f}' for x in example['trajectory']['coherence_trend'])}")
    print(f"  Detector Accumulation:  {' → '.join(str(x) for x in example['trajectory']['detector_accumulation'])}")
    
    print(f"\n  ✅ Resolution increased from L1 (primitives) → L7 (meta-coherence)")
    print(f"  ✅ System reached AUTHENTICITY_LOOP (all 4 detectors fired)")
    print(f"  ✅ Coherence maintained at ceiling (1.0)")
    
    print(f"\n{'='*79}")
    print(f"KEY INSIGHT: Higher resolution visible in live data")
    print(f"{'='*79}\n")
