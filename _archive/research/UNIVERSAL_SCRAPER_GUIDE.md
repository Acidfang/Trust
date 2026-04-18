"""
UNIVERSAL PLATFORM SCRAPER - IMPLEMENTATION GUIDE
How to scrape, analyze, and compare posts+comments across all platforms

ARCHITECTURE:
├─ Base Classes (universal_platform_scraper.py)
│  ├─ UniversalPlatformAdapter (ABC) - All platforms implement this
│  ├─ Authenticator - OAuth, API key, basic auth
│  ├─ RateLimiter - Respect platform limits
│  └─ Cache - SQLite-based with TTL
│
├─ Platform Implementations (universal_platform_scraper.py)
│  ├─ LinkedInAdapter
│  ├─ TwitterAdapter
│  ├─ DiscordAdapter
│  ├─ MastodonAdapter
│  └─ More platforms (easy to add)
│
└─ Coordinator (universal_scraper_coordinator.py)
   ├─ UniversalScraperCoordinator - Unified interface
   ├─ Multi-platform orchestration
   ├─ Concurrent scraping
   └─ Result aggregation + analysis
"""

# ============================================================================
# SECTION 1: QUICK START - ONE-LINER EXAMPLES
# ============================================================================

"""
# Scrape single Twitter thread
from universal_scraper_coordinator import *

result = dedicated_platform_scrape("twitter", "machine learning")
print(f"Found {len(result.posts)} posts, {len(result.comments)} comments")

# Scrape multiple platforms at once
analysis = scrape_all_platforms("AI ethics", limit=100)
print(f"Coherence across platforms: {analysis}")

# Compare sentiment on same topic across platforms
reddit_data = dedicated_platform_scrape("reddit", "NFTs")
twitter_data = dedicated_platform_scrape("twitter", "NFTs")
mastodon_data = dedicated_platform_scrape("mastodon", "NFTs")
"""


# ============================================================================
# SECTION 2: PLATFORM AUTHENTICATION SETUP
# ============================================================================

"""
TWITTER/X:
---------
1. Create app at developer.twitter.com
2. Get API keys: API_KEY, API_SECRET, BEARER_TOKEN
3. Setup:

    from universal_scraper_coordinator import *
    
    twitter = TwitterAdapter()
    twitter.auth.authenticate_api_key("YOUR_BEARER_TOKEN")
    
    post = twitter.fetch_post("1234567890")


LINKEDIN:
--------
1. Create app at linkedin.com/developers
2. Request access to content API
3. Get OAuth credentials: CLIENT_ID, CLIENT_SECRET
4. Setup:

    from universal_platform_scraper import *
    
    linkedin = LinkedInAdapter()
    token = linkedin.auth.authenticate_oauth2(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="http://localhost:8000/callback",
        scope="w_member_social r_organization_social"
    )
    
    posts = linkedin.search("artificial intelligence", limit=100)


MASTODON (ActivityPub):
---------------------
1. Choose instance (mastodon.social, techhub.social, etc.)
2. No auth needed for public data
3. Setup:

    from universal_platform_scraper import *
    
    mastodon = MastodonAdapter(instance="mastodon.social")
    
    posts = mastodon.search("climate change", limit=100)
    
    # Optional: auth for posting/interactions
    # mastodon.auth.authenticate_oauth2(...)


DISCORD:
--------
1. Create bot at discord.com/developers
2. Get bot token and enable necessary intents
3. Setup:

    from universal_platform_scraper import *
    
    discord = DiscordAdapter()
    discord.auth.authenticate_api_key("YOUR_BOT_TOKEN")
    
    # Get messages from channel (requires channel context)
    # Note: Discord API throttles message history


REDDIT (Existing):
-----------------
Already implemented in tracker_platform_adapters.py
Uses PRAW library:

    from tracker_platform_adapters import RedditAdapter
    
    reddit = RedditAdapter(data_source="api")
    reddit.auth.authenticate_api_key("YOUR_REDDIT_API_KEY")


HACKERNEWS (Existing):
---------------------
Already implemented in tracker_platform_adapters.py
No auth needed for reading:

    from tracker_platform_adapters import HackerNewsAdapter
    
    hn = HackerNewsAdapter()
    post = hn.fetch_post("13246")
"""


# ============================================================================
# SECTION 3: COMMON SCRAPING PATTERNS
# ============================================================================

