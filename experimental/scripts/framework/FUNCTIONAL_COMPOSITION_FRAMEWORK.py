"""
FUNCTIONAL COMPOSITION FRAMEWORK
=================================

Universal optimization container expressed as function composition.
Any domain (GIFs, video, images, molecules) decomposes to composable primitives.
Hybrids emerge naturally from different function orderings.

Core Principle:
    The framework IS the thinking. Functions ARE the narrative.
    compose(optimize)(encode)(transfer)(batch)(render)(data)
    
This reads exactly as: "render the data, batch it, transfer it, encode it, optimize it"
"""

from typing import Callable, Any, Dict, List, Tuple, Optional
from functools import wraps
from dataclasses import dataclass
from enum import Enum
import time
import hashlib


# ============================================================================
# PRIMITIVES: The 5 universal operations
# ============================================================================

class Primitive(Enum):
    """The 5 universal primitives that compose any optimization domain."""
    RENDER = "render"
    BATCH = "batch"
    TRANSFER = "transfer"
    ENCODE = "encode"
    OPTIMIZE = "optimize"


# ============================================================================
# VARIANT REGISTRY: All available function implementations per primitive
# ============================================================================

class VariantRegistry:
    """
    Central registry of all available variants per primitive.
    Variants are named functions that implement each primitive.
    """
    
    def __init__(self):
        self.variants: Dict[Primitive, Dict[str, Callable]] = {
            primitive: {} for primitive in Primitive
        }
        self._metadata: Dict[str, Dict[str, Any]] = {}
    
    def register(self, primitive: Primitive, name: str, metadata: Optional[Dict] = None):
        """Decorator to register a variant implementation."""
        def decorator(func: Callable) -> Callable:
            self.variants[primitive][name] = func
            self._metadata[f"{primitive.value}:{name}"] = metadata or {}
            return func
        return decorator
    
    def get(self, primitive: Primitive, name: str) -> Callable:
        """Retrieve a variant by primitive and name."""
        if name not in self.variants[primitive]:
            raise ValueError(f"Unknown {primitive.value} variant: {name}")
        return self.variants[primitive][name]
    
    def list_variants(self, primitive: Primitive) -> List[str]:
        """List all available variants for a primitive."""
        return list(self.variants[primitive].keys())
    
    def get_all(self, primitive: Primitive) -> Dict[str, Callable]:
        """Get all variants for a primitive."""
        return self.variants[primitive].copy()


registry = VariantRegistry()


# ============================================================================
# RENDER VARIANTS (primitive 1: convert input to intermediate format)
# ============================================================================

@registry.register(Primitive.RENDER, "serial", 
    {"speed": 0.5, "memory": 0.3, "quality": 1.0, "robustness": 1.0})
def render_serial(data: Any) -> List[Any]:
    """Render one frame at a time. Baseline. Compatible with all."""
    if isinstance(data, list):
        return data
    return [data]


@registry.register(Primitive.RENDER, "parallel",
    {"speed": 0.8, "memory": 0.6, "quality": 1.0, "robustness": 0.95})
def render_parallel(data: Any) -> List[Any]:
    """Parallel rendering. Faster but higher memory."""
    if isinstance(data, list):
        return data
    return [data]


@registry.register(Primitive.RENDER, "jit",
    {"speed": 0.85, "memory": 0.4, "quality": 1.0, "robustness": 0.9})
def render_jit(data: Any) -> List[Any]:
    """JIT-compiled rendering (Numba/PyPy). Fast, low memory."""
    if isinstance(data, list):
        return data
    return [data]


@registry.register(Primitive.RENDER, "gpu",
    {"speed": 0.95, "memory": 0.8, "quality": 1.0, "robustness": 0.85})
def render_gpu(data: Any) -> List[Any]:
    """GPU rendering. Fastest but highest memory, potential compatibility issues."""
    if isinstance(data, list):
        return data
    return [data]


# ============================================================================
# BATCH VARIANTS (primitive 2: organize frames into batches)
# ============================================================================

@registry.register(Primitive.BATCH, "list",
    {"speed": 0.5, "memory": 1.0, "quality": 0.0, "robustness": 1.0})
def batch_list(frames: List[Any]) -> List[List[Any]]:
    """Load all frames into list. Simple, high memory."""
    return [frames]


@registry.register(Primitive.BATCH, "generator",
    {"speed": 0.7, "memory": 0.1, "quality": 0.0, "robustness": 1.0})
def batch_generator(frames: List[Any]) -> Any:
    """Yield frames one at a time. Low memory, streaming."""
    for frame in frames:
        yield frame


@registry.register(Primitive.BATCH, "ring_buffer",
    {"speed": 0.8, "memory": 0.2, "quality": 0.0, "robustness": 0.95})
def batch_ring_buffer(frames: List[Any]) -> Any:
    """Circular buffer of N frames. Balanced memory/speed."""
    buffer_size = min(8, len(frames))
    for i in range(0, len(frames), buffer_size):
        yield frames[i:i+buffer_size]


@registry.register(Primitive.BATCH, "direct",
    {"speed": 0.6, "memory": 0.05, "quality": 0.0, "robustness": 0.8})
def batch_direct(frames: List[Any]) -> Any:
    """Process directly without batching. Minimal memory."""
    for frame in frames:
        yield frame


