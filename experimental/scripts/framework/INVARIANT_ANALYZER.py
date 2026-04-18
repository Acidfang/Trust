"""
INVARIANT PRIMITIVE ANALYZER

The best primitives should be INVARIANT.
- They work well regardless of surrounding context
- They don't depend on specific partners
- They're universally effective

Bad primitives:
- Only work in specific combinations
- Fail when paired differently
- Context-dependent

Find which primitives are actually invariant.
"""

import sys
sys.path.insert(0, r'c:\Determined')

from FUNCTIONAL_COMPOSITION_FRAMEWORK import (
    Primitive, HybridGenerator, registry, hybrid_generator
)
from collections import defaultdict
from typing import Dict, List, Tuple

class InvarianceAnalyzer:
    """
    Find which primitives are INVARIANT (universally effective).
    """
    
    def __init__(self, hybrids: List, weights: Dict[str, float]):
        self.hybrids = hybrids
        self.weights = weights
    
    def _score_simple(self, method) -> float:
        """Quick score."""
        score = 0.0
        count = 0
        for prim_name, metadata in method.metadata.items():
            for dim, weight in self.weights.items():
                if dim in metadata:
                    score += metadata[dim] * weight
                    count += 1
        return (score / count) if count > 0 else 0.5
    
    def analyze_invariance(self) -> Dict:
        """
        For each primitive+variant, measure:
        - How it performs on average
        - How much its performance varies
        - Is it consistent (invariant)?
        """
        
        results = {}
        
        for prim in Primitive:
            results[prim.value] = {}
            
            # Get all variants for this primitive
            variants = registry.list_variants(prim)
            
            for variant_name in variants:
                # Find all methods using this variant
                using_this = [h for h in self.hybrids if h.variants[prim] == variant_name]
                
                if not using_this:
                    continue
                
                # Score each
                scores = [self._score_simple(h) for h in using_this]
                
                avg_score = sum(scores) / len(scores)
                min_score = min(scores)
                max_score = max(scores)
                variance = max_score - min_score
                
                # Coefficient of variation (how consistent?)
                std_dev = (sum((s - avg_score) ** 2 for s in scores) / len(scores)) ** 0.5
                
                results[prim.value][variant_name] = {
                    "usage_count": len(using_this),
                    "avg_score": avg_score,
                    "min_score": min_score,
                    "max_score": max_score,
                    "variance": variance,
                    "std_dev": std_dev,
                    "is_invariant": variance < 0.08,  # Less than 8% variance = invariant
                    "consistency": 1.0 - min(1.0, variance / 0.5)  # 0-1 scale
                }
        
        return results
    
    def find_best_invariant_per_primitive(self, analysis: Dict) -> Dict:
        """
        For each primitive, which variant is invariant AND has best average score?
        """
        best = {}
        
        for prim_name, variants in analysis.items():
            invariant_variants = {
                v_name: v_info for v_name, v_info in variants.items()
                if v_info["is_invariant"]
            }
            
            if invariant_variants:
                # Pick the one with best average score
                best_variant = max(
                    invariant_variants.items(),
                    key=lambda x: x[1]["avg_score"]
                )
                best[prim_name] = best_variant
            else:
                # No invariant variant, pick the most consistent one
                most_consistent = max(
                    variants.items(),
                    key=lambda x: x[1]["consistency"]
                )
                best[prim_name] = most_consistent
        
        return best
    
    def report(self, analysis: Dict, best: Dict) -> str:
        """Generate human-readable report."""
        lines = []
        
        lines.append("\n" + "=" * 100)
        lines.append("INVARIANT PRIMITIVE ANALYSIS")
        lines.append("=" * 100)
        
        lines.append("\nBEST INVARIANT PRIMITIVES (work well everywhere):")
        lines.append("-" * 100)
        
        for prim_name, (variant_name, info) in best.items():
            invariant_status = "INVARIANT" if info["is_invariant"] else "variable"
            lines.append(f"\n{prim_name.upper()}")
            lines.append(f"  Best choice: {variant_name}")
            lines.append(f"  Avg score: {info['avg_score']:.3f}")
            lines.append(f"  Score range: {info['min_score']:.3f} - {info['max_score']:.3f} (variance: {info['variance']:.3f})")
            lines.append(f"  Consistency: {info['consistency']:.1%}")
            lines.append(f"  Status: {invariant_status}")
            lines.append(f"  Used in {info['usage_count']} combinations")
        
        lines.append("\n" + "-" * 100)
        lines.append("INVARIANT vs VARIABLE PRIMITIVES:")
        lines.append("-" * 100)
        
        for prim_name, variants in analysis.items():
            lines.append(f"\n{prim_name}:")
            
            invariant_list = []
            variable_list = []
            
            for v_name, v_info in sorted(variants.items(), key=lambda x: x[1]["avg_score"], reverse=True):
                if v_info["is_invariant"]:
                    invariant_list.append(f"{v_name} (avg:{v_info['avg_score']:.3f})")
                else:
                    variable_list.append(f"{v_name} (avg:{v_info['avg_score']:.3f}, var:{v_info['variance']:.3f})")
            
            if invariant_list:
                lines.append(f"  INVARIANT (use these): {', '.join(invariant_list)}")
            if variable_list:
                lines.append(f"  VARIABLE (avoid): {', '.join(variable_list[:3])}")  # Top 3
        
        lines.append("\n" + "=" * 100)
        lines.append("INTERPRETATION:")
        lines.append("=" * 100)
        lines.append("\nInvariant primitives are RELIABLE:")
        lines.append("  - Work well with any surrounding context")
        lines.append("  - Don't depend on specific partners")
        lines.append("  - Score stays consistent across combinations")
        
        lines.append("\nVariable primitives are RISKY:")
        lines.append("  - Only work in specific combinations")
        lines.append("  - Performance sinks with wrong partners")
        lines.append("  - Not worth using unless context is perfect")
        
        return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 100)
    print("INVARIANT PRIMITIVE ANALYZER")
    print("=" * 100)
    
    weights = {"speed": 0.4, "memory": 0.15, "quality": 0.35, "robustness": 0.1}
    
    # Generate hybrids
    all_hybrids = hybrid_generator.generate_all_combinations()
    print(f"Analyzing {len(all_hybrids)} combinations...")
    
    analyzer = InvarianceAnalyzer(all_hybrids, weights)
    analysis = analyzer.analyze_invariance()
    best = analyzer.find_best_invariant_per_primitive(analysis)
    
    report = analyzer.report(analysis, best)
    print(report)
    
    # Specific finding about each primitive
    print("\n" + "=" * 100)
    print("KEY FINDINGS:")
    print("=" * 100)
    
    # Show the "canonical" best method using only invariant primitives
    invariant_variants = {
        prim_name: variant_name 
        for prim_name, (variant_name, _) in best.items()
    }
    
    print(f"\nThe MOST INVARIANT COMPOSITION (best primitives everywhere):")
    composition = " > ".join(f"{k}({v})" for k, v in invariant_variants.items())
    print(f"  {composition}")
    
    print(f"\nThis composition should:")
    print(f"  - Work well regardless of scale (small/medium/large)")
    print(f"  - Work well regardless of domain (GIF/video/scientific)")
    print(f"  - Not depend on specific context")
    print(f"  - Be RELIABLY EFFECTIVE")
