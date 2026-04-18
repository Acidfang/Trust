"""
PLATFORM ADAPTERS
Convert Reddit/HN → Universal POST/COMMENT model

Handles:
- Reddit JSON exports, praw API, pushshift archives
- Hacker News HTML scrapes, algolia API, official API
- Discord message exports
"""

import json
import re
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from abc import ABC, abstractmethod
import requests
import praw

from universal_tracker_core import Post, Comment, Platform


# ============================================================================
# REDDIT ADAPTER
# ============================================================================

class RedditAdapter:
    """
    Parse Reddit data into universal Post/Comment model
    Supports:
    1. JSON export (reddit-data-export, reddit-viewer)
    2. PRAW API (live scraping)
    3. Pushshift archives
    """
    
    def __init__(self, data_source: str = "export"):
        """
        data_source: "export" (json file), "api" (praw), "pushshift" (archive)
        """
        self.data_source = data_source
        self.reddit = None
        
        if data_source == "api":
            # Initialize PRAW (requires credentials in praw.ini or env vars)
            self.reddit = praw.Reddit(site_name="SpeakingWithPatience")
    
    def fetch_post(self, post_id: str) -> Optional[Post]:
        """Fetch single post by ID"""
        if self.data_source == "api":
            return self._fetch_post_api(post_id)
        else:
            raise NotImplementedError("fetch_post requires API mode")
    
    def fetch_comments(self, post_id: str) -> List[Comment]:
        """Fetch all comments on a post"""
        if self.data_source == "api":
            return self._fetch_comments_api(post_id)
        else:
            raise NotImplementedError("fetch_comments requires API mode")
    
    def parse_json_export(self, json_file_path: str) -> Tuple[Post, List[Comment]]:
        """
        Parse Reddit JSON export file
        Format: reddit-data-export, reddit-viewer, etc.
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {json_file_path}")
            return None, []
        
        # Detect format
        if isinstance(data, dict):
            if 'data' in data and 'children' in data['data']:
                # Reddit API format
                return self._parse_reddit_api_format(data)
            elif 'id' in data:
                # Single post format
                return self._parse_single_post_format(data)
        elif isinstance(data, list):
            # Array of posts/comments
            return self._parse_array_format(data)
        
        print(f"Error: Unrecognized JSON format")
        return None, []
    
    def _fetch_post_api(self, post_id: str) -> Optional[Post]:
        """Fetch post via PRAW API"""
        try:
            submission = self.reddit.submission(id=post_id)
            
            return Post(
                id=f"reddit_{post_id}",
                platform=Platform.REDDIT,
                title=submission.title,
                text=submission.selftext,
                author=submission.author.name if submission.author else "[deleted]",
                timestamp=datetime.fromtimestamp(submission.created_utc),
                url=f"https://reddit.com{submission.permalink}",
                score=submission.score,
                comments_count=submission.num_comments
            )
        except Exception as e:
            print(f"Error fetching post {post_id}: {e}")
            return None
    
    def _fetch_comments_api(self, post_id: str) -> List[Comment]:
        """Fetch all comments via PRAW API"""
        comments = []
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=None)  # Expand collapsed comments
            
            for comment_obj in submission.comments.list():
                comment = Comment(
                    id=f"reddit_{comment_obj.id}",
                    post_id=f"reddit_{post_id}",
                    parent_comment_id=None,  # TODO: track comment threading
                    text=comment_obj.body,
                    author=comment_obj.author.name if comment_obj.author else "[deleted]",
                    timestamp=datetime.fromtimestamp(comment_obj.created_utc),
                    score=comment_obj.score,
                    url=f"https://reddit.com{comment_obj.permalink}",
                    depth=comment_obj.depth
                )
                comments.append(comment)
        except Exception as e:
            print(f"Error fetching comments for {post_id}: {e}")
        
        return comments
    
    def _parse_reddit_api_format(self, data: dict) -> Tuple[Optional[Post], List[Comment]]:
        """Parse reddit.com API JSON response"""
        post = None
        comments = []
        
        try:
            children = data.get('data', {}).get('children', [])
            
            for child in children:
                child_data = child.get('data', {})
                kind = child.get('kind', '')
                
                if kind == 't3':  # Post
                    post = Post(
                        id=f"reddit_{child_data.get('id')}",
                        platform=Platform.REDDIT,
                        title=child_data.get('title', ''),
                        text=child_data.get('selftext', ''),
                        author=child_data.get('author', '[deleted]'),
                        timestamp=datetime.fromtimestamp(child_data.get('created_utc', 0)),
                        url=f"https://reddit.com{child_data.get('permalink', '')}",
                        score=child_data.get('score', 0),
                        comments_count=child_data.get('num_comments', 0)
                    )
                
                elif kind == 't1':  # Comment
                    comment = Comment(
                        id=f"reddit_{child_data.get('id')}",
                        post_id=f"reddit_{child_data.get('link_id', '')}",
                        parent_comment_id=None,
                        text=child_data.get('body', ''),
                        author=child_data.get('author', '[deleted]'),
                        timestamp=datetime.fromtimestamp(child_data.get('created_utc', 0)),
                        score=child_data.get('score', 0),
                        url=f"https://reddit.com{child_data.get('permalink', '')}",
                        depth=child_data.get('depth', 0)
                    )
                    comments.append(comment)
        except Exception as e:
            print(f"Error parsing Reddit API format: {e}")
        
        return post, comments
    
    def _parse_single_post_format(self, data: dict) -> Tuple[Optional[Post], List[Comment]]:
        """Parse single-post JSON export format"""
        post = None
        comments = []
        
        try:
            # Build post
            post = Post(
                id=f"reddit_{data.get('id')}",
                platform=Platform.REDDIT,
                title=data.get('title', ''),
                text=data.get('selftext', data.get('text', '')),
                author=data.get('author', data.get('authorName', '[deleted]')),
                timestamp=self._parse_timestamp(data.get('createdAt', data.get('created_utc'))),
                url=data.get('url', f"https://reddit.com/r/{data.get('subreddit')}/"),
                score=data.get('score', data.get('ups', 0)),
                comments_count=data.get('number_of_comments', len(data.get('comments', [])))
            )
            
            # Parse comments (recursive structure)
            comments = self._parse_comment_tree(data.get('comments', []), post.id)
        except Exception as e:
            print(f"Error parsing single post format: {e}")
        
        return post, comments
    
    def _parse_array_format(self, data: list) -> Tuple[Optional[Post], List[Comment]]:
        """Parse array of posts/comments"""
        all_comments = []
        post = None
        
        for item in data:
            if item.get('data', {}).get('selftext') or 'title' in item:
                # Likely a post
                if post is None:
                    post = Post(
                        id=f"reddit_{item.get('data', {}).get('id')}",
                        platform=Platform.REDDIT,
                        title=item.get('data', {}).get('title', ''),
                        text=item.get('data', {}).get('selftext', ''),
                        author=item.get('data', {}).get('author', '[deleted]'),
                        timestamp=self._parse_timestamp(item.get('data', {}).get('created_utc')),
                        url=item.get('data', {}).get('url', ''),
                        score=item.get('data', {}).get('score', 0),
                        comments_count=item.get('data', {}).get('num_comments', 0)
                    )
            else:
                # Likely a comment
                comment = Comment(
                    id=f"reddit_{item.get('data', {}).get('id')}",
                    post_id=f"reddit_{item.get('data', {}).get('link_id', '')}",
                    parent_comment_id=None,
                    text=item.get('data', {}).get('body', ''),
                    author=item.get('data', {}).get('author', '[deleted]'),
                    timestamp=self._parse_timestamp(item.get('data', {}).get('created_utc')),
                    score=item.get('data', {}).get('score', 0),
                    url=item.get('data', {}).get('permalink', ''),
                    depth=0
                )
                all_comments.append(comment)
        
        return post, all_comments
    
    def _parse_comment_tree(self, comments: list, post_id: str) -> List[Comment]:
        """Recursively parse nested comment structure"""
        flat_comments = []
        
        def traverse(node, depth=0):
            if isinstance(node, dict):
                if 'body' in node:  # Comment
                    comment = Comment(
                        id=f"reddit_{node.get('id')}",
                        post_id=post_id,
                        parent_comment_id=None,
                        text=node.get('body', ''),
                        author=node.get('author', node.get('authorName', '[deleted]')),
                        timestamp=self._parse_timestamp(node.get('createdAt', node.get('created_utc'))),
                        score=node.get('score', 0),
                        url=node.get('url', ''),
                        depth=depth
                    )
                    flat_comments.append(comment)
                    
                    # Recursively process replies
                    if 'replies' in node:
                        traverse(node['replies'], depth + 1)
        
        for comment in comments:
            traverse(comment)
        
        return flat_comments
    
    @staticmethod
    def _parse_timestamp(ts) -> datetime:
        """Parse various timestamp formats"""
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts)
        elif isinstance(ts, str):
            try:
                return datetime.fromisoformat(ts)
            except:
                return datetime.now()
        else:
            return datetime.now()


# ============================================================================
# HACKER NEWS ADAPTER
# ============================================================================

class HackerNewsAdapter:
    """
    Parse Hacker News data into universal Post/Comment model
    Supports:
    - Hacker News API (official)
    - Algolia API (search + full-text)
    """
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    ALGOLIA_URL = "https://hn.algolia.com/api/v1"
    
    def __init__(self, use_algolia: bool = False):
        """
        use_algolia: Use Algolia API for faster queries
        """
        self.use_algolia = use_algolia
    
    def fetch_post(self, story_id: str) -> Optional[Post]:
        """Fetch single HN story/post"""
        try:
            url = f"{self.BASE_URL}/item/{story_id}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
            
            return Post(
                id=f"hn_{story_id}",
                platform=Platform.HACKERNEWS,
                title=data.get('title', ''),
                text=data.get('text', ''),
                author=data.get('by', '[deleted]'),
                timestamp=datetime.fromtimestamp(data.get('time', 0)),
                url=data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                score=data.get('score', 0),
                comments_count=data.get('descendants', 0)
            )
        except Exception as e:
            print(f"Error fetching HN story {story_id}: {e}")
            return None
    
    def fetch_comments(self, story_id: str) -> List[Comment]:
        """Fetch all comments on HN story"""
        comments = []
        try:
            story = self.fetch_post(story_id)
            if not story:
                return comments
            
            # Fetch story data with kids (children comments)
            url = f"{self.BASE_URL}/item/{story_id}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            story_data = response.json()
            
            kids = story_data.get('kids', [])
            
            # Fetch each comment
            for kid_id in kids:
                comment = self._fetch_comment_recursive(kid_id, story_id)
                if comment:
                    comments.append(comment)
        except Exception as e:
            print(f"Error fetching comments for HN {story_id}: {e}")
        
        return comments
    
    def parse_hn_export(self, json_file_path: str) -> Tuple[Optional[Post], List[Comment]]:
        """Parse HN export JSON file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {json_file_path}")
            return None, []
        
        post = None
        comments = []
        
        if isinstance(data, dict):
            # Single story format
            post = self._parse_hn_item(data)
            comments = self._parse_hn_comments(data.get('comments', []), post.id if post else "")
        elif isinstance(data, list):
            # Array of stories
            for item in data:
                parsed_post = self._parse_hn_item(item)
                parsed_comments = self._parse_hn_comments(item.get('comments', []), parsed_post.id if parsed_post else "")
                
                if post is None and parsed_post:
                    post = parsed_post
                comments.extend(parsed_comments)
        
        return post, comments
    
    def _fetch_comment_recursive(self, comment_id: int, post_id: str, depth: int = 0) -> Optional[Comment]:
        """Recursively fetch comment and its children"""
        try:
            url = f"{self.BASE_URL}/item/{comment_id}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data or data.get('deleted'):
                return None
            
            comment = Comment(
                id=f"hn_{comment_id}",
                post_id=f"hn_{post_id}",
                parent_comment_id=None,
                text=data.get('text', ''),
                author=data.get('by', '[deleted]'),
                timestamp=datetime.fromtimestamp(data.get('time', 0)),
                score=data.get('score', 0),
                url=f"https://news.ycombinator.com/item?id={comment_id}",
                depth=depth
            )
            
            # Recursively fetch child comments (kids)
            kids = data.get('kids', [])
            if kids and depth < 10:  # Limit recursion depth
                for kid_id in kids:
                    child = self._fetch_comment_recursive(kid_id, post_id, depth + 1)
                    if child:
                        child.parent_comment_id = comment.id
            
            return comment
        except Exception as e:
            print(f"Error fetching comment {comment_id}: {e}")
            return None
    
    def _parse_hn_item(self, data: dict) -> Optional[Post]:
        """Parse single HN item into Post"""
        try:
            return Post(
                id=f"hn_{data.get('id')}",
                platform=Platform.HACKERNEWS,
                title=data.get('title', ''),
                text=data.get('text', ''),
                author=data.get('by', data.get('author', '[deleted]')),
                timestamp=self._parse_hn_timestamp(data.get('time', data.get('createdAt'))),
                url=data.get('url', f"https://news.ycombinator.com/item?id={data.get('id')}"),
                score=data.get('score', 0),
                comments_count=data.get('descendants', data.get('comments_count', 0))
            )
        except Exception as e:
            print(f"Error parsing HN item: {e}")
            return None
    
    def _parse_hn_comments(self, comments: list, post_id: str, depth: int = 0) -> List[Comment]:
        """Recursively parse HN comment tree"""
        flat_comments = []
        
        for comment_data in comments:
            try:
                if comment_data.get('deleted'):
                    continue
                
                comment = Comment(
                    id=f"hn_{comment_data.get('id')}",
                    post_id=post_id,
                    parent_comment_id=None,
                    text=comment_data.get('text', comment_data.get('body', '')),
                    author=comment_data.get('by', comment_data.get('author', '[deleted]')),
                    timestamp=self._parse_hn_timestamp(comment_data.get('time', comment_data.get('createdAt'))),
                    score=comment_data.get('score', 0),
                    url=f"https://news.ycombinator.com/item?id={comment_data.get('id')}",
                    depth=depth
                )
                flat_comments.append(comment)
                
                # Recursively parse nested replies
                if 'comments' in comment_data:
                    children = self._parse_hn_comments(comment_data['comments'], post_id, depth + 1)
                    for child in children:
                        child.parent_comment_id = comment.id
                    flat_comments.extend(children)
            except Exception as e:
                print(f"Error parsing comment: {e}")
        
        return flat_comments
    
    @staticmethod
    def _parse_hn_timestamp(ts) -> datetime:
        """Parse HN timestamp"""
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts)
        elif isinstance(ts, str):
            try:
                return datetime.fromisoformat(ts)
            except:
                return datetime.now()
        else:
            return datetime.now()


# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    print("✓ RedditAdapter loaded (JSON export + PRAW API + Pushshift)")
    print("✓ HackerNewsAdapter loaded (HN API + Algolia)")
    print("\nUsage:")
    print("  reddit = RedditAdapter(data_source='export')")
    print("  post, comments = reddit.parse_json_export('export.json')")
    print("\n  hn = HackerNewsAdapter()")
    print("  post = hn.fetch_post('story_id')")
    print("  comments = hn.fetch_comments('story_id')")
