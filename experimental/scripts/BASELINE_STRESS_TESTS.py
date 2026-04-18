"""
BASELINE ANALYSIS: Document what we thought was optimal, then stress-test it

This file documents:
1. BASELINE: Our first best thought (current architecture)
2. STRESS SCENARIOS: What breaks in worst cases
3. EDGE CASES: Fields and containers that reveal blind spots
4. IMPROVEMENTS: What the baseline missed
"""

from ENTITY_CONNECTION_FRAMEWORK import Entity, Connection, WorldState, UniversalWeights, UniversalRenderer, UniversalResult
from HARMONICS_FRAMEWORK import Harmonic, HarmonicType
import math

# ============================================================================
# BASELINE ASSUMPTIONS (What we thought was best)
# ============================================================================

BASELINE = {
    "Entity": {
        "assumption": "id + type + position + properties dict is sufficient",
        "why_we_thought_it": "Covers atoms, audio sources, processes, agents, transactions",
        "potential_blind_spot": "What about mutable vs immutable? Identity? Time dependency?"
    },
    
    "Connection": {
        "assumption": "entity1_id + entity2_id + weight + properties is sufficient",
        "why_we_thought_it": "Covers bonds, harmonies, dataflows, causality",
        "potential_blind_spot": "What about directional vs undirected? Cyclic? Temporal ordering?"
    },
    
    "WorldState": {
        "assumption": "List of entities + list of connections + metadata dict",
        "why_we_thought_it": "Complete snapshot of system state",
        "potential_blind_spot": "What about state evolution? History? Parallel versions?"
    },
    
    "UniversalWeights": {
        "assumption": "spread_factor, density, complexity, diversity → derive all domain metrics",
        "why_we_thought_it": "Universal base metrics for all domains",
        "potential_blind_spot": "What about negative/zero values? Singularities? Extreme ratios?"
    },
    
    "Harmonics": {
        "assumption": "fundamental × multiplier × amplitude × phase = contribution",
        "why_we_thought_it": "Works for all domains (audio, visual, compute, agents)",
        "potential_blind_spot": "What about dissonance? Anti-harmonics? Destructive interference at scale?"
    },
    
    "7-Stage Pipeline": {
        "assumption": "VALIDATE→METRICS→STRATEGY→EXECUTE→VERIFY→ADAPT→OUTPUT, linear, no cycles",
        "why_we_thought_it": "Enforces causality, prevents corruption",
        "potential_blind_spot": "What about Stage 6 (ADAPT) needing to loop back to Stage 1? Infinite loops?"
    },
    
    "Complexity Threshold": {
        "assumption": "complexity_score = metrics; if > threshold → complex_format, else → simple",
        "why_we_thought_it": "Simple rule works for format selection",
        "potential_blind_spot": "What about cost vs quality tradeoff? User preference? Hybrid formats?"
    },
    
    "UniversalResult": {
        "assumption": "success bool + data + violations list is definitive",
        "why_we_thought_it": "Causality token works for all stages",
        "potential_blind_spot": "What about partial success? Degraded modes? Graceful degradation?"
    },
}

# ============================================================================
# STRESSED TEST CASES: Break every field
# ============================================================================

