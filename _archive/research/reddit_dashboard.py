#!/usr/bin/env python3
"""
Reddit Tracking Dashboard
Monitor your posts and engagement over time
"""

import json
import os
from datetime import datetime
from pathlib import Path

class RedditTrackingDashboard:
    def __init__(self, tracking_file="reddit_tracking.json"):
        self.tracking_file = tracking_file
        self.load_tracking_data()
    
    def load_tracking_data(self):
        """Load tracking database"""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'posts': [],
                'last_updated': None,
                'username': 'Agitated_Age_2785'
            }
    
    def save_tracking_data(self):
        """Save tracking database"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_tracked_post(self, post_id, title, subreddit, url, initial_score=None, initial_comments=None):
        """Add a post to track"""
        post = {
            'post_id': post_id,
            'title': title,
            'subreddit': subreddit,
            'url': url,
            'added_date': datetime.now().isoformat(),
            'snapshots': [
                {
                    'timestamp': datetime.now().isoformat(),
                    'score': initial_score or 0,
                    'comments': initial_comments or 0
                }
            ]
        }
        
        self.data['posts'].append(post)
        self.save_tracking_data()
        print(f"[+] Added tracking for: {title}")
    
    def update_post_snapshot(self, post_id, score, comments):
        """Add a new snapshot of post stats"""
        post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
        
        if post:
            post['snapshots'].append({
                'timestamp': datetime.now().isoformat(),
                'score': score,
                'comments': comments
            })
            self.save_tracking_data()
            print(f"[+] Updated {post_id}: Score={score}, Comments={comments}")
            return True
        return False
    
    def view_dashboard(self):
        """Display dashboard"""
        print("\n" + "="*120)
        print(f"REDDIT TRACKING DASHBOARD - u/{self.data['username']}")
        print("="*120)
        print(f"Last updated: {self.data['last_updated'] or 'Never'}")
        print(f"Posts tracked: {len(self.data['posts'])}\n")
        
        if not self.data['posts']:
            print("No posts tracked yet.\n")
            return
        
        # Sort by engagement
        for i, post in enumerate(self.data['posts'], 1):
            snapshots = post['snapshots']
            latest = snapshots[-1]
            first = snapshots[0]
            
            score_change = latest['score'] - first['score']
            comment_change = latest['comments'] - first['comments']
            
            score_arrow = "📈" if score_change > 0 else "📉" if score_change < 0 else "→"
            comment_arrow = "📈" if comment_change > 0 else "📉" if comment_change < 0 else "→"
            
            print(f"{i}. {post['title'][:80]}")
            print(f"   Subreddit: r/{post['subreddit']}")
            print(f"   Link: {post['url']}")
            print(f"   Added: {post['added_date'][:10]}")
            print(f"   Current Score: {latest['score']} {score_arrow} (was {first['score']}, {score_change:+d})")
            print(f"   Comments: {latest['comments']} {comment_arrow} (was {first['comments']}, {comment_change:+d})")
            print(f"   Snapshots: {len(snapshots)}")
            print()
        
        # Summary stats
        all_scores = [s['score'] for p in self.data['posts'] for s in p['snapshots']]
        all_comments = [s['comments'] for p in self.data['posts'] for s in p['snapshots']]
        
        print(f"SUMMARY STATS:")
        print(f"  Total engagement (latest): {sum(p['snapshots'][-1]['score'] for p in self.data['posts'])} points")
        print(f"  Total comments (across all posts): {sum(p['snapshots'][-1]['comments'] for p in self.data['posts'])}")
        print(f"  Average post score: {sum(p['snapshots'][-1]['score'] for p in self.data['posts']) / len(self.data['posts']):.1f}")
        print("="*120 + "\n")
    
    def export_summary(self, output_file="reddit_summary.json"):
        """Export current tracking as summary"""
        summary = {
            'username': self.data['username'],
            'exported_at': datetime.now().isoformat(),
            'posts': []
        }
        
        for post in self.data['posts']:
            latest = post['snapshots'][-1]
            first = post['snapshots'][0]
            
            summary['posts'].append({
                'title': post['title'],
                'subreddit': post['subreddit'],
                'url': post['url'],
                'current_score': latest['score'],
                'current_comments': latest['comments'],
                'initial_score': first['score'],
                'initial_comments': first['comments'],
                'score_change': latest['score'] - first['score'],
                'comment_change': latest['comments'] - first['comments'],
                'snapshots_taken': len(post['snapshots']),
                'first_snapshot': first['timestamp'],
                'last_snapshot': latest['timestamp']
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"[+] Exported summary to {output_file}")
        return output_file

def main():
    """Interactive dashboard"""
    dashboard = RedditTrackingDashboard()
    
    while True:
        print("\nREDDIT TRACKING SYSTEM")
        print("="*60)
        print("1. View dashboard")
        print("2. Add post to track")
        print("3. Update post snapshot")
        print("4. Export summary")
        print("5. Exit")
        print("="*60)
        
        choice = input("Choose option: ").strip()
        
        if choice == '1':
            dashboard.view_dashboard()
        
        elif choice == '2':
            post_id = input("Post ID (e.g., 1sgddb0): ").strip()
            title = input("Post title: ").strip()
            subreddit = input("Subreddit (without r/): ").strip()
            url = input("Reddit URL: ").strip()
            score = input("Current score (optional): ").strip()
            comments = input("Comment count (optional): ").strip()
            
            dashboard.add_tracked_post(
                post_id, title, subreddit, url,
                int(score) if score else None,
                int(comments) if comments else None
            )
        
        elif choice == '3':
            dashboard.view_dashboard()
            post_id = input("Post ID to update: ").strip()
            score = input("New score: ").strip()
            comments = input("New comment count: ").strip()
            
            try:
                dashboard.update_post_snapshot(post_id, int(score), int(comments))
            except ValueError:
                print("[!] Invalid input")
        
        elif choice == '4':
            dashboard.export_summary()
        
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("[!] Invalid choice")

if __name__ == '__main__':
    import sys
    
    dashboard = RedditTrackingDashboard()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'view':
            dashboard.view_dashboard()
        elif sys.argv[1] == 'export':
            dashboard.export_summary()
    else:
        main()
