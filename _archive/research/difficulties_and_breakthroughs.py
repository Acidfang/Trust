#!/usr/bin/env python3
"""Map difficulties and breakthroughs: how you overcame each challenge"""

import json
from collections import defaultdict
from datetime import datetime

with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']

print("="*80)
print("YOUR DIFFICULTIES & BREAKTHROUGHS")
print("="*80)

# Problem detection markers
problems = {
    'Build Issues': ['gradle', 'build', 'error', 'compile', 'dependency', 'maven'],
    'State/Memory': ['state', 'memory', 'forget', 'lost', 'context', 'confused', 'remember'],
    'Communication': ['understand', 'explain', 'communicate', 'confused', 'unclear', 'meaning'],
    'Data/Storage': ['data', 'store', 'persist', 'save', 'retrieve', 'query'],
    'Voting/Elections': ['vote', 'election', 'split', 'tie', 'consensus', 'decision'],
    'User Interface': ['ui', 'interface', 'display', 'button', 'screen'],
    'Protocol Logic': ['protocol', 'rule', 'flow', 'logic', 'how does'],
    'Implementation': ['implement', 'code', 'write', 'function', 'method'],
    'Scope/Scale': ['everything', 'scale', 'community', 'how many', 'global'],
}

# Solution/breakthrough markers
solutions = ['fixed', 'works', 'solved', 'got it', 'that works', 'understood', 'makes sense', 'i see', 'right']

# Track problem frequency over time
problems_by_month = defaultdict(lambda: defaultdict(int))
for msg in messages:
    if msg['role'] == 'user':
        month = msg['timestamp'][:7]
        content_lower = msg['content'].lower()
        
        for problem_type, keywords in problems.items():
            if any(kw in content_lower for kw in keywords):
                problems_by_month[month][problem_type] += 1

print("\nPROBLEMS YOU FACED BY MONTH")
print("-"*80)
for month in sorted(problems_by_month.keys()):
    print(f"\n{month}:")
    month_problems = problems_by_month[month]
    for problem, count in sorted(month_problems.items(), key=lambda x: -x[1])[:5]:
        print(f"  {problem:20} {count:4} times")

# Find patterns: problem → resolution
print("\n" + "="*80)
print("BREAKTHROUGH SEQUENCES: Problem → Solution")
print("="*80)

# Group messages into problem-solution pairs
current_problem = None
problem_start = None
resolution_time = None

breakthrough_patterns = []

for i, msg in enumerate(messages):
    content_lower = msg['content'].lower()
    
    # Detect problem
    for problem_type, keywords in problems.items():
        if any(kw in content_lower for kw in keywords) and msg['role'] == 'user':
            if current_problem != problem_type:
                current_problem = problem_type
                problem_start = msg['timestamp']
            break
    
    # Detect solution
    if current_problem and msg['role'] == 'gemini' and any(sol in content_lower for sol in solutions):
        if problem_start:
            breakthrough_patterns.append({
                'problem': current_problem,
                'problem_time': problem_start,
                'solution_time': msg['timestamp'],
                'solution_preview': msg['content'][:100]
            })
            current_problem = None
            problem_start = None

# Find recurring difficulties
print("\nMOST FREQUENT DIFFICULTIES")
print("-"*80)
problem_freq = defaultdict(int)
for pattern in breakthrough_patterns:
    problem_freq[pattern['problem']] += 1

for problem, count in sorted(problem_freq.items(), key=lambda x: -x[1]):
    print(f"  {problem:20} {count:4} times overcome")

# Track how problems evolved
print("\n" + "="*80)
print("HOW YOUR APPROACH TO PROBLEMS EVOLVED")
print("="*80)

# October: What were the problems?
oct_probs = problems_by_month['2025-10']
print("\nOctober 2025 - Foundation Phase:")
print("  Struggled with:")
for p, c in sorted(oct_probs.items(), key=lambda x: -x[1])[:5]:
    print(f"    • {p} ({c})")
print("  Approach: Asking Gemini HOW to do everything")
print("  Frustration: High (building from scratch)")

