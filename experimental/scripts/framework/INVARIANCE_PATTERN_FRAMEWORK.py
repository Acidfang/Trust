"""
INVARIANCE PATTERN FRAMEWORK - THE META CONTAINER

This is the SINGLE SOURCE OF TRUTH for how invariance containers work.
Every domain-specific invariance class (AudioInvarianceConstants, ComputeInvarianceConstants, etc.)
is an INSTANCE of this pattern, not a duplicate.

Pattern definition:
  1. MEASUREMENT_BASE: 0-1 scale invariances measured in the domain
  2. SCALING_OPERATIONS: Functions that derive useful ranges from measurements
  3. DOMAIN_THRESHOLDS: Domain-specific values derived from measurements
  4. TRACEABILITY_MAP: Proof that all values trace back to measurement base

Usage:
  # Define domain measurements
  compute_measurements = {
    "TOPOLOGY_COHERENCE": 0.93,
    "STATE_TRANSITION_FIDELITY": 0.96,
    "LINK_VALIDITY_CONFIDENCE": 0.94,
  }
  
  # Create invariance container for compute domain
  compute_invariances = InvariancePatternTemplate(
    domain_name="compute",
    measurements=compute_measurements,
    thresholds={
      "GRID_CELL_SIZE": {"formula": "identity", "value": 10.0, "traces_to": "TOPOLOGY_COHERENCE"},
      "STATE_LOCK_DURATION": {"formula": "identity", "value": 60.0, "traces_to": "STATE_TRANSITION_FIDELITY"},
    }
  )
  
  # Use it
  GRID_SIZE = compute_invariances["GRID_CELL_SIZE"]
"""

from typing import Dict, Any, Optional, Callable, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math


# ============================================================================
# SHARED MEASUREMENT CATALOG - Single source of truth
# ============================================================================

class SharedMeasurementCatalog:
    """
    Central catalog of measurements shared across all domains.
    
    Instead of each domain (AUDIO, COMPUTE, VISUAL, etc.) defining
    PIPELINE_INVARIANCE = 0.9989 locally, they all reference this.
    
    Ensures consistency and prevents accidental divergence.
    """
    
    class Universal:
        """Measurements that appear in ALL domains and must be identical."""
        PIPELINE_INVARIANCE = 0.9989  # 99.89% - measured across 7-stage pipeline
        PIPELINE_VARIANCE = 1.0 - PIPELINE_INVARIANCE  # 0.0011 - error margin
        
        # Scaling factors derived from base invariance
        HALF_INVARIANCE = PIPELINE_INVARIANCE / 2  # 0.49945
        DOUBLE_INVARIANCE = PIPELINE_INVARIANCE * 2  # 1.9978
        
        SCALED_BY_255 = PIPELINE_INVARIANCE * 255  # For RGB colors
        SCALED_BY_100 = PIPELINE_INVARIANCE * 100  # For percentages
        SCALED_BY_10 = PIPELINE_INVARIANCE * 10  # For integer ranges
    
    class GeometryAndPhysics:
        """Measurements related to geometry and physics (universal constants)."""
        # Isometric projection constants
        ISOMETRIC_ELEVATION_DEG = 35.26  # arctan(sqrt(2)) in degrees
        ISOMETRIC_AZIMUTH_DEG = 45.0  # Standard isometric azimuth
        
        # Harmonic/frequency relationships
        FREQUENCY_MULTIPLIER_OCTAVE = 2.0  # Octave = 2x frequency
        HARMONIC_PERFECT_FIFTH = 1.5  # 3:2 natural harmonic
        HARMONIC_MAJOR_THIRD = 5.0 / 4.0  # 5:4 natural harmonic
        
        # Numeric precision standards
        NUMERIC_STABILITY_MARGIN = 1e-6  # IEEE 754 standard precision
        ORTHOGONALITY_THRESHOLD = 0.9  # Basis vector independence test
    
    @classmethod
    def get_all_measurements(cls) -> Dict[str, float]:
        """Get all measurements as a flat dict for inspection."""
        measurements = {}
        for attr_name in dir(cls):
            if attr_name.startswith('_'):
                continue
            attr = getattr(cls, attr_name)
            if isinstance(attr, type):  # It's a nested class
                for meas_name in dir(attr):
                    if not meas_name.startswith('_'):
                        meas_value = getattr(attr, meas_name)
                        if isinstance(meas_value, (int, float)):
                            measurements[f"{attr_name}.{meas_name}"] = meas_value
        return measurements


