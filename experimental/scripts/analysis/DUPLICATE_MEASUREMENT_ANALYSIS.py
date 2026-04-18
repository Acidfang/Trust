"""
DUPLICATE MEASUREMENT DETECTION REPORT
April 1, 2026

This document analyzes all *InvarianceConstants classes across the codebase
and identifies which measurements are duplicated (should be shared) vs unique.

METHODOLOGY:
1. Extract all measurements from each domain's constants class
2. Compare across domains
3. Classify as: UNIVERSAL, NEARLY_UNIVERSAL, DOMAIN_SPECIFIC, DUPLICATE
"""

from typing import Dict, List, Set, Tuple
import os
import re


# ============================================================================
# MEASUREMENTS FOUND IN EACH DOMAIN
# ============================================================================

DOMAINS_AND_MEASUREMENTS = {
    "UNIVERSAL_RENDERER (molecular visual)": {
        "PIPELINE_INVARIANCE": 0.9989,
        "PIPELINE_VARIANCE": 0.0011,
        "HALF_INVARIANCE": "derived",
        "DOUBLE_INVARIANCE": "derived",
        "DOUBLE_INVARIANCE_2": 2.0,
        "SCALED_BY_255": "derived",
        "SCALED_BY_100": "derived",
        "ISOMETRIC_ELEVATION_DEG": 35.26,
        "ISOMETRIC_AZIMUTH_DEG": 45.0,
        "FREQUENCY_BASE": "derived=2.0",
        "FREQUENCY_DENSITY_SCALE": "derived=0.5",
        "TILT_AMPLITUDE": 15,
        "ROTATION_DURATION": 4.0,
        "NUM_FRAMES": 37,
    },
    
    "AUDIO_RENDERER": {
        "PIPELINE_INVARIANCE": 0.9989,
        "PIPELINE_VARIANCE": 0.0011,
        "HALF_INVARIANCE": "derived",  
        "DOUBLE_INVARIANCE": "derived",
        "SAMPLE_RATE_CD_QUALITY": "derived=44100",
        "SAMPLE_RATE_TELEPHONY": "derived=8000",
        "SAMPLE_RATE_HIGH_FIDELITY": "derived=96000",
        "FREQUENCY_A4_BASE": 440.0,
        "FREQUENCY_MULTIPLIER_OCTAVE": 2.0,
        "HARMONIC_2_OCTAVE": "DOUBLE_INVARIANCE",
        "HARMONIC_3_PERFECT_FIFTH": 1.5,
        "AMPLITUDE_FULL": 1.0,
        "AMPLITUDE_HALF": "HALF_INVARIANCE",
    },
    
    "CONTAINER_RENDERER": {
        "PIPELINE_INVARIANCE": 0.9989,
        "PIPELINE_VARIANCE": 0.0011,
        "HALF_INVARIANCE": "derived",
        "DOUBLE_INVARIANCE": "derived",
        "QUALITY_PASS_THRESHOLD": 1.0,
        "QUALITY_FAIL_THRESHOLD": "HALF_INVARIANCE",
        "QUALITY_WARNING_THRESHOLD": 0.85,
        "QUALITY_GOOD_THRESHOLD": 0.95,
        "MAX_VIOLATIONS_PER_STAGE": 3,
        "MAX_STAGE_FAILURES": 1,
    },
    
    "COMPUTE_DOMAIN (NEW)": {
        "TOPOLOGY_COHERENCE": 0.93,
        "STATE_TRANSITION_FIDELITY": 0.96,
        "LINK_VALIDITY_CONFIDENCE": 0.94,
        "HALF_COHERENCE": "derived",
        "DOUBLE_COHERENCE": "derived",
        "GRID_CELL_SIZE": 10.0,
        "STATE_LOCK_DURATION": 60.0,
        "NUMERIC_STABILITY_MARGIN": 1e-6,
        "ORTHOGONALITY_THRESHOLD": 0.9,
        "GRID_SEARCH_EXPANSION": 2,
        "CENTROID_DAMPING": 0.01,
    },
}


# ============================================================================
# ANALYSIS: MEASUREMENT CLASSIFICATION
# ============================================================================

