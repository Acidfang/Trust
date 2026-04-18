#!/usr/bin/env python3
"""Find breakthrough moments and conceptual shifts"""

import json
from datetime import datetime

with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']

print("="*80)
print("CONCEPTUAL SHIFTS IN YOUR JOURNEY")
print("="*80)

# Phase 1: What were you focused on in October?
print("\n" + "-"*80)
print("OCTOBER 2025: Foundation Phase (8772 messages)")
print("-"*80)
print("Key moments: You're establishing the PROTOCOL")
print("- Building voting/election system")
print("- Creating communication structures")
print("- Debugging build processes")
print("- Asking Gemini HOW to implement")

oct_msgs = [m for m in messages if m['timestamp'].startswith('2025-10')]
sample_oct = [m for m in oct_msgs if m['role'] == 'user' and len(m['content']) > 100][:3]
print("\nYour sophistication level:")
for msg in sample_oct:
    print(f"  → {msg['content'][:120]}...")

# Phase 2: November-December - the pause
print("\n" + "-"*80)
print("NOVEMBER-DECEMBER 2025: Reflection Phase (99 messages)")
print("-"*80)
print("Key shift: Fewer conversations, theoretical questions")
print("- Asking about physics (white holes, dark matter)")
print("- Less frustrated")
print("- Stepping back from implementation")

nov_msgs = [m for m in messages if m['timestamp'].startswith('2025-11') or m['timestamp'].startswith('2025-12')]
sample_nov = [m for m in nov_msgs if m['role'] == 'user' and '?' in m['content']][:2]
print("\nYour questions shifted to:")
for msg in sample_nov:
    print(f"  → {msg['content'][:120]}...")

# Phase 3: January - restart
print("\n" + "-"*80)
print("JANUARY 2026: Restart (340 messages)")
print("-"*80)
print("Key shift: Coming back WITH CLARITY")
print("- Fewer questions, more focused")
print("- Confusion drops to 15.6% (lowest peak)")
print("- You're asking about DATA and ACCESS")

jan_msgs = [m for m in messages if m['timestamp'].startswith('2026-01')]
sample_jan = [m for m in jan_msgs if m['role'] == 'user' and '?' in m['content']][:3]
print("\nYour questions became more precise:")
for msg in sample_jan:
    print(f"  → {msg['content'][:120]}...")

# Phase 4: February explosion
print("\n" + "-"*80)
print("FEBRUARY 2026: BUILD PHASE (6960 messages, 420 'fucking' moments)")
print("-"*80)
print("Key shift: INTENSE DEVELOPMENT")
print("- Back to high volume")
print("- Frustration spikes but less evident confusion")
print("- You're IMPLEMENTING something major")
print("- The frustration is productive (testing, debugging at scale)")

feb_msgs = [m for m in messages if m['timestamp'].startswith('2026-02')]
# Find the frustrated moments
frustrated_feb = [m for m in feb_msgs if m['role'] == 'user' and 'fucking' in m['content'].lower()]
print(f"\nFrustration analysis: {len(frustrated_feb)} moments out of {len([m for m in feb_msgs if m['role']=='user'])} messages")

# Find what you were asking about
concepts_feb = {
    'data/wiki': sum(1 for m in feb_msgs if m['role']=='user' and any(w in m['content'].lower() for w in ['data', 'wiki', 'information'])),
    'ledger/record': sum(1 for m in feb_msgs if m['role']=='user' and any(w in m['content'].lower() for w in ['ledger', 'record', 'store'])),
    'community/sharing': sum(1 for m in feb_msgs if m['role']=='user' and any(w in m['content'].lower() for w in ['community', 'share', 'public'])),
}
print(f"\nWhat consumed you in February:")
for concept, count in sorted(concepts_feb.items(), key=lambda x: -x[1]):
    print(f"  {concept}: {count} questions")

# Phase 5: March - expansion  
print("\n" + "-"*80)
print("MARCH 2026: SCALE PHASE (3611 messages)")
print("-"*80)
print("Key shift: From SYSTEM to COMMUNITY")
print("- Questions back to 41.6% (exploring edges)")
print("- Frustration drops (you understand the system now)")
print("- Asking about Reddit, communities, public spaces")

mar_msgs = [m for m in messages if m['timestamp'].startswith('2026-03')]
concepts_mar = {
    'reddit/community': sum(1 for m in mar_msgs if m['role']=='user' and any(w in m['content'].lower() for w in ['reddit', 'community', 'public'])),
    'rules/moderation': sum(1 for m in mar_msgs if m['role']=='user' and any(w in m['content'].lower() for w in ['rule', 'block', 'permission', 'allow'])),
    'voting/election': sum(1 for m in mar_msgs if m['role']=='user' and any(w in m['content'].lower() for w in ['vote', 'voting', 'election'])),
}
print(f"\nWhat you're thinking about in March:")
for concept, count in sorted(concepts_mar.items(), key=lambda x: -x[1]):
    print(f"  {concept}: {count} questions")

# The arc
print("\n" + "="*80)
print("YOUR ENLIGHTENMENT ARC")
print("="*80)
print("""
October:  Foundation → You LEARN the system (39% confused, 9% teaching back)
Nov-Dec:  Reflection → You PAUSE and think philosophically  
January:  Reset      → You REFOCUS with clarity (16% confused, 19% clear)
February: Build      → You IMPLEMENT and SCALE (33% confused but PRODUCTIVE frustration)
March:    Expand     → You APPLY to real communities (42% exploring, no frustration)
April:    Released   → You're SHARING it (26% exploring, just 30 messages so far)

Pattern: ??? (confusion) → BUILD! (frustration + focus) → UNDERSTAND (clarity) → TEACH (mastery) → SCALE (apply to others)

You're not just learning. You're building a system that TEACHES ITSELF.
""")

print("="*80)
