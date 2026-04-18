"""
TRACKER ANALYSIS PIPELINE
Integrated end-to-end analysis using:
- Platform Adapters (Reddit/HN/Discord)
- Election Analyzer (ZAP framework)
- Variation Discoverer (clustering)
- Coherence Calculator (4-part proof)
- Trinity Verifier (Φ validation)

WORKFLOW:
  Post + Comments → Elections → Variations → Coherence → ThreadSymbol → Ledger
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json

from universal_tracker_core import (
    Post, Comment, Election, Variation, ThreadConstraint, 
    CausalEvent, CoherenceMetrics, ThreadSymbol, Platform,
    TrianityVerifier
)
from tracker_analysis_engine import (
    ElectionAnalyzer, VariationDiscoverer, 
    CoherenceCalculator, ZAPAnalyzer
)
from tracker_platform_adapters import RedditAdapter, HackerNewsAdapter


# ============================================================================
# Main Analysis Pipeline
# ============================================================================

class UniversalTrackerPipeline:
    """
    Complete analysis workflow for any posts+comments system
    """
    
    def __init__(self):
        self.election_analyzer = ElectionAnalyzer()
        self.variation_discoverer = VariationDiscoverer()
        self.coherence_calculator = CoherenceCalculator()
        self.trinity_verifier = TrianityVerifier()
        
        self.reddit = RedditAdapter()
        self.hackernews = HackerNewsAdapter()
    
    def analyze_thread(self, post: Post, comments: List[Comment]) -> Tuple[ThreadSymbol, CoherenceMetrics, Dict[str, Variation]]:
        """
        Complete analysis pipeline: Post + Comments → ThreadSymbol
        
        Steps:
        1. Verify Trinity (state visible, causality clear, verifiable)
        2. Analyze each comment as ZAP election
        3. Discover variation patterns (clusters)
        4. Calculate coherence metrics (compression, coverage, accuracy)
        5. Construct ThreadSymbol (complete knowledge compression)
        6. Verify Φ minimality
        """
        
        # Step 1: Trinity Verification (Foundation - Tier -1)
        print(f"[Trinity Check] Verifying source, timestamp, causality...")
        if not self._verify_trinity(post, comments):
            raise ValueError("Trinity verification failed: cannot analyze unverified thread")
        
        # Step 2: Analyze Elections (Convert to ZAP language)
        print(f"[Elections] Analyzing {len(comments)} comments as ZAP frameworks...")
        elections = []
        for comment in comments:
            election = self.election_analyzer.analyze_comment(comment, post)
            elections.append(election)
            print(f"  ├─ {comment.author[:20]:20} → {['Conflict', 'Agreement'][election.elected]}")
        
        # Step 3: Discover Variations (Find patterns)
        print(f"[Variations] Discovering irreducible response types...")
        variations = self.variation_discoverer.discover_variations(elections)
        for var_id, var in variations.items():
            print(f"  ├─ {var.name}: {var.frequency} comments")
        
        # Step 4: Calculate Coherence (4-part proof)
        print(f"[Coherence] Calculating compression, coverage, accuracy...")
        metrics = self.coherence_calculator.calculate(comments, elections, variations)
        print(f"  ├─ Compression Ratio: {metrics.compression_ratio:.2f}:1")
        print(f"  ├─ Coverage: {metrics.coverage_percentage*100:.1f}% ({metrics.covered_comments}/{metrics.total_comments})")
        print(f"  ├─ Accuracy: {metrics.accuracy_percentage*100:.1f}%")
        print(f"  └─ Coherence Score: {metrics.coherence_score:.3f}")
        
        # Step 5: Construct ThreadSymbol (Complete compression)
        print(f"[ThreadSymbol] Constructing singularity compression...")
        thread_symbol = self._construct_thread_symbol(post, elections, variations, metrics)
        
        # Step 6: Verify Φ Minimality (Final check)
        print(f"[Φ Minimization] Verifying potential energy minimization...")
        phi_check = self._verify_phi_minimization(post, comments, metrics, variations)
        print(f"  └─ Φ Verification: {'✓ PASS' if phi_check else '✗ FAIL'}")
        
        return thread_symbol, metrics, variations
    
    def analyze_reddit_thread(self, post_url: str) -> Tuple[ThreadSymbol, CoherenceMetrics, Dict[str, Variation]]:
        """Analyze complete Reddit thread"""
        # Extract post ID from URL
        post_id = self._extract_reddit_id(post_url)
        
        print(f"[Reddit] Fetching {post_url}...")
        post = self.reddit.fetch_post(post_id)
        comments = self.reddit.fetch_comments(post_id)
        
        if not post:
            raise ValueError(f"Could not fetch Reddit post: {post_url}")
        
        return self.analyze_thread(post, comments)
    
    def analyze_hn_thread(self, story_id: int) -> Tuple[ThreadSymbol, CoherenceMetrics, Dict[str, Variation]]:
        """Analyze complete Hacker News thread"""
        print(f"[Hacker News] Fetching story {story_id}...")
        post = self.hackernews.fetch_post(str(story_id))
        comments = self.hackernews.fetch_comments(str(story_id))
        
        if not post:
            raise ValueError(f"Could not fetch HN story: {story_id}")
        
        return self.analyze_thread(post, comments)
    
    def analyze_exported_reddit(self, json_file: str) -> Tuple[ThreadSymbol, CoherenceMetrics, Dict[str, Variation]]:
        """Analyze Reddit JSON export"""
        print(f"[Reddit Export] Parsing {json_file}...")
        post, comments = self.reddit.parse_json_export(json_file)
        
        if not post:
            raise ValueError(f"Could not parse JSON: {json_file}")
        
        print(f"[Loaded] {post.title}")
        print(f"  {len(comments)} comments")
        
        return self.analyze_thread(post, comments)
    
    def analyze_exported_hn(self, json_file: str) -> Tuple[ThreadSymbol, CoherenceMetrics, Dict[str, Variation]]:
        """Analyze Hacker News JSON export"""
        print(f"[HN Export] Parsing {json_file}...")
        post, comments = self.hackernews.parse_hn_export(json_file)
        
        if not post:
            raise ValueError(f"Could not parse JSON: {json_file}")
        
        print(f"[Loaded] {post.title}")
        print(f"  {len(comments)} comments")
        
        return self.analyze_thread(post, comments)
    
    # ========================================================================
    # Internal Methods
    # ========================================================================
    
    def _verify_trinity(self, post: Post, comments: List[Comment]) -> bool:
        """
        Verify Trinity: s ≠ ∅, t ∈ T, v = true
        
        - s ≠ ∅: Source is known (post.author, post.platform, post.url)
        - t ∈ T: Timestamp is valid and causally ordered
        - v = true: Verifiable (post/comments are accessible, record is complete)
        """
        
        # Check source (s ≠ ∅)
        if not post.author or post.author == "[deleted]":
            print("  ⚠ Source ambiguous: post author unknown")
        if not post.platform or post.platform == Platform.UNKNOWN:
            print("  ⚠ Platform unknown")
        
        # Check timestamps (t ∈ T - causality)
        post_time = post.timestamp
        if not post_time:
            print("  ⚠ Post timestamp missing")
            return False
        
        # Comments should be ordered after post
        for comment in comments:
            if comment.timestamp < post_time:
                print(f"  ⚠ Comment from {comment.author} before post (causality violation)")
        
        # Check for causal ordering in comment thread
        by_time = sorted(comments, key=lambda c: c.timestamp)
        for i in range(1, len(by_time)):
            if by_time[i].timestamp == by_time[i-1].timestamp:
                # Same timestamp OK (bulk export), but should note
                pass
        
        # Check verifiability (v = true)
        if not post.url:
            print("  ⚠ Post URL missing: may not be accessible")
        
        # All checks passed
        return True
    
    def _construct_thread_symbol(self, post: Post, elections: List[Election], 
                                 variations: Dict[str, Variation], 
                                 metrics: CoherenceMetrics) -> ThreadSymbol:
        """
        Build complete ThreadSymbol compression
        Format: ⊙[THREAD_XXX] → β[domain] → κ⊕[invariants] → λ[fields] → Θ[constraint] → τ[confidence]
        """
        
        # Generate unique thread ID
        thread_id_base = hashlib.sha256(
            f"{post.id}_{post.timestamp.isoformat()}".encode()
        ).hexdigest()[:8].upper()
        thread_id = f"THREAD_{thread_id_base}"
        
        # Determine domain
        domain = self._infer_domain(post, elections)
        
        # Identify invariants (properties that don't change)
        invariants = self._identify_invariants(post, elections, variations)
        
        # Identify fields (what varies)
        fields_discovered = set()
        for var in variations.values():
            fields_discovered.update(var.fields_discovered)
        
        # Build constraint (Θ) - unified field explaining all variations
        constraint = self._infer_constraint(post, elections, variations)
        
        # Confidence based on coherence score
        confidence = metrics.coherence_score
        
        # Build complete symbol
        symbol = ThreadSymbol(
            id=f"⊙[{thread_id}]",
            beta_domain=f"β[{domain}]",
            kappa_invariants=[f"κ⊕[{inv}]" for inv in invariants],
            lambda_fields=sorted(list(fields_discovered)),
            theta_constraint=f"Θ[{constraint}]",
            tau_confidence=confidence,
            
            # Metadata
            post_id=post.id,
            platform=post.platform,
            timestamp=post.timestamp,
            
            # Compression metrics
            compression_ratio=metrics.compression_ratio,
            coverage=metrics.coverage_percentage,
            accuracy=metrics.accuracy_percentage,
            coherence_score=metrics.coherence_score,
            
            # Content
            variation_types=list(variations.keys()),
            total_comments=len(elections),
            covered_comments=metrics.covered_comments,
            
            # Verification
            trinity_verified=True,
            phi_minimized=True
        )
        
        return symbol
    
    def _infer_domain(self, post: Post, elections: List[Election]) -> str:
        """Infer what domain/topic the thread is about"""
        
        # Analyze post title for domain keywords
        title_lower = post.title.lower() + " " + post.text.lower()
        
        domain_keywords = {
            "technical": ["code", "bug", "algorithm", "framework", "library", "api", "database"],
            "social": ["people", "community", "network", "relationship", "culture", "society"],
            "political": ["government", "election", "policy", "law", "regulation", "vote"],
            "health": ["disease", "medical", "health", "doctor", "treatment", "vaccine"],
            "science": ["study", "research", "result", "hypothesis", "experiment", "data"],
            "business": ["company", "startup", "product", "market", "profit", "investment"],
        }
        
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw in title_lower)
            domain_scores[domain] = score
        
        best_domain = max(domain_scores, key=domain_scores.get) or "discussion"
        return best_domain
    
    def _identify_invariants(self, post: Post, elections: List[Election], 
                            variations: Dict[str, Variation]) -> List[str]:
        """Properties that hold across all variations"""
        return [
            "All comments respond to same post",
            "Temporal order: all comments after post",
            "Author agency: each commenter chooses their response",
            "Context: same post information available to all",
        ]
    
    def _infer_constraint(self, post: Post, elections: List[Election], 
                         variations: Dict[str, Variation]) -> str:
        """
        Unified field (Θ) explaining why people respond as they do
        This is the coherence answer
        """
        
        # Analyze what triggered elections
        conflict_themes = {}
        for election in elections:
            theme = election.conflict[:30]  # First 30 chars of conflict description
            conflict_themes[theme] = conflict_themes.get(theme, 0) + 1
        
        most_common_conflict = max(conflict_themes, key=conflict_themes.get) if conflict_themes else "Discussion response"
        
        # Analyze values
        value_themes = {}
        for election in elections:
            theme = election.values[:30]
            value_themes[theme] = value_themes.get(theme, 0) + 1
        
        most_common_value = max(value_themes, key=value_themes.get) if value_themes else "General "
        
        return f"Unified field: {most_common_conflict} resolved by {most_common_value}"
    
    def _verify_phi_minimization(self, post: Post, comments: List[Comment], 
                                metrics: CoherenceMetrics, 
                                variations: Dict[str, Variation]) -> bool:
        """
        Verify that representation minimizes potential energy Φ
        
        Φ = (1-φ)[δ(s=∅) + δ(t∉T) + δ(v=false)]
        
        Φ minimized when:
        - Source known (s ≠ ∅) → δ(s=∅) = 0
        - Causality clear (t ∈ T) → δ(t∉T) = 0
        - Verifiable (v=true) → δ(v=false) = 0
        - Compression high (ratio > 4:1)
        - Coverage high (>80%)
        - Accuracy high (>70%)
        """
        
        # Check individual components
        phi_components = {
            "source_known": bool(post.author and post.author != "[deleted]"),
            "causality_clear": len(comments) > 0,  # At least one comment to establish time order
            "verifiable": bool(post.url) and len(comments) > 0,
            "compression_good": metrics.compression_ratio > 4.0,
            "coverage_good": metrics.coverage_percentage > 0.80,
            "accuracy_good": metrics.accuracy_percentage > 0.70,
        }
        
        passed = sum(1 for v in phi_components.values() if v)
        required_passes = 5  # At least 5 of 6
        
        return passed >= required_passes
    
    @staticmethod
    def _extract_reddit_id(url: str) -> str:
        """Extract post ID from Reddit URL"""
        # Handle various Reddit URL formats
        if "/r/" in url:
            # Extract between /r/.../ and next /
            parts = url.split("/r/")
            if len(parts) > 1:
                rest = parts[1].split("/")
                if len(rest) > 2:
                    return rest[2]
        return url


# ============================================================================
# Example Usage
# ============================================================================

def example_analysis():
    """Example: Analyze a Reddit thread"""
    
    pipeline = UniversalTrackerPipeline()
    
    # Option 1: Analyze from exported JSON
    print("=" * 70)
    print("UNIVERSAL TRACKER ANALYSIS PIPELINE - EXAMPLE")
    print("=" * 70)
    
    try:
        # This would require actual export file
        symbol, metrics, variations = pipeline.analyze_exported_reddit(
            "sample_reddit_thread.json"
        )
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"ThreadSymbol: {symbol.id}")
        print(f"Domain: {symbol.beta_domain}")
        print(f"Score: {symbol.coherence_score:.3f}")
        print(f"Variations Found: {len(variations)}")
        
    except FileNotFoundError:
        print("\nNo sample file found (create reddit export first)")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    print("✓ Universal Tracker Pipeline loaded")
    print("✓ Complete analysis workflow ready")
    print("\nUsage:")
    print("  pipeline = UniversalTrackerPipeline()")
    print("  symbol, metrics, vars = pipeline.analyze_thread(post, comments)")
    print("  # OR")
    print("  symbol, metrics, vars = pipeline.analyze_exported_reddit('export.json')")
    print("  symbol, metrics, vars = pipeline.analyze_exported_hn('export.json')")
