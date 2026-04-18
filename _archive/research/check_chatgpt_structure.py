#!/usr/bin/env python3
import json

with open('D:\\Downloads\\Copilot\\chatgpt-_02.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Root type: {type(data).__name__}")
print(f"Items: {len(data)}")

if data and isinstance(data, list):
    item = data[0]
    print(f"First item type: {type(item).__name__}")
    if isinstance(item, dict):
        print(f"Keys: {list(item.keys())}")
        for key in list(item.keys())[:7]:
            val = item[key]
            if isinstance(val, (dict, list)):
                print(f"  {key}: {type(val).__name__} ({len(val)} items)")
            else:
                print(f"  {key}: {str(val)[:80]}")
