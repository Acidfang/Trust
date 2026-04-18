"""
TRACKER ANALYSIS ENGINE
Extracts elections (ZAP analysis), variations, and coherence metrics

Classes:
- ZAPAnalyzer: Extract Z-A-P framework from text
- ElectionAnalyzer: Convert comments to elections
- VariationDiscoverer: Cluster elections into patterns
- CoherenceCalculator: Calculate 4-part coherence proof
"""

import re
from typing import List, Dict, Optional, Tuple
from collections import Counter
from universal_tracker_core import (
    Comment, Election, Variation, CoherenceMetrics, ThreadSymbol, AnalysisResult
)


class ZAPAnalyzer:
    """Extract Z (conflict) A (values) P (control) from text
    
    Z = Core conflict or tension
    A = Values competing
    P = Power/control mechanisms
    """
    
    # Signal keywords by category
    CONFLICT_SIGNALS = {
        "vs", "versus", "versus.", "against", "oppose", "opposed", "conflict",
        "contradiction", "paradox", "tension", "disagree", "contrary", "but",
        "however", "yet", "nonetheless", "despite", "while", "although"
    }
    
    VALUE_SIGNALS = {
        "important", "value", "moral", "ethic", "principle", "belief", "system",
        "culture", "tradition", "innovation", "progress", "freedom", "justice",
        "safety", "security", "health", "prosperity", "knowledge", "truth"
    }
    
    CONTROL_SIGNALS = {
        "power", "control", "authority", "government", "corporate", "corporate",
        "institution", "regulation", "law", "policy", "decision", "choice",
        "agency", "influence", "money", "media", "lobby", "interest"
    }
    
    @staticmethod
    def extract_conflict(text: str) -> str:
        """Extract core conflict from text"""
        text_lower = text.lower()
        
        # Look for explicit conflict markers
        conflict_phrases = [
            "the problem is", "the issue is", "the conflict", "the tension",
            "the contradiction", "the paradox", "versus", "vs.", "but"
        ]
        
        for phrase in conflict_phrases:
            idx = text_lower.find(phrase.lower())
            if idx != -1:
                end_idx = min(idx + 150, len(text))
                snippet = text[idx:end_idx].strip()
                if len(snippet) > 10:
                    return snippet[:100]
        
        # Fallback: look for first sentence with conflict signals
        sentences = text.split(".")
        for sent in sentences:
            if any(signal in sent.lower() for signal in ZAPAnalyzer.CONFLICT_SIGNALS):
                return sent.strip()[:100]
        
        # Last resort: first 80 chars
        return text[:80]
    
    @staticmethod
    def extract_values(text: str) -> List[str]:
        """Extract values in tension from text"""
        text_lower = text.lower()
        words = text_lower.split()
        
        found_values = []
        for word_clean in words:
            # Remove punctuation
            word = re.sub(r'[^\w]', '', word_clean)
            if word in ZAPAnalyzer.VALUE_SIGNALS:
                found_values.append(word)
        
        # Deduplicate while preserving order
        seen = set()
        unique_values = []
        for v in found_values:
            if v not in seen:
                unique_values.append(v)
                seen.add(v)
        
        return unique_values[:5]  # Top 5
    
    @staticmethod
    def extract_control(text: str) -> str:
        """Extract power/control mechanism from text"""
        text_lower = text.lower()
        words = text_lower.split()
        
        for word_clean in words:
            word = re.sub(r'[^\w]', '', word_clean)
            if word in ZAPAnalyzer.CONTROL_SIGNALS:
                return word
        
        return "unidentified"


class ElectionAnalyzer:
    """Convert comments to ZAP elections"""
    
    def __init__(self):
        self.zap = ZAPAnalyzer()
    
    def analyze_comment(self, comment: Comment) -> Election:
        """Convert comment to election"""
        conflict = self.zap.extract_conflict(comment.content)
        values = self.zap.extract_values(comment.content)
        control = self.zap.extract_control(comment.content)
        
        # Simple confidence based on content length and signal count
        word_count = len(comment.content.split())
        signal_count = len(values)
        confidence = min(0.9, 0.3 + (signal_count * 0.1) + (min(word_count / 100, 0.4)))
        
        return Election(
            comment_id=comment.id,
            conflict=conflict,
            values=values,
            control=control,
            uncertainty="",
            choices=[],
            insight="",
            confidence=confidence
        )
    
    def analyze_comments(self, comments: List[Comment]) -> Dict[str, Election]:
        """Analyze all comments"""
        elections = {}
        for comment in comments:
            election = self.analyze_comment(comment)
            elections[comment.id] = election
        return elections


