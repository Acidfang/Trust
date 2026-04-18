"""
ELECTION ANALYZER & COHERENCE METRICS
Implement core UFM analysis logic for posts+comments

Converts platform data through:
1. Election Analysis (ZAP framework per comment)
2. Variation Discovery (cluster elections)
3. Coherence Metrics (4-part Φ proof)
"""

from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import hashlib
import json
from datetime import datetime
from enum import Enum

from universal_tracker_core import (
    Post, Comment, Election, Variation, ThreadConstraint, 
    CausalEvent, CoherenceMetrics, ThreadSymbol, Platform
)


# ============================================================================
# PHASE 2A: ELECTION ANALYZER (ZAP Framework Extraction)
# ============================================================================

class ElectionOutcome(Enum):
    """Binary election outcome"""
    AGREEMENT = 1
    CONFLICT = 0


class ZAPAnalyzer:
    """
    Extract ZAP components from comment text
    CONFLICT → VALUES → CONTROL → UNCERTAINTY → CHOICES → INSIGHT
    """
    
    # Conflict markers
    CONFLICT_KEYWORDS = {
        'disagree', 'wrong', 'incorrect', 'false', 'mistake', 'error',
        'contradicts', 'contradicting', 'opposes', 'opposed', 'against',
        'but', 'however', 'although', 'yet', 'still',
        'problem', 'issue', 'flaw', 'fallacy', 'nonsense'
    }
    
    AGREEMENT_KEYWORDS = {
        'agree', 'correct', 'right', 'well said', 'exactly', 'precisely',
        'indeed', 'true', 'yes', 'absolutely', 'definitely', 'certainly',
        'good point', 'good catch', 'well done', 'great', 'excellent'
    }
    
    UNCERTAINTY_KEYWORDS = {
        'maybe', 'perhaps', 'possibly', 'might', 'could', 'may be',
        'uncertain', 'unclear', 'unknown', 'question', 'doubt', 'wonder',
        '?', 'what if', 'what about', 'consider'
    }
    
    EVIDENCE_KEYWORDS = {
        'study', 'research', 'evidence', 'data', 'statistics', 'source',
        'cite', 'reference', 'according to', 'based on', 'shows that',
        'document', 'proof', 'example', 'case study', 'research shows'
    }
    
    VALUE_KEYWORDS = {
        'believe', 'should', 'ought', 'important', 'value', 'matter',
        'care', 'principle', 'ethics', 'morality', 'right', 'wrong',
        'fundamental', 'core', 'essential'
    }
    
    @staticmethod
    def extract_conflict(text: str) -> str:
        """What contradiction triggered this response?"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['wrong', 'false', 'incorrect', 'mistake']):
            return "Claims statement is factually wrong"
        elif any(kw in text_lower for kw in ['disagree', 'opposes', 'against']):
            return "Disagrees with position or claim"
        elif any(kw in text_lower for kw in ['problem', 'issue', 'flaw', 'fallacy']):
            return "Identifies logical flaw or weakness"
        elif any(kw in text_lower for kw in ['but', 'however', 'although', 'yet']):
            return "Provides counterargument or exception"
        elif any(kw in text_lower for kw in ['?', 'what about', 'what if']):
            return "Raises uncertain or unanswered question"
        else:
            return "General response or discussion"
    
    @staticmethod
    def extract_values(text: str) -> str:
        """What matters to the commenter?"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['evidence', 'data', 'research', 'study']):
            return "Belief in evidence-based reasoning"
        elif any(kw in text_lower for kw in ['ought', 'should', 'must', 'need']):
            return "Normative principles (what should be)"
        elif any(kw in text_lower for kw in ['ethics', 'moral', 'principle', 'integrity']):
            return "Ethical or moral values"
        elif any(kw in text_lower for kw in ['experience', 'personally', 'found that', 'happened']):
            return "Direct personal experience"
        elif any(kw in text_lower for kw in ['community', 'society', 'people', 'everyone']):
            return "Social or collective welfare"
        else:
            return "Unstated or implicit values"
    
    @staticmethod
    def extract_control(text: str) -> str:
        """What leverage did they use?"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['study shows', 'research shows', 'data shows', 'evidence']):
            return "Use of citations and external evidence"
        elif any(kw in text_lower for kw in ['i personally', 'i found', 'my experience', 'i learned']):
            return "Personal authority and lived experience"
        elif any(kw in text_lower for kw in ['logic', 'therefore', 'because', 'since']):
            return "Logical argument or reasoning"
        elif any(kw in text_lower for kw in ['expert', 'professional', 'trained', 'certified']):
            return "Claims to expertise or authority"
        elif any(kw in text_lower for kw in ['most people', 'everyone', 'common', 'obvious']):
            return "Appeal to common sense or consensus"
        else:
            return "Unspecified control strategy"
    
    @staticmethod
    def extract_uncertainty(text: str) -> str:
        """What gaps or unknowns?"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['?', 'what about', 'but what', 'what if']):
            return "Unanswered questions or exceptions"
        elif any(kw in text_lower for kw in ['maybe', 'perhaps', 'possibly', 'might']):
            return "Acknowledged uncertainty"
        elif any(kw in text_lower for kw in ['not clear', 'unclear', 'ambiguous', 'vague']):
            return "Information gaps identified"
        elif any(kw in text_lower for kw in ['depends on', 'it depends', 'circumstances', 'context']):
            return "Context-dependent factors"
        else:
            return "No explicit uncertainty acknowledged"
    
    @staticmethod
    def extract_choices(comment_text: str, post_text: str) -> List[str]:
        """What options did commenter have?"""
        # Generic choices that exist for any response
        return [
            "Agree with post/prior comment",
            "Disagree or provide counterargument",
            "Ask clarifying question",
            "Share personal experience or anecdote",
            "Cite evidence or authority",
            "Remain silent (don't respond)"
        ]
    
    @staticmethod
    def extract_insight(text: str) -> str:
        """What did they conclude (their actual response)?"""
        text_lower = text.lower()
        
        # Sample first sentence and key claims
        sentences = text.split('.')
        if sentences:
            return sentences[0][:100]  # First 100 chars of first sentence
        return text[:100]
    
    @staticmethod
    def detect_outcome(text: str) -> int:
        """Did they elect agreement (1) or conflict (0)?"""
        text_lower = text.lower()
        
        agreement_count = sum(1 for kw in ZAPAnalyzer.AGREEMENT_KEYWORDS if kw in text_lower)
        conflict_count = sum(1 for kw in ZAPAnalyzer.CONFLICT_KEYWORDS if kw in text_lower)
        
        if agreement_count > conflict_count:
            return 1  # Agreement
        elif conflict_count > agreement_count:
            return 0  # Conflict
        else:
            return 1 if 'good' in text_lower or 'like' in text_lower else 0
    
    @staticmethod
    def calculate_utilities(text: str) -> Tuple[float, float]:
        """
        How "good" is agreement vs conflict as choice?
        Based on sentiment and constructiveness
        """
        text_lower = text.lower()
        
        # Simple utility scoring
        agreement_score = sum(1 for kw in ZAPAnalyzer.AGREEMENT_KEYWORDS if kw in text_lower)
        conflict_score = sum(1 for kw in ZAPAnalyzer.CONFLICT_KEYWORDS if kw in text_lower)
        evidence_score = sum(1 for kw in ZAPAnalyzer.EVIDENCE_KEYWORDS if kw in text_lower)
        
        # Normalize
        total = max(agreement_score + conflict_score + 1, 1)
        utility_agree = (agreement_score + evidence_score * 0.5) / total
        utility_conflict = conflict_score / total
        
        return float(utility_agree), float(utility_conflict)


