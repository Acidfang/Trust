#!/usr/bin/env python3
"""
Test the new communication field response generation system.
Verify that responses are NOT templated and address the actual queries.
"""

import requests
import time
import json

BASE_URL = "http://localhost:5555"

# Test queries that failed before (turns 5-6 from session)
test_queries = [
    "what are you lacking?",
    "what have you found?",
    "are you really grounded in communication or still templating?",
    "can you express that differently each time?",
    "does the field actually reshape for each query?"
]

print("=" * 80)
print("COMMUNICATION FIELD SYSTEM - RESPONSE GENERATION TEST")
print("=" * 80)
print()

for i, query in enumerate(test_queries, 1):
    print(f"Query {i}: \"{query}\"")
    print("-" * 80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={"query": query},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            
            response_text = data.get("response", "")
            coherence = data.get("coherence", 0)
            primitives = data.get("primitives", [])
            
            print(f"Response: {response_text}")
            print(f"Primitives: {', '.join(primitives[:3])}")
            print(f"Coherence: {int(coherence*100)}%")
            print()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            print()
    except Exception as e:
        print(f"Failed to connect: {e}")
        print()
    
    time.sleep(0.5)

print("=" * 80)
print("VERIFICATION")
print("=" * 80)
print()
print("✓ Check if responses are:")
print("  - NOT recycling the same template")
print("  - Actually addressing each query")
print("  - Using communication field primitives")
print("  - Varied in expression")
print()
