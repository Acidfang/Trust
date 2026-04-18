#!/usr/bin/env python3
"""
CORE SYSTEMS INTEGRATION
═══════════════════════════════════════════════════════════════════════════════

Orchestrates all 4 core systems:
  1. L1: Primitive field activation (already in analyze_query_semantics)
  2. L5: Coherence validation
  3. L7: Meta-coherence detectors (emergent patterns)
  4. L4: Emergence telemetry logging
"""

from typing import Dict, List, Tuple
from datetime import datetime

# Import core systems
from L5_COHERENCE_VALIDATOR import L5_CoherenceValidator
from META_COHERENCE_PRIMITIVES_L7 import META_COHERENCE_PRIMITIVES
from EMERGENCE_TELEMETRY import EmergenceTelemetry


class CoreSystemsIntegration:
    """Orchestrates L1 → L7 → L5 → L4 pipeline"""
    
    def __init__(self):
        self.validator = L5_CoherenceValidator()
        self.telemetry = EmergenceTelemetry()
        self.conversation_id = None
        self.turn_number = 0
    
    def set_conversation_context(self, conversation_id: str):
        """Set context for telemetry tracking"""
        self.conversation_id = conversation_id
        self.turn_number = 0
    
    def process_response(self,
                        response_text: str,
                        activated_primitives: List[Dict],
                        guardian_metadata: Dict,
                        field_coherence: float) -> Tuple[float, Dict, List[str]]:
        """
        Process response through L5 and L7 systems
        
        Returns:
          - coherence_score (0.0-1.0)
          - quality_metadata (detailed checks)
          - detected_patterns (which L7 patterns fired)
        """
        
        self.turn_number += 1
        
        # ─────────────────────────────────────────────────────────
        # STEP 1: Prepare metadata for validation
        # ─────────────────────────────────────────────────────────
        
        response_metadata = {
            "response_text": response_text,
            "response_length": len(response_text),
            "activated_primitives": activated_primitives,
            "primitives_count": len(activated_primitives),
            "primitives_logged": activated_primitives is not None,
            "guardian_action": guardian_metadata.get("action"),
            "guardian_decision_visible": guardian_metadata.get("action") in ["BLOCK", "REWRITE_APPLIED", "PASS"],
            "field_coherence": field_coherence,
            "response_id": f"{self.conversation_id}_turn{self.turn_number}",
            "timestamp": datetime.now().isoformat(),
        }
        
        # Add undo capability tracking
        response_metadata["undo_capability"] = {
            "timestamp": datetime.now().isoformat(),
            "can_revert": True,
            "mechanism": "ledger_entry_reversible"
        }
        
        # Add input traceability  
        response_metadata["input_hash"] = hash(
            response_text[:100] + str(len(activated_primitives))
        )
        
        # ─────────────────────────────────────────────────────────
        # STEP 2: L5 Coherence Validator
        # ─────────────────────────────────────────────────────────
        
        coherence_score, principle_checks = self.validator.validate_response(
            response_metadata
        )
        
        quality_metadata = {
            "coherence_score": coherence_score,
            "principle_checks": principle_checks,
            "reversibility": principle_checks.get("reversibility"),
            "transparency": principle_checks.get("transparency"),
            "causal_grounding": principle_checks.get("causal_grounding"),
            "domain_isolation": principle_checks.get("domain_isolation"),
            "application_monotonicity": principle_checks.get("application_monotonicity"),
        }
        
        # ─────────────────────────────────────────────────────────
        # STEP 3: L7 Meta-Coherence Detectors
        # ─────────────────────────────────────────────────────────
        
        detected_patterns = self._detect_emergent_patterns(
            response_metadata,
            coherence_score,
            activated_primitives
        )
        
        # ─────────────────────────────────────────────────────────
        # STEP 4: L4 Telemetry Logging
        # ─────────────────────────────────────────────────────────
        
        for pattern_name in detected_patterns:
            contributing_prims = [p["name"] for p in activated_primitives[:5]]
            self.telemetry.log_pattern_activation(
                conversation_id=self.conversation_id,
                turn=self.turn_number,
                pattern_name=pattern_name,
                confidence=coherence_score,
                contributing_primitives=contributing_prims
            )
        
        return coherence_score, quality_metadata, detected_patterns
    
    def _detect_emergent_patterns(self,
                                 response_metadata: Dict,
                                 coherence_score: float,
                                 activated_primitives: List[Dict]) -> List[str]:
        """Detect which L7 patterns are firing"""
        
        patterns_fired = []
        primitives_by_domain = {}
        
        # Organize primitives by domain
        for prim in activated_primitives:
            domain = prim.get("domain", "UNKNOWN")
            if domain not in primitives_by_domain:
                primitives_by_domain[domain] = []
            primitives_by_domain[domain].append(prim)
        
        # ─────────────────────────────────────────────────────────
        # Pattern 1: COHERENCE_GRAVITY
        # ─────────────────────────────────────────────────────────
        
        if coherence_score > 0.85:
            # Multiple domains activated on same query?
            if len(primitives_by_domain) >= 3:
                patterns_fired.append("COHERENCE_GRAVITY")
        
        # ─────────────────────────────────────────────────────────
        # Pattern 2: LEARNING_ACCELERATION
        # ─────────────────────────────────────────────────────────
        
        # If LEARNING primitives + ERROR_RECOVERY + quick response = learning acceleration
        learning_prims = [p for p in activated_primitives 
                         if "LEARNING" in p.get("domain", "")]
        recovery_prims = [p for p in activated_primitives 
                         if "ERROR" in p.get("name", "")]
        
        if learning_prims and recovery_prims and len(activated_primitives) <= 6:
            patterns_fired.append("LEARNING_ACCELERATION")
        
        # ─────────────────────────────────────────────────────────
        # Pattern 3: TRUST_EMERGENCE
        # ─────────────────────────────────────────────────────────
        
        # If ERROR_RECOVERY + RELATIONSHIPS + high coherence = trust forming
        relationship_prims = [p for p in activated_primitives 
                            if "RELATIONSHIP" in p.get("domain", "")]
        
        if recovery_prims and relationship_prims and coherence_score > 0.75:
            patterns_fired.append("TRUST_EMERGENCE")
        
        # ─────────────────────────────────────────────────────────
        # Pattern 4: CREATIVE_FREEDOM
        # ─────────────────────────────────────────────────────────
        
        # If CONTINUITY + BEHAVIOUR__INQUIRY + novel response = creative
        continuity_prims = [p for p in activated_primitives 
                          if "CONTINUITY" in p.get("domain", "")]
        inquiry_prims = [p for p in activated_primitives 
                        if "INQUIRY" in p.get("name", "")]
        
        if continuity_prims and inquiry_prims and len(activated_primitives) >= 5:
            patterns_fired.append("CREATIVE_FREEDOM")
        
        # ─────────────────────────────────────────────────────────
        # Check for Authenticity Loop
        # ─────────────────────────────────────────────────────────
        
        if len(patterns_fired) == 4:
            patterns_fired.append("AUTHENTICITY_LOOP")
        
        return patterns_fired
    
    def get_telemetry_stats(self) -> Dict:
        """Get current telemetry statistics"""
        return self.telemetry.get_pattern_statistics()
    
    def get_conversation_arc(self) -> Dict:
        """Get pattern emergence arc for current conversation"""
        if self.conversation_id:
            return self.telemetry.get_conversation_arc(self.conversation_id)
        return None
