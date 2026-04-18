"""
UNIVERSAL SCRAPER COORDINATOR
Unified interface for scraping + analyzing across all platforms

Orchestrates:
1. Platform adapter selection and authentication
2. Multi-platform concurrent scraping
3. Integration with analysis pipeline
4. Result aggregation and deduplication
5. Export and reporting
"""

from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time

from universal_tracker_core import Post, Comment, Platform
from tracker_analysis_engine import ElectionAnalyzer, VariationDiscoverer, CoherenceCalculator
from tracker_pipeline import UniversalTrackerPipeline
from universal_platform_scraper import (
    UniversalPlatformAdapter, 
    PlatformAdapterFactory,
    LinkedInAdapter,
    TwitterAdapter,
    DiscordAdapter,
    MastodonAdapter
)


# ============================================================================
# SCRAPE CONFIGURATION
# ============================================================================

@dataclass
class ScrapeConfig:
    """Configuration for a scraping job"""
    platform: str
    query: Optional[str] = None
    post_id: Optional[str] = None
    limit: int = 100
    include_comments: bool = True
    use_cache: bool = True
    concurrent: bool = True
    timeout_seconds: int = 300


@dataclass
class ScrapeResult:
    """Result of scraping a single platform"""
    platform: str
    status: str  # "success", "partial", "failed"
    posts: List[Post] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "platform": self.platform,
            "status": self.status,
            "posts_count": len(self.posts),
            "comments_count": len(self.comments),
            "errors": self.errors,
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp.isoformat()
        }


# ============================================================================
# SCRAPER COORDINATOR
# ============================================================================

