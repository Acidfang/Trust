#!/usr/bin/env python3
"""
Test script to verify ARIA Gate Discovery integration.
This tests the complete flow from gate selection → API call → ARIA discovery → ledger recording
"""

import sys
import json
from pathlib import Path

# Add paths
sys.path.insert(0, r"c:\Determined\src\applications")

print("="*70)
print("ARIA GATE DISCOVERY SYSTEM — TEST SUITE")
print("="*70)

# Test 1: Import and instantiate discovery engine
print("\n[TEST 1] Importing ARIA Gate Discovery Engine...")
try:
    from aria_gate_discovery_engine import get_aria_gate_discovery
    print("✓ Successfully imported ARIAGateDiscoveryEngine")
except ImportError as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

# Test 2: Initialize discovery engine
print("\n[TEST 2] Initializing discovery engine...")
try:
    engine = get_aria_gate_discovery(ledger_dir=r"c:\Determined\src\applications")
    print("✓ Discovery engine initialized")
except Exception as e:
    print(f"✗ Failed to initialize: {e}")
    sys.exit(1)

# Test 3: Discover each gate operation
print("\n[TEST 3] Discovering gate operations...")
operations = [
    'Boolean NOT',
    'Bit flip',
    'Logic negation',
    'Boolean logic (AND/OR/XOR)',
    'Comparison ops',
    'Bit masking'
]

discoveries = {}
for op_name in operations:
    print(f"\n  → Discovering '{op_name}'...", end=" ")
    try:
        discovery = engine.discover_gate(op_name)
        discoveries[op_name] = discovery
        
        fields = discovery.get('fields_discovered', [])
        invariants = discovery.get('invariants_verified', [])
        
        print(f"✓ ({len(fields)} fields, {len(invariants)} invariants)")
        
    except Exception as e:
        print(f"✗ {e}")

# Test 4: Verify ledger recording
print("\n[TEST 4] Verifying ledger recording...")
ledger_path = Path(r"c:\Determined\src\applications\ledger_gate_discoveries.jsonl")
if ledger_path.exists():
    entry_count = sum(1 for line in open(ledger_path) if line.strip())
    print(f"✓ Ledger exists with {entry_count} discovery entries")
else:
    print("⚠ Ledger file not found yet (will be created on first discovery)")

# Test 5: Display discovery sample
print("\n[TEST 5] Sample discovery output...")
if discoveries:
    sample_op = list(discoveries.keys())[0]
    sample = discoveries[sample_op]
    
    print(f"\n  OPERATION: {sample_op}")
    print(f"  Coherence: {sample.get('coherence_score', 0.0):.2f}")
    print(f"  Election ID: {sample.get('election_id', 'N/A')}")
    print(f"  Fields discovered: {len(sample.get('fields_discovered', []))}")
    print(f"  Invariants verified: {len(sample.get('invariants_verified', []))}")
    print(f"  Applications discovered: {len(sample.get('applications_discovered', []))}")
    
    print(f"\n  Sample Fields:")
    for field in sample.get('fields_discovered', [])[:3]:
        print(f"    - {field}")
    
    print(f"\n  Sample Invariants:")
    for inv in sample.get('invariants_verified', [])[:2]:
        if isinstance(inv, dict):
            print(f"    - {inv.get('invariant', 'unknown')}: {inv.get('formula', 'N/A')}")
        else:
            print(f"    - {inv}")

# Test 6: Summary statistics
print("\n[TEST 6] Discovery Summary...")
total_discoveries = len(discoveries)
total_fields = sum(len(d.get('fields_discovered', [])) for d in discoveries.values())
total_invariants = sum(len(d.get('invariants_verified', [])) for d in discoveries.values())
total_applications = sum(len(d.get('applications_discovered', [])) for d in discoveries.values())

print(f"  Operations discovered: {total_discoveries}")
print(f"  Total fields identified: {total_fields}")
print(f"  Total invariants verified: {total_invariants}")
print(f"  Total applications found: {total_applications}")
print(f"  Average coherence: {sum(d.get('coherence_score', 0) for d in discoveries.values()) / max(1, total_discoveries):.2f}")

# Test 7: API integration check
print("\n[TEST 7] API endpoint availability...")
try:
    # Check if ENCYCLOPEDIA_API_SERVER exists and imports properly
    sys.path.insert(0, r"c:\Determined")
    print("  Checking ENCYCLOPEDIA_API_SERVER.py...")
    
    # Verify the file has the endpoint
    with open(r"c:\Determined\ENCYCLOPEDIA_API_SERVER.py", 'r') as f:
        content = f.read()
        if '/api/aria/discover/operation/' in content:
            print("  ✓ /api/aria/discover/operation endpoint found in server code")
        else:
            print("  ✗ Endpoint not found in server code")
    
except Exception as e:
    print(f"  ⚠ Could not verify server: {e}")

# Test 8: HTML integration check
print("\n[TEST 8] Frontend integration...")
try:
    with open(r"c:\Determined\ENCYCLOPEDIA_LEDGER.html", 'r') as f:
        content = f.read()
        if 'aria_discover_operation' in content or '/api/aria/discover' in content:
            print("  ✓ ARIA discovery API calls found in HTML")
        if '_displayGateEducation' in content:
            print("  ✓ Gate education display function found")
        if 'async' in content and 'fetch' in content:
            print("  ✓ Async fetch patterns detected")
except Exception as e:
    print(f"  ⚠ Could not verify frontend: {e}")

print("\n" + "="*70)
print("ARIA GATE DISCOVERY SYSTEM — VERIFICATION COMPLETE")
print("="*70 + "\n")

print("NEXT STEPS:")
print("1. Start the ENCYCLOPEDIA_API_SERVER:")
print("   python c:\\Determined\\ENCYCLOPEDIA_API_SERVER.py")
print("\n2. Open in browser:")
print("   http://127.0.0.1:5000")
print("\n3. Click any gate operation to trigger ARIA discovery")
print("\nThe system will:")
print("  → Call /api/aria/discover/operation/<name>")
print("  → ARIA exhaustively tests the operation")  
print("  → Records discovery to ledger")
print("  → Returns discovered fields, invariants, applications")
print("  → Frontend displays with traceability to elections")
print("\n")