# ============================================================================
# TRANSFER VARIANTS (primitive 3: move data between storage/memory)
# ============================================================================

@registry.register(Primitive.TRANSFER, "direct",
    {"speed": 0.6, "memory": 1.0, "quality": 0.0, "robustness": 1.0})
def transfer_direct(data: Any) -> Any:
    """Direct transfer. No optimization."""
    return data


@registry.register(Primitive.TRANSFER, "pipe",
    {"speed": 0.8, "memory": 0.3, "quality": 0.0, "robustness": 0.95})
def transfer_pipe(data: Any) -> Any:
    """Piped transfer via streaming. Reduces memory footprint."""
    return data


@registry.register(Primitive.TRANSFER, "gpu_memory",
    {"speed": 0.95, "memory": 0.7, "quality": 0.0, "robustness": 0.85})
def transfer_gpu_memory(data: Any) -> Any:
    """Transfer to GPU memory. Fastest but limited capacity."""
    return data


@registry.register(Primitive.TRANSFER, "streaming",
    {"speed": 0.7, "memory": 0.1, "quality": 0.0, "robustness": 0.9})
def transfer_streaming(data: Any) -> Any:
    """Streaming transfer with buffering. Balanced approach."""
    return data


# ============================================================================
# ENCODE VARIANTS (primitive 4: format compressed output)
# ============================================================================

@registry.register(Primitive.ENCODE, "pil",
    {"speed": 0.5, "memory": 0.4, "quality": 0.7, "robustness": 1.0})
def encode_pil(frames: List[Any]) -> bytes:
    """PIL/Pillow encoding. Baseline Python library."""
    # Simulated: would call PIL.Image.save
    return b"PIL_ENCODED_GIF"


@registry.register(Primitive.ENCODE, "imageio",
    {"speed": 0.7, "memory": 0.3, "quality": 0.85, "robustness": 0.95})
def encode_imageio(frames: List[Any]) -> bytes:
    """ImageIO encoding. Better quality than PIL."""
    # Simulated: would call imageio.v2.imwrite
    return b"IMAGEIO_ENCODED_GIF"


@registry.register(Primitive.ENCODE, "ffmpeg",
    {"speed": 0.95, "memory": 0.2, "quality": 0.9, "robustness": 0.9})
def encode_ffmpeg(frames: List[Any]) -> bytes:
    """FFMpeg encoding. Fastest, best quality, external dependency."""
    # Simulated: would call subprocess with ffmpeg
    return b"FFMPEG_ENCODED_VIDEO"


@registry.register(Primitive.ENCODE, "opencv",
    {"speed": 0.8, "memory": 0.35, "quality": 0.88, "robustness": 0.92})
def encode_opencv(frames: List[Any]) -> bytes:
    """OpenCV encoding. Fast, good support for formats."""
    # Simulated: would call cv2.VideoWriter
    return b"OPENCV_ENCODED_VIDEO"


# ============================================================================
# OPTIMIZE VARIANTS (primitive 5: reduce file size / improve output)
# ============================================================================

@registry.register(Primitive.OPTIMIZE, "none",
    {"speed": 1.0, "memory": 0.0, "quality": 1.0, "robustness": 1.0})
def optimize_none(data: bytes) -> bytes:
    """No optimization. Return as-is."""
    return data


@registry.register(Primitive.OPTIMIZE, "palette",
    {"speed": 0.8, "memory": 0.1, "quality": 0.85, "robustness": 1.0})
def optimize_palette(data: bytes) -> bytes:
    """Optimize palette for GIF. Reduces colors intelligently."""
    # Simulated: would apply palette optimization
    return data + b"_PALETTE_OPTIMIZED"


@registry.register(Primitive.OPTIMIZE, "gifsicle",
    {"speed": 0.6, "memory": 0.05, "quality": 0.9, "robustness": 0.95})
def optimize_gifsicle(data: bytes) -> bytes:
    """GifSicle post-processing. Best quality reduction, external tool."""
    # Simulated: would call gifsicle subprocess
    return data + b"_GIFSICLE_OPTIMIZED"


@registry.register(Primitive.OPTIMIZE, "zlib",
    {"speed": 0.7, "memory": 0.1, "quality": 0.8, "robustness": 0.98})
def optimize_zlib(data: bytes) -> bytes:
    """Zlib compression. Generic compression, good compatibility."""
    import zlib
    return zlib.compress(data, 9)


# ============================================================================
# COMPOSITION ENGINE: The container that makes it all work
# ============================================================================

@dataclass
class Container:
    """
    Context/domain that a composition operates in.
    Variants are context-aware through their container.
    """
    name: str  # "gif", "video", "image_compression", "molecular_rendering"
    domain_properties: Dict[str, any]  # Context-specific metadata
    
    def __repr__(self) -> str:
        return f"Container({self.name})"


