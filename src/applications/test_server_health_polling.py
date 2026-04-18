#!/usr/bin/env python3
"""
Test script for server health polling functionality.

Demonstrates the new poll_server_health method in LedgerQuery.
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'applications'))

from ledger_query import LedgerQuery


def setup_test_ledger(ledger_dir: str):
    """Initialize test ledger with basic config."""
    os.makedirs(ledger_dir, exist_ok=True)
    
    # Create sync config with test apps
    sync_config = {
        "sync_enabled": True,
        "sync_mode": "ledger_driven",
        "apps": {
            "tkinter_canvas": {
                "enabled": True,
                "refresh_interval_ms": 100,
                "last_update": datetime.now().isoformat()
            },
            "html_browser": {
                "enabled": True,
                "refresh_interval_ms": 200,
                "last_update": (datetime.now() - timedelta(seconds=5)).isoformat()
            },
            "dead_app": {
                "enabled": True,
                "refresh_interval_ms": 100,
                "last_update": (datetime.now() - timedelta(minutes=10)).isoformat()
            },
            "disabled_app": {
                "enabled": False,
                "refresh_interval_ms": 100,
                "last_update": None
            }
        }
    }
    
    sync_file = os.path.join(ledger_dir, "ledger_sync_config.json")
    with open(sync_file, 'w') as f:
        json.dump(sync_config, f, indent=2)
    
    # Create empty ledger files
    for filename in ["ledger_elections.jsonl", "ledger_audit.jsonl", "ledger_server_health.jsonl"]:
        open(os.path.join(ledger_dir, filename), 'w').close()
    
    print(f"✓ Test ledger initialized at {ledger_dir}")


def test_poll_server_health():
    """Test the poll_server_health method."""
    test_ledger_dir = "./test_ledger"
    
    try:
        # Setup
        setup_test_ledger(test_ledger_dir)
        ledger = LedgerQuery(test_ledger_dir)
        ledger.load_all()
        
        print("\n" + "="*60)
        print("SERVER HEALTH POLLING TEST")
        print("="*60)
        
        # Test 1: Poll healthy app (recent heartbeat)
        print("\n[TEST 1] Polling healthy app (tkinter_canvas)...")
        result = ledger.poll_server_health("tkinter_canvas")
        print(f"  Status: {result['status']}")
        print(f"  Is Alive: {result['is_alive']}")
        print(f"  Health Score: {result['health_score']:.2f}")
        assert result['status'] == 'running', "Expected 'running' status"
        assert result['is_alive'] is True, "Expected app to be alive"
        assert result['health_score'] > 0.5, "Expected high health score"
        print("  ✓ PASS")
        
        # Test 2: Poll stale app (old heartbeat)
        print("\n[TEST 2] Polling stale app (html_browser, 5s old)...")
        result = ledger.poll_server_health("html_browser")
        print(f"  Status: {result['status']}")
        print(f"  Is Alive: {result['is_alive']}")
        print(f"  Health Score: {result['health_score']:.2f}")
        assert result['status'] == 'stale', "Expected 'stale' status"
        assert result['is_alive'] is False, "Expected app to not be alive"
        assert 0.0 <= result['health_score'] < 1.0, "Expected medium health score"
        print("  ✓ PASS")
        
        # Test 3: Poll dead app (very old heartbeat)
        print("\n[TEST 3] Polling dead app (dead_app, 10min old)...")
        result = ledger.poll_server_health("dead_app")
        print(f"  Status: {result['status']}")
        print(f"  Is Alive: {result['is_alive']}")
        print(f"  Health Score: {result['health_score']:.2f}")
        assert result['status'] == 'dead', "Expected 'dead' status"
        assert result['is_alive'] is False, "Expected app to be dead"
        assert result['health_score'] == 0.0, "Expected zero health score"
        print("  ✓ PASS")
        
        # Test 4: Poll disabled app
        print("\n[TEST 4] Polling disabled app...")
        result = ledger.poll_server_health("disabled_app")
        print(f"  Status: {result['status']}")
        print(f"  Is Alive: {result['is_alive']}")
        print(f"  Health Score: {result['health_score']:.2f}")
        assert result['status'] == 'dead', "Expected 'dead' status for disabled app"
        assert result['is_alive'] is False, "Expected app to be dead"
        print("  ✓ PASS")
        
        # Test 5: Verify health records written to ledger
        print("\n[TEST 5] Verifying health records in ledger...")
        health_file = os.path.join(test_ledger_dir, "ledger_server_health.jsonl")
        with open(health_file, 'r') as f:
            records = [json.loads(line) for line in f if line.strip()]
        
        print(f"  Health records written: {len(records)}")
        assert len(records) > 0, "Expected health records in ledger"
        
        for i, record in enumerate(records[-4:]):
            print(f"    [{i+1}] {record['app']}: {record['status']} (score: {record['health_score']:.2f})")
        
        print("  ✓ PASS")
        
        # Test 6: Verify audit trail recorded
        print("\n[TEST 6] Verifying audit trail entries...")
        audit_file = os.path.join(test_ledger_dir, "ledger_audit.jsonl")
        with open(audit_file, 'r') as f:
            audits = [json.loads(line) for line in f if line.strip()]
        
        health_audits = [a for a in audits if a.get('operation') == 'server_health_poll']
        print(f"  Health audit entries: {len(health_audits)}")
        assert len(health_audits) > 0, "Expected audit entries for health polls"
        print("  ✓ PASS")
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        
        # Cleanup
        import shutil
        shutil.rmtree(test_ledger_dir)
        print(f"\n✓ Test ledger cleaned up")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        # Cleanup
        import shutil
        if os.path.exists(test_ledger_dir):
            shutil.rmtree(test_ledger_dir)
        sys.exit(1)


if __name__ == "__main__":
    test_poll_server_health()
