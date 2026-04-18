#!/usr/bin/env python3
"""Test enhanced operations discovery"""

import sys
sys.path.insert(0, r'c:\Determined\src\applications')
from aria_gate_discovery_engine import ARIAGateDiscoveryEngine
import json

engine = ARIAGateDiscoveryEngine(r'c:\Determined\src\applications')

# Discover more gates to unlock combinations
gates = [
    'Boolean NOT',
    'Boolean logic (AND/OR/XOR)',
    'Logic negation',
    'Bit flip'
]

for gate_name in gates:
    print(f"\n{'='*60}")
    print(f"Discovering: {gate_name}")
    print('='*60)
    
    discovery = engine.discover_gate(gate_name)
    
    # Show enhanced operations
    enhanced = discovery.get('enhanced_operations_now_possible', [])
    if enhanced:
        print("\nEnhanced Operations Now Possible:")
        for op in enhanced:
            print(f"  [OK] {op['operation']}")
            print(f"    Requires: {', '.join(op['gates_required'])}")
            print(f"    Principle: {op['discovery_principle']}")
    else:
        print("\n(No enhanced operations unlocked yet)")
    
    # Show bit level status
    status = discovery['bit_level_collection_status']
    print(f"\nBit Level Collection Status:")
    print(f"  Discovered: {status['discovered_gates_count']} / {status['total_gates_at_level']}")
    print(f"  Coherence: {status['coherence']:.2%}")
    print(f"  Gates: {', '.join(status['gates_discovered'])}")
    
    # Show overall metrics derived from single source
    if 'overall_metrics' in discovery:
        metrics = discovery['overall_metrics']
        print(f"\nOverall Discovery Metrics:")
        print(f"  Bit Level Completion: {metrics['bit_level_completion_percent']}")
        print(f"  Average Domain Coherence: {metrics['average_domain_coherence']:.0%}")
        print(f"  Domains at Full Coherence: {metrics['domains_at_full_coherence']} / {metrics['total_domains']}")
        print(f"  Total Enhanced Operations Unlocked: {metrics['total_enhanced_operations']}")

print("\n" + "="*60)
print("SUMMARY: Enhanced operations discovered as gates combine")
print("="*60)