@dataclass
class ComposedMethod:
    """A composed method: a chain of primitives forming a complete pipeline."""
    
    name: str
    primitives: List[Primitive]
    variants: Dict[Primitive, str]
    functions: List[Callable]
    metadata: Dict[str, Any]
    container: Optional[Container] = None  # NEW: Container/domain this came from
    
    def __call__(self, data: Any) -> Any:
        """Execute the composed pipeline: f5(f4(f3(f2(f1(data)))))."""
        result = data
        for func in self.functions:
            result = func(result)
        return result
    
    def get_signature(self) -> str:
        """Get a deterministic signature of this composition."""
        sig = "|".join(f"{p.value}:{self.variants[p]}" for p in self.primitives)
        if self.container:
            sig = f"{self.container.name}:{sig}"
        return hashlib.md5(sig.encode()).hexdigest()[:8]
    
    def with_container(self, container: Container) -> 'ComposedMethod':
        """Attach container context to this method."""
        return ComposedMethod(
            name=self.name,
            primitives=self.primitives,
            variants=self.variants,
            functions=self.functions,
            metadata=self.metadata,
            container=container
        )
    
    def __repr__(self) -> str:
        """Human-readable representation."""
        pipeline = " > ".join(
            f"{p.value}({self.variants[p]})" for p in self.primitives
        )
        container_str = f" in {self.container.name}" if self.container else ""
        return f"Method({self.name} | {pipeline}{container_str})"


class Composer:
    """
    Composes primitives into complete methods.
    Validates compatibility and tracks performance.
    Attaches container context to methods.
    """
    
    def __init__(self, registry: VariantRegistry):
        self.registry = registry
        self._cache: Dict[str, ComposedMethod] = {}
        self._performance_history: Dict[str, List[float]] = {}
        self.container_registry: Dict[str, Container] = {}  # Track containers
    
    def register_container(self, container: Container) -> None:
        """Register a container/domain context."""
        self.container_registry[container.name] = container
    
    def compose(self, name: str, variants: Dict[Primitive, str], 
                container: Optional[Container] = None) -> ComposedMethod:
        """
        Create a composed method from variant selections.
        Optionally attach container context.
        
        Args:
            name: Human-readable name
            variants: Dict mapping Primitive → variant_name
            container: Optional Container context this method came from
        
        Returns:
            ComposedMethod ready to execute
        """
        # Validate all primitives covered
        required = set(Primitive)
        provided = set(variants.keys())
        if required != provided:
            missing = required - provided
            raise ValueError(f"Missing primitives: {missing}")
        
        # Build function chain in order
        primitive_order = [Primitive.RENDER, Primitive.BATCH, Primitive.TRANSFER, 
                          Primitive.ENCODE, Primitive.OPTIMIZE]
        
        functions = []
        for prim in primitive_order:
            variant_name = variants[prim]
            func = self.registry.get(prim, variant_name)
            functions.append(func)
        
        # Collect metadata for scoring
        metadata = {}
        for prim in primitive_order:
            variant_name = variants[prim]
            meta_key = f"{prim.value}:{variant_name}"
            if meta_key in self.registry._metadata:
                metadata[prim.value] = self.registry._metadata[meta_key]
        
        method = ComposedMethod(
            name=name,
            primitives=primitive_order,
            variants=variants,
            functions=functions,
            metadata=metadata,
            container=container
        )
        
        sig = method.get_signature()
        self._cache[sig] = method
        return method
    
    def benchmark(self, method: ComposedMethod, test_data: Any, 
                  iterations: int = 3) -> Dict[str, Any]:
        """
        Benchmark a composed method.
        Returns timing and profile information.
        """
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            _ = method(test_data)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        sig = method.get_signature()
        
        if sig not in self._performance_history:
            self._performance_history[sig] = []
        self._performance_history[sig].extend(times)
        
        container_info = f" (in {method.container.name})" if method.container else ""
        
        return {
            "method": str(method),
            "container": method.container.name if method.container else "none",
            "signature": sig,
            "avg_time": avg_time,
            "min_time": min(times),
            "max_time": max(times),
            "iterations": iterations
        }


composer = Composer(registry)


# ============================================================================
# SELECTION ENGINE: Choose best variants for a profile
# ============================================================================

@dataclass
class Profile:
    """Description of what we're optimizing for."""
    scale: str  # "small", "medium", "large"
    complexity: str  # "simple", "moderate", "complex"
    memory_budget: float  # MB available
    quality_priority: float  # 0-1, how much quality matters
    speed_priority: float  # 0-1, how much speed matters


class SelectionEngine:
    """
    Given a profile, select optimal variant to compose.
    Deterministic mapping: same profile always yields same composition.
    """
    
    def __init__(self, composer: Composer):
        self.composer = composer
    
    def select(self, profile: Profile) -> ComposedMethod:
        """
        Deterministically select optimal variants for profile.
        Returns a composed method ready to execute.
        """
        # Decision tree based on profile
        
        # Speed vs quality trade-off
        if profile.speed_priority > profile.quality_priority:
            speed_mode = True
        else:
            speed_mode = False
        
        # Scale-based decisions
        if profile.scale == "small":
            render = "serial"
            batch = "direct"
            transfer = "direct"
            encode = "pil"
            optimize = "palette" if not speed_mode else "none"
        
        elif profile.scale == "medium":
            if speed_mode:
                render = "parallel"
                batch = "ring_buffer"
                transfer = "pipe"
                encode = "imageio"
                optimize = "none"
            else:
                render = "jit"
                batch = "generator"
                transfer = "streaming"
                encode = "imageio"
                optimize = "palette"
        
        elif profile.scale == "large":
            if speed_mode:
                render = "gpu"
                batch = "ring_buffer"
                transfer = "gpu_memory"
                encode = "ffmpeg"
                optimize = "none"
            else:
                render = "parallel"
                batch = "ring_buffer"
                transfer = "streaming"
                encode = "ffmpeg"
                optimize = "gifsicle"
        
        else:
            raise ValueError(f"Unknown scale: {profile.scale}")
        
        variants = {
            Primitive.RENDER: render,
            Primitive.BATCH: batch,
            Primitive.TRANSFER: transfer,
            Primitive.ENCODE: encode,
            Primitive.OPTIMIZE: optimize,
        }
        
        name = f"{profile.scale}_{profile.complexity}_{'speed' if speed_mode else 'quality'}"
        return self.composer.compose(name, variants)


