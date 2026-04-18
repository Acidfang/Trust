#!/usr/bin/env python3
"""Quick API verification"""
import urllib.request
import json

try:
    with urllib.request.urlopen('http://localhost:5000/api/entity/Electron', timeout=2) as r:
        data = json.loads(r.read().decode())
        print('✓ API responding')
        print(f'✓ Entity: {data.get("entity")}')
        print(f'✓ Fields found: {len(data.get("field_narratives", {}))}')
        
        # Check corrections
        if data.get('field_narratives', {}).get('corrections'):
            print('✓ Corrections/What We Got Wrong: Present')
            print('\nCorrections preview:')
            corr = data.get('field_narratives', {}).get('corrections')
            if len(corr) > 100:
                print(corr[:200] + '...')
            else:
                print(corr)
        
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
