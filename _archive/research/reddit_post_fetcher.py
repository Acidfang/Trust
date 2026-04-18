#!/usr/bin/env python3
"""
Reddit Post Fetcher by URL
Fetches specific posts and their comment threads
"""

import requests
import json
from datetime import datetime
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class RedditPostFetcher:
    def __init__(self, data_dir="reddit_data"):
        self.data_dir = data_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def extract_post_id(self, url):
        """Extract post ID from Reddit URL"""
        # Handle various Reddit URL formats
        url = url.strip('/')
        if '/comments/' in url:
            parts = url.split('/comments/')
            if len(parts) > 1:
                post_id = parts[1].split('/')[0]
                return post_id
        return None
    
    def fetch_post_and_comments(self, post_url):
        """Fetch a post and all its comments"""
        post_id = self.extract_post_id(post_url)
        if not post_id:
            print(f"[!] Could not extract post ID from {post_url}")
            return None
        
        json_url = f"https://www.reddit.com/comments/{post_id}.json"
        print(f"[*] Fetching: {json_url}")
        
        try:
            response = requests.get(json_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract post data
            post_data = data[0]['data']['children'][0]['data']
            post_info = {
                'id': post_data['id'],
                'title': post_data['title'],
                'author': post_data.get('author', '[deleted]'),
                'subreddit': post_data['subreddit'],
                'created': datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                'score': post_data['score'],
                'num_comments': post_data['num_comments'],
                'url': f"https://reddit.com{post_data['permalink']}",
                'selftext': post_data.get('selftext', '')[:1000],
                'fetched_at': datetime.now().isoformat()
            }
            
            # Extract comments
            comments = []
            
            def extract_comments(comment_list, depth=0):
                for item in comment_list:
                    if item['kind'] == 't1':  # Comment
                        comment = item['data']
                        comments.append({
                            'id': comment['id'],
                            'author': comment.get('author', '[deleted]'),
                            'body': comment['body'],
                            'created': datetime.fromtimestamp(comment['created_utc']).isoformat(),
                            'score': comment['score'],
                            'depth': depth
                        })
                        
                        # Get replies
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            reply_children = replies.get('data', {}).get('children', [])
                            extract_comments(reply_children, depth + 1)
            
            if len(data) > 1:
                comment_children = data[1]['data']['children']
                extract_comments(comment_children)
            
            post_info['comments'] = comments
            post_info['comment_count'] = len(comments)
            
            return post_info
        
        except Exception as e:
            print(f"[!] Error fetching post: {e}")
            return None
    
    def save_post(self, post_info):
        """Save post data to JSON"""
        if not post_info:
            return None
        
        filename = f"{post_info['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(post_info, f, indent=2, ensure_ascii=False)
        
        print(f"[+] Saved to {filepath}")
        return filepath
    
    def analyze_and_display(self, post_info):
        """Display analysis of post and comments"""
        if not post_info:
            return
        
        print("\n" + "="*100)
        print("POST ANALYSIS")
        print("="*100)
        print(f"Title: {post_info['title']}")
        print(f"Author: u/{post_info['author']}")
        print(f"Subreddit: r/{post_info['subreddit']}")
        print(f"Posted: {post_info['created']}")
        print(f"URL: {post_info['url']}")
        print(f"Score: {post_info['score']} | Comments: {post_info['comment_count']}")
        print("-"*100)
        
        # Analyze comments
        comments = post_info['comments']
        top_comments = sorted(comments, key=lambda x: x['score'], reverse=True)[:5]
        
        print(f"\nTOP COMMENTS (by score):\n")
        for i, comment in enumerate(top_comments, 1):
            preview = comment['body'][:100].replace('\n', ' ')
            print(f"{i}. u/{comment['author']} ({comment['score']} pts)")
            print(f"   {preview}...\n")
        
        # Comment depth analysis
        depth_counts = {}
        for comment in comments:
            d = comment['depth']
            depth_counts[d] = depth_counts.get(d, 0) + 1
        
        print(f"\nCOMMENT THREAD DEPTH:")
        for depth in sorted(depth_counts.keys()):
            print(f"  Depth {depth}: {depth_counts[depth]} comments")
        
        print("\n" + "="*100)

def main():
    """Command line interface"""
    import sys
    
    fetcher = RedditPostFetcher()
    
    if len(sys.argv) > 1:
        # URL provided as argument
        post_url = sys.argv[1]
        print(f"[*] Processing: {post_url}")
        
        post_info = fetcher.fetch_post_and_comments(post_url)
        if post_info:
            fetcher.save_post(post_info)
            fetcher.analyze_and_display(post_info)
    else:
        print("Usage: python reddit_post_fetcher.py <reddit_post_url>")
        print("Example: python reddit_post_fetcher.py https://reddit.com/r/ContradictionisFuel/comments/1sgddb0/...")
        print("\nOr provide URL interactively:")
        
        while True:
            url = input("\nEnter Reddit post URL (or 'quit'): ").strip()
            if url.lower() == 'quit':
                break
            
            if not url:
                continue
            
            print(f"\n[*] Processing: {url}")
            post_info = fetcher.fetch_post_and_comments(url)
            if post_info:
                fetcher.save_post(post_info)
                fetcher.analyze_and_display(post_info)

if __name__ == '__main__':
    main()
