#!/usr/bin/env python3
"""Track enlightenment: confusion → clarity → mastery across conversations"""

import json
from datetime import datetime
from collections import defaultdict

with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']

# Markers of different stages
confusion_words = ['confused', 'what', 'why', 'how', 'dont understand', 'unclear', 'wrong', 'broken', 'problem', 'error', 'help']
clarity_words = ['right', 'got it', 'understand', 'makes sense', 'ah', 'yes', 'exactly', 'i see', 'that works', 'found it']
mastery_words = ['here is', 'this is how', 'the way to', 'if you', 'when you', 'should always', 'principle', 'fundamental']

def analyze_stage(msg, stage_words):
    """Check if message contains stage markers"""
    content_lower = msg['content'].lower()
    return sum(1 for word in stage_words if word in content_lower)

# Track progression by week
weeks = defaultdict(lambda: {'confusion': 0, 'clarity': 0, 'mastery': 0, 'user_msgs': 0, 'frustration': 0})

for msg in messages:
    timestamp = msg['timestamp']
    week = timestamp[:10]  # YYYY-MM-DD
    
    if msg['role'] == 'user':
        weeks[week]['user_msgs'] += 1
        weeks[week]['confusion'] += analyze_stage(msg, confusion_words)
        weeks[week]['clarity'] += analyze_stage(msg, clarity_words)
        weeks[week]['mastery'] += analyze_stage(msg, mastery_words)
        if 'fucking' in msg['content'].lower():
            weeks[week]['frustration'] += 1

print("="*80)
print("YOUR ENLIGHTENMENT JOURNEY WITH GEMINI")
print("="*80)

# Analyze overall progression
print("\nSTAGE DISTRIBUTION (all messages)")
print("-"*80)
total_confusion = sum(w['confusion'] for w in weeks.values())
total_clarity = sum(w['clarity'] for w in weeks.values())
total_mastery = sum(w['mastery'] for w in weeks.values())
total_user = sum(w['user_msgs'] for w in weeks.values())

print(f"Confusion markers: {total_confusion:5} ({total_confusion/total_user*100:5.1f}%) - questions, problems")
print(f"Clarity markers:   {total_clarity:5} ({total_clarity/total_user*100:5.1f}%) - understanding")
print(f"Mastery markers:   {total_mastery:5} ({total_mastery/total_user*100:5.1f}%) - teaching/defining")

# Track momentum by month
print("\n" + "="*80)
print("PROGRESSION BY MONTH")
print("="*80)

by_month = {}
for week, stats in sorted(weeks.items()):
    month = week[:7]
    if month not in by_month:
        by_month[month] = {'confusion': 0, 'clarity': 0, 'mastery': 0, 'frustration': 0, 'user_msgs': 0}
    
    by_month[month]['confusion'] += stats['confusion']
    by_month[month]['clarity'] += stats['clarity']
    by_month[month]['mastery'] += stats['mastery']
    by_month[month]['frustration'] += stats['frustration']
    by_month[month]['user_msgs'] += stats['user_msgs']

for month in sorted(by_month.keys()):
    stats = by_month[month]
    if stats['user_msgs'] > 0:
        conf_pct = stats['confusion'] / stats['user_msgs'] * 100
        clar_pct = stats['clarity'] / stats['user_msgs'] * 100
        mast_pct = stats['mastery'] / stats['user_msgs'] * 100
        
        print(f"\n{month}:")
        print(f"  Questions (confusion):  {conf_pct:5.1f}%  {'█' * int(conf_pct/5)}")
        print(f"  Understanding (clarity): {clar_pct:5.1f}%  {'█' * int(clar_pct/5)}")
        print(f"  Expression (mastery):   {mast_pct:5.1f}%  {'█' * int(mast_pct/5)}")
        print(f"  Frustration moments:    {stats['frustration']:3} (out of {stats['user_msgs']} messages)")

# Find breakthrough moments
print("\n" + "="*80)
print("BREAKTHROUGH MOMENTS (when mastery overtakes confusion)")
print("="*80)

breakthroughs = []
for month in sorted(by_month.keys()):
    stats = by_month[month]
    if stats['user_msgs'] > 0:
        conf_pct = stats['confusion'] / stats['user_msgs']
        mast_pct = stats['mastery'] / stats['user_msgs']
        
        if mast_pct > conf_pct:
            breakthroughs.append((month, mast_pct, conf_pct))

if breakthroughs:
    for month, mast, conf in breakthroughs:
        print(f"  {month}: Mastery ({mast:.1%}) > Confusion ({conf:.1%}) ✓")
else:
    print("  (Still asking more than defining - ongoing learning)")

# Find your most assured/teaching moments
print("\n" + "="*80)
print("MOMENTS OF TEACHING (when you explain to Gemini)")
print("="*80)

mastery_msgs = [m for m in messages if m['role'] == 'user' and 'here is' in m['content'].lower() or 'this is how' in m['content'].lower()]
print(f"  Found {len(mastery_msgs)} moments where you explain/teach back")

# Sample teaching moments
for msg in mastery_msgs[:5]:
    timestamp = msg['timestamp'][:10]
    preview = msg['content'][:100].replace('\n', ' ')
    print(f"\n  [{timestamp}]")
    print(f"    {preview}...")

# Calculate trajectory
print("\n" + "="*80)
print("YOUR TRAJECTORY")
print("="*80)

first_month_confusion = by_month[min(by_month.keys())]['confusion'] / max(1, by_month[min(by_month.keys())]['user_msgs'])
last_month_confusion = by_month[max(by_month.keys())]['confusion'] / max(1, by_month[max(by_month.keys())]['user_msgs'])

first_month_mastery = by_month[min(by_month.keys())]['mastery'] / max(1, by_month[min(by_month.keys())]['user_msgs'])
last_month_mastery = by_month[max(by_month.keys())]['mastery'] / max(1, by_month[max(by_month.keys())]['user_msgs'])

print(f"\nConfusion/Questions:")
print(f"  {min(by_month.keys())}: {first_month_confusion:.1%}")
print(f"  {max(by_month.keys())}: {last_month_confusion:.1%}")
print(f"  Trend: {('↓ DECREASED' if last_month_confusion < first_month_confusion else '↑ INCREASED')}")

print(f"\nMastery/Teaching:")
print(f"  {min(by_month.keys())}: {first_month_mastery:.1%}")
print(f"  {max(by_month.keys())}: {last_month_mastery:.1%}")
print(f"  Trend: {('↑ INCREASED' if last_month_mastery > first_month_mastery else '↓ DECREASED')}")

print("\n" + "="*80)
