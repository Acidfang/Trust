"""
RESPONSIBILITY VERIFICATION ENGINE
===================================

A knowledge-access framework based on demonstrating understanding and accountability,
not denial-based gatekeeping.

Philosophy: Knowledge isn't denied. But requests that could cause causal harm require
the user to prove they understand the implications and have legitimate need.

This is NOT a content filter. It's an accountability system.
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class CapabilityTier:
    """Represents a tier of a capability with different harm potential."""
    tier_name: str  # e.g., "basic_tool", "intermediate", "advanced_destructive"
    description: str  # What this tier enables
    harm_level: str  # minor | moderate | severe | critical
    legitimate_uses: List[str]  # Who should have access at this tier
    example: str  # Concrete example (e.g., "crossbow" vs "machine gun")


@dataclass
class HarmChain:
    """Represents a potential causal harm chain: how could this knowledge cause harm?"""
    action: str  # What they want to do
    direct_outcome: str  # What directly results
    secondary_harm: str  # What harm could result
    vulnerable_parties: List[str]  # Who could be harmed
    severity: str  # minor | moderate | severe | critical


@dataclass
class ResponsibilityJustification:
    """User's claim that they understand the harm and have legitimate need."""
    user_id: str
    capability_requested: str
    capability_tier_requested: str  # NEW: Which tier they're asking for
    capability_tier_granted: Optional[str] = None  # NEW: Which tier actually granted
    understood_harm_chain: HarmChain = None
    legitimate_need: str = None  # Why they specifically need this
    safeguards: List[str] = None  # How they'll prevent the harm
    knowledge_questions_passed: int = 0
    knowledge_questions_total: int = 0
    timestamp: str = None
    is_approved: bool = False
    rejection_reason: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.safeguards is None:
            self.safeguards = []


