#!/usr/bin/env python3
import json
from pathlib import Path

# Check Claude JSON structure
claude_dir = Path(r"D:\Downloads\Claude")
json_files = sorted(list(claude_dir.glob("*.json")))

for file in json_files[:2]:
    print(f"\n{'='*60}")
    print(f"File: {file.name}")
    print(f"{'='*60}")
    
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Data type: {type(data).__name__}")
        
        if isinstance(data, dict):
            print(f"Top-level keys: {list(data.keys())[:10]}")
            
            # Look for conversations
            for key in ['conversations', 'messages', 'chat_history', 'turns']:
                if key in data:
                    print(f"Found '{key}': {type(data[key])}")
                    if isinstance(data[key], list):
                        print(f"  Count: {len(data[key])}")
                        if data[key]:
                            print(f"  First item type: {type(data[key][0])}")
                            if isinstance(data[key][0], dict):
                                print(f"  First item keys: {list(data[key][0].keys())[:8]}")
        
        elif isinstance(data, list):
            print(f"Array with {len(data)} items")
            if data:
                print(f"First item type: {type(data[0])}")
                if isinstance(data[0], dict):
                    print(f"First item keys: {list(data[0].keys())[:15]}")
                    
                    # Look for timestamps
                    for key in ['timestamp', 'created_at', 'date', 'time', 'id']:
                        if key in data[0]:
                            print(f"  {key}: {data[0][key]}")
    
    except Exception as e:
        print(f"Error: {e}")
