#!/usr/bin/env python3
"""Diagnostic test to see exactly what the API returns"""

import urllib.request
import json

def test_api(endpoint):
    """Make request and return parsed response"""
    try:
        url = f'http://localhost:5000{endpoint}'
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        return {"error": str(e)}

print("=" * 70)
print("DIAGNOSTIC TEST - API RESPONSE STRUCTURE")
print("=" * 70)

print("\n[1] Health Check Response:")
health = test_api('/api/health')
print(json.dumps(health, indent=2))

print("\n[2] Organisms List Response:")
organisms = test_api('/api/organisms')
print(f"Type: {type(organisms)}")
print(f"Keys: {list(organisms.keys()) if isinstance(organisms, dict) else 'N/A'}")
if 'organisms' in organisms:
    print(f"First organism: {organisms['organisms'][0] if organisms['organisms'] else 'None'}")

print("\n[3] Wolf Organism Response (FULL):")
wolf = test_api('/api/organism/Wolf')
print(f"Type: {type(wolf)}")
print(f"Top-level keys: {list(wolf.keys()) if isinstance(wolf, dict) else 'N/A'}")

if isinstance(wolf, dict):
    for key in wolf.keys():
        value = wolf[key]
        if isinstance(value, dict):
            print(f"\n  {key} (dict):")
            if value:
                print(f"    Keys: {list(value.keys())[:5]}")  # First 5 keys
                print(f"    Sample: {str(value)[:100]}...")
            else:
                print(f"    EMPTY DICT")
        elif isinstance(value, list):
            print(f"  {key} (list): length={len(value)}")
            if value:
                print(f"    First item: {value[0]}")
        else:
            print(f"  {key}: {value}")

print("\n[4] Wolf Organism - Full JSON:")
print(json.dumps(wolf, indent=2)[:500] + "...")

print("\n" + "=" * 70)