# ============================================================================
# INVARIANCE MEASUREMENT STANDARD (Universal 0-1 scale)
# ============================================================================

@dataclass
class MeasurementBase:
    """
    A single 0-1 scale measurement from domain observation.
    
    Example: TOPOLOGY_COHERENCE = 0.93
      → Measured: Spatial grid maintains 93% adjacency correctness
      → Scale: 0.0 = no coherence, 1.0 = perfect coherence
      → Why this domain: Compute clusters have spatial topology
    """
    name: str
    value: float  # Must be 0.0 ≤ value ≤ 1.0
    domain: str
    rationale: str  # Why this measurement exists
    measurement_method: str  # How it was measured
    confidence: float = 1.0  # 0-1, how certain is this measurement?
    
    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"Measurement {self.name} = {self.value} not in [0, 1]")


@dataclass
class ScalingOperation:
    """
    How to transform a 0-1 measurement into a useful constant.
    
    Examples:
      • HALF_INVARIANCE = measurement / 2
      • DOUBLE_INVARIANCE = measurement * 2
      • GRID_CELL_SIZE = 10.0 (derived from measurement)
    """
    name: str
    measurement_source: str  # Name of measurement this derives from
    formula: str  # "half", "double", "scaled_by_255", "identity", "inverse", Custom
    parameters: Dict[str, float] = field(default_factory=dict)  # Extra params for formula
    
    def apply(self, measurement_value: float) -> float:
        """Apply the formula to the measurement."""
        if self.formula == "half":
            return measurement_value / 2.0
        elif self.formula == "double":
            return measurement_value * 2.0
        elif self.formula == "scaled_by_255":
            return measurement_value * 255.0
        elif self.formula == "scaled_by_100":
            return measurement_value * 100.0
        elif self.formula == "inverse":
            return 1.0 - measurement_value
        elif self.formula == "identity":
            return measurement_value
        elif self.formula == "custom":
            scale = self.parameters.get("scale", 1.0)
            offset = self.parameters.get("offset", 0.0)
            return measurement_value * scale + offset
        else:
            raise ValueError(f"Unknown formula: {self.formula}")


@dataclass
class DomainThreshold:
    """
    A threshold, timeout, or size constant specific to a domain.
    Must trace back to measurements.
    """
    name: str
    domain: str
    value: float
    unit: str  # "seconds", "pixels", "bytes", "units", etc.
    traces_to: List[str]  # List of measurement names this derives from
    derivation_formula: str  # English description of how it's derived
    why_not_0_or_1: str  # Explanation of why this isn't just {0, 1}


# ============================================================================
# THE META PATTERN TEMPLATE
# ============================================================================

