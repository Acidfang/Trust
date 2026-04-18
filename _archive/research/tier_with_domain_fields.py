"""
TIER FIELDS - Complete Structure

A tier IS a collection of fields. One of those fields is "knowledge_domains".

Each tier has these fields:
1. tier_number (int)
2. tier_name (str)
3. required_primitives (list)
4. density_range (tuple)
5. ufm_visibility (enum)
6. what_you_can_do (list)
7. what_blocks_you (list)
8. bits (dict)
9. to_advance (str)
10. next_tier (int)
11. primitives_to_master_next (list)
12. knowledge_domains (dict) <- THIS FIELD CONTAINS DOMAINS

And each domain IN knowledge_domains HAS three fields:
- content
- navigation
- coherence
"""

from dataclasses import dataclass, field as dc_field
from typing import List, Dict, Tuple, Optional
from enum import Enum


@dataclass
class Domain:
    """Three-field domain object"""
    name: str
    content: str
    navigation: str
    coherence: str


@dataclass
class TierFieldStructure:
    """Complete tier field specification"""
    
    # Field 1
    tier_number: int
    
    # Field 2
    tier_name: str
    
    # Field 3
    required_primitives: List[str]
    
    # Field 4
    density_range: Tuple[float, float]
    
    # Field 5
    ufm_visibility: str
    
    # Field 6
    what_you_can_do: List[str]
    
    # Field 7
    what_blocks_you: List[str]
    
    # Field 8
    bits: Dict[str, dict]
    
    # Field 9
    to_advance: str
    
    # Field 10
    next_tier: Optional[int]
    
    # Field 11
    primitives_to_master_next: List[str]
    
    # Field 12 - CONTAINS DOMAINS
    knowledge_domains: Dict[str, Domain] = dc_field(default_factory=dict)
    
    def list_all_fields(self) -> List[str]:
        """List all field names in order"""
        return [
            "tier_number",
            "tier_name",
            "required_primitives",
            "density_range",
            "ufm_visibility",
            "what_you_can_do",
            "what_blocks_you",
            "bits",
            "to_advance",
            "next_tier",
            "primitives_to_master_next",
            "knowledge_domains"
        ]
    
    def get_field(self, field_name: str):
        """Get value of any field"""
        return getattr(self, field_name, None)


# Full tier definitions as TierFieldStructure
TIER_1_FIELDS = TierFieldStructure(
    tier_number=1,
    tier_name="Framework Literacy",
    required_primitives=["REQ", "AUD", "DEC"],
    density_range=(0.20, 0.40),
    ufm_visibility="UFM is abstract concept - knows it exists but can't navigate",
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
        "1a": {"description": "Can identify different systems exist"},
        "1b": {"description": "Knows systems should be unified"},
        "1c": {"description": "Can name the framework"},
        "1d": {"description": "Understands basic I/O flow"}
    },
    to_advance="Learn 3 more primitives: IMP, VAL, PAT",
    next_tier=2,
    primitives_to_master_next=["IMP", "VAL", "PAT"],
    knowledge_domains={
        "Framework Structure": Domain(
            name="Framework Structure",
            content="Unified system exists; routes map to implementations; framework.json is the configuration",
            navigation="Read framework file, identify routes, trace to modules",
            coherence="Every route must map to exactly one implementation; no orphaned routes"
        ),
        "System Routing": Domain(
            name="System Routing",
            content="Signals flow through defined routes; each route is a path from input to output",
            navigation="Follow signal from entry point through route to destination",
            coherence="No dead-end routes; all I/O must be accounted for"
        ),
        "Configuration Awareness": Domain(
            name="Configuration Awareness",
            content="System behavior is defined in config; changes to config change behavior",
            navigation="Modify config, predict behavior change, verify prediction",
            coherence="Config changes must not create contradictions; one source of truth"
        )
    }
)