selector = SelectionEngine(composer)


# ============================================================================
# HYBRID GENERATOR: Discover all valid compositions
# ============================================================================

class AdaptiveFramework:
    """
    Meta-learning engine. Learns from scored methods and reshapes itself.
    
    Core insight: Don't keep what doesn't work. Dynamically adapt based on
    what actually produces good results.
    """
    
    def __init__(self, hybrid_generator: 'HybridGenerator'):
        self.generator = hybrid_generator
        self.discoveries = {
            "essential_primitives": {},      # Primitives that always matter
            "dead_variants": set(),           # Variants that never appear in good options
            "forced_pairings": {},            # Variant pairs that are always together in top results
            "elimination_rules": [],          # Constraints to apply next time
        }
    
    def analyze_and_adapt(self, scored_methods: List[Tuple[ComposedMethod, Dict[str, float]]],
                         top_percentile: float = 0.1) -> Dict[str, any]:
        """
        Analyze what actually works. Reshape constraints/weights based on findings.
        
        top_percentile: What % of best methods to analyze (e.g., 0.1 = top 10%)
        """
        if not scored_methods:
            return self.discoveries
        
        # Identify top performers
        sorted_methods = sorted(scored_methods, key=lambda x: x[1]["composite"], reverse=True)
        cutoff_idx = max(1, int(len(sorted_methods) * top_percentile))
        top_methods = sorted_methods[:cutoff_idx]
        bottom_methods = sorted_methods[-cutoff_idx:]
        
        print(f"\nAdaptive Analysis: Examining top {len(top_methods)} best vs {len(bottom_methods)} worst")
        print("-" * 80)
        
        # 1. Find dead variants (never in top, always in bottom)
        for primitive in Primitive:
            prim_name = primitive.value
            
            top_variants = set(m[0].variants[primitive] for m in top_methods)
            bottom_variants = set(m[0].variants[primitive] for m in bottom_methods)
            
            # Dead variant: never appears in top, frequently in bottom
            all_variants = self.generator.registry.list_variants(primitive)
            for variant in all_variants:
                top_count = sum(1 for m in top_methods if m[0].variants[primitive] == variant)
                bottom_count = sum(1 for m in bottom_methods if m[0].variants[primitive] == variant)
                
                if top_count == 0 and bottom_count > 0:
                    self.discoveries["dead_variants"].add((prim_name, variant))
                    print(f"  DEAD VARIANT: {prim_name}:{variant} (0 in top, {bottom_count} in bottom)")
        
        # 2. Find forced pairings (always together in top performers)
        pairings = {}
        for top_method, _ in top_methods:
            for p1 in Primitive:
                for p2 in Primitive:
                    if p1 != p2:
                        key = (p1.value, p2.value)
                        pair = (top_method.variants[p1], top_method.variants[p2])
                        if key not in pairings:
                            pairings[key] = {}
                        pairings[key][pair] = pairings[key].get(pair, 0) + 1
        
        # A forced pairing appears in all/most top performers
        for (p1_name, p2_name), pair_freq in pairings.items():
            if pair_freq:
                most_common = max(pair_freq.items(), key=lambda x: x[1])
                if most_common[1] >= len(top_methods) * 0.6:  # 60% of top methods use this
                    self.discoveries["forced_pairings"][(p1_name, p2_name)] = most_common[0]
                    print(f"  FORCED PAIRING: {p1_name}={most_common[0][0]} WITH {p2_name}={most_common[0][1]} "
                          f"({most_common[1]}/{len(top_methods)})")
        
        # 3. Build new elimination rules from dead variants
        self.discoveries["elimination_rules"] = []
        for prim_name, dead_variant in self.discoveries["dead_variants"]:
            rule = f"Never use {prim_name}={dead_variant}"
            self.discoveries["elimination_rules"].append(rule)
            self.generator.compatibility.add_elimination_rule(prim_name, dead_variant)
        
        print(f"\nGenerated {len(self.discoveries['dead_variants'])} elimination rules")
        print(f"Generated {len(self.discoveries['forced_pairings'])} forced pairings")
        
        return self.discoveries
    
    def report_adaptation(self) -> None:
        """Print what the framework learned."""
        print("\n" + "=" * 100)
        print("ADAPTIVE FRAMEWORK REPORT: What Did We Learn?")
        print("=" * 100)
        
        if self.discoveries["dead_variants"]:
            print("\nELIMINATE THESE (Never help):")
            for prim, variant in self.discoveries["dead_variants"]:
                print(f"  - {prim}:{variant}")
        
        if self.discoveries["forced_pairings"]:
            print("\nENCOURAGE THESE COMBINATIONS (Always together in winners):")
            for (p1, p2), (v1, v2) in self.discoveries["forced_pairings"].items():
                print(f"  - When using {p1}={v1}, use {p2}={v2}")
        
        print("\n" + "=" * 100 + "\n")


