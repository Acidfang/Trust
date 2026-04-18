#!/usr/bin/env python3
"""Fetch and parse Reddit post content"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import io

# Fix output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fetch_reddit_post(url):
    """Fetch Reddit post and extract text content"""
    
    # Try with JSON API first (most reliable for text)
    json_url = url.rstrip('/') + '.json'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"[*] Fetching: {json_url}")
        response = requests.get(json_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract post data from Reddit's JSON structure
        post = data[0]['data']['children'][0]['data']
        
        print("\n" + "="*80)
        print(f"TITLE: {post.get('title', 'N/A')}")
        print(f"AUTHOR: u/{post.get('author', 'N/A')}")
        print(f"SUBREDDIT: r/{post.get('subreddit', 'N/A')}")
        print("="*80 + "\n")
        
        # Get the body text
        if post.get('selftext'):
            print("POST BODY:")
            print("-"*80)
            print(post['selftext'])
            print("-"*80)
        else:
            print("[!] Post has no text body (likely image/video post)")
            
        # Also try to get comments
        if len(data) > 1:
            comments = data[1]['data']['children']
            print(f"\n\nALL COMMENTS ({len(comments)} total):")
            print("-"*80)
            
            def print_comments(comment_list, depth=0):
                for comment_data in comment_list:
                    if comment_data['kind'] == 't1':
                        comment = comment_data['data']
                        indent = "  " * depth
                        print(f"\n{indent}[COMMENT] u/{comment.get('author', 'N/A')} ({comment.get('score', 0)} pts, {comment.get('created_utc', 0)})")
                        print(f"{indent}{'='*76}")
                        body = comment.get('body', '')
                        # Word wrap the body
                        for line in body.split('\n'):
                            if line.strip():
                                words = line.split()
                                current_line = indent
                                for word in words:
                                    if len(current_line) + len(word) > 76:
                                        print(current_line)
                                        current_line = indent + word + " "
                                    else:
                                        current_line += word + " "
                                if current_line.strip():
                                    print(current_line)
                            else:
                                print("")
                        
                        # Handle replies recursively
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            reply_children = replies.get('data', {}).get('children', [])
                            if reply_children:
                                print(f"{indent}[REPLIES:]")
                                print_comments(reply_children, depth + 1)
            
            print_comments(comments)
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error: {e}")
        return False
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"[!] JSON parsing error: {e}")
        print("[*] Trying HTML fallback...")
        return fetch_reddit_html(url, headers)

def fetch_reddit_html(url, headers):
    """Fallback: parse HTML directly"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find post title and content
        title = soup.find('h1')
        if title:
            print(f"TITLE: {title.get_text()}")
        
        # Look for post content
        post_content = soup.find('div', {'data-testid': 'post-container'})
        if post_content:
            print("\nPOST CONTENT:")
            print(post_content.get_text(separator='\n'))
        
        return True
    except Exception as e:
        print(f"[!] HTML parsing failed: {e}")
        return False

if __name__ == '__main__':
    url = 'https://www.reddit.com/r/ContradictionisFuel/comments/1sgddb0/an_argument_for_three_irreducible_ontological/'
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    success = fetch_reddit_post(url)
    sys.exit(0 if success else 1)
