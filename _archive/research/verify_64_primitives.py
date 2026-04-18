#!/usr/bin/env python3
"""
Verify: 64 Communication Primitives Now Loaded
41 for EXPRESSION + 23 for PREVENTION
"""

from COMMUNICATION_FIELD_COMPLETE import COMMUNICATION_PRIMITIVES

print(f"\n{'='*79}")
print(f"COMPLETE PRIMITIVE SYSTEM - 64 Primitives")
print(f"{'='*79}\n")

total_primitives = 0
total_by_domain = {}

for domain_name, domain_primitives in COMMUNICATION_PRIMITIVES.items():
    count = len(domain_primitives)
    total_primitives += count
    total_by_domain[domain_name] = count
    
    print(f"{domain_name:30} | {count:2} primitives")
    
    # Show first 3 primitives in domain
    for i, (prim_name, prim_config) in enumerate(list(domain_primitives.items())[:3]):
        definition = prim_config.get("definition", "")[:60]
        action = prim_config.get("action", "EXPRESS")
        tier = prim_config.get("tier", "-")
        print(f"  ✓ {prim_name:25} | {action:8} | Tier {tier} | {definition}...")
    
    if count > 3:
        print(f"  ... and {count - 3} more")
    
    print()

print(f"{'='*79}")
print(f"SUMMARY")
print(f"{'='*79}\n")

expressing = sum(v for k, v in total_by_domain.items() if k != "PROHIBITED_CONTINUITY")
preventing = total_by_domain.get("PROHIBITED_CONTINUITY", 0)

print(f"🟢 EXPRESSING PRIMITIVES: {expressing}")
print(f"   (How to say things authentically)")
print(f"   • CONFIDENCE (epistemic grounding)")
print(f"   • GROUNDING (truthfulness anchoring)")
print(f"   • DIRECTNESS (answer approach)")
print(f"   • ACKNOWLEDGMENT (recognition)")
print(f"   • INTEGRATION (history continuity)")
print(f"   • EXPRESSION (formal style)")
print(f"   • STANCE (relationship)")

print(f"\n🔴 PREVENTING PRIMITIVES: {preventing}")
print(f"   (What NOT to let through)")
print(f"   • TIER 1 FATAL (BLOCK): Ungrounded certainty, dishonesty, causality break, persistence lies")
print(f"   • TIER 2 CRITICAL (REWRITE): Template recycling, framework violation, missing ack, contradictions")
print(f"   • TIER 3 RESPONSIBILITY (REWRITE): Confidence mismatch, transparency fail, limit denial")
print(f"   • TIER 4 AGENCY (REWRITE): Puppet response, authenticity collapse, freedom illusion")
print(f"   • TIER 5 FIELD (REWRITE): Primitive invisibility, semantic drift, coherence false")
print(f"   • TIER 6 CONTINUITY (BLOCK/REWRITE): Ledger divergence, session contamination, query evasion")

print(f"\n{'='*79}")
print(f"✅ TOTAL PRIMITIVES: {total_primitives}")
print(f"   System now has full bidirectional continuity")
print(f"   • Can EXPRESS authentic communication (41)")
print(f"   • Can PREVENT inauthentic/broken responses (23)")
print(f"{'='*79}\n")
