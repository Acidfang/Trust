#!/usr/bin/env python3
import json

# Verify JSON timeline
with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ JSON Timeline Valid")
print(f"  Total Messages: {data['metadata']['total_messages']}")
print(f"  Date Range: {data['metadata']['date_range']['first']} to {data['metadata']['date_range']['last']}")
print(f"  Sources: {data['metadata']['sources']}")
print(f"\n  First message timestamp: {data['messages'][0]['timestamp']}")
print(f"  First message role: {data['messages'][0]['role']}")
print(f"  First message content (first 80 chars): {data['messages'][0]['content'][:80]}")
