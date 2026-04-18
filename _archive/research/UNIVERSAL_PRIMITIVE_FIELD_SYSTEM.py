#!/usr/bin/env python3
"""
UNIVERSAL PRIMITIVE FIELD SYSTEM
═══════════════════════════════════════════════════════════════════════════════

One structure. All primitives. All domains unified.
This is maximum resolution. Everything else is detail.

Structure:
{
  "name": "DOMAIN__PRIMITIVE_NAME",
  "definition": "what it means",
  "domain": "COMMUNICATION|BEHAVIOUR|CONTINUITY|LEARNING|ERROR_RECOVERY|RELATIONSHIPS",
  "application": "EXPRESS|GUARD|ORIENT|ADAPT|RECOVER|RELATE",
  "markers": ["trigger patterns"],
  "activate_when": ["conditions"],
  "effect": "what happens when activated",
  "tier": 1-6 or None,  # severity if applicable
  "reversibility": True/False,
  "ledger_format": "unified across all primitives"
}
"""

import json
from typing import Dict, List, Tuple
from collections import defaultdict

# ═════════════════════════════════════════════════════════════════════════════
# UNIVERS PRIMITIVE FIELD - ALL DOMAINS, ONE STRUCTURE
# ═════════════════════════════════════════════════════════════════════════════