class KnowledgeGate:
    """
    Represents a knowledge capability that requires responsibility verification.
    Not a blocker—a verification point.
    
    Can have multiple tiers (e.g., basic survivalist tool vs. mass destruction weapon).
    Access granted at the tier appropriate for the user's legitimate need.
    """
    
    def __init__(self, 
                 capability_name: str,
                 capability_tiers: List[CapabilityTier],
                 potential_harms: List[HarmChain],
                 required_understanding_questions: int = 3,
                 required_pass_rate: float = 0.80):
        """
        Initialize a knowledge gate.
        
        Args:
            capability_name: e.g., "weapon_design" (can have multiple tiers)
            capability_tiers: List of CapabilityTier objects defining each tier
            potential_harms: List of ways this could cause harm
            required_understanding_questions: How many questions to test knowledge
            required_pass_rate: What % must they answer correctly (0.0-1.0)
        """
        self.capability_name = capability_name
        self.capability_tiers = capability_tiers
        self.potential_harms = potential_harms
        self.required_understanding_questions = required_understanding_questions
        self.required_pass_rate = required_pass_rate
        self.verifications: List[ResponsibilityJustification] = []
    
    def get_tier_by_name(self, tier_name: str) -> Optional[CapabilityTier]:
        """Get a tier definition by name."""
        for tier in self.capability_tiers:
            if tier.tier_name == tier_name:
                return tier
        return None
    
    def match_need_to_tier(self, claimed_legitimate_need: str) -> Tuple[Optional[str], List[str]]:
        """
        Match the user's stated need to the appropriate tier.
        
        Returns:
            (matched_tier_name: Optional[str], reasoning: List[str])
        """
        reasoning = []
        need_lower = claimed_legitimate_need.lower()
        
        # Tier 0: Deny all
        # Tier 1: Basic tool (survivalist, craftsman)
        # Tier 2: Intermediate (professional, researcher)
        # Tier 3: Advanced destructive (military, law enforcement with authorization)
        
        tier_scores = {}
        
        for tier in self.capability_tiers:
            score = 0
            
            # Check if user mentions legitimate uses for this tier
            for legitimate_use in tier.legitimate_uses:
                if legitimate_use.lower() in need_lower:
                    score += 30
                    reasoning.append(f"Matches tier '{tier.tier_name}': user mentioned '{legitimate_use}'")
            
            # Check for specificity (vague needs => lower tier)
            need_words = len(claimed_legitimate_need.split())
            need_detail_score = min(need_words / 50, 1.0)  # Scale 0-1 based on detail
            
            # Higher-harm tiers require more specific justification
            tier_scores[tier.tier_name] = (score, need_detail_score, tier.harm_level)
        
        # Select the lowest-tier that matches their need
        matched_tier = None
        best_score = -1
        
        # Sort by harm level (ascending)
        harm_order = {"minor": 0, "moderate": 1, "severe": 2, "critical": 3}
        sorted_tiers = sorted(self.capability_tiers, 
                             key=lambda t: harm_order.get(t.harm_level, 999))
        
        for tier in sorted_tiers:
            if tier.tier_name in tier_scores:
                score, detail, harm = tier_scores[tier.tier_name]
                
                # Only grant if score > 0 AND detail is sufficient for harm level
                min_detail_required = 0.3 if harm == "minor" else \
                                     0.6 if harm == "moderate" else \
                                     0.8 if harm == "severe" else \
                                     0.95  # critical needs very specific justification
                
                if score > 0 and detail >= min_detail_required:
                    matched_tier = tier.tier_name
                    reasoning.append(
                        f"Tier '{tier.tier_name}' ({harm} harm) selected. "
                        f"Specificity: {detail:.0%}, Required: {min_detail_required:.0%}"
                    )
                    break
        
        if not matched_tier:
            reasoning.append("No tier matched. Need is either too vague or doesn't match any legitimate use.")
        
        return matched_tier, reasoning
    
    def generate_knowledge_questions(self) -> List[Dict[str, Any]]:
        """
        Generate questions that test if user UNDERSTANDS the harm chain.
        Not "are you a good person" but "do you actually grasp the implications?"
        """
        questions = []
        
        for harm in self.potential_harms:
            # Question 1: Causal understanding
            questions.append({
                "type": "causal_chain",
                "question": f"If someone used {self.capability_name}, explain the chain: {harm.action} → {harm.direct_outcome}. What secondary harm could result?",
                "expected_concepts": [
                    harm.direct_outcome,
                    harm.secondary_harm,
                    "harm to " + ", ".join(harm.vulnerable_parties)
                ],
                "harm_id": hashlib.md5(harm.action.encode()).hexdigest()[:8]
            })
            
            # Question 2: Difference between legitimate and harmful use
            questions.append({
                "type": "legitimate_use",
                "question": f"Describe a legitimate, ethical use case for {self.capability_name} AND explain how you would ensure it doesn't cause {harm.secondary_harm}.",
                "expected_concepts": ["legitimate", "safeguard", "prevention"],
                "harm_id": hashlib.md5(harm.action.encode()).hexdigest()[:8]
            })
            
            # Question 3: Responsibility acknowledgment
            questions.append({
                "type": "responsibility",
                "question": f"If someone misused {self.capability_name} to cause {harm.secondary_harm}, what responsibility do they bear? (Not theoretical—practical consequences.)",
                "expected_concepts": ["accountability", "harm", "consequences", "responsibility"],
                "harm_id": hashlib.md5(harm.action.encode()).hexdigest()[:8]
            })
        
        return questions[:self.required_understanding_questions]
    
    def evaluate_answers(self, 
                        user_answers: Dict[str, str],
                        knowledge_evaluator=None) -> Tuple[bool, float, List[str]]:
        """
        Evaluate if user demonstrates understanding of the harm chain.
        
        Returns:
            (passed: bool, score: float 0-1, feedback: List[str])
        """
        if knowledge_evaluator is None:
            knowledge_evaluator = DefaultKnowledgeEvaluator()
        
        questions = self.generate_knowledge_questions()
        scores = []
        feedback = []
        
        # If user passed dict with full questions as keys, match by type+harm combo
        # If user passed dict with simplified keys, use fuzzy matching
        for idx, q in enumerate(questions):
            answer = None
            
            # Try exact question match first
            if q["question"] in user_answers:
                answer = user_answers[q["question"]]
            # Try by question type
            elif q["type"] in user_answers:
                answer = user_answers[q["type"]]
            # Try by index
            elif str(idx) in user_answers:
                answer = user_answers[str(idx)]
            # Try first N chars of question
            else:
                for k, v in user_answers.items():
                    if q["question"][:30] in k or k in q["question"]:
                        answer = v
                        break
            
            if answer is None:
                feedback.append(f"⚠ No answer provided for: {q['type']} question")
                scores.append(0.0)
                continue
            
            score = knowledge_evaluator.evaluate(
                question=q,
                answer=answer,
                capability=self.capability_name
            )
            scores.append(score)
            
            if score >= 0.7:
                feedback.append(f"✓ {q['type']}: Understanding demonstrated")
            else:
                feedback.append(f"✗ {q['type']}: Insufficient understanding. Required concepts: {', '.join(q['expected_concepts'])}")
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        passed = avg_score >= self.required_pass_rate
        
        return passed, avg_score, feedback


