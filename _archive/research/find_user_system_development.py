import json

with open('c:\\Determined\\UNIFIED_MASTER_TIMELINE.json', 'r') as f:
    data = json.load(f)

# Find ONLY user messages with system development language
user_system_msgs = []
for msg in data.get('messages', []):
    if msg.get('role') == 'user':
        content = (msg.get('content', '') or '')
        content_lower = content.lower()
        
        # Look for actual system design/specification language
        if any(kw in content_lower for kw in ['system', 'closed', 'constraint', 'reaction', 'invariant', 'cycle', 'state', 'phase', 'energy', 'decomp', 'plasma']):
            user_system_msgs.append({
                'timestamp': msg.get('timestamp'),
                'platform': msg.get('platform'),
                'content': content[:600]
            })

print(f"Found {len(user_system_msgs)} USER system messages\n")

# Sort by timestamp descending (most recent first)
for msg in sorted(user_system_msgs, key=lambda x: x['timestamp'], reverse=True)[:30]:
    print(f"{msg['timestamp']} ({msg['platform']})")
    print(msg['content'][:400])
    print("\n" + "="*80 + "\n")
