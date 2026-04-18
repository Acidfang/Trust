#!/usr/bin/env python3
"""
Test the User Posts tab directly without opening the full GUI
"""
import sys
import json
import os
from reddit_tracker_gui import RedditTrackerGUI
import tkinter as tk

print("=" * 70)
print("USER POSTS TAB FUNCTIONALITY TEST")
print("=" * 70)

# Create a dummy root (but don't display it)
root = tk.Tk()
root.withdraw()  # Hide the window

# Create GUI instance
print("\n[TEST 1] Initializing GUI...")
try:
    app = RedditTrackerGUI(root)
    print("✓ GUI initialized")
except Exception as e:
    print(f"✗ GUI init failed: {e}")
    sys.exit(1)

# Check if data loaded
print("\n[TEST 2] Checking tracked posts...")
posts = app.data.get('posts', [])
print(f"  Tracked posts: {len(posts)}")
if posts:
    for p in posts:
        print(f"    - {p['post_id']}: {p.get('title', 'Untitled')[:50]}")
else:
    print("  ✗ NO POSTS TRACKED")
    sys.exit(1)

# Check if post combo was populated
print("\n[TEST 3] Checking post combo box...")
combo_values = app.post_combo['values']
print(f"  Combo values: {len(combo_values)}")
print(f"  Values: {combo_values}")
if combo_values:
    print("✓ Post combo populated")
else:
    print("✗ Post combo is empty!")

# Check if users tree was populated
print("\n[TEST 4] Checking users tree...")
users = app.users_tree.get_children()
print(f"  Users in tree: {len(users)}")
if users:
    for user in users:
        exchanges = app.users_tree.item(user)['values']
        print(f"    - {user}: {exchanges[0]} dialogues")
    print("✓ Users tree populated")
else:
    print("✗ Users tree is EMPTY!")
    
    # Check what's in the users_text widget
    text_content = app.users_text.get('1.0', tk.END)
    print(f"\n  Text widget content:\n{text_content}")

# Clean up
root.destroy()

print("\n" + "=" * 70)
if users:
    print("✓ TEST PASSED - User Posts tab is working")
else:
    print("✗ TEST FAILED - User Posts tab is not populating users")
    sys.exit(1)
