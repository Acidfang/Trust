#!/usr/bin/env python3
"""
Reddit Post & Comment Tracker
Monitors your posts, comments, and their replies
"""

import requests
import json
import csv
from datetime import datetime
import os
import sys
import io

# Fix output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class RedditTracker:
    def __init__(self, username, data_dir="reddit_tracking_data"):
        self.username = username
        self.data_dir = data_dir
        self.base_url = "https://www.reddit.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def fetch_user_posts(self, limit=100):
        """Fetch all posts by the user"""
        print(f"[*] Fetching posts by u/{self.username}...")
        
        # Try user profile submissions endpoint
        url = f"{self.base_url}/user/{self.username}/submitted.json"
        posts = []
        after = None
        
        while len(posts) < limit:
            params = {'limit': 100}
            if after:
                params['after'] = after
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                children = data['data']['children']
                if not children:
                    break
                
                for post_data in children:
                    if post_data['kind'] == 't3':  # t3 = post
                        post = post_data['data']
                        posts.append({
                            'id': post['id'],
                            'title': post['title'],
                            'subreddit': post['subreddit'],
                            'created_utc': post['created_utc'],
                            'score': post['score'],
                            'num_comments': post['num_comments'],
                            'url': f"{self.base_url}{post['permalink']}",
                            'full_link': post.get('url', ''),
                            'selftext': post.get('selftext', '')[:500],  # First 500 chars
                            'timestamp': datetime.fromtimestamp(post['created_utc']).isoformat()
                        })
                
                after = data['data']['after']
                if not after or len(posts) >= limit:
                    break
                    
            except Exception as e:
                print(f"[!] Error fetching posts: {e}")
                break
        
        return posts[:limit]
    
    def fetch_post_comments(self, post_id):
        """Fetch all comments on a specific post"""
        url = f"{self.base_url}/comments/{post_id}.json"
        comments = []
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            def extract_comments(comment_list, depth=0):
                for item in comment_list:
                    if item['kind'] == 't1':  # t1 = comment
                        comment = item['data']
                        comments.append({
                            'id': comment['id'],
                            'author': comment.get('author', '[deleted]'),
                            'body': comment['body'][:300],
                            'created_utc': comment['created_utc'],
                            'score': comment['score'],
                            'depth': depth,
                            'timestamp': datetime.fromtimestamp(comment['created_utc']).isoformat(),
                            'is_user': comment.get('author', '').lower() == self.username.lower()
                        })
                        
                        # Recursively get replies
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            reply_children = replies.get('data', {}).get('children', [])
                            extract_comments(reply_children, depth + 1)
            
            if len(data) > 1:
                comment_children = data[1]['data']['children']
                extract_comments(comment_children)
        
        except Exception as e:
            print(f"[!] Error fetching comments for post {post_id}: {e}")
        
        return comments
    
    def find_user_comment_threads(self, post_id):
        """Find all threads where the user replied and extract replies to those comments"""
        url = f"{self.base_url}/comments/{post_id}.json"
        user_comment_threads = []
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            def traverse_comments(comment_list):
                for item in comment_list:
                    if item['kind'] == 't1':
                        comment = item['data']
                        author = comment.get('author', '').lower()
                        
                        # If this is a user comment, track its replies
                        if author == self.username.lower():
                            replies = comment.get('replies', '')
                            reply_count = 0
                            reply_list = []
                            
                            if replies and isinstance(replies, dict):
                                reply_children = replies.get('data', {}).get('children', [])
                                for reply_item in reply_children:
                                    if reply_item['kind'] == 't1':
                                        reply = reply_item['data']
                                        reply_list.append({
                                            'author': reply.get('author', '[deleted]'),
                                            'body': reply['body'][:300],
                                            'score': reply['score'],
                                            'timestamp': datetime.fromtimestamp(reply['created_utc']).isoformat()
                                        })
                                        reply_count += 1
                            
                            user_comment_threads.append({
                                'comment_id': comment['id'],
                                'your_comment': comment['body'][:300],
                                'your_score': comment['score'],
                                'created': datetime.fromtimestamp(comment['created_utc']).isoformat(),
                                'reply_count': reply_count,
                                'replies': reply_list
                            })
                        
                        # Continue traversing
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            reply_children = replies.get('data', {}).get('children', [])
                            traverse_comments(reply_children)
            
            if len(data) > 1:
                comment_children = data[1]['data']['children']
                traverse_comments(comment_children)
        
        except Exception as e:
            print(f"[!] Error traversing comments: {e}")
        
        return user_comment_threads
    
    def save_posts(self, posts):
        """Save posts to JSON and CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON
        json_file = os.path.join(self.data_dir, f"posts_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"[+] Saved {len(posts)} posts to {json_file}")
        
        # CSV
        csv_file = os.path.join(self.data_dir, f"posts_{timestamp}.csv")
        if posts:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=posts[0].keys())
                writer.writeheader()
                writer.writerows(posts)
            print(f"[+] Saved posts to {csv_file}")
    
    def save_post_analysis(self, analysis):
        """Save post analysis with comment threads"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = os.path.join(self.data_dir, f"post_analysis_{timestamp}.json")
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"[+] Saved analysis to {json_file}")
    
    def generate_summary(self, posts, analysis_list):
        """Generate tracking summary"""
        summary = {
            'generated_at': datetime.now().isoformat(),
            'username': self.username,
            'total_posts': len(posts),
            'posts': []
        }
        
        for post, analysis in zip(posts, analysis_list):
            total_user_replies = sum(t['reply_count'] for t in analysis)
            post_summary = {
                'title': post['title'],
                'subreddit': post['subreddit'],
                'url': post['url'],
                'created': post['timestamp'],
                'post_score': post['score'],
                'total_comments_on_post': post['num_comments'],
                'your_comment_threads': len(analysis),
                'replies_to_your_comments': total_user_replies,
                'engagement': {
                    'has_replies': total_user_replies > 0,
                    'active_threads': len([t for t in analysis if t['reply_count'] > 0])
                }
            }
            summary['posts'].append(post_summary)
        
        return summary
    
    def track_all(self):
        """Full tracking run: fetch posts and all replies"""
        print(f"\n[*] Starting tracking for u/{self.username}")
        print("=" * 80)
        
        # Fetch posts
        posts = self.fetch_user_posts(limit=10)
        print(f"\n[+] Found {len(posts)} recent posts")
        
        # Save posts
        self.save_posts(posts)
        
        # Analyze each post for user comments and replies
        print(f"\n[*] Analyzing comments and replies...")
        all_analysis = []
        summary_data = {
            'generated_at': datetime.now().isoformat(),
            'username': self.username,
            'posts': []
        }
        
        for i, post in enumerate(posts, 1):
            print(f"\n[{i}/{len(posts)}] Analyzing: {post['title'][:60]}...")
            
            comment_threads = self.find_user_comment_threads(post['id'])
            all_analysis.append(comment_threads)
            
            total_replies = sum(t['reply_count'] for t in comment_threads)
            
            post_data = {
                'title': post['title'],
                'subreddit': post['subreddit'],
                'url': post['url'],
                'created': post['timestamp'],
                'post_score': post['score'],
                'total_comments_on_post': post['num_comments'],
                'your_comments': len(comment_threads),
                'total_replies_to_your_comments': total_replies,
                'comment_threads': comment_threads
            }
            summary_data['posts'].append(post_data)
        
        # Save analysis
        self.save_post_analysis(summary_data)
        
        # Print summary
        print(f"\n{'='*80}")
        print(f"TRACKING SUMMARY FOR u/{self.username}")
        print(f"{'='*80}")
        print(f"Total posts analyzed: {len(posts)}")
        print(f"Generated: {datetime.now().isoformat()}\n")
        
        for post in summary_data['posts']:
            print(f"📌 {post['title'][:70]}")
            print(f"   Subreddit: r/{post['subreddit']}")
            print(f"   Posted: {post['created']}")
            print(f"   Post Score: {post['post_score']} | Comments: {post['total_comments_on_post']}")
            print(f"   Your comments: {post['your_comments']} | Replies to you: {post['total_replies_to_your_comments']}")
            print(f"   Link: {post['url']}\n")
        
        print(f"{'='*80}")
        print(f"[+] Tracking complete. Data saved in {self.data_dir}/")
        return summary_data

if __name__ == '__main__':
    username = 'Agitated_Age_2785'
    tracker = RedditTracker(username)
    tracker.track_all()