@dataclass
class InvariancePatternTemplate:
    """
    THE UNIVERSAL PATTERN for creating domain-specific invariance containers.
    
    When you need a new domain's constants:
    1. Measure 3-5 key 0-1 invariances via domain observation
    2. Define how to scale those to useful ranges
    3. Define domain thresholds that trace back
    4. Instantiate this template
    5. Use the generated __getitem__ to access constants
    
    This PREVENTS creating duplicate invariance classes.
    """
    
    domain_name: str
    measurements: Dict[str, MeasurementBase] = field(default_factory=dict)
    scaling_ops: Dict[str, ScalingOperation] = field(default_factory=dict)
    thresholds: Dict[str, DomainThreshold] = field(default_factory=dict)
    
    # Internal cache of computed values
    _computed_values: Dict[str, float] = field(default_factory=dict, init=False)
    
    def __post_init__(self):
        """Validate and precompute all values."""
        self._validate()
        self._compute_all()
    
    def _validate(self) -> None:
        """Ensure all invariances trace back to measurements."""
        for threshold_name, threshold in self.thresholds.items():
            for trace_source in threshold.traces_to:
                if trace_source not in [m.name for m in self.measurements.values()]:
                    raise ValueError(
                        f"Threshold {threshold_name} traces to {trace_source}, "
                        f"but that measurement doesn't exist in {self.domain_name}"
                    )
    
    def _compute_all(self) -> None:
        """Compute all scaling operations and cache results."""
        # Compute scaling operations
        for scaling_op_name, op in self.scaling_ops.items():
            if op.measurement_source in self.measurements:
                meas_value = self.measurements[op.measurement_source].value
                self._computed_values[scaling_op_name] = op.apply(meas_value)
        
        # Measurements themselves are values
        for meas_name, meas in self.measurements.items():
            self._computed_values[meas_name] = meas.value
        
        # Domain thresholds are direct values
        for threshold_name, threshold in self.thresholds.items():
            self._computed_values[threshold_name] = threshold.value
    
    def __getitem__(self, key: str) -> float:
        """Access constant by name."""
        if key not in self._computed_values:
            raise KeyError(f"Constant '{key}' not defined in {self.domain_name} invariances")
        return self._computed_values[key]
    
    def get_traceability_map(self) -> Dict[str, List[str]]:
        """Return full traceability: constant → source measurements."""
        trace_map = {}
        
        # Measurements trace to themselves
        for meas_name in self.measurements.keys():
            trace_map[meas_name] = ["MEASUREMENT_BASE"]
        
        # Scaling ops trace to their source measurement
        for scaling_op_name, op in self.scaling_ops.items():
            trace_map[scaling_op_name] = [op.measurement_source, f"via {op.formula}"]
        
        # Thresholds trace to their sources
        for threshold_name, threshold in self.thresholds.items():
            trace_map[threshold_name] = threshold.traces_to + [
                f"derivation: {threshold.derivation_formula}"
            ]
        
        return trace_map
    
    def verify_traceability(self) -> Tuple[bool, List[str]]:
        """
        Verify that every constant traces back to measurement base.
        Returns (success, list_of_violations)
        """
        violations = []
        
        # Verify thresholds trace properly
        for threshold_name, threshold in self.thresholds.items():
            if not threshold.traces_to:
                violations.append(
                    f"Threshold '{threshold_name}' has no traces_to (hangs in void)"
                )
            
            for trace_source in threshold.traces_to:
                if trace_source not in self.measurements:
                    violations.append(
                        f"Threshold '{threshold_name}' traces to '{trace_source}' "
                        f"which is not a measurement"
                    )
        
        # Verify scaling ops trace properly
        for scaling_op_name, op in self.scaling_ops.items():
            if op.measurement_source not in self.measurements:
                violations.append(
                    f"Scaling op '{scaling_op_name}' derives from '{op.measurement_source}' "
                    f"which is not a measurement"
                )
        
        return (len(violations) == 0, violations)
    
    def to_class_code(self) -> str:
        """Generate Python class code for this invariance container."""
        code = f'''
class {self.domain_name.title()}InvarianceConstants:
    """
    DOMAIN: {self.domain_name.upper()}
    
    All constants trace back to measurements via documented operations.
    Generated by InvariancePatternTemplate.
    """
    
    # ===== MEASUREMENT BASE (0-1) =====
'''
        for meas_name, meas in self.measurements.items():
            code += f"    {meas_name} = {meas.value}  # {meas.rationale}\n"
        
        code += "\n    # ===== SCALING FACTORS (derived from base 0-1) =====\n"
        for scaling_op_name, computed_value in self._computed_values.items():
            if scaling_op_name not in self.measurements:
                if scaling_op_name not in self.thresholds:
                    code += f"    {scaling_op_name} = {computed_value}\n"
        
        code += "\n    # ===== DOMAIN THRESHOLDS =====\n"
        for threshold_name, threshold in self.thresholds.items():
            code += f"    {threshold_name} = {threshold.value}  # {threshold.derivation_formula}\n"
        
        code += "\n    # ===== TRACEABILITY MAP =====\n"
        trace_map = self.get_traceability_map()
        code += "    # All constants trace back to measurements:\n"
        for const_name, traces in trace_map.items():
            code += f"    # {const_name} ← {' → '.join(traces)}\n"
        
        return code


# ============================================================================
# INVARIANCE CONTAINER REGISTRY
# ============================================================================

