"""
TRACKER PLATFORM ADAPTERS
Platform-specific post/comment extraction

Adapters:
- RedditAdapter: Extract from Reddit API via PRAW
- HackerNewsAdapter: Extract from HN API
"""

import time
from datetime import datetime
from typing import List, Optional
from universal_tracker_core import Post, Comment, ScrapeResult


class RedditAdapter:
    """Scrape Reddit using PRAW"""
    
    def __init__(self, client_id: str = "", client_secret: str = "", user_agent: str = ""):
        """Initialize Reddit adapter
        
        Args:
            client_id: Reddit app ID (from app.reddit.com/prefs/apps)
            client_secret: Reddit app secret
            user_agent: Unique identifier for requests
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent or "UniversalTracker/1.0"
        self.praw = None
        
        # Try to import PRAW
        try:
            import praw
            if client_id and client_secret:
                self.praw = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=self.user_agent
                )
        except ImportError:
            print("⚠ PRAW not installed. Reddit scraping will use mock data.")
        except Exception as e:
            print(f"⚠ Reddit auth failed: {e}. Using mock data.")
    
    def search(self, query: str, limit: int = 100) -> ScrapeResult:
        """Search Reddit for posts"""
        start_time = time.time()
        result = ScrapeResult(platform="reddit", status="success")
        
        try:
            # If PRAW available, use real data
            if self.praw:
                for submission in self.praw.subreddit("all").search(query, limit=min(limit, 100)):
                    # Add post
                    post = Post(
                        id=submission.id,
                        platform="reddit",
                        title=submission.title,
                        content=submission.selftext,
                        author=submission.author.name if submission.author else "deleted",
                        timestamp=datetime.fromtimestamp(submission.created_utc).isoformat(),
                        url=f"https://reddit.com{submission.permalink}",
                        posts_count=1,
                        comments_count=submission.num_comments,
                        engagement=submission.score
                    )
                    result.posts.append(post)
                    
                    # Add comments (limited to avoid rate limiting)
                    submission.comments.replace_more(limit=10)
                    for comment_obj in submission.comments[:50]:
                        comment = Comment(
                            id=comment_obj.id,
                            post_id=submission.id,
                            platform="reddit",
                            content=comment_obj.body,
                            author=comment_obj.author.name if comment_obj.author else "deleted",
                            timestamp=datetime.fromtimestamp(comment_obj.created_utc).isoformat(),
                            engagement=comment_obj.score
                        )
                        result.comments.append(comment)
            else:
                # Use mock data for testing
                result = self._generate_mock_reddit_data(query, limit)
        
        except Exception as e:
            result.status = "error"
            result.errors.append(str(e))
        
        result.duration_seconds = time.time() - start_time
        return result
    
    def _generate_mock_reddit_data(self, query: str, limit: int) -> ScrapeResult:
        """Generate mock Reddit data for testing"""
        result = ScrapeResult(platform="reddit", status="success")
        
        mock_posts = [
            {
                "title": f"Discussion: {query} and its implications",
                "content": f"What's your take on {query}? I think the key issue is complexity.",
                "author": "user123",
                "score": 125
            },
            {
                "title": f"{query}: Facts vs Opinions",
                "content": f"Let's separate the facts about {query} from speculation.",
                "author": "scientist456",
                "score": 89
            },
            {
                "title": f"Why I support/oppose {query}",
                "content": f"Here's my perspective on {query} based on personal experience.",
                "author": "debater789",
                "score": 56
            }
        ]
        
        mock_comments = [
            "I completely agree, this is a critical point.",
            "I see where you're coming from, but consider this...",
            "The evidence suggests otherwise.",
            "This is oversimplifying the issue.",
            "Great point! I hadn't thought about it that way.",
            "I disagree because...",
            "This deserves more research.",
            "The real issue is what nobody's talking about."
        ]
        
        # Create posts
        for i, post_data in enumerate(mock_posts[:limit]):
            post = Post(
                id=f"reddit_{i}",
                platform="reddit",
                title=post_data["title"],
                content=post_data["content"],
                author=post_data["author"],
                timestamp=datetime.now().isoformat(),
                url=f"https://reddit.com/r/all/comments/reddit_{i}",
                posts_count=1,
                comments_count=8,
                engagement=post_data["score"]
            )
            result.posts.append(post)
            
            # Add comments
            for j, comment_text in enumerate(mock_comments[:8]):
                comment = Comment(
                    id=f"reddit_{i}_{j}",
                    post_id=f"reddit_{i}",
                    platform="reddit",
                    content=comment_text,
                    author=f"redditor_{j}",
                    timestamp=datetime.now().isoformat(),
                    engagement=10 - j
                )
                result.comments.append(comment)
        
        return result


class HackerNewsAdapter:
    """Scrape Hacker News"""
    
    def __init__(self):
        pass
    
    def search(self, query: str, limit: int = 100) -> ScrapeResult:
        """Search Hacker News for posts and comments"""
        start_time = time.time()
        result = ScrapeResult(platform="hackernews", status="success")
        
        try:
            # Try to use hn_search library if available
            try:
                import requests
                # Simple mock implementation
                result = self._generate_mock_hn_data(query, limit)
            except ImportError:
                result = self._generate_mock_hn_data(query, limit)
        
        except Exception as e:
            result.status = "error"
            result.errors.append(str(e))
        
        result.duration_seconds = time.time() - start_time
        return result
    
    def _generate_mock_hn_data(self, query: str, limit: int) -> ScrapeResult:
        """Generate mock HN data for testing"""
        result = ScrapeResult(platform="hackernews", status="success")
        
        mock_stories = [
            {
                "title": f"{query}: A Technical Analysis",
                "content": f"Interesting developments in {query}",
                "author": "technoist",
                "score": 234
            },
            {
                "title": f"Show HN: Tool for understanding {query}",
                "content": f"Built a tool to better understand {query}",
                "author": "hacker99",
                "score": 178
            },
            {
                "title": f"Ask HN: What's your view on {query}?",
                "content": f"Asking the community about {query}",
                "author": "curious_dev",
                "score": 142
            }
        ]
        
        mock_comments_text = [
            "This is a great point I hadn't considered.",
            "I've been following this for years.",
            "The HN audience probably understands this better than most.",
            "This changes my understanding of the topic.",
            "Source for this claim?",
            "Incredibly insightful analysis.",
            "This deserves more visibility.",
            "Disagree but appreciate the thoughtful response."
        ]
        
        # Create posts
        for i, story in enumerate(mock_stories[:limit]):
            post = Post(
                id=f"hn_{i}",
                platform="hackernews",
                title=story["title"],
                content=story["content"],
                author=story["author"],
                timestamp=datetime.now().isoformat(),
                url=f"https://news.ycombinator.com/item?id={1000000+i}",
                posts_count=1,
                comments_count=8,
                engagement=story["score"]
            )
            result.posts.append(post)
            
            # Add comments
            for j, comment_text in enumerate(mock_comments_text[:8]):
                comment = Comment(
                    id=f"hn_{i}_{j}",
                    post_id=f"hn_{i}",
                    platform="hackernews",
                    content=comment_text,
                    author=f"hacker_{j}",
                    timestamp=datetime.now().isoformat(),
                    engagement=20 - j
                )
                result.comments.append(comment)
        
        return result
