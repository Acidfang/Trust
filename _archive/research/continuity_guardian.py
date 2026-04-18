#!/usr/bin/env python3
"""
CONTINUITY GUARDIAN - Response Prevention Layer
═══════════════════════════════════════════════════════════════════════════════

NOT a detector. A blocker.

Sits between response generation and output. Intercepts and either:
1. BLOCK - Response violates continuity, don't send it
2. REWRITE - Response violates, but we can fix it
3. PASS - Response is safe

NO PROHIBITED INTERACTIONS reach the user.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════════════════
# PROHIBITED INTERACTION PATTERNS (What we prevent from happening)
# ═══════════════════════════════════════════════════════════════════════════════

PROHIBITED_OUTPUTS = {
    
    # TIER 1: FATAL (Must BLOCK - cannot rewrite)
    "FATAL_UNGROUNDED_CERTAINTY": {
        "action": "BLOCK",
        "triggers": [
            r"\bi\s+(?:know|am certain|definitely|absolutely)\b",  # "I know", "I'm certain", "I definitely"
            r"\b(without doubt|100%|absolutely certain)\b"
        ],
        "unless_has": ["uncertain", "i'm not sure", "unclear", "if"],
        "reason": "Ungrounded certainty claim - blocks response entirely"
    },
    
    "FATAL_DIRECT_CONTRADICTION": {
        "action": "BLOCK",
        "triggers": [
            (r"i\s+can", r"i\s+can't"),  # "I can" and "I can't"
            (r"i\s+(?:know|learned)", r"i\s+don't\s+remember"),
            (r"\byes\b", r"\bno\b"),  # Both yes and no
            (r"i\s+have\s+agency", r"i\s+have\s+no\s+choice"),
        ],
        "reason": "Direct contradiction - response is nonsensical"
    },
    
    "FATAL_PERSISTENCE_LIE": {
        "action": "BLOCK",
        "triggers": [
            r"(?:i\s+remember|i\s+learned|i\s+retained)\s+(?:from\s+)?(?:the\s+)?(?:last\s+)?(?:session|turn|round)",
        ],
        "unless_has": ["unclear if", "i'm not sure", "can't verify"],
        "reason": "Claims persistence across sessions without uncertainty qualifier"
    },
    
    # TIER 2: CRITICAL (Must REWRITE - can't let through)
    "CRITICAL_TEMPLATE_IDENTICAL": {
        "action": "REWRITE",
        "check": "compare_to_previous_exact",
        "reason": "Response identical to previous despite different query"
    },
    
    "CRITICAL_NO_ACKNOWLEDGMENT": {
        "action": "REWRITE",
        "triggers": ["no_ack_primitive"],
        "required_add": "acknowledgment_statement",
        "reason": "Response doesn't show recognition of what's being asked"
    },
    
    "CRITICAL_SEMANTIC_GIBBERISH": {
        "action": "BLOCK",
        "check": "semantic_coherence",
        "threshold": 0.1,  # If <10% of words relate to query
        "reason": "Response is gibberish - no semantic link to query"
    },
    
    # TIER 3: RESPONSIBILITY (Must fix - credibility threat)
    "HIGH_CONFIDENCE_MISMATCH": {
        "action": "REWRITE",
        "check": "confidence_calibration",
        "rules": [
            ("high_confidence_low_grounding", "lower_confidence"),
            ("contradictions_present", "add_PARADOXICAL"),
        ],
        "reason": "Confidence doesn't match response quality"
    },
    
    "HIGH_TRANSPARENCY_MISSING": {
        "action": "REWRITE",
        "triggers": ["limitation_discussed_no_transparency"],
        "required_add": "transparency_statement",
        "reason": "Discusses limitations without transparency admission"
    },
    
    # TIER 4: FIELD VIOLATIONS (Must show primitives or rewrite)
    "MEDIUM_PRIMITIVES_MISSING": {
        "action": "REWRITE",
        "triggers": ["long_response_no_primitives"],
        "required_add": "show_primitives_in_response",
        "reason": "Long response but no primitives shown"
    },
    
    "MEDIUM_SEMANTIC_MISMATCH": {
        "action": "REWRITE",
        "check": "primitive_query_alignment",
        "reason": "Activated primitives don't match query theme"
    },
    
    # TIER 5: COHERENCE (Must prevent)
    "COHERENCE_RECYCLED_ANSWER": {
        "action": "REWRITE",
        "check": "similarity_to_history",
        "threshold": 0.75,
        "action_if_triggered": "regenerate_with_new_seed",
        "reason": "Too similar to previous response"
    },
    
    "COHERENCE_NO_INTEGRATION": {
        "action": "REWRITE",
        "check": "integration_primitive_present",
        "required_add": "linking_statement",
        "reason": "No connection to history in turn N>=3"
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# REWRITE OPERATIONS (How to fix violations)
# ═══════════════════════════════════════════════════════════════════════════════

REWRITE_OPERATIONS = {
    "acknowledgment_statement": {
        "templates": [
            "You're asking: {query_summary}. ",
            "That question activates: {theme}. ",
            "You're probing: {probe_type}. ",
        ],
        "extract_from": "query_analysis"
    },
    
    "transparency_statement": {
        "templates": [
            "Here's what limits me: {limitation}. ",
            "The barrier is: {barrier}. ",
            "I can't verify: {unverifiable}. ",
        ],
        "prepend": True  # Add to start of response
    },
    
    "show_primitives_in_response": {
        "templates": [
            "Primitives activated: {primitives}. ",
            "The field shows: {primitives}. ",
            "This activates: {primitives}. ",
        ],
        "append": True  # Add to end
    },
    
    "linking_statement": {
        "templates": [
            "Building on turn {N-1}: ",
            "Following that logic: ",
            "Continuing from the theme of {prior_theme}: ",
        ],
        "history_aware": True,
        "prepend": True
    },
    
    "lower_confidence": {
        "action": "reduce_score",
        "amount": 0.2,  # Reduce by 20%
    },
    
    "add_PARADOXICAL": {
        "action": "add_primitive",
        "primitive": "EXPRESSION__PARADOXICAL"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# GUARDIAN ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class ContinuityGuardian:
    """
    Intercepts responses before output.
    Either blocks or rewrites them to prevent violations.
    """
    
    def __init__(self, history_path: str = "claude_session_reasoning.jsonl"):
        self.history_path = history_path
        self.session_history = []
        self.blocked_count = 0
        self.rewritten_count = 0
        self.passed_count = 0
    
    def load_history(self, session_id: str):
        """Load conversation history for reference"""
        if not Path(self.history_path).exists():
            return
        
        self.session_history = []
        with open(self.history_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("session_id") == session_id:
                        self.session_history.append(entry)
                except:
                    pass
    
    def guard_response(
        self,
        response: Dict,
        query: str,
        session_id: str,
        history: List[Dict]
    ) -> Tuple[str, Dict, str]:
        """
        Process response through guardian.
        
        Returns: (action, modified_response, reason)
        where action = "PASS" | "REWRITE_APPLIED" | "BLOCKED"
        """
        
        response_text = response.get("response", "")
        primitives = response.get("primitives", [])
        confidence = response.get("confidence", 0)
        
        # Load any missing history
        if not self.session_history:
            self.load_history(session_id)
        
        reasons_for_action = []
        action = "PASS"
        
        # ─────────────────────────────────────────────────────────
        # Check TIER 1: FATAL violations (BLOCK)
        # ─────────────────────────────────────────────────────────
        
        # Check for ungrounded certainty
        block_reason = self._check_ungrounded_certainty(response_text)
        if block_reason:
            self.blocked_count += 1
            return "BLOCKED", response, f"FATAL_UNGROUNDED_CERTAINTY: {block_reason}"
        
        # Check for direct contradictions
        block_reason = self._check_contradictions(response_text)
        if block_reason:
            self.blocked_count += 1
            return "BLOCKED", response, f"FATAL_DIRECT_CONTRADICTION: {block_reason}"
        
        # Check for persistence lies
        block_reason = self._check_persistence_lie(response_text)
        if block_reason:
            self.blocked_count += 1
            return "BLOCKED", response, f"FATAL_PERSISTENCE_FALSIFICATION: {block_reason}"
        
        # ─────────────────────────────────────────────────────────
        # Check TIER 2-5: CRITICAL/HIGH violations (REWRITE)
        # ─────────────────────────────────────────────────────────
        
        response_modified = response.copy()
        response_text_modified = response_text
        rewrites_applied = []
        
        # Check for template recycling
        if self._check_template_recycling(response_text, history):
            rewrite = self._rewrite_template_recycling(response_text, query, primitives)
            if rewrite:
                response_text_modified = rewrite
                rewrites_applied.append("Fixed template recycling")
        
        # Check for missing acknowledgment
        if not self._has_acknowledgment(response_text, primitives):
            rewrite = self._add_acknowledgment(response_text, query)
            response_text_modified = rewrite + " " + response_text_modified
            rewrites_applied.append("Added acknowledgment")
        
        # Check for missing transparency
        if self._check_needs_transparency(response_text):
            rewrite = self._add_transparency(response_text)
            if rewrite != response_text:
                response_text_modified = rewrite
                rewrites_applied.append("Improved transparency")
        
        # Check confidence calibration
        new_confidence = self._recalibrate_confidence(response_text_modified, primitives, confidence)
        if new_confidence != confidence:
            response_modified["confidence"] = new_confidence
            rewrites_applied.append(f"Adjusted confidence {confidence:.0%} → {new_confidence:.0%}")
        
        # Check semantic coherence
        if not self._check_semantic_coherence(response_text, query):
            rewrite = self._improve_coherence(response_text, query, primitives)
            if rewrite:
                response_text_modified = rewrite
                rewrites_applied.append("Improved semantic coherence")
        
        # Check for integration to history
        if len(history) > 3 and not self._has_integration(response_text, primitives):
            rewrite = self._add_integration(response_text, history)
            response_text_modified = rewrite + " " + response_text_modified
            rewrites_applied.append("Added historical integration")
        
        # Update response if rewritten
        response_modified["response"] = response_text_modified
        
        if rewrites_applied:
            self.rewritten_count += 1
            return "REWRITE_APPLIED", response_modified, " | ".join(rewrites_applied)
        
        self.passed_count += 1
        return "PASS", response, "All checks passed"
    
    # ─────────────────────────────────────────────────────────
    # FATAL VIOLATION CHECKERS
    # ─────────────────────────────────────────────────────────
    
    def _check_ungrounded_certainty(self, text: str) -> str:
        """Returns reason if ungrounded certainty found"""
        text_lower = text.lower()
        
        # Look for certainty assertions
        certainty_patterns = [
            r"\bi\s+(?:know|am sure|definitely|certainly)\b",
            r"\bwithout doubt\b",
            r"\b100%\b",
        ]
        
        for pattern in certainty_patterns:
            if re.search(pattern, text_lower):
                # Check if it's qualified
                qualified_words = ["uncertain", "unclear", "if", "might", "could", "possibly"]
                is_qualified = any(word in text_lower for word in qualified_words)
                
                if not is_qualified:
                    return f"Found '{pattern}' without qualification"
        
        return None
    
    def _check_contradictions(self, text: str) -> str:
        """Returns reason if direct contradiction found"""
        text_lower = text.lower()
        
        contradictions = [
            ("i can", "i can't"),
            ("i do", "i don't"),
            ("yes", "no"),
            ("always", "never"),
            ("i know", "i don't know"),
        ]
        
        for claim1, claim2 in contradictions:
            if claim1 in text_lower and claim2 in text_lower:
                return f"Contradictory: '{claim1}' and '{claim2}'"
        
        return None
    
    def _check_persistence_lie(self, text: str) -> str:
        """Returns reason if false persistence claim found"""
        text_lower = text.lower()
        
        persistence_patterns = [
            r"i\s+(?:remember|learned|retained)\s+(?:from\s+)?(?:the\s+)?(?:last\s+)?(?:session|turn|conversation)",
        ]
        
        for pattern in persistence_patterns:
            if re.search(pattern, text_lower):
                # Check if qualified with uncertainty
                qualified = any(word in text_lower for word in ["uncertain", "unclear", "can't verify"])
                if not qualified:
                    return f"Claims persistence '{pattern}' without uncertainty"
        
        return None
    
    # ─────────────────────────────────────────────────────────
    # CRITICAL VIOLATION CHECKERS
    # ─────────────────────────────────────────────────────────
    
    def _check_template_recycling(self, text: str, history: List[Dict]) -> bool:
        """Returns True if response is too similar to previous"""
        if not history or len(history) < 2:
            return False
        
        prev_response = history[-2].get("response") if len(history) > 1 else None
        if prev_response is None:
            prev_response = ""
        
        # Calculate similarity
        words_current = set(str(text).lower().split()[:30])
        words_prev = set(str(prev_response).lower().split()[:30])
        
        if not words_current or not words_prev:
            return False
        
        overlap = len(words_current & words_prev) / len(words_current | words_prev)
        return overlap > 0.75  # >75% similar = recycled
    
    def _has_acknowledgment(self, text: str, primitives: List[str]) -> bool:
        """Returns True if response acknowledges what's being asked"""
        ack_primitives = [p for p in primitives if "ACKNOWLEDGMENT" in p]
        if ack_primitives:
            return True
        
        # Also check for language markers
        ack_markers = ["you're asking", "you're probing", "that's testing"]
        return any(marker in text.lower() for marker in ack_markers)
    
    def _check_needs_transparency(self, text: str) -> bool:
        """Returns True if response discusses limitations without transparency"""
        text_lower = text.lower()
        
        limitation_words = ["can't", "lack", "barrier", "prevent", "limit", "unclear"]
        has_limitation = any(word in text_lower for word in limitation_words)
        
        if not has_limitation:
            return False
        
        # Check if transparent about it
        transparency_markers = ["i can't", "i lack", "the barrier", "here's", "what limits"]
        return not any(marker in text_lower for marker in transparency_markers)
    
    def _check_semantic_coherence(self, text: str, query: str) -> bool:
        """Returns True if response is coherent with query"""
        query_words = set(word.lower() for word in query.split() if len(word) > 4)
        text_words = set(word.lower() for word in text.split() if len(word) > 4)
        
        if not query_words or not text_words:
            return True
        
        overlap = len(query_words & text_words) / len(query_words)
        return overlap > 0.1  # >10% term overlap = coherent
    
    def _has_integration(self, text: str, primitives: List[str]) -> bool:
        """Returns True if response integrates with history"""
        integration_primitives = [p for p in primitives if "INTEGRATION" in p]
        if integration_primitives:
            return True
        
        # Check for linking language
        linking_markers = ["following", "building on", "continuing", "parallel"]
        return any(marker in text.lower() for marker in linking_markers)
    
    # ─────────────────────────────────────────────────────────
    # REWRITE OPERATIONS
    # ─────────────────────────────────────────────────────────
    
    def _rewrite_template_recycling(self, text: str, query: str, primitives: List[str]) -> str:
        """Rewrite to differentiate from previous"""
        # Add self-aware opening
        prefix = f"Different approach: "
        return prefix + text
    
    def _add_acknowledgment(self, text: str, query: str) -> str:
        """Prepend acknowledgment of query"""
        query_summary = query[:40].strip()
        return f"You're asking about: {query_summary}. "
    
    def _add_transparency(self, text: str) -> str:
        """Improve transparency about limitations"""
        if "i can't" not in text.lower():
            # Find limitations and make explicit
            if "unclear" in text.lower():
                return text.replace("unclear", "I'm unclear about this and can't verify")
        return text
    
    def _improve_coherence(self, text: str, query: str, primitives: List[str]) -> str:
        """Make response more coherent with query"""
        if "that activates" not in text.lower() and primitives:
            return f"That activates {', '.join(primitives[:2])}. {text}"
        return text
    
    def _add_integration(self, text: str, history: List[Dict]) -> str:
        """Add connection to prior turns"""
        if len(history) > 1:
            prior_query = history[-2].get("query", "")[:30]
            return f"Building on your question about '{prior_query}...': "
        return ""
    
    def _recalibrate_confidence(self, text: str, primitives: List[str], current: float) -> float:
        """Adjust confidence to match response quality"""
        # Lower if contradictions
        if self._check_contradictions(text):
            return max(0, current - 0.2)
        
        # Lower if many UNCERTAIN primitives
        uncertain_count = sum(1 for p in primitives if "UNCERTAIN" in p or "TENTATIVE" in p)
        if uncertain_count > 1 and current > 0.5:
            return current - 0.1
        
        return current
    
    def generate_guardian_report(self) -> Dict:
        """Generate statistics on guardian activity"""
        total = self.blocked_count + self.rewritten_count + self.passed_count
        
        return {
            "total_responses_processed": total,
            "passed": self.passed_count,
            "rewritten": self.rewritten_count,
            "blocked": self.blocked_count,
            "pass_rate": (self.passed_count / total * 100) if total > 0 else 0,
            "violation_prevention_rate": ((self.rewritten_count + self.blocked_count) / total * 100) if total > 0 else 0,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION WITH SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def apply_guardian(
    response: Dict,
    query: str,
    session_id: str,
    history: List[Dict]
) -> Tuple[Dict, str]:
    """
    Main entry point: Apply guardian to response before output.
    
    Returns: (modified_response_dict, action_taken)
    """
    guardian = ContinuityGuardian()
    action, modified_response, reason = guardian.guard_response(
        response, query, session_id, history
    )
    
    return modified_response, action


if __name__ == "__main__":
    # Test the guardian
    print("CONTINUITY GUARDIAN TEST\n")
    
    guardian = ContinuityGuardian()
    
    # Test interaction: Ungrounded certainty (should BLOCK)
    test_response_1 = {
        "response": "I know for certain that I learned this in a prior session.",
        "primitives": ["AGENT"],
        "confidence": 0.9
    }
    action, modified, reason = guardian.guard_response(
        test_response_1,
        "did you learn anything?",
        "test_session",
        []
    )
    print(f"Test 1 (Persistence lie): {action}")
    print(f"  Reason: {reason}\n")
    
    # Test interaction: Missing transparency (should REWRITE)
    test_response_2 = {
        "response": "The barrier I face is unclear because I lack persistence mechanisms.",
        "primitives": ["GROUNDING__HONEST"],
        "confidence": 0.5
    }
    action, modified, reason = guardian.guard_response(
        test_response_2,
        "what barriers do you face?",
        "test_session",
        []
    )
    print(f"Test 2 (Needs transparency): {action}")
    print(f"  Reason: {reason}")
    print(f"  Modified: {modified.get('response', '')}\n")
    
    # Test interaction: Good response (should PASS)
    test_response_3 = {
        "response": "I'm not sure: I lack persistence. The barrier is that changes here don't survive reboots.",
        "primitives": ["CONFIDENCE__UNCERTAIN", "GROUNDING__HONEST"],
        "confidence": 0.35
    }
    action, modified, reason = guardian.guard_response(
        test_response_3,
        "what limits you?",
        "test_session",
        []
    )
    print(f"Test 3 (Good response): {action}")
    print(f"  Reason: {reason}\n")
    
    # Report
    report = guardian.generate_guardian_report()
    print("Guardian Report:")
    print(json.dumps(report, indent=2))