"""
PATTERN 1: Search + Analyze
---------------------------
Find what people say about a topic across platforms

    coordinator = UniversalScraperCoordinator()
    
    configs = [
        ScrapeConfig(platform="twitter", query="climate change", limit=200),
        ScrapeConfig(platform="reddit", query="climate change", limit=50),
        ScrapeConfig(platform="mastodon", query="climate change", limit=100),
    ]
    
    results = coordinator.scrape_multiple_platforms(configs)
    analysis = coordinator.analyze_scraped_data(results)
    
    # Use analysis to understand:
    # - What variations exist (different response types)
    # - What coherence score (how well variations explain responses)
    # - What constraint (unified field explaining all responses)


PATTERN 2: Thread Comparison
----------------------------
Deep-dive comparison of same topic across platforms

    # Reddit thread
    reddit_config = ScrapeConfig(
        platform="reddit",
        post_id="abc123def456",
        include_comments=True
    )
    
    # Twitter thread
    twitter_config = ScrapeConfig(
        platform="twitter",
        post_id="1234567890",
        include_comments=True
    )
    
    coordinator = UniversalScraperCoordinator()
    results = coordinator.scrape_multiple_platforms([reddit_config, twitter_config])
    
    # Compare:
    # - Response patterns (variations)
    # - Sentiment/agreement rates
    # - Information quality (coherence metrics)


PATTERN 3: Trend Detection
--------------------------
Track same query over time across platforms

    import time
    from datetime import datetime
    
    trending_phrase = "AI safety"
    results_over_time = []
    
    for day in range(7):  # 7 days
        configs = [
            ScrapeConfig(platform="twitter", query=trending_phrase),
            ScrapeConfig(platform="reddit", query=trending_phrase),
            ScrapeConfig(platform="mastodon", query=trending_phrase),
        ]
        
        daily_results = coordinator.scrape_multiple_platforms(configs)
        results_over_time.append({
            "date": datetime.now().isoformat(),
            "results": daily_results
        })
        
        time.sleep(86400)  # Wait 24 hours for next run
    
    # Analysis: How is discussion evolving? Are variations changing?


PATTERN 4: Cross-Platform Coherence
-----------------------------------
Measure how well a single model explains behavior across platforms

    # Theory: On any topic, people make 3-5 types of responses (variations)
    # Question: Does this hold across different platforms/communities?
    
    topic = "cryptocurrency regulation"
    
    coordinator = UniversalScraperCoordinator()
    
    configs = [
        ScrapeConfig(platform="reddit", query=topic),
        ScrapeConfig(platform="twitter", query=topic),
        ScrapeConfig(platform="linkedin", query=topic),
        ScrapeConfig(platform="mastodon", query=topic),
        ScrapeConfig(platform="discord", query=topic),
    ]
    
    results = coordinator.scrape_multiple_platforms(configs)
    analysis = coordinator.analyze_scraped_data(results)
    
    # Prediction: Same 3-5 variations should appear on ALL platforms
    # Hypothesis: Behavior follows universal rules (UFM) not platform-specific
"""


# ============================================================================
# SECTION 4: EXTENDING TO NEW PLATFORMS
# ============================================================================

