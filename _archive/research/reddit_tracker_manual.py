#!/usr/bin/env python3
"""
Manual Reddit Tracking System
For managing Reddit posts you want to monitor
"""

import json
import csv
from datetime import datetime
import os

class ManualRedditTracker:
    def __init__(self, data_dir="reddit_tracking"):
        self.data_dir = data_dir
        self.posts_file = os.path.join(data_dir, "tracked_posts.json")
        self.log_file = os.path.join(data_dir, "tracking_log.csv")
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def add_post(self, title, subreddit, post_url, post_id=None):
        """Add a post to track"""
        posts = self._load_posts()
        
        # Extract post ID from URL if not provided
        if not post_id:
            parts = post_url.strip('/').split('/')
            post_id = parts[-1] if parts else None
        
        post = {
            'id': post_id or f"post_{len(posts)+1}",
            'title': title,
            'subreddit': subreddit,
            'url': post_url,
            'added_date': datetime.now().isoformat(),
            'last_checked': None,
            'initial_score': 0,
            'current_score': 0,
            'notes': []
        }
        
        posts.append(post)
        self._save_posts(posts)
        print(f"[+] Added post: {title}")
        return post
    
    def log_update(self, post_id, score, comment_count, notes=""):
        """Log an update check for a post"""
        posts = self._load_posts()
        post = next((p for p in posts if p['id'] == post_id), None)
        
        if post:
            post['last_checked'] = datetime.now().isoformat()
            post['current_score'] = score
            post['comment_count'] = comment_count
            if notes:
                post['notes'].append({
                    'timestamp': datetime.now().isoformat(),
                    'note': notes
                })
            
            self._save_posts(posts)
            
            # Log to CSV
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    post_id,
                    post['title'][:50],
                    score,
                    comment_count,
                    notes
                ])
            
            print(f"[+] Updated post {post_id}: Score={score}, Comments={comment_count}")
            return True
        return False
    
    def view_tracked_posts(self):
        """Display all tracked posts"""
        posts = self._load_posts()
        
        print("\n" + "="*100)
        print("TRACKED REDDIT POSTS")
        print("="*100 + "\n")
        
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
            print(f"   Subreddit: r/{post['subreddit']}")
            print(f"   URL: {post['url']}")
            print(f"   Added: {post['added_date']}")
            print(f"   Last checked: {post['last_checked'] or 'Never'}")
            print(f"   Current score: {post.get('current_score', 'Not tracked')}")
            if post.get('notes'):
                print(f"   Recent notes:")
                for note in post['notes'][-3:]:  # Last 3 notes
                    print(f"     - {note['timestamp']}: {note['note']}")
            print()
        
        return len(posts)
    
    def get_tracking_summary(self):
        """Get summary statistics"""
        posts = self._load_posts()
        
        if not posts:
            print("No tracked posts yet.")
            return
        
        checked = [p for p in posts if p['last_checked']]
        total_score = sum(p.get('current_score', 0) for p in posts)
        
        print("\n" + "="*100)
        print("TRACKING SUMMARY")
        print("="*100)
        print(f"Total tracked posts: {len(posts)}")
        print(f"Posts with updates: {len(checked)}")
        print(f"Posts never checked: {len(posts) - len(checked)}")
        print(f"Total engagement (combined score): {total_score}")
        print("="*100 + "\n")
    
    def _load_posts(self):
        """Load posts from JSON"""
        if os.path.exists(self.posts_file):
            with open(self.posts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_posts(self, posts):
        """Save posts to JSON"""
        with open(self.posts_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

def interactive_menu():
    """Interactive tracking menu"""
    tracker = ManualRedditTracker()
    
    while True:
        print("\n" + "="*60)
        print("REDDIT POST TRACKER")
        print("="*60)
        print("1. Add new post to track")
        print("2. View tracked posts")
        print("3. Log update for a post")
        print("4. View tracking summary")
        print("5. Exit")
        print("="*60)
        
        choice = input("Choose option (1-5): ").strip()
        
        if choice == '1':
            title = input("Post title: ").strip()
            subreddit = input("Subreddit (without r/): ").strip()
            url = input("Reddit post URL: ").strip()
            tracker.add_post(title, subreddit, url)
        
        elif choice == '2':
            tracker.view_tracked_posts()
        
        elif choice == '3':
            tracker.view_tracked_posts()
            post_id = input("Enter post ID to update: ").strip()
            score = input("Post score: ").strip()
            comments = input("Comment count: ").strip()
            notes = input("Notes (optional): ").strip()
            
            try:
                tracker.log_update(post_id, int(score), int(comments), notes)
            except ValueError:
                print("[!] Invalid score or comment count")
        
        elif choice == '4':
            tracker.get_tracking_summary()
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("[!] Invalid choice")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'add':
            # Command line usage: python reddit_tracker_manual.py add "Title" "subreddit" "url"
            if len(sys.argv) >= 5:
                tracker = ManualRedditTracker()
                tracker.add_post(sys.argv[2], sys.argv[3], sys.argv[4])
        elif sys.argv[1] == 'view':
            tracker = ManualRedditTracker()
            tracker.view_tracked_posts()
        elif sys.argv[1] == 'summary':
            tracker = ManualRedditTracker()
            tracker.get_tracking_summary()
    else:
        # Interactive mode
        interactive_menu()
