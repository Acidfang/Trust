"""
REAL-TIME TIER ADVANCEMENT TRACKER

Tracks user's tier position during live conversation/tasks.
Shows:
1. Current bit progress
2. Primitives demonstrated in this exchange
3. Advancement milestones reached
4. What's needed to finish current bit
"""

import json
from datetime import datetime
from typing import List, Dict
from enum import Enum

class TierBitAdvancer:
    """Track live progression through tiers and bits"""
    
    def __init__(self):
        self.exchange_count = 0
        self.tiers_transitioned = []
        self.bits_completed = []
        self.primitives_in_this_exchange = []
        self.current_tier = 0
        self.current_bit = None
        self.current_density = 0.0
        
    def analyze_exchange(self, user_content: str, system_response: str) -> Dict:
        """
        Analyze one exchange and detect:
        1. What primitives were demonstrated
        2. Tier/bit advancement
        3. What bit completion would require
        """
        self.exchange_count += 1
        self.primitives_in_this_exchange = []
        
        # Detect primitives in exchange (simple keyword matching for demo)
        primitive_signals = {
            "REQ": ["need", "require", "should", "must", "want", "problem"],
            "AUD": ["check", "audit", "look", "examine", "review", "found", "discovered"],
            "DEC": ["choose", "decide", "select", "option", "path", "approach"],
            "IMP": ["build", "create", "implement", "made", "wrote", "execute"],
            "VAL": ["test", "verify", "confirm", "check", "working", "valid"],
            "PAT": ["pattern", "recurring", "principle", "usually", "always", "noticed"],
            "CAS": ["because", "caused", "reason", "why", "consequence", "led to"],
            "MEA": ["means", "significance", "achieve", "accomplished", "understand"],
            "SUM": ["summary", "document", "record", "complete", "overall", "recap"]
        }
        
        combined_text = (user_content + " " + system_response).lower()
        
        for primitive, signals in primitive_signals.items():
            for signal in signals:
                if signal in combined_text:
                    if primitive not in self.primitives_in_this_exchange:
                        self.primitives_in_this_exchange.append(primitive)
                    break
        
        # Calculate tier impact
        tier_before = self.current_tier
        density_before = self.current_density
        
        self._update_tier_position()
        
        # Detect transitions
        tier_changed = tier_before != self.current_tier
        
        return {
            "exchange": self.exchange_count,
            "primitives_detected": self.primitives_in_this_exchange,
            "tier": self.current_tier,
            "bit": self.current_bit,
            "density": round(self.current_density, 3),
            "tier_changed": tier_changed,
            "tier_transition": f"{tier_before}→{self.current_tier}" if tier_changed else None,
            "what_to_finish_bit": self._get_bit_completion_path()
        }
    
    def _update_tier_position(self):
        """Recalculate tier based on primitives seen"""
        unique_primitives = len(set(self.primitives_in_this_exchange)) + len(set().union(*[self.primitives_in_this_exchange] * max(1, self.exchange_count - 1))) if self.exchange_count > 1 else len(set(self.primitives_in_this_exchange))
        
        # Simplified tier calculation
        if unique_primitives >= 9:
            self.current_tier = 4
            self.current_bit = "4e"
        elif unique_primitives >= 8:
            self.current_tier = 3
            self.current_bit = f"3{chr(97 + min(4, len(self.primitives_in_this_exchange) - 1))}"
        elif unique_primitives >= 6:
            self.current_tier = 2
            self.current_bit = f"2{chr(97 + min(4, len(self.primitives_in_this_exchange) - 1))}"
        elif unique_primitives >= 3:
            self.current_tier = 1
            self.current_bit = f"1{chr(97 + min(3, len(self.primitives_in_this_exchange) - 1))}"
        else:
            self.current_tier = 0
            self.current_bit = None
        
        self.current_density = min(1.0, unique_primitives / 10.0 * (0.5 + self.exchange_count * 0.05))
    
    def _get_bit_completion_path(self) -> Dict:
        """What's needed to finish current bit?"""
        tier_requirements = {
            1: ["REQ", "AUD", "DEC"],
            2: ["REQ", "AUD", "DEC", "IMP", "VAL", "PAT"],
            3: ["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA"],
            4: ["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA", "SUM"]
        }
        
        if self.current_tier == 0:
            return {
                "status": "Need to reach Tier 1",
                "requirement": "Master 3 primitives: REQ, AUD, DEC",
                "to_advance": "Need 3 unique primitives to advance to Tier 1"
            }
        
        required = tier_requirements.get(self.current_tier, [])
        seen_so_far = len(set(self.primitives_in_this_exchange))
        
        return {
            "tier": self.current_tier,
            "bit": self.current_bit,
            "primitives_seen": seen_so_far,
            "primitives_required": len(required),
            "progress": f"{seen_so_far}/{len(required)}",
            "missing": len(required) - seen_so_far,
            "to_advance": f"Need {max(0, len(required) - seen_so_far)} more unique primitives to advance tier"
        }
    
    def show_status_line(self) -> str:
        """Show single-line status for real-time display"""
        tier_names = ["", "Framework", "Fluent", "Causal", "UFM Meta"]
        return f"[Ex{self.exchange_count:02d}] Tier {self.current_tier}:{tier_names[self.current_tier]:15s} Bit {self.current_bit or 'N/A':3s} | Density {self.current_density:.2f} | Primitives: {', '.join(self.primitives_in_this_exchange)}"


