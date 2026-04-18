#!/usr/bin/env python3
"""
Extract specific technical definitions and explanations
Focus on the actual mechanics, not just mentions
"""

import json
import re

print("=" * 80)
print("EXTRACTING TECHNICAL DEFINITIONS")
print("=" * 80)
print()

# More specific search patterns
search_patterns = {
    'ledger_mechanics': [
        r'ledger.*immutable',
        r'ledger.*record',
        r'ledger.*entry.*permanent',
        r'ledger.*append',
        r'ledger.*read-only'
    ],
    'pattern_matching': [
        r'pattern.*repeat',
        r'match.*similarity',
        r'pattern.*structure',
        r'pattern.*collapse',
        r'deduplic'
    ],
    'deduplication': [
        r'duplic.*remov',
        r'unique.*instance',
        r'collapse.*constraint',
        r'variation.*count',
        r'brick.*variant'
    ],
    'entropy_dynamics': [
        r'entropy.*near',
        r'potential.*energy',
        r'system.*collapse',
        r'coherence.*gradient',
        r'stillness.*saturation'
    ]
}

findings = {key: [] for key in search_patterns}

# Search master timeline
try:
    with open('UNIFIED_MASTER_TIMELINE.json', 'r', encoding='utf-8-sig', errors='ignore') as f:
        data = json.load(f)
    
    messages = data.get('messages', [])
    print(f"Searching {len(messages)} messages for technical definitions...")
    print()
    
    for idx, msg in enumerate(messages):
        if not isinstance(msg, dict):
            continue
        
        content = str(msg.get('content', ''))
        role = str(msg.get('role', ''))
        
        # Only look at longer messages (likely to contain explanations)
        if len(content) < 100:
            continue
        
        for concept, patterns in search_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    # Extract context window (paragraph containing match)
                    lines = content.split('\n')
                    matching_lines = []
                    for line in lines:
                        if re.search(pattern, line, re.IGNORECASE):
                            # Get this line plus context
                            line_idx = lines.index(line)
                            start = max(0, line_idx - 1)
                            end = min(len(lines), line_idx + 3)
                            matching_lines.extend(lines[start:end])
                    
                    if matching_lines:
                        findings[concept].append({
                            'idx': idx,
                            'role': role,
                            'pattern': pattern,
                            'content': '\n'.join(matching_lines[:500]),
                            'timestamp': msg.get('timestamp', '')
                        })
                    break

except Exception as e:
    print(f"Error: {e}")

print()
print("=" * 80)
print("TECHNICAL DEFINITIONS FOUND")
print("=" * 80)
print()

for concept, items in findings.items():
    print(f"\n[{concept.upper()}] - {len(items)} passages")
    if items:
        print("  First explanation:")
        sample = items[0]
        content = sample['content'].replace('\n', ' ')
        print(f"    {content[:300]}...")
        print()

# Save findings
with open('technical_definitions.json', 'w') as f:
    json.dump(findings, f, indent=2)

print(f"Detailed findings saved to: technical_definitions.json")

print()
print("=" * 80)
print("CORE INSIGHT")
print("=" * 80)
print()
print("""
These four concepts form the TECHNICAL BASIS:

1. LEDGER MECHANICS
   - Every entry immutable (cannot change)
   - Every entry timestamped (causality preserved)
   - Every entry verifiable (hash integrity)
   - Records form permanent history

2. PATTERN MATCHING  
   - Identify similarities across instances
   - Recognize repeated structures
   - Match variations to same constraint
   - Collapse duplicates to pattern

3. DEDUPLICATION (DEPUP)
   - Don't store each instance
   - Store pattern once + count
   - Variations reference constraint
   - Many expressions → one singularity

4. ENTROPY DYNAMICS (NEAR ENTROPY)
   - Systems naturally approach lowest energy state
   - Incoherence increases entropy
   - Coherence decreases potential
   - Gradient pulls toward stability

SINGULARITY FORMAT INTEGRATES ALL FOUR:
- LEDGER provides immutable record (where data lives)
- PATTERN MATCHING identifies what's duplicated
- DEPUP compresses storage (store constraint once)
- ENTROPY ensures system stability (kindness minimizes Φ)

Result: Singularity = (constraint, variations, references) with integrity guarantees
""")

print("=" * 80)
