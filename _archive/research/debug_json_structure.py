#!/usr/bin/env python3
import json
from pathlib import Path

# Debug: check actual structure
json_file = Path(r"D:\Downloads\_A Brief Exchange .json")

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Data is list of {len(data)} items\n")

for idx, item in enumerate(data):
    print(f"Item {idx}:")
    print(f"  Keys: {list(item.keys())}")
    print(f"  role: {item.get('role')}")
    print(f"  created_at: {item.get('created_at')}")
    
    contents = item.get('contents', [])
    print(f"  contents type: {type(contents)}, length: {len(contents) if isinstance(contents, list) else 'N/A'}")
    
    if isinstance(contents, list) and contents:
        print(f"  First content item: {type(contents[0])}")
        print(f"  First content: {str(contents[0])[:100]}")
    
    print()
