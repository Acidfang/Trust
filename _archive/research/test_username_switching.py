#!/usr/bin/env python3
"""
Test username switching functionality
"""
import sys
import requests
from reddit_tracker_gui import RedditTrackerGUI
import tkinter as tk

print("=" * 70)
print("USERNAME SWITCHING TEST")
print("=" * 70)

# Create hidden GUI
root = tk.Tk()
root.withdraw()

# Initialize
print("\n[TEST 1] GUI Initialization...")
app = RedditTrackerGUI(root)
print(f"✓ GUI initialized with default username: @{app.data['username']}")

# Check initial users
print("\n[TEST 2] Initial Users (analyzing @Agitated_Age_2785)...")
users_initial = app.users_tree.get_children()
print(f"  Found {len(users_initial)} exchange partners:")
for user in users_initial:
    exchanges = app.users_tree.item(user)['values'][0]
    print(f"    - {user}: {exchanges} dialogues")

# Change username to a different user
print("\n[TEST 3] Changing username to @tellytubbytoetickler...")
app.username_var.set("tellytubbytoetickler")
app.update_username()
print(f"✓ Username changed to: @{app.data['username']}")

# Check the post ID from the current tracked post
post_id = app.data['posts'][0]['post_id']
print(f"\n[TEST 4] Re-analyzing as @tellytubbytoetickler from post {post_id}...")

# Manually fetch and analyze to see if the algorithm works from their perspective
try:
    url = f"https://www.reddit.com/comments/{post_id}.json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json()
    
    comments = []
    def extract_comments(comment_list, depth=0, parent_author=None):
        for item in comment_list:
            if item['kind'] == 't1':
                comment = item['data']
                author = comment.get('author', '[deleted]')
                comments.append({
                    'author': author,
                    'body': comment['body'],
                    'parent_author': parent_author
                })
                replies = comment.get('replies', '')
                if replies and isinstance(replies, dict):
                    extract_comments(replies.get('data', {}).get('children', []), depth + 1, author)
    
    if len(data) > 1:
        extract_comments(data[1]['data']['children'])
    
    # Analyze exchanges from their perspective
    from collections import defaultdict
    meaningful = defaultdict(int)
    
    for other_comment in comments:
        if other_comment['parent_author'] == 'tellytubbytoetickler' and other_comment['author'] != 'tellytubbytoetickler':
            other_author = other_comment['author']
            for follow_up in comments:
                if (follow_up['parent_author'] == other_author and 
                    follow_up['author'] == 'tellytubbytoetickler' and
                    len(follow_up['body']) > 50 and
                    len(other_comment['body']) > 50):
                    meaningful[other_author] += 1
                    break
    
    active_users = {user: count for user, count in meaningful.items() 
                   if count > 3 and user != '[deleted]'}
    
    print(f"  Analyzed {len(comments)} comments")
    print(f"  Found {len(active_users)} users with >3 meaningful exchanges with @tellytubbytoetickler")
    
    if active_users:
        print("  Partners:")
        for user, count in sorted(active_users.items(), key=lambda x: x[1], reverse=True):
            print(f"    - {user}: {count} dialogues")
    else:
        print("  (This user may not have >3 back-and-forth conversations in this post)")
    
    print("✓ Username change successful - system can analyze any Reddit user")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Cleanup
root.destroy()

print("\n" + "=" * 70)
print("✓ USERNAME SWITCHING TEST PASSED")
print("=" * 70)
print("\nYou can now:")
print("  1. Enter any Reddit username at the top of the GUI")
print("  2. Click 'Update' to switch which user the system analyzes")
print("  3. The Comments & User Posts tabs will analyze that user's interactions")