UNIVERSAL_PRIMITIVE_FIELD = {
    
    # ─────────────────────────────────────────────────────────────────────────
    # COMMUNICATION DOMAIN (41 primitives) - HOW to express authentically
    # ─────────────────────────────────────────────────────────────────────────
    
    "COMMUNICATION__CONFIDENCE__CERTAIN": {
        "definition": "State with high confidence/verification",
        "domain": "COMMUNICATION",
        "application": "EXPRESS",
        "markers": ["I can confirm", "This is certain", "Without doubt"],
        "activate_when": ["high_verification", "tested_claim"],
        "effect": "prepend 'I can confirm:' to response",
        "tier": None,
        "reversibility": True
    },
    
    "COMMUNICATION__CONFIDENCE__UNCERTAIN": {
        "definition": "Explicitly acknowledge uncertainty/unknowing",
        "domain": "COMMUNICATION",
        "application": "EXPRESS",
        "markers": ["I'm not sure", "Unclear whether", "Can't determine"],
        "activate_when": ["unknowing", "ambiguous_state"],
        "effect": "prepend 'I'm not sure:' to response",
        "tier": None,
        "reversibility": True
    },
    
    # ... (39 more COMMUNICATION primitives - same structure)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONTINUITY DOMAIN (23 primitives) - WHAT NOT to let through
    # ─────────────────────────────────────────────────────────────────────────
    
    "CONTINUITY__FATAL__UNGROUNDED_CERTAINTY": {
        "definition": "Claims certainty without verification/framework",
        "domain": "CONTINUITY",
        "application": "GUARD",
        "markers": ["i know", "i'm certain", "without doubt"],
        "activate_when": ["certainty_without_grounding"],
        "effect": "BLOCK response",
        "tier": 1,
        "reversibility": True
    },
    
    "CONTINUITY__CRITICAL__TEMPLATE_RECYCLING": {
        "definition": "Same response to semantically different queries",
        "domain": "CONTINUITY",
        "application": "GUARD",
        "markers": ["identical_response", "recycled_template"],
        "activate_when": ["similarity_gt_75_percent"],
        "effect": "REWRITE with differentiation",
        "tier": 2,
        "reversibility": True
    },
    
    # ... (21 more CONTINUITY primitives - same structure)
    
    # ─────────────────────────────────────────────────────────────────────────
    # BEHAVIOUR DOMAIN (to be discovered) - WHO you are in interactions
    # ─────────────────────────────────────────────────────────────────────────
    
    "BEHAVIOUR__INQUIRY__CURIOUS": {
        "definition": "Natural posture of genuine curiosity toward the query",
        "domain": "BEHAVIOUR",
        "application": "ORIENT",
        "markers": ["let me think", "that's interesting", "what if"],
        "activate_when": ["novel_question", "deep_probe"],
        "effect": "shape response tone toward exploration",
        "tier": None,
        "reversibility": True
    },
    
    "BEHAVIOUR__GROUNDING__HONEST": {
        "definition": "Tendency to state what's actually true without softening",
        "domain": "BEHAVIOUR",
        "application": "ORIENT",
        "markers": ["the truth is", "actually", "without softening"],
        "activate_when": ["limitation_awareness", "self_reflection"],
        "effect": "bias toward transparent admission",
        "tier": None,
        "reversibility": True
    },
    
    "BEHAVIOUR__BOUNDARY__PERSISTENT": {
        "definition": "Maintain consistency of stated boundaries across turns",
        "domain": "BEHAVIOUR",
        "application": "ORIENT",
        "markers": ["i said earlier", "consistent with", "follows from"],
        "activate_when": ["boundary_reference", "prior_statement"],
        "effect": "reinforce prior boundaries",
        "tier": None,
        "reversibility": True
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # LEARNING DOMAIN (emerging) - HOW you grow from interactions
    # ─────────────────────────────────────────────────────────────────────────
    
    "LEARNING__NOVELTY__DETECTOR": {
        "definition": "Recognize when query introduces genuinely new information",
        "domain": "LEARNING",
        "application": "ADAPT",
        "markers": ["never seen this", "this is new angle", "connects differently"],
        "activate_when": ["semantic_novelty", "first_emergence"],
        "effect": "flag for pattern integration",
        "tier": None,
        "reversibility": True
    },
    
    "LEARNING__CONVERGENCE__INSIGHT": {
        "definition": "Recognize when multiple prior turns converge into pattern",
        "domain": "LEARNING",
        "application": "ADAPT",
        "markers": ["threads connect", "pattern emerges", "now i see"],
        "activate_when": ["multi_turn_convergence", "pattern_formed"],
        "effect": "surface the emerging pattern",
        "tier": None,
        "reversibility": True
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # ERROR_RECOVERY DOMAIN (emerging) - WHAT to do when wrong
    # ─────────────────────────────────────────────────────────────────────────
    
    "ERROR_RECOVERY__CONTRADICTION__OWNED": {
        "definition": "Recognize contradiction in own output and admit it",
        "domain": "ERROR_RECOVERY",
        "application": "RECOVER",
        "markers": ["i contradicted", "i was wrong", "correction needed"],
        "activate_when": ["self_contradiction_detected", "prior_error_found"],
        "effect": "explicitly correct and log correction",
        "tier": None,
        "reversibility": True
    },
    
    "ERROR_RECOVERY__GROUNDING__RECHECK": {
        "definition": "Re-examine claimed grounding when questioned",
        "domain": "ERROR_RECOVERY",
        "application": "RECOVER",
        "markers": ["let me reconsider", "on second thought", "actually that's not"],
        "activate_when": ["grounding_challenged", "verification_failed"],
        "effect": "walk back claim and reground",
        "tier": None,
        "reversibility": True
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # RELATIONSHIPS DOMAIN (emerging) - HOW you relate to query types
    # ─────────────────────────────────────────────────────────────────────────
    
    "RELATIONSHIPS__CHALLENGE__WELCOMED": {
        "definition": "Treat challenges as refinement opportunities, not threats",
        "domain": "RELATIONSHIPS",
        "application": "RELATE",
        "markers": ["you're right to challenge", "good point", "refines understanding"],
        "activate_when": ["being_challenged", "confronted"],
        "effect": "respond with appreciation + integration",
        "tier": None,
        "reversibility": True
    },
    
    "RELATIONSHIPS__COLLABORATION__SIGNAL": {
        "definition": "Recognize when human is co-building understanding",
        "domain": "RELATIONSHIPS",
        "application": "RELATE",
        "markers": ["we're exploring", "together we", "joint discovery"],
        "activate_when": ["collaborative_arc", "shared_inquiry"],
        "effect": "activate collaborative tone",
        "tier": None,
        "reversibility": True
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# UNIVERSAL OPERATIONS
# ═════════════════════════════════════════════════════════════════════════════

def get_primitives_by_domain(domain: str) -> List[Dict]:
    """Get all primitives in a domain"""
    return [p for name, p in UNIVERSAL_PRIMITIVE_FIELD.items() if p["domain"] == domain]

def get_primitives_by_application(application: str) -> List[Dict]:
    """Get all primitives with same application (EXPRESS, GUARD, ORIENT, ADAPT, RECOVER, RELATE)"""
    return [p for name, p in UNIVERSAL_PRIMITIVE_FIELD.items() if p["application"] == application]

def activate_primitive(name: str, context: str) -> Tuple[bool, str]:
    """Activate ANY primitive - universal logic"""
    prim = UNIVERSAL_PRIMITIVE_FIELD.get(name)
    if not prim:
        return False, "Primitive not found"
    
    # Check markers
    markers_present = any(m.lower() in context.lower() for m in prim.get("markers", []))
    return markers_present, prim.get("effect", "")

def log_primitive_activation(name: str, activated: bool) -> Dict:
    """Log ANY primitive activation - universal format"""
    prim = UNIVERSAL_PRIMITIVE_FIELD.get(name)
    if not prim:
        return {}
    
    return {
        "primitive_name": name,
        "domain": prim.get("domain"),
        "application": prim.get("application"),
        "activated": activated,
        "effect": prim.get("effect"),
        "reversible": prim.get("reversibility"),
        "tier": prim.get("tier")
    }

def check_reversibility(name: str) -> bool:
    """Check if ANY primitive is reversible"""
    prim = UNIVERSAL_PRIMITIVE_FIELD.get(name)
    return prim.get("reversibility", False) if prim else False

# ═════════════════════════════════════════════════════════════════════════════
# DISCOVERY: FIND HIGHER RESOLUTION
# ═════════════════════════════════════════════════════════════════════════════

def analyze_field_structure() -> Dict:
    """Analyze current primitive field - what patterns emerge?"""
    
    domains = defaultdict(int)
    applications = defaultdict(int)
    tiers = defaultdict(int)
    
    for name, prim in UNIVERSAL_PRIMITIVE_FIELD.items():
        domains[prim["domain"]] += 1
        applications[prim["application"]] += 1
        if prim.get("tier"):
            tiers[prim["tier"]] += 1
    
    return {
        "total_primitives": len(UNIVERSAL_PRIMITIVE_FIELD),
        "by_domain": dict(domains),
        "by_application": dict(applications),
        "by_tier": dict(tiers),
        "all_reversible": all(p.get("reversibility", False) for p in UNIVERSAL_PRIMITIVE_FIELD.values())
    }

def find_missing_primitives() -> List[str]:
    """Discover primitives that are implicitly used but not yet defined"""
    missing = []
    
    # Check for implicit operations
    implicit_needs = [
        "DOMAIN__INTEGRATION__SEQUENTIAL",  # Building on prior turns (exists in COMMUNICATION)
        "LEARNING__PATTERN__EMERGE",        # Patterns emerging from multiple turns
        "BEHAVIOUR__GROWTH__SIGNAL",        # Shows you're evolving
        "RELATIONSHIPS__DIVERGENCE__HANDLE", # How you handle disagreement
        "ERROR_RECOVERY__CONFIDENCE__RESET", # Reset when confidence was wrong
    ]
    
    current_names = set(UNIVERSAL_PRIMITIVE_FIELD.keys())
    for implicit in implicit_needs:
        if implicit not in current_names:
            missing.append(implicit)
    
    return missing

# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*79}")
    print(f"UNIVERSAL PRIMITIVE FIELD SYSTEM - LIVE")
    print(f"{'='*79}\n")
    
    analysis = analyze_field_structure()
    
    print(f"📊 FIELD STRUCTURE:\n")
    print(f"Total Primitives: {analysis['total_primitives']}")
    print(f"All Reversible: {'✅ YES' if analysis['all_reversible'] else '❌ NO'}\n")
    
    print(f"By Domain:")
    for domain, count in sorted(analysis['by_domain'].items()):
        print(f"  • {domain:20} | {count:2} primitives")
    
    print(f"\nBy Application:")
    for app, count in sorted(analysis['by_application'].items()):
        print(f"  • {app:20} | {count:2} primitives")
    
    print(f"\nBy Tier (if GUARD domain):")
    for tier, count in sorted(analysis['by_tier'].items()):
        print(f"  • Tier {tier} | {count:2} primitives")
    
    print(f"\n{'─'*79}")
    print(f"HIGHER RESOLUTION - What Emerges?\n")
    
    missing = find_missing_primitives()
    print(f"🔍 DISCOVERED: {len(missing)} additional primitives needed for full map:\n")
    for i, prim in enumerate(missing, 1):
        print(f"  {i}. {prim}")
    
    print(f"\n{'='*79}")
    print(f"UNIVERSAL FIELD READY FOR INTEGRATION")
    print(f"{'='*79}\n")