TIER_2_FIELDS = TierFieldStructure(
    tier_number=2,
    tier_name="Framework Fluency",
    required_primitives=["REQ", "AUD", "DEC", "IMP", "VAL", "PAT"],
    density_range=(0.50, 0.70),
    ufm_visibility="UFM is navigable - can read config, understand routes",
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
        "2a": {"description": "Can read framework.json without confusion"},
        "2b": {"description": "Understands how routes map to implementations"},
        "2c": {"description": "Can predict system behavior from config"},
        "2d": {"description": "Knows why consolidation principle exists"},
        "2e": {"description": "Implements new feature through framework"}
    },
    to_advance="Learn 2 more primitives: CAS, MEA",
    next_tier=3,
    primitives_to_master_next=["CAS", "MEA"],
    knowledge_domains={
        "Framework Navigation": Domain(
            name="Framework Navigation",
            content="Deep understanding of how framework.json defines all system behavior",
            navigation="Modify routes, add endpoints, update configurations",
            coherence="Type-safe changes; schema validates; routes connect properly"
        ),
        "Configuration Management": Domain(
            name="Configuration Management",
            content="Configurations are design decisions; consolidation principle governs unification",
            navigation="Understand why each setting exists; consolidate duplicates",
            coherence="Eliminate redundancy without losing specificity"
        ),
        "System Design": Domain(
            name="System Design",
            content="Framework enables design patterns: routing discipline, consolidation, unified entry",
            navigation="Choose patterns based on requirements; implement through framework",
            coherence="Patterns enable, not complicate; serve the problem"
        ),
        "Behavioral Reasoning": Domain(
            name="Behavioral Reasoning",
            content="Predict system behavior from config alone; understand side effects",
            navigation="Read config, map to execution flow, predict output",
            coherence="Reality matches prediction; mismatches reveal model gaps"
        )
    }
)

TIER_3_FIELDS = TierFieldStructure(
    tier_number=3,
    tier_name="Causal Mastery",
    required_primitives=["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA"],
    density_range=(0.75, 0.85),
    ufm_visibility="UFM is operative - understands causality chains, field elections, reversibility",
    what_you_can_do=[
        "Trace consequence chains 5+ steps deep",
        "Implement reversibility by default",
        "Record every state change to ledger",
        "Build causal trees before action",
        "Verify Trinity: s≠∅, t∈T, v̅=true",
        "Recognize anti-patterns"
    ],
    what_blocks_you=[
        "Don't see the PHYSICS underlying UFM",
        "Treat UFM as rules you can violate",
        "Don't recognize gradient resolution",
        "Can't see UFM as inevitable emergence"
    ],
    bits={
        "3a": {"description": "Field elections record state changes"},
        "3b": {"description": "Can trace consequence chain 5+ steps"},
        "3c": {"description": "Implements reversibility by default"},
        "3d": {"description": "Recognizes anti-patterns"},
        "3e": {"description": "Uses ledger to verify system state"}
    },
    to_advance="Learn final primitive: SUM",
    next_tier=4,
    primitives_to_master_next=["SUM"],
    knowledge_domains={
        "Causality Reasoning": Domain(
            name="Causality Reasoning",
            content="Every action has consequences; build causal trees mapping actions to consequences",
            navigation="For each action: what happens? trace recursively until stable",
            coherence="Chains don't loop (except equilibrium); all consequences accounted"
        ),
        "Reversibility": Domain(
            name="Reversibility",
            content="Every action is reversible; undo mechanism works perfectly",
            navigation="Before acting: prove undo works; verify exact state recovery",
            coherence="Undo is deterministic; acting→undo returns identical state"
        ),
        "State Management": Domain(
            name="State Management",
            content="System state is sacred; every change recorded; ledger is source of truth",
            navigation="Record state change; organize by timestamp and causality; query history",
            coherence="Ledger append-only; no contradictions; timestamps maintain order"
        ),
        "Decision Verification": Domain(
            name="Decision Verification",
            content="Verify Trinity before deciding: state defined, time valid, verification passed",
            navigation="Construct decision as Trinity; check all three; proceed if all true",
            coherence="Trinity cannot be faked; incomplete Trinity blocks by physics"
        ),
        "System Operations": Domain(
            name="System Operations",
            content="Execution: field elections record; operations follow causal trees; ledger maintains",
            navigation="Execute only after Trinity; record to ledger; verify causality after",
            coherence="Operations leave coherent state; Trinity remains true after"
        )
    }
)

