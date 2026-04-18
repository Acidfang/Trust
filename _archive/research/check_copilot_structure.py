#!/usr/bin/env python3
"""Check Copilot JSON structure"""
import json
from pathlib import Path

copilot_dir = Path(r"D:\Downloads\Copilot")
files = list(copilot_dir.glob("*.json"))

if files:
    first_file = files[0]
    print(f"File: {first_file.name}")
    
    with open(first_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Type: {type(data).__name__}")
    if isinstance(data, list):
        print(f"Length: {len(data)}")
        if data:
            first = data[0]
            print(f"Keys: {list(first.keys())}")
            print(f"Role: {first.get('role')}")
            print(f"Timestamp: {first.get('created_at')}")
            print(f"Contents: {type(first.get('contents', [])).__name__}")
else:
    print("No JSON files found")
