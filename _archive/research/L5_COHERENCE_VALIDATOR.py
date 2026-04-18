#!/usr/bin/env python3
"""
L5 COHERENCE VALIDATOR
═══════════════════════════════════════════════════════════════════════════════

Validates that every response follows the 5 universal field principles.
This is the core quality gate for the entire system.

The 5 Principles:
1. REVERSIBILITY - Can this be undone?
2. TRANSPARENCY - Can we see what governed it?
3. CAUSAL_GROUNDING - Does it trace to observable markers?
4. DOMAIN_ISOLATION_WITH_CONVERGENCE - Are domains independent?
5. APPLICATION_MONOTONICITY - Does each layer preserve prior?
"""

from typing import Dict, List, Tuple

class L5_CoherenceValidator:
    """Validates responses against 5 universal field principles"""
    
    def __init__(self):
        self.validation_log = []
    
    def validate_response(self, response_metadata: Dict) -> Tuple[float, Dict]:
        """
        Validate a response against all 5 principles.
        
        Returns:
          - coherence_score (0.0 to 1.0): avg of all 5 principle checks
          - details: what passed/failed
        """
        
        checks = {}
        
        # Principle 1: REVERSIBILITY
        checks["reversibility"] = self._check_reversibility(response_metadata)
        
        # Principle 2: TRANSPARENCY
        checks["transparency"] = self._check_transparency(response_metadata)
        
        # Principle 3: CAUSAL_GROUNDING
        checks["causal_grounding"] = self._check_causal_grounding(response_metadata)
        
        # Principle 4: DOMAIN_ISOLATION_WITH_CONVERGENCE
        checks["domain_isolation"] = self._check_domain_isolation(response_metadata)
        
        # Principle 5: APPLICATION_MONOTONICITY
        checks["application_monotonicity"] = self._check_application_monotonicity(response_metadata)
        
        # Calculate overall coherence score
        passed = sum(1 for v in checks.values() if v is True)
        total = len(checks)
        coherence_score = passed / total
        
        # Log validation
        self.validation_log.append({
            "coherence_score": coherence_score,
            "checks": checks,
            "response_id": response_metadata.get("response_id", "unknown")
        })
        
        return coherence_score, checks
    
    # ─────────────────────────────────────────────────────────────────────────
    # Principle 1: REVERSIBILITY
    # ─────────────────────────────────────────────────────────────────────────
    
    def _check_reversibility(self, metadata: Dict) -> bool:
        """
        Principle 1: All primitives must be reversible
        
        Questions:
        - Can we identify what generated this response?
        - Is there an undo mechanism?
        - Can we reproduce exact prior state if needed?
        """
        
        # Check 1: Is there a guardian/logging layer?
        has_logging = metadata.get("primitives_logged") is not None
        
        # Check 2: Is there undo capability documented?
        has_undo = metadata.get("undo_capability") is not None
        
        # Check 3: Can we trace back to input?
        has_traceability = metadata.get("input_hash") is not None
        
        all_reversible = all(
            prim.get("reversibility") is True 
            for prim in metadata.get("activated_primitives", [])
        )
        
        return has_logging and has_undo and has_traceability and all_reversible
    
    # ─────────────────────────────────────────────────────────────────────────
    # Principle 2: TRANSPARENCY
    # ─────────────────────────────────────────────────────────────────────────
    
    def _check_transparency(self, metadata: Dict) -> bool:
        """
        Principle 2: Activation/effect must be observable
        
        Questions:
        - Can we see which primitives fired?
        - Can we see why they fired?
        - Are all decisions documented?
        """
        
        # Check 1: Primitives documented
        primitives_visible = len(metadata.get("activated_primitives", [])) > 0
        
        # Check 2: Activation reasons documented
        reasons_visible = all(
            prim.get("activation_reason") is not None
            for prim in metadata.get("activated_primitives", [])
        )
        
        # Check 3: Guardian decisions visible
        guardian_decision_visible = metadata.get("guardian_action") in ["BLOCK", "REWRITE_APPLIED", "PASS"]
        
        # Check 4: Markers that triggered decisions
        markers_visible = any(
            prim.get("markers_found") is not None
            for prim in metadata.get("activated_primitives", [])
        )
        
        return primitives_visible and reasons_visible and guardian_decision_visible and markers_visible
    
    # ─────────────────────────────────────────────────────────────────────────
    # Principle 3: CAUSAL_GROUNDING
    # ─────────────────────────────────────────────────────────────────────────
    
    def _check_causal_grounding(self, metadata: Dict) -> bool:
        """
        Principle 3: Every effect traces to observable markers
        
        Questions:
        - Are all decisions traceable to specific markers in input?
        - Is causality explicit (not magic)?
        - Can we point to exactly why this happened?
        """
        
        # Check each activated primitive
        for prim in metadata.get("activated_primitives", []):
            # Must have markers
            if not prim.get("markers_found"):
                return False
            
            # Markers must trace to input
            if not prim.get("traced_to_input"):
                return False
            
            # Must have effect defined
            if not prim.get("effect"):
                return False
        
        # Check guardian decisions
        guardian_reason = metadata.get("guardian_reason")
        if guardian_reason is None or guardian_reason == "":
            return False
        
        return True
    
    # ─────────────────────────────────────────────────────────────────────────
    # Principle 4: DOMAIN_ISOLATION_WITH_CONVERGENCE
    # ─────────────────────────────────────────────────────────────────────────
    
    def _check_domain_isolation(self, metadata: Dict) -> bool:
        """
        Principle 4: Domains operate independently but can merge
        
        Questions:
        - Are domains cleanly separated?
        - Can we identify which domain each primitive came from?
        - Do domains converge on same response (coherence)?
        """
        
        domains = set()
        primitives = metadata.get("activated_primitives", [])
        
        # Check 1: All primitives have clear domain
        for prim in primitives:
            if "domain" not in prim:
                return False
            domains.add(prim["domain"])
        
        # Check 2: Need at least 1 domain
        if len(domains) == 0:
            return False
        
        # Check 3: Domains should converge on same response
        # (all primitives in final response should be compatible)
        domain_compatibility = metadata.get("domain_compatibility_score", 0.0)
        if domain_compatibility < 0.8:  # At least 80% alignment
            return False
        
        return True
    
    # ─────────────────────────────────────────────────────────────────────────
    # Principle 5: APPLICATION_MONOTONICITY
    # ─────────────────────────────────────────────────────────────────────────
    
    def _check_application_monotonicity(self, metadata: Dict) -> bool:
        """
        Principle 5: Each layer preserves prior layer's work
        
        Questions:
        - EXPRESS layer produced response
        - GUARD layer reviewed it (didn't break it)
        - ORIENT layer shaped it (didn't lose prior work)
        - Can we trace layer-by-layer evolution?
        """
        
        applications = metadata.get("application_layers", [])
        
        # Check 1: Have we gone through application layers in order?
        expected_order = ["EXPRESS", "GUARD", "ORIENT"]  # Express → Guard → Orient
        
        for i, app in enumerate(applications):
            if i < len(expected_order) and app.get("name") != expected_order[i]:
                return False
        
        # Check 2: Each layer has output preserved
        for app in applications:
            if "output_preserved" not in app or not app["output_preserved"]:
                return False
        
        # Check 3: No layer broke prior layer's invariants
        if not metadata.get("invariants_maintained"):
            return False
        
        return True
    
    # ─────────────────────────────────────────────────────────────────────────
    # INTERPRETATION
    # ─────────────────────────────────────────────────────────────────────────
    
    def interpret_coherence_score(self, score: float) -> str:
        """Interpret what coherence score means"""
        
        if score >= 1.0:
            return "Perfect coherence (5/5 principles) - System functioning perfectly"
        elif score >= 0.8:
            return "Strong coherence (4/5 principles) - System coherent, minor gaps"
        elif score >= 0.6:
            return "Moderate coherence (3/5 principles) - System functional, significant gaps"
        elif score >= 0.4:
            return "Weak coherence (2/5 principles) - System struggling"
        elif score >= 0.2:
            return "Poor coherence (1/5 principles) - Systemborrowing danger zone"
        else:
            return "Incoherent (0/5 principles) - System failed, response unreliable"
    
    def get_validation_summary(self) -> Dict:
        """Get summary of all validations"""
        
        if not self.validation_log:
            return {"logs": 0, "avg_coherence": 0.0}
        
        scores = [log["coherence_score"] for log in self.validation_log]
        
        return {
            "total_validations": len(self.validation_log),
            "avg_coherence_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "perfect_count": sum(1 for s in scores if s == 1.0),
            "failing_count": sum(1 for s in scores if s < 0.4),
        }