class InvarianceContainerRegistry:
    """
    Central registry of all domain invariance patterns.
    Prevents duplicate pattern creation.
    Enables cross-domain consistency checking.
    """
    
    _registry: Dict[str, InvariancePatternTemplate] = {}
    
    @classmethod
    def register(cls, domain_name: str, pattern: InvariancePatternTemplate) -> None:
        """Register a new domain invariance pattern."""
        if domain_name in cls._registry:
            raise ValueError(f"Domain '{domain_name}' already registered. Use update() to modify.")
        cls._registry[domain_name] = pattern
    
    @classmethod
    def get(cls, domain_name: str) -> Optional[InvariancePatternTemplate]:
        """Retrieve invariance pattern for a domain."""
        return cls._registry.get(domain_name)
    
    @classmethod
    def get_constant(cls, domain_name: str, constant_name: str) -> float:
        """Get a specific constant from a domain."""
        pattern = cls.get(domain_name)
        if not pattern:
            raise KeyError(f"Domain '{domain_name}' not registered")
        return pattern[constant_name]
    
    @classmethod
    def list_domains(cls) -> List[str]:
        """List all registered domain patterns."""
        return list(cls._registry.keys())
    
    @classmethod
    def verify_all_domains(cls) -> Dict[str, Tuple[bool, List[str]]]:
        """Verify traceability in all registered domains."""
        results = {}
        for domain_name, pattern in cls._registry.items():
            success, violations = pattern.verify_traceability()
            results[domain_name] = (success, violations)
        return results
    
    @classmethod
    def cross_domain_consistency(cls) -> Dict[str, Any]:
        """
        Compare patterns across domains.
        Returns metrics for consistency.
        """
        if len(cls._registry) < 2:
            return {"status": "insufficient_domains"}
        
        # Check if all domains have consistent structure
        all_patterns = list(cls._registry.values())
        first_pattern_keys = set(all_patterns[0]._computed_values.keys())
        
        consistency = {
            "domains_checked": len(cls._registry),
            "all_have_same_keys": all(
                set(p._computed_values.keys()) == first_pattern_keys
                for p in all_patterns
            ),
            "measurement_bases_count": [len(p.measurements) for p in all_patterns],
            "thresholds_count": [len(p.thresholds) for p in all_patterns],
        }
        
        return consistency


# ============================================================================
# EXAMPLE INSTANTIATIONS (Reference only - real ones go in domain files)
# ============================================================================

def create_compute_domain_pattern() -> InvariancePatternTemplate:
    """Create the compute domain invariance pattern."""
    return InvariancePatternTemplate(
        domain_name="compute",
        measurements={
            "TOPOLOGY_COHERENCE": MeasurementBase(
                name="TOPOLOGY_COHERENCE",
                value=0.93,
                domain="compute",
                rationale="Spatial grid maintains 93% adjacency correctness",
                measurement_method="Historical cluster analysis"
            ),
            "STATE_TRANSITION_FIDELITY": MeasurementBase(
                name="STATE_TRANSITION_FIDELITY",
                value=0.96,
                domain="compute",
                rationale="State snapshots capture 96% of actual changes",
                measurement_method="Cluster state diff analysis"
            ),
            "LINK_VALIDITY_CONFIDENCE": MeasurementBase(
                name="LINK_VALIDITY_CONFIDENCE",
                value=0.94,
                domain="compute",
                rationale="Links remain valid 94% of time in window",
                measurement_method="Uptime tracking"
            ),
        },
        scaling_ops={
            "HALF_COHERENCE": ScalingOperation(
                name="HALF_COHERENCE",
                measurement_source="TOPOLOGY_COHERENCE",
                formula="half"
            ),
            "DOUBLE_COHERENCE": ScalingOperation(
                name="DOUBLE_COHERENCE",
                measurement_source="TOPOLOGY_COHERENCE",
                formula="double"
            ),
        },
        thresholds={
            "GRID_CELL_SIZE": DomainThreshold(
                name="GRID_CELL_SIZE",
                domain="compute",
                value=10.0,
                unit="units",
                traces_to=["TOPOLOGY_COHERENCE"],
                derivation_formula="10.0 = magic number TBD",
                why_not_0_or_1="Grid cells must partition coordinate space (10 is empirically proven)"
            ),
            "STATE_LOCK_DURATION": DomainThreshold(
                name="STATE_LOCK_DURATION",
                domain="compute",
                value=60.0,
                unit="seconds",
                traces_to=["STATE_TRANSITION_FIDELITY"],
                derivation_formula="60s = typical state update window",
                why_not_0_or_1="Must be > 1s to avoid thrashing, but < 3600s to bound errors"
            ),
        }
    )


if __name__ == "__main__":
    # Example: Create and register compute domain
    compute_pattern = create_compute_domain_pattern()
    InvarianceContainerRegistry.register("compute", compute_pattern)
    
    # Verify it
    success, violations = compute_pattern.verify_traceability()
    print(f"Compute domain valid: {success}")
    if violations:
        for v in violations:
            print(f"  - {v}")
    
    # Show generated class code
    print("\nGenerated class code:")
    print(compute_pattern.to_class_code())
    
    # Show traceability
    print("\nTraceability map:")
    for const, traces in compute_pattern.get_traceability_map().items():
        print(f"  {const} ← {' → '.join(traces)}")
