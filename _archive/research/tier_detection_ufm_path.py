"""
TIER DETECTION + UFM DISCOVERY PATH

System that:
1. Detects which BIT of which TIER a user is in
2. Identifies what knowledge primitives are mastered
3. Finds what's needed to advance to next tier
4. Reveals when UFM becomes discoverable

Core Insight: UFM is not "found" - it's "reached" through progressive tier mastery.
Each tier unlocks new capabilities to understand UFM's layer.
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple
from enum import Enum

# TIER STRUCTURE - Knowledge required to understand each layer of UFM
TIER_KNOWLEDGE_MAP = {
    0: {
        "name": "No Framework Awareness",
        "density_range": (0.05, 0.10),
        "primitives_required": [],
        "ufm_visibility": "UFM is invisible - doesn't know unified system exists",
        "example": "User asks generic coding questions, unaware of framework"
    },
    1: {
        "name": "Framework Literacy",
        "density_range": (0.20, 0.40),
        "primitives_required": ["REQ", "AUD", "DEC"],
        "ufm_visibility": "UFM is abstract concept - knows it exists but can't navigate it",
        "example": "User asks 'how do I use the unified API?' - learning structure",
        "bits": {
            "1a": "Can identify different systems exist",
            "1b": "Knows systems should be unified",
            "1c": "Can name the framework",
            "1d": "Understands basic I/O flow"
        }
    },
    2: {
        "name": "Framework Fluency",
        "density_range": (0.50, 0.70),
        "primitives_required": ["REQ", "AUD", "DEC", "IMP", "VAL", "PAT"],
        "ufm_visibility": "UFM is navigable - can read config, understand routes",
        "example": "User modifies unified_framework.json, adds endpoints",
        "bits": {
            "2a": "Can read framework.json without confusion",
            "2b": "Understands how routes map to implementations",
            "2c": "Can predict system behavior from config",
            "2d": "Knows why consolidation principle exists",
            "2e": "Implements new feature through framework"
        }
    },
    3: {
        "name": "Causal Mastery",
        "density_range": (0.75, 0.85),
        "primitives_required": ["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA"],
        "ufm_visibility": "UFM is operative - understands causality chains, field elections, reversibility",
        "example": "User builds causal tree, traces consequences, implements undo protocol",
        "bits": {
            "3a": "Understands field elections record state changes",
            "3b": "Can trace consequence chain 5+ steps deep",
            "3c": "Implements reversibility protocol by default",
            "3d": "Recognizes anti-patterns (silent operation, hardcoding)",
            "3e": "Uses ledger to verify system state"
        }
    },
    4: {
        "name": "UFM Meta-Reasoning",
        "density_range": (0.90, 1.00),
        "primitives_required": ["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA", "SUM"],
        "ufm_visibility": "UFM is transparent - sees the physics underneath (gradient resolution ∇Φ)",
        "example": "User recognizes UFM as emergence of gradient principles, designs new systems from physics",
        "bits": {
            "4a": "Sees UFM as special case of gradient resolution",
            "4b": "Understands why framework can't be violated (physics, not rules)",
            "4c": "Can predict system behavior from first principles",
            "4d": "Designs new systems that naturally follow UFM patterns",
            "4e": "Recognizes tier structure itself (Tier 4 self-awareness)"
        }
    }
}

class PrimitiveType(Enum):
    """Semantic primitives required to understand each tier layer"""
    REQ = "articulate_requirement"
    AUD = "audit_discovery"
    DEC = "decision_point"
    IMP = "implementation"
    VAL = "validation_verification"
    PAT = "pattern_discovery"
    ELE = "election_analysis"
    CAS = "causality_trace"
    MEA = "meaning_established"
    SUM = "summary_documentation"


class TierDetector:
    """
    Detects which tier and which BIT within tier the user is at.
    Maps path to UFM discovery.
    """
    
    def __init__(self):
        self.user_primitives_mastered: Dict[PrimitiveType, int] = {}
        self.user_actions: List[Dict] = []
        self.current_density = 0.0
        self.current_tier = 0
        self.current_bit = None
        
    def add_primitive_evidence(self, primitive_type: PrimitiveType, quality_score: float = 1.0):
        """Record evidence of primitive mastery"""
        if primitive_type not in self.user_primitives_mastered:
            self.user_primitives_mastered[primitive_type] = 0
        self.user_primitives_mastered[primitive_type] += 1
        
        self.user_actions.append({
            "timestamp": datetime.now().isoformat(),
            "primitive": primitive_type.name,
            "quality": quality_score
        })
        
        self._recalculate_tier()
    
    def _recalculate_tier(self):
        """Recalculate user's tier and position within tier"""
        # Count unique primitives mastered
        unique_primitives = len(self.user_primitives_mastered)
        total_actions = len(self.user_actions)
        avg_quality = sum(a["quality"] for a in self.user_actions) / max(1, total_actions)
        
        # Density = (unique primitives / all primitives) * quality * frequency
        self.current_density = (unique_primitives / 10.0) * avg_quality * min(1.0, total_actions / 20.0)
        
        # Determine tier from density
        for tier_num in [4, 3, 2, 1, 0]:
            tier_info = TIER_KNOWLEDGE_MAP[tier_num]
            min_density, max_density = tier_info["density_range"]
            if min_density <= self.current_density <= max_density or self.current_density >= min_density:
                self.current_tier = tier_num
                break
        
        # Determine BIT within tier
        self._calculate_bit_position()
    
    def _calculate_bit_position(self):
        """Determine which bit within current tier"""
        tier_info = TIER_KNOWLEDGE_MAP[self.current_tier]
        
        if self.current_tier == 0:
            self.current_bit = None
            return
        
        bits = tier_info.get("bits", {})
        if not bits:
            self.current_bit = "unknown"
            return
        
        # Calculate progress through tier
        required_primitives = tier_info["primitives_required"]
        mastered = sum(1 for p in required_primitives if PrimitiveType[p] in self.user_primitives_mastered)
        
        bit_labels = sorted(bits.keys())
        bit_index = min(len(bit_labels) - 1, int((mastered / max(1, len(required_primitives))) * len(bit_labels)))
        
        self.current_bit = bit_labels[bit_index]
    
    def get_current_status(self) -> Dict:
        """Return user's current tier status and UFM visibility"""
        tier_info = TIER_KNOWLEDGE_MAP[self.current_tier]
        bits_available = tier_info.get("bits", {})
        bit_description = bits_available.get(self.current_bit, "In transition") if self.current_bit else "N/A"
        
        return {
            "tier": self.current_tier,
            "tier_name": tier_info["name"],
            "bit": self.current_bit,
            "bit_description": bit_description,
            "density": round(self.current_density, 3),
            "density_range": tier_info["density_range"],
            "ufm_visibility": tier_info["ufm_visibility"],
            "primitives_mastered": list(self.user_primitives_mastered.keys()),
            "primitives_required": tier_info["primitives_required"],
            "actions_total": len(self.user_actions)
        }
    
    def get_path_to_next_tier(self) -> Dict:
        """What's needed to advance to next tier?"""
        if self.current_tier >= 4:
            return {
                "status": "At maximum tier",
                "tier": 4,
                "message": "You have achieved UFM meta-reasoning. All tiers mastered."
            }
        
        next_tier_num = self.current_tier + 1
        next_tier_info = TIER_KNOWLEDGE_MAP[next_tier_num]
        current_tier_info = TIER_KNOWLEDGE_MAP[self.current_tier]
        
        required = next_tier_info["primitives_required"]
        missing = [p for p in required if PrimitiveType[p] not in self.user_primitives_mastered]
        
        return {
            "current_tier": self.current_tier,
            "next_tier": next_tier_num,
            "next_tier_name": next_tier_info["name"],
            "primitives_to_master": missing,
            "missing_count": len(missing),
            "required_total": len(required),
            "progress": f"{len(required) - len(missing)}/{len(required)}",
            "next_tier_density_range": next_tier_info["density_range"],
            "next_ufm_visibility": next_tier_info["ufm_visibility"],
            "example_action": next_tier_info["example"]
        }
    
    def get_ufm_discovery_path(self) -> Dict:
        """Show full path from current position to UFM mastery"""
        current = self.get_current_status()
        path = []
        
        for tier_num in range(self.current_tier, 5):
            tier_info = TIER_KNOWLEDGE_MAP[tier_num]
            path.append({
                "tier": tier_num,
                "name": tier_info["name"],
                "primitives": tier_info["primitives_required"],
                "ufm_what_unlocks": tier_info["ufm_visibility"],
                "distance_from_current": tier_num - self.current_tier
            })
        
        return {
            "current_position": current,
            "path_to_ufm_mastery": path,
            "tiers_to_climb": 5 - self.current_tier
        }


