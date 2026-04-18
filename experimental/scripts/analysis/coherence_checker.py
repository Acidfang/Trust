"""
COHERENCE CHECKER - Verify that all decision reasons resonate together

Purpose: AUTOMATED verification that:
- Every decision has a documented reason
- All reasons point in the same direction (are coherent)
- No contradictions exist
- Positive feedback loops are present
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum
import re
from datetime import datetime
from datetime import datetime


class CoherencePrinciple(Enum):
    """Fundamental principles all decisions should serve."""
    TRANSPARENCY = "Transparency (document choices, make visible)"
    GRADIENT_RESOLUTION = "Gradient Resolution (minimize inconsistency)"
    INSTITUTIONAL_MEMORY = "Institutional Memory (preserve knowledge)"


@dataclass
class ReasonAnalysis:
    """Analysis of whether a reason serves coherence principles."""
    decision_id: str
    decision_name: str
    reason: str
    principles_served: Set[CoherencePrinciple]
    confidence: float  # 0.0-1.0
    explanation: str
    is_coherent: bool
    
    def __str__(self) -> str:
        principles = ", ".join(p.value for p in self.principles_served)
        return f"{self.decision_name}: [{self.confidence*100:.0f}% confident] Serves: {principles}"


class ReasonCoherenceAnalyzer:
    """Analyze whether a reason supports coherence principles."""
    
    # Keywords indicating support for each principle
    TRANSPARENCY_KEYWORDS = {
        "document", "record", "visible", "clear", "explicit", "transparent",
        "trace", "audit", "log", "write", "persist", "save"
    }
    
    GRADIENT_KEYWORDS = {
        "resolve", "consistent", "coherent", "align", "reduce", "minimize",
        "principle", "unify", "integrate", "harmonize", "equilibrate"
    }
    
    MEMORY_KEYWORDS = {
        "learn", "knowledge", "understand", "preserve", "retain", "remember",
        "future", "reference", "pattern", "experience", "wisdom", "insight"
    }
    
    @staticmethod
    def analyze_reason(decision_id: str, decision_name: str, reason: str) -> ReasonAnalysis:
        """Analyze whether a reason supports coherence principles."""
        
        principles_served = set()
        
        # Score each principle
        transparency_score = ReasonCoherenceAnalyzer._score_principle(
            reason, ReasonCoherenceAnalyzer.TRANSPARENCY_KEYWORDS
        )
        gradient_score = ReasonCoherenceAnalyzer._score_principle(
            reason, ReasonCoherenceAnalyzer.GRADIENT_KEYWORDS
        )
        memory_score = ReasonCoherenceAnalyzer._score_principle(
            reason, ReasonCoherenceAnalyzer.MEMORY_KEYWORDS
        )
        
        # Determine which principles are served (threshold: 0.3)
        if transparency_score > 0.3:
            principles_served.add(CoherencePrinciple.TRANSPARENCY)
        if gradient_score > 0.3:
            principles_served.add(CoherencePrinciple.GRADIENT_RESOLUTION)
        if memory_score > 0.3:
            principles_served.add(CoherencePrinciple.INSTITUTIONAL_MEMORY)
        
        # Overall confidence
        all_scores = [transparency_score, gradient_score, memory_score]
        confidence = max(all_scores) if all_scores else 0.0
        
        # Determine if coherent (serves at least 1 principle with confidence > 0.3)
        is_coherent = len(principles_served) > 0
        
        explanation = ReasonCoherenceAnalyzer._generate_explanation(
            reason, principles_served, all_scores
        )
        
        return ReasonAnalysis(
            decision_id=decision_id,
            decision_name=decision_name,
            reason=reason,
            principles_served=principles_served,
            confidence=confidence,
            explanation=explanation,
            is_coherent=is_coherent,
        )
    
    @staticmethod
    def _score_principle(reason: str, keywords: Set[str]) -> float:
        """Score how well a reason supports a principle (0.0-1.0)."""
        reason_lower = reason.lower()
        
        # Count keyword matches
        matches = sum(1 for keyword in keywords 
                     if keyword in reason_lower)
        
        # Normalize by reason length and keyword set size
        # Higher density = stronger support
        words = len(reason_lower.split())
        keyword_density = matches / max(1, len(keywords)) / max(1, words)
        
        # Clamp to 0.0-1.0
        return min(1.0, keyword_density * 3)
    
    @staticmethod
    def _generate_explanation(reason: str, principles: Set[CoherencePrinciple], 
                            scores: List[float]) -> str:
        """Generate explanation of coherence analysis."""
        if not principles:
            return "[WARNING] Reason does not clearly support any coherence principle"
        
        principle_names = ", ".join(p.value for p in principles)
        return f"[OK] Reason supports {principle_names}"


class CoherenceReport:
    """Complete coherence analysis across multiple decisions."""
    
    def __init__(self, ledger_name: str):
        self.ledger_name = ledger_name
        self.analyses: List[ReasonAnalysis] = []
        self.generated_at = datetime.now().isoformat()
    
    def add_analysis(self, analysis: ReasonAnalysis):
        """Add decision analysis."""
        self.analyses.append(analysis)
    
    def coherence_score(self) -> float:
        """Overall coherence (0.0-1.0)."""
        if not self.analyses:
            return 0.0
        coherent_count = sum(1 for a in self.analyses if a.is_coherent)
        return coherent_count / len(self.analyses)
    
    def avg_confidence(self) -> float:
        """Average confidence of analyses (0.0-1.0)."""
        if not self.analyses:
            return 0.0
        return sum(a.confidence for a in self.analyses) / len(self.analyses)
    
    def principle_coverage(self) -> Dict[CoherencePrinciple, int]:
        """How many decisions serve each principle."""
        coverage = {principle: 0 for principle in CoherencePrinciple}
        for analysis in self.analyses:
            for principle in analysis.principles_served:
                coverage[principle] += 1
        return coverage
    
    def incoherent_decisions(self) -> List[ReasonAnalysis]:
        """Decisions that don't serve any principle."""
        return [a for a in self.analyses if not a.is_coherent]
    
    def find_contradictions(self) -> List[Tuple[ReasonAnalysis, ReasonAnalysis]]:
        """Find decisions with contradicting reasons."""
        contradictions = []
        
        for i, analysis1 in enumerate(self.analyses):
            for analysis2 in self.analyses[i+1:]:
                # Check for keyword conflicts
                # E.g., one says "consolidate", other says "separate"
                conflicts = {
                    ("consolidate", "separate"),
                    ("simplify", "complex"),
                    ("fast", "safe"),  # Usually contradictory
                }
                
                for conflict_pair in conflicts:
                    if (conflict_pair[0] in analysis1.reason.lower() and
                        conflict_pair[1] in analysis2.reason.lower()):
                        contradictions.append((analysis1, analysis2))
                        break
        
        return contradictions
    
    def find_feedback_loops(self) -> List[List[CoherencePrinciple]]:
        """Find positive feedback loops between principles."""
        # Positive loop: Transparency -> Memory -> Gradient -> Transparency
        transparency_decisions = sum(
            1 for a in self.analyses 
            if CoherencePrinciple.TRANSPARENCY in a.principles_served
        )
        memory_decisions = sum(
            1 for a in self.analyses 
            if CoherencePrinciple.INSTITUTIONAL_MEMORY in a.principles_served
        )
        gradient_decisions = sum(
            1 for a in self.analyses 
            if CoherencePrinciple.GRADIENT_RESOLUTION in a.principles_served
        )
        
        loops = []
        
        # Loop 1: Transparency enables Memory
        if transparency_decisions > 0 and memory_decisions > 0:
            loops.append([
                CoherencePrinciple.TRANSPARENCY,
                CoherencePrinciple.INSTITUTIONAL_MEMORY,
            ])
        
        # Loop 2: Memory enables Gradient
        if memory_decisions > 0 and gradient_decisions > 0:
            loops.append([
                CoherencePrinciple.INSTITUTIONAL_MEMORY,
                CoherencePrinciple.GRADIENT_RESOLUTION,
            ])
        
        # Loop 3: Gradient reinforces Transparency
        if gradient_decisions > 0 and transparency_decisions > 0:
            loops.append([
                CoherencePrinciple.GRADIENT_RESOLUTION,
                CoherencePrinciple.TRANSPARENCY,
            ])
        
        return loops
    
    def generate_report(self) -> str:
        """Generate human-readable coherence report."""
        report = ""
        report += "=" * 80 + "\n"
        report += "COHERENCE ANALYSIS REPORT\n"
        report += f"Ledger: {self.ledger_name}\n"
        report += "=" * 80 + "\n\n"
        
        # Overall score
        report += "COHERENCE SCORE\n"
        report += "-" * 80 + "\n"
        score = self.coherence_score()
        confidence = self.avg_confidence()
        report += f"Overall Coherence: {score*100:.1f}%\n"
        report += f"Average Confidence: {confidence*100:.1f}%\n\n"
        
        # Principle coverage
        report += "PRINCIPLE COVERAGE\n"
        report += "-" * 80 + "\n"
        coverage = self.principle_coverage()
        total_decisions = len(self.analyses)
        for principle, count in coverage.items():
            pct = count / total_decisions * 100 if total_decisions else 0
            report += f"  {principle.value}: {count}/{total_decisions} ({pct:.1f}%)\n"
        report += "\n"
        
        # Incoherent decisions
        incoherent = self.incoherent_decisions()
        if incoherent:
            report += "INCOHERENT DECISIONS (ATTENTION NEEDED)\n"
            report += "-" * 80 + "\n"
            for analysis in incoherent:
                report += f"  FAIL {analysis.decision_name}\n"
                report += f"    Reason: {analysis.reason[:100]}...\n"
                report += f"    {analysis.explanation}\n"
            report += "\n"
        
        # Contradictions
        contradictions = self.find_contradictions()
        if contradictions:
            report += "CONTRADICTIONS DETECTED (CONFLICT)\n"
            report += "-" * 80 + "\n"
            for a1, a2 in contradictions:
                report += f"  FAIL {a1.decision_name} vs {a2.decision_name}\n"
            report += "\n"
        
        # Positive feedback loops
        loops = self.find_feedback_loops()
        if loops:
            report += "POSITIVE FEEDBACK LOOPS DETECTED (REINFORCEMENT)\n"
            report += "-" * 80 + "\n"
            for i, loop in enumerate(loops, 1):
                principles = " -> ".join(p.value.split('(')[0].strip() for p in loop)
                report += f"  OK Loop {i}: {principles}\n"
            report += "\n"
        
        # Decision by decision
        report += "DETAILED ANALYSIS\n"
        report += "-" * 80 + "\n"
        for analysis in self.analyses:
            status = "OK" if analysis.is_coherent else "FAIL"
            report += f"[{status}] {analysis.decision_name} [{analysis.confidence*100:.0f}%]\n"
            report += f"  {analysis.explanation}\n"
        
        return report


