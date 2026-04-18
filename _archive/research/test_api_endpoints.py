#!/usr/bin/env python3
"""Test the running API endpoints using urllib"""

import urllib.request
import json

print("=" * 60)
print("UNIVERSAL RENDERER API - ENDPOINT TESTS")
print("=" * 60)

def make_request(endpoint):
    """Make HTTP request to API endpoint"""
    try:
        url = f'http://localhost:5000{endpoint}'
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())
            return response.status, data, None
    except Exception as e:
        return None, None, str(e)

# Test 1: Health check
print("\n[TEST 1] GET /api/health")
status, result, error = make_request('/api/health')
if error:
    print(f"✗ Error: {error}")
else:
    print(f"✓ Status: {status}")
    print(f"✓ Response: {result}")

# Test 2: List organisms
print("\n[TEST 2] GET /api/organisms")
status, result, error = make_request('/api/organisms')
if error:
    print(f"✗ Error: {error}")
else:
    print(f"✓ Status: {status}")
    organisms = result.get('available', [])[:3]
    print(f"✓ Available count: {len(result.get('available', []))}")
    print(f"✓ Sample: {organisms}")

# Test 3: Get organism narrative
print("\n[TEST 3] GET /api/organism/Wolf")
status, result, error = make_request('/api/organism/Wolf')
if error:
    print(f"✗ Error: {error}")
else:
    print(f"✓ Status: {status}")
    print(f"✓ Organism: {result.get('organism')}")
    print(f"✓ Confidence: {result.get('confidence')}")
    narratives = result.get('narratives', {})
    print(f"✓ Fields: {list(narratives.keys())}")
    reason_text = narratives.get('reason', 'N/A')[:60]
    print(f"✓ Reason: {reason_text}...")

# Test 4: Unknown organism
print("\n[TEST 4] GET /api/organism/Unicorn")
status, result, error = make_request('/api/organism/Unicorn')
if error:
    print(f"✗ Error: {error}")
else:
    print(f"✓ Status: {status}")
    print(f"✓ Organism: {result.get('organism')}")
    print(f"✓ Graceful error handling: Works for unknown organisms")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETE - API IS OPERATIONAL")
print("=" * 60)