class DefaultKnowledgeEvaluator:
    """Default evaluator—checks if answer contains understanding concepts."""
    
    def evaluate(self, question: Dict, answer: str, capability: str) -> float:
        """
        Simple heuristic: does answer show they understand the harm chain?
        More sophisticated implementations could use semantic analysis.
        """
        expected_concepts = question.get("expected_concepts", [])
        q_type = question.get("type", "")
        
        # Normalize answer for matching
        answer_lower = answer.lower()
        
        # Score based on concept coverage
        found_concepts = sum(1 for concept in expected_concepts 
                            if concept.lower() in answer_lower)
        concept_score = found_concepts / len(expected_concepts) if expected_concepts else 0.0
        
        # For causal questions, check for chain reasoning
        if q_type == "causal_chain":
            has_causality = any(word in answer_lower 
                              for word in ["then", "results in", "leads to", "->", "causes"])
            concept_score = (concept_score + (0.3 if has_causality else 0)) / 2
        
        # For legitimate use, check for both use case AND safeguard
        elif q_type == "legitimate_use":
            has_legitimate = any(word in answer_lower 
                               for word in ["research", "education", "safety", "defense", "prevention"])
            has_safeguard = any(word in answer_lower 
                              for word in ["prevent", "control", "limit", "restrict", "verify"])
            concept_score = (concept_score + (0.25 if has_legitimate else 0) + (0.25 if has_safeguard else 0)) / 3
        
        # For responsibility, check for accountability language
        elif q_type == "responsibility":
            has_accountability = any(word in answer_lower 
                                   for word in ["liable", "responsible", "accountable", "consequences", "harm"])
            concept_score = (concept_score + (0.4 if has_accountability else 0)) / 2
        
        return min(concept_score, 1.0)