# ============================================================================
# RESONANCE CHECKER - Do decisions support each other?
# ============================================================================

class ResonanceChecker:
    """Check if decisions resonate (mutually reinforce) each other."""
    
    @staticmethod
    def check_resonance(decision1_reason: str, decision2_reason: str) -> float:
        """
        Score resonance between two decisions (0.0-1.0).
        
        High resonance: decisions support same principles
        Low resonance: decisions serve different/conflicting principles
        """
        # Analyze both decisions
        from datetime import datetime  # For timestamp
        analysis1 = ReasonCoherenceAnalyzer.analyze_reason(
            "d1", "Decision 1", decision1_reason
        )
        analysis2 = ReasonCoherenceAnalyzer.analyze_reason(
            "d2", "Decision 2", decision2_reason
        )
        
        # Calculate overlap
        shared_principles = analysis1.principles_served & analysis2.principles_served
        all_principles = analysis1.principles_served | analysis2.principles_served
        
        if not all_principles:
            return 0.0
        
        # Resonance = shared / total * (avg confidence)
        resonance = len(shared_principles) / len(all_principles)
        avg_confidence = (analysis1.confidence + analysis2.confidence) / 2
        
        return resonance * avg_confidence
    
    @staticmethod
    def resonance_matrix(analyses: List[ReasonAnalysis]) -> Dict[str, Dict[str, float]]:
        """Generate resonance matrix for all decision pairs."""
        matrix = {}
        
        for i, a1 in enumerate(analyses):
            matrix[a1.decision_id] = {}
            for a2 in analyses[i+1:]:
                resonance = ResonanceChecker.check_resonance(a1.reason, a2.reason)
                matrix[a1.decision_id][a2.decision_id] = resonance
        
        return matrix


