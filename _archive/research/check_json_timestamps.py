#!/usr/bin/env python3
import json
from pathlib import Path

json_dir = Path(r"D:\Downloads")
json_files = sorted(list(json_dir.glob("*.json")))[:5]

for file in json_files:
    print(f"\nFile: {file.name}")
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list) and data:
            first = data[0]
            created = first.get('created_at')
            updated = first.get('updated_at')
            print(f"  created_at: {created} (type: {type(created).__name__})")
            print(f"  updated_at: {updated} (type: {type(updated).__name__})")
            if 'contents' in first:
                print(f"  contents type: {type(first['contents'])}")
                if isinstance(first['contents'], list):
                    print(f"  contents count: {len(first['contents'])}")
    except Exception as e:
        print(f"  Error: {e}")

print(f"\n\nTotal JSON files available: {len(sorted(list(json_dir.glob('*.json'))))}")
