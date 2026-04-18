#!/usr/bin/env python3
"""Check attributes for Electron"""
import urllib.request
import json

try:
    with urllib.request.urlopen('http://localhost:5000/api/entity/Electron', timeout=2) as r:
        data = json.loads(r.read().decode())
        
        print("ELECTRON ATTRIBUTES:")
        attrs = data.get('attributes', {})
        for key, val in attrs.items():
            print(f"  {key}: {val}")
        
        print("\nContext found:", "context" in attrs or "habitat" in attrs)
        if "context" in attrs:
            print(f"✓ Context: {attrs.get('context')}")
        elif "habitat" in attrs:
            print(f"✗ Still using habitat: {attrs.get('habitat')}")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
