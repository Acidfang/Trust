"""
Learning Features for Coherence Laboratory

Hypothesis testing, pattern detection, and comparison views
to help understand what drives coherence progression.

Every choice shows outcome. Every outcome teaches pattern.
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Hypothesis:
    """A testable hypothesis about coherence"""
    statement: str
    test_parameter: str  # e.g., "clarity", "tier"
    min_value: float
    max_value: float
    expected_outcome: str
    test_results: List[Tuple[float, bool]] = None  # (parameter_value, success)
    
    def __post_init__(self):
        if self.test_results is None:
            self.test_results = []
    
    def add_result(self, parameter_value: float, success: bool):
        """Record test result"""
        self.test_results.append((parameter_value, success))
    
    def confidence_level(self) -> float:
        """Calculate confidence (0.0-1.0) based on results"""
        if not self.test_results:
            return 0.0
        
        successes = sum(1 for _, success in self.test_results if success)
        return successes / len(self.test_results)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get human-readable summary"""
        return {
            "statement": self.statement,
            "parameter": self.test_parameter,
            "range": f"{self.min_value:.2f}-{self.max_value:.2f}",
            "tests_run": len(self.test_results),
            "confidence": f"{self.confidence_level():.2%}",
            "expected": self.expected_outcome
        }


@dataclass
class Pattern:
    """Discovered pattern in coherence data"""
    pattern_name: str
    description: str
    conditions: List[Dict[str, Any]]  # e.g., [{'tier': 4}, {'clarity': '>0.9'}]
    outcomes: List[str]  # What happens when pattern occurs
    frequency: int = 0  # How often observed
    strength: float = 0.0  # Pattern strength (0.0-1.0)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get human-readable summary"""
        return {
            "pattern": self.pattern_name,
            "description": self.description,
            "conditions": self.conditions,
            "outcomes": self.outcomes,
            "frequency": self.frequency,
            "strength": f"{self.strength:.2%}"
        }


