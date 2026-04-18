import json

with open('c:\\Determined\\UNIFIED_MASTER_TIMELINE.json', 'r') as f:
    data = json.load(f)

# Search for messages containing the actual thermochemical system keywords
corp_keywords = ['decomposition', 'h2o2', 'h₂o₂', 'plasma', 'recombination', 'thermal dissociation', 'reaction limiter', 'oxygen surplus', 'hydrogen limiting', 'peroxide', 'botton', 'liquid phase', 'steam turbine', 'inconel']

results = []
for msg in data.get('messages', []):
    content = (msg.get('content', '') or '').lower()
    if any(kw in content for kw in corp_keywords):
        results.append({
            'timestamp': msg.get('timestamp'),
            'role': msg.get('role'),
            'platform': msg.get('platform'),
            'content': msg.get('content', '')[:500]
        })

print(f"Found {len(results)} messages with CORP-RHS keywords")

if results:
    print("\n=== THERMOCHEMICAL SYSTEM MESSAGES ===\n")
    for r in sorted(results, key=lambda x: x['timestamp'], reverse=True)[:20]:
        print(f"{r['timestamp']} ({r['platform']}) - {r['role']}")
        print(r['content'][:250])
        print("---\n")
else:
    print("\nNo messages found with those specific keywords")
    print("\nThe Θ system (CORP-RHS) document exists in the share link")
    print("But it doesn't appear in the unified timeline (Oct 2025 - Apr 6 2026)")
    print("\nThis suggests:")
    print("  1. It was added to the share after the last timeline export")
    print("  2. Or it exists in a separate conversation thread")
    print("  3. Or it's a synthesis/export from multiple conversations")