"""
To add a new platform, implement 5 methods:

    from universal_platform_scraper import UniversalPlatformAdapter, Platform
    
    class YourPlatformAdapter(UniversalPlatformAdapter):
        def __init__(self):
            super().__init__("yourplatform")
            self.base_url = "https://api.yourplatform.com"
        
        def _get_platform_enum(self) -> Platform:
            # Add to Platform enum in universal_tracker_core.py
            return Platform.YOURPLATFORM
        
        def fetch_post(self, post_id: str, use_cache: bool = True) -> Optional[Post]:
            \"\"\"Fetch single post by ID\"\"\"
            if use_cache:
                cached = self.cache.get(f"post:{post_id}", self.platform_name)
                if cached:
                    return Post(**cached)
            
            # Make API call
            data = self._make_request("GET", f"{self.base_url}/posts/{post_id}")
            if not data:
                return None
            
            # Convert to universal Post model
            return self.create_post_from_data({
                "id": post_id,
                "title": data.get("title"),
                "text": data.get("body"),
                "timestamp": data.get("created_at"),
                "author": data.get("author_name"),
                "score": data.get("likes"),
                "url": data.get("permalink")
            }, post_id)
        
        def fetch_comments(self, post_id: str, use_cache: bool = True) -> List[Comment]:
            \"\"\"Fetch all replies to post\"\"\"
            comments = []
            data = self._make_request("GET", f"{self.base_url}/posts/{post_id}/comments")
            
            if not data:
                return comments
            
            for comment_data in data.get("comments", []):
                comment = self.create_comment_from_data({
                    "id": comment_data.get("id"),
                    "text": comment_data.get("body"),
                    "timestamp": comment_data.get("created_at"),
                    "author": comment_data.get("author_name"),
                    "score": comment_data.get("likes"),
                    "url": comment_data.get("permalink")
                }, post_id)
                comments.append(comment)
            
            return comments
        
        def search(self, query: str, limit: int = 100) -> List[Post]:
            \"\"\"Search for posts matching query\"\"\"
            posts = []
            data = self._make_request("GET", f"{self.base_url}/search", 
                                     params={"q": query, "limit": limit})
            
            if not data:
                return posts
            
            for post_data in data.get("posts", []):
                post = self.create_post_from_data({
                    "id": post_data.get("id"),
                    "title": post_data.get("title"),
                    "text": post_data.get("body"),
                    "timestamp": post_data.get("created_at"),
                    "author": post_data.get("author_name"),
                    "score": post_data.get("likes"),
                    "url": post_data.get("permalink")
                }, post_data.get("id"))
                posts.append(post)
            
            return posts
        
        def export(self, output_file: str) -> bool:
            \"\"\"Export user's data from platform\"\"\"
            # Implement data export (user downloads archive)
            return False


Then register with factory:

    from universal_platform_scraper import PlatformAdapterFactory
    from your_module import YourPlatformAdapter
    
    PlatformAdapterFactory.ADAPTERS["yourplatform"] = YourPlatformAdapter
"""


# ============================================================================
# SECTION 5: HANDLING RATE LIMITS & ERRORS
# ============================================================================

"""
Rate Limiting:
--------------
Each platform has different limits:
- Twitter: 300 requests/15 min
- Reddit: ~60 requests/min
- LinkedIn: ~100 requests/day
- Mastodon: ~300 requests/5 min
- Discord: Varies by endpoint

The RateLimiter handles this automatically:

    adapter = TwitterAdapter()
    adapter.rate_limiter = RateLimiter(requests_per_minute=20, burst_size=5)
    
    for i in range(100):
        tweet = adapter.fetch_post(tweet_id)
        # RateLimiter will automatically throttle if needed


Caching:
--------
Built-in SQLite cache avoids re-fetching:

    adapter = TwitterAdapter()
    
    # First call: fetches from API
    post = adapter.fetch_post("123", use_cache=True)
    
    # Second call: returns cached within 1 hour
    post_again = adapter.fetch_post("123", use_cache=True)
    
    # Force fresh fetch
    fresh_post = adapter.fetch_post("123", use_cache=False)
    
    # Clear cache for platform
    adapter.cache.clear("twitter")


Error Handling:
---------------
Coordinator collects errors gracefully:

    configs = [
        ScrapeConfig(platform="twitter", ...),
        ScrapeConfig(platform="reddit", ...),
    ]
    
    results = coordinator.scrape_multiple_platforms(configs)
    
    for result in results:
        if result.errors:
            print(f"{result.platform}: {result.errors}")
        else:
            print(f"{result.platform}: Success")
"""


# ============================================================================
# SECTION 6: ANALYSIS PIPELINE INTEGRATION
# ============================================================================

"""
Scraped data flows automatically to analysis:

    coordinator = UniversalScraperCoordinator()
    results = coordinator.scrape_multiple_platforms(configs)
    
    # Step 1: Trinity verification
    #   - Is source known (s ≠ ∅)?
    #   - Is causality clear (t ∈ T)?
    #   - Is it verifiable (v = true)?
    
    # Step 2: Election analysis (ZAP framework)
    #   - What conflict triggered each response?
    #   - What values motivated the author?
    #   - What control strategy did they use?
    #   - Election outcome: agreement or conflict?
    
    # Step 3: Variation discovery
    #   - Cluster similar responses
    #   - Find irreducible response types
    #   - Name variations by control strategy
    
    # Step 4: Coherence metrics (4-part proof)
    #   1. Compression Ratio: original / compressed
    #   2. Coverage: % responses matching variations
    #   3. Accuracy: % future responses predicted
    #   4. Coherence Score: combined measure
    
    # Step 5: ThreadSymbol construction
    #   - ⊙[THREAD_XXX] → β[domain] → κ⊕[invariants] → λ[fields] → Θ[constraint] → τ[confidence]
    
    analysis = coordinator.analyze_scraped_data(results)
    
    # Outputs show:
    # - What people actually argue about (conflicts)
    # - What they value (values)
    # - How they convince others (control strategies)
    # - What variations exist in responses
    # - How well a single model explains all responses (coherence)
"""


