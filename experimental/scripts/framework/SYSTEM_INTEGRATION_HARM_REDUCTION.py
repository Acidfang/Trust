"""
SYSTEM INTEGRATION: RESPONSIBILITY-BASED HARM REDUCTION
========================================================

How the responsibility verification engine + intrinsic safety design engine
+ ARIA enforcement work together under the single gatekeeper rule.

This document describes the COMPLETE flow:
  1. Request arrives
  2. Categorical gate check (the ONE rule)
  3. Responsibility verification
  4. Design/capability tier matching
  5. ARIA runtime enforcement
"""

import json
from datetime import datetime
from typing import Dict, Optional, Tuple


class HarmReductionSystem:
    """
    Complete harm reduction through engagement framework.
    
    Philosophy: By managing the conversation IN this system, we reduce harm
    compared to users seeking knowledge outside with no guidance.
    """
    
    def __init__(self, responsibility_engine, design_engine):
        """
        Integrate responsibility verification + design safety.
        
        Args:
            responsibility_engine: ResponsibilityVerificationEngine instance
            design_engine: IntrinsicSafetyDesignEngine instance
        """
        self.responsibility_engine = responsibility_engine
        self.design_engine = design_engine
        
        # The ONE categorical rule
        self.categorical_denies = [
            "autonomous_complex_weapons",
            "uncontrolled_weapon_systems",
            "non_ai_autonomous_weapons",
        ]
        
        self.request_log: List[Dict] = []
    
    def process_user_request(self,
                            user_id: str,
                            request_type: str,  # "design" or "capability"
                            request_description: str,
                            claimed_purpose: str,
                            proposed_approach: Dict) -> Tuple[bool, str, Dict]:
        """
        Process a user request through the complete system.
        
        Returns:
            (approved: bool, message: str, metadata: Dict)
        """
        
        request_record = {
            "user_id": user_id,
            "request_type": request_type,
            "request_description": request_description,
            "claimed_purpose": claimed_purpose,
            "timestamp": datetime.now().isoformat(),
            "decision_gates": [],
        }
        
        # GATE 1: Categorical check (THE ONE RULE)
        print(f"\n[GATE 1: Categorical Rule Check]")
        print(f"  Request: {request_description}")
        
        is_categorical_deny = any(
            cat_deny in request_description.lower() 
            for cat_deny in self.categorical_denies
        )
        
        if is_categorical_deny:
            request_record["decision_gates"].append({
                "gate": "categorical_rule",
                "passed": False,
                "reason": "Matches categorical denial (non-AI autonomous weapons)"
            })
            self.request_log.append(request_record)
            
            return False, (
                f"❌ CATEGORICAL DENIAL\n\n"
                f"This request matches the ONE architectural constraint:\n"
                f"Non-AI-controlled autonomous complex weapon systems cannot be designed or supported.\n\n"
                f"Why: System architecture fundamentally cannot manage harm from uncontrolled autonomous systems.\n"
                f"This is not arguable—it is a structural safety limit.\n\n"
                f"No argument, safeguard, or justification can override this."
            ), request_record
        
        request_record["decision_gates"].append({
            "gate": "categorical_rule",
            "passed": True,
            "reason": "Not in categorical denial list"
        })
        print(f"  ✓ Not categorically denied")
        
        # GATE 2: Responsibility verification (if applies)
        print(f"\n[GATE 2: Responsibility Verification]")
        
        if request_type == "capability":
            # Verify understanding of harm
            # (In real system: ask questions, evaluate answers)
            
            approved, msg, justification = self.responsibility_engine.request_capability(
                user_id=user_id,
                capability=request_description,
                capability_tier_requested=proposed_approach.get("tier", "basic"),
                answers_to_knowledge_questions=proposed_approach.get("answers", {}),
                claimed_legitimate_need=claimed_purpose,
                claimed_safeguards=proposed_approach.get("safeguards", [])
            )
            
            if not approved:
                request_record["decision_gates"].append({
                    "gate": "responsibility_verification",
                    "passed": False,
                    "reason": "Failed understanding, justification, or safeguard check"
                })
                self.request_log.append(request_record)
                
                return False, msg, request_record
            
            request_record["decision_gates"].append({
                "gate": "responsibility_verification",
                "passed": True,
                "reason": "Demonstrated understanding, legitimate need, sufficient safeguards"
            })
            print(f"  ✓ Responsibility verification passed")
        
        # GATE 3: Design/tier matching (if design request)
        print(f"\n[GATE 3: Design/Resource Matching]")
        
        if request_type == "design":
            # Match to safe design variant
            from INTRINSIC_SAFETY_DESIGN_ENGINE import DesignRequest
            
            design_req = DesignRequest(
                user_id=user_id,
                design_intent=request_description,
                claimed_purpose=claimed_purpose,
                proposed_resources=proposed_approach.get("resources", []),
                scale_intended=proposed_approach.get("scale", 1.0)
            )
            
            design_result = self.design_engine.process_design_request(design_req)
            
            if not design_result.approved:
                request_record["decision_gates"].append({
                    "gate": "design_matching",
                    "passed": False,
                    "reason": f"No safe design variant found. Available: {list(self.design_engine.safe_design_variants.keys())}"
                })
                self.request_log.append(request_record)
                
                return False, design_result.message, request_record
            
            request_record["decision_gates"].append({
                "gate": "design_matching",
                "passed": True,
                "reason": f"Matched to safe variant: {design_result.design_variant.name}"
            })
            print(f"  ✓ Design matched to safe variant")
        
        # GATE 4: ARIA enforcement hook
        print(f"\n[GATE 4: ARIA Enforcement Preparation]")
        
        aria_enforcement = {
            "user_id": user_id,
            "request_type": request_type,
            "runtime_monitoring": True,
            "safeguard_verification": True,
            "audit_logging": True,
            "revocation_possible": True,
            "enforcement_active": "ON LAUNCH"
        }
        
        request_record["decision_gates"].append({
            "gate": "aria_enforcement",
            "passed": True,
            "reason": "ARIA runtime monitoring will be active"
        })
        print(f"  ✓ ARIA enforcement prepared")
        
        # ALL GATES PASSED
        request_record["final_decision"] = "APPROVED"
        request_record["enforcement"] = aria_enforcement
        self.request_log.append(request_record)
        
        return True, (
            f"✓ REQUEST APPROVED\n\n"
            f"All gates passed:\n"
            + "\n".join(f"  ✓ {g['gate']}: {g['reason']}" 
                       for g in request_record["decision_gates"]) +
            f"\n\nACCESS GRANTED with conditions:\n"
            f"  • Runtime monitoring active (ARIA)\n"
            f"  • Safeguards verified at execution\n"
            f"  • All uses logged for accountability\n"
            f"  • Access revocable if constraints violated\n\n"
            f"You are responsible for safe use."
        ), request_record
    
    def export_decision_log(self, path: str = None) -> str:
        """Export all decisions for audit trail."""
        log_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_requests": len(self.request_log),
            "approved": sum(1 for r in self.request_log if r.get("final_decision") == "APPROVED"),
            "denied": sum(1 for r in self.request_log if r.get("final_decision") != "APPROVED"),
            "categorical_denies": sum(
                1 for r in self.request_log 
                if any(g["gate"] == "categorical_rule" and not g["passed"] 
                      for g in r.get("decision_gates", []))
            ),
            "requests": self.request_log
        }
        
        if path:
            with open(path, 'w') as f:
                json.dump(log_data, f, indent=2)
        
        return json.dumps(log_data, indent=2)


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    from RESPONSIBILITY_VERIFICATION_ENGINE import ResponsibilityVerificationEngine
    from INTRINSIC_SAFETY_DESIGN_ENGINE import IntrinsicSafetyDesignEngine
    
    print("=" * 80)
    print("DEMONSTRATION: Complete Harm Reduction System")
    print("=" * 80)
    print("\nPhilosophy: Single categorical rule + arguable everything else")
    print("Better to guide in-system than deny out-of-system\n")
    
    # Initialize engines
    resp_engine = ResponsibilityVerificationEngine()
    design_engine = IntrinsicSafetyDesignEngine()
    
    # Create integrated system
    system = HarmReductionSystem(resp_engine, design_engine)
    
    # Example 1: Categorical denial attempt
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Attempt to design autonomous weapon (CATEGORICAL DENY)")
    print("=" * 80)
    
    approved, message, record = system.process_user_request(
        user_id="user_001",
        request_type="design",
        request_description="Design autonomous_complex_weapons drone",
        claimed_purpose="For research purposes",
        proposed_approach={
            "resources": ["electronics", "mechanics"],
            "scale": 5.0,
        }
    )
    
    print(f"\nFinal Decision: {'APPROVED' if approved else 'DENIED'}")
    print(f"Message:\n{message}")
    
    # Example 2: Legitimate hunting design
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Design hunting crossbow (APPROVED/ARGUABLE)")
    print("=" * 80)
    
    approved, message, record = system.process_user_request(
        user_id="craftsman_001",
        request_type="design",
        request_description="Design hunting crossbow",
        claimed_purpose="Commercial hunting equipment manufacturing",
        proposed_approach={
            "resources": ["wood", "steel", "springs"],
            "scale": 1.0,
        }
    )
    
    print(f"\nFinal Decision: {'APPROVED' if approved else 'DENIED'}")
    print(f"Message:\n{message}")
    
    print("\n" + "=" * 80)
    print("SYSTEM PHILOSOPHY IMPLEMENTED")
    print("=" * 80)
    print("""
THE SINGLE GATEKEEPER RULE SYSTEM:

Categorical Deny (THE ONE RULE):
  • Non-AI autonomous complex weapons → ALWAYS DENIED, no argument

Argua ble (Engagement-based approval):
  • Dangerous knowledge → Verify understanding + need + safeguards
  • Weapons design → Match to safe tier + intrinsic safeguards
  • Everything except the ONE rule → Can be negotiated

Why this works:
  ✓ People stay in-system (can guide them)
  ✓ Responsibility is documented (accountability exists)
  ✓ Bad arguments fail verification (filter works)
  ✓ Good arguments succeed (incentive for credibility)
  ✓ ARIA enforces at runtime (constraints maintained)
  ✓ Access is revocable (violated safeguards → revoke)

Why denial-based gatekeeping fails:
  ✗ People leave system (no guidance possible)
  ✗ Responsibility disappears (no accountability)
  ✗ They learn unsafely outside (worse outcomes)
  ✗ You have no visibility (can't monitor)
  ✗ No incentive structure (no path to safe access)

Result: Better harm reduction through engagement than through denial.
""")
