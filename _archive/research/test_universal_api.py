#!/usr/bin/env python3
"""Test the universalized API"""

import urllib.request
import json

print("Testing Updated Universal API")
print("=" * 60)

# Test 1: Universal entity endpoint
print("\n[TEST 1] Universal /api/entity/Electron")
try:
    url = 'http://localhost:5000/api/entity/Electron'
    with urllib.request.urlopen(url, timeout=2) as r:
        data = json.loads(r.read().decode())
        print("✓ Success")
        print(f"  entity: {data.get('entity')}")
        print(f"  entity_type: {data.get('entity_type')}")
        print(f"  scale_agnostic: {data.get('scale_agnostic')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Backward compatibility
print("\n[TEST 2] Backward compat /api/organism/Wolf")
try:
    url = 'http://localhost:5000/api/organism/Wolf'
    with urllib.request.urlopen(url, timeout=2) as r:
        data = json.loads(r.read().decode())
        print("✓ Success")
        print(f"  entity (was organism): {data.get('entity')}")
        print(f"  scale_agnostic: {data.get('scale_agnostic')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: New universal entities list
print("\n[TEST 3] Universal /api/entities list")
try:
    url = 'http://localhost:5000/api/entities'
    with urllib.request.urlopen(url, timeout=2) as r:
        data = json.loads(r.read().decode())
        entities = data.get('entities', [])
        print("✓ Success")
        print(f"  entities count: {len(entities)}")
        print(f"  Samples: {[e['name'] for e in entities[:3]]}")
        print(f"  Covers scales:")
        scales = set(e.get('scale', '') for e in entities)
        print(f"    {', '.join(scales)}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Health check
print("\n[TEST 4] Health check")
try:
    url = 'http://localhost:5000/api/health'
    with urllib.request.urlopen(url, timeout=2) as r:
        data = json.loads(r.read().decode())
        print("✓ Success")
        print(f"  status: {data.get('status')}")
        print(f"  principle: {data.get('principle')}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("Universal API Tests Complete")
print("Format: Universally agnostic (electrons → cosmic systems)")
print("=" * 60)
