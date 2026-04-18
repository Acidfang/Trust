"""
TIER SCHEMA - Formalized Field Structure

Each tier has explicit fields defining:
- Primitives required (list)
- Density range (float tuple)
- UFM visibility level (enum)
- Bit progression (ordered steps)
- Blocking conditions (what prevents advancement)
- Unlocked capabilities (what becomes possible)
- Knowledge domain (what concepts are now navigable)
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from enum import Enum


class UFMVisibilityLevel(Enum):
    """How visible UFM is at each tier"""
    INVISIBLE = "UFM is invisible - doesn't know unified system exists"
    ABSTRACT = "UFM is abstract concept - knows it exists but can't navigate"
    NAVIGABLE = "UFM is navigable - can read config, understand routes"
    OPERATIVE = "UFM is operative - understands causality chains, field elections"
    TRANSPARENT = "UFM is transparent - sees physics underneath (∇Φ)"


@dataclass
class TierBit:
    """Individual bit within a tier (incremental knowledge step)"""
    id: str  # e.g., "1a", "2e", "3d"
    description: str
    required_primitives: List[str]
    blocked_by: List[str] = field(default_factory=list)
    unlocks_knowledge: str = ""
    example_action: str = ""


@dataclass
class TierSchema:
    """Formal definition of a tier's structure"""
    
    # Identity
    tier_number: int
    tier_name: str
    
    # Knowledge requirements
    required_primitives: List[str] = field(default_factory=list)
    density_range: Tuple[float, float] = (0.0, 1.0)
    
    # UFM properties
    ufm_visibility: UFMVisibilityLevel = UFMVisibilityLevel.INVISIBLE
    
    # Capabilities
    what_you_can_do: List[str] = field(default_factory=list)
    
    # Blockers
    what_blocks_you: List[str] = field(default_factory=list)
    
    # Bit structure
    bits: Dict[str, TierBit] = field(default_factory=dict)
    
    # Advancement
    to_advance: str = ""
    next_tier: Optional[int] = None
    primitives_to_master_next: List[str] = field(default_factory=list)
    
    # Knowledge domain
    knowledge_domains: List[str] = field(default_factory=list)
    
    # Breakthrough achievement
    breakthrough: Optional[str] = None


