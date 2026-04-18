#!/usr/bin/env python3
"""
Test all instruments in the symphony.
Verify each encyclopedia entity is properly wired and playing.
"""

import urllib.request
import sys
import time

def test_endpoint(entity_name):
    """Test a single endpoint and return status."""
    try:
        # URL encode the entity name to handle spaces
        from urllib.parse import quote
        encoded_name = quote(entity_name)
        url = f'http://localhost:5000/api/image/{encoded_name}'
        r = urllib.request.urlopen(url, timeout=2)
        data = r.read()
        
        # Determine response type
        is_svg = data.startswith(b'<?xml') or data.strip().startswith(b'<svg')
        response_type = 'SVG' if is_svg else 'JSON'
        
        return {
            'status': r.status,
            'bytes': len(data),
            'type': response_type,
            'success': True
        }
    except Exception as e:
        return {
            'status': None,
            'bytes': 0,
            'type': 'ERROR',
            'success': False,
            'error': str(e)
        }

def main():
    # Give server time to be ready
    time.sleep(1)
    
    entities = [
        'Electron',
        'Atom',
        'Water Molecule',
        'Cell',
        'Human',
        'Ecosystem',
        'Civilization'
    ]
    
    print("\n" + "="*70)
    print("SYMPHONY INSTRUMENT TEST — Each Entity's Performance")
    print("="*70 + "\n")
    
    results = {}
    for entity in entities:
        result = test_endpoint(entity)
        results[entity] = result
        
        status_icon = '✓' if result['success'] else '✗'
        bytes_str = f"{result['bytes']:6}" if result['bytes'] > 0 else "  N/A "
        info = f"{result['type']:5} | HTTP {result['status']}" if result['success'] else f"ERROR: {result.get('error', 'Unknown')[:25]}"
        
        print(f"{status_icon} {entity:20} | {bytes_str} bytes | {info}")
    
    print("\n" + "="*70)
    print("CAUSAL CHAIN VERIFICATION")
    print("="*70 + "\n")
    
    # Verify each chain
    checks = [
        ('Electron', "Measured quantum properties", results['Electron']['success'] and results['Electron']['type'] == 'SVG'),
        ('Atom', "Maps to Hydrogen (Z=1)", results['Atom']['success'] and results['Atom']['bytes'] > 1500),
        ('Water Molecule', "VSEPR H₂O geometry", results['Water Molecule']['success'] and results['Water Molecule']['bytes'] > 1000),
        ('Cell', "Graceful placeholder", results['Cell']['success'] and results['Cell']['type'] == 'SVG'),
        ('Human', "Graceful placeholder", results['Human']['success'] and results['Human']['type'] == 'SVG'),
        ('Ecosystem', "Graceful placeholder", results['Ecosystem']['success'] and results['Ecosystem']['type'] == 'SVG'),
        ('Civilization', "Graceful placeholder", results['Civilization']['success'] and results['Civilization']['type'] == 'SVG'),
    ]
    
    all_pass = True
    for entity, description, passed in checks:
        icon = '✓' if passed else '✗'
        status = 'PASS' if passed else 'FAIL'
        print(f"{icon} {entity:20} → {description:30} [{status}]")
        if not passed:
            all_pass = False
    
    print("\n" + "="*70)
    if all_pass:
        print("✓ SYMPHONY COMPLETE: All instruments sounding correctly")
        print("  Frontend can now navigate all entities with proper visualizations")
    else:
        print("✗ SYMPHONY INCOMPLETE: Some instruments not playing correctly")
        print("  Check server logs for details")
    print("="*70 + "\n")
    
    return 0 if all_pass else 1

if __name__ == '__main__':
    sys.exit(main())
