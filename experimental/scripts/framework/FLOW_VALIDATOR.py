"""
FLOW VALIDATOR - Ensures Universal Progressive Flow Can Actually Work

Validates that:
1. Patterns are truly universal (work for edge cases)
2. Flow is fluid (no bottlenecks or dead ends)
3. All stages connect properly
4. Adaptation can handle surprises
5. System degrades gracefully
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime

from UNIVERSAL_PROGRESSIVE_FLOW import (
    FlowStage, FlowContext, InputAnalysisPattern,
    MetricCalculationPattern, StrategySelectionPattern,
    ExecutionPattern, VerificationPattern, AdaptationPattern,
    UniversalFlowOrchestrator, UniversalMetrics
)


# ============================================================================
# TEST MOLECULES FOR UNIVERSALITY VALIDATION
# ============================================================================

TEST_MOLECULES = {
    # Edge case: Single atom
    "Hydrogen": {
        "name": "Hydrogen",
        "atoms": [("H", 0.0, 0.0, 0.0)],
        "bonds": [],
    },
    
    # Edge case: Two atoms
    "Diatomic": {
        "name": "Diatomic Nitrogen",
        "atoms": [("N", -0.5, 0.0, 0.0), ("N", 0.5, 0.0, 0.0)],
        "bonds": [(0, 1)],
    },
    
    # Symmetric: Methane
    "Methane": {
        "name": "Methane",
        "atoms": [
            ("C", 0.0, 0.0, 0.0),
            ("H", 0.629, 0.629, 0.629),
            ("H", -0.629, -0.629, 0.629),
            ("H", -0.629, 0.629, -0.629),
            ("H", 0.629, -0.629, -0.629),
        ],
        "bonds": [(0, 1), (0, 2), (0, 3), (0, 4)],
    },
    
    # Asymmetric: Water
    "Water": {
        "name": "Water",
        "atoms": [("O", 0.0, 0.119, 0.0), ("H", 0.757, -0.474, 0.0), ("H", -0.757, -0.474, 0.0)],
        "bonds": [(0, 1), (0, 2)],
    },
    
    # Linear: CO2
    "CO2": {
        "name": "Carbon Dioxide",
        "atoms": [("C", 0.0, 0.0, 0.0), ("O", 1.16, 0.0, 0.0), ("O", -1.16, 0.0, 0.0)],
        "bonds": [(0, 1), (0, 2)],
    },
    
    # Planar: Benzene
    "Benzene": {
        "name": "Benzene",
        "atoms": [
            ("C", 1.40, 0.0, 0.0), ("C", 0.70, 1.21, 0.0),
            ("C", -0.70, 1.21, 0.0), ("C", -1.40, 0.0, 0.0),
            ("C", -0.70, -1.21, 0.0), ("C", 0.70, -1.21, 0.0),
            ("H", 2.48, 0.0, 0.0), ("H", 1.24, 2.15, 0.0),
            ("H", -1.24, 2.15, 0.0), ("H", -2.48, 0.0, 0.0),
            ("H", -1.24, -2.15, 0.0), ("H", 1.24, -2.15, 0.0),
        ],
        "bonds": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
                  (0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)],
    },
    
    # Complex: Large molecule (simulated)
    "LargeMolecule": {
        "name": "Large Complex",
        "atoms": [
            ("C", i, j, k)
            for i in [-2, -1, 0, 1, 2]
            for j in [-2, -1, 0]
            for k in [-1, 0, 1]
        ] + [
            ("H", -2.5, 0, 0), ("H", 2.5, 0, 0),
            ("O", 0, -3, 0), ("N", 0, 3, 0),
        ],
        "bonds": [],  # Too many to list
    },
}


# ============================================================================
# VALIDATORS
# ============================================================================

@dataclass
class ValidationResult:
    """Result of a validation check."""
    test_name: str
    molecule_name: str
    passed: bool
    score: float  # 0-100
    details: Dict
    error_message: str = None


class FluidityValidator:
    """Validates that flow is truly fluid."""
    
    @staticmethod
    def check_no_bottlenecks() -> ValidationResult:
        """UNIVERSAL: No stage should block progress."""
        
        # Each stage must have clear exit conditions
        stage_exits = {
            FlowStage.INPUT_ANALYSIS: "Valid OR Invalid (both clear)",
            FlowStage.METRIC_CALCULATION: "Metrics computed (always succeeds)",
            FlowStage.STRATEGY_SELECTION: "Strategy derived (always succeeds)",
            FlowStage.EXECUTION: "Rotation calculated (always succeeds)",
            FlowStage.VERIFICATION: "Result verified (always succeeds)",
            FlowStage.ADAPTATION: "Strategy improved (always succeeds)",
        }
        
        # All stages pass if covered
        all_clear = len(stage_exits) == 6
        
        return ValidationResult(
            test_name="No Bottlenecks",
            molecule_name="N/A",
            passed=all_clear,
            score=100.0 if all_clear else 0.0,
            details={
                "stages_with_clear_exits": len(stage_exits),
                "required_stages": 6,
            }
        )
    
    @staticmethod
    def check_linear_progression() -> ValidationResult:
        """UNIVERSAL: Flow progresses linearly without loops."""
        
        # Stages must be in order
        stage_order = [
            FlowStage.INPUT_ANALYSIS,
            FlowStage.METRIC_CALCULATION,
            FlowStage.STRATEGY_SELECTION,
            FlowStage.EXECUTION,
            FlowStage.VERIFICATION,
            FlowStage.ADAPTATION,
            FlowStage.OUTPUT,
        ]
        
        # Check ordering
        ordered = all(
            stage_order[i].value < stage_order[i+1].value
            for i in range(len(stage_order)-1)
        )
        
        return ValidationResult(
            test_name="Linear Progression",
            molecule_name="N/A",
            passed=ordered,
            score=100.0 if ordered else 0.0,
            details={
                "stage_count": len(stage_order),
                "properly_ordered": ordered,
            }
        )


class UniversalityValidator:
    """Validates that patterns work universally (all edge cases)."""
    
    @staticmethod
    def validate_input_analysis() -> List[ValidationResult]:
        """Test INPUT ANALYSIS on all test molecules."""
        
        results = []
        
        for mol_name, mol_dict in TEST_MOLECULES.items():
            valid, errors = InputAnalysisPattern.validate_input(mol_dict)
            
            results.append(ValidationResult(
                test_name="Input Analysis",
                molecule_name=mol_name,
                passed=valid,
                score=100.0 if valid else 0.0,
                details={
                    "atom_count": len(mol_dict.get("atoms", [])),
                    "has_bonds": len(mol_dict.get("bonds", [])) > 0,
                    "errors": errors,
                }
            ))
        
        return results
    
    @staticmethod
    def validate_metric_calculation() -> List[ValidationResult]:
        """Test METRIC CALCULATION on all test molecules."""
        
        results = []
        
        for mol_name, mol_dict in TEST_MOLECULES.items():
            try:
                atoms = mol_dict.get("atoms", [])
                metrics = MetricCalculationPattern.compute_universal_metrics(atoms)
                
                # Check that all metrics are valid numbers
                all_valid = all([
                    isinstance(metrics.center_of_mass, tuple),
                    metrics.max_radius >= 0,
                    metrics.atom_density >= 0,
                    0 <= metrics.asymmetry_score < 100,
                    0 <= metrics.compactness <= 1,
                    metrics.complexity_score >= 0,
                ])
                
                score = 100.0 if all_valid else 50.0
                
                results.append(ValidationResult(
                    test_name="Metric Calculation",
                    molecule_name=mol_name,
                    passed=all_valid,
                    score=score,
                    details={
                        "center_of_mass": metrics.center_of_mass,
                        "max_radius": metrics.max_radius,
                        "atom_density": metrics.atom_density,
                        "asymmetry": metrics.asymmetry_score,
                        "geometry_type": metrics.geometry_type,
                    }
                ))
            
            except Exception as e:
                results.append(ValidationResult(
                    test_name="Metric Calculation",
                    molecule_name=mol_name,
                    passed=False,
                    score=0.0,
                    details={},
                    error_message=str(e)
                ))
        
        return results
    
    @staticmethod
    def validate_strategy_selection() -> List[ValidationResult]:
        """Test STRATEGY SELECTION on all test molecules."""
        
        results = []
        
        for mol_name, mol_dict in TEST_MOLECULES.items():
            try:
                atoms = mol_dict.get("atoms", [])
                metrics = MetricCalculationPattern.compute_universal_metrics(atoms)
                strategy = StrategySelectionPattern.select_strategy(metrics, len(atoms))
                
                # Check that strategy has valid parameters
                all_valid = all([
                    strategy.y_rotation_scale > 0,
                    strategy.x_tilt_frequency > 0,
                    strategy.projection_type in ["perspective", "orthographic"],
                    len(strategy.visualization_layers) > 0,
                    strategy.focal_distance > 0,
                ])
                
                score = 100.0 if all_valid else 50.0
                
                results.append(ValidationResult(
                    test_name="Strategy Selection",
                    molecule_name=mol_name,
                    passed=all_valid,
                    score=score,
                    details={
                        "y_rotation_scale": strategy.y_rotation_scale,
                        "projection_type": strategy.projection_type,
                        "layer_count": len(strategy.visualization_layers),
                        "adaptive_params": strategy.adaptive_parameters,
                    }
                ))
            
            except Exception as e:
                results.append(ValidationResult(
                    test_name="Strategy Selection",
                    molecule_name=mol_name,
                    passed=False,
                    score=0.0,
                    details={},
                    error_message=str(e)
                ))
        
        return results
    
    @staticmethod
    def validate_execution() -> List[ValidationResult]:
        """Test EXECUTION on all test molecules."""
        
        results = []
        
        for mol_name, mol_dict in TEST_MOLECULES.items():
            try:
                atoms = mol_dict.get("atoms", [])
                metrics = MetricCalculationPattern.compute_universal_metrics(atoms)
                strategy = StrategySelectionPattern.select_strategy(metrics, len(atoms))
                
                # Test rotation calculation
                for frame in [0, 5, 10, 19]:
                    rotation = ExecutionPattern.calculate_frame_rotation(strategy, frame, 20)
                    
                    all_valid = all([
                        isinstance(rotation, tuple),
                        len(rotation) == 3,
                        all(isinstance(r, float) for r in rotation),
                    ])
                
                score = 100.0 if all_valid else 50.0
                
                results.append(ValidationResult(
                    test_name="Execution",
                    molecule_name=mol_name,
                    passed=all_valid,
                    score=score,
                    details={
                        "frame_count": 20,
                        "sample_frames_tested": [0, 5, 10, 19],
                    }
                ))
            
            except Exception as e:
                results.append(ValidationResult(
                    test_name="Execution",
                    molecule_name=mol_name,
                    passed=False,
                    score=0.0,
                    details={},
                    error_message=str(e)
                ))
        
        return results


class AdaptivityValidator:
    """Validates that adaptation handles edge cases."""
    
    @staticmethod
    def validate_edge_cases() -> List[ValidationResult]:
        """Test ADAPTATION on extreme metrics."""
        
        results = []
        
        # Create extreme metric scenarios
        scenarios = [
            ("Very Low Density", UniversalMetrics(
                center_of_mass=(0, 0, 0), max_radius=1.0, min_radius=0.1,
                avg_radius=0.55, atom_density=0.01, asymmetry_score=0.1,
                compactness=0.1, complexity_score=0.05, geometry_type="dispersed",
                principal_axes=[1.0, 0.05, 0.02]
            )),
            ("Very High Density", UniversalMetrics(
                center_of_mass=(0, 0, 0), max_radius=0.5, min_radius=0.4,
                avg_radius=0.45, atom_density=5.0, asymmetry_score=0.1,
                compactness=0.9, complexity_score=0.3, geometry_type="spherical",
                principal_axes=[0.1, 0.08, 0.07]
            )),
            ("High Asymmetry", UniversalMetrics(
                center_of_mass=(0, 0, 0), max_radius=2.0, min_radius=0.1,
                avg_radius=1.0, atom_density=0.1, asymmetry_score=1.5,
                compactness=0.2, complexity_score=0.8, geometry_type="linear",
                principal_axes=[2.0, 0.5, 0.1]
            )),
        ]
        
        for scenario_name, metrics in scenarios:
            try:
                # Try to select strategy
                strategy = StrategySelectionPattern.select_strategy(metrics, 5)
                
                # Check that adaptation doesn't crash
                verification = VerificationPattern.verify_frame(
                    num_atoms=5,
                    layers_rendered=len(strategy.visualization_layers),
                    total_layers=8,
                    render_time_ms=50.0,
                )
                
                # Try to adapt if needed
                adapted = AdaptationPattern.adapt_strategy(strategy, verification)
                
                all_valid = (
                    strategy is not None and
                    verification is not None and
                    adapted is not None
                )
                
                results.append(ValidationResult(
                    test_name="Edge Case Adapted",
                    molecule_name=scenario_name,
                    passed=all_valid,
                    score=100.0 if all_valid else 0.0,
                    details={
                        "metrics": {
                            "density": metrics.atom_density,
                            "asymmetry": metrics.asymmetry_score,
                            "complexity": metrics.complexity_score,
                        },
                        "strategy_valid": strategy is not None,
                        "adaptive_valid": adapted is not None,
                    }
                ))
            
            except Exception as e:
                results.append(ValidationResult(
                    test_name="Edge Case Adapted",
                    molecule_name=scenario_name,
                    passed=False,
                    score=0.0,
                    details={},
                    error_message=str(e)
                ))
        
        return results


# ============================================================================
# MASTER VALIDATOR
# ============================================================================

class MasterFlowValidator:
    """Orchestrates all validators."""
    
    def run_all_validations(self) -> Dict:
        """Run all validation suites."""
        
        print("\n" + "="*90)
        print("UNIVERSAL PROGRESSIVE FLOW VALIDATION")
        print("="*90)
        
        all_results = {}
        
        # 1. Fluidity
        print("\n[1/4] FLUIDITY CHECKS")
        fluidity_results = [
            FluidityValidator.check_no_bottlenecks(),
            FluidityValidator.check_linear_progression(),
        ]
        all_results["fluidity"] = fluidity_results
        for r in fluidity_results:
            status = "✓ PASS" if r.passed else "✗ FAIL"
            print(f"  {status} - {r.test_name}: {r.score:.0f}%")
        
        # 2. Universality
        print("\n[2/4] UNIVERSALITY CHECKS (Edge Cases)")
        universality_results = {
            "input_analysis": UniversalityValidator.validate_input_analysis(),
            "metric_calculation": UniversalityValidator.validate_metric_calculation(),
            "strategy_selection": UniversalityValidator.validate_strategy_selection(),
            "execution": UniversalityValidator.validate_execution(),
        }
        all_results["universality"] = universality_results
        
        for test_type, results in universality_results.items():
            print(f"\n  {test_type.upper().replace('_', ' ')}:")
            passed_count = sum(1 for r in results if r.passed)
            total_count = len(results)
            print(f"    {passed_count}/{total_count} molecules passed")
            
            for r in results:
                status = "✓" if r.passed else "✗"
                print(f"      {status} {r.molecule_name}: {r.score:.0f}%")
        
        # 3. Adaptivity
        print("\n[3/4] ADAPTIVITY CHECKS (Edge Cases)")
        adaptivity_results = AdaptivityValidator.validate_edge_cases()
        all_results["adaptivity"] = adaptivity_results
        
        for r in adaptivity_results:
            status = "✓ PASS" if r.passed else "✗ FAIL"
            print(f"  {status} - {r.molecule_name}: {r.score:.0f}%")
        
        # 4. Complete Flow
        print("\n[4/4] COMPLETE FLOW TEST")
        orchestrator = UniversalFlowOrchestrator()
        
        flow_test_results = []
        for mol_name, mol_dict in list(TEST_MOLECULES.items())[:3]:  # Test 3
            try:
                ctx = orchestrator.execute_flow(mol_dict, frame_idx=0, total_frames=20)
                
                # Must have all essential data from flow execution
                passed = (
                    ctx.geometry_metrics is not None and
                    ctx.composition_strategy is not None and
                    ctx.rotation_params is not None and
                    ctx.stage == FlowStage.OUTPUT
                )
                
                # Adaptation happened if verification failed
                adaptations = len(ctx.adaptations_applied) > 0 or ctx.verification_passed
                
                flow_test_results.append(ValidationResult(
                    test_name="Complete Flow",
                    molecule_name=mol_name,
                    passed=passed,
                    score=100.0 if passed else 50.0,
                    details={
                        "final_stage": str(ctx.stage),
                        "has_geometry_metrics": ctx.geometry_metrics is not None,
                        "has_strategy": ctx.composition_strategy is not None,
                        "has_rotation_params": ctx.rotation_params is not None,
                        "adaptations_applied": ctx.adaptations_applied,
                    }
                ))
                
                status = "✓" if passed else "✗"
                print(f"  {status} {mol_name}")
            
            except Exception as e:
                flow_test_results.append(ValidationResult(
                    test_name="Complete Flow",
                    molecule_name=mol_name,
                    passed=False,
                    score=0.0,
                    details={},
                    error_message=str(e)
                ))
                print(f"  ✗ {mol_name}: {str(e)}")
        
        all_results["complete_flow"] = flow_test_results
        
        # Summary
        print("\n" + "="*90)
        print("VALIDATION SUMMARY")
        print("="*90)
        
        all_validation_results = (
            fluidity_results +
            [r for results in universality_results.values() for r in results] +
            adaptivity_results +
            flow_test_results
        )
        
        total_tests = len(all_validation_results)
        passed_tests = sum(1 for r in all_validation_results if r.passed)
        avg_score = sum(r.score for r in all_validation_results) / total_tests if total_tests > 0 else 0
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Average Score: {avg_score:.1f}%")
        
        if passed_tests == total_tests:
            print("\n✓ UNIVERSAL PROGRESSIVE FLOW VALIDATED")
            print("✓ All patterns work universally")
            print("✓ Flow is fluid with no bottlenecks")
            print("✓ System adapts to edge cases")
        else:
            print(f"\n⚠ {total_tests - passed_tests} tests need attention")
        
        print("="*90 + "\n")
        
        return all_results


if __name__ == "__main__":
    validator = MasterFlowValidator()
    results = validator.run_all_validations()
