"""
UNIVERSAL PLATFORM SCRAPER
Framework for scraping any platform with unified interface

Classes:
- Authenticator: OAuth2, API keys, basic auth
- RateLimiter: Platform-specific request throttling
- Cache: SQLite with TTL
- UniversalPlatformAdapter: Abstract base class
- Concrete adapters: TwitterAdapter, MastodonAdapter, etc.
"""

import sqlite3
import time
import threading
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from universal_tracker_core import ScrapeResult


class Cache:
    """SQLite caching layer with TTL"""
    
    def __init__(self, db_path: str = ".tracker_cache.db", ttl_hours: int = 1):
        self.db_path = db_path
        self.ttl_seconds = ttl_hours * 3600
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"✗ Cache init error: {e}")
    
    def get(self, key: str) -> Optional[str]:
        """Get cached value if not expired"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value, timestamp FROM cache WHERE key=?", (key,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                value, timestamp = row
                if time.time() - timestamp < self.ttl_seconds:
                    return value
                else:
                    # Expired
                    self.delete(key)
                    return None
            return None
        except Exception as e:
            print(f"✗ Cache get error: {e}")
            return None
    
    def set(self, key: str, value: str):
        """Store value with timestamp"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)",
                (key, value, time.time())
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"✗ Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete cached value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cache WHERE key=?", (key,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"✗ Cache delete error: {e}")
    
    def clear(self, platform: str = ""):
        """Clear all cache entries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if platform:
                cursor.execute("DELETE FROM cache WHERE key LIKE ?", (f"{platform}:%",))
            else:
                cursor.execute("DELETE FROM cache")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"✗ Cache clear error: {e}")


class RateLimiter:
    """Platform-specific rate limiting"""
    
    # Platform limits: (requests_per_interval, interval_seconds)
    LIMITS = {
        "twitter": (15, 900),      # 15 requests per 15 min
        "reddit": (60, 60),         # 60 per minute
        "hackernews": (1, 0),       # No official limit
        "mastodon": (300, 300),     # 300 per 5 min
        "discord": (50, 60),        # 50 per minute
        "linkedin": (100, 3600),    # 100 per hour
    }
    
    def __init__(self, platform: str):
        self.platform = platform.lower()
        self.limit, self.interval = self.LIMITS.get(platform, (1000, 3600))
        self.request_times = []
        self.lock = threading.Lock()
    
    def wait_if_needed(self):
        """Block if rate limit exceeded"""
        with self.lock:
            now = time.time()
            # Remove old requests outside window
            self.request_times = [t for t in self.request_times if now - t < self.interval]
            
            # If at limit, wait
            if len(self.request_times) >= self.limit:
                wait_time = self.interval - (now - self.request_times[0])
                if wait_time > 0:
                    time.sleep(wait_time)
            
            self.request_times.append(time.time())


class Authenticator:
    """Handle various auth methods"""
    
    # Supported methods
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BASIC = "basic"
    TOKEN = "token"
    
    def __init__(self, method: str = "", credentials: Dict[str, str] = None):
        self.method = method
        self.credentials = credentials or {}
    
    def authenticate_oauth2(self, client_id: str, client_secret: str, scope: str = "") -> Dict[str, str]:
        """OAuth2 authentication (mock)"""
        return {
            "access_token": f"oauth2_{client_id[:8]}",
            "token_type": "Bearer",
            "expires_in": 3600
        }
    
    def authenticate_api_key(self, api_key: str, api_secret: str = "") -> Dict[str, str]:
        """API key authentication"""
        return {
            "api_key": api_key,
            "api_secret": api_secret or ""
        }
    
    def authenticate_basic(self, username: str, password: str) -> Dict[str, str]:
        """Basic auth (base64 encoded)"""
        import base64
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {
            "Authorization": f"Basic {credentials}"
        }
    
    def authenticate_token(self, token: str) -> Dict[str, str]:
        """Bearer token authentication"""
        return {
            "Authorization": f"Bearer {token}"
        }
    
    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        if self.method == self.API_KEY:
            return {"X-API-Key": self.credentials.get("api_key", "")}
        elif self.method == self.BASIC:
            return self.authenticate_basic(
                self.credentials.get("username", ""),
                self.credentials.get("password", "")
            )
        elif self.method == self.TOKEN:
            return self.authenticate_token(self.credentials.get("token", ""))
        return {}


class UniversalPlatformAdapter(ABC):
    """Abstract base class for platform adapters"""
    
    def __init__(self, platform: str, auth: Authenticator = None):
        self.platform = platform
        self.auth = auth
        self.rate_limiter = RateLimiter(platform)
        self.cache = Cache()
    
    @abstractmethod
    def search(self, query: str, limit: int = 100) -> ScrapeResult:
        """Search platform for posts"""
        pass
    
    def _cache_key(self, query: str) -> str:
        """Generate cache key"""
        return f"{self.platform}:{query}"


class TwitterAdapter(UniversalPlatformAdapter):
    """Twitter/X adapter"""
    
    def __init__(self, bearer_token: str = ""):
        super().__init__("twitter")
        self.bearer_token = bearer_token
    
    def search(self, query: str, limit: int = 100) -> ScrapeResult:
        """Search Twitter (mock implementation)"""
        # Check cache
        cache_key = self._cache_key(query)
        cached = self.cache.get(cache_key)
        if cached:
            # Parse and return cached result
            import json
            data = json.loads(cached)
            result = ScrapeResult(platform="twitter", status="success")
            # Reconstruct from JSON (simplified)
            return result
        
        # Rate limit
        self.rate_limiter.wait_if_needed()
        
        # Mock data
        result = ScrapeResult(platform="twitter", status="success")
        mock_tweets = [
            f"Thoughts on {query}? I think the key insight is...",
            f"Just learned about {query}. Mind blown 🤯",
            f"Unpopular opinion: {query} is misunderstood"
        ]
        
        from universal_tracker_core import Post, Comment
        for i, tweet_text in enumerate(mock_tweets[:limit]):
            post = Post(
                id=f"tw_{i}",
                platform="twitter",
                title="Tweet",
                content=tweet_text,
                author=f"user_{i}",
                timestamp=datetime.now().isoformat(),
                url=f"https://twitter.com/user_{i}/status/{1000000000+i}",
                posts_count=1,
                comments_count=0,
                engagement=0
            )
            result.posts.append(post)
        
        # Cache result
        import json
        self.cache.set(cache_key, json.dumps({"posts": len(result.posts)}))
        
        return result


class MastodonAdapter(UniversalPlatformAdapter):
    """Mastodon adapter"""
    
    def __init__(self, instance: str = "mastodon.social", access_token: str = ""):
        super().__init__("mastodon")
        self.instance = instance
        self.access_token = access_token
    
    def search(self, query: str, limit: int = 100) -> ScrapeResult:
        """Search Mastodon (mock)"""
        result = ScrapeResult(platform="mastodon", status="success")
        
        self.rate_limiter.wait_if_needed()
        
        from universal_tracker_core import Post, Comment
        mock_statuses = [
            f"Thoughts on {query}",
            f"Has anyone else noticed about {query}?",
            f"The {query} situation is getting interesting"
        ]
        
        for i, status_text in enumerate(mock_statuses[:limit]):
            post = Post(
                id=f"mdn_{i}",
                platform="mastodon",
                title="Status",
                content=status_text,
                author=f"user@{self.instance}",
                timestamp=datetime.now().isoformat(),
                url=f"https://{self.instance}/users/user_{i}/statuses/{1000+i}",
                posts_count=1,
                comments_count=0,
                engagement=0
            )
            result.posts.append(post)
        
        return result


class DiscordAdapter(UniversalPlatformAdapter):
    """Discord adapter (message scraping)"""
    
    def __init__(self, bot_token: str = ""):
        super().__init__("discord")
        self.bot_token = bot_token
    
    def search(self, query: str, limit: int = 100) -> ScrapeResult:
        """Search Discord messages (mock)"""
        result = ScrapeResult(platform="discord", status="success")
        
        self.rate_limiter.wait_if_needed()
        
        from universal_tracker_core import Post, Comment
        # In real implementation would search across guild channels
        result.status = "success"
        return result


class LinkedInAdapter(UniversalPlatformAdapter):
    """LinkedIn adapter"""
    
    def __init__(self, access_token: str = ""):
        super().__init__("linkedin")
        self.access_token = access_token
    
    def search(self, query: str, limit: int = 100) -> ScrapeResult:
        """Search LinkedIn (mock)"""
        result = ScrapeResult(platform="linkedin", status="success")
        
        self.rate_limiter.wait_if_needed()
        
        from universal_tracker_core import Post, Comment
        mock_posts = [
            f"Analyzing {query} from a business perspective",
            f"Industry insights: {query} is transforming markets",
            f"Professional take on {query}"
        ]
        
        for i, post_text in enumerate(mock_posts[:limit]):
            post = Post(
                id=f"lin_{i}",
                platform="linkedin",
                title="Post",
                content=post_text,
                author="Professional User",
                timestamp=datetime.now().isoformat(),
                url=f"https://linkedin.com/feed/update/urn:li:post:{1000+i}",
                posts_count=1,
                comments_count=0,
                engagement=0
            )
            result.posts.append(post)
        
        return result


# ============================================================================
# FACTORY
# ============================================================================

class PlatformAdapterFactory:
    """Create adapters by platform name"""
    
    ADAPTERS = {
        "twitter": TwitterAdapter,
        "mastodon": MastodonAdapter,
        "discord": DiscordAdapter,
        "linkedin": LinkedInAdapter,
        "reddit": lambda: "RedditAdapter",  # Define in tracker_platform_adapters.py
        "hackernews": lambda: "HackerNewsAdapter"
    }
    
    @staticmethod
    def create(platform: str, credentials: Dict[str, str] = None) -> UniversalPlatformAdapter:
        """Create adapter for platform"""
        credentials = credentials or {}
        
        if platform.lower() == "twitter":
            return TwitterAdapter(credentials.get("bearer_token", ""))
        elif platform.lower() == "mastodon":
            return MastodonAdapter(
                instance=credentials.get("instance", "mastodon.social"),
                access_token=credentials.get("access_token", "")
            )
        elif platform.lower() == "discord":
            return DiscordAdapter(credentials.get("bot_token", ""))
        elif platform.lower() == "linkedin":
            return LinkedInAdapter(credentials.get("access_token", ""))
        else:
            # Default to mock adapter
            return UniversalPlatformAdapter(platform)
    
    @staticmethod
    def list_platforms() -> List[str]:
        """List all supported platforms"""
        return list(PlatformAdapterFactory.ADAPTERS.keys())
