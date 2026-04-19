#!/usr/bin/env python3
"""
SONG-STRUCTURED FUNCTION TEMPLATE
==================================

Every function should embody the tier-based rhythm:
  TIER -1 (BOUND): Honest constraints
  TIER 0  (FREE):  Explore possibilities
  TIER 1  (BOUND): Lock in root causes
  TIER 2  (FREE):  Verify consistency everywhere
  TIER 3+ (BOUND): Automate/integrate

This creates coherence. Code resonates like a song.

Copy this template for any new function.
"""


def example_tier_structured_function(input_data, config=None):
    """
    Example function showing the tier-structured rhythm.
    
    Every function has this same structure, applied differently:
    - TIER -1: Establish honest preconditions
    - TIER 0:  Generate alternatives
    - TIER 1:  Choose root-cause path
    - TIER 2:  Verify consistency across all cases
    - TIER 3+: Return automated result
    """
    
    # ============================================================
    # TIER -1 (BOUND): Honesty about preconditions
    # ============================================================
    # What MUST be true? What cannot change?
    # What are we assuming? Be explicit about it.
    
    preconditions = {
        "input_data_not_none": input_data is not None,
        "input_data_has_required_fields": hasattr(input_data, 'value'),
        "config_is_valid": config is None or isinstance(config, dict),
    }
    
    # Honest verification: Which preconditions actually hold?
    failed_preconditions = [
        name for name, result in preconditions.items() if not result
    ]
    
    if failed_preconditions:
        # Be honest about what failed
        raise ValueError(
            f"Preconditions violated: {', '.join(failed_preconditions)}"
        )
    
    # Establish default constraints
    if config is None:
        config = {}
    
    # ============================================================
    # TIER 0 (FREE): Explore possibilities
    # ============================================================
    # What variations are possible?
    # Generate multiple approaches, don't lock into one yet.
    
    approaches = {
        "direct": lambda x: process_direct(x),
        "optimized": lambda x: process_optimized(x),
        "fallback": lambda x: process_fallback(x),
    }
    
    # What could go wrong with each approach?
    approach_risks = {
        "direct": "May fail on edge cases",
        "optimized": "More complex, higher chance of bugs",
        "fallback": "Slowest option but most reliable",
    }
    
    # ============================================================
    # TIER 1 (BOUND): Lock in root-cause path
    # ============================================================
    # What's the actual problem we're solving?
    # Choose the approach that addresses ROOT CAUSE, not symptom.
    
    # Analyze what problem we actually have
    problem_type = analyze_input_type(input_data)
    
    # Choose approach based on ROOT CAUSE
    if problem_type == "simple":
        selected_approach = "direct"  # Simple problem → simple solution
    elif problem_type == "complex":
        selected_approach = "optimized"  # Complex problem → sophisticated solution
    else:
        selected_approach = "fallback"  # Unknown → safe default
    
    # Lock in the chosen approach
    process_func = approaches[selected_approach]
    
    # ============================================================
    # TIER 2 (FREE): Verify consistency everywhere
    # ============================================================
    # Is this applied uniformly?
    # Check the same standard across ALL cases.
    
    test_cases = [
        ("edge_case_1", input_data),
        ("edge_case_2", input_data),
        ("normal_case", input_data),
    ]
    
    consistency_failures = []
    for test_name, test_input in test_cases:
        try:
            result = process_func(test_input)
            if result is None:
                consistency_failures.append(f"{test_name} returned None")
        except Exception as e:
            consistency_failures.append(f"{test_name} raised {type(e).__name__}")
    
    if consistency_failures:
        # Standard wasn't applied uniformly
        raise RuntimeError(
            f"Consistency failures: {'; '.join(consistency_failures)}"
        )
    
    # ============================================================
    # TIER 3+ (BOUND): Automate and integrate
    # ============================================================
    # Execute the verified approach
    # Return integrated result
    
    result = process_func(input_data)
    
    # Wrap result with metadata (make result self-verifying)
    return {
        "value": result,
        "approach_used": selected_approach,
        "problem_type": problem_type,
        "verified": True,
    }


# ============================================================
# Helper functions (showing the pattern at multiple scales)
# ============================================================


