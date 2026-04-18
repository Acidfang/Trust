import json

# Load the unified master timeline
with open('c:\\Determined\\UNIFIED_MASTER_TIMELINE.json', 'r') as f:
    data = json.load(f)

# Search for USER messages with system/constraint/reaction/heat related content
user_results = []
for msg in data.get('messages', []):
    if msg.get('role') == 'user':
        content = (msg.get('content', '') or '').lower()
        # Look for technical/system design language
        if any(term in content for term in ['system', 'closed', 'reaction', 'heat', 'constraint', 'oxygen', 'hydrogen', 'decompose', 'peroxide', 'invariant', 'cycle', 'energy', 'mass', 'protocol', 'thinking', 'compute']):
            user_results.append({
                'timestamp': msg.get('timestamp'),
                'platform': msg.get('platform'),
                'content': (msg.get('content', '') or '')[:500]
            })

print(f"Found {len(user_results)} USER messages with system/technical language")
print("\n=== USER MESSAGES WITH TECHNICAL CONTENT (reverse chronological) ===\n")

# Sort by timestamp descending to see recent ones
for r in sorted(user_results, key=lambda x: x['timestamp'], reverse=True)[:20]:
    print(f"{r['timestamp']} ({r['platform']})")
    print(f"{r['content'][:300]}")
    print("---\n")
