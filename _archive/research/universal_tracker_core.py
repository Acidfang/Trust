"""
UNIVERSAL TRACKER - CORE DATA MODEL
Core data structures for post/comment tracking and analysis

Classes:
- Post: Represents a social media post
- Comment: Represents a comment on a post
- Election: Represents ZAP analysis of a comment
- Variation: Groups comments by analysis pattern
- CoherenceMetrics: 4-part coherence proof
- ThreadSymbol: Compressed representation of thread
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
import json


@dataclass
class Post:
    """Represents a social media post"""
    id: str
    platform: str
    title: str
    content: str
    author: str
    timestamp: str
    url: str
    posts_count: int = 0
    comments_count: int = 0
    engagement: int = 0
    
    def to_json(self) -> dict:
        return asdict(self)
    
    def __repr__(self) -> str:
        return f"<Post {self.platform}:{self.id[:8]}>"


@dataclass
class Comment:
    """Represents a comment on a post"""
    id: str
    post_id: str
    platform: str
    content: str
    author: str
    timestamp: str
    sentiment: Optional[str] = None
    engagement: int = 0
    
    def to_json(self) -> dict:
        return asdict(self)
    
    def __repr__(self) -> str:
        return f"<Comment {self.platform}:{self.id[:8]}>"


@dataclass
class Election:
    """ZAP Election: Analysis of a comment
    
    ZAP Framework:
    - Z (conflict): What's the core conflict?
    - A (values): What values are in tension?
    - P (control): Who/what controls the narrative?
    - (uncertainty): What's uncertain?
    - (choices): What choices led here?
    - (insight): What insight emerges?
    """
    comment_id: str
    conflict: str  # Z: Core conflict identified
    values: List[str] = field(default_factory=list)  # A: Values in tension
    control: str = ""  # P: Control point
    uncertainty: str = ""  # What's uncertain
    choices: List[str] = field(default_factory=list)  # What choices led here
    insight: str = ""  # Emerging insight
    confidence: float = 0.0  # Confidence in election (0-1)
    
    def to_json(self) -> dict:
        return asdict(self)
    
    def __repr__(self) -> str:
        return f"<Election conflict={self.conflict[:20]}...>"


@dataclass
class Variation:
    """Groups elections by analysis pattern"""
    id: str
    name: str  # Pattern name (e.g., "pro-climate narrative")
    elections: List[str] = field(default_factory=list)  # Comment IDs
    frequency: int = 0  # How often this pattern appears
    confidence: float = 0.0  # Confidence score
    
    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "frequency": self.frequency,
            "confidence": self.confidence,
            "election_count": len(self.elections)
        }
    
    def __repr__(self) -> str:
        return f"<Variation {self.name} x{self.frequency}>"


@dataclass
class CoherenceMetrics:
    """4-part coherence proof: Φ = (1-φ)[δ₁ + δ₂ + δ₃ + δ₄]
    
    Components:
    - compression_ratio: How well does ThreadSymbol compress the thread?
    - coverage: What % of comments are captured in variations?
    - accuracy: How well do elections predict new comments?
    - coherence_score: Combined metric (0-1)
    """
    compression_ratio: float  # posts→symbol compression (higher = better)
    coverage: float  # % of comments in variations (0-1)
    accuracy: float  # Prediction accuracy (0-1)
    coherence_score: float  # Combined score (0-1)
    
    def to_json(self) -> dict:
        return asdict(self)
    
    def __repr__(self) -> str:
        return f"<Coherence Φ={self.coherence_score:.3f}>"


@dataclass
class ThreadSymbol:
    """Compressed representation of entire discussion thread
    
    Format: ⊙[THREAD_XXX] → β[domain] → κ⊕[invariants] → λ[fields] → Θ[constraint] → τ[score]
    
    Components:
    - id: Unique thread identifier
    - domain: Discussion domain (politics, science, etc.)
    - invariants: Core unchanging facts
    - fields: Dynamic aspects
    - constraint: Main limiting factor
    - confidence: Score (0-1)
    """
    id: str  # ⊙[THREAD_XXX]
    domain: str  # β[domain]
    invariants: List[str] = field(default_factory=list)  # κ⊕[invariants]
    fields: Dict[str, Any] = field(default_factory=dict)  # λ[fields]
    constraint: str = ""  # Θ[constraint]
    confidence: float = 0.0  # τ[score]
    
    def to_json(self) -> dict:
        return asdict(self)
    
    def __repr__(self) -> str:
        return f"⊙[{self.id}]"
    
    def to_singularity(self) -> str:
        """Convert to singularity format"""
        return (f"⊙[{self.id}]→β[{self.domain}]→"
                f"κ⊕{self.invariants}→λ{self.fields}→"
                f"Θ[{self.constraint}]→τ[{self.confidence:.3f}]")


# ============================================================================
# BATCH CONTAINER
# ============================================================================

@dataclass
class ScrapeResult:
    """Result of scraping a single platform"""
    platform: str
    status: str  # "success" or "error"
    posts: List[Post] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    
    def to_json(self) -> dict:
        return {
            "platform": self.platform,
            "status": self.status,
            "posts": [p.to_json() for p in self.posts],
            "comments": [c.to_json() for c in self.comments],
            "errors": self.errors,
            "duration_seconds": self.duration_seconds
        }
    
    def __repr__(self) -> str:
        return f"<{self.platform.upper()} posts={len(self.posts)} comments={len(self.comments)}>"


@dataclass
class AnalysisResult:
    """Result of analyzing scraped data"""
    platform: str
    posts: List[Post] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    elections: Dict[str, Election] = field(default_factory=dict)
    variations: List[Variation] = field(default_factory=list)
    symbol: Optional[ThreadSymbol] = None
    metrics: Optional[CoherenceMetrics] = None
    
    def to_json(self) -> dict:
        return {
            "platform": self.platform,
            "posts_analyzed": len(self.posts),
            "comments_analyzed": len(self.comments),
            "elections_count": len(self.elections),
            "variations": [v.to_json() for v in self.variations],
            "symbol": self.symbol.to_json() if self.symbol else None,
            "metrics": self.metrics.to_json() if self.metrics else None
        }
    
    def __repr__(self) -> str:
        return f"<Analysis {self.platform} elections={len(self.elections)} variations={len(self.variations)}>"
