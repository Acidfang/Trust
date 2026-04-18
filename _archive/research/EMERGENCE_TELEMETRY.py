#!/usr/bin/env python3
"""
EMERGENCE TELEMETRY
═══════════════════════════════════════════════════════════════════════════════

Live tracking of when emergent patterns (L6) appear in conversations.
This is how we know the system is working - patterns should naturally appear
when primitives cooperate properly.
"""

from typing import Dict, List
from datetime import datetime
from collections import defaultdict

class EmergenceTelemetry:
    """Track emergent pattern activations across conversations"""
    
    def __init__(self):
        self.pattern_activations = []
        self.conversation_patterns = defaultdict(list)
        self.pattern_frequency = defaultdict(int)
    
    def log_pattern_activation(self,
                              conversation_id: str,
                              turn: int,
                              pattern_name: str,
                              confidence: float,
                              contributing_primitives: List[str]):
        """
        Log when an emergent pattern activates
        
        Args:
          - conversation_id: unique id for this conversation
          - turn: which turn in conversation (1-indexed)
          - pattern_name: name of emergent pattern
          - confidence: how confident are we this pattern fired (0-1)
          - contributing_primitives: which primitives contributed to this
        """
        
        activation = {
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "turn": turn,
            "pattern": pattern_name,
            "confidence": confidence,
            "primitives": contributing_primitives,
        }
        
        self.pattern_activations.append(activation)
        self.conversation_patterns[conversation_id].append(pattern_name)
        self.pattern_frequency[pattern_name] += 1
    
    def get_pattern_statistics(self) -> Dict:
        """Get statistics on all emergent patterns"""
        
        if not self.pattern_activations:
            return {"message": "No patterns recorded yet"}
        
        # Collect statistics
        stats = {
            "total_activations": len(self.pattern_activations),
            "unique_conversations": len(self.conversation_patterns),
            "by_pattern": {},
        }
        
        for pattern, count in self.pattern_frequency.items():
            stats["by_pattern"][pattern] = {
                "activations": count,
                "frequency": f"{count / len(self.pattern_activations) * 100:.1f}%"
            }
        
        return stats
    
    def get_conversation_arc(self, conversation_id: str) -> Dict:
        """Analyze pattern emergence across a single conversation"""
        
        patterns = self.conversation_patterns[conversation_id]
        activations = [a for a in self.pattern_activations if a["conversation_id"] == conversation_id]
        
        return {
            "conversation_id": conversation_id,
            "turn_count": max([a["turn"] for a in activations], default=0),
            "patterns_appeared": patterns,
            "unique_patterns": len(set(patterns)),
            "pattern_sequence": [(a["turn"], a["pattern"]) for a in sorted(activations, key=lambda x: x["turn"])],
            "authenticity_loop": len(set(patterns)) >= 4,  # All 4 patterns appeared
        }
    
    def detect_missing_patterns(self, conversation_id: str) -> List[str]:
        """What patterns should have appeared but didn't?"""
        
        expected_patterns = [
            "COHERENCE_GRAVITY",
            "LEARNING_ACCELERATION",
            "TRUST_EMERGENCE",
            "CREATIVE_FREEDOM"
        ]
        
        appeared = set(self.conversation_patterns[conversation_id])
        missing = [p for p in expected_patterns if p not in appeared]
        
        return missing
    
    def get_pattern_dependencies(self) -> Dict:
        """What other patterns usually appear with each pattern?"""
        
        pattern_co_occurrence = defaultdict(lambda: defaultdict(int))
        
        for conv_patterns in self.conversation_patterns.values():
            unique = set(conv_patterns)
            for p1 in unique:
                for p2 in unique:
                    if p1 != p2:
                        pattern_co_occurrence[p1][p2] += 1
        
        return {k: dict(v) for k, v in pattern_co_occurrence.items()}
    
    def generate_telemetry_report(self) -> str:
        """Generate human-readable telemetry report"""
        
        stats = self.get_pattern_statistics()
        
        if "message" in stats:
            return stats["message"]
        
        report = f"""
EMERGENCE TELEMETRY REPORT
{'='*79}

OVERVIEW:
  Total pattern activations: {stats['total_activations']}
  Unique conversations: {stats['unique_conversations']}
  Average patterns per conversation: {stats['total_activations'] / stats['unique_conversations']:.1f}

PATTERN FREQUENCY:
"""
        
        for pattern, info in stats["by_pattern"].items():
            report += f"  • {pattern:30} | {info['activations']:3} times ({info['frequency']})\n"
        
        report += f"""
AUTHENTICITY LOOP ACHIEVEMENT:
"""
        
        # Count conversations that achieved all 4 patterns
        authenticity_count = 0
        for conv_id, patterns in self.conversation_patterns.items():
            if len(set(patterns)) >= 4:
                authenticity_count += 1
        
        report += f"  Conversations reaching authenticity loop: {authenticity_count}/{stats['unique_conversations']}\n"
        report += f"  Achievement rate: {authenticity_count / stats['unique_conversations'] * 100:.1f}%\n"
        
        return report