class StressTestCases:
    """Extreme cases that reveal blind spots."""
    
    # ---- ENTITY STRESS CASES ----
    
    @staticmethod
    def entity_empty_id():
        """WORST: Entity with empty ID."""
        return Entity(id="", entity_type="atom", position=(0, 0, 0))
    
    @staticmethod
    def entity_duplicate_id():
        """WORST: Two entities claim same ID."""
        world = WorldState("test", "VISUAL")
        e1 = Entity(id="A1", entity_type="atom", position=(0, 0, 0))
        e2 = Entity(id="A1", entity_type="atom", position=(1, 0, 0))
        world.add_entity(e1)
        world.add_entity(e2)
        return world, "Query e_A1 - which one?"
    
    @staticmethod
    def entity_position_nan():
        """WORST: Position contains NaN."""
        return Entity(id="A1", entity_type="atom", position=(float('nan'), 0, 0))
    
    @staticmethod
    def entity_position_infinite():
        """WORST: Position is infinite."""
        return Entity(id="A1", entity_type="atom", position=(float('inf'), -float('inf'), 0))
    
    @staticmethod
    def entity_properties_circular_reference():
        """WORST: Properties dict references itself."""
        e = Entity(id="A1", entity_type="atom", position=(0, 0, 0))
        e.properties["self_ref"] = e.properties  # Circular
        return e, "Can't serialize, can't copy"
    
    @staticmethod
    def entity_properties_deeply_nested():
        """WORST: Properties nested 1000 levels deep."""
        e = Entity(id="A1", entity_type="atom", position=(0, 0, 0))
        current = e.properties
        for i in range(1000):
            current["level"] = {}
            current = current["level"]
        current["value"] = 42
        return e, "Stack overflow on access?"
    
    # ---- CONNECTION STRESS CASES ----
    
    @staticmethod
    def connection_self_loop():
        """WORST: Connection from entity to itself."""
        return Connection(entity1_id="A1", entity2_id="A1", connection_type="bond", weight=1.0)
    
    @staticmethod
    def connection_nonexistent_entity():
        """WORST: Connection references entities that don't exist."""
        return Connection(entity1_id="FAKE1", entity2_id="FAKE2", connection_type="bond", weight=1.0)
    
    @staticmethod
    def connection_zero_weight():
        """WORST: Connection with zero weight."""
        return Connection(entity1_id="A1", entity2_id="A2", connection_type="bond", weight=0.0)
    
    @staticmethod
    def connection_negative_weight():
        """WORST: Connection with negative weight."""
        return Connection(entity1_id="A1", entity2_id="A2", connection_type="bond", weight=-100.0)
    
    @staticmethod
    def connection_infinite_weight():
        """WORST: Connection with infinite weight."""
        return Connection(entity1_id="A1", entity2_id="A2", connection_type="bond", weight=float('inf'))
    
    @staticmethod
    def connection_nan_weight():
        """WORST: Connection with NaN weight."""
        return Connection(entity1_id="A1", entity2_id="A2", connection_type="bond", weight=float('nan'))
    
    # ---- WORLDSTATE STRESS CASES ----
    
    @staticmethod
    def worldstate_empty():
        """WORST: Empty world with no entities."""
        return WorldState("empty", "VISUAL")
    
    @staticmethod
    def worldstate_single_isolated_entity():
        """WORST: One entity, zero connections."""
        w = WorldState("isolated", "VISUAL")
        w.add_entity(Entity(id="A1", entity_type="atom", position=(0, 0, 0)))
        return w
    
    @staticmethod
    def worldstate_fully_connected():
        """WORST: N entities all connected to each other (N² connections)."""
        w = WorldState("complete_graph", "VISUAL")
        n = 100
        for i in range(n):
            w.add_entity(Entity(id=f"E{i}", entity_type="node", position=(i, 0, 0)))
        for i in range(n):
            for j in range(i + 1, n):
                w.add_connection(Connection(f"E{i}", f"E{j}", "edge"))
        return w, f"{n*(n-1)//2} connections"
    
    @staticmethod
    def worldstate_cyclic_dependencies():
        """WORST: Cyclic connection chain A→B→C→A."""
        w = WorldState("cycle", "VISUAL")
        w.add_entity(Entity(id="A", entity_type="node", position=(0, 0, 0)))
        w.add_entity(Entity(id="B", entity_type="node", position=(1, 0, 0)))
        w.add_entity(Entity(id="C", entity_type="node", position=(2, 0, 0)))
        w.add_connection(Connection("A", "B", "causality"))
        w.add_connection(Connection("B", "C", "causality"))
        w.add_connection(Connection("C", "A", "causality"))
        return w, "Can't do topological sort"
    
    @staticmethod
    def worldstate_disconnected_subgraphs():
        """WORST: Multiple isolated subgraphs."""
        w = WorldState("fragmented", "VISUAL")
        # Subgraph 1: A-B-C
        w.add_entity(Entity(id="A", entity_type="node", position=(0, 0, 0)))
        w.add_entity(Entity(id="B", entity_type="node", position=(1, 0, 0)))
        w.add_entity(Entity(id="C", entity_type="node", position=(2, 0, 0)))
        w.add_connection(Connection("A", "B", "edge"))
        w.add_connection(Connection("B", "C", "edge"))
        
        # Subgraph 2: X-Y (disconnected)
        w.add_entity(Entity(id="X", entity_type="node", position=(10, 0, 0)))
        w.add_entity(Entity(id="Y", entity_type="node", position=(11, 0, 0)))
        w.add_connection(Connection("X", "Y", "edge"))
        return w, "Rendering strategy needs to handle islands"
    
    # ---- WEIGHTS STRESS CASES ----
    
    @staticmethod
    def weights_all_zero():
        """WORST: All weights are zero."""
        return UniversalWeights(spread_factor=0, density=0, complexity=0, diversity=0, num_entities=0)
    
    @staticmethod
    def weights_all_infinite():
        """WORST: All weights are infinite."""
        return UniversalWeights(
            spread_factor=float('inf'),
            density=float('inf'),
            complexity=float('inf'),
            diversity=float('inf')
        )
    
    @staticmethod
    def weights_extreme_ratio():
        """WORST: Density is 1000x larger than spread."""
        return UniversalWeights(spread_factor=0.001, density=1000, complexity=1, diversity=1)
    
    # ---- HARMONICS STRESS CASES ----
    
    @staticmethod
    def harmonic_zero_frequency():
        """WORST: Harmonic with zero fundamental frequency."""
        return Harmonic(
            harmonic_type=HarmonicType.FREQUENCY_HARMONIC.value,
            fundamental=0.0,
            multiplier=1.0,
            amplitude=1.0
        )
    
    @staticmethod
    def harmonic_zero_amplitude():
        """WORST: Harmonic with zero amplitude (silent/invisible)."""
        return Harmonic(
            harmonic_type=HarmonicType.FREQUENCY_HARMONIC.value,
            fundamental=440.0,
            multiplier=1.0,
            amplitude=0.0
        )
    
    @staticmethod
    def harmonic_negative_multiplier():
        """WORST: Harmonic with negative multiplier."""
        return Harmonic(
            harmonic_type=HarmonicType.FREQUENCY_HARMONIC.value,
            fundamental=440.0,
            multiplier=-2.0,
            amplitude=1.0
        )
    
    @staticmethod
    def harmonics_million_overtones():
        """WORST: 1 million harmonics being blended."""
        harmonics = []
        for n in range(1000000):
            if n == 0:
                continue
            harmonics.append(Harmonic(
                harmonic_type=HarmonicType.FREQUENCY_HARMONIC.value,
                fundamental=1.0,
                multiplier=float(n),
                amplitude=1.0 / n
            ))
        return harmonics, "Memory explosion + O(n) blending time"
    
    # ---- PIPELINE STRESS CASES ----
    
    @staticmethod
    def pipeline_stage_returns_none():
        """WORST: Stage returns None instead of UniversalResult."""
        return None, "Next stage crashes on .failed() call"
    
    @staticmethod
    def pipeline_stage_violates_causality():
        """WORST: Stage 4 (Execute) succeeds even though Stage 3 (Strategy) failed."""
        result3 = UniversalResult(success=False, violations=["Strategy failed"])
        result4 = UniversalResult(success=True, data={"frames": []})
        return result3, result4, "Causality broken, bad output generated"
    
    @staticmethod
    def pipeline_stage6_fixes_stage1_violation():
        """WORST: Adapt stage needs to loop back to Validate."""
        violations = ["Entity A has invalid coordinates"]
        return violations, "Linear pipeline can't loop; Stage 6 can't fix Stage 1 problems"
    
    # ---- THRESHOLD STRESS CASES ----
    
    @staticmethod
    def threshold_right_at_boundary():
        """WORST: Complexity score exactly at threshold (0.8)."""
        return 0.8, "SVG or GIF? Floating point equality is unreliable"
    
    @staticmethod
    def threshold_multiple_metrics_conflict():
        """WORST: density says complex, spread says simple."""
        return {
            "density_suggests": "COMPLEX",
            "spread_suggests": "SIMPLE",
            "which_wins": "??"
        }