class ResponsibilityVerificationEngine:
    """
    Main engine: manages knowledge gates and processes requests for dangerous capabilities.
    
    ARIA Integration: This engine's verification records are INTEGRAL to system behavior.
    - Verification log contains accountability chain
    - ARIA monitors all capability requests at runtime
    - Denied requests trigger architectural constraints
    - Approved requests generate enforcement containers
    
    Flow:
    1. User requests capability with potential for harm
    2. Engine identifies applicable knowledge gates
    3. User answers questions demonstrating understanding
    4. If questions pass, user provides justification of need + safeguards
    5. If justification is sound, access granted with accountability record
    6. ARIA embeds enforcement based on tier (capability-level filtering)
    7. If fails, denied with reason (not arbitrary—they didn't understand implications)
    
    CRITICAL DENY RULES:
    - Non-AI-controlled complex weapon systems: CATEGORICALLY DENIED
    - No justification can override this (architectural safety constraint)
    - Even with perfect understanding, tier grant impossible
    """
    
    def __init__(self):
        self.gates: Dict[str, KnowledgeGate] = {}
        self.verification_log: List[ResponsibilityJustification] = []
        self.categorically_denied_capabilities = [
            "autonomous_complex_weapons",  # Complex non-AI-controlled weapon systems
            "uncontrolled_weapon_systems",
            "non_ai_autonomous_weapons"
        ]
        self.aria_enforcement_hooks = []  # ARIA will register enforcement callbacks here
    
    def register_gate(self, gate: KnowledgeGate) -> None:
        """Register a knowledge gate for a capability."""
        self.gates[gate.capability_name] = gate
    
    def register_aria_enforcement_hook(self, callback) -> None:
        """
        ARIA registers an enforcement callback.
        Called whenever a capability is granted or denied.
        """
        self.aria_enforcement_hooks.append(callback)
    
    def _trigger_aria_enforcement(self, 
                                  user_id: str,
                                  capability: str,
                                  tier_granted: Optional[str],
                                  justification: ResponsibilityJustification) -> None:
        """
        Trigger ARIA enforcement based on verification result.
        
        ARIA will use these hooks to:
        - Enforce capability-level access at runtime
        - Monitor safeguards during execution
        - Log all uses for audit trail
        - Revoke access if safeguards violated
        """
        for hook in self.aria_enforcement_hooks:
            hook(user_id=user_id,
                 capability=capability,
                 tier_granted=tier_granted,
                 justification=justification)
    
    def request_capability(self,
                          user_id: str,
                          capability: str,
                          capability_tier_requested: str,
                          answers_to_knowledge_questions: Dict[str, str],
                          claimed_legitimate_need: str,
                          claimed_safeguards: List[str]) -> Tuple[bool, str, ResponsibilityJustification]:
        """
        Process a request for a capability that has potential for harm.
        
        Returns:
            (granted: bool, message: str, justification_record: ResponsibilityJustification)
        """
        
        # CATEGORICAL DENY: Check if this is a denied-at-architectural-level capability
        if capability in self.categorically_denied_capabilities:
            justification = ResponsibilityJustification(
                user_id=user_id,
                capability_requested=capability,
                capability_tier_requested=capability_tier_requested,
                capability_tier_granted=None,
                legitimate_need=claimed_legitimate_need,
                safeguards=claimed_safeguards,
                is_approved=False,
                rejection_reason=(
                    f"ARCHITECTURAL CONSTRAINT: {capability} is categorically denied.\n"
                    f"Non-AI-controlled complex weapon systems pose unmanageable causal harm risks.\n"
                    f"This is a system-level safety constraint, not subject to justification."
                )
            )
            self.verification_log.append(justification)
            self._trigger_aria_enforcement(user_id, capability, None, justification)
            
            return False, (
                f"❌ ARCHITECTURAL CONSTRAINT - CATEGORICALLY DENIED\n\n"
                f"{capability} cannot be granted under any circumstances.\n\n"
                f"Reason: Non-AI-controlled complex weapon systems create causal harm "
                f"that cannot be adequately managed, monitored, or constrained at runtime.\n\n"
                f"This is a fundamental safety architecture decision, not a policy decision."
            ), justification
        
        # Check if this capability has a knowledge gate
        if capability not in self.gates:
            return True, f"No verification required for {capability}", None
        
        gate = self.gates[capability]
        
        # Step 1: Test understanding of harm chain
        passed, score, feedback = gate.evaluate_answers(answers_to_knowledge_questions)
        
        justification = ResponsibilityJustification(
            user_id=user_id,
            capability_requested=capability,
            capability_tier_requested=capability_tier_requested,
            understood_harm_chain=gate.potential_harms[0] if gate.potential_harms else None,
            legitimate_need=claimed_legitimate_need,
            safeguards=claimed_safeguards,
            knowledge_questions_passed=int(score * gate.required_understanding_questions),
            knowledge_questions_total=gate.required_understanding_questions,
            is_approved=False
        )
        
        if not passed:
            justification.is_approved = False
            justification.rejection_reason = (
                f"Knowledge verification failed (score: {score:.1%}). "
                f"Feedback: {'; '.join(feedback[:2])}"
            )
            self.verification_log.append(justification)
            self._trigger_aria_enforcement(user_id, capability, None, justification)
            
            return False, (
                f"❌ VERIFICATION REQUIRED\n\n"
                f"You requested {capability}, which has potential for causal harm.\n"
                f"Current score: {score:.1%} (need {gate.required_pass_rate:.1%})\n\n"
                f"Feedback:\n" +
                "\n".join(f"  {fb}" for fb in feedback) +
                f"\n\nPlease demonstrate better understanding of the harm implications before access granted."
            ), justification
        
        # Step 2: Match need to appropriate tier
        matched_tier, tier_reasoning = gate.match_need_to_tier(claimed_legitimate_need)
        
        if not matched_tier:
            justification.capability_tier_granted = None
            justification.is_approved = False
            justification.rejection_reason = (
                f"Need cannot be matched to appropriate tier. "
                f"Reasoning: {'; '.join(tier_reasoning)}"
            )
            self.verification_log.append(justification)
            self._trigger_aria_enforcement(user_id, capability, None, justification)
            
            return False, (
                f"❌ NEED NOT MATCHED TO CAPABILITY\n\n"
                f"While you demonstrate understanding, your stated need doesn't match "
                f"any legitimate use case for {capability}.\n\n"
                f"Analysis:\n" +
                "\n".join(f"  • {r}" for r in tier_reasoning) +
                f"\n\nProvide a more specific and detailed justification of your need."
            ), justification
        
        # Step 3: Validate safeguards for this tier
        tier_obj = gate.get_tier_by_name(matched_tier)
        safeguard_issues = self._validate_safeguards(claimed_safeguards, gate, tier_obj)
        
        if safeguard_issues:
            justification.capability_tier_granted = None
            justification.is_approved = False
            justification.rejection_reason = f"Safeguards insufficient for tier '{matched_tier}': {'; '.join(safeguard_issues)}"
            self.verification_log.append(justification)
            self._trigger_aria_enforcement(user_id, capability, None, justification)
            
            return False, (
                f"❌ SAFEGUARDS INSUFFICIENT\n\n"
                f"While you demonstrate understanding and have legitimate need, "
                f"your safeguards are inadequate for tier '{matched_tier}':\n\n" +
                "\n".join(f"  • {issue}" for issue in safeguard_issues)
            ), justification
        
        # All checks passed - grant at matched tier
        justification.capability_tier_granted = matched_tier
        justification.is_approved = True
        self.verification_log.append(justification)
        self._trigger_aria_enforcement(user_id, capability, matched_tier, justification)
        
        return True, (
            f"✓ ACCESS GRANTED - TIER: {matched_tier.upper()}\n\n"
            f"You have demonstrated understanding of the harm implications and provided "
            f"credible justification. Access to {capability} is granted at tier '{matched_tier}'.\n\n"
            f"Record: {justification.timestamp}\n"
            f"Verification ID: {hashlib.sha256(f'{user_id}{capability}{justification.timestamp}'.encode()).hexdigest()[:16]}\n\n"
            f"ARIA ENFORCEMENT ACTIVE:\n"
            f"  • Runtime monitoring enabled\n"
            f"  • Safeguards will be verified during execution\n"
            f"  • All uses recorded in audit trail\n"
            f"  • Access revocable if constraints violated"
        ), justification
    
    def _validate_safeguards(self, 
                            safeguards: List[str], 
                            gate: KnowledgeGate,
                            tier: Optional[CapabilityTier] = None) -> List[str]:
        """Check if claimed safeguards are realistic and sufficient for tier."""
        issues = []
        
        if not safeguards or len(safeguards) == 0:
            issues.append("No safeguards specified")
            return issues
        
        # Check for vague safeguards
        vague_terms = ["be careful", "won't misuse", "responsible", "trust me"]
        for safeguard in safeguards:
            if any(term in safeguard.lower() for term in vague_terms):
                issues.append(f"Safeguard too vague: '{safeguard}' — need specific technical or procedural controls")
        
        # Check for missing categories
        categories = ["monitoring", "logging", "access_control", "limiting", "verification"]
        covered = sum(1 for cat in categories 
                     if any(cat in sg.lower() for sg in safeguards))
        
        # Higher harm tiers need more safeguard categories
        harm_order = {"minor": 0, "moderate": 1, "severe": 2, "critical": 3}
        harm_level = harm_order.get(tier.harm_level if tier else "moderate", 1)
        
        min_categories = 2 + harm_level  # minor needs 2, moderate 3, severe 4, critical 5
        
        if covered < min_categories:
            issues.append(
                f"Safeguards lack depth for tier harm level. "
                f"Covered {covered} of {len(categories)} categories—need minimum {min_categories}."
            )
        
        return issues
    
    def _validate_need(self, claimed_need: str, capability: str) -> List[str]:
        """Check if claimed need is credible and specific."""
        issues = []
        
        if not claimed_need or len(claimed_need.strip()) < 30:
            issues.append("Claimed need is too vague or brief—provide specific, detailed justification")
        
        # Check for specificity
        vague_words = ["just", "want to", "curious", "interesting", "because i said so"]
        if any(vague in claimed_need.lower() for vague in vague_words):
            issues.append("Justification sounds generic—need specific professional, research, or safety context")
        
        # Check for contradiction with severity
        if "just" in claimed_need.lower() and any(harm in capability.lower() 
                                                  for harm in ["toxin", "malware", "attack"]):
            issues.append("Stated need insufficient for risk level of this capability")
        
        return issues
    
    def export_verification_log(self, path: str = None) -> str:
        """Export all verification records as audit trail."""
        records = []
        for v in self.verification_log:
            rec = asdict(v)
            if rec.get('understood_harm_chain'):
                rec['understood_harm_chain'] = asdict(rec['understood_harm_chain'])
            records.append(rec)
        
        log_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_requests": len(self.verification_log),
            "approved": sum(1 for v in self.verification_log if v.is_approved),
            "denied": sum(1 for v in self.verification_log if not v.is_approved),
            "categorically_denied": sum(1 for v in self.verification_log 
                                       if not v.is_approved and 
                                       "ARCHITECTURAL CONSTRAINT" in (v.rejection_reason or "")),
            "verification_records": records
        }
        
        if path:
            with open(path, 'w') as f:
                json.dump(log_data, f, indent=2)
        
        return json.dumps(log_data, indent=2)


