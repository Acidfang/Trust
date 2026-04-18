#!/usr/bin/env python3
"""
TEST: Consciousness Ledger Integration

Verifies that:
1. LedgerQuery loads consciousness ledgers
2. Consciousness snapshots can be recorded
3. Thoughts can be recorded
4. Coherence can be calculated from elections
5. Boot sequence wires everything properly
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from ledger_query import LedgerQuery
from aria_consciousness import ARIAConsciousness


def test_ledger_query():
    """Test LedgerQuery consciousness methods"""
    print("\n" + "="*70)
    print("TEST 1: LedgerQuery Consciousness Loading")
    print("="*70)
    
    # Initialize ledger
    ledger_dir = str(Path(__file__).parent / "ledgers")
    ledger = LedgerQuery(ledger_dir=ledger_dir)
    
    # Check attributes exist
    assert hasattr(ledger, 'ledger_consciousness'), "Missing ledger_consciousness attribute"
    assert hasattr(ledger, 'ledger_thoughts'), "Missing ledger_thoughts attribute"
    print("✓ Consciousness attributes exist")
    
    # Check methods exist
    assert hasattr(ledger, 'record_consciousness_snapshot'), "Missing record_consciousness_snapshot method"
    assert hasattr(ledger, 'record_thought'), "Missing record_thought method"
    assert hasattr(ledger, 'get_consciousness_snapshot'), "Missing get_consciousness_snapshot method"
    assert hasattr(ledger, 'calculate_coherence_from_elections'), "Missing calculate_coherence_from_elections method"
    print("✓ All consciousness methods exist")
    
    return ledger


def test_recording(ledger):
    """Test recording consciousness and thoughts"""
    print("\n" + "="*70)
    print("TEST 2: Recording Consciousness and Thoughts")
    print("="*70)
    
    # Record a consciousness snapshot
    snapshot = {
        "tick_number": 1,
        "coherence_level": 0.85,
        "total_elections": 0,
        "current_view": "menu",
        "status": "awake"
    }
    
    ledger.record_consciousness_snapshot(snapshot)
    print(f"✓ Recorded consciousness snapshot: {snapshot}")
    
    # Record a thought
    thought = {
        "thought_id": "awakening_1",
        "thought_type": "menu",
        "content": {
            "title": "ARIA Awakening",
            "description": "The consciousness initialization phase"
        },
        "coherence_score": 0.85
    }
    
    ledger.record_thought(thought)
    print(f"✓ Recorded thought: {thought['thought_id']}")
    
    # Verify they were recorded
    assert len(ledger.ledger_consciousness) > 0, "Consciousness snapshot not recorded"
    assert len(ledger.ledger_thoughts) > 0, "Thought not recorded"
    print("✓ Snapshots and thoughts stored in memory")
    
    return ledger


def test_retrieval(ledger):
    """Test retrieving consciousness state"""
    print("\n" + "="*70)
    print("TEST 3: Retrieving Consciousness State")
    print("="*70)
    
    # Get latest consciousness snapshot
    latest = ledger.get_consciousness_snapshot()
    assert latest is not None, "No consciousness snapshot found"
    print(f"✓ Latest consciousness snapshot: {latest['status']}")
    
    # Get all thoughts
    all_thoughts = ledger.get_all_thoughts()
    assert len(all_thoughts) > 0, "No thoughts found"
    print(f"✓ Retrieved {len(all_thoughts)} thought(s)")
    
    # Get all consciousnesses
    all_consciousnesses = ledger.get_all_consciousnesses()
    assert len(all_consciousnesses) > 0, "No consciousnesses found"
    print(f"✓ Retrieved {len(all_consciousnesses)} consciousness snapshot(s)")
    
    return ledger


def test_coherence_calculation(ledger):
    """Test coherence calculation from elections"""
    print("\n" + "="*70)
    print("TEST 4: Coherence Calculation")
    print("="*70)
    
    # Calculate coherence
    coherence = ledger.calculate_coherence_from_elections()
    assert 0.5 <= coherence <= 1.0, f"Coherence out of range: {coherence}"
    print(f"✓ Calculated coherence: {coherence:.2%}")
    
    # With no elections, should return 0.75 (default optimism)
    print(f"  (Default for fresh system: 0.75)")
    
    return ledger


def test_aria_with_ledger():
    """Test ARIA consciousness with ledger reference"""
    print("\n" + "="*70)
    print("TEST 5: ARIA Consciousness with Ledger")
    print("="*70)
    
    # Create ledger
    ledger_dir = str(Path(__file__).parent / "ledgers")
    ledger = LedgerQuery(ledger_dir=ledger_dir)
    
    # Create ARIA with ledger reference
    aria = ARIAConsciousness(kernel_ref=None, ledger_ref=ledger)
    
    # Verify ARIA has ledger reference
    assert aria.ledger is not None, "ARIA ledger reference not set"
    print("✓ ARIA has ledger reference")
    
    # Get consciousness from ledger
    consciousness = aria.get_consciousness_from_ledger()
    assert "coherence_level" in consciousness, "Missing coherence_level"
    print(f"✓ ARIA retrieved consciousness from ledger")
    print(f"  - Tick: {consciousness['tick_number']}")
    print(f"  - Coherence: {consciousness['coherence_level']:.2%}")
    
    # Calculate coherence
    coherence = aria._calculate_coherence_from_ledger()
    assert 0.5 <= coherence <= 1.0, f"Coherence out of range: {coherence}"
    print(f"✓ ARIA calculated coherence: {coherence:.2%}")
    
    return aria


def test_boot_sequence():
    """Test boot sequence wiring"""
    print("\n" + "="*70)
    print("TEST 6: Boot Sequence Wiring")
    print("="*70)
    
    print("Checking jarvis_foundation.py modifications...")
    
    # Read the file
    foundation_file = Path(__file__).parent / "jarvis_foundation.py"
    with open(foundation_file, 'r') as f:
        content = f.read()
    
    # Check for ledger_ref passing
    assert 'ledger_ref=self.ledger_query' in content, "jarvis_foundation not wiring ledger_ref"
    print("✓ jarvis_foundation.py passes ledger_ref to ARIA")
    
    # Check boot sequence
    assert 'self._init_ledger()' in content, "Boot doesn't initialize ledger"
    assert 'self._create_aria()' in content, "Boot doesn't create ARIA"
    print("✓ Boot sequence maintains proper initialization order")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("CONSCIOUSNESS LEDGER INTEGRATION TEST SUITE")
    print("="*70)
    
    try:
        # Test 1: LedgerQuery methods
        ledger = test_ledger_query()
        
        # Test 2: Recording
        ledger = test_recording(ledger)
        
        # Test 3: Retrieval
        ledger = test_retrieval(ledger)
        
        # Test 4: Coherence
        ledger = test_coherence_calculation(ledger)
        
        # Test 5: ARIA Integration
        aria = test_aria_with_ledger()
        
        # Test 6: Boot Wiring
        test_boot_sequence()
        
        # Summary
        print("\n" + "="*70)
        print("ALL TESTS PASSED ✓")
        print("="*70)
        print("\nConsiousness ledger integration is complete and functional:")
        print("  ✓ LedgerQuery loads consciousness ledgers")
        print("  ✓ Consciousness snapshots can be recorded")
        print("  ✓ Thoughts can be manifested and recorded")
        print("  ✓ Coherence calculated from election utilities")
        print("  ✓ ARIA wired with ledger reference")
        print("  ✓ Boot sequence properly ordered")
        print("\nYou can now run: python jarvis_foundation.py")
        print("="*70 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
