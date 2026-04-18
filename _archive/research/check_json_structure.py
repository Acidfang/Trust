#!/usr/bin/env python3
import json
from pathlib import Path

# Check first JSON file structure
json_dir = Path(r"D:\Downloads")
json_files = list(json_dir.glob("*.json"))

if json_files:
    first_file = json_files[0]
    print(f"Checking: {first_file.name}\n")
    
    try:
        with open(first_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if list or dict
        if isinstance(data, list):
            print(f"Data is LIST with {len(data)} elements")
            if data:
                print(f"First element type: {type(data[0])}")
                if isinstance(data[0], dict):
                    print(f"First element keys: {list(data[0].keys())[:15]}")
                    print()
                    for key in ['timestamp', 'created', 'date', 'createTime', 'create_time', 'time', 'createTime']:
                        if key in data[0]:
                            print(f"  ✓ Found {key}: {str(data[0][key])[:80]}")
        else:
            print("Top-level keys:", list(data.keys())[:15])
            print()
            for key in ['timestamp', 'created', 'date', 'createTime', 'updateTime', 'metadata']:
                if key in data:
                    print(f"Found {key}: {data[key]}")
        
        print(f"\nTotal JSON files: {len(json_files)}")
    except Exception as e:
        print(f"Error: {e}")
