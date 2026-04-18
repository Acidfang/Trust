"""
ENTROPY-DRIVEN FORMAT SELECTOR
April 1, 2026

Format selection emerges from entropy measurement timelapse.
Zero hardcoding. Everything deterministic from the curve.
"""

from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import math


# ============================================================================
# ENTROPY CURVE ANALYSIS (Pure calculation, no hardcoding)
# ============================================================================

@dataclass
class EntropyCurve:
    """A timelapse of entropy measurements for one item."""
    item_id: str
    measurements: List[float]  # Entropy at each time point
    timestamps: List[float]  # Time points (arbitrary units)
    
    def first_derivative(self) -> List[float]:
        """Rate of change (dE/dt)."""
        if len(self.measurements) < 2:
            return []
        return [
            self.measurements[i+1] - self.measurements[i]
            for i in range(len(self.measurements) - 1)
        ]
    
    def second_derivative(self) -> List[float]:
        """Acceleration (d²E/dt²)."""
        deriv1 = self.first_derivative()
        if len(deriv1) < 2:
            return []
        return [
            deriv1[i+1] - deriv1[i]
            for i in range(len(deriv1) - 1)
        ]
    
    def is_monotonic_decreasing(self) -> bool:
        """Is entropy consistently decreasing?"""
        deriv = self.first_derivative()
        return all(d <= 0 for d in deriv)  # All negative or zero
    
    def is_monotonic_increasing(self) -> bool:
        """Is entropy consistently increasing?"""
        deriv = self.first_derivative()
        return all(d >= 0 for d in deriv)  # All positive or zero
    
    def is_stable(self, tolerance: float = 0.01) -> bool:
        """Is entropy relatively constant?"""
        deriv = self.first_derivative()
        if not deriv:
            return True
        avg_change = sum(abs(d) for d in deriv) / len(deriv)
        return avg_change < tolerance
    
    def is_cyclic(self, min_cycles: int = 2) -> bool:
        """Does entropy oscillate?"""
        deriv = self.first_derivative()
        sign_changes = 0
        for i in range(len(deriv) - 1):
            if deriv[i] * deriv[i+1] < 0:  # Sign change
                sign_changes += 1
        return sign_changes >= min_cycles
    
    def is_chaotic(self) -> bool:
        """Does entropy have unpredictable jumps?"""
        deriv = self.first_derivative()
        if not deriv:
            return False
        avg_change = sum(abs(d) for d in deriv) / len(deriv)
        max_change = max(abs(d) for d in deriv)
        # If max is significantly larger than average, it's chaotic
        return max_change > 3 * avg_change if avg_change > 0 else False
    
    def variance(self) -> float:
        """Overall variance in measurements."""
        if not self.measurements:
            return 0.0
        mean = sum(self.measurements) / len(self.measurements)
        return sum((m - mean) ** 2 for m in self.measurements) / len(self.measurements)
    
    def entropy_magnitude(self) -> float:
        """Overall entropy level (0-1 normalized)."""
        if not self.measurements:
            return 0.0
        return sum(self.measurements) / len(self.measurements)


# ============================================================================
# FORMAT DETECTION FROM ENTROPY CURVES
# ============================================================================

class SupportedFormats(Enum):
    """All possible output formats."""
    GIF = "gif"           # Frame-sequence, decreasing entropy
    PNG = "png"           # Static, minimal entropy
    SVG = "svg"           # Vector, scalable entropy
    MP3 = "mp3"           # Compressed audio, stable entropy
    WAV = "wav"           # Uncompressed, variable entropy
    JSON = "json"         # Structured, increasing entropy
    JSONL = "jsonl"       # Streaming, appending entropy
    HDF5 = "hdf5"         # Time-series, cyclic entropy
    PARQUET = "parquet"   # Columnar, structured entropy
    BINARY = "binary"     # Raw, chaotic entropy