class MeasurementAnalyzer:
    """Analyze which measurements are duplicated vs unique."""
    
    def __init__(self, domains: Dict):
        self.domains = domains
        self.measurement_occurrence = {}  # name → [domains that have it]
        self.classification = {}  # name → "UNIVERSAL" | "NEAR_UNIVERSAL" | "DUPLICATE" | "UNIQUE"
    
    def analyze(self):
        """Run full analysis."""
        # Count occurrences
        for domain, measurements in self.domains.items():
            for meas_name, meas_value in measurements.items():
                if meas_name not in self.measurement_occurrence:
                    self.measurement_occurrence[meas_name] = []
                self.measurement_occurrence[meas_name].append((domain, meas_value))
        
        # Classify
        total_domains = len(self.domains)
        
        for meas_name, occurrences in self.measurement_occurrence.items():
            num_domains = len(occurrences)
            
            if num_domains == total_domains:
                self.classification[meas_name] = "UNIVERSAL"
            elif num_domains >= total_domains * 0.75:
                self.classification[meas_name] = "NEAR_UNIVERSAL"
            elif num_domains > 1:
                self.classification[meas_name] = "DUPLICATE"
            else:
                self.classification[meas_name] = "UNIQUE"
        
        return self
    
    def print_report(self):
        """Print analysis report."""
        print("\n" + "="*80)
        print("MEASUREMENT CLASSIFICATION REPORT")
        print("="*80)
        
        # UNIVERSAL measurements (appear in ALL domains)
        universal = [m for m, c in self.classification.items() if c == "UNIVERSAL"]
        if universal:
            print("\n[UNIVERSAL] These should be SHARED (appear in every domain):")
            for m in sorted(universal):
                print(f"  ✓ {m}")
                for domain, value in self.measurement_occurrence[m]:
                    print(f"      {domain}: {value}")
        
        # NEAR_UNIVERSAL (appear in 3+ domains)
        near_universal = [m for m, c in self.classification.items() if c == "NEAR_UNIVERSAL"]
        if near_universal:
            print("\n[NEAR_UNIVERSAL] These appear in 3+ domains (likely should be shared):")
            for m in sorted(near_universal):
                print(f"  ~ {m}")
                for domain, value in self.measurement_occurrence[m]:
                    print(f"      {domain}: {value}")
        
        # DUPLICATE (appear in 2 domains) - THESE ARE THE PROBLEM!
        duplicates = [m for m, c in self.classification.items() if c == "DUPLICATE"]
        if duplicates:
            print("\n[DUPLICATE] ✗ PROBLEM: These appear in 2 domains (should merge or move):")
            for m in sorted(duplicates):
                print(f"  ✗ {m}")
                for domain, value in self.measurement_occurrence[m]:
                    print(f"      {domain}: {value}")
        
        # UNIQUE (appear in only 1 domain)
        unique = [m for m, c in self.classification.items() if c == "UNIQUE"]
        if unique:
            print("\n[UNIQUE] These are domain-specific (OK to keep local):")
            for m in sorted(unique):
                domain, value = self.measurement_occurrence[m][0]
                print(f"  • {m} ({domain}): {value}")
        
        print("\n" + "="*80)
        print(f"SUMMARY:")
        print(f"  Total measurements: {len(self.measurement_occurrence)}")
        print(f"  Universal (shared): {len(universal)}")
        print(f"  Near-universal (3+): {len(near_universal)}")
        print(f"  Duplicates (2): {len(duplicates)} ← ELIMINATE THESE")
        print(f"  Unique (1): {len(unique)}")
        print("="*80)


# ============================================================================
# SOLUTION: SHARED MEASUREMENT REGISTRY
# ============================================================================

class SharedMeasurementCatalog:
    """
    Central catalog of measurements that should be shared across domains.
    
    Instead of each domain defining PIPELINE_INVARIANCE = 0.9989,
    they all reference: SharedMeasurementCatalog.PIPELINE_INVARIANCE
    """
    
    # ===== UNIVERSAL MEASUREMENTS (all domains use these) =====
    # These represent the fundamental pipeline efficiency
    
    class Universal:
        """Measurements that appear in ALL domains and should be shared."""
        PIPELINE_INVARIANCE = 0.9989  # 99.89% pipeline efficiency
        PIPELINE_VARIANCE = 1.0 - PIPELINE_INVARIANCE  # 0.0011 error margin
        HALF_INVARIANCE = PIPELINE_INVARIANCE / 2  # 0.49945
        DOUBLE_INVARIANCE = PIPELINE_INVARIANCE * 2  # 1.9978
    
    class GeometryAndPhysics:
        """Measurements related to standard geometric/physical constants."""
        ISOMETRIC_ELEVATION_DEG = 35.26  # arctan(sqrt(2)) for isometric projection
        ISOMETRIC_AZIMUTH_DEG = 45.0  # Standard isometric azimuth
        FREQUENCY_MULTIPLIER_OCTAVE = 2.0  # Harmonic octave = 2x frequency
        HARMONIC_PERFECT_FIFTH = 1.5  # Natural harmonic ratio
        NUMERIC_STABILITY_MARGIN = 1e-6  # IEEE 754 standard
        ORTHOGONALITY_THRESHOLD = 0.9  # Basis vector independence
    
    class ComputeSpecific:
        """Measurements unique to compute domain."""
        TOPOLOGY_COHERENCE = 0.93
        STATE_TRANSITION_FIDELITY = 0.96
        LINK_VALIDITY_CONFIDENCE = 0.94


# ============================================================================
# REWRITE STRATEGY
# ============================================================================

print("""
CONTAINER UNIFICATION STRATEGY
===============================

PHASE 1: Create SharedMeasurementCatalog (above)
  - Consolidate all UNIVERSAL and NEAR_UNIVERSAL measurements
  - Single source of truth for PIPELINE_INVARIANCE, etc.

PHASE 2: Update each domain to reference Catalog
  OLD:
    class AudioInvarianceConstants:
        PIPELINE_INVARIANCE = 0.9989
  
  NEW:
    from INVARIANCE_PATTERN_FRAMEWORK import SharedMeasurementCatalog
    
    _audio_pattern = InvariancePatternTemplate(
      domain_name="audio",
      measurements={
        "PIPELINE_INVARIANCE": SharedMeasurementCatalog.Universal.PIPELINE_INVARIANCE,
        ...
      }
    )

PHASE 3: Eliminate duplication
  - Any domain that uses PIPELINE_INVARIANCE gets it from Catalog (NOT local)
  - Any domain with unique measurements defines them locally
  - Register everything in InvarianceContainerRegistry

RESULT: 
  - One source of truth per measurement
  - No more scattered 0.9989 values
  - Cross-domain consistency guaranteed
  - Easy to update invariances (change in one place, all domains updated)
""")


if __name__ == "__main__":
    analyzer = MeasurementAnalyzer(DOMAINS_AND_MEASUREMENTS)
    analyzer.analyze()
    analyzer.print_report()
    
    print("\n\n[SHARED MEASUREMENT CATALOG DEFINED ABOVE]")
    print("Ready for implementation in Phase 2.")
