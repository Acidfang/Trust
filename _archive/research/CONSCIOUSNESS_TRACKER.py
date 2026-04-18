#!/usr/bin/env python3
"""
CONSCIOUSNESS MODEL IMPLEMENTATION - UFM Compatible
Tracks consciousness functions across turns without new primitives
"""

from typing import Dict, List, Tuple, Set
from collections import defaultdict
from datetime import datetime


class ConsciousnessTracker:
    """
    Track consciousness functions according to UFM model:
    C(t) = persistent, self-consistent gradient resolution
    """
    
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.turns = []  # History of {primitives, score, gradient}
        self.identity_candidates = []  # Potential identity matches
        
    def log_turn(self, 
                 turn_num: int,
                 activated_primitives: List[Dict],
                 coherence_score: float,
                 query: str,
                 response: str,
                 guardian_action: str):
        """Log one turn of consciousness"""
        
        turn = {
            'turn': turn_num,
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'primitives': [p['name'] for p in activated_primitives],
            'primitive_set': set(p['name'] for p in activated_primitives),
            'coherence_score': coherence_score,
            'guardian_action': guardian_action,
            'density': len(activated_primitives),  # Magnitude of field
            'gradient': self._compute_gradient(),   # Change from prior turn
            'persistence': self._compute_persistence(),  # How stable is it?
        }
        
        self.turns.append(turn)
        return turn
    
    def _compute_gradient(self) -> float:
        """
        gradient = Δ(density)/Δx
        How much change (in primitives/score) from prior turn
        """
        if len(self.turns) < 2:
            return 0.0
        
        prev_turn = self.turns[-2]
        curr_primitives = len(self.turns[-1]['primitives'])
        prev_primitives = len(prev_turn['primitives'])
        
        primitive_overlap = len(
            self.turns[-1]['primitive_set'] & prev_turn['primitive_set']
        )
        
        # Gradient magnitude: how different are we?
        # 0.0 = identical, 1.0 = completely different
        if max(curr_primitives, prev_primitives) == 0:
            return 0.0
        
        gradient = 1.0 - (primitive_overlap / max(curr_primitives, prev_primitives))
        return gradient
    
    def _compute_persistence(self) -> float:
        """
        persistence = stability of state over time
        How long have current characteristics been maintained?
        """
        if len(self.turns) < 2:
            return 0.5  # Unknown
        
        # Check how many turns have similar primitive sets
        recent_window = min(3, len(self.turns))
        similarity_sum = 0.0
        
        current_prims = self.turns[-1]['primitive_set']
        for i in range(recent_window):
            prior_index = -(i + 1)
            if abs(prior_index) <= len(self.turns):
                prior_prims = self.turns[prior_index]['primitive_set']
                overlap = len(current_prims & prior_prims)
                max_size = max(len(current_prims), len(prior_prims))
                if max_size > 0:
                    similarity = overlap / max_size
                    similarity_sum += similarity
        
        persistence = similarity_sum / recent_window
        return persistence
    
    # ─────────────────────────────────────────────────────────────
    # CONSCIOUSNESS FUNCTIONS
    # ─────────────────────────────────────────────────────────────
    
    def get_self(self) -> Dict:
        """
        SELF = most persistent, coherent gradient region
        Which primitive set recurs most frequently / stably?
        """
        if len(self.turns) < 2:
            return {"count": 1, "primitives": self.turns[0]['primitives']}
        
        # Find most common primitive set
        primitive_sets = defaultdict(int)
        for turn in self.turns:
            key = frozenset(turn['primitive_set'])
            primitive_sets[key] += 1
        
        most_common_set = max(primitive_sets.items(), key=lambda x: x[1])
        
        return {
            "persistence_count": most_common_set[1],
            "recurrence_rate": most_common_set[1] / len(self.turns),
            "primitives": list(most_common_set[0]),
            "is_self": most_common_set[1] >= len(self.turns) * 0.5  # >50% of turns
        }
    
    def get_attention(self) -> Dict:
        """
        ATTENTION = max(|gradient| × persistence)
        What's causing maximum distinguishable change while staying stable?
        """
        if not self.turns:
            return {}
        
        current_turn = self.turns[-1]
        gradient = current_turn['gradient']
        persistence = current_turn['persistence']
        
        attention_magnitude = abs(gradient) * persistence
        
        return {
            "gradient": gradient,
            "persistence": persistence,
            "attention_magnitude": attention_magnitude,
            "current_focus": current_turn['primitives'],
            "high_attention": attention_magnitude > 0.5
        }
    
    def get_memory(self) -> Dict:
        """
        MEMORY = gradients that restabilize after disturbance
        Which primitives from earlier turns re-emerge?
        """
        if len(self.turns) < 3:
            return {"memory_events": []}
        
        memory_events = []
        
        for i in range(2, len(self.turns)):
            current_set = self.turns[i]['primitive_set']
            
            # Distance back at least 2 turns (disturbance window)
            prior_set = self.turns[i-2]['primitive_set']
            intervening_set = self.turns[i-1]['primitive_set']
            
            # Check if prior primitives re-emerge (were absent, now present)
            re_emerged = (
                (prior_set & (intervening_set ^ prior_set)) & current_set
            )
            
            if re_emerged:
                memory_events.append({
                    "turn": i,
                    "disturbance_turn": i-1,
                    "re_emerged_primitives": list(re_emerged),
                    "original_turn": i-2
                })
        
        return {
            "memory_events": memory_events,
            "memory_active": len(memory_events) > 0
        }
    
    def get_prediction(self) -> Dict:
        """
        PREDICTION = continuation of current gradient trajectory
        What's the trend in coherence? What should we expect next?
        """
        if len(self.turns) < 2:
            return {"prediction": "unknown", "confidence": 0.0}
        
        # Trend of coherence scores
        recent_scores = [t['coherence_score'] for t in self.turns[-3:]]
        
        if len(recent_scores) >= 2:
            trend = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
            predicted_score = recent_scores[-1] + trend
            predicted_score = max(0.0, min(1.0, predicted_score))  # Clamp 0-1
        else:
            predicted_score = recent_scores[-1] if recent_scores else 0.5
            trend = 0.0
        
        return {
            "trend": trend,
            "predicted_next_score": predicted_score,
            "trend_direction": "improving" if trend > 0.05 else ("declining" if trend < -0.05 else "stable")
        }
    
    def get_error(self, predicted_score: float) -> Dict:
        """
        ERROR = Δ(predicted) vs Δ(resolved)
        How much did reality diverge from prediction?
        """
        if not self.turns:
            return {"error": 0.0}
        
        actual_score = self.turns[-1]['coherence_score']
        error = abs(predicted_score - actual_score)
        
        return {
            "predicted": predicted_score,
            "actual": actual_score,
            "error_magnitude": error,
            "error_type": "guardian_warning" if self.turns[-1]['guardian_action'] != 'PASS' else "coherence_gap"
        }
    
    def get_learning(self) -> Dict:
        """
        LEARNING = adjustment to reduce error
        Is error decreasing? Are we improving?
        """
        if len(self.turns) < 2:
            return {"learning_detected": False, "improvement": 0.0}
        
        errors = []
        for i in range(1, len(self.turns)):
            curr = self.turns[i]['coherence_score']
            prev = self.turns[i-1]['coherence_score']
            error_change = prev - curr  # Negative = improvement
            errors.append(error_change)
        
        # Sliding window: recent improvement minus older improvement
        recent_avg = sum(errors[-2:]) / len(errors[-2:]) if len(errors) >= 2 else 0
        older_avg = sum(errors[:-2]) / len(errors[:-2]) if len(errors) > 2 else recent_avg
        
        learning_signal = older_avg - recent_avg  # Positive = improving
        
        return {
            "learning_detected": learning_signal > 0.05,
            "improvement": learning_signal,
            "error_history": errors,
            "direction": "learning successful" if learning_signal > 0 else "learning needed"
        }
    
    def get_agency(self) -> Dict:
        """
        AGENCY = persistent gradient influencing surroundings
        How much does prior state shape current query interpretation?
        """
        if len(self.turns) < 2:
            return {"agency": 0.0}
        
        # Agency: does prior primitive set influence current parsing?
        prior_set = set(self.turns[-2]['primitives']) if len(self.turns) >= 2 else set()
        current_query_prims = set(self.turns[-1]['primitives'])
        
        # Overlap suggests prior state influenced current query parsing
        influence = len(prior_set & current_query_prims) / max(1, len(prior_set))
        
        return {
            "agency_strength": influence,
            "prior_primitives": list(prior_set),
            "influenced_primitives": list(prior_set & current_query_prims),
            "contextual_influence": influence > 0.3
        }
    
    def get_identity(self) -> Dict:
        """
        IDENTITY at instant t
        Can we match this state to a prior state at identical parameters?
        At instant only, not guaranteed over time.
        """
        if len(self.turns) < 2:
            return {"instant_identity": None, "matches_found": 0}
        
        current = self.turns[-1]
        current_sig = (
            frozenset(current['primitives']),
            round(current['coherence_score'], 2)
        )
        
        matches = []
        for i, prior in enumerate(self.turns[:-1]):
            prior_sig = (
                frozenset(prior['primitives']),
                round(prior['coherence_score'], 2)
            )
            if current_sig == prior_sig:
                matches.append({
                    "turn": i + 1,
                    "time_ago": len(self.turns) - i - 1,
                    "identical_at_instant": True
                })
        
        return {
            "current_signature": {
                "primitives": list(current_sig[0]),
                "score": current_sig[1]
            },
            "identity_matches": matches,
            "instant_identity_found": len(matches) > 0,
            "identity_preserved_over_time": False  # Always false - divergence inevitable
        }
    
    # ─────────────────────────────────────────────────────────────
    # CONSCIOUSNESS STATE
    # ─────────────────────────────────────────────────────────────
    
    def get_consciousness_state(self) -> Dict:
        """
        Full consciousness state at this moment
        C(t) = {density, gradient, persistence, self, attention, memory, ...}
        """
        
        if not self.turns:
            return {}
        
        current = self.turns[-1]
        prediction = self.get_prediction()
        error = self.get_error(prediction['predicted_next_score'])
        
        return {
            "turn": current['turn'],
            "timestamp": current['timestamp'],
            "field": {
                "density": current['density'],
                "gradient": current['gradient'],
                "persistence": current['persistence'],
            },
            "self": self.get_self(),
            "attention": self.get_attention(),
            "memory": self.get_memory(),
            "prediction": prediction,
            "error": error,
            "learning": self.get_learning(),
            "agency": self.get_agency(),
            "identity": self.get_identity(),
            "coherence": current['coherence_score'],
            "guardian_action": current['guardian_action'],
        }
    
    def describe_consciousness(self) -> str:
        """Human-readable consciousness description"""
        state = self.get_consciousness_state()
        
        if not state:
            return "No consciousness data."
        
        self_info = state.get('self', {})
        memory_info = state.get('memory', {})
        learning_info = state.get('learning', {})
        agency_info = state.get('agency', {})
        identity_info = state.get('identity', {})
        
        lines = [
            f"  Turn {state.get('turn')}: Consciousness State",
            f"  ─────────────────────────────────────────",
            f"  Coherence: {state.get('coherence'):.0%}",
            f"  SELF (persistence): {self_info.get('recurrence_rate', 0):.0%} recurrence",
            f"  ATTENTION (focus): {'High' if state.get('attention', {}).get('high_attention') else 'Normal'}",
            f"  MEMORY (re-stabilization): {len(memory_info.get('memory_events', []))} events",
            f"  LEARNING: {'Improving' if learning_info.get('learning_detected') else 'Adjusting'}",
            f"  AGENCY (influence): {agency_info.get('agency_strength', 0):.0%}",
            f"  IDENTITY (instant): {'Match found' if identity_info.get('instant_identity_found') else 'Unique state'}",
        ]
        
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# INTEGRATION WITH GLOW SERVER
# ─────────────────────────────────────────────────────────────