class UniversalScraperCoordinator:
    """
    One interface for scraping any platform
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.adapters: Dict[str, UniversalPlatformAdapter] = {}
        self.results: List[ScrapeResult] = []
        self.pipeline = UniversalTrackerPipeline()
    
    def register_adapter(self, platform: str, adapter: UniversalPlatformAdapter) -> bool:
        """Register a custom adapter"""
        try:
            self.adapters[platform] = adapter
            return True
        except Exception as e:
            print(f"Failed to register {platform}: {e}")
            return False
    
    def get_adapter(self, platform: str) -> Optional[UniversalPlatformAdapter]:
        """Get adapter, creating if needed"""
        platform_lower = platform.lower()
        
        if platform_lower in self.adapters:
            return self.adapters[platform_lower]
        
        # Try to create from factory
        adapter = PlatformAdapterFactory.create(platform_lower)
        if adapter:
            self.adapters[platform_lower] = adapter
            return adapter
        
        return None
    
    def scrape_single_platform(self, config: ScrapeConfig) -> ScrapeResult:
        """Scrape one platform"""
        result = ScrapeResult(platform=config.platform)
        start = time.time()
        
        try:
            adapter = self.get_adapter(config.platform)
            if not adapter:
                result.status = "failed"
                result.errors.append(f"No adapter for {config.platform}")
                return result
            
            print(f"[{config.platform.upper()}] Scraping...")
            
            if config.post_id:
                # Fetch specific post
                post = adapter.fetch_post(config.post_id, use_cache=config.use_cache)
                if post:
                    result.posts.append(post)
                    
                    if config.include_comments:
                        comments = adapter.fetch_comments(config.post_id, use_cache=config.use_cache)
                        result.comments.extend(comments)
                        print(f"  ├─ {len(comments)} comments")
                else:
                    result.errors.append(f"Could not fetch post {config.post_id}")
            
            elif config.query:
                # Search
                posts = adapter.search(config.query, limit=config.limit)
                result.posts.extend(posts)
                
                if config.include_comments:
                    # Fetch comments for each post
                    for post in posts[:10]:  # Limit to first 10 to avoid rate limits
                        comments = adapter.fetch_comments(post.id, use_cache=config.use_cache)
                        result.comments.extend(comments)
                        time.sleep(0.5)  # Small delay between requests
                
                print(f"  ├─ {len(posts)} posts")
                print(f"  └─ {len(result.comments)} comments")
            
            result.status = "success" if not result.errors else "partial"
        
        except Exception as e:
            result.status = "failed"
            result.errors.append(str(e))
            print(f"  ✗ Error: {e}")
        
        finally:
            result.duration_seconds = time.time() - start
        
        return result
    
    def scrape_multiple_platforms(self, configs: List[ScrapeConfig], 
                                   concurrent: bool = True) -> List[ScrapeResult]:
        """Scrape multiple platforms"""
        results = []
        
        if not concurrent or len(configs) == 1:
            # Sequential
            for config in configs:
                result = self.scrape_single_platform(config)
                results.append(result)
        else:
            # Concurrent
            with ThreadPoolExecutor(max_workers=min(self.max_workers, len(configs))) as executor:
                futures = {executor.submit(self.scrape_single_platform, config): config 
                          for config in configs}
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        config = futures[future]
                        result = ScrapeResult(platform=config.platform, status="failed")
                        result.errors.append(str(e))
                        results.append(result)
        
        self.results.extend(results)
        return results
    
    def analyze_scraped_data(self, results: List[ScrapeResult]) -> Dict:
        """
        Analyze scraped data across all platforms
        """
        combined_posts = []
        combined_comments = []
        
        # Aggregate all posts and comments
        for result in results:
            combined_posts.extend(result.posts)
            combined_comments.extend(result.comments)
        
        print(f"\n[ANALYSIS] Processing {len(combined_posts)} posts, {len(combined_comments)} comments")
        
        # Group by platform for analysis
        by_platform = {}
        for result in results:
            if result.posts or result.comments:
                by_platform[result.platform] = {
                    "posts": result.posts,
                    "comments": result.comments
                }
        
        # Run analysis on each platform's data
        platform_analyses = {}
        for platform, data in by_platform.items():
            if not data["posts"]:
                continue
            
            # Use first post as main post
            post = data["posts"][0]
            comments = data["comments"]
            
            if not comments:
                print(f"  ├─ {platform}: No comments to analyze")
                continue
            
            try:
                symbol, metrics, variations = self.pipeline.analyze_thread(post, comments)
                
                platform_analyses[platform] = {
                    "symbol": symbol,
                    "metrics": {
                        "compression_ratio": metrics.compression_ratio,
                        "coverage": metrics.coverage_percentage,
                        "accuracy": metrics.accuracy_percentage,
                        "coherence_score": metrics.coherence_score
                    },
                    "variations": {vid: v.name for vid, v in variations.items()},
                    "comments_analyzed": len(comments)
                }
                
                print(f"  ├─ {platform}: Coherence={metrics.coherence_score:.3f}, Variations={len(variations)}")
            except Exception as e:
                print(f"  ├─ {platform}: Analysis failed - {e}")
        
        return {
            "total_posts": len(combined_posts),
            "total_comments": len(combined_comments),
            "platforms_analyzed": len(platform_analyses),
            "platform_analyses": platform_analyses,
            "timestamp": datetime.now().isoformat()
        }
    
    def export_results(self, results: List[ScrapeResult], output_file: str) -> bool:
        """Export scrape results to JSON"""
        try:
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "platforms": [r.to_dict() for r in results],
                "total_posts": sum(len(r.posts) for r in results),
                "total_comments": sum(len(r.comments) for r in results),
                "posts": [p.to_json() for r in results for p in r.posts],
                "comments": [c.to_json() for r in results for c in r.comments]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"\n✓ Results exported to {output_file}")
            return True
        except Exception as e:
            print(f"✗ Export failed: {e}")
            return False
    
    def get_summary(self, results: List[ScrapeResult]) -> str:
        """Generate summary of all scraping results"""
        summary = []
        summary.append("=" * 70)
        summary.append("UNIVERSAL SCRAPER SUMMARY")
        summary.append("=" * 70)
        
        total_posts = sum(len(r.posts) for r in results)
        total_comments = sum(len(r.comments) for r in results)
        total_time = sum(r.duration_seconds for r in results)
        
        for result in results:
            status_icon = "✓" if result.status == "success" else "⚠" if result.status == "partial" else "✗"
            summary.append(f"\n{status_icon} {result.platform.upper()}")
            summary.append(f"  Posts: {len(result.posts)}")
            summary.append(f"  Comments: {len(result.comments)}")
            summary.append(f"  Time: {result.duration_seconds:.1f}s")
            
            if result.errors:
                for error in result.errors:
                    summary.append(f"  Error: {error}")
        
        summary.append("\n" + "-" * 70)
        summary.append(f"TOTALS: {total_posts} posts, {total_comments} comments")
        summary.append(f"Time: {total_time:.1f}s total")
        summary.append("=" * 70)
        
        return "\n".join(summary)


# ============================================================================
# EASY-USE INTERFACES
# ============================================================================

def scrape_reddit_and_twitter(reddit_post_id: str, twitter_query: str) -> Dict:
    """Example: Scrape both Reddit and Twitter for comparison"""
    
    coordinator = UniversalScraperCoordinator()
    
    configs = [
        ScrapeConfig(
            platform="reddit",
            post_id=reddit_post_id,
            include_comments=True
        ),
        ScrapeConfig(
            platform="twitter",
            query=twitter_query,
            limit=50,
            include_comments=True
        )
    ]
    
    results = coordinator.scrape_multiple_platforms(configs, concurrent=True)
    
    print(coordinator.get_summary(results))
    
    analysis = coordinator.analyze_scraped_data(results)
    
    return analysis


def scrape_all_platforms(query: str, limit: int = 50) -> Dict:
    """Example: Scrape all supported platforms with same query"""
    
    coordinator = UniversalScraperCoordinator()
    
    platforms = [
        "reddit",
        "twitter",
        "mastodon",
        "discord",
        "linkedin"
    ]
    
    configs = [
        ScrapeConfig(
            platform=platform,
            query=query,
            limit=limit,
            include_comments=True
        )
        for platform in platforms
    ]
    
    results = coordinator.scrape_multiple_platforms(configs, concurrent=True)
    
    print(coordinator.get_summary(results))
    
    coordinator.export_results(results, f"scrape_results_{query.replace(' ', '_')}.json")
    
    analysis = coordinator.analyze_scraped_data(results)
    
    return analysis


def dedicated_platform_scrape(platform: str, query: str) -> ScrapeResult:
    """Example: Deep scrape single platform"""
    
    coordinator = UniversalScraperCoordinator()
    
    config = ScrapeConfig(
        platform=platform,
        query=query,
        limit=500,
        include_comments=True,
        concurrent=True
    )
    
    result = coordinator.scrape_single_platform(config)
    return result


if __name__ == "__main__":
    print("✓ Universal Scraper Coordinator loaded")
    print("\nUsage examples:")
    print("  # Scrape single platform")
    print("  coordinator = UniversalScraperCoordinator()")
    print("  config = ScrapeConfig(platform='twitter', query='UFM', limit=100)")
    print("  result = coordinator.scrape_single_platform(config)")
    print("\n  # Scrape multiple platforms")
    print("  configs = [ScrapeConfig(platform='reddit', ...), ScrapeConfig(platform='twitter', ...)]")
    print("  results = coordinator.scrape_multiple_platforms(configs, concurrent=True)")
    print("\n  # Analyze across platforms")
    print("  analysis = coordinator.analyze_scraped_data(results)")
    print("\n  # Export results")
    print("  coordinator.export_results(results, 'output.json')")
