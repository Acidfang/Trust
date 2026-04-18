"""
Weighted Comparison System for Image Generation Methods

Core principle: Apply same verification + weighted scoring system to compare
different AI image generation approaches (Stable Diffusion, DALL-E, etc)

The "HOW to compare" - define measurable dimensions, assign weights, calculate scores
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import json
from datetime import datetime

# ============================================================================
# DIMENSION DEFINITIONS - What we actually measure
# ============================================================================

@dataclass
class ComparisonDimension:
    """Single measurable aspect of image generation"""
    name: str
    description: str
    unit: str
    measurable: bool  # Can we objectively measure this?
    verifiable: bool  # Can we prove the measurement?
    
    def __post_init__(self):
        if not self.measurable:
            raise ValueError(f"Dimension '{self.name}' must be objectively measurable")
        if not self.verifiable:
            raise ValueError(f"Dimension '{self.name}' must be verifiable")


# Core dimensions used by state-of-the-art systems
STANDARD_DIMENSIONS = {
    "inference_speed": ComparisonDimension(
        name="inference_speed",
        description="Time to generate single 512x512 image",
        unit="seconds",
        measurable=True,
        verifiable=True
    ),
    
    "vram_required": ComparisonDimension(
        name="vram_required",
        description="GPU memory needed for generation",
        unit="GB",
        measurable=True,
        verifiable=True
    ),
    
    "prompt_adherence": ComparisonDimension(
        name="prompt_adherence",
        description="How well generated image matches text prompt",
        unit="score 0-100",  # Measured via CLIP similarity
        measurable=True,
        verifiable=True
    ),
    
    "output_quality": ComparisonDimension(
        name="output_quality",
        description="Visual fidelity of generated image",
        unit="score 0-100",  # Via FID (Frechet Inception Distance)
        measurable=True,
        verifiable=True
    ),
    
    "aesthetic_score": ComparisonDimension(
        name="aesthetic_score",
        description="Visual appeal and composition quality",
        unit="score 0-100",  # Via aesthetic model scoring
        measurable=True,
        verifiable=True
    ),
    
    "diversity": ComparisonDimension(
        name="diversity",
        description="Variation in outputs for same prompt",
        unit="score 0-100",  # Via embedding space analysis
        measurable=True,
        verifiable=True
    ),
    
    "consistency": ComparisonDimension(
        name="consistency",
        description="Reproducibility with same seed",
        unit="match percentage 0-100",
        measurable=True,
        verifiable=True
    ),
    
    "cost_per_image": ComparisonDimension(
        name="cost_per_image",
        description="Financial cost to generate one image",
        unit="USD",
        measurable=True,
        verifiable=True
    )
}


# ============================================================================
# WEIGHT SYSTEM - What matters most?
# ============================================================================

@dataclass
class WeightProfile:
    """Different weight profiles for different use cases"""
    name: str
    description: str
    weights: Dict[str, float]  # dimension_name -> weight (0-1)
    context: str  # When to use this profile
    
    def verify(self):
        """Ensure weights are valid"""
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.001:  # Allow small float error
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        
        for dim_name, weight in self.weights.items():
            if dim_name not in STANDARD_DIMENSIONS:
                raise ValueError(f"Unknown dimension: {dim_name}")
            if not 0 <= weight <= 1:
                raise ValueError(f"Weight must be 0-1, got {weight}")


# Predefined profiles matching real-world use cases
WEIGHT_PROFILES = {
    "high_quality_art": WeightProfile(
        name="high_quality_art",
        description="Prioritize visual quality and aesthetics",
        weights={
            "output_quality": 0.30,
            "aesthetic_score": 0.25,
            "prompt_adherence": 0.20,
            "consistency": 0.15,
            "inference_speed": 0.05,
            "vram_required": 0.03,
            "diversity": 0.01,
            "cost_per_image": 0.01
        },
        context="Professional art generation, high-res printing"
    ),
    
    "fast_iteration": WeightProfile(
        name="fast_iteration",
        description="Prioritize speed for rapid exploration",
        weights={
            "inference_speed": 0.40,
            "prompt_adherence": 0.25,
            "output_quality": 0.15,
            "vram_required": 0.10,
            "cost_per_image": 0.05,
            "consistency": 0.03,
            "aesthetic_score": 0.02,
            "diversity": 0.00
        },
        context="Brainstorming, concept exploration, user-facing UI"
    ),
    
    "cost_optimized": WeightProfile(
        name="cost_optimized",
        description="Minimize financial and resource costs",
        weights={
            "cost_per_image": 0.35,
            "vram_required": 0.25,
            "inference_speed": 0.20,
            "prompt_adherence": 0.10,
            "output_quality": 0.05,
            "consistency": 0.03,
            "aesthetic_score": 0.01,
            "diversity": 0.01
        },
        context="Large-scale generation, production systems"
    ),
    
    "balanced": WeightProfile(
        name="balanced",
        description="Balance all factors equally",
        weights={
            "output_quality": 0.15,
            "aesthetic_score": 0.12,
            "prompt_adherence": 0.15,
            "inference_speed": 0.15,
            "consistency": 0.12,
            "vram_required": 0.10,
            "cost_per_image": 0.10,
            "diversity": 0.11
        },
        context="General-purpose generation, unknown requirements"
    )
}

# Verify all profiles on load
for profile in WEIGHT_PROFILES.values():
    profile.verify()


# ============================================================================
# METHOD DEFINITION - Specific approach to generate images
# ============================================================================

@dataclass
class GenerationMethod:
    """Concrete implementation of image generation"""
    name: str
    model_name: str
    description: str
    
    # Measured parameters
    measurements: Dict[str, float]  # dimension_name -> measured_value
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""
    
    def validate(self):
        """Verify all measurements are present and valid"""
        for dim_name in STANDARD_DIMENSIONS.keys():
            if dim_name not in self.measurements:
                raise ValueError(f"Missing measurement: {dim_name}")
            
            value = self.measurements[dim_name]
            if not isinstance(value, (int, float)):
                raise ValueError(f"Measurement {dim_name} must be numeric")
            if value < 0:
                raise ValueError(f"Measurement {dim_name} cannot be negative")


# ============================================================================
# COMPARISON SCORE - The actual comparison math
# ============================================================================

@dataclass
class ComparisonScore:
    """Result of comparing a method against a weight profile"""
    method: GenerationMethod
    profile: WeightProfile
    
    # Component scores
    dimension_scores: Dict[str, float]  # normalized 0-1 for each dimension
    weighted_score: float  # final score 0-100
    
    # Ranking info
    rank: int = 0
    percentile: float = 0.0
    
    def __post_init__(self):
        if not 0 <= self.weighted_score <= 100:
            raise ValueError(f"Weighted score must be 0-100, got {self.weighted_score}")


def normalize_dimension_value(dimension_name: str, raw_value: float) -> float:
    """
    Convert raw measurement to 0-1 normalized score.
    
    This is where domain knowledge comes in:
    - For "more is better" dimensions: faster speed, higher quality
    - For "less is better" dimensions: lower cost, less VRAM
    - Reference points from actual systems
    
    Verification: scores must be reproducible and consistent
    """
    
    # Reference points from Stable Diffusion, DALL-E, Midjourney
    REFERENCE_RANGES = {
        "inference_speed": {
            "best": 2.0,      # seconds (fastest observed)
            "good": 5.0,      # reasonable
            "acceptable": 15.0,
            "poor": 60.0      # unacceptable slowness
        },
        
        "vram_required": {
            "best": 2.0,      # GB (most efficient)
            "good": 8.0,
            "acceptable": 16.0,
            "poor": 40.0
        },
        
        "prompt_adherence": {
            "best": 95.0,     # Perfect match (0-100 scale)
            "good": 85.0,
            "acceptable": 70.0,
            "poor": 50.0
        },
        
        "output_quality": {
            "best": 95.0,     # FID score (0-100 scale)
            "good": 80.0,
            "acceptable": 65.0,
            "poor": 40.0
        },
        
        "aesthetic_score": {
            "best": 95.0,
            "good": 80.0,
            "acceptable": 70.0,
            "poor": 50.0
        },
        
        "diversity": {
            "best": 95.0,
            "good": 80.0,
            "acceptable": 60.0,
            "poor": 30.0
        },
        
        "consistency": {
            "best": 99.0,
            "good": 95.0,
            "acceptable": 90.0,
            "poor": 70.0
        },
        
        "cost_per_image": {
            "best": 0.01,     # USD (cheapest)
            "good": 0.05,
            "acceptable": 0.20,
            "poor": 1.00
        }
    }
    
    if dimension_name not in REFERENCE_RANGES:
        raise ValueError(f"No normalization defined for {dimension_name}")
    
    refs = REFERENCE_RANGES[dimension_name]
    
    # Less-is-better dimensions (speed, cost, vram)
    if dimension_name in ["inference_speed", "vram_required", "cost_per_image"]:
        if raw_value <= refs["best"]:
            return 1.0
        elif raw_value <= refs["good"]:
            return 0.9
        elif raw_value <= refs["acceptable"]:
            return 0.7
        elif raw_value <= refs["poor"]:
            return 0.4
        else:
            return 0.0
    
    # More-is-better dimensions (quality, adherence, diversity, etc)
    else:
        if raw_value >= refs["best"]:
            return 1.0
        elif raw_value >= refs["good"]:
            return 0.9
        elif raw_value >= refs["acceptable"]:
            return 0.7
        elif raw_value >= refs["poor"]:
            return 0.4
        else:
            return 0.0


def calculate_comparison_score(
    method: GenerationMethod,
    profile: WeightProfile
) -> ComparisonScore:
    """
    Calculate how well a method performs given a weight profile.
    
    VERIFICATION:
    - Norm all dimensions to 0-1 scale
    - Apply weights
    - Calculate final score
    - Result must be 0-100
    - Reproducible with same inputs
    """
    
    method.validate()
    profile.verify()
    
    # Normalize each dimension
    dimension_scores = {}
    for dim_name in STANDARD_DIMENSIONS.keys():
        raw_value = method.measurements[dim_name]
        normalized = normalize_dimension_value(dim_name, raw_value)
        dimension_scores[dim_name] = normalized
    
    # Apply weights and calculate final score
    weighted_score = 0.0
    for dim_name, weight in profile.weights.items():
        weighted_score += dimension_scores[dim_name] * weight * 100
    
    return ComparisonScore(
        method=method,
        profile=profile,
        dimension_scores=dimension_scores,
        weighted_score=weighted_score
    )


def compare_methods(
    methods: List[GenerationMethod],
    profile: WeightProfile,
    sort_descending: bool = True
) -> List[ComparisonScore]:
    """
    Compare multiple methods against a single weight profile.
    
    Returns ranked list with percentile scores.
    """
    
    scores = [calculate_comparison_score(method, profile) for method in methods]
    
    # Sort and add ranking
    scores.sort(key=lambda s: s.weighted_score, reverse=sort_descending)
    
    total = len(scores)
    for idx, score in enumerate(scores):
        score.rank = idx + 1
        score.percentile = (total - idx) / total * 100
    
    return scores


# ============================================================================
# EXAMPLE IMPLEMENTATIONS - Real systems
# ============================================================================

# Stable Diffusion v1.5 on 10GB GPU
STABLE_DIFFUSION_1_5 = GenerationMethod(
    name="Stable Diffusion 1.5",
    model_name="CompVis/stable-diffusion-v1-5",
    description="Open-source latent diffusion, 860M parameters",
    measurements={
        "inference_speed": 8.5,           # seconds for 512x512, 50 steps
        "vram_required": 6.0,              # GB
        "prompt_adherence": 82.0,          # CLIP similarity
        "output_quality": 78.0,            # FID score
        "aesthetic_score": 75.0,
        "diversity": 85.0,
        "consistency": 98.5,
        "cost_per_image": 0.0              # Local, no API cost
    },
    notes="Baseline open-source model"
)

# Stable Diffusion v3 (newer, better)
STABLE_DIFFUSION_3 = GenerationMethod(
    name="Stable Diffusion 3",
    model_name="stabilityai/stable-diffusion-3",
    description="Newer architecture with rectified flow, transformer backbone",
    measurements={
        "inference_speed": 12.0,           # Slightly slower, better quality
        "vram_required": 8.0,              # Needs more memory
        "prompt_adherence": 90.0,          # Better prompt following
        "output_quality": 88.0,            # Significantly better
        "aesthetic_score": 87.0,           # Better composition
        "diversity": 82.0,                 # Slightly less diverse
        "consistency": 99.0,               # Very consistent
        "cost_per_image": 0.0
    },
    notes="State-of-the-art open model"
)

# DALL-E 3 (closed, expensive, proven high quality)
DALLE_3 = GenerationMethod(
    name="DALL-E 3",
    model_name="openai/dalle-3",
    description="Closed-source, text-conditional, proven high quality",
    measurements={
        "inference_speed": 20.0,           # Slower (remote API)
        "vram_required": 0.0,              # Cloud-hosted, user doesn't pay
        "prompt_adherence": 95.0,          # Excellent instruction following
        "output_quality": 92.0,            # Very high quality
        "aesthetic_score": 91.0,           # Excellent composition
        "diversity": 80.0,                 # Less diverse by design
        "consistency": 100.0,              # Perfect with same seed
        "cost_per_image": 0.080            # ~$0.080 per image
    },
    notes="Commercial API, premium quality"
)

# Fast local inference (fewer steps, lower quality)
STABLE_DIFFUSION_FAST = GenerationMethod(
    name="Stable Diffusion 1.5 (Fast)",
    model_name="CompVis/stable-diffusion-v1-5",
    description="Same model, 20 inference steps instead of 50",
    measurements={
        "inference_speed": 3.5,            # Much faster (20 steps)
        "vram_required": 6.0,
        "prompt_adherence": 75.0,          # Slightly degraded
        "output_quality": 65.0,            # Noticeably lower
        "aesthetic_score": 62.0,
        "diversity": 88.0,
        "consistency": 98.5,
        "cost_per_image": 0.0
    },
    notes="Speed optimization via fewer steps"
)


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    # Example methods
    methods = [
        STABLE_DIFFUSION_1_5,
        STABLE_DIFFUSION_3,
        DALLE_3,
        STABLE_DIFFUSION_FAST
    ]
    
    print("=" * 80)
    print("IMAGE GENERATION COMPARISON SYSTEM")
    print("=" * 80)
    print()
    
    # Test each profile
    for profile_name, profile in WEIGHT_PROFILES.items():
        print(f"\n{profile_name.upper()}")
        print(f"Context: {profile.context}")
        print("-" * 80)
        
        scores = compare_methods(methods, profile)
        
        for score in scores:
            print(f"\n{score.rank}. {score.method.name}")
            print(f"   Score: {score.weighted_score:.1f}/100 (Percentile: {score.percentile:.0f}%)")
            print(f"   Dimensions:")
            for dim_name, dim_score in score.dimension_scores.items():
                weight = profile.weights[dim_name]
                raw_value = score.method.measurements[dim_name]
                dim_unit = STANDARD_DIMENSIONS[dim_name].unit
                print(f"     - {dim_name}: {dim_score*100:.0f}% (weight: {weight*100:.0f}%, value: {raw_value} {dim_unit})")
        
        print()