class ElectionAnalyzer:
    """
    Analyze each comment as ZAP election
    """
    
    def __init__(self):
        self.zap = ZAPAnalyzer()
    
    def analyze_comment(self, comment: Comment, post: Post, parent_event_id: Optional[str] = None) -> Election:
        """
        Analyze single comment as complete ZAP election
        """
        election = Election(
            comment_id=comment.id,
            post_id=post.id,
            timestamp=comment.timestamp,
            
            # ZAP analysis
            conflict=self.zap.extract_conflict(comment.text),
            values=self.zap.extract_values(comment.text),
            control=self.zap.extract_control(comment.text),
            uncertainty=self.zap.extract_uncertainty(comment.text),
            choices=self.zap.extract_choices(comment.text, post.text),
            insight=self.zap.extract_insight(comment.text),
            
            # Election outcome
            elected=self.zap.detect_outcome(comment.text),
            
            # Utilities
            utility_agree=0.0,
            utility_conflict=0.0
        )
        
        # Calculate utilities
        election.utility_agree, election.utility_conflict = self.zap.calculate_utilities(comment.text)
        
        return election


# ============================================================================
# PHASE 2B: VARIATION DISCOVERY (Clustering)
# ============================================================================

class VariationDiscoverer:
    """
    Cluster similar elections into irreducible response types
    Uses TF-IDF similarity + K-means
    """
    
    def __init__(self, min_cluster_size: int = 2):
        self.min_cluster_size = min_cluster_size
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    
    def discover_variations(self, elections: List[Election]) -> Dict[str, Variation]:
        """
        Discover variation types by clustering elections
        """
        if len(elections) < self.min_cluster_size:
            # Too few to cluster, create single synthetic variation
            return self._create_synthetic_variations(elections)
        
        # Extract features
        insights = [e.insight for e in elections]
        try:
            feature_matrix = self.vectorizer.fit_transform(insights)
        except ValueError:
            # Not enough unique words
            return self._create_synthetic_variations(elections)
        
        # Optimal clusters = min(5, n_elections / 2)
        n_clusters = max(1, min(5, len(elections) // 2))
        
        if n_clusters == 1:
            return self._create_synthetic_variations(elections)
        
        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(feature_matrix)
        
        # Build variations
        variations = {}
        for cluster_id in range(n_clusters):
            cluster_elections = [e for e, label in zip(elections, labels) if label == cluster_id]
            variation = self._create_variation_from_cluster(cluster_id, cluster_elections)
            variations[variation.id] = variation
        
        return variations
    
    def _create_synthetic_variations(self, elections: List[Election]) -> Dict[str, Variation]:
        """
        When clustering fails, create variations manually
        """
        variations = {}
        
        # Group by elected outcome
        agreements = [e for e in elections if e.elected == 1]
        conflicts = [e for e in elections if e.elected == 0]
        
        if agreements:
            var = Variation(
                id="VARIATION_agreement",
                name="Agreement/Support",
                description="Comments expressing agreement or support",
                constraint_id="discussion",
                frequency=len(agreements),
                confidence=0.8,
                examples=[e.comment_id for e in agreements[:5]]
            )
            variations[var.id] = var
        
        if conflicts:
            var = Variation(
                id="VARIATION_conflict",
                name="Disagreement/Challenge",
                description="Comments expressing disagreement or opposing views",
                constraint_id="discussion",
                frequency=len(conflicts),
                confidence=0.8,
                examples=[e.comment_id for e in conflicts[:5]]
            )
            variations[var.id] = var
        
        return variations
    
    def _create_variation_from_cluster(self, cluster_id: int, elections: List[Election]) -> Variation:
        """
        Create variation object from cluster of elections
        """
        # Determine variation type from cluster characteristics
        avg_elected = sum(e.elected for e in elections) / len(elections)
        
        if avg_elected > 0.6:
            var_type = "agreement"
            base_name = "Agreement/Support"
        elif avg_elected < 0.4:
            var_type = "conflict"
            base_name = "Disagreement/Challenge"
        else:
            var_type = "mixed"
            base_name = "Mixed Response"
        
        # Count by control type
        evidence_count = sum(1 for e in elections if 'evidence' in e.control.lower())
        value_count = sum(1 for e in elections if 'value' in e.values.lower())
        experience_count = sum(1 for e in elections if 'experience' in e.control.lower())
        
        # Name variation by most common control strategy
        if evidence_count > value_count and evidence_count > experience_count:
            name = f"Evidence Citation ({base_name})"
        elif value_count > evidence_count and value_count > experience_count:
            name = f"Value Assertion ({base_name})"
        elif experience_count > 0:
            name = f"Personal Story ({base_name})"
        else:
            name = base_name
        
        return Variation(
            id=f"VARIATION_{cluster_id}_{var_type}",
            name=name,
            description=f"Cluster {cluster_id}: {name}",
            constraint_id="discussion",
            frequency=len(elections),
            confidence=0.85,
            examples=[e.comment_id for e in elections[:5]],
            invariants=[
                f"Outcome: {'Agreement' if avg_elected > 0.5 else 'Conflict' if avg_elected < 0.5 else 'Mixed'}",
                "Comment authored independently",
                "Response to post or prior comment"
            ],
            fields_discovered=[
                "response_type",
                "outcome_elected",
                "primary_control_strategy",
                "underlying_values"
            ]
        )


# ============================================================================
# COHERENCE METRICS CALCULATION
# ============================================================================

class CoherenceCalculator:
    """
    Calculate 4-part coherence proof:
    1. Compression Ratio (original / compressed bytes)
    2. Variation Coverage (% of comments matching discovered types)
    3. Prediction Accuracy (% of future comments predicted correctly)
    4. Coherence Score (combined measure)
    """
    
    @staticmethod
    def calculate_compression(comments: List[Comment], variations: Dict[str, Variation]) -> float:
        """
        Compression Ratio = original_bytes / compressed_bytes
        
        Original: All comment text
        Compressed: Variation definitions + timeline references
        """
        # Original bytes
        original_bytes = sum(len(c.text.encode()) for c in comments)
        
        if original_bytes == 0:
            return 0.0
        
        # Compressed bytes (rough estimate)
        # Each variation definition
        var_bytes = sum(len(json.dumps(v.to_json()).encode()) for v in variations.values())
        
        # Timeline (comment_id + variation_id per comment)
        timeline_bytes = len(comments) * 50  # ~50 bytes per reference
        
        compressed_bytes = var_bytes + timeline_bytes
        
        if compressed_bytes == 0:
            return float('inf')
        
        ratio = original_bytes / compressed_bytes
        return ratio
    
    @staticmethod
    def calculate_coverage(elections: List[Election], variations: Dict[str, Variation]) -> float:
        """
        Variation Coverage = covered_comments / total_comments
        
        A comment is "covered" if it matches a discovered variation
        """
        if not elections:
            return 0.0
        
        all_examples = []
        for var in variations.values():
            all_examples.extend(var.examples)
        
        covered = len(set(all_examples))
        total = len(elections)
        
        return covered / total if total > 0 else 0.0
    
    @staticmethod
    def calculate_prediction_accuracy(elections: List[Election], variations: Dict[str, Variation]) -> float:
        """
        Prediction Accuracy = correct_predictions / total_future_comments
        
        For each comment after observation point,
        predict which variation it matches based on discovered distribution
        """
        if len(elections) < 3:
            return 0.0
        
        # Observation point: first 50% or 3 comments
        observation_point = max(3, len(elections) // 2)
        
        # Build variation distribution from observations
        observed_elections = elections[:observation_point]
        future_elections = elections[observation_point:]
        
        if not future_elections:
            return 0.0
        
        # Calculate variation frequencies
        variation_freq = {}
        for var in variations.values():
            freq = sum(1 for e in observed_elections if e.comment_id in var.examples)
            if freq > 0:
                variation_freq[var.id] = freq / len(observed_elections)
        
        if not variation_freq:
            return 0.5  # Random baseline
        
        # Predict most likely variation for each future comment
        most_likely_var = max(variation_freq, key=variation_freq.get)
        
        # Check if predictions match (simplified version)
        correct = sum(1 for e in future_elections if e.comment_id in variations[most_likely_var].examples)
        
        return correct / len(future_elections)
    
    @staticmethod
    def calculate_coherence_score(compression: float, coverage: float, accuracy: float) -> float:
        """
        Combined coherence score = weighted average of three metrics
        
        Φ minimization requires all three to be strong
        """
        # Weights
        w_compression = 0.3
        w_coverage = 0.4
        w_accuracy = 0.3
        
        # Normalize metrics to 0-1 range
        # Compression: ratio of 6:1 = good (0.167 = 16.7% compression) → score 0.8
        # Above ratio 10:1 → score 1.0
        compression_score = min(compression / 10.0, 1.0)  # Cap at 1.0
        
        # Coverage: >85% = good
        coverage_score = min(coverage / 0.85, 1.0)
        
        # Accuracy: >70% = good
        accuracy_score = min(accuracy / 0.70, 1.0)
        
        # Combined
        coherence = (w_compression * compression_score +
                    w_coverage * coverage_score +
                    w_accuracy * accuracy_score)
        
        return min(coherence, 1.0)
    
    @staticmethod
    def calculate(comments: List[Comment], elections: List[Election], 
                  variations: Dict[str, Variation]) -> CoherenceMetrics:
        """
        Calculate all coherence metrics
        """
        compression = CoherenceCalculator.calculate_compression(comments, variations)
        coverage = CoherenceCalculator.calculate_coverage(elections, variations)
        accuracy = CoherenceCalculator.calculate_prediction_accuracy(elections, variations)
        coherence = CoherenceCalculator.calculate_coherence_score(compression, coverage, accuracy)
        
        return CoherenceMetrics(
            original_bytes=sum(len(c.text.encode()) for c in comments),
            compressed_bytes=int(sum(len(c.text.encode()) for c in comments) / max(compression, 1)),
            compression_ratio=compression,
            
            total_comments=len(comments),
            covered_comments=int(len(comments) * coverage),
            coverage_percentage=coverage,
            unexplained_count=len(comments) - int(len(comments) * coverage),
            
            observation_point=max(3, len(comments) // 2),
            correct_predictions=int(len(comments) * accuracy) if len(comments) > 3 else 0,
            total_predictions=max(1, len(comments) - max(3, len(comments) // 2)),
            accuracy_percentage=accuracy,
            
            coherence_score=coherence,
            confidence=0.85
        )


# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    print("✓ Election Analyzer loaded (ZAP framework)")
    print("✓ Variation Discoverer loaded (clustering)")
    print("✓ Coherence Calculator loaded (4-metric proof)")
