import json

filepath = r'D:\Downloads\AI Chat\ChatGPT\conversations.json'

with open(filepath, 'r', encoding='utf-8') as f:
    conversations = json.load(f)

# Find the largest conversation
largest = max(conversations, key=lambda c: len(c.get('mapping', {})))
print(f"Largest conversation: {largest.get('title', 'UNTITLED')}")
print(f"Message nodes: {len(largest.get('mapping', {}))}")

mapping = largest.get('mapping', {})
print(f"\nSample node structure (first 3 nodes):")

for i, (node_id, node) in enumerate(list(mapping.items())[:3]):
    print(f"\nNode {i}: {node_id}")
    print(f"  Keys: {list(node.keys())}")
    
    if 'message' in node:
        msg = node['message']
        print(f"  Message keys: {list(msg.keys())}")
        print(f"  Role: {msg.get('role')}")
        print(f"  Content type: {type(msg.get('content'))}")
        
        content = msg.get('content', [])
        if isinstance(content, list):
            print(f"  Content length (list): {len(content)}")
            if len(content) > 0:
                print(f"  First content item keys: {list(content[0].keys()) if isinstance(content[0], dict) else type(content[0])}")
        else:
            print(f"  Content: {str(content)[:100]}")

# Count actual messages
msg_count = 0
for node in mapping.values():
    if node.get('message') and node['message'].get('content'):
        msg_count += 1

print(f"\nTotal messages in mapping: {msg_count}")
print(f"Total nodes: {len(mapping)}")