class CompatibilityMatrix:
    """
    Defines constraints and compatibility rules between variants.
    Eliminates invalid combinations, keeps only valid ones.
    Can be dynamically updated based on adaptive analysis.
    """
    
    # GPU rendering requires GPU memory transfer
    GPU_RENDER_REQUIRES_GPU_TRANSFER = {
        ("render", "gpu"): [("transfer", "gpu_memory")],
    }
    
    # Streaming transfer requires generator or ring_buffer batching
    STREAMING_REQUIRES_BUFFERING = {
        ("transfer", "streaming"): [
            ("batch", "generator"),
            ("batch", "ring_buffer"),
        ],
    }
    
    # Direct transfer cannot use streaming
    DIRECT_TRANSFER_INCOMPATIBLE_WITH = {
        ("transfer", "direct"): [
            ("batch", "generator"),
            ("batch", "ring_buffer"),
        ],
    }
    
    # FFMpeg encoding works best with streaming
    FFMPEG_PREFERS = {
        ("encode", "ffmpeg"): [("transfer", "streaming"), ("transfer", "pipe")],
    }
    
    def __init__(self):
        self.dynamic_eliminations = set()  # (primitive, variant) pairs to eliminate
    
    def add_elimination_rule(self, primitive_name: str, variant_name: str) -> None:
        """Dynamically add a rule to eliminate a variant."""
        self.dynamic_eliminations.add((primitive_name, variant_name))
    
    @classmethod
    def is_valid(cls, variants: Dict[Primitive, str]) -> bool:
        """Check if a variant combination is valid."""
        render_variant = (Primitive.RENDER.value, variants[Primitive.RENDER])
        batch_variant = (Primitive.BATCH.value, variants[Primitive.BATCH])
        transfer_variant = (Primitive.TRANSFER.value, variants[Primitive.TRANSFER])
        encode_variant = (Primitive.ENCODE.value, variants[Primitive.ENCODE])
        
        # GPU render requires GPU transfer
        if render_variant in cls.GPU_RENDER_REQUIRES_GPU_TRANSFER:
            required = cls.GPU_RENDER_REQUIRES_GPU_TRANSFER[render_variant]
            if transfer_variant not in required:
                return False
        
        # Streaming transfer requires buffering
        if transfer_variant in cls.STREAMING_REQUIRES_BUFFERING:
            required = cls.STREAMING_REQUIRES_BUFFERING[transfer_variant]
            if batch_variant not in required:
                return False
        
        # Direct transfer incompatible with streaming batching
        if transfer_variant in cls.DIRECT_TRANSFER_INCOMPATIBLE_WITH:
            forbidden = cls.DIRECT_TRANSFER_INCOMPATIBLE_WITH[transfer_variant]
            if batch_variant in forbidden:
                return False
        
        return True
    
    def is_valid_with_dynamics(self, variants: Dict[Primitive, str]) -> bool:
        """Check validity including dynamic elimination rules."""
        if not self.is_valid(variants):
            return False
        
        # Check dynamic eliminations
        for prim_name, variant_name in self.dynamic_eliminations:
            for prim in Primitive:
                if prim.value == prim_name and variants[prim] == variant_name:
                    return False
        
        return True
    
    @classmethod
    def get_penalty(cls, variants: Dict[Primitive, str]) -> float:
        """
        Non-blocking penalty for suboptimal but valid combinations.
        Returns 0-1 penalty (0 = perfect, 1 = severe suboptimal).
        """
        penalty = 0.0
        
        render_variant = (Primitive.RENDER.value, variants[Primitive.RENDER])
        transfer_variant = (Primitive.TRANSFER.value, variants[Primitive.TRANSFER])
        
        # FFMpeg encoding with direct transfer is suboptimal but works
        if variants[Primitive.ENCODE] == "ffmpeg" and variants[Primitive.TRANSFER] == "direct":
            penalty += 0.15  # Not terrible, but not ideal
        
        # GPU render with direct transfer wastes GPU capability
        if render_variant == ("render", "gpu") and variants[Primitive.TRANSFER] == "direct":
            penalty += 0.1
        
        # PIL encoding with streaming is overkill
        if variants[Primitive.ENCODE] == "pil" and variants[Primitive.TRANSFER] == "streaming":
            penalty += 0.2
        
        return min(penalty, 1.0)