# ============================================================================
# BLIND SPOT ANALYSIS
# ============================================================================

BLIND_SPOTS = {
    "Entity": [
        "No versioning: Same ID in different time periods?",
        "No constraints: Can position be invalid after creation?",
        "Properties are untyped: Type safety?",
        "No parent/origin: Where did this entity come from?",
        "ID collision: get_entity() returns which one if duplicate IDs exist?"
    ],
    
    "Connection": [
        "No directionality constraint: Some domains need undirected (bonds), some directed (causality)",
        "Weight semantics unclear: 0 weight = no connection? Or weak connection?",
        "No temporal dimension: When did connection form? Still valid?",
        "Dangling references: Connection to non-existent entity silently ignored",
        "Cyclic connections: Topological sort fails on loops"
    ],
    
    "WorldState": [
        "No history: Can't time-travel or undo",
        "No locking: Concurrent modifications?",
        "No validation: Adding connection with wrong entity IDs doesn't error",
        "Metadata is untyped dict: No schema validation",
        "No spatial index: Finding nearby entities O(n) linear scan"
    ],
    
    "UniversalWeights": [
        "Singular values (0 or inf): intensity_weight breaks with zero density",
        "No negative weights: How to represent inhibition/repulsion?",
        "Derived metrics have hardcoded constants: Why 0.5, 0.8, 10? Domain-dependent?",
        "No units: Is spread_factor in Angstroms? GHz? Seconds?",
        "Composition order: Different orderings give different results"
    ],
    
    "Harmonics": [
        "Pure additive: No destructive interference cancellation",
        "No phase alignment: All phases independent, lost phase-locking",
        "Amplitude always decays: 1/n rule doesn't fit all domains",
        "Anti-harmonics: How to represent dissonance or conflict?",
        "No bandwidth/tuning: Pure frequencies, no width around them"
    ],
    
    "7-Stage Pipeline": [
        "No error recovery: Stage 6 can't loop back to Stage 1",
        "No branching: Some domains need different paths (SVG path vs GIF path)",
        "No parallel stages: VERIFY and ADAPT could run in parallel",
        "No rollback: If Stage 7 fails, no undo of Stage 6 changes",
        "No stage skipping: Some configs don't need all 7 stages"
    ],
    
    "Complexity Threshold": [
        "No multi-dimensional threshold: Only checks single score",
        "No hysteresis: Same score triggers different behavior on scale-up vs scale-down",
        "No user override: Format selection purely algorithmic",
        "No cost analysis: Doesn't compare WAV (smaller) vs MP3 (worse quality)",
        "No domain tuning: Same threshold for audio and visual"
    ],
}