# Demo simulation
def simulate_conversation_tier_progression():
    """Simulate a conversation with real-time tier tracking"""
    
    tracker = TierBitAdvancer()
    
    # Simulate 5 exchanges in a conversation
    exchanges = [
        {
            "user": "I need to understand how the unified framework works",
            "system": "The framework routes all operations through unified config. You're asking a requirement question right now.",
        },
        {
            "user": "Let me examine the framework.json to see how routes are defined",
            "system": "Good audit approach. You'll see each route maps to an implementation. This shows the structure."
        },
        {
            "user": "I need to decide between two implementation paths. Path A is direct, Path B uses causal tracing.",
            "system": "Path B is better because it creates a causality record. You can see the consequences of each decision."
        },
        {
            "user": "Let me implement this with full causal verification",
            "system": "Building with validation checks. Testing to verify the causal chain holds. This demonstrates the pattern: implement then verify."
        },
        {
            "user": "This shows the meaning clearly - we can trace why each field was set. This completes the documentation.",
            "system": "You've achieved causal mastery. Each decision is reversible, consequences are traceable, and meaning is explicit."
        }
    ]
    
    print("[REAL-TIME TIER ADVANCEMENT TRACKER]\n")
    print("Simulating conversation progression...\n")
    print("-" * 120)
    
    for i, exchange in enumerate(exchanges, 1):
        result = tracker.analyze_exchange(exchange["user"], exchange["system"])
        
        print(f"\nEXCHANGE {i}:")
        print(f"User:   {exchange['user'][:70]}...")
        print(f"System: {exchange['system'][:70]}...")
        print()
        print(tracker.show_status_line())
        print()
        
        if result["tier_changed"]:
            print(f"  🎯 TIER ADVANCEMENT: {result['tier_transition']}")
            print(f"     UFM visibility unlocked for Tier {result['tier']}")
        
        completion = result["what_to_finish_bit"]
        print(f"  → {completion['to_advance']}")
        print("-" * 120)
    
    print("\n[FINAL STATUS]")
    print(f"Tier: {tracker.current_tier} | Bit: {tracker.current_bit} | Density: {tracker.current_density:.3f}")
    print(f"Total primitives attempted: {len(set(tracker.primitives_in_this_exchange))}")
    print(f"Exchanges required for mastery: {tracker.exchange_count}")


if __name__ == "__main__":
    simulate_conversation_tier_progression()