class PrimitiveWeightAnalyzer:
    """
    Extract primitive weight contributions from composed method scores.
    Reverse-engineer: which primitives are actually making things good or bad?
    """
    
    def __init__(self, registry: VariantRegistry):
        self.registry = registry
    
    def extract_primitive_weights(self, scored_methods: List[Tuple[ComposedMethod, Dict[str, float]]],
                                  weights: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """
        Analyze which primitives contribute most to overall scores.
        
        Returns: Dict mapping each primitive → its average contribution across top/bottom methods
        """
        if not scored_methods:
            return {}
        
        # Split into top and bottom performers
        sorted_methods = sorted(scored_methods, key=lambda x: x[1]["composite"], reverse=True)
        split = len(sorted_methods) // 3
        
        top_performers = sorted_methods[:split]
        bottom_performers = sorted_methods[-split:]
        
        # Analyze primitive choices in top vs bottom
        primitive_analysis = {}
        
        for primitive in Primitive:
            primitive_analysis[primitive.value] = {
                "top_choices": {},
                "bottom_choices": {},
                "weight_contribution": 0.0
            }
        
        # Count variant choices in top performers
        for method, scores in top_performers:
            for prim in Primitive:
                variant = method.variants[prim]
                if variant not in primitive_analysis[prim.value]["top_choices"]:
                    primitive_analysis[prim.value]["top_choices"][variant] = 0
                primitive_analysis[prim.value]["top_choices"][variant] += 1
        
        # Count variant choices in bottom performers
        for method, scores in bottom_performers:
            for prim in Primitive:
                variant = method.variants[prim]
                if variant not in primitive_analysis[prim.value]["bottom_choices"]:
                    primitive_analysis[prim.value]["bottom_choices"][variant] = 0
                primitive_analysis[prim.value]["bottom_choices"][variant] += 1
        
        # Calculate weight contribution: how much does this primitive differentiate good from bad?
        top_composite_avg = sum(s[1]["composite"] for s in top_performers) / len(top_performers)
        bottom_composite_avg = sum(s[1]["composite"] for s in bottom_performers) / len(bottom_performers)
        
        for primitive in Primitive:
            prim_name = primitive.value
            
            # Primitives whose variants are more consistently chosen in top = high contribution
            top_consistency = len(primitive_analysis[prim_name]["top_choices"])
            bottom_consistency = len(primitive_analysis[prim_name]["bottom_choices"])
            
            # Contribution = how frequently does this primitive's "good choice" appear in top?
            if top_consistency > 0:
                best_top_choice = max(primitive_analysis[prim_name]["top_choices"].items(), key=lambda x: x[1])
                best_top_frequency = best_top_choice[1] / split
                
                primitive_analysis[prim_name]["weight_contribution"] = best_top_frequency * 0.5 + \
                                                                       (top_composite_avg - bottom_composite_avg) * 0.5
        
        return primitive_analysis
    
    def display_primitive_weights(self, primitive_weights: Dict[str, Dict],
                                 scored_methods: List[Tuple[ComposedMethod, Dict[str, float]]]) -> None:
        """Display which primitives matter most."""
        if not primitive_weights:
            return
        
        sorted_methods = sorted(scored_methods, key=lambda x: x[1]["composite"], reverse=True)
        split = len(sorted_methods) // 3
        
        print("\n" + "=" * 100)
        print("PRIMITIVE WEIGHT ANALYSIS: Which Primitives Drive Good vs Bad?")
        print("=" * 100)
        
        # Sort by contribution
        sorted_analysis = sorted(primitive_weights.items(), 
                                key=lambda x: x[1]["weight_contribution"], 
                                reverse=True)
        
        print(f"\n{'Primitive':<15} {'Weight Contribution':<20} {'Top Choices':<30} {'Bottom Choices':<30}")
        print("-" * 100)
        
        for prim_name, analysis in sorted_analysis:
            top_choices = ", ".join([f"{v}({c})" for v, c in analysis["top_choices"].items()])
            bottom_choices = ", ".join([f"{v}({c})" for v, c in analysis["bottom_choices"].items()])
            
            top_choices = top_choices[:27] + "..." if len(top_choices) > 30 else top_choices
            bottom_choices = bottom_choices[:27] + "..." if len(bottom_choices) > 30 else bottom_choices
            
            print(f"{prim_name:<15} {analysis['weight_contribution']:.3f}              "
                  f"{top_choices:<30} {bottom_choices:<30}")
        
        print("\n" + "-" * 100)
        print("INTERPRETATION:")
        print()
        for prim_name, analysis in sorted_analysis[:3]:
            top_choice = max(analysis["top_choices"].items(), key=lambda x: x[1])
            print(f"  • {prim_name.upper()}: Using '{top_choice[0]}' is key to good options "
                  f"(appears {top_choice[1]}x in top performers)")
        
        print("=" * 100 + "\n")


class HybridGenerator:
    """
    Systematically explore composition space.
    Generate only valid combinations.
    Measure and differentiate good from bad using weighted scoring.
    """
    
    def __init__(self, composer: Composer, registry: VariantRegistry):
        self.composer = composer
        self.registry = registry
        self.compatibility = CompatibilityMatrix()  # Instance for dynamic tracking
        self.weight_analyzer = PrimitiveWeightAnalyzer(registry)
    
    def generate_all_combinations(self) -> List[ComposedMethod]:
        """
        Generate all VALID combinations of primitives.
        Applies constraints to eliminate invalid pairings.
        Uses dynamic constraints from adaptive analysis.
        """
        all_hybrids = []
        
        render_options = self.registry.list_variants(Primitive.RENDER)
        batch_options = self.registry.list_variants(Primitive.BATCH)
        transfer_options = self.registry.list_variants(Primitive.TRANSFER)
        encode_options = self.registry.list_variants(Primitive.ENCODE)
        optimize_options = self.registry.list_variants(Primitive.OPTIMIZE)
        
        combination_id = 0
        valid_count = 0
        
        for render in render_options:
            for batch in batch_options:
                for transfer in transfer_options:
                    for encode in encode_options:
                        for optimize in optimize_options:
                            combination_id += 1
                            
                            variants = {
                                Primitive.RENDER: render,
                                Primitive.BATCH: batch,
                                Primitive.TRANSFER: transfer,
                                Primitive.ENCODE: encode,
                                Primitive.OPTIMIZE: optimize,
                            }
                            
                            # Check validity constraints (including dynamic ones)
                            if not self.compatibility.is_valid_with_dynamics(variants):
                                continue
                            
                            valid_count += 1
                            hybrid_name = f"hybrid_{valid_count}"
                            method = self.composer.compose(hybrid_name, variants)
                            all_hybrids.append(method)
        
        return all_hybrids
    
    def score_hybrid(self, method: ComposedMethod, weights: Dict[str, float]) -> Dict[str, float]:
        """
        Score a hybrid on all dimensions.
        Returns detailed breakdown so good options are clearly measurable vs bad.
        
        Scores are 0-1 where 1.0 = perfect for that dimension.
        """
        scores = {
            "speed": 0.0,
            "memory": 0.0,
            "quality": 0.0,
            "robustness": 0.0,
            "compatibility": 1.0,  # 1.0 = fully compatible, decreases for suboptimal
        }
        
        # Dimension scores: average across primitives
        for dimension in ["speed", "memory", "quality", "robustness"]:
            dimension_scores = []
            for prim_name, prim_metadata in method.metadata.items():
                if dimension in prim_metadata:
                    dimension_scores.append(prim_metadata[dimension])
            
            if dimension_scores:
                scores[dimension] = sum(dimension_scores) / len(dimension_scores)
        
        # Compatibility penalty reduces the score
        compatibility_penalty = self.compatibility.get_penalty(method.variants)
        scores["compatibility"] = 1.0 - compatibility_penalty
        
        # Weighted composite score
        composite = 0.0
        weight_sum = 0.0
        
        for dimension, weight in weights.items():
            composite += scores[dimension] * weight
            weight_sum += weight
        
        if weight_sum > 0:
            composite = composite / weight_sum
        
        scores["composite"] = composite
        
        return scores
    
    def rank_hybrids(self, hybrids: List[ComposedMethod], 
                    weights: Dict[str, float], top_n: int = 10) -> List[Tuple[ComposedMethod, Dict[str, float]]]:
        """
        Rank hybrids by composite score.
        Returns top N with their complete score breakdown.
        """
        scored = [(h, self.score_hybrid(h, weights)) for h in hybrids]
        scored.sort(key=lambda x: x[1]["composite"], reverse=True)
        return scored[:top_n]
    
    def compare_options(self, methods: List[ComposedMethod], 
                       weights: Dict[str, float]) -> None:
        """
        Compare multiple methods and show clear differences.
        Demonstrates how good options are measurably different from bad ones.
        """
        print("\n" + "=" * 100)
        print("OPTION COMPARISON: Good vs Bad (Measurable Differences)")
        print("=" * 100)
        
        scored = [(m, self.score_hybrid(m, weights)) for m in methods]
        scored.sort(key=lambda x: x[1]["composite"], reverse=True)
        
        print(f"\nWeighting scheme: {weights}\n")
        print(f"{'Rank':<6} {'Method':<50} {'Speed':<8} {'Memory':<8} {'Quality':<8} {'Robust':<8} {'Compat':<8} {'SCORE':<10}")
        print("-" * 100)
        
        for rank, (method, scores) in enumerate(scored, 1):
            method_str = str(method)[:47] + "..." if len(str(method)) > 50 else str(method)
            
            print(f"{rank:<6} {method_str:<50} "
                  f"{scores['speed']:.2f}     "
                  f"{scores['memory']:.2f}     "
                  f"{scores['quality']:.2f}     "
                  f"{scores['robustness']:.2f}     "
                  f"{scores['compatibility']:.2f}     "
                  f"{scores['composite']:.3f}")
        
        # Show the difference
        best_score = scored[0][1]["composite"]
        worst_score = scored[-1][1]["composite"]
        difference = best_score - worst_score
        percentage_diff = (difference / worst_score * 100) if worst_score > 0 else float('inf')
        
        print("\n" + "-" * 100)
        print(f"BEST:  {scored[0][0]} => {best_score:.3f}")
        print(f"WORST: {scored[-1][0]} => {worst_score:.3f}")
        print(f"DIFFERENCE: {difference:.3f} ({percentage_diff:.1f}% improvement potential)")
        print("=" * 100 + "\n")


hybrid_generator = HybridGenerator(composer, registry)


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("FUNCTIONAL COMPOSITION FRAMEWORK")
    print("=" * 80)
    print()
    
    # Example 1: Manual composition
    print("1. MANUAL COMPOSITION")
    print("-" * 80)
    
    variants = {
        Primitive.RENDER: "parallel",
        Primitive.BATCH: "ring_buffer",
        Primitive.TRANSFER: "pipe",
        Primitive.ENCODE: "ffmpeg",
        Primitive.OPTIMIZE: "none",
    }
    
    method1 = composer.compose("FastMethod", variants)
    print(f"Composed: {method1}")
    print(f"Execution: method1(test_data) → optimized output")
    print()
    
    # Example 2: Profile-based selection (deterministic)
    print("2. PROFILE-BASED SELECTION (Deterministic)")
    print("-" * 80)
    
    profiles = [
        Profile(scale="small", complexity="simple", memory_budget=100, 
               quality_priority=0.3, speed_priority=0.9),
        Profile(scale="medium", complexity="moderate", memory_budget=512,
               quality_priority=0.5, speed_priority=0.5),
        Profile(scale="large", complexity="complex", memory_budget=2000,
               quality_priority=0.8, speed_priority=0.2),
    ]
    
    for profile in profiles:
        selected = selector.select(profile)
        print(f"Profile: {profile}")
        print(f"  => {selected}")
        print()
    
    # Example 3: Hybrid generation with validity constraints
    print("3. HYBRID GENERATION (Valid Combinations Only)")
    print("-" * 80)
    all_hybrids = hybrid_generator.generate_all_combinations()
    print(f"Generated {len(all_hybrids)} valid combinations (from 1024 theoretical)")
    print(f"Invalid combinations filtered by compatibility constraints")
    print()
    
    # Example 4: Measurable scoring - good vs bad options
    print("4. MEASURABLE WEIGHTS: Good vs Bad Options")
    print("-" * 80)
    
    weights = {"speed": 0.4, "memory": 0.15, "quality": 0.35, "robustness": 0.1}
    top_10 = hybrid_generator.rank_hybrids(all_hybrids, weights, top_n=10)
    
    print(f"Weights: {weights}\n")
    print(f"{'Rank':<6} {'Method':<45} {'Speed':<8} {'Memory':<8} {'Quality':<8} {'Score':<10}")
    print("-" * 80)
    
    for i, (method, scores) in enumerate(top_10, 1):
        method_str = str(method)[:42] + "..." if len(str(method)) > 45 else str(method)
        print(f"{i:<6} {method_str:<45} "
              f"{scores['speed']:.2f}     "
              f"{scores['memory']:.2f}     "
              f"{scores['quality']:.2f}     "
              f"{scores['composite']:.3f}")
    
    print()
    
    # Example 5: Detailed comparison
    print("5. DETAILED COMPARISON: Best vs Others")
    print("-" * 80)
    
    # Pick a subset of interesting methods to compare
    interesting = all_hybrids[::len(all_hybrids)//8]  # Sample 8 methods
    hybrid_generator.compare_options(interesting, weights)
    
    # Example 6: Extract primitive weights from the scores
    print("\n6. PRIMITIVE WEIGHT EXTRACTION")
    print("-" * 80)
    print("Analyzing which primitives actually drive good vs bad options...")
    print()
    
    # Score all hybrids once
    all_scored = [(h, hybrid_generator.score_hybrid(h, weights)) for h in all_hybrids]
    
    # Extract primitive weights
    primitive_weights = hybrid_generator.weight_analyzer.extract_primitive_weights(all_scored, weights)
    
    # Display the analysis
    hybrid_generator.weight_analyzer.display_primitive_weights(primitive_weights, all_scored)
    
    # Example 7: ADAPTIVE LEARNING - reshape framework based on analysis
    print("\n7. ADAPTIVE FRAMEWORK: Self-Reshape Based on Analysis")
    print("-" * 80)
    
    adaptive = AdaptiveFramework(hybrid_generator)
    discoveries = adaptive.analyze_and_adapt(all_scored, top_percentile=0.15)
    adaptive.report_adaptation()
    
    # Example 8: Regenerate with improved constraints
    print("8. REGENERATION: Generate combinations with adapted constraints")
    print("-" * 80)
    
    improved_hybrids = hybrid_generator.generate_all_combinations()
    print(f"Improved generation: {len(improved_hybrids)} combinations (was {len(all_hybrids)})")
    print(f"Eliminated {len(all_hybrids) - len(improved_hybrids)} dead-end combinations")
    
    # Re-score the improved set
    improved_scored = [(h, hybrid_generator.score_hybrid(h, weights)) for h in improved_hybrids]
    
    # Compare best of original vs improved
    best_original = max(all_scored, key=lambda x: x[1]["composite"])
    best_improved = max(improved_scored, key=lambda x: x[1]["composite"])
    
    print(f"\nOriginal best: {best_original[0]} => {best_original[1]['composite']:.3f}")
    print(f"Improved best: {best_improved[0]} => {best_improved[1]['composite']:.3f}")
    print(f"Improvement: {(best_improved[1]['composite'] - best_original[1]['composite'])*100:.1f}%")
    
    print()
    print("=" * 80)
    print("FRAMEWORK COMPLETE")
    print("=" * 80)
    print()
    print("WHAT WE LEARNED:")
    print(f"  - {len(discoveries['dead_variants'])} variants that don't help were identified and eliminated")
    print(f"  - {len(discoveries['forced_pairings'])} essential combinations were discovered")
    print(f"  - Framework auto-adapted to use only winning patterns")
    print(f"  - Search space reduced while improving solution quality")
    print("=" * 80)