# January: How did they change?
jan_probs = problems_by_month['2026-01']
print("\nJanuary 2026 - After 3 months:")
print("  Struggles with:")
for p, c in sorted(jan_probs.items(), key=lambda x: -x[1])[:5]:
    print(f"    • {p} ({c})")
print("  Approach: Asking specific clarification questions")
print("  Frustration: LOW - confident in what you're building")

# March: New challenges
mar_probs = problems_by_month['2026-03']
print("\nMarch 2026 - Scaling Phase:")
print("  Struggles with:")
for p, c in sorted(mar_probs.items(), key=lambda x: -x[1])[:5]:
    print(f"    • {p} ({c})")
print("  Approach: Asking about real-world constraints (Reddit, communities)")
print("  Frustration: None - you understand your system, now learning applications")

# Find your actual breakthrough moments
print("\n" + "="*80)
print("YOUR ACTUAL BREAKTHROUGH MOMENTS")
print("="*80)

# Look for specific "aha" patterns
breakthroughs = []
for i in range(1, min(100, len(messages))):
    # Gemini gives a detailed explanation, then you respond with understanding
    if messages[i]['role'] == 'gemini' and len(messages[i]['content']) > 200:
        if i+1 < len(messages) and messages[i+1]['role'] == 'user':
            user_response = messages[i+1]['content'].lower()
            if any(marker in user_response for marker in ['got it', 'that makes', 'i see', 'right', 'ok', 'yes']):
                breakthroughs.append({
                    'timestamp': messages[i+1]['timestamp'],
                    'topic': messages[i]['content'][:50],
                    'your_understanding': messages[i+1]['content'][:80]
                })

print(f"\nFound {len(breakthroughs)} moments of clear understanding reached")

# Sample breakthroughs from different phases
print("\nSample breakthroughs across your journey:\n")

# Early breakthroughs
early = [b for b in breakthroughs if b['timestamp'].startswith('2025-10')]
if early:
    print(f"October (Foundation):")
    for b in early[:2]:
        print(f"  [{b['timestamp']}]")
        print(f"    Topic: {b['topic']}")
        print(f"    Your understanding: {b['your_understanding']}")
        print()

# Mid breakthroughs
mid = [b for b in breakthroughs if b['timestamp'].startswith('2026-02')]
if mid:
    print(f"February (Build):")
    for b in mid[:2]:
        print(f"  [{b['timestamp']}]")
        print(f"    Topic: {b['topic']}")
        print(f"    Your understanding: {b['your_understanding']}")
        print()

# Later breakthroughs
late = [b for b in breakthroughs if b['timestamp'].startswith('2026-03')]
if late:
    print(f"March (Scale):")
    for b in late[:2]:
        print(f"  [{b['timestamp']}]")
        print(f"    Topic: {b['topic']}")
        print(f"    Your understanding: {b['your_understanding']}")
        print()

# Analyze your "stuck" patterns
print("\n" + "="*80)
print("WHEN YOU GOT STUCK (and how you got unstuck)")
print("="*80)

stuck_markers = ['stuck', 'still broken', 'still doesnt', 'still wrong', 'still fucking', 'still have', 'still need']
stuck_moments = []

for i, msg in enumerate(messages):
    if msg['role'] == 'user' and any(marker in msg['content'].lower() for marker in stuck_markers):
        stuck_moments.append({
            'timestamp': msg['timestamp'],
            'stuck_with': msg['content'][:100],
            'index': i
        })

print(f"\nYou had {len(stuck_moments)} moments of being stuck")
print("Pattern: Getting stuck meant you needed to:")
print("  1. Redefine the problem (step back)")
print("  2. Ask a different question")
print("  3. Try a new approach")

# Sample stuck moments
for stuck in stuck_moments[:5]:
    print(f"\n  [{stuck['timestamp']}]")
    print(f"    '{stuck['stuck_with']}...'")
    # Find what helped you get unstuck
    if stuck['index'] + 5 < len(messages):
        for j in range(stuck['index'] + 1, min(stuck['index'] + 5, len(messages))):
            if 'works' in messages[j]['content'].lower() or 'right' in messages[j]['content'].lower():
                print(f"    → Resolution: {messages[j]['content'][:80]}...")
                break

print("\n" + "="*80)
