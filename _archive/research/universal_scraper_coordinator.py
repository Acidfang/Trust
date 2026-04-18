"""
UNIVERSAL SCRAPER COORDINATOR
Orchestration layer for multi-platform scraping and analysis

Classes:
- ScrapeConfig: Configuration for scraping job
- ScrapeResult: Results from single platform
- UniversalScraperCoordinator: Main orchestrator
"""

import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from tracker_platform_adapters import RedditAdapter, HackerNewsAdapter
from universal_platform_scraper import (
    PlatformAdapterFactory, UniversalPlatformAdapter
)
from universal_tracker_core import ScrapeResult, AnalysisResult
from tracker_analysis_engine import AnalysisPipeline


@dataclass
class ScrapeConfig:
    """Configuration for scraping job"""
    platform: str
    query: str
    limit: int = 100
    include_comments: bool = True
    use_cache: bool = True
    concurrent: bool = False
    credentials: Dict[str, str] = field(default_factory=dict)


@dataclass
class ScrapeResult:
    """Results from scraping multiple platforms"""
    query: str
    platforms: List[str] = field(default_factory=list)
    results: List['PlatformScrapeResult'] = field(default_factory=list)
    duration_seconds: float = 0.0
    
    def to_json(self) -> dict:
        return {
            "query": self.query,
            "platforms": self.platforms,
            "results": [r.to_json() for r in self.results],
            "duration_seconds": self.duration_seconds
        }


@dataclass
class PlatformScrapeResult:
    """Result from single platform"""
    platform: str
    status: str
    posts: int = 0
    comments: int = 0
    errors: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    
    def to_json(self) -> dict:
        return {
            "platform": self.platform,
            "status": self.status,
            "posts": self.posts,
            "comments": self.comments,
            "errors": self.errors,
            "duration_seconds": self.duration_seconds
        }


class UniversalScraperCoordinator:
    """Orchestrate scraping across platforms"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.adapters: Dict[str, UniversalPlatformAdapter] = {}
        self.analysis_pipeline = AnalysisPipeline()
        self._init_adapters()
    
    def _init_adapters(self):
        """Initialize built-in adapters"""
        try:
            self.adapters["reddit"] = RedditAdapter()
            self.adapters["hackernews"] = HackerNewsAdapter()
        except Exception as e:
            print(f"⚠ Built-in adapters initialization: {e}")
    
    def get_adapter(self, platform: str) -> Optional[UniversalPlatformAdapter]:
        """Get or create adapter for platform"""
        platform = platform.lower()
        
        if platform not in self.adapters:
            try:
                self.adapters[platform] = PlatformAdapterFactory.create(platform)
            except Exception as e:
                print(f"✗ Failed to create adapter for {platform}: {e}")
                return None
        
        return self.adapters[platform]
    
    def scrape_single_platform(self, config: ScrapeConfig) -> 'PlatformScrapeResult':
        """Scrape single platform"""
        start_time = time.time()
        result = PlatformScrapeResult(
            platform=config.platform,
            status="queued"
        )
        
        try:
            adapter = self.get_adapter(config.platform)
            if not adapter:
                result.status = "error"
                result.errors.append(f"No adapter for {config.platform}")
                return result
            
            # Scrape
            result.status = "scraping"
            scrape_result = adapter.search(config.query, config.limit)
            
            # Convert to result
            result.status = scrape_result.status
            result.posts = len(scrape_result.posts)
            result.comments = len(scrape_result.comments)
            result.errors = scrape_result.errors
            
            return result
        
        except Exception as e:
            result.status = "error"
            result.errors.append(str(e))
            return result
        
        finally:
            result.duration_seconds = time.time() - start_time
    
    def scrape_multiple_platforms(self, configs: List[ScrapeConfig], concurrent: bool = True) -> List['PlatformScrapeResult']:
        """Scrape multiple platforms"""
        if concurrent and len(configs) > 1:
            return self._scrape_concurrent(configs)
        else:
            return self._scrape_sequential(configs)
    
    def _scrape_sequential(self, configs: List[ScrapeConfig]) -> List['PlatformScrapeResult']:
        """Scrape platforms sequentially"""
        results = []
        for config in configs:
            result = self.scrape_single_platform(config)
            results.append(result)
        return results
    
    def _scrape_concurrent(self, configs: List[ScrapeConfig]) -> List['PlatformScrapeResult']:
        """Scrape platforms concurrently"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.scrape_single_platform, config): config
                for config in configs
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=30)
                    results.append(result)
                except Exception as e:
                    config = futures[future]
                    result = PlatformScrapeResult(
                        platform=config.platform,
                        status="error",
                        errors=[str(e)]
                    )
                    results.append(result)
        
        return results
    
    def analyze_scraped_data(self, results: List['PlatformScrapeResult']) -> Dict[str, Dict]:
        """Run analysis pipeline on scraped data"""
        analysis_output = {
            "total_posts": 0,
            "total_comments": 0,
            "platforms_analyzed": 0,
            "platform_analyses": {}
        }
        
        # Note: In real implementation, we'd need to store actual post/comment objects
        # For now, this is a skeleton that the Flask API can call
        
        return analysis_output
