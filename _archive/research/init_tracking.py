#!/usr/bin/env python3
"""Initialize Reddit tracking with your post"""

import json
from datetime import datetime

# Initialize tracking database with your post
tracking_data = {
    'posts': [
        {
            'post_id': '1sgddb0',
            'title': 'An Argument for Three Irreducible Ontological Primitives: Difference, Resolution, and Persistence',
            'subreddit': 'ContradictionisFuel',
            'url': 'https://www.reddit.com/r/ContradictionisFuel/comments/1sgddb0/an_argument_for_three_irreducible_ontological/',
            'added_date': '2026-04-09T14:41:43',
            'snapshots': [
                {
                    'timestamp': '2026-04-09T14:41:43',
                    'score': 6,
                    'comments': 67
                },
                {
                    'timestamp': datetime.now().isoformat(),
                    'score': 6,
                    'comments': 67
                }
            ]
        }
    ],
    'last_updated': datetime.now().isoformat(),
    'username': 'Agitated_Age_2785'
}

with open('reddit_tracking.json', 'w', encoding='utf-8') as f:
    json.dump(tracking_data, f, indent=2, ensure_ascii=False)

print("[+] Initialized reddit_tracking.json with your post")
print(f"[+] Post: {tracking_data['posts'][0]['title'][:70]}...")
print(f"[+] Current engagement: {tracking_data['posts'][0]['snapshots'][-1]['score']} score, {tracking_data['posts'][0]['snapshots'][-1]['comments']} comments")
print("\n[+] Now you can track this post with:")
print("    python reddit_dashboard.py view")
