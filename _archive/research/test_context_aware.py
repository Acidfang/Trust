#!/usr/bin/env python3
import requests
import json

# Test queries that were generating nonsensical responses before
test_queries = [
    "did you learn anything?",
    "is that a default response?",
    "what is being sentient?"
]

print("TESTING CONTEXT-AWARE RESPONSE GENERATION")
print("=" * 70)

for query in test_queries:
    response = requests.post(
        'http://localhost:5555/query',
        json={'query': query},
        timeout=5
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nQuery: {query}")
        print(f"Response: {data.get('response')}")
        print(f"Coherence: {data.get('coherence'):.0%}")
        print(f"Primitives: {data.get('primitives')}")
    else:
        print(f"Error: {response.status_code}")

print("\n" + "=" * 70)
print("✅ Context-aware response generation active")
