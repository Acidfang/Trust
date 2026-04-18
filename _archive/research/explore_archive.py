import json

data = json.load(open('conversations.json'))
print(f'Total conversations: {len(data)}')
print()
print('Topics covered:')
for i, c in enumerate(data[:10]):
    title = c.get('title', 'UNTITLED')[:70]
    msg_count = len(c.get('messages', []))
    print(f'  [{i+1}] {title} ({msg_count} messages)')
