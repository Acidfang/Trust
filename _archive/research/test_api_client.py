#!/usr/bin/env python3
"""Test API with Flask test client"""

import sys
sys.path.insert(0, r'c:\Determined')

try:
    from ENCYCLOPEDIA_API_SERVER import ENTITY_DATABASE, app
    print(f"Loaded {len(ENTITY_DATABASE)} entities")
    
    # Check causal_composition in database
    for name, entity in ENTITY_DATABASE.items():
        has_cc = 'causal_composition' in entity
        print(f"  {name}: causal_composition={has_cc}")
        if has_cc:
            cc = entity['causal_composition']
            print(f"    - emerges_from: {cc.get('emerges_from')}")
            print(f"    - components: {len(cc.get('components', []))} items")
    
    # Test Flask app
    print("\nTesting API with Flask test client...")
    with app.test_client() as client:
        resp = client.get('/api/entity/Atom')
        print(f"API Response Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            entity = data.get('entity', {})
            print(f"Response has causal_composition: {'causal_composition' in entity}")
            if 'causal_composition' in entity:
                cc = entity['causal_composition']
                print(f"  - emerges_from: {cc.get('emerges_from')}")
                print(f"  - components: {cc.get('components')}")
        else:
            print(f"Error: {resp.status_code}")
            print(f"Response: {resp.data[:300]}")
            
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
