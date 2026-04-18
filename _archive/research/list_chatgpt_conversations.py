import json
from datetime import datetime

filepath = r'D:\Downloads\AI Chat\ChatGPT\conversations.json'

with open(filepath, 'r', encoding='utf-8') as f:
    conversations = json.load(f)

print(f"{'='*70}")
print(f"CHATGPT CONSOLIDATED EXPORT - 72 CONVERSATIONS")
print(f"{'='*70}\n")

for i, conv in enumerate(conversations):
    title = conv.get('title', 'NO TITLE')
    conv_id = conv.get('id', 'NO ID')
    
    # Count messages
    mapping = conv.get('mapping', {})
    msg_count = len([v for v in mapping.values() if v.get('message') and v['message'].get('content')])
    
    # Get date
    create_time = conv.get('create_time', 0)
    if create_time:
        date_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M')
    else:
        date_str = 'unknown'
    
    print(f"{i+1:2d}. {title[:60]:60s} | {msg_count:3d} msgs | {date_str}")

print(f"\n{'='*70}")
print(f"Total: {len(conversations)} conversations")