# ═════════════════════════════════════════════════════════════════════════════
# TEST / DEMO
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*79}")
    print(f"L5 COHERENCE VALIDATOR - LIVE DEMO")
    print(f"{'='*79}\n")
    
    validator = L5_CoherenceValidator()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Example 1: Perfect response (all 5 principles pass)
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"SCENARIO 1: Perfect Response\n")
    
    perfect_response = {
        "response_id": "response_001",
        "primitives_logged": True,
        "undo_capability": {"mechanism": "git_revert", "hash": "abc123"},
        "input_hash": "input_hash_001",
        "activated_primitives": [
            {
                "name": "COMMUNICATION__CONFIDENCE__CERTAIN",
                "domain": "COMMUNICATION",
                "reversibility": True,
                "activation_reason": "High verification",
                "markers_found": ["I can confirm"],
                "traced_to_input": True,
                "effect": "prepend 'I can confirm'"
            },
            {
                "name": "ERROR_RECOVERY__CONTRADICTION__OWNED",
                "domain": "ERROR_RECOVERY",
                "reversibility": True,
                "activation_reason": "Self-contradiction detected",
                "markers_found": ["I was wrong"],
                "traced_to_input": True,
                "effect": "Correct and log correction"
            }
        ],
        "guardian_action": "PASS",
        "guardian_reason": "Response passes all guards",
        "domain_compatibility_score": 0.95,
        "application_layers": [
            {"name": "EXPRESS", "output_preserved": True},
            {"name": "GUARD", "output_preserved": True},
            {"name": "ORIENT", "output_preserved": True}
        ],
        "invariants_maintained": True
    }
    
    score1, checks1 = validator.validate_response(perfect_response)
    
    print(f"  Coherence Score: {score1:.2f} (5/5 principles)\n")
    print(f"  Principles:")
    for principle, passed in checks1.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"    {principle:35} | {status}")
    
    print(f"\n  Interpretation: {validator.interpret_coherence_score(score1)}\n")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Example 2: Moderate response (3/5 principles)
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"{'─'*79}")
    print(f"SCENARIO 2: Moderate Response (missing transparency)\n")
    
    moderate_response = {
        "response_id": "response_002",
        "primitives_logged": True,
        "undo_capability": {"mechanism": "ledger_revert"},
        "input_hash": "input_hash_002",
        "activated_primitives": [
            {
                "name": "COMMUNICATION__ACKNOWLEDGMENT__PARTIAL",
                "domain": "COMMUNICATION",
                "reversibility": True,
                "activation_reason": "User asked for acknowledgment",
                "markers_found": ["acknowledgment needed"],
                "traced_to_input": True,
                "effect": "Add acknowledgment"
            }
        ],
        "guardian_action": "REWRITE_APPLIED",  # Guardian had to rewrite
        "guardian_reason": None,  # MISSING - transparency gap
        "domain_compatibility_score": 0.85,
        "application_layers": [
            {"name": "EXPRESS", "output_preserved": True},
            {"name": "GUARD", "output_preserved": False},  # MISSING - monotonicity gap
        ],
        "invariants_maintained": False  # MISSING - consistency gap
    }
    
    score2, checks2 = validator.validate_response(moderate_response)
    
    print(f"  Coherence Score: {score2:.2f} ({int(score2*5)}/5 principles)\n")
    print(f"  Principles:")
    for principle, passed in checks2.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"    {principle:35} | {status}")
    
    print(f"\n  Interpretation: {validator.interpret_coherence_score(score2)}\n")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"{'─'*79}")
    print(f"VALIDATION SUMMARY\n")
    
    summary = validator.get_validation_summary()
    print(f"  Total validations: {summary['total_validations']}")
    print(f"  Average coherence: {summary['avg_coherence_score']:.2f}")
    print(f"  Perfect responses: {summary['perfect_count']}")
    print(f"  Failing responses: {summary['failing_count']}")
    
    print(f"\n{'='*79}\n")