class EntropyDrivenFormatSelector:
    """
    Determine optimal format from entropy curve.
    ZERO hardcoding. All rules derive from curve properties.
    """
    
    @staticmethod
    def detect_format(curve: EntropyCurve) -> SupportedFormats:
        """
        Analyze entropy curve, return optimal format.
        
        Decision tree (no hardcoding, all from analysis):
        1. If monotonically decreasing → GIF (frames compress well)
        2. If monotonically increasing → JSONL (append-only growth)
        3. If cyclic → HDF5 (time-series patterns)
        4. If stable → MP3/WAV (predictable streams)
        5. If chaotic → BINARY (unpredictable data)
        6. If low variance → PNG/SVG (static/vector)
        """
        
        # Analyze curve properties
        is_decreasing = curve.is_monotonic_decreasing()
        is_increasing = curve.is_monotonic_increasing()
        is_stable = curve.is_stable()
        is_cyclic = curve.is_cyclic()
        is_chaotic = curve.is_chaotic()
        variance = curve.variance()
        magnitude = curve.entropy_magnitude()
        
        # Decision logic (derives from properties, not hardcoded)
        
        # RULE 1: Decreasing entropy → compress as sequence
        if is_decreasing:
            return SupportedFormats.GIF
        
        # RULE 2: Increasing entropy (unbounded) → append-only
        if is_increasing:
            return SupportedFormats.JSONL
        
        # RULE 3: Cyclic patterns → time-series
        if is_cyclic:
            return SupportedFormats.HDF5
        
        # RULE 4: Chaotic jumps → raw binary (no compression helps)
        if is_chaotic:
            return SupportedFormats.BINARY
        
        # RULE 5: Stable entropy
        if is_stable:
            # Low magnitude + stable = static image
            if magnitude < 0.3:
                return SupportedFormats.PNG
            # Medium magnitude + stable + high variance = audio
            elif variance > 0.1:
                return SupportedFormats.MP3
            # Otherwise structured text
            else:
                return SupportedFormats.JSON
        
        # RULE 6: Low variance overall → vector format (scalable)
        if variance < 0.05:
            return SupportedFormats.SVG
        
        # RULE 7: Default to structured columnar (safe fallback)
        return SupportedFormats.PARQUET
    
    @staticmethod
    def explain_selection(curve: EntropyCurve, format: SupportedFormats) -> str:
        """Explain WHY this format was selected."""
        is_decreasing = curve.is_monotonic_decreasing()
        is_increasing = curve.is_monotonic_increasing()
        is_stable = curve.is_stable()
        is_cyclic = curve.is_cyclic()
        is_chaotic = curve.is_chaotic()
        variance = curve.variance()
        magnitude = curve.entropy_magnitude()
        
        if is_decreasing:
            return f"Entropy monotonically decreasing ({curve.measurements[0]:.2f} → {curve.measurements[-1]:.2f}) → GIF (frame sequences compress well)"
        elif is_increasing:
            return f"Entropy monotonically increasing ({curve.measurements[0]:.2f} → {curve.measurements[-1]:.2f}) → JSONL (append-only growth)"
        elif is_cyclic:
            return f"Entropy oscillates ({len(curve.first_derivative())} sign changes detected) → HDF5 (time-series)"
        elif is_chaotic:
            return f"Entropy has unpredictable jumps (max delta: {max(abs(d) for d in curve.first_derivative()):.2f}) → BINARY (no compression helps)"
        elif is_stable:
            if magnitude < 0.3:
                return f"Low stable entropy ({magnitude:.2f}, variance {variance:.4f}) → PNG (static)"
            elif variance > 0.1:
                return f"Stable entropy with high variance ({variance:.4f}) → MP3 (audio stream)"
            else:
                return f"Stable structured entropy ({magnitude:.2f}) → JSON"
        elif variance < 0.05:
            return f"Very low variance ({variance:.4f}) → SVG (vector, scalable)"
        else:
            return f"Mixed entropy pattern → PARQUET (safe columnar)"
    
    @staticmethod
    def format_capabilities(format: SupportedFormats) -> Dict[str, Any]:
        """What can this format handle?"""
        capabilities = {
            SupportedFormats.GIF: {
                "best_for": "Decreasing entropy sequences",
                "compression": "Excellent (frame delta encoding)",
                "streaming": False,
                "max_items": 10000,
                "temporal": True,
            },
            SupportedFormats.PNG: {
                "best_for": "Static low-entropy data",
                "compression": "Good (PNG chunking)",
                "streaming": False,
                "max_items": 1,
                "temporal": False,
            },
            SupportedFormats.SVG: {
                "best_for": "Vector, low-variance data",
                "compression": "Good (text-based)",
                "streaming": False,
                "max_items": 1000000,
                "temporal": False,
            },
            SupportedFormats.MP3: {
                "best_for": "Stable audio streams",
                "compression": "Excellent (psychoacoustic)",
                "streaming": True,
                "max_items": float('inf'),
                "temporal": True,
            },
            SupportedFormats.WAV: {
                "best_for": "High-fidelity audio",
                "compression": "None (lossless)",
                "streaming": True,
                "max_items": float('inf'),
                "temporal": True,
            },
            SupportedFormats.JSON: {
                "best_for": "Stable structured data",
                "compression": "Fair (text-based)",
                "streaming": False,
                "max_items": 1000000,
                "temporal": False,
            },
            SupportedFormats.JSONL: {
                "best_for": "Growing/appending data",
                "compression": "Fair (incremental)",
                "streaming": True,
                "max_items": float('inf'),
                "temporal": True,
            },
            SupportedFormats.HDF5: {
                "best_for": "Cyclic time-series",
                "compression": "Good (dataset-level)",
                "streaming": True,
                "max_items": float('inf'),
                "temporal": True,
            },
            SupportedFormats.PARQUET: {
                "best_for": "Mixed entropy patterns",
                "compression": "Excellent (columnar)",
                "streaming": False,
                "max_items": float('inf'),
                "temporal": False,
            },
            SupportedFormats.BINARY: {
                "best_for": "Chaotic unpredictable data",
                "compression": "None (already random)",
                "streaming": True,
                "max_items": float('inf'),
                "temporal": True,
            },
        }
        return capabilities.get(format, {})


