import json

with open(r'c:\Determined\UNIFIED_CONVERSATION_TIMELINE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']

print("\n" + "="*60)
print("FINAL 40 MESSAGES - APRIL 2026 ENDPOINT")
print("="*60 + "\n")

for msg in messages[-40:]:
    ts = msg.get('timestamp_str', 'unknown')
    platform = msg.get('platform', '?').upper()
    role = msg.get('role', '?').upper()
    content = msg.get('content', '')[:200]
    content = content.replace('\n', ' ')
    
    print(f"{ts} | {platform:8} | {role:9} | {content}...")
    print()
