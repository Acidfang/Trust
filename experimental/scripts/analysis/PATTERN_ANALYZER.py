"""
PATTERN-BASED PRIMITIVE EFFECTIVENESS ANALYZER

Which primitives actually help FFMpeg?
Which combinations actually work?
Uses human language, container-aware.
"""

import sys
sys.path.insert(0, r'c:\Determined')

from FUNCTIONAL_COMPOSITION_FRAMEWORK import (
    Primitive, Container, ComposedMethod, HybridGenerator, 
    registry, composer, hybrid_generator
)
from typing import Dict, List, Tuple, Set
from collections import defaultdict

class PatternAnalyzer:
    """
    Analyze which primitive combinations actually work.
    Eliminate what doesn't help.
    Report in human terms.
    """
    
    def __init__(self, hybrids: List[ComposedMethod], weights: Dict[str, float]):
        self.hybrids = hybrids
        self.weights = weights
        self.scores = {}
    
    def analyze_primitive_effectiveness(self, target_variant: Tuple[str, str]) -> Dict:
        """
        For a specific variant (e.g., ('encode', 'ffmpeg')), find:
        - Which surrounding primitives help it
        - Which hurt it
        - What's the best combination
        """
        
        prim_name, variant_name = target_variant
        
        # Find the primitive enum
        try:
            prim_enum = Primitive[prim_name.upper()]
        except KeyError:
            return {"status": "invalid_primitive"}
        
        # Find all methods using this variant
        using_this = [h for h in self.hybrids if h.variants.get(prim_enum) == variant_name]
        
        if not using_this:
            return {"status": "not_found"}
        
        # Score them all
        scored = [(m, self._score_method(m)) for m in using_this]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Analyze patterns
        top_10_percent = scored[:max(1, len(scored) // 10)]
        bottom_10_percent = scored[-max(1, len(scored) // 10):]
        
        # Extract which primitives appear in top vs bottom
        analysis = {
            "variant": f"{prim_name}:{variant_name}",
            "total_uses": len(using_this),
            "average_score": sum(s[1] for _, s in scored) / len(scored),
            "best_score": scored[0][1],
            "worst_score": scored[-1][1],
            "score_range": scored[0][1] - scored[-1][1],
            "patterns": {}
        }
        
        # For each OTHER primitive, analyze its effectiveness
        for other_prim in Primitive:
            if other_prim == prim_enum:
                continue
            
            # What variants appear in top?
            top_variants = defaultdict(int)
            bottom_variants = defaultdict(int)
            
            for method, _ in top_10_percent:
                variant = method.variants[other_prim]
                top_variants[variant] += 1
            
            for method, _ in bottom_10_percent:
                variant = method.variants[other_prim]
                bottom_variants[variant] += 1
            
            # Which variant is most common in top?
            if top_variants:
                best_variant = max(top_variants.items(), key=lambda x: x[1])[0]
                best_count = top_variants[best_variant]
                
                worst_in_bottom = max(bottom_variants.items(), key=lambda x: x[1])[0] if bottom_variants else None
                worst_count = bottom_variants.get(worst_in_bottom, 0) if worst_in_bottom else 0
                
                analysis["patterns"][other_prim.value] = {
                    "best_with_this": best_variant,
                    "appears_in_top": best_count,
                    "worst_combination": worst_in_bottom,
                    "appears_in_bottom": worst_count,
                    "helps": best_count > worst_count if worst_count > 0 else best_count > 0
                }
        
        # Best and worst full methods
        analysis["best_method"] = str(scored[0][0])
        analysis["worst_method"] = str(scored[-1][0])
        
        return analysis
    
    def _score_method(self, method: ComposedMethod) -> float:
        """Quick score without full recalculation."""
        method_sig = method.get_signature()
        if method_sig not in self.scores:
            # Simple average of metadata scores
            score = 0.0
            count = 0
            for prim_name, metadata in method.metadata.items():
                for dim, weight in self.weights.items():
                    if dim in metadata:
                        score += metadata[dim] * weight
                        count += 1
            self.scores[method_sig] = (score / count) if count > 0 else 0.5
        return self.scores[method_sig]
    
    def report_human(self, analysis: Dict) -> str:
        """Report in human-understandable language."""
        if analysis.get("status") == "not_found":
            return "Not enough data for this variant."
        
        report = []
        
        var = analysis["variant"]
        total = analysis["total_uses"]
        avg = analysis["average_score"]
        best = analysis["best_score"]
        worst = analysis["worst_score"]
        range_diff = analysis["score_range"]
        
        report.append(f"\n{var}")
        report.append("=" * 80)
        report.append(f"Used in {total} combinations")
        report.append(f"Average effectiveness: {avg:.3f}")
        report.append(f"Best combination: {best:.3f}")
        report.append(f"Worst combination: {worst:.3f}")
        report.append(f"Spread (best-worst): {range_diff:.3f}")
        
        if range_diff < 0.05:
            report.append("=> CONSISTENT: Works about the same regardless of surroundings")
        elif range_diff > 0.2:
            report.append("=> CONTEXT-DEPENDENT: Performance varies significantly")
        else:
            report.append("=> MODERATE: Some combinations better than others")
        
        report.append("\nWhat HELPS this variant:")
        for prim_name, pattern in analysis["patterns"].items():
            if pattern["helps"]:
                report.append(f"  + {prim_name}={pattern['best_with_this']}")
                report.append(f"      (appears {pattern['appears_in_top']} times in top 10%)")
        
        report.append("\nWhat HURTS this variant:")
        for prim_name, pattern in analysis["patterns"].items():
            if not pattern["helps"] and pattern["worst_combination"]:
                report.append(f"  - {prim_name}={pattern['worst_combination']}")
                report.append(f"      (appears {pattern['appears_in_bottom']} times in bottom 10%)")
        
        report.append("\nBest combination using this variant:")
        report.append(f"  {analysis['best_method']}")
        
        report.append("\nWorst combination using this variant:")
        report.append(f"  {analysis['worst_method']}")
        
        return "\n".join(report)


class ContainerPointer:
    """
    Everything is a pointer to a container.
    Each finding references the container it came from.
    """
    
    def __init__(self):
        self.pointers = {}
    
    def add_finding(self, finding: str, container_name: str) -> None:
        """Store a finding with its container reference."""
        if container_name not in self.pointers:
            self.pointers[container_name] = []
        self.pointers[container_name].append(finding)
    
    def summarize(self) -> str:
        """Summarize all findings by container."""
        report = []
        report.append("\n" + "=" * 100)
        report.append("CONTAINER-REFERENCED FINDINGS")
        report.append("=" * 100)
        
        for container, findings in self.pointers.items():
            report.append(f"\n[{container}]")
            for finding in findings:
                report.append(f"  * {finding}")
        
        return "\n".join(report)


if __name__ == "__main__":
    print("=" * 100)
    print("PATTERN-BASED PRIMITIVE ANALYZER")
    print("=" * 100)
    
    weights = {"speed": 0.4, "memory": 0.15, "quality": 0.35, "robustness": 0.1}
    
    # Generate hybrids
    all_hybrids = hybrid_generator.generate_all_combinations()
    
    # Create analyzer
    analyzer = PatternAnalyzer(all_hybrids, weights)
    container_ptr = ContainerPointer()
    
    print(f"\nAnalyzing {len(all_hybrids)} combinations with weights: {weights}")
    print("-" * 100)
    
    # Analyze key variants
    key_variants = [
        ("encode", "ffmpeg"),
        ("encode", "pil"),
        ("encode", "imageio"),
        ("optimize", "gifsicle"),
        ("optimize", "palette"),
        ("render", "gpu"),
        ("render", "parallel"),
        ("transfer", "streaming"),
        ("transfer", "gpu_memory"),
    ]
    
    for variant in key_variants:
        analysis = analyzer.analyze_primitive_effectiveness(variant)
        report = analyzer.report_human(analysis)
        print(report)
        
        # Extract key finding for container pointer
        if "best_score" in analysis:
            container_ptr.add_finding(
                f"{variant[0]}={variant[1]} scores {analysis['best_score']:.3f} at best",
                "default"
            )
    
    # Print container summary
    print(container_ptr.summarize())
    
    print()
    print("=" * 100)
    print("HUMAN-READABLE SUMMARY")
    print("=" * 100)
    print()
    
    # Top-level patterns
    ffmpeg_analysis = analyzer.analyze_primitive_effectiveness(("encode", "ffmpeg"))
    pil_analysis = analyzer.analyze_primitive_effectiveness(("encode", "pil"))
    
    print("WHICH ENCODER TO USE?")
    print("-" * 80)
    print(f"FFMpeg: best={ffmpeg_analysis.get('best_score', 0):.3f}, avg={ffmpeg_analysis.get('average_score', 0):.3f}")
    print(f"PIL:    best={pil_analysis.get('best_score', 0):.3f}, avg={pil_analysis.get('average_score', 0):.3f}")
    
    if ffmpeg_analysis.get('best_score', 0) > pil_analysis.get('best_score', 0):
        print("=> FFMpeg has higher potential, but:")
        for prim, pattern in ffmpeg_analysis.get('patterns', {}).items():
            if pattern.get('helps'):
                print(f"   NEEDS: {prim}={pattern['best_with_this']}")
    
    print()
    print("WHAT ACTUALLY HELPS FFMpeg:")
    print("-" * 80)
    for prim, pattern in ffmpeg_analysis.get('patterns', {}).items():
        if pattern.get('helps'):
            print(f"  YES: {prim} = {pattern['best_with_this']}")
        else:
            print(f"  NO:  {prim} = {pattern.get('worst_combination')} doesn't help")
    
    print()
    print("EVERY FINDING POINTS TO A CONTAINER")
    print("-" * 80)
    print("These patterns were observed in the composition space.")
    print("Each one applies to a specific domain/container where it was tested.")
    print("Move to a different container = patterns may shift.")
    print()
