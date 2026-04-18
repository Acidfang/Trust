import json

with open('c:\\Determined\\UNIFIED_MASTER_TIMELINE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract messages around April 5-6 when Θ system discussion happened
# Get all messages in a time window and sort chronologically
messages = data.get('messages', [])

# Filter for the consciousness/Θ discussion period
theta_window = []
for msg in messages:
    ts = msg.get('timestamp', '')
    if '2026-04-05' in ts or '2026-04-06' in ts:
        theta_window.append(msg)

# Sort chronologically
theta_window.sort(key=lambda x: x.get('timestamp', ''))

# Format as chat log
chat_log = "# CONVERSATION LOG: CONSCIOUSNESS MAPPING & Θ SYSTEM\n"
chat_log += f"## April 5-6, 2026\n"
chat_log += f"## {len(theta_window)} messages\n\n"

for msg in theta_window:
    role = msg.get('role', '?').upper()
    platform = msg.get('platform', '?')
    timestamp = msg.get('timestamp', '?')
    content = msg.get('content', '')
    
    chat_log += f"\n### [{timestamp}] {role} ({platform})\n"
    chat_log += f"{content}\n"
    chat_log += "\n---\n"

# Save the chat log
with open('c:\\Determined\\THETA_CONVERSATION_LOG.md', 'w', encoding='utf-8') as f:
    f.write(chat_log)

print(f"✓ Saved {len(theta_window)} messages to THETA_CONVERSATION_LOG.md")
print(f"\nChat log spans: {theta_window[0].get('timestamp')} to {theta_window[-1].get('timestamp')}")
print(f"\nPlatforms involved:")
for platform in set(m.get('platform') for m in theta_window):
    count = len([m for m in theta_window if m.get('platform') == platform])
    print(f"  {platform}: {count} messages")