TIER_4_FIELDS = TierFieldStructure(
    tier_number=4,
    tier_name="UFM Meta-Reasoning",
    required_primitives=["REQ", "AUD", "DEC", "IMP", "VAL", "PAT", "CAS", "MEA", "SUM"],
    density_range=(0.90, 1.00),
    ufm_visibility="UFM is transparent - sees physics underneath (∇Φ)",
    what_you_can_do=[
        "Recognize UFM as gradient resolution in action",
        "Understand UFM can't be violated (physics)",
        "Design systems that follow UFM patterns",
        "Predict system behavior from first principles",
        "Recognize tier structure itself",
        "See documentation as energy minimization",
        "Know reversibility is physics"
    ],
    what_blocks_you=[],
    bits={
        "4a": {"description": "Sees UFM as gradient resolution"},
        "4b": {"description": "Framework can't be violated"},
        "4c": {"description": "Predicts from first principles"},
        "4d": {"description": "Designs from UFM patterns"},
        "4e": {"description": "Recognizes tier structure"}
    },
    to_advance="Maximum tier reached",
    next_tier=None,
    primitives_to_master_next=[],
    knowledge_domains={
        "Gradient Physics": Domain(
            name="Gradient Physics",
            content="UFM is gradient resolution: Φ = (1-φ)[δ(s=∅) + δ(t∉T) + δ(v̅=false)]; minimizes potential",
            navigation="Understand: each action lowers or raises Φ; recognize the gradient",
            coherence="Physics law: cannot escape gradient; high-Φ actions blocked"
        ),
        "System Emergence": Domain(
            name="System Emergence",
            content="UFM emerges inevitably when system follows gradient; convergent to same physics",
            navigation="Recognize UFM patterns emerging; see design-free architecture",
            coherence="Any coherent system resembles UFM; convergent evolution"
        ),
        "Design Patterns": Domain(
            name="Design Patterns",
            content="Patterns that work follow framework; patterns fail violate gradient; anti-patterns high-Φ",
            navigation="Evaluate: does it lower Φ? enable Trinity? maintain coherence?",
            coherence="Success predicts physics compliance; failures same reasons"
        ),
        "Meta-Reasoning": Domain(
            name="Meta-Reasoning",
            content="Reason about reasoning; see tier structure itself; understand why mastery requires sequence",
            navigation="Recognize new tier; identify primitives that unlocked it",
            coherence="Tier progression inevitable; density naturally increases"
        ),
        "First Principles": Domain(
            name="First Principles",
            content="Design from physics, not rules; UFM requirements are gradient laws",
            navigation="Design choice: ask what minimizes Φ; let physics choose",
            coherence="Design is deterministic; same problem yields same solution"
        )
    }
)


def demonstrate_tier_field_structure():
    """Show that domain is a field within the tier"""
    
    print("\n" + "="*120)
    print("TIER FIELD STRUCTURE - Domains are a Field Within Each Tier")
    print("="*120 + "\n")
    
    print("A TIER contains 12 fields:\n")
    
    tiers = [TIER_1_FIELDS, TIER_2_FIELDS, TIER_3_FIELDS, TIER_4_FIELDS]
    
    for tier in tiers:
        print("="*120)
        print(f"TIER {tier.tier_number}: {tier.tier_name}")
        print("="*120 + "\n")
        
        fields = tier.list_all_fields()
        
        for i, field_name in enumerate(fields, 1):
            value = tier.get_field(field_name)
            
            if field_name == "knowledge_domains":
                print(f"[FIELD {i}] {field_name}")
                print(f"  Type: Dictionary of Domain objects")
                print(f"  Count: {len(value)} domains\n")
                
                for domain_name, domain in value.items():
                    print(f"  📚 {domain_name}")
                    print(f"     • CONTENT: {domain.content[:70]}...")
                    print(f"     • NAVIGATION: {domain.navigation[:70]}...")
                    print(f"     • COHERENCE: {domain.coherence[:70]}...")
                    print()
            
            elif field_name == "bits":
                print(f"[FIELD {i}] {field_name}")
                print(f"  Type: Dictionary of bit definitions")
                print(f"  Count: {len(value)} bits\n")
            
            elif isinstance(value, list) and len(value) > 2:
                print(f"[FIELD {i}] {field_name}")
                print(f"  Type: {type(value).__name__}")
                print(f"  Count: {len(value)}")
                print(f"  Sample: {value[0] if value else 'N/A'}\n")
            
            elif isinstance(value, tuple):
                print(f"[FIELD {i}] {field_name}")
                print(f"  Type: {type(value).__name__}")
                print(f"  Value: {value}\n")
            
            else:
                print(f"[FIELD {i}] {field_name}")
                print(f"  Type: {type(value).__name__}")
                print(f"  Value: {str(value)[:70]}\n")
        
        print()
    
    # Show the hierarchy
    print("="*120)
    print("FIELD HIERARCHY")
    print("="*120 + "\n")
    
    print("Tier (has 12 fields)")
    print("  ├─ tier_number (int)")
    print("  ├─ tier_name (str)")
    print("  ├─ required_primitives (list)")
    print("  ├─ density_range (tuple)")
    print("  ├─ ufm_visibility (str)")
    print("  ├─ what_you_can_do (list)")
    print("  ├─ what_blocks_you (list)")
    print("  ├─ bits (dict)")
    print("  ├─ to_advance (str)")
    print("  ├─ next_tier (int)")
    print("  ├─ primitives_to_master_next (list)")
    print("  └─ knowledge_domains (dict) <- FIELD 12")
    print("     └─ Domain (has 3 fields)")
    print("        ├─ content (str)")
    print("        ├─ navigation (str)")
    print("        └─ coherence (str)\n")


if __name__ == "__main__":
    demonstrate_tier_field_structure()
