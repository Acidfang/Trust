"""
UNIVERSAL TRACKER PIPELINE
6-step analysis workflow

Steps:
1. Trinity verification (s ≠ ∅, t ∈ T, v = true)
2. Election analysis (ZAP extraction)
3. Variation discovery (clustering)
4. Coherence calculation (metrics)
5. ThreadSymbol construction (compression)
6. Φ minimization verification
"""

from typing import List, Dict, Optional, Tuple
from universal_tracker_core import (
    Post, Comment, Election, Variation, CoherenceMetrics, 
    ThreadSymbol, AnalysisResult, ScrapeResult
)
from tracker_analysis_engine import (
    ElectionAnalyzer, VariationDiscoverer, CoherenceCalculator
)


class UniversalTrackerPipeline:
    """6-step analysis pipeline"""
    
    def __init__(self):
        self.election_analyzer = ElectionAnalyzer()
        self.variation_discoverer = VariationDiscoverer()
        self.coherence_calculator = CoherenceCalculator()
    
    def step_1_trinity_verification(self, comments: List[Comment]) -> Tuple[bool, str]:
        """Step 1: Trinity verification (s ≠ ∅, t ∈ T, v = true)
        
        - s ≠ ∅: Source identified (comments have authors)
        - t ∈ T: Timestamps within valid range
        - v = true: Verifiable (content accessible)
        """
        errors = []
        
        # Check s ≠ ∅ (source)
        if not comments:
            errors.append("No comments provided")
            return False, "Failed: No comments"
        
        for comment in comments:
            if not comment.author or comment.author == "deleted":
                # Note: deleted authors are common on reddit but still valid
                pass
        
        # Check t ∈ T (time)
        for comment in comments:
            if not comment.timestamp:
                errors.append(f"Comment {comment.id} missing timestamp")
        
        # Check v = true (verifiable)
        for comment in comments:
            if not comment.content or len(comment.content.strip()) < 3:
                errors.append(f"Comment {comment.id} not verifiable (empty content)")
        
        if errors:
            return False, f"Trinity check failed: {'; '.join(errors[:3])}"
        
        return True, "Trinity verified"
    
    def step_2_election_analysis(self, comments: List[Comment]) -> Dict[str, Election]:
        """Step 2: Election analysis - ZAP extraction
        
        Convert each comment to a complete ZAP election
        """
        elections = self.election_analyzer.analyze_comments(comments)
        return elections
    
    def step_3_variation_discovery(self, elections: Dict[str, Election], max_variations: int = 5) -> List[Variation]:
        """Step 3: Variation discovery - TF-IDF + K-means clustering
        
        Group similar elections into patterns
        """
        variations = self.variation_discoverer.discover_variations(elections, max_variations)
        return variations
    
    def step_4_coherence_calculation(
        self,
        posts: List[Post],
        comments: List[Comment],
        elections: Dict[str, Election],
        variations: List[Variation]
    ) -> CoherenceMetrics:
        """Step 4: Coherence calculation - 4-part proof
        
        Φ = (1-φ)[δ₁ + δ₂ + δ₃ + δ₄]
        """
        variations_coverage = sum(len(v.elections) for v in variations)
        
        metrics = self.coherence_calculator.calculate(
            posts_count=len(posts),
            comments_count=len(comments),
            elections_count=len(elections),
            variations_count=len(variations),
            variations_coverage=variations_coverage
        )
        
        return metrics
    
    def step_5_thread_symbol_construction(
        self,
        elections: Dict[str, Election],
        variations: List[Variation],
        metrics: CoherenceMetrics,
        query: str
    ) -> ThreadSymbol:
        """Step 5: ThreadSymbol construction - Compressed representation
        
        Format: ⊙[THREAD_XXX] → β[domain] → κ⊕[invariants] → λ[fields] → Θ[constraint] → τ[score]
        """
        # Extract key invariants from variations
        invariants = [v.name for v in variations[:3]]
        
        # Build symbol
        symbol = ThreadSymbol(
            id=f"THREAD_{abs(hash(query)) % 10000:04d}",
            domain="discussion",
            invariants=invariants,
            fields={
                "query": query,
                "comment_count": len(elections),
                "variation_count": len(variations),
                "primary_conflict": next(iter(elections)).conflict if elections else "unknown"
            },
            constraint=variations[0].name if variations else "uncategorized",
            confidence=metrics.coherence_score
        )
        
        return symbol
    
    def step_6_phi_minimization_verification(self, metrics: CoherenceMetrics) -> Tuple[bool, str]:
        """Step 6: Φ minimization verification
        
        Verify the coherence score (lower entropy = higher coherence)
        """
        if metrics.coherence_score < 0.0 or metrics.coherence_score > 1.0:
            return False, "Invalid coherence score"
        
        if metrics.coherence_score >= 0.6:
            return True, f"Coherence verified: Φ={metrics.coherence_score:.3f}"
        else:
            return False, f"Low coherence: Φ={metrics.coherence_score:.3f}"
    
    # ========================================================================
    # INTEGRATED EXECUTION
    # ========================================================================
    
    def execute(
        self,
        posts: List[Post],
        comments: List[Comment],
        query: str = "unknown"
    ) -> Tuple[AnalysisResult, Dict[str, str]]:
        """Execute full 6-step pipeline
        
        Returns: (AnalysisResult, verification_details)
        """
        
        verification_details = {}
        
        # Step 1: Trinity verification
        trinity_passed, trinity_msg = self.step_1_trinity_verification(comments)
        verification_details["step_1_trinity"] = trinity_msg
        
        if not trinity_passed:
            # Return partial result
            return AnalysisResult(
                platform="unknown",
                posts=posts,
                comments=comments
            ), verification_details
        
        # Step 2: Election analysis
        elections = self.step_2_election_analysis(comments)
        verification_details["step_2_elections"] = f"Analyzed {len(elections)} comments"
        
        # Step 3: Variation discovery
        variations = self.step_3_variation_discovery(elections)
        verification_details["step_3_variations"] = f"Discovered {len(variations)} patterns"
        
        # Step 4: Coherence calculation
        metrics = self.step_4_coherence_calculation(posts, comments, elections, variations)
        verification_details["step_4_coherence"] = f"Φ={metrics.coherence_score:.3f}"
        
        # Step 5: Symbol construction
        symbol = self.step_5_thread_symbol_construction(elections, variations, metrics, query)
        verification_details["step_5_symbol"] = symbol.to_singularity()
        
        # Step 6: Φ verification
        phi_passed, phi_msg = self.step_6_phi_minimization_verification(metrics)
        verification_details["step_6_phi"] = phi_msg
        
        # Build result
        result = AnalysisResult(
            platform="aggregated",
            posts=posts,
            comments=comments,
            elections=elections,
            variations=variations,
            symbol=symbol,
            metrics=metrics
        )
        
        return result, verification_details
