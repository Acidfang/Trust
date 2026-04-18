#!/usr/bin/env python3
import requests
import json

# Test reasoning server integration
try:
    print("Testing Reasoning Server Integration...")
    print("=" * 60)
    
    response = requests.post(
        'http://localhost:5555/query',
        json={'query': 'what is coherence?'},
        timeout=5
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nQuery: {data.get('query')}")
        print(f"Response: {data.get('response')[:150]}...")
        print(f"Coherence: {data.get('coherence'):.1%}")
        print(f"Activated Primitives: {data.get('primitives')}")
        print(f"Domains: {data.get('domains')}")
        print("\n✅ Integration working!")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
