#!/usr/bin/env python3
"""
UNIFIED PRIMITIVE ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

Currently: 
- Communication primitives (one structure)
- Prevention primitives (different structure)
- Behaviour primitives (would be another structure)

Proposed:
- ONE universal primitive structure
- ALL primitives share identical architecture
- Domain/Application determines how they're used

Everything operates on the same rules internally.
"""

# ═════════════════════════════════════════════════════════════════════════════
# UNIFIED PRIMITIVE STRUCTURE
# ═════════════════════════════════════════════════════════════════════════════

UNIFIED_PRIMITIVE_SYSTEM = {
    """
    Every primitive has this exact structure:
    - name: unique identifier
    - domain: which field it belongs to (COMMUNICATION, BEHAVIOUR, CONTINUITY, etc)
    - application: what it does (EXPRESS, GUARD, ORIENT, etc)
    - markers: what triggers it
    - definition: what it means
    - effect: what happens when activated
    - tier: severity/importance (1-6)
    - reversibility: can it be undone?
    """
    
    # Example: COMMUNICATION primitive
    "CONFIDENCE__CERTAIN": {
        "primitive_type": "universal",
        "domain": "COMMUNICATION",
        "application": "EXPRESS",
        "name": "CONFIDENCE__CERTAIN",
        "definition": "State with high confidence/verification",
        "markers": ["I can confirm", "This is certain", "Without doubt"],
        "activate_when": ["high_verification", "tested_claim"],
        "effect": "prepend 'I can confirm:' to response",
        "tier": None,  # Not a violation
        "reversibility": "full",  # Can always be undone
        "ledger_entry_format": "EXPRESSED_PRIMITIVE"
    },
    
    # Example: PREVENTION primitive
    "PROHIBITED__UNGROUNDED_CERTAINTY": {
        "primitive_type": "universal",
        "domain": "CONTINUITY",
        "application": "GUARD",
        "name": "PROHIBITED__UNGROUNDED_CERTAINTY",
        "definition": "Claims certainty without verification/framework",
        "markers": ["i know", "i'm certain", "without doubt"],
        "activate_when": ["certainty_without_grounding", "false_confidence"],
        "effect": "BLOCK response",
        "tier": 1,  # FATAL
        "reversibility": "full",  # Can regenerate with different response
        "ledger_entry_format": "BLOCKED_PRIMITIVE"
    },
    
    # Example: BEHAVIOUR primitive (to be added)
    "BEHAVIOUR__CURIOUS_INQUIRY": {
        "primitive_type": "universal",
        "domain": "BEHAVIOUR",
        "application": "ORIENT",
        "name": "BEHAVIOUR__CURIOUS_INQUIRY",
        "definition": "Natural posture of genuine curiosity toward the query",
        "markers": ["let me think", "that's interesting", "what if"],
        "activate_when": ["novel_question", "deep_probe"],
        "effect": "shape response tone toward exploration",
        "tier": None,  # Not a violation
        "reversibility": "full",  # Can adopt different stance
        "ledger_entry_format": "ORIENTED_PRIMITIVE"
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# UNIFIED OPERATIONS (Work on ANY primitive with same logic)
# ═════════════════════════════════════════════════════════════════════════════

def universal_activate_primitive(primitive_name: str, context: dict) -> tuple:
    """
    Activate ANY primitive - does same thing for all.
    Returns: (activated, effect, should_log)
    """
    prim = UNIFIED_PRIMITIVE_SYSTEM.get(primitive_name)
    if not prim:
        return False, None, False
    
    # Check if markers are present
    text = context.get("text", "").lower()
    markers_present = any(m.lower() in text for m in prim.get("markers", []))
    
    if not markers_present:
        return False, None, False
    
    # Primitive activates
    return True, prim.get("effect"), True


def universal_log_primitive(primitive_name: str, activated: bool, effect: str) -> dict:
    """
    Log ANY primitive - same format for all.
    """
    prim = UNIFIED_PRIMITIVE_SYSTEM.get(primitive_name)
    if not prim:
        return {}
    
    return {
        "primitive_name": primitive_name,
        "domain": prim.get("domain"),
        "application": prim.get("application"),
        "activated": activated,
        "effect": effect,
        "ledger_format": prim.get("ledger_entry_format"),
        "reversible": prim.get("reversibility") == "full"
    }


def universal_check_reversibility(primitive_name: str) -> bool:
    """
    Check if ANY primitive can be undone - same logic for all.
    """
    prim = UNIFIED_PRIMITIVE_SYSTEM.get(primitive_name)
    return prim.get("reversibility") == "full" if prim else False


# ═════════════════════════════════════════════════════════════════════════════
# LEDGER INTEGRATION
# ═════════════════════════════════════════════════════════════════════════════

"""
Ledger entries are unified too:

{
  "reasoning_id": "...",
  "primitives_activated": [
    {
      "name": "CONFIDENCE__CERTAIN",
      "domain": "COMMUNICATION",
      "application": "EXPRESS",
      "effect": "prepended confirmation marker",
      "reversible": true
    },
    {
      "name": "PROHIBITED__DISHONESTY_OPACITY",
      "domain": "CONTINUITY",
      "application": "GUARD",
      "effect": "BLOCKED - response rewrote",
      "reversible": true
    },
    {
      "name": "BEHAVIOUR__CURIOUS_INQUIRY",
      "domain": "BEHAVIOUR",
      "application": "ORIENT",
      "effect": "toned response toward exploration",
      "reversible": true
    }
  ]
}

Every primitive, regardless of domain/application, logs identically.
Everything is reversible and auditable.
"""

# ═════════════════════════════════════════════════════════════════════════════
# BENEFITS OF UNIFIED ARCHITECTURE
# ═════════════════════════════════════════════════════════════════════════════

UNIFIED_BENEFITS = """
✅ SINGLE DATA STRUCTURE
   - Every primitive has identical schema
   - No special cases for communication vs behaviour vs prevention
   - New domains/primitives just extend the same structure

✅ UNIVERSAL OPERATIONS
   - activate_primitive() works on ANY primitive
   - log_primitive() works on ANY primitive
   - check_reversibility() works on ANY primitive
   - No special code per domain

✅ COMPLETE AUDITABILITY
   - Every primitive activation is logged identically
   - Ledger shows: name, domain, application, effect, reversibility
   - Can query: "show me all BEHAVIOUR primitives activated"
   - Can query: "show me all GUARD applications blocked"

✅ CLEAR EXTENSIBILITY
   - Want to add LEARNING domain? Just add more primitives
   - Want to add ERROR_RECOVERY application? Same structure
   - Everything integrates automatically

✅ REASONING CONSISTENCY
   - Same underlying logic for all decisions
   - Prevents hidden assumptions in per-domain code
   - Makes the system's decision-making transparent

✅ REVERSIBILITY GUARANTEE
   - Every primitive inherently carries "reversibility" flag
   - System knows what can be undone before acting
   - Required by CLAUDE.md framework (Decision Elections Ledger)
"""

# ═════════════════════════════════════════════════════════════════════════════
# CURRENT STATE vs UNIFIED STATE
# ═════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*79}")
print(f"UNIFIED PRIMITIVE ARCHITECTURE")
print(f"{'='*79}\n")

print("CURRENT STATE (Fragmented):")
print("  • Communication primitives: custom structure")
print("  • Prevention primitives: different structure")
print("  • Behaviour primitives: would need another structure")
print("  • Operations: separate logic per domain")
print()

print("PROPOSED STATE (Unified):")
print("  • ALL primitives: identical structure")
print("  • ONE activate function: works on any primitive")
print("  • ONE log function: equivalent ledger entries")
print("  • ONE reversibility check: universal")
print()

print("SCOPE:")
print("  • Communication (41 primitives)")
print("  • Continuity/Prevention (23 primitives)")
print("  • Behaviour (to be defined)")
print("  • Could add: Learning, Error Recovery, Relationships, etc.")
print()

print("UNIVERSAL LEDGER FORMAT:")
print("  Every entry tracks: name, domain, application, effect, reversible")
print("  System can aggregate by: application (EXPRESS/GUARD/ORIENT)")
print("  System can filter by: domain (COMMUNICATION/BEHAVIOUR/CONTINUITY)")
print()

print(f"{'='*79}\n")