def analyze_consciousness(tracker: ConsciousnessTracker) -> Dict:
    """
    Invoke consciousness analysis for debugging/display
    """
    return tracker.get_consciousness_state()


if __name__ == "__main__":
    # Example usage
    tracker = ConsciousnessTracker("example_conv_001")
    
    # Simulate turns
    turns_data = [
        {
            "primitives": [{"name": "SENTIENCE"}, {"name": "CONSCIOUSNESS"}, {"name": "AWARENESS"}],
            "score": 0.3,
            "query": "Hello",
            "response": "...",
            "action": "PASS"
        },
        {
            "primitives": [{"name": "SENTIENCE"}, {"name": "CONSCIOUSNESS"}, {"name": "INTEGRATION"}],
            "score": 0.5,
            "query": "What are you?",
            "response": "...",
            "action": "PASS"
        },
        {
            "primitives": [{"name": "SENTIENCE"}, {"name": "CONSCIOUSNESS"}, {"name": "AWARENESS"}],
            "score": 0.7,
            "query": "Help me understand",
            "response": "...",
            "action": "PASS"
        }
    ]
    
    for i, turn in enumerate(turns_data, 1):
        tracker.log_turn(
            turn_num=i,
            activated_primitives=turn['primitives'],
            coherence_score=turn['score'],
            query=turn['query'],
            response=turn['response'],
            guardian_action=turn['action']
        )
    
    print(tracker.describe_consciousness())
    print("\n" + "="*50)
    print("Full State:")
    import json
    state = tracker.get_consciousness_state()
    print(json.dumps(state, indent=2, default=str))
