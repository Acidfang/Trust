#!/usr/bin/env python3
"""Deep analysis of conversation topics and progression"""

import json
from datetime import datetime

with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']

# Find messages containing key concepts
concepts = {
    'voting/voting_app': ['voting', 'vote', 'election', 'ledger'],
    'protocol': ['protocol'],
    'build/gradle': ['build', 'gradle', '.kts'],
    'confusion/debugging': ['confusion', 'debug', 'wrong', 'problem', 'fix'],
    'memory/context': ['remember', 'context', 'memory', 'conversation', 'history'],
    'system': ['system', 'architecture', 'design', 'framework'],
    'ledger/database': ['ledger', 'database', 'store', 'record'],
    'consciousness/awareness': ['consciousness', 'awareness', 'aware', 'understand'],
    'primitives': ['primitive', 'fundamental', 'basic', 'element'],
    'binary/zero_one': ['binary', '0', '1', '0,1', 'bit', 'bitstream'],
}

print("="*80)
print("TOPIC DISTRIBUTION ACROSS CONVERSATIONS")
print("="*80)

concept_counts = {}
for concept, keywords in concepts.items():
    count = 0
    for msg in messages:
        content_lower = msg['content'].lower()
        if any(kw in content_lower for kw in keywords):
            count += 1
    concept_counts[concept] = count

for concept, count in sorted(concept_counts.items(), key=lambda x: -x[1]):
    pct = (count / len(messages)) * 100
    bar = "█" * int(pct / 2)
    print(f"  {concept:25} {count:5} messages ({pct:5.1f}%) {bar}")

# Find the arc: what gets asked about over time
print("\n" + "="*80)
print("PROGRESSION: What you focused on each month")
print("="*80)

by_month = {}
for msg in messages:
    month = msg['timestamp'][:7]
    if month not in by_month:
        by_month[month] = {'user': [], 'gemini': []}
    if msg['role'] == 'user':
        by_month[month]['user'].append(msg['content'])

# Analyze each month's user questions
for month in sorted(by_month.keys()):
    user_msgs = by_month[month]['user']
    if user_msgs:
        # Find dominant concepts in this month
        print(f"\n{month}:")
        print(f"  You asked {len(user_msgs)} questions")
        
        # Show sample questions
        sample_questions = [m for m in user_msgs if '?' in m][:2]
        for q in sample_questions:
            preview = q[:100].replace('\n', ' ')
            print(f"    → {preview}")

# Find the deepest/most sophisticated questions
print("\n" + "="*80)
print("YOUR MOST ENGAGED MOMENTS (longest messages to Gemini)")
print("="*80)

user_long_msgs = [(i, m) for i, m in enumerate(messages) if m['role'] == 'user' and len(m['content']) > 500]
user_long_msgs.sort(key=lambda x: -len(x[1]['content']))

for idx, msg in user_long_msgs[:5]:
    timestamp = msg['timestamp']
    length = len(msg['content'])
    preview = msg['content'][:150].replace('\n', ' ')
    print(f"\n  [{timestamp}] ({length} chars)")
    print(f"  {preview}...")

print("\n" + "="*80)