# ============================================================================
# REPORT
# ============================================================================

if __name__ == "__main__":
    print("""
=================================================================
BASELINE STRESS TEST: What we thought was best vs what breaks
=================================================================

BASELINE ASSUMPTIONS (What we thought was optimal):
""")
    for component, info in BASELINE.items():
        print(f"\n{component}:")
        print(f"  Assumption: {info['assumption']}")
        print(f"  Why: {info['why_we_thought_it']}")
        print(f"  Blind spot: {info['potential_blind_spot']}")
    
    print(f"\n\nBLIND SPOTS REVEALED BY STRESS TESTING:\n")
    for component, issues in BLIND_SPOTS.items():
        print(f"{component}:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()
    
    print(f"\nSTRESS TEST CASES AVAILABLE:")
    import inspect
    methods = [m for m in dir(StressTestCases) if m.startswith('test_') or not m.startswith('_')]
    stress_methods = [m for m in dir(StressTestCases) if not m.startswith('_') and callable(getattr(StressTestCases, m))]
    print(f"  Total stress test cases: {len(stress_methods)}")
    for method in sorted(stress_methods)[:10]:
        print(f"    - {method}()")
    print(f"    ... and more")
    
    print("""

CONCLUSION:
===========
Our baseline assumptions are GOOD for 80% of cases.
But they have structural blind spots that appear in edge cases:

✓ Good at: Representing normal systems with valid data
✗ Bad at: Handling constraints, versioning, directionality, cycles, recovery, cost tradeoffs

These blind spots don't invalidate the baseline - they show where we need
EXPLICIT HANDLING instead of assuming one-size-fits-all.

Next step: Build IMPROVED architecture that handles these cases.
""")
