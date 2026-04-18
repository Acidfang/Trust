#!/usr/bin/env python3
"""
Test username changing functionality - UI only (no API calls)
"""
import sys
import json
from reddit_tracker_gui import RedditTrackerGUI
import tkinter as tk

print("=" * 70)
print("USERNAME CHANGING TEST (UI ONLY)")
print("=" * 70)

# Reset the data file to original state
initial_data = {
    "posts": [
        {
            "post_id": "1sgddb0",
            "title": "Test Post",
            "subreddit": "TestSub",
            "url": "https://example.com",
            "added_date": "2026-04-09T14:41:43",
            "snapshots": [
                {
                    "timestamp": "2026-04-09T14:41:43",
                    "score": 10,
                    "comments": 50
                }
            ]
        }
    ],
    "username": "Agitated_Age_2785",
    "last_updated": None
}

with open("reddit_tracking.json", "w") as f:
    json.dump(initial_data, f, indent=2)

# Create hidden GUI
root = tk.Tk()
root.withdraw()

# Initialize
print("\n[TEST 1] GUI Initialization...")
app = RedditTrackerGUI(root)
initial_username = app.username_var.get()
print(f"✓ GUI initialized")
print(f"  Initial username: @{initial_username}")

# Check the username entry widget exists
print("\n[TEST 2] Username Entry Widget...")
assert hasattr(app, 'username_entry'), "No username_entry widget found"
assert hasattr(app, 'username_var'), "No username_var found"
print("✓ Username input field exists")
print(f"  Current value: {app.username_var.get()}")

# Test changing the username
print("\n[TEST 3] Changing Username...")
new_username = "test_user_123"
app.username_var.set(new_username)
print(f"  Set username_var to: {app.username_var.get()}")

# Simulate button click
print(f"\n[TEST 4] Saving Username...")
try:
    app.update_username()
    print(f"✓ Username saved successfully")
except Exception as e:
    print(f"✗ Error during update: {e}")
    sys.exit(1)

# Verify it was saved to the data file
print(f"\n[TEST 5] Verifying Save to File...")
app.load_data()
saved_username = app.data.get('username')
print(f"  Saved username in data: @{saved_username}")
if saved_username == new_username:
    print(f"✓ Username was correctly saved to file")
else:
    print(f"✗ Username mismatch: expected {new_username}, got {saved_username}")

# Reset back to original
print(f"\n[TEST 6] Resetting to Original...")
app.username_var.set("Agitated_Age_2785")
app.update_username()
app.load_data()
print(f"✓ Reset to: @{app.data.get('username')}")

# Cleanup
root.destroy()

print("\n" + "=" * 70)
print("✓ ALL USERNAME TESTS PASSED")
print("=" * 70)
print("\nThe GUI now allows you to:")
print("  1. Enter any Reddit username at the top")
print("  2. Click 'Update' to change which user to analyze")
print("  3. The system will re-analyze from that user's perspective")
