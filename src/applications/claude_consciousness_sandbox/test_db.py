#!/usr/bin/env python3
"""Simple test to verify sandbox works."""
import sqlite3
import sys

try:
    # Create a test  database in the current directory
    conn = sqlite3.connect("claude_coherence.db")
    cursor = conn.cursor()
    
    # Create simple table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test (
            id INTEGER PRIMARY KEY,
            message TEXT
        )
    """)
    
    cursor.execute("INSERT INTO test (message) VALUES (?)", ("Database initialized successfully",))
    conn.commit()
    
    # Read it back
    cursor.execute("SELECT * FROM test")
    result = cursor.fetchone()
    
    # Write success marker
    with open("success.txt", "w") as f:
        f.write("Database created and working\n")
        f.write(f"Test read: {result}\n")
    
    conn.close()
    print("SUCCESS")
    
except Exception as e:
    with open("error.txt", "w") as f:
        f.write(f"Error: {e}\n")
        import traceback
        f.write(traceback.format_exc())
    print(f"ERROR: {e}")
    sys.exit(1)