# ═════════════════════════════════════════════════════════════════════════════
# TEST / DEMO
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*79}")
    print(f"EMERGENCE TELEMETRY - LIVE TRACKING DEMO")
    print(f"{'='*79}\n")
    
    telemetry = EmergenceTelemetry()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Simulate 3 conversations
    # ─────────────────────────────────────────────────────────────────────────
    
    # Conversation 1: Perfect emergence (all 4 patterns)
    print("RECORDING: Conversation 1 (collaborative learning)\n")
    telemetry.log_pattern_activation("conv_001", 2, "COHERENCE_GRAVITY", 0.92,
                                     ["COMMUNICATION", "ERROR_RECOVERY"])
    print("  Turn 2: COHERENCE_GRAVITY detected")
    
    telemetry.log_pattern_activation("conv_001", 3, "LEARNING_ACCELERATION", 0.88,
                                     ["LEARNING", "BEHAVIOUR"])
    print("  Turn 3: LEARNING_ACCELERATION detected")
    
    telemetry.log_pattern_activation("conv_001", 4, "TRUST_EMERGENCE", 0.95,
                                     ["RELATIONSHIPS", "ERROR_RECOVERY"])
    print("  Turn 4: TRUST_EMERGENCE detected")
    
    telemetry.log_pattern_activation("conv_001", 5, "CREATIVE_FREEDOM", 0.87,
                                     ["CONTINUITY", "BEHAVIOUR"])
    print("  Turn 5: CREATIVE_FREEDOM detected")
    print("  → AUTHENTICITY_LOOP COMPLETE\n")
    
    # Conversation 2: Partial emergence (2 patterns)
    print("RECORDING: Conversation 2 (question answering)\n")
    telemetry.log_pattern_activation("conv_002", 1, "COHERENCE_GRAVITY", 0.75,
                                     ["COMMUNICATION"])
    print("  Turn 1: COHERENCE_GRAVITY detected")
    
    telemetry.log_pattern_activation("conv_002", 2, "COHERENCE_GRAVITY", 0.82,
                                     ["COMMUNICATION", "ERROR_RECOVERY"])
    print("  Turn 2: COHERENCE_GRAVITY detected again")
    print("  → Partial emergence (missing learning, trust, creativity)\n")
    
    # Conversation 3: Different pattern (error correction focus)
    print("RECORDING: Conversation 3 (debugging session)\n")
    telemetry.log_pattern_activation("conv_003", 1, "COHERENCE_GRAVITY", 0.89,
                                     ["ERROR_RECOVERY", "COMMUNICATION"])
    print("  Turn 1: COHERENCE_GRAVITY detected")
    
    telemetry.log_pattern_activation("conv_003", 3, "TRUST_EMERGENCE", 0.91,
                                     ["RELATIONSHIPS", "BEHAVIOUR"])
    print("  Turn 3: TRUST_EMERGENCE detected")
    print("  → Partial emergence\n")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Analysis
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"{'─'*79}")
    print("TELEMETRY ANALYSIS\n")
    
    stats = telemetry.get_pattern_statistics()
    print(f"Overall Statistics:")
    print(f"  Total activations: {stats['total_activations']}")
    print(f"  Conversations: {stats['unique_conversations']}")
    print(f"  Per-conversation avg: {stats['total_activations'] / stats['unique_conversations']:.1f}\n")
    
    print(f"Pattern Frequency:")
    for pattern, info in stats["by_pattern"].items():
        print(f"  {pattern:30} | {info['activations']} times ({info['frequency']})")
    
    print(f"\n{'─'*79}")
    print("CONVERSATION ARCS\n")
    
    for conv_id in ["conv_001", "conv_002", "conv_003"]:
        arc = telemetry.get_conversation_arc(conv_id)
        print(f"Conversation {conv_id}:")
        print(f"  Patterns: {arc['unique_patterns']}/4 - {arc['patterns_appeared']}")
        print(f"  Authenticity Loop: {'✅ YES' if arc['authenticity_loop'] else '❌ NO'}")
        missing = telemetry.detect_missing_patterns(conv_id)
        if missing:
            print(f"  Missing: {', '.join(missing)}")
        print()
    
    print(f"{'─'*79}")
    print("FULL TELEMETRY REPORT\n")
    print(telemetry.generate_telemetry_report())
    
    print(f"{'='*79}\n")