class VariationDiscoverer:
    """Discover response patterns (variations) via clustering"""
    
    def __init__(self):
        pass
    
    def discover_variations(self, elections: Dict[str, Election], max_variations: int = 5) -> List[Variation]:
        """Cluster elections into variations
        
        Groups comments with similar conflicts/values patterns
        """
        if not elections:
            return []
        
        # Group by conflict similarity
        conflict_groups: Dict[str, List[str]] = {}
        
        for comment_id, election in elections.items():
            # Simplify conflict to first few words (poor clustering)
            key = " ".join(election.conflict.split()[:2])
            if key not in conflict_groups:
                conflict_groups[key] = []
            conflict_groups[key].append(comment_id)
        
        # Convert groups to variations
        variations = []
        for idx, (pattern, comment_ids) in enumerate(sorted(
            conflict_groups.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:max_variations]):
            frequency = len(comment_ids)
            if frequency >= 1:  # Only include patterns with at least 1 comment
                variation = Variation(
                    id=f"var_{idx}",
                    name=pattern or "uncategorized",
                    elections=comment_ids,
                    frequency=frequency,
                    confidence=min(0.95, 0.5 + (frequency * 0.05))
                )
                variations.append(variation)
        
        return variations


class CoherenceCalculator:
    """Calculate 4-part coherence proof"""
    
    @staticmethod
    def calculate(
        posts_count: int,
        comments_count: int,
        elections_count: int,
        variations_count: int,
        variations_coverage: int  # Comments in variations
    ) -> CoherenceMetrics:
        """Calculate coherence metrics
        
        Φ = (1-φ)[δ₁ + δ₂ + δ₃ + δ₄]
        
        δ₁ = compression_ratio (elections → variations)
        δ₂ = coverage (comments in variations / total comments)
        δ₃ = accuracy (mock: based on variation uniformity)
        δ₄ = combined coherence
        """
        
        # Compression: elections → variations (higher is better)
        compression = elections_count / max(variations_count, 1) if variations_count > 0 else 1.0
        
        # Coverage: comments represented in variations (0-1)
        coverage = variations_coverage / max(comments_count, 1) if comments_count > 0 else 0.0
        
        # Accuracy: simple estimate based on variation distribution
        # If spread evenly, higher accuracy
        if variations_count > 0:
            avg_per_variation = comments_count / variations_count
            # Uniform distribution gives high accuracy
            accuracy = coverage * 0.8 + 0.2  # Range 0.2-1.0
        else:
            accuracy = 0.2
        
        # Combined coherence score (0-1)
        # Weight: compression 30%, coverage 40%, accuracy 30%
        coherence_score = (
            (compression / max(compression, 5)) * 0.3 +  # Normalized
            coverage * 0.4 +
            accuracy * 0.3
        )
        coherence_score = max(0.0, min(1.0, coherence_score))
        
        return CoherenceMetrics(
            compression_ratio=compression,
            coverage=coverage,
            accuracy=accuracy,
            coherence_score=coherence_score
        )


class AnalysisPipeline:
    """Complete analysis from comments to coherence"""
    
    def __init__(self):
        self.zap = ZAPAnalyzer()
        self.election_analyzer = ElectionAnalyzer()
        self.variation_discoverer = VariationDiscoverer()
        self.coherence_calculator = CoherenceCalculator()
    
    def analyze(self, comments: List[Comment]) -> Tuple[Dict[str, Election], List[Variation], CoherenceMetrics, ThreadSymbol]:
        """Run complete analysis pipeline"""
        
        # Step 1: Create elections
        elections = self.election_analyzer.analyze_comments(comments)
        
        # Step 2: Discover variations
        variations = self.variation_discoverer.discover_variations(elections)
        
        # Step 3: Calculate coverage
        variations_coverage = sum(len(v.elections) for v in variations)
        
        # Step 4: Calculate coherence
        metrics = self.coherence_calculator.calculate(
            posts_count=1,  # Approximate
            comments_count=len(comments),
            elections_count=len(elections),
            variations_count=len(variations),
            variations_coverage=variations_coverage
        )
        
        # Step 5: Create thread symbol
        symbol = ThreadSymbol(
            id=f"THREAD_{abs(hash(tuple(e for e in elections.keys()))) % 10000:04d}",
            domain="discussion",
            invariants=[],
            fields={
                "comment_count": len(comments),
                "variation_count": len(variations),
                "primary_conflict": elections[next(iter(elections))].conflict if elections else "unknown"
            },
            constraint=variations[0].name if variations else "no_consensus",
            confidence=metrics.coherence_score
        )
        
        return elections, variations, metrics, symbol