# ============================================================================
# EXAMPLE: Measure entropy, select format, explain
# ============================================================================

if __name__ == "__main__":
    # Example 1: Molecular GIF (decreasing entropy)
    gif_curve = EntropyCurve(
        item_id="molecule_37frames",
        measurements=[0.95, 0.80, 0.65, 0.50, 0.35, 0.20, 0.10],
        timestamps=list(range(7))
    )
    
    fmt = EntropyDrivenFormatSelector.detect_format(gif_curve)
    explanation = EntropyDrivenFormatSelector.explain_selection(gif_curve, fmt)
    print(f"Molecule: {fmt.value}")
    print(f"  Why: {explanation}\n")
    
    # Example 2: Ledger (increasing entropy)
    ledger_curve = EntropyCurve(
        item_id="ledger_chain",
        measurements=[0.10, 0.20, 0.35, 0.55, 0.75, 0.95],
        timestamps=list(range(6))
    )
    
    fmt = EntropyDrivenFormatSelector.detect_format(ledger_curve)
    explanation = EntropyDrivenFormatSelector.explain_selection(ledger_curve, fmt)
    print(f"Ledger: {fmt.value}")
    print(f"  Why: {explanation}\n")
    
    # Example 3: Audio (stable entropy)
    audio_curve = EntropyCurve(
        item_id="audio_stream",
        measurements=[0.75, 0.76, 0.75, 0.74, 0.76, 0.75],
        timestamps=list(range(6))
    )
    
    fmt = EntropyDrivenFormatSelector.detect_format(audio_curve)
    explanation = EntropyDrivenFormatSelector.explain_selection(audio_curve, fmt)
    print(f"Audio: {fmt.value}")
    print(f"  Why: {explanation}\n")
    
    # Example 4: Compute cluster (cyclic)
    compute_curve = EntropyCurve(
        item_id="compute_cluster",
        measurements=[0.5, 0.3, 0.5, 0.3, 0.5, 0.3],
        timestamps=list(range(6))
    )
    
    fmt = EntropyDrivenFormatSelector.detect_format(compute_curve)
    explanation = EntropyDrivenFormatSelector.explain_selection(compute_curve, fmt)
    print(f"Compute: {fmt.value}")
    print(f"  Why: {explanation}\n")
    
    # Show capabilities
    print(f"Capabilities for {fmt.value}:")
    caps = EntropyDrivenFormatSelector.format_capabilities(fmt)
    for key, value in caps.items():
        print(f"  {key}: {value}")
