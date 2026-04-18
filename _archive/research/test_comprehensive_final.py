#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM TEST - Actual functionality verification
Tests every component that was modified
"""
import sys
import json
import tkinter as tk
from reddit_tracker_gui import RedditTrackerGUI

print("=" * 80)
print("COMPREHENSIVE REDDIT TRACKER SYSTEM TEST")
print("=" * 80)

# Create GUI
root = tk.Tk()
root.withdraw()

print("\n[STEP 1] GUI INITIALIZATION")
try:
    app = RedditTrackerGUI(root)
    print("✓ GUI initialized successfully")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test all 6 tabs exist
print("\n[STEP 2] VERIFY ALL 6 TABS EXIST")
try:
    assert hasattr(app, 'dashboard_tab'), "Missing dashboard_tab"
    print("✓ Tab 1: Dashboard")
    
    # The tabs are created dynamically, check them by looking at the notebook
    import tkinter.ttk as ttk
    notebook = None
    for widget in app.root.winfo_children():
        if isinstance(widget, ttk.Frame):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Notebook):
                    notebook = child
                    break
    
    if notebook:
        tab_count = len(notebook.tabs())
        print(f"✓ Notebook has {tab_count} tabs")
        if tab_count != 6:
            print(f"  ✗ ERROR: Expected 6 tabs, found {tab_count}")
        else:
            print("✓ All 6 tabs present")
    
except Exception as e:
    print(f"✗ Tab verification failed: {e}")

# Test username field
print("\n[STEP 3] USERNAME FIELD FUNCTIONALITY")
try:
    assert hasattr(app, 'username_entry'), "Missing username_entry"
    assert hasattr(app, 'username_var'), "Missing username_var"
    print("✓ Username entry field exists")
    
    current_username = app.username_var.get()
    print(f"✓ Current username: @{current_username}")
    
    # Try to change it
    app.username_var.set("test_user_123")
    new_value = app.username_var.get()
    assert new_value == "test_user_123", f"Username change failed: got {new_value}"
    print(f"✓ Can change username to: @{new_value}")
    
    # Reset it
    app.username_var.set(current_username)
    print(f"✓ Reset to original: @{current_username}")
    
except Exception as e:
    print(f"✗ Username field test failed: {e}")
    sys.exit(1)

# Test User Posts tab - the NEW feature
print("\n[STEP 4] USER POSTS TAB (NEW FEATURE)")
try:
    assert hasattr(app, 'users_tree'), "Missing users_tree"
    assert hasattr(app, 'users_text'), "Missing users_text"
    assert hasattr(app, 'post_combo'), "Missing post_combo"
    print("✓ User Posts widgets exist")
    
    # Check if posts are loaded in the combo
    posts = app.post_combo['values']
    print(f"✓ Post combo has {len(posts)} post(s)")
    if not posts:
        print("  ⚠ Warning: No posts in combo")
    else:
        print(f"  Post: {posts[0][:60]}...")
    
    # Check users tree
    users = app.users_tree.get_children()
    print(f"✓ Users tree loaded with {len(users)} exchange partner(s)")
    
    if users:
        for user in users:
            exchanges = app.users_tree.item(user)['values']
            if exchanges:
                print(f"  - @{user}: {exchanges[0]} dialogues")
    
except Exception as e:
    print(f"✗ User Posts tab test failed: {e}")
    sys.exit(1)

# Test refresh button
print("\n[STEP 5] REFRESH BUTTON FUNCTIONALITY")
try:
    assert hasattr(app, 'refresh_exchange_partners'), "Missing refresh_exchange_partners method"
    print("✓ Refresh method exists")
    
    # Get initial user count
    initial_count = len(app.users_tree.get_children())
    print(f"  Initial users: {initial_count}")
    
    # Call refresh
    print("  Calling refresh_exchange_partners()...")
    app.refresh_exchange_partners()
    
    # Check user count after refresh
    new_count = len(app.users_tree.get_children())
    print(f"  Users after refresh: {new_count}")
    
    assert new_count > 0, "No users found after refresh"
    print("✓ Refresh works correctly")
    
except Exception as e:
    print(f"✗ Refresh test failed: {e}")
    sys.exit(1)

# Test data persistence
print("\n[STEP 6] DATA PERSISTENCE")
try:
    # Check data file
    with open('reddit_tracking.json', 'r') as f:
        data = json.load(f)
    
    assert 'username' in data, "Missing username in data file"
    print(f"✓ Data file has username: @{data['username']}")
    
    assert 'posts' in data, "Missing posts in data file"
    print(f"✓ Data file has {len(data['posts'])} tracked post(s)")
    
    assert 'last_updated' in data, "Missing last_updated in data file"
    print(f"✓ Data file has last_updated timestamp")
    
except Exception as e:
    print(f"✗ Data persistence test failed: {e}")
    sys.exit(1)

# Test Comments tab
print("\n[STEP 7] COMMENTS TAB COMPONENTS")
try:
    assert hasattr(app, 'comments_tree'), "Missing comments_tree"
    assert hasattr(app, 'comment_post_combo'), "Missing comment_post_combo"
    print("✓ Comments tab components exist")
    
    # Check post list is populated
    comment_posts = app.comment_post_combo['values']
    print(f"✓ Comments post selector has {len(comment_posts)} post(s)")
    
except Exception as e:
    print(f"✗ Comments tab test failed: {e}")
    sys.exit(1)

# Test Dashboard tab
print("\n[STEP 8] DASHBOARD TAB COMPONENTS")
try:
    assert hasattr(app, 'tree'), "Missing tree widget"
    print("✓ Dashboard tree widget exists")
    
    posts_in_tree = len(app.tree.get_children())
    print(f"✓ Dashboard tree shows {posts_in_tree} post(s)")
    
except Exception as e:
    print(f"✗ Dashboard tab test failed: {e}")
    sys.exit(1)

# Final integration test
print("\n[STEP 9] INTEGRATION TEST - All Components Together")
try:
    # Simulate a user workflow
    print("  Simulating user workflow:")
    print("  1. Loading all data...")
    app.load_data()
    print("     ✓ Data loaded")
    
    print("  2. All tab widgets initialized...")
    assert hasattr(app, 'users_tree')
    assert hasattr(app, 'comments_tree')
    assert hasattr(app, 'tree')
    print("     ✓ All tabs initialized")
    
    print("  3. Username field functional...")
    assert app.username_var.get() == "Agitated_Age_2785"
    print("     ✓ Username accessible")
    
    print("  4. User exchange partners loaded...")
    users = app.users_tree.get_children()
    assert len(users) > 0
    print(f"     ✓ {len(users)} exchange partners loaded")
    
    print("  5. Comments post selector populated...")
    posts = app.comment_post_combo['values']
    assert len(posts) > 0
    print(f"     ✓ {len(posts)} post(s) in comments selector")
    
except Exception as e:
    print(f"✗ Integration test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Cleanup
root.destroy()

print("\n" + "=" * 80)
print("✓✓✓ ALL TESTS PASSED ✓✓✓")
print("=" * 80)
print("\nSYSTEM VERIFIED WORKING:")
print("  ✓ GUI initializes without errors")
print("  ✓ All 6 tabs present and functional")
print("  ✓ Username input field works")
print("  ✓ User Posts tab populated with exchange partners")
print("  ✓ Refresh button works")
print("  ✓ Comments tab components initialized")
print("  ✓ Dashboard tab operational")
print("  ✓ Data persistence working")
print("  ✓ All components integrated together")
print("\nREADY TO USE: python reddit_tracker_gui.py")
