import json

with open('c:\\Determined\\UNIFIED_MASTER_TIMELINE.json', 'r', encoding='utf-8') as f:
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
output = []
for msg in sorted(user_system_msgs, key=lambda x: x['timestamp'], reverse=True)[:40]:
    output.append(f"{msg['timestamp']} ({msg['platform']})")
    output.append(msg['content'][:450])
    output.append("\n" + "="*80 + "\n")

# Write to file to avoid encoding issues
with open('c:\\Determined\\user_system_messages.txt', 'w', encoding='utf-8') as f:
    f.write(f"Found {len(user_system_msgs)} USER system messages\n\n")
    f.write('\n'.join(output))

print("Saved to user_system_messages.txt")
print("First 30 messages:")
for msg in sorted(user_system_msgs, key=lambda x: x['timestamp'], reverse=True)[:30]:
    ts = msg['timestamp']
    plat = msg['platform']
    preview = msg['content'][:150].replace('\n', ' ')[:150]
    print(f"{ts} ({plat})")
    print(f"  {preview}...")
    print()
