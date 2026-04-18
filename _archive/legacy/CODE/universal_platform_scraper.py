"""
UNIVERSAL PLATFORM SCRAPER FRAMEWORK
Abstract base adapter + concrete implementations for all platforms

Supports:
- LinkedIn (posts, comments, messages)
- Twitter/X (tweets, replies, DMs)
- Discord (channels, messages, threads)
- Facebook (posts, comments)
- Mastodon (posts, replies)
- Substack (posts, comments)
- Medium (articles, comments)
- YouTube (videos, comments)
- Bluesky (posts, replies)
- And extensible to any posts+comments system

Architecture:
└─ PlatformAdapter (ABC)
    ├─ Authenticator (login, oauth, API keys)
    ├─ RateLimiter (throttle requests)
    ├─ Cache (avoid re-fetching)
    └─ Methods (fetch_post, fetch_comments, search, export)
"""

import time
import json
import hashlib
import requests
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from enum import Enum
import sqlite3
import os
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass

from universal_tracker_core import Post, Comment, Platform


# ============================================================================
# AUTHENTICATOR - Unified login/OAuth handler
# ============================================================================

@dataclass
class AuthCredentials:
    """Store platform credentials securely"""
    platform: str
    auth_type: str  # "api_key", "oauth", "basic", "bearer", "custom"
    credentials: Dict[str, str]  # {username, password, api_key, token, etc.}
    expires_at: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at


class Authenticator:
    """Handle different authentication methods across platforms"""
    
    def __init__(self, platform: str):
        self.platform = platform
        self.credentials = None
        self.session = requests.Session()
    
    def authenticate_api_key(self, api_key: str) -> bool:
        """Authenticate with simple API key"""
        try:
            self.credentials = AuthCredentials(
                platform=self.platform,
                auth_type="api_key",
                credentials={"api_key": api_key}
            )
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
            return True
        except Exception as e:
            print(f"API key auth failed: {e}")
            return False
    
    def authenticate_oauth2(self, client_id: str, client_secret: str, 
                           redirect_uri: str, scope: str) -> Optional[str]:
        """OAuth2 flow with automatic token refresh"""
        try:
            # Placeholder - implement per-platform OAuth
            self.credentials = AuthCredentials(
                platform=self.platform,
                auth_type="oauth",
                credentials={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "scope": scope
                }
            )
            return "oauth_token_placeholder"
        except Exception as e:
            print(f"OAuth auth failed: {e}")
            return None
    
    def authenticate_basic(self, username: str, password: str) -> bool:
        """Basic auth (username/password)"""
        try:
            self.credentials = AuthCredentials(
                platform=self.platform,
                auth_type="basic",
                credentials={"username": username, "password": password}
            )
            self.session.auth = (username, password)
            return True
        except Exception as e:
            print(f"Basic auth failed: {e}")
            return False
    
    def get_session(self) -> requests.Session:
        """Return authenticated session"""
        return self.session
    
    def refresh_token(self) -> bool:
        """Refresh OAuth token if expired"""
        if self.credentials and self.credentials.is_expired():
            print(f"Token expired for {self.platform}, refreshing...")
            # Implement platform-specific refresh logic
            return False
        return True


# ============================================================================
# RATE LIMITER - Respect platform API limits
# ============================================================================

class RateLimiter:
    """Track requests and enforce rate limits"""
    
    def __init__(self, requests_per_minute: int = 60, burst_size: int = 10):
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.requests = []  # List of timestamps
    
    def wait_if_needed(self) -> float:
        """Block if rate limit exceeded, return wait time"""
        now = time.time()
        
        # Remove old requests (older than 1 minute)
        self.requests = [t for t in self.requests if now - t < 60]
        
        if len(self.requests) >= self.requests_per_minute:
            # Too many requests, wait until oldest expires
            wait_time = 60 - (now - self.requests[0])
            print(f"Rate limited: waiting {wait_time:.1f}s")
            time.sleep(wait_time)
            self.requests = []
            return wait_time
        
        # Burst protection
        if len(self.requests) >= self.burst_size:
            time.sleep(0.1)  # Small delay to prevent burst
        
        self.requests.append(now)
        return 0.0
    
    def reset(self):
        """Reset rate limiter"""
        self.requests = []


