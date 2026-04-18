#!/usr/bin/env python3
"""Debug Copilot JSON structure to understand content extraction."""

import json
from pathlib import Path

json_file = r"D:\Downloads\Copilot\A Philosophy of Kindness and Self-Improvement.json"

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Type: {type(data)}")
print(f"Length: {len(data)}")

if data:
    first_msg = data[0]
    print("\nFirst message structure:")
    print(f"Keys: {list(first_msg.keys())}")
    print(f"\nFull first message:")
    print(json.dumps(first_msg, indent=2)[:2000])
    
    print("\n" + "="*80)
    print("Checking 'contents' field:")
    contents = first_msg.get('contents')
    print(f"Contents type: {type(contents)}")
    print(f"Contents: {contents}")