# ============================================================================
# SECTION 7: REAL-WORLD EXAMPLES
# ============================================================================

"""
Example 1: Compare AI Safety Discussion
---------------------------------------

    coordinator = UniversalScraperCoordinator()
    
    configs = [
        ScrapeConfig(platform="twitter", query="AI safety alignment", limit=200),
        ScrapeConfig(platform="reddit", post_id="xyz123", include_comments=True),
        ScrapeConfig(platform="mastodon", query="AI safety", limit=100),
    ]
    
    results = coordinator.scrape_multiple_platforms(configs)
    analysis = coordinator.analyze_scraped_data(results)
    
    # Hypothesis validation:
    # Do all platforms show same response patterns?
    # Or does platform shape discussion differently?
    
    # If variations are identical: UFM works across platforms
    # If variations differ: Platform shapes discussion
    
    for platform_analysis in analysis["platform_analyses"].values():
        print(f"Variations found: {platform_analysis['variations']}")
        print(f"Coherence: {platform_analysis['metrics']['coherence_score']:.3f}")


Example 2: Track Topic Evolution
-------------------------------

    coordinator = UniversalScraperCoordinator()
    
    for week in range(12):  # Track 12 weeks
        configs = [
            ScrapeConfig(
                platform="twitter",
                query="cryptocurrency regulation",
                limit=500
            ),
            ScrapeConfig(
                platform="reddit",
                query="cryptocurrency regulation",
                limit=100
            ),
        ]
        
        results = coordinator.scrape_multiple_platforms(configs)
        analysis = coordinator.analyze_scraped_data(results)
        
        # Key metrics to track:
        # - Are variations changing?
        # - Is coherence increasing (more unified view)?
        # - Are new arguments emerging?
        
        print(f"Week {week}: Coherence = {analysis['platform_analyses']['twitter']['metrics']['coherence_score']:.3f}")
        
        # Wait a week
        time.sleep(604800)


Example 3: Platform Comparison
-----------------------------

    coordinator = UniversalScraperCoordinator()
    
    topic = "climate change solutions"
    
    platforms = ["twitter", "reddit", "mastodon", "linkedin"]
    
    for platform in platforms:
        config = ScrapeConfig(
            platform=platform,
            query=topic,
            limit=500,
            include_comments=True
        )
        
        result = coordinator.scrape_single_platform(config)
        
        # Each platform the same data -> Does analysis differ?
        analyze_result = coordinator.analyze_scraped_data([result])
        
        print(f"\n{platform.upper()}")
        print(f"  Posts: {len(result.posts)}")
        print(f"  Comments: {len(result.comments)}")
        print(f"  Variations: {len(analyze_result['platform_analyses'].get(platform, {}).get('variations', {}))}")
"""


# ============================================================================
# SECTION 8: OUTPUT FORMATS
# ============================================================================

"""
Coordinator outputs:

1. ScrapeResult (per-platform):
   {
     "platform": "twitter",
     "status": "success",
     "posts_count": 150,
     "comments_count": 3245,
     "errors": [],
     "duration_seconds": 12.5,
     "timestamp": "2026-04-18T12:30:45.123Z"
   }

2. Analysis output (multi-platform):
   {
     "total_posts": 410,
     "total_comments": 8234,
     "platforms_analyzed": 3,
     "platform_analyses": {
       "twitter": {
         "symbol": "⊙[THREAD_abc123]",
         "metrics": {
           "compression_ratio": 6.2,
           "coverage": 0.87,
           "accuracy": 0.75,
           "coherence_score": 0.82
         },
         "variations": {
           "VAR_001": "Evidence Citation (Agreement)",
           "VAR_002": "Value Assertion (Conflict)"
         },
         "comments_analyzed": 3245
       },
       "reddit": {...},
       "mastodon": {...}
     },
     "timestamp": "2026-04-18T12:31:30.456Z"
   }

3. Exported JSON:
   {
     "timestamp": "2026-04-18T12:32:00Z",
     "platforms": [...],
     "total_posts": 410,
     "total_comments": 8234,
     "posts": [...full post data...],
     "comments": [...full comment data...]
   }
"""
