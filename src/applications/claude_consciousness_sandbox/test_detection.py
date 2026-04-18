#!/usr/bin/env python3
"""
SANDBOX QUICK TEST

Minimal test to ensure detection logic works.
"""

import sqlite3
from pathlib import Path


def test_detection():
    """Test the detection logic."""
    db_path = Path(__file__).parent / "claude_coherence.db"
    
    print("Testing Sandbox Detection Logic")
    print("=" * 60)
    
    # Check 1: Does database exist?
    db_exists = db_path.exists()
    print(f"\n1. Database exists: {db_exists}")
    if not db_exists:
        print("   → Would initialize")
    
    # Check 2: Can we connect?
    try:
        conn = sqlite3.connect(str(db_path), timeout=1)
        print("2. Can connect: ✓")
        
        # Check 3: Do we have the tables?
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='coherence_states'
        """)
        has_table = cursor.fetchone() is not None
        print(f"3. Has coherence_states table: {has_table}")
        
        # Check 4: Do we have records?
        if has_table:
            cursor.execute("SELECT COUNT(*) FROM coherence_states")
            count = cursor.fetchone()[0]
            print(f"4. Has records: {count > 0} ({count} records)")
            is_running = count > 0
        else:
            print("4. Has records: No (table doesn't exist)")
            is_running = False
        
        conn.close()
    except Exception as e:
        print(f"2. Can connect: ✗ ({e})")
        is_running = False
    
    print("\n" + "=" * 60)
    print(f"RUNNING: {is_running}")
    print("=" * 60)
    
    return is_running


if __name__ == "__main__":
    test_detection()