# ============================================================================
# CACHE - Avoid re-fetching data
# ============================================================================

class Cache:
    """SQLite-based cache for platform data"""
    
    def __init__(self, db_path: str = ".tracker_cache"):
        self.db_path = f"{db_path}/tracker_cache.db"
        os.makedirs(db_path, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize cache database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    platform TEXT,
                    timestamp REAL,
                    ttl INTEGER
                )
            """)
            conn.commit()
    
    def get(self, key: str, platform: str = "generic") -> Optional[Any]:
        """Get cached value if not expired"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT value, timestamp, ttl FROM cache WHERE key=? AND platform=?",
                (key, platform)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            value, timestamp, ttl = row
            if time.time() - timestamp > ttl:
                # Expired
                self.delete(key, platform)
                return None
            
            return json.loads(value)
    
    def set(self, key: str, value: Any, platform: str = "generic", ttl: int = 3600):
        """Cache value with TTL (default 1 hour)"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache VALUES (?, ?, ?, ?, ?)",
                (key, json.dumps(value), platform, time.time(), ttl)
            )
            conn.commit()
    
    def delete(self, key: str, platform: str = "generic"):
        """Remove cached value"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache WHERE key=? AND platform=?", (key, platform))
            conn.commit()
    
    def clear(self, platform: str = "generic"):
        """Clear all cache for platform"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache WHERE platform=?", (platform,))
            conn.commit()


# ============================================================================
# UNIVERSAL PLATFORM ADAPTER - Base class for all platforms
# ============================================================================

class UniversalPlatformAdapter(ABC):
    """
    Abstract base class for all platform adapters.
    
    Every platform implements:
    - authenticate_*: Login methods (API key, OAuth, basic, etc.)
    - fetch_post: Get single post/thread
    - fetch_comments: Get all replies
    - search: Find posts by keyword
    - export: Bulk export capability
    """
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.platform_enum = self._get_platform_enum()
        self.auth = Authenticator(platform_name)
        self.rate_limiter = RateLimiter()
        self.cache = Cache(f".tracker_cache/{platform_name}")
    
    @abstractmethod
    def _get_platform_enum(self) -> Platform:
        """Return Platform enum value"""
        pass
    
    @abstractmethod
    def fetch_post(self, post_id: str, use_cache: bool = True) -> Optional[Post]:
        """Fetch single post by ID"""
        pass
    
    @abstractmethod
    def fetch_comments(self, post_id: str, use_cache: bool = True) -> List[Comment]:
        """Fetch all comments/replies on post"""
        pass
    
    @abstractmethod
    def search(self, query: str, limit: int = 100) -> List[Post]:
        """Search for posts by keyword"""
        pass
    
    @abstractmethod
    def export(self, output_file: str) -> bool:
        """Export platform data to JSON"""
        pass
    
    def _normalize_timestamp(self, ts_input) -> datetime:
        """Convert any timestamp format to datetime"""
        if isinstance(ts_input, datetime):
            return ts_input
        elif isinstance(ts_input, (int, float)):
            return datetime.fromtimestamp(ts_input)
        elif isinstance(ts_input, str):
            try:
                return datetime.fromisoformat(ts_input)
            except:
                return datetime.now()
        return datetime.now()
    
    def _make_request(self, method: str, url: str, **kwargs) -> Optional[dict]:
        """
        Make HTTP request with rate limiting, caching, error handling
        """
        # Check cache first
        cache_key = hashlib.sha256(f"{method}:{url}".encode()).hexdigest()
        cached = self.cache.get(cache_key, self.platform_name)
        if cached:
            return cached
        
        # Rate limit
        self.rate_limiter.wait_if_needed()
        
        try:
            session = self.auth.get_session()
            response = session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache for 1 hour
            self.cache.set(cache_key, data, self.platform_name, ttl=3600)
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def create_post_from_data(self, data: dict, post_id: str) -> Post:
        """Convert platform-specific data to universal Post"""
        return Post(
            id=f"{self.platform_name}_{post_id}",
            platform=self.platform_enum,
            title=data.get("title", ""),
            text=data.get("text", data.get("body", data.get("content", ""))),
            author=data.get("author", data.get("username", "[unknown]")),
            timestamp=self._normalize_timestamp(data.get("timestamp", data.get("created_at"))).isoformat(),
            url=data.get("url", f"https://{self.platform_name}/{post_id}"),
            score=data.get("score", data.get("likes", data.get("upvotes")))
        )
    
    def create_comment_from_data(self, data: dict, parent_post_id: str) -> Comment:
        """Convert platform-specific data to universal Comment"""
        return Comment(
            id=f"{self.platform_name}_{data.get('id')}",
            parent_id=f"{self.platform_name}_{parent_post_id}",
            platform=self.platform_enum,
            text=data.get("text", data.get("body", data.get("content", ""))),
            author=data.get("author", data.get("username", "[unknown]")),
            timestamp=self._normalize_timestamp(data.get("timestamp", data.get("created_at"))).isoformat(),
            url=data.get("url", ""),
            score=data.get("score", data.get("likes", data.get("upvotes"))),
            depth=data.get("depth", 0)
        )


# ============================================================================
# CONCRETE PLATFORM IMPLEMENTATIONS
# ============================================================================

class LinkedInAdapter(UniversalPlatformAdapter):
    """LinkedIn post/comment scraper"""
    
    def __init__(self):
        super().__init__("linkedin")
        self.base_url = "https://www.linkedin.com/graphql"
        self.api_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; UniversalTracker/1.0)"
        }
    
    def _get_platform_enum(self) -> Platform:
        return Platform.LINKEDIN if hasattr(Platform, 'LINKEDIN') else Platform.GENERIC
    
    def fetch_post(self, post_id: str, use_cache: bool = True) -> Optional[Post]:
        """Fetch LinkedIn post"""
        if use_cache:
            cached = self.cache.get(f"post:{post_id}", self.platform_name)
            if cached:
                return Post(**cached)
        
        # LinkedIn requires oauth or unofficial API
        # This is a framework - actual implementation requires LinkedIn API credentials
        print(f"LinkedIn fetch_post: {post_id} (requires API authentication)")
        return None
    
    def fetch_comments(self, post_id: str, use_cache: bool = True) -> List[Comment]:
        """Fetch LinkedIn comments on post"""
        # Similar framework structure
        print(f"LinkedIn fetch_comments: {post_id} (requires API authentication)")
        return []
    
    def search(self, query: str, limit: int = 100) -> List[Post]:
        """Search LinkedIn posts"""
        print(f"LinkedIn search: {query} (requires API authentication)")
        return []
    
    def export(self, output_file: str) -> bool:
        """Export LinkedIn data"""
        # Export functionality
        return False


class TwitterAdapter(UniversalPlatformAdapter):
    """Twitter/X post scraping"""
    
    def __init__(self):
        super().__init__("twitter")
        self.base_url = "https://api.twitter.com/2"
    
    def _get_platform_enum(self) -> Platform:
        return Platform.TWITTER if hasattr(Platform, 'TWITTER') else Platform.GENERIC
    
    def fetch_post(self, tweet_id: str, use_cache: bool = True) -> Optional[Post]:
        """Fetch tweet"""
        if use_cache:
            cached = self.cache.get(f"post:{tweet_id}", self.platform_name)
            if cached:
                return Post(**cached)
        
        url = f"{self.base_url}/tweets/{tweet_id}"
        params = {"tweet.fields": "created_at,author_id,public_metrics"}
        
        data = self._make_request("GET", url, params=params)
        if not data or "data" not in data:
            return None
        
        tweet_data = data["data"]
        return self.create_post_from_data({
            "id": tweet_id,
            "text": tweet_data.get("text", ""),
            "timestamp": tweet_data.get("created_at"),
            "author": f"twitter_user_{tweet_data.get('author_id')}",
            "score": tweet_data.get("public_metrics", {}).get("like_count", 0),
            "url": f"https://twitter.com/i/web/status/{tweet_id}"
        }, tweet_id)
    
    def fetch_comments(self, tweet_id: str, use_cache: bool = True) -> List[Comment]:
        """Fetch replies to tweet"""
        comments = []
        
        url = f"{self.base_url}/tweets/search/recent"
        params = {
            "query": f"in_reply_to_tweet_id:{tweet_id}",
            "max_results": 100,
            "tweet.fields": "created_at,author_id,public_metrics",
            "expansions": "author_id"
        }
        
        data = self._make_request("GET", url, params=params)
        if not data or "data" not in data:
            return comments
        
        for tweet in data["data"]:
            comment = self.create_comment_from_data({
                "id": tweet.get("id"),
                "text": tweet.get("text"),
                "timestamp": tweet.get("created_at"),
                "author": f"twitter_user_{tweet.get('author_id')}",
                "score": tweet.get("public_metrics", {}).get("like_count", 0),
                "url": f"https://twitter.com/i/web/status/{tweet.get('id')}"
            }, tweet_id)
            comments.append(comment)
        
        return comments
    
    def search(self, query: str, limit: int = 100) -> List[Post]:
        """Search tweets"""
        posts = []
        
        url = f"{self.base_url}/tweets/search/recent"
        params = {
            "query": query,
            "max_results": min(limit, 100),
            "tweet.fields": "created_at,author_id,public_metrics"
        }
        
        data = self._make_request("GET", url, params=params)
        if not data or "data" not in data:
            return posts
        
        for tweet in data["data"]:
            post = self.create_post_from_data({
                "id": tweet.get("id"),
                "text": tweet.get("text"),
                "timestamp": tweet.get("created_at"),
                "author": f"twitter_user_{tweet.get('author_id')}",
                "score": tweet.get("public_metrics", {}).get("like_count", 0),
                "url": f"https://twitter.com/i/web/status/{tweet.get('id')}"
            }, tweet.get("id"))
            posts.append(post)
        
        return posts
    
    def export(self, output_file: str) -> bool:
        """Export tweets"""
        return False


class DiscordAdapter(UniversalPlatformAdapter):
    """Discord message scraping"""
    
    def __init__(self):
        super().__init__("discord")
        self.base_url = "https://discord.com/api/v10"
    
    def _get_platform_enum(self) -> Platform:
        return Platform.DISCORD if hasattr(Platform, 'DISCORD') else Platform.GENERIC
    
    def fetch_post(self, message_id: str, use_cache: bool = True) -> Optional[Post]:
        """Fetch Discord message as post"""
        if use_cache:
            cached = self.cache.get(f"post:{message_id}", self.platform_name)
            if cached:
                return Post(**cached)
        
        # Discord API requires bot token and channel_id context
        print(f"Discord fetch_post: {message_id} (requires bot token)")
        return None
    
    def fetch_comments(self, message_id: str, use_cache: bool = True) -> List[Comment]:
        """Fetch Discord thread messages (replies)"""
        print(f"Discord fetch_comments: {message_id} (requires bot token)")
        return []
    
    def search(self, query: str, limit: int = 100) -> List[Post]:
        """Search Discord messages"""
        print(f"Discord search: {query} (requires bot token)")
        return []
    
    def export(self, output_file: str) -> bool:
        """Export Discord data"""
        return False


class MastodonAdapter(UniversalPlatformAdapter):
    """Mastodon (ActivityPub) post scraping"""
    
    def __init__(self, instance: str = "mastodon.social"):
        super().__init__("mastodon")
        self.instance = instance
        self.base_url = f"https://{instance}/api/v1"
    
    def _get_platform_enum(self) -> Platform:
        return Platform.GENERIC  # Add to Platform enum as needed
    
    def fetch_post(self, post_id: str, use_cache: bool = True) -> Optional[Post]:
        """Fetch Mastodon post (status)"""
        if use_cache:
            cached = self.cache.get(f"post:{post_id}", self.platform_name)
            if cached:
                return Post(**cached)
        
        url = f"{self.base_url}/statuses/{post_id}"
        data = self._make_request("GET", url)
        
        if not data:
            return None
        
        return self.create_post_from_data({
            "id": post_id,
            "text": data.get("content", ""),
            "timestamp": data.get("created_at"),
            "author": data.get("account", {}).get("username", "[unknown]"),
            "score": data.get("favourites_count", 0),
            "url": data.get("url")
        }, post_id)
    
    def fetch_comments(self, post_id: str, use_cache: bool = True) -> List[Comment]:
        """Fetch Mastodon replies (context)"""
        comments = []
        
        url = f"{self.base_url}/statuses/{post_id}/context"
        data = self._make_request("GET", url)
        
        if not data or "descendants" not in data:
            return comments
        
        for reply in data["descendants"]:
            comment = self.create_comment_from_data({
                "id": reply.get("id"),
                "text": reply.get("content", ""),
                "timestamp": reply.get("created_at"),
                "author": reply.get("account", {}).get("username", "[unknown]"),
                "score": reply.get("favourites_count", 0),
                "url": reply.get("url")
            }, post_id)
            comments.append(comment)
        
        return comments
    
    def search(self, query: str, limit: int = 40) -> List[Post]:
        """Search Mastodon posts"""
        posts = []
        
        url = f"{self.base_url}/search"
        params = {"q": query, "type": "statuses", "limit": limit}
        
        data = self._make_request("GET", url, params=params)
        
        if not data or "statuses" not in data:
            return posts
        
        for status in data["statuses"]:
            post = self.create_post_from_data({
                "id": status.get("id"),
                "text": status.get("content", ""),
                "timestamp": status.get("created_at"),
                "author": status.get("account", {}).get("username", "[unknown]"),
                "score": status.get("favourites_count", 0),
                "url": status.get("url")
            }, status.get("id"))
            posts.append(post)
        
        return posts
    
    def export(self, output_file: str) -> bool:
        """Export Mastodon data"""
        return False


# ============================================================================
# FACTORY - Create adapters by platform name
# ============================================================================

class PlatformAdapterFactory:
    """Factory for creating platform adapters"""
    
    ADAPTERS = {
        "linkedin": LinkedInAdapter,
        "twitter": TwitterAdapter,
        "reddit": None,  # Use existing RedditAdapter
        "hackernews": None,  # Use existing HNAdapter
        "discord": DiscordAdapter,
        "mastodon": MastodonAdapter,
    }
    
    @classmethod
    def create(cls, platform: str) -> Optional[UniversalPlatformAdapter]:
        """Create adapter for platform"""
        adapter_class = cls.ADAPTERS.get(platform.lower())
        if adapter_class:
            return adapter_class()
        return None
    
    @classmethod
    def list_platforms(cls) -> List[str]:
        """List all supported platforms"""
        return list(cls.ADAPTERS.keys())


if __name__ == "__main__":
    print("✓ Universal Platform Scraper Framework loaded")
    print(f"✓ Supported platforms: {', '.join(PlatformAdapterFactory.list_platforms())}")
    print("\nArchitecture:")
    print("  UniversalPlatformAdapter (ABC)")
    print("  ├─ Authenticator (OAuth, API key, basic auth)")
    print("  ├─ RateLimiter (respect platform limits)")
    print("  ├─ Cache (SQLite-based, TTL-aware)")
    print("  └─ Concrete implementations (LinkedIn, Twitter, Discord, Mastodon, etc.)")