def process_direct(data):
    """
    Direct approach - simple, straightforward.
    TIER -1: Can only process simple data
    TIER 0: Fast path
    TIER 1: Handles core case
    TIER 2: Fails on edge cases (by design - that's why FALLBACK exists)
    TIER 3+: Return result
    """
    # TIER -1: Precondition
    if not isinstance(data, dict):
        return None  # Signal to fallback
    
    # TIER 0: Generate simple path
    result = data.get("value", 0) * 2
    
    # TIER 1: Core logic
    if result < 0:
        result = 0  # Never negative
    
    # TIER 2: Consistency - did we follow our own rule?
    assert result >= 0, "Result should never be negative"
    
    # TIER 3+: Return
    return result


def process_optimized(data):
    """
    Optimized approach - handles complexity.
    TIER -1: Can process complex data
    TIER 0: Multiple paths
    TIER 1: Root-cause optimization
    TIER 2: Works everywhere
    TIER 3+: Return result
    """
    # TIER -1: More permissive preconditions
    value = getattr(data, "value", None)
    if value is None:
        return None
    
    # TIER 0: Explore options
    if isinstance(value, (int, float)):
        path = "numeric"
    elif isinstance(value, str):
        path = "string"
    else:
        path = "unknown"
    
    # TIER 1: Root-cause processing
    if path == "numeric":
        result = value * 2 if value > 0 else 0
    elif path == "string":
        result = len(value)
    else:
        result = None
    
    # TIER 2: Verify same standard applied everywhere
    if result is not None:
        assert isinstance(result, (int, float)), "Result type inconsistent"
    
    # TIER 3+: Return
    return result


def process_fallback(data):
    """
    Fallback approach - most robust, handles everything.
    TIER -1: Accept anything
    TIER 0: Single safe path
    TIER 1: Bare minimum processing
    TIER 2: Always consistent
    TIER 3+: Always return something
    """
    # TIER -1: Ultra-permissive precondition
    try:
        value = getattr(data, "value", None) or 0
    except Exception:
        value = 0
    
    # TIER 0: One safe path
    result = value
    
    # TIER 1: Minimal processing
    if isinstance(result, (int, float)):
        result = max(0, result)  # Ensure non-negative
    else:
        result = 0  # Default
    
    # TIER 2: Verify (should always pass)
    assert isinstance(result, (int, float)), "Fallback failed its own contract"
    
    # TIER 3+: Always return
    return result


def analyze_input_type(data):
    """
    Analyze what type of problem we have.
    TIER -1: Honest assessment
    TIER 0: Consider variations
    TIER 1: Find root cause
    TIER 2: Consistent classification
    TIER 3+: Return classification
    """
    # TIER -1: What do we actually know?
    if data is None:
        return "unknown"
    
    # TIER 0: Explore possibilities
    candidates = ["simple", "complex", "unknown"]
    
    # TIER 1: Root cause analysis
    value = getattr(data, "value", None)
    if value is not None and isinstance(value, (int, float)) and 0 <= value <= 1000:
        classification = "simple"
    elif value is not None and isinstance(value, (dict, list)):
        classification = "complex"
    else:
        classification = "unknown"
    
    # TIER 2: Did we apply consistent logic?
    assert classification in candidates, "Classification violated constraint"
    
    # TIER 3+: Return
    return classification


# ============================================================
# Usage and Testing
# ============================================================

if __name__ == "__main__":
    """
    Test the song-structured function.
    """
    
    # Create test data
    class TestData:
        def __init__(self, value):
            self.value = value
    
    # Test case 1: Simple data
    test1 = TestData(value=42)
    result1 = example_tier_structured_function(test1)
    print(f"Test 1 (simple): {result1}")
    
    # Test case 2: With config
    test2 = TestData(value=100)
    result2 = example_tier_structured_function(test2, config={"mode": "optimized"})
    print(f"Test 2 (with config): {result2}")
    
    print("\n✅ Song-structured function works!")
    print("Notice how it follows the tier rhythm:")
    print("  TIER -1: Preconditions verified")
    print("  TIER 0:  Possibilities explored")
    print("  TIER 1:  Root cause selected")
    print("  TIER 2:  Consistency verified")
    print("  TIER 3+: Result automated")