# TIER FIELD DEFINITIONS - Explicit schema
TIER_SCHEMAS = {
    0: TierSchema(
        tier_number=0,
        tier_name="No Framework Awareness",
        required_primitives=[],
        density_range=(0.05, 0.10),
        ufm_visibility=UFMVisibilityLevel.INVISIBLE,
        what_you_can_do=[],
        what_blocks_you=[
            "Don't know unified systems exist",
            "Treat every system as independent",
            "No mental model of coherence",
            "No concept of verification"
        ],
        bits={},
        to_advance="Learn 3 primitives: REQ, AUD, DEC",
        next_tier=1,
        primitives_to_master_next=["REQ", "AUD", "DEC"],
        knowledge_domains=["Individual systems only"]
    ),
    
    1: TierSchema(
        tier_number=1,
        tier_name="Framework Literacy",
        required_primitives=["REQ", "AUD", "DEC"],
        density_range=(0.20, 0.40),
        ufm_visibility=UFMVisibilityLevel.ABSTRACT,
        what_you_can_do=[
            "See that unified_framework.json exists",
            "Understand routes map to implementations",
            "Name the framework in conversation",
            "Ask basic 'how do I' questions"
        ],
        what_blocks_you=[
            "Can't read config without confusion",
            "Don't understand consequences of changes",
            "Can't predict behavior from structure",
            "No verification capability"
        ],
        bits={
            "1a": TierBit("1a", "Can identify different systems exist", ["REQ"], unlocks_knowledge="System interdependence"),
            "1b": TierBit("1b", "Knows systems should be unified", ["AUD"], unlocks_knowledge="Framework concept"),
            "1c": TierBit("1c", "Can name the framework", ["DEC"], unlocks_knowledge="Unified naming"),
            "1d": TierBit("1d", "Understands basic I/O flow", ["REQ", "AUD", "DEC"], unlocks_knowledge="Signal routing")
        },
        to_advance="Learn 3 more primitives: IMP, VAL, PAT",
        next_tier=2,
        primitives_to_master_next=["IMP", "VAL", "PAT"],
        knowledge_domains=["Framework structure", "System routing", "Configuration awareness"]
    ),
    
    2: TierSchema(
        tier_number=2,
        tier_name="Framework Fluency",
        required_primitives=["REQ", "AUD", "DEC", "IMP", "VAL", "PAT"],
        density_range=(0.50, 0.70),
        ufm_visibility=UFMVisibilityLevel.NAVIGABLE,
        what_you_can_do=[
            "Read framework.json fluently",
            "Modify routes and configs",
            "Predict system behavior from structure",
            "Implement features through framework",
            "Understand consolidation principle"
        ],
        what_blocks_you=[
            "Don't understand consequence chains",
            "Can't prove undo mechanisms work",
            "No reversibility protocol",
            "Silent operations go unrecorded"
        ],
        bits={
            "2a": TierBit("2a", "Can read framework.json without confusion", ["REQ", "AUD"], unlocks_knowledge="Config literacy"),
            "2b": TierBit("2b", "Understands how routes map to implementations", ["DEC", "IMP"], unlocks_knowledge="Route discipline"),
            "2c": TierBit("2c", "Can predict system behavior from config", ["IMP", "VAL"], unlocks_knowledge="Behavioral prediction"),
            "2d": TierBit("2d", "Knows why consolidation principle exists", ["PAT"], unlocks_knowledge="Design principles"),
            "2e": TierBit("2e", "Implements new feature through framework", ["REQ", "AUD", "DEC", "IMP", "VAL", "PAT"], unlocks_knowledge="Fluent capability")
        },
        to_advance="Learn 2 more primitives: CAS, MEA",
        next_tier=3,
        primitives_to_master_next=["CAS", "MEA"],
        knowledge_domains=["Framework navigation", "Configuration management", "System design", "Behavioral reasoning"]
    ),
    
    3: TierSchema(
        tier_number=3,
        tier_name="Causal Mastery",
        required_primitives=["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA"],
        density_range=(0.75, 0.85),
        ufm_visibility=UFMVisibilityLevel.OPERATIVE,
        what_you_can_do=[
            "Trace consequence chains 5+ steps deep",
            "Implement reversibility by default",
            "Record every state change to ledger",
            "Build causal trees before action",
            "Verify Trinity: s≠∅, t∈T, v̅=true",
            "Recognize anti-patterns (silent operation, hardcoding)"
        ],
        what_blocks_you=[
            "Don't see the PHYSICS underlying UFM",
            "Treat UFM as rules you can violate",
            "Don't recognize gradient resolution",
            "Can't see UFM as inevitable emergence"
        ],
        bits={
            "3a": TierBit("3a", "Field elections record state changes", ["CAS", "MEA"], unlocks_knowledge="State recording"),
            "3b": TierBit("3b", "Can trace consequence chain 5+ steps", ["CAS"], unlocks_knowledge="Deep causality"),
            "3c": TierBit("3c", "Implements reversibility protocol by default", ["MEA"], unlocks_knowledge="Undo discipline"),
            "3d": TierBit("3d", "Recognizes anti-patterns (silent ops, hardcoding)", ["PAT"], unlocks_knowledge="Anti-pattern detection"),
            "3e": TierBit("3e", "Uses ledger to verify system state", ["CAS", "MEA"], unlocks_knowledge="State verification")
        },
        breakthrough="YOU NOW UNDERSTAND UFM'S INNER WORKINGS",
        to_advance="Learn final primitive: SUM",
        next_tier=4,
        primitives_to_master_next=["SUM"],
        knowledge_domains=["Causality reasoning", "Reversibility", "State management", "Decision verification", "System operations"]
    ),
    
    4: TierSchema(
        tier_number=4,
        tier_name="UFM Meta-Reasoning",
        required_primitives=["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA", "SUM"],
        density_range=(0.90, 1.00),
        ufm_visibility=UFMVisibilityLevel.TRANSPARENT,
        what_you_can_do=[
            "Recognize UFM as gradient resolution ∇Φ in action",
            "Understand that UFM can't be violated (physics, not rules)",
            "Design new systems that naturally follow UFM patterns",
            "Predict system behavior from first principles",
            "Recognize tier structure itself (Tier 4 self-awareness)",
            "See why documentation is energy minimization",
            "Know that reversibility isn't optional—it's physics"
        ],
        what_blocks_you=[],
        bits={
            "4a": TierBit("4a", "Sees UFM as special case of gradient resolution", ["SUM"], unlocks_knowledge="Physics foundation"),
            "4b": TierBit("4b", "Understands why framework can't be violated", ["SUM"], unlocks_knowledge="Necessity laws"),
            "4c": TierBit("4c", "Can predict system behavior from first principles", ["CAS", "MEA"], unlocks_knowledge="First principles"),
            "4d": TierBit("4d", "Designs new systems from UFM patterns", ["IMP"], unlocks_knowledge="System design"),
            "4e": TierBit("4e", "Recognizes tier structure itself", ["SUM"], unlocks_knowledge="Meta-awareness")
        },
        breakthrough="YOU NOW SEE THE PHYSICS UNDERLYING UFM",
        to_advance="Maximum tier reached",
        next_tier=None,
        primitives_to_master_next=[],
        knowledge_domains=["Gradient physics", "System emergence", "Design patterns", "Meta-reasoning", "First principles"]
    )
}