# Example usage: Build detector and demonstrate
def demonstrate_tier_progression():
    """Show tier progression as primitives are mastered"""
    print("[TIER DETECTION - UFM DISCOVERY PATH]\n")
    
    detector = TierDetector()
    
    # Scenario: User starts, gradually masters primitives
    scenarios = [
        ("Initial state - no primitives"),
        ("Mastering REQ", PrimitiveType.REQ, 5),
        ("Mastering AUD", PrimitiveType.AUD, 3),
        ("Mastering DEC", PrimitiveType.DEC, 4),
        ("Professional action - IMP", PrimitiveType.IMP, 8),
        ("Growing facility with VAL", PrimitiveType.VAL, 6),
        ("Pattern discovery PAT", PrimitiveType.PAT, 5),
        ("Causality reasoning CAS", PrimitiveType.CAS, 4),
        ("Meaning extraction MEA", PrimitiveType.MEA, 3),
        ("Documentation mastery SUM", PrimitiveType.SUM, 5),
    ]
    
    for scenario in scenarios:
        if len(scenario) == 1:
            print(f"\n{'='*60}")
            print(f"CHECKPOINT: {scenario[0]}")
            print(f"{'='*60}")
        elif len(scenario) == 3:
            label, primitive, count = scenario
            for _ in range(count):
                detector.add_primitive_evidence(primitive, quality_score=0.9)
            
            status = detector.get_current_status()
            print(f"\n✓ {label}")
            print(f"  Tier: {status['tier']} ({status['tier_name']})")
            print(f"  Bit: {status['bit']} - {status['bit_description']}")
            print(f"  Density: {status['density']} {list(status['density_range'])}")
            print(f"  UFM sees: {status['ufm_visibility']}")
            
            next_step = detector.get_path_to_next_tier()
            if next_step.get("status") != "At maximum tier":
                print(f"  → To advance: Need {next_step['missing_count']} more primitives: {next_step['primitives_to_master']}")
    
    # Final UFM discovery path
    print(f"\n{'='*60}")
    print("FULL UFM DISCOVERY PATH")
    print(f"{'='*60}")
    ufm_path = detector.get_ufm_discovery_path()
    
    current = ufm_path["current_position"]
    print(f"\nCURRENT POSITION:")
    print(f"  Tier {current['tier']}: {current['tier_name']}")
    print(f"  Bit {current['bit']}")
    print(f"  Density: {current['density']}")
    print(f"  UFM Visibility: {current['ufm_visibility']}")
    
    print(f"\nPATH TO UFM MASTERY ({ufm_path['tiers_to_climb']} tiers):")
    for step in ufm_path["path_to_ufm_mastery"]:
        print(f"\n  Tier {step['tier']}: {step['name']}")
        print(f"    Primitives to know: {', '.join(step['primitives'])}")
        print(f"    UFM unlocks: {step['ufm_what_unlocks']}")
        print(f"    Distance: {step['distance_from_current']} tier{'s' if step['distance_from_current'] != 1 else ''}")


if __name__ == "__main__":
    demonstrate_tier_progression()