class ComparisonScenario:
    """Side-by-side comparison of two scenarios"""
    
    def __init__(self, scenario_a_name: str, scenario_b_name: str):
        """Initialize comparison"""
        self.scenario_a_name = scenario_a_name
        self.scenario_b_name = scenario_b_name
        self.scenario_a_params = {}
        self.scenario_b_params = {}
        self.scenario_a_outcomes = []
        self.scenario_b_outcomes = []
    
    def set_scenario_a(self, params: Dict[str, float], outcomes: List[str] = None):
        """Set scenario A parameters and outcomes"""
        self.scenario_a_params = params
        self.scenario_a_outcomes = outcomes or []
    
    def set_scenario_b(self, params: Dict[str, float], outcomes: List[str] = None):
        """Set scenario B parameters and outcomes"""
        self.scenario_b_params = params
        self.scenario_b_outcomes = outcomes or []
    
    def get_differences(self) -> Dict[str, Tuple[Any, Any]]:
        """Get differing parameters between scenarios"""
        all_keys = set(self.scenario_a_params.keys()) | set(self.scenario_b_params.keys())
        differences = {}
        
        for key in all_keys:
            val_a = self.scenario_a_params.get(key)
            val_b = self.scenario_b_params.get(key)
            
            if val_a != val_b:
                differences[key] = (val_a, val_b)
        
        return differences
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comparison summary"""
        return {
            "scenario_a": {
                "name": self.scenario_a_name,
                "params": self.scenario_a_params,
                "outcomes": self.scenario_a_outcomes
            },
            "scenario_b": {
                "name": self.scenario_b_name,
                "params": self.scenario_b_params,
                "outcomes": self.scenario_b_outcomes
            },
            "differences": self.get_differences()
        }


class PatternDetector:
    """Analyzes coherence data to discover patterns"""
    
    def __init__(self, sandbox_interface):
        """Initialize with access to sandbox"""
        self.sandbox = sandbox_interface
        self.discovered_patterns: List[Pattern] = []
    
    def detect_tier_patterns(self) -> List[Pattern]:
        """Detect patterns related to tier progression"""
        patterns = []
        
        # Pattern: Tier jumps after clarity increase
        clarity_trend = self.sandbox.get_dialogue_clarity_trend()
        if clarity_trend and len(clarity_trend) > 1:
            high_clarity_indices = [
                i for i, record in enumerate(clarity_trend)
                if record['clarity_level'] > 0.85
            ]
            
            if high_clarity_indices:
                pattern = Pattern(
                    pattern_name="High Clarity → Tier Jump",
                    description="Tier progression follows periods of high dialogue clarity",
                    conditions=[{'clarity_threshold': 0.85}],
                    outcomes=["tier_progression", "new_achievement"],
                    frequency=len(high_clarity_indices),
                    strength=min(1.0, len(high_clarity_indices) / max(1, len(clarity_trend)))
                )
                patterns.append(pattern)
        
        return patterns
    
    def detect_coherence_drivers(self) -> List[Pattern]:
        """Detect what increases coherence"""
        patterns = []
        
        # Pattern: Recording moments increases coherence
        current_state = self.sandbox.get_current_coherence()
        tier_progression = []
        for tier in range(1, 7):
            records = self.sandbox.get_tier_progression_for_tier(tier)
            if records:
                tier_progression.append({
                    'tier': tier,
                    'count': len(records),
                    'last_achieved': records[-1]['timestamp']
                })
        
        if len(tier_progression) > 1:
            pattern = Pattern(
                pattern_name="Recording Creates Progression",
                description="Each recorded moment contributes to tier advancement",
                conditions=[{'action': 'record_state'}],
                outcomes=["coherence_increase", "tier_unlock"],
                frequency=sum(p['count'] for p in tier_progression),
                strength=min(1.0, len(tier_progression) / 6.0)
            )
            patterns.append(pattern)
        
        return patterns
    
    def find_optimal_parameters(self) -> Dict[str, Tuple[float, float]]:
        """Find parameter ranges that maximize coherence"""
        optimal = {}
        
        # Analyze clarity's effect
        clarity_trend = self.sandbox.get_dialogue_clarity_trend()
        if clarity_trend:
            clarities = [r['clarity_level'] for r in clarity_trend]
            avg_clarity = sum(clarities) / len(clarities)
            max_clarity = max(clarities)
            
            optimal['clarity'] = (avg_clarity, max_clarity)
        
        # Analyze tier distribution
        tier_distribution = {}
        for tier in range(1, 7):
            records = self.sandbox.get_tier_progression_for_tier(tier)
            tier_distribution[tier] = len(records)
        
        if tier_distribution:
            optimal['tier_balanced'] = (
                sum(tier_distribution.values()) / len(tier_distribution),
                max(tier_distribution.values())
            )
        
        return optimal


class ComparisonView:
    """Creates and manages comparison visualizations"""
    
    def __init__(self, sandbox_interface):
        """Initialize with access to sandbox"""
        self.sandbox = sandbox_interface
        self.scenarios: List[ComparisonScenario] = []
    
    def create_hypothetical_comparison(self, param_name: str, value_range: Tuple[float, float]) -> ComparisonScenario:
        """Create hypothetical comparison (e.g., "what if clarity was 0.8 vs 0.95?")"""
        scenario_a = ComparisonScenario(
            f"{param_name} = {value_range[0]:.2f}",
            f"{param_name} = {value_range[1]:.2f}"
        )
        
        current_state = self.sandbox.get_current_coherence()
        if current_state:
            # Scenario A: lower value
            params_a = {'clarity': value_range[0]}
            scenario_a.set_scenario_a(params_a)
            
            # Scenario B: higher value
            params_b = {'clarity': value_range[1]}
            scenario_a.set_scenario_b(params_b)
            
            self.scenarios.append(scenario_a)
        
        return scenario_a
    
    def compare_tier_outcomes(self, tier_a: int, tier_b: int) -> ComparisonScenario:
        """Compare outcomes between two tier levels"""
        scenario = ComparisonScenario(
            f"Tier {tier_a}",
            f"Tier {tier_b}"
        )
        
        tier_a_records = self.sandbox.get_tier_progression_for_tier(tier_a)
        tier_b_records = self.sandbox.get_tier_progression_for_tier(tier_b)
        
        scenario.set_scenario_a(
            {'tier': tier_a, 'records': len(tier_a_records)},
            [r['achieved_through'] for r in tier_a_records[:3]]
        )
        
        scenario.set_scenario_b(
            {'tier': tier_b, 'records': len(tier_b_records)},
            [r['achieved_through'] for r in tier_b_records[:3]]
        )
        
        self.scenarios.append(scenario)
        return scenario


class HypothesisTester:
    """Framework for testing hypotheses about coherence"""
    
    def __init__(self, sandbox_interface):
        """Initialize with access to sandbox"""
        self.sandbox = sandbox_interface
        self.hypotheses: List[Hypothesis] = []
        self.test_history: List[Dict[str, Any]] = []
    
    def create_hypothesis(self, statement: str, parameter: str,
                         min_val: float, max_val: float,
                         expected_outcome: str) -> Hypothesis:
        """Create a new hypothesis to test"""
        hypothesis = Hypothesis(
            statement=statement,
            test_parameter=parameter,
            min_value=min_val,
            max_value=max_val,
            expected_outcome=expected_outcome
        )
        self.hypotheses.append(hypothesis)
        return hypothesis
    
    def test_hypothesis(self, hypothesis: Hypothesis, test_value: float) -> bool:
        """Run a single test of the hypothesis"""
        # Record the test in sandbox
        description = (
            f"Hypothesis test: {hypothesis.statement} "
            f"with {hypothesis.test_parameter}={test_value:.2f}"
        )
        
        self.sandbox.record_coherence_state(
            state="hypothesis_test",
            description=description
        )
        
        # Check if expected outcome occurred
        # This is simplified - real implementation would track actual outcomes
        success = test_value > (hypothesis.min_value + hypothesis.max_value) / 2
        
        hypothesis.add_result(test_value, success)
        
        self.test_history.append({
            'timestamp': datetime.now().isoformat(),
            'hypothesis': hypothesis.statement,
            'test_value': test_value,
            'success': success,
            'confidence': hypothesis.confidence_level()
        })
        
        return success
    
    def get_top_hypotheses(self, count: int = 5) -> List[Hypothesis]:
        """Get hypotheses ranked by confidence"""
        sorted_hypotheses = sorted(
            self.hypotheses,
            key=lambda h: h.confidence_level(),
            reverse=True
        )
        return sorted_hypotheses[:count]
    
    def get_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        return {
            'total_hypotheses': len(self.hypotheses),
            'total_tests': sum(len(h.test_results) for h in self.hypotheses),
            'average_confidence': (
                sum(h.confidence_level() for h in self.hypotheses) / max(1, len(self.hypotheses))
                if self.hypotheses else 0.0
            ),
            'top_hypotheses': [h.get_summary() for h in self.get_top_hypotheses(3)],
            'test_history_sample': self.test_history[-10:]  # Last 10 tests
        }


# Export public API
__all__ = [
    "Hypothesis",
    "Pattern",
    "ComparisonScenario",
    "PatternDetector",
    "ComparisonView",
    "HypothesisTester",
]
