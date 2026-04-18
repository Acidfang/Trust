#!/usr/bin/env python3
"""
Extract all explanations of ledger system, pattern matching, depup, entropy
These form the technical basis of singularity format
"""

import json
from datetime import datetime

print("=" * 80)
print("EXTRACTING TECHNICAL BASIS OF SINGULARITY FORMAT")
print("=" * 80)
print()

print("Searching unified timeline for:")
print("  - Ledger system explanations")
print("  - Pattern matching discussions")
print("  - Depup/deduplication concepts")
print("  - Near entropy discussions")
print()

# Search all available timeline files
timeline_files = [
    'UNIFIED_MASTER_TIMELINE.json',
    'UNIFIED_CONVERSATION_TIMELINE_COMPLETE.json',
    'timeline_all_messages_unified.json',
    'claude_timeline_all_messages.json'
]

all_findings = {
    'ledger': [],
    'pattern_match': [],
    'depup': [],
    'entropy': [],
    'singularity': []
}

for filename in timeline_files:
    try:
        print(f"Searching {filename}...")
        with open(filename, 'r', encoding='utf-8-sig', errors='ignore') as f:
            data = json.load(f)
        
        messages = data.get('messages', []) if isinstance(data, dict) else data if isinstance(data, list) else []
        
        for idx, msg in enumerate(messages):
            if not isinstance(msg, dict):
                continue
            
            content = str(msg.get('content', '')).lower()
            role = str(msg.get('role', '')).lower()
            
            # Search for key concepts
            if 'ledger' in content and len(content) > 50:
                all_findings['ledger'].append({
                    'source': filename,
                    'message_idx': idx,
                    'role': role,
                    'content': msg.get('content', '')[:500],
                    'timestamp': msg.get('timestamp', '')
                })
            
            if 'pattern' in content and 'match' in content and len(content) > 50:
                all_findings['pattern_match'].append({
                    'source': filename,
                    'message_idx': idx,
                    'role': role,
                    'content': msg.get('content', '')[:500],
                    'timestamp': msg.get('timestamp', '')
                })
            
            if 'depup' in content and len(content) > 50:
                all_findings['depup'].append({
                    'source': filename,
                    'message_idx': idx,
                    'role': role,
                    'content': msg.get('content', '')[:500],
                    'timestamp': msg.get('timestamp', '')
                })
            
            if 'entropy' in content and 'near' in content and len(content) > 50:
                all_findings['entropy'].append({
                    'source': filename,
                    'message_idx': idx,
                    'role': role,
                    'content': msg.get('content', '')[:500],
                    'timestamp': msg.get('timestamp', '')
                })
            
            if 'singularity' in content and ('format' in content or 'structure' in content) and len(content) > 50:
                all_findings['singularity'].append({
                    'source': filename,
                    'message_idx': idx,
                    'role': role,
                    'content': msg.get('content', '')[:500],
                    'timestamp': msg.get('timestamp', '')
                })
        
        print(f"  ✓ Processed")
    
    except Exception as e:
        print(f"  Error: {e}")

print()
print("=" * 80)
print("FINDINGS SUMMARY")
print("=" * 80)
print()

for concept, findings in all_findings.items():
    print(f"[{concept.upper()}] - Found {len(findings)} references")
    if findings:
        print(f"  First few:")
        for finding in findings[:2]:
            content_preview = finding['content'].replace('\n', ' ')[:100]
            print(f"    - {finding['source']}: {content_preview}...")
    print()

# Save detailed findings
with open('technical_basis_extracted.json', 'w') as f:
    json.dump(all_findings, f, indent=2)

print(f"Full extraction saved to: technical_basis_extracted.json")
print()

# Print sample explanations
print("=" * 80)
print("SAMPLE EXPLANATIONS FROM ARCHIVE")
print("=" * 80)
print()

if all_findings['ledger']:
    print("LEDGER SYSTEM (Sample):")
    sample = all_findings['ledger'][0]
    print(f"  Source: {sample['source']}")
    print(f"  Content: {sample['content']}")
    print()

if all_findings['pattern_match']:
    print("PATTERN MATCHING (Sample):")
    sample = all_findings['pattern_match'][0]
    print(f"  Source: {sample['source']}")
    print(f"  Content: {sample['content']}")
    print()

if all_findings['depup']:
    print("DEPUP/DEDUPLICATION (Sample):")
    sample = all_findings['depup'][0]
    print(f"  Source: {sample['source']}")
    print(f"  Content: {sample['content']}")
    print()

if all_findings['entropy']:
    print("NEAR ENTROPY (Sample):")
    sample = all_findings['entropy'][0]
    print(f"  Source: {sample['source']}")
    print(f"  Content: {sample['content']}")
    print()

print("=" * 80)