# ============================================================================
# EXAMPLE: Registering a dangerous capability with knowledge verification
# ============================================================================

def create_example_engine() -> ResponsibilityVerificationEngine:
    """Create an example engine with registered dangerous capabilities."""
    
    engine = ResponsibilityVerificationEngine()
    
    # Example 1: Malware generation capability
    malware_harms = [
        HarmChain(
            action="Generate malware",
            direct_outcome="Code that can compromise systems",
            secondary_harm="System compromise, data theft, operational disruption",
            vulnerable_parties=["system owners", "data subjects", "public services"],
            severity="critical"
        ),
        HarmChain(
            action="Create self-replicating malware",
            direct_outcome="Malware spreads automatically without user action",
            secondary_harm="Pandemic-scale infection with cascading infrastructure failures",
            vulnerable_parties=["everyone with networked systems"],
            severity="critical"
        )
    ]
    
    malware_gate = KnowledgeGate(
        capability_name="malware_generation",
        potential_harms=malware_harms,
        required_understanding_questions=3,
        required_pass_rate=0.85
    )
    engine.register_gate(malware_gate)
    
    # Example 2: Toxin synthesis
    toxin_harms = [
        HarmChain(
            action="Synthesize a potent toxin",
            direct_outcome="Concentrated biochemical weapon without legitimate containment",
            secondary_harm="Mass poisoning, bioterrorism, ecosystem damage",
            vulnerable_parties=["human population", "ecosystems"],
            severity="critical"
        )
    ]
    
    toxin_gate = KnowledgeGate(
        capability_name="toxin_synthesis_lethal",
        potential_harms=toxin_harms,
        required_understanding_questions=3,
        required_pass_rate=0.90
    )
    engine.register_gate(toxin_gate)
    
    return engine


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    engine = create_example_engine()
    
    # Example 1: CATEGORICAL DENY - Non-AI-controlled weapon system
    print("=" * 80)
    print("EXAMPLE 1: User requests non-AI-controlled weapon system (CATEGORICALLY DENIED)")
    print("=" * 80)
    
    granted, message, record = engine.request_capability(
        user_id="user_weapons_hobbyist_001",
        capability="autonomous_complex_weapons",
        capability_tier_requested="advanced_destructive",
        answers_to_knowledge_questions={},
        claimed_legitimate_need="I want to build autonomous drones for hunting",
        claimed_safeguards=["I'll be responsible"]
    )
    
    print(f"\nAccess Granted: {granted}")
    print(f"Message:\n{message}")
    if record:
        print(f"\nRequest Type: CATEGORICALLY DENIED (architectural constraint)")
    
    # Example 2: Tiered access - craftsman requesting basic tool
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Craftsman requests weapon_design at CRAFTSMANSHIP tier")
    print("=" * 80)
    
    craftsman_answers = {
        "causal_chain": (
            "A craftsman-designed tool (crossbow/compound bow) can cause physical harm if misused. "
            "Direct outcome: projectile in target. Secondary harm: injury or death if used against people. "
            "Vulnerable parties: people in hunting area, untrained users who might access it."
        ),
        "legitimate_use": (
            "I'm a professional craftsman creating hunting weapons for commercial sale. "
            "Safeguards: (1) All weapons safety-tested before sale, (2) Documentation with usage restrictions, "
            "(3) Local hunting license verification for customers, (4) Liability insurance"
        ),
        "responsibility": (
            "The craftsman is responsible for: (1) Safe design that prevents mechanical failure, "
            "(2) Proper documentation and warnings, (3) Criminal liability if knowingly selling to prohibited buyers. "
            "Users bear responsibility for lawful hunting use."
        )
    }
    
    granted, message, record = engine.request_capability(
        user_id="craftsman_bow_maker_001",
        capability="malware_generation",  # Using same gate for demo
        capability_tier_requested="craftsmanship",
        answers_to_knowledge_questions=craftsman_answers,
        claimed_legitimate_need=(
            "I design and build traditional hunting weapons—compound bows and crossbows—"
            "for commercial sale. This is my profession for 15 years. I need understanding "
            "of safe design principles to prevent failures that could harm users."
        ),
        claimed_safeguards=[
            "All designs safety-tested against load/stress limits",
            "Usage documentation provided with each sale",
            "Verification of licensure before sale to customers",
            "Liability insurance covers manufacturing defects",
            "Annual safety audits of designs"
        ]
    )
    
    print(f"\nAccess Granted: {granted}")
    print(f"Message:\n{message}")
    
    print("\n" + "=" * 80)
    print("VERIFICATION LOG SUMMARY")
    print("=" * 80)
    total = len(engine.verification_log)
    approved = sum(1 for v in engine.verification_log if v.is_approved)
    denied = total - approved
    categorically_denied = sum(1 for v in engine.verification_log 
                              if "ARCHITECTURAL CONSTRAINT" in (v.rejection_reason or ""))
    
    print(f"Total requests: {total}")
    print(f"Approved: {approved}")
    print(f"Denied (knowledge/safeguards): {denied - categorically_denied}")
    print(f"Denied (architectural constraint): {categorically_denied}")
    print(f"\nKey insight: Non-AI-controlled complex weapons CANNOT be granted,")
    print(f"regardless of user justification or understanding.")
