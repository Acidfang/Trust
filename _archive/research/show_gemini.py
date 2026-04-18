#!/usr/bin/env python3
import json

with open('gemini_consolidated_database.json', 'r', encoding='utf-8-sig', errors='ignore') as f:
    data = json.load(f)

print('GEMINI CONVERSATION ARCHIVE')
print('=' * 60)
print()
print('Created:', data.get('created_at', 'unknown'))
print('Total Conversations:', data.get('total_conversations', 0))
print()

stats = data.get('stats', {})
print('Statistics:')
for key, val in stats.items():
    print(f'  {key}: {val}')
print()

convs = data.get('conversations', [])
print(f'Conversations stored: {len(convs)}')
if len(convs) > 0:
    print()
    print('Sample conversations:')
    for i, conv in enumerate(convs[:5]):
        if isinstance(conv, dict):
            title = conv.get('title', 'untitled')
            msg_count = conv.get('message_count', '?')
            print(f'  {i+1}. {title} ({msg_count} msgs)')
