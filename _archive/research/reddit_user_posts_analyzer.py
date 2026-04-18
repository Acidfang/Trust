"""
Analyze Reddit exchanges and fetch posts by users
"""
import requests
import json
from collections import defaultdict
from datetime import datetime

def fetch_post_comments(post_id):
    """Fetch all comments from a Reddit post"""
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
                        'id': comment['id'],
                        'author': author,
                        'body': comment['body'],
                        'score': comment['score'],
                        'created': comment['created_utc'],
                        'depth': depth,
                        'parent_author': parent_author
                    })
                    replies = comment.get('replies', '')
                    if replies and isinstance(replies, dict):
                        extract_comments(replies.get('data', {}).get('children', []), depth + 1, author)
        
        if len(data) > 1:
            extract_comments(data[1]['data']['children'])
        
        return comments
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []

def analyze_exchanges(comments, your_username):
    """
    Analyze MEANINGFUL exchanges - back-and-forth dialogue with substance.
    Only count users where there's actual conversation continuity.
    """
    # Build a map of comment ID to comment for quick lookup
    comment_map = {c['id']: c for c in comments}
    
    # Find your comments
    your_comments = {c['id']: c for c in comments if c['author'] == your_username}
    
    # Track meaningful dialogue threads
    meaningful_exchanges = defaultdict(lambda: {'threads': [], 'count': 0})
    
    for your_comment_id, your_comment in your_comments.items():
        # Find direct replies to this comment
        for other_comment in comments:
            if other_comment['parent_author'] == your_username and other_comment['author'] != your_username:
                # They replied to you
                other_author = other_comment['author']
                
                # Check if you replied back to them (meaningful dialogue)
                for follow_up in comments:
                    if (follow_up['parent_author'] == other_author and 
                        follow_up['author'] == your_username and
                        len(follow_up['body']) > 50 and  # Meaningful length
                        len(other_comment['body']) > 50):  # Their reply was substantial
                        
                        # This is a meaningful exchange
                        meaningful_exchanges[other_author]['threads'].append({
                            'your_comment': your_comment['body'][:80],
                            'their_reply': other_comment['body'][:80],
                            'your_follow_up': follow_up['body'][:80]
                        })
                        meaningful_exchanges[other_author]['count'] += 1
                        break  # Count once per thread
    
    # Filter for real conversations (>3 meaningful back-and-forths)
    active_users = {user: data['count'] for user, data in meaningful_exchanges.items() 
                    if data['count'] > 3 and user != '[deleted]'}
    
    return active_users, meaningful_exchanges

def fetch_user_posts(username, limit=20):
    """Fetch recent posts by a user"""
    try:
        url = f"https://www.reddit.com/user/{username}/posts.json"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 404:
            # Try alternative endpoint
            url = f"https://www.reddit.com/user/{username}/submitted.json"
            response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        posts = []
        
        for item in data.get('data', {}).get('children', []):
            if item['kind'] == 't3':
                post = item['data']
                posts.append({
                    'id': post['id'],
                    'title': post['title'],
                    'subreddit': post['subreddit'],
                    'score': post['score'],
                    'comments': post['num_comments'],
                    'created': post['created_utc'],
                    'selftext': post.get('selftext', '')[:200],
                    'url': post['url']
                })
        
        return posts[:limit]
    except Exception as e:
        print(f"Error fetching posts for {username}: {e}")
        return []

if __name__ == "__main__":
    # Test: Analyze exchanges from tracked post
    print("Fetching comments from tracked post...")
    comments = fetch_post_comments("1sgddb0")
    print(f"Fetched {len(comments)} comments\n")
    
    print("Analyzing exchanges...")
    active_users, meaningful_exchanges = analyze_exchanges(comments, "Agitated_Age_2785")
    
    print(f"Users with >3 MEANINGFUL exchanges ({len(active_users)}):")
    for user, count in sorted(active_users.items(), key=lambda x: x[1], reverse=True):
        print(f"  @{user}: {count} dialogue threads")
    
    print("\nMeaningful dialogue threads:")
    for user, data in sorted(meaningful_exchanges.items(), 
                             key=lambda x: x[1]['count'], reverse=True):
        if data['count'] > 3:
            print(f"\n@{user} ({data['count']} back-and-forth conversations):")
            for i, thread in enumerate(data['threads'][:2], 1):  # Show first 2 threads
                print(f"  Thread {i}:")
                print(f"    You: {thread['your_comment']}")
                print(f"    Them: {thread['their_reply']}")
                print(f"    You: {thread['your_follow_up']}")
    
    print("\n" + "="*60)
    print("Fetching posts by active users...")
    print("="*60)
    
    # Fetch posts by user
    your_posts = fetch_user_posts("Agitated_Age_2785", limit=10)
    print(f"\nYour recent posts ({len(your_posts)}):")
    for post in your_posts:
        print(f"  - r/{post['subreddit']}: {post['title']}")
        print(f"    Score: {post['score']} | Comments: {post['comments']}")
    
    # Fetch posts by exchange partners
    for user in list(active_users.keys())[:3]:  # Top 3 users
        user_posts = fetch_user_posts(user, limit=5)
        print(f"\n@{user}'s recent posts ({len(user_posts)}):")
        for post in user_posts:
            print(f"  - r/{post['subreddit']}: {post['title']}")
            print(f"    Score: {post['score']} | Comments: {post['comments']}")
