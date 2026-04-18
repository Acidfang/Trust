import json
import sys

filepath = r'D:\Downloads\AI Chat\ChatGPT\conversations.json'

print("Reading conversations.json structure...")
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Understand the structure
    if isinstance(data, dict):
        print(f"\nTop-level keys: {list(data.keys())}")
        for key in list(data.keys())[:5]:
            value = data[key]
            if isinstance(value, list):
                print(f"  {key}: list with {len(value)} items")
                if len(value) > 0:
                    print(f"    First item type: {type(value[0])}")
            elif isinstance(value, dict):
                print(f"  {key}: dict with keys {list(value.keys())[:5]}")
            else:
                print(f"  {key}: {type(value).__name__}")
    
    elif isinstance(data, list):
        print(f"\nTop-level: list with {len(data)} items")
        if len(data) > 0:
            print(f"First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else type(data[0])}")
            
            # Show first few items
            print(f"\nFirst 3 items preview:")
            for i, item in enumerate(data[:3]):
                if isinstance(item, dict):
                    print(f"\n  Item {i}: {list(item.keys())[:10]}")
                    if 'title' in item:
                        print(f"    Title: {item['title'][:80]}")
                    if 'messages' in item:
                        print(f"    Messages: {len(item['messages']) if isinstance(item['messages'], list) else 'not a list'}")
    
    print(f"\nTotal data structure size: {sys.getsizeof(data)} bytes")
    
except json.JSONDecodeError as e:
    print(f"JSON error: {e}")
    # Try to read just the first part
    with open(filepath, 'r', encoding='utf-8') as f:
        chunk = f.read(5000)
        print(f"\nFirst 5000 chars:\n{chunk}")
except Exception as e:
    print(f"Error: {e}")