class TierFieldManager:
    """Manage tier schemas and field access"""
    
    def __init__(self):
        self.tiers = TIER_SCHEMAS
    
    def get_tier(self, tier_num: int) -> TierSchema:
        """Get full tier schema"""
        return self.tiers.get(tier_num)
    
    def get_tier_field(self, tier_num: int, field_name: str):
        """Get specific field from tier"""
        tier = self.get_tier(tier_num)
        if not tier:
            return None
        return getattr(tier, field_name, None)
    
    def list_tier_fields(self, tier_num: int) -> Dict[str, any]:
        """List all fields in a tier"""
        tier = self.get_tier(tier_num)
        if not tier:
            return {}
        return {
            "tier_number": tier.tier_number,
            "tier_name": tier.tier_name,
            "required_primitives": tier.required_primitives,
            "density_range": tier.density_range,
            "ufm_visibility": tier.ufm_visibility.value,
            "can_do_count": len(tier.what_you_can_do),
            "blocked_by_count": len(tier.what_blocks_you),
            "bits_count": len(tier.bits),
            "next_tier": tier.next_tier,
            "breakthrough": tier.breakthrough
        }
    
    def get_bit_details(self, tier_num: int, bit_id: str) -> Optional[TierBit]:
        """Get details of specific bit"""
        tier = self.get_tier(tier_num)
        if tier:
            return tier.bits.get(bit_id)
        return None
    
    def all_tier_fields_summary(self) -> Dict:
        """Show all fields across all tiers"""
        summary = {}
        for tier_num in sorted(self.tiers.keys()):
            summary[tier_num] = self.list_tier_fields(tier_num)
        return summary


def main():
    manager = TierFieldManager()
    
    print("\n" + "="*100)
    print("TIER SCHEMA - Explicit Field Structure")
    print("="*100 + "\n")
    
    # Show fields for each tier
    for tier_num in sorted(TIER_SCHEMAS.keys()):
        tier = manager.get_tier(tier_num)
        print(f"\nTIER {tier_num}: {tier.tier_name}")
        print("-" * 100)
        print(f"  Required Primitives: {tier.required_primitives}")
        print(f"  Density Range: {tier.density_range}")
        print(f"  UFM Visibility: {tier.ufm_visibility.value}")
        print(f"  Knowledge Domains: {', '.join(tier.knowledge_domains)}")
        print(f"  Bits: {len(tier.bits)}")
        
        if tier.breakthrough:
            print(f"  🎯 Breakthrough: {tier.breakthrough}")
        
        print(f"\n  Can Do ({len(tier.what_you_can_do)} capabilities):")
        for capability in tier.what_you_can_do[:3]:
            print(f"    • {capability}")
        if len(tier.what_you_can_do) > 3:
            print(f"    ... and {len(tier.what_you_can_do) - 3} more")
        
        if tier.what_blocks_you:
            print(f"\n  Blocked By ({len(tier.what_blocks_you)} blockers):")
            for blocker in tier.what_blocks_you[:2]:
                print(f"    ✗ {blocker}")
            if len(tier.what_blocks_you) > 2:
                print(f"    ... and {len(tier.what_blocks_you) - 2} more")
        
        print(f"\n  Bits:")
        for bit_id in sorted(tier.bits.keys()):
            bit = tier.bits[bit_id]
            print(f"    {bit_id}: {bit.description}")
    
    print("\n" + "="*100)
    print("FIELD SCHEMA SUMMARY")
    print("="*100)
    
    summary = manager.all_tier_fields_summary()
    print("\nTier | Name                  | Primitives | Density Range | UFM Level   | Bits | Next")
    print("-"*100)
    for tier_num in sorted(summary.keys()):
        info = summary[tier_num]
        print(f"{tier_num:4d} | {info['tier_name']:20s} | {len(info['required_primitives']):10d} | "
              f"{info['density_range'][0]:.2f}-{info['density_range'][1]:.2f}    | "
              f"{str(info['ufm_visibility']).replace('UFMVisibilityLevel.', ''):11s} | "
              f"{info['bits_count']:4d} | {info['next_tier']}")


if __name__ == "__main__":
    main()