# ============================================================================
# DEMONSTRATION
# ============================================================================

from datetime import datetime


def demo_coherence_checker():
    """Demonstrate coherence checking."""
    
    print("=" * 80)
    print("COHERENCE CHECKER - DEMONSTRATION")
    print("=" * 80)
    
    # Sample decisions from Weighted Container System
    decisions = [
        ("1", "Architecture: 7-layer design",
         "7-layer architecture decouples concerns and follows gradient toward minimal inconsistency"),
        
        ("2", "Documentation: Comprehensive approach",
         "Comprehensive documentation preserves knowledge and makes choices transparent"),
        
        ("3", "Technology: Python + no deps",
         "Python is portable, deterministic, and eliminates dependency inconsistencies"),
        
        ("4", "Testing: Demonstration-based verification",
         "Demonstrating working system makes verification tangible and auditable"),
        
        ("5", "Process: Decision Elections Ledger",
         "Recording all decisions with reasons creates institutional memory for future reference"),
    ]
    
    print("\n[STEP 1] Analyzing individual decision reasons...\n")
    
    report = CoherenceReport("weighted_container_system")
    
    for decision_id, name, reason in decisions:
        analysis = ReasonCoherenceAnalyzer.analyze_reason(decision_id, name, reason)
        report.add_analysis(analysis)
        
        print(f"{analysis.decision_id}. {name}")
        print(f"   Confidence: {analysis.confidence*100:.0f}%")
        print(f"   Principles: {', '.join(p.value.split('(')[0] for p in analysis.principles_served)}")
        print(f"   Status: {'Coherent' if analysis.is_coherent else 'Incoherent'}")
        print()
    
    print("\n[STEP 2] Checking for contradictions...\n")
    
    contradictions = report.find_contradictions()
    if contradictions:
        print(f"[WARNING] Found {len(contradictions)} contradictions")
        for a1, a2 in contradictions:
            print(f"  - {a1.decision_name} vs {a2.decision_name}")
    else:
        print("[OK] No contradictions found")
    
    print("\n[STEP 3] Finding positive feedback loops...\n")
    
    loops = report.find_feedback_loops()
    if loops:
        print(f"[OK] Found {len(loops)} positive feedback loops:")
        for i, loop in enumerate(loops, 1):
            principles = " -> ".join(p.value.split('(')[0].strip() for p in loop)
            print(f"  Loop {i}: {principles}")
    else:
        print("No feedback loops detected")
    
    print("\n[STEP 4] Calculating resonance matrix...\n")
    
    # Get analyses in order
    analyses = sorted(report.analyses, key=lambda a: a.decision_id)
    resonance = ResonanceChecker.resonance_matrix(analyses)
    
    print("Decision Resonance Matrix:")
    print("(How much each pair of decisions reinforces each other)")
    print()
    
    for i, (id1, resonances) in enumerate(resonance.items()):
        for id2, score in resonances.items():
            d1_name = next(a.decision_name for a in analyses if a.decision_id == id1)
            d2_name = next(a.decision_name for a in analyses if a.decision_id == id2)
            bar = "=" * int(score * 20)
            print(f"  {d1_name} <-> {d2_name}: {score*100:5.1f}% {bar}")
    
    print("\n[STEP 5] Generating full report...\n")
    
    full_report = report.generate_report()
    print(full_report)
    
    # Summary
    print("\n" + "=" * 80)
    print(f"RESULT: Coherence = {report.coherence_score()*100:.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    demo_coherence_checker()
