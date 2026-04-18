#!/usr/bin/env python3
"""
Simple GUI import test
"""
import json
import sys

print("Testing reddit_tracker_gui.py...")
print("=" * 70)

try:
    # Test data
    print("[TEST 1] Data file...")
    with open('reddit_tracking.json', 'r') as f:
        data = json.load(f)
    print("  ✓ JSON valid")
    print(f"  ✓ {len(data['posts'])} posts loaded")
    
    # Test imports
    print("\n[TEST 2] Imports...")
    import tkinter as tk
    print("  ✓ tkinter")
    from tkinter import ttk, messagebox, scrolledtext
    print("  ✓ tkinter submodules")
    import requests
    print("  ✓ requests") 
    from datetime import datetime
    print("  ✓ datetime")
    
    # Test GUI module
    print("\n[TEST 3] GUI module...")
    from reddit_tracker_gui import RedditTrackerGUI
    print("  ✓ reddit_tracker_gui imports successfully")
    
    # Test instantiation
    print("\n[TEST 4] GUI initialization...")
    root = tk.Tk()
    root.withdraw()
    
    app = RedditTrackerGUI(root)
    print(f"  ✓ GUI instantiated")
    print(f"  ✓ {len(app.data['posts'])} posts in GUI")
    
    root.destroy()
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED - GUI IS FUNCTIONAL")
    print("=" * 70)

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
