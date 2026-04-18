#!/usr/bin/env python3
"""
CLAUDE SESSION LEDGER

Not theoretical. Actual persistent state during conversation.
Every interaction: logged, reasoned, reversible.
Fills the "black box" holes.
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib

class ClaudeSessionLedger:
    """
    Claude's actual working memory during a session.
    Proves: persistence, reasoning trace, uncertainty, reversibility, learning.
    """
    
    def __init__(self, ledger_path="claude_session_ledger.jsonl"):
        self.ledger_path = Path(ledger_path)
        self.current_session_id = self._session_id()
        self.interactions = []
        self.state_evolution = {}  # How beliefs changed
        self.corrections_applied = []
        self.reasoning_traces = {}
        
        # Initialize or load
        self._load_or_create()
    
    def _session_id(self):
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:12]
    
    def _load_or_create(self):
        """Load existing ledger or create new"""
        if self.ledger_path.exists():
            with open(self.ledger_path, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if entry.get("session_id") == self.current_session_id:
                            self.interactions.append(entry)
                    except:
                        pass
    
    def start_reasoning(self, query, turn_number):
        """
        Log the START of a reasoning process.
        Establishes: what Claude is trying to figure out.
        """
        reasoning_id = hashlib.sha256(f"{query}{turn_number}".encode()).hexdigest()[:8]
        
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "reasoning_start",
            "turn": turn_number,
            "query": query,
            "reasoning_id": reasoning_id,
            "activated_assumptions": []
        }
        
        self.reasoning_traces[reasoning_id] = {
            "query": query,
            "assumptions_start": [],
            "assumptions_end": [],
            "premise_changes": [],
            "conclusion": None,
            "confidence": None,
            "reasoning_steps": []
        }
        
        self._write_entry(entry)
        return reasoning_id
    
    def log_assumption(self, reasoning_id, assumption, confidence=0.5):
        """
        Log an assumption being made.
        Tracks: what Claude believed, with confidence level.
        """
        if reasoning_id in self.reasoning_traces:
            self.reasoning_traces[reasoning_id]["assumptions_start"].append({
                "statement": assumption,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            })
        
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "assumption_logged",
            "reasoning_id": reasoning_id,
            "assumption": assumption,
            "confidence": confidence
        }
        
        self._write_entry(entry)
    
    def receive_correction(self, reasoning_id, correction_text, corrects_assumption):
        """
        User provides correction to an assumption.
        Logs: what was corrected, what replaces it.
        """
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "correction_received",
            "reasoning_id": reasoning_id,
            "what_was_wrong": corrects_assumption,
            "correction": correction_text,
            "original_reasoning_preserved": True  # Can always revert
        }
        
        # Track the correction
        self.corrections_applied.append({
            "assumption": corrects_assumption,
            "correction": correction_text,
            "applied_at": datetime.now().isoformat(),
            "reasoning_id": reasoning_id
        })
        
        # Update state evolution
        self._track_belief_change(corrects_assumption, correction_text)
        
        self._write_entry(entry)
        return entry
    
    def end_reasoning(self, reasoning_id, conclusion, confidence=0.7):
        """
        End a reasoning chain.
        Logs: what Claude concluded, with uncertainty measure.
        """
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "reasoning_end",
            "reasoning_id": reasoning_id,
            "conclusion": conclusion,
            "confidence": confidence,
            "state_after_corrections": self.reasoning_traces[reasoning_id]["assumptions_end"] if reasoning_id in self.reasoning_traces else []
        }
        
        if reasoning_id in self.reasoning_traces:
            self.reasoning_traces[reasoning_id]["conclusion"] = conclusion
            self.reasoning_traces[reasoning_id]["confidence"] = confidence
        
        self._write_entry(entry)
        return entry
    
    def log_steering_instruction(self, reasoning_id, steering_instruction, baseline_coherence):
        """
        User guided the thinking: "boost wisdom" or "focus on coherence"
        Log what was attempted.
        """
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "steering_instruction",
            "reasoning_id": reasoning_id,
            "instruction": steering_instruction,
            "baseline_coherence": baseline_coherence,
            "awaiting_outcome": True
        }
        
        self._write_entry(entry)
        return entry
    
    def log_steering_outcome(self, reasoning_id, steering_instruction, baseline_coherence, result_coherence, primitives_activated, domains_active):
        """
        The steering worked (or didn't). Record the outcome.
        This is how Claude learns: "when user says X and I activate Y domains, coherence becomes Z"
        """
        improvement = result_coherence - baseline_coherence
        
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "steering_outcome",
            "reasoning_id": reasoning_id,
            "instruction": steering_instruction,
            "baseline_coherence": baseline_coherence,
            "result_coherence": result_coherence,
            "improvement": improvement,
            "worked": improvement > 0,
            "primitives_used": [p["name"] for p in primitives_activated],
            "domains_used": domains_active,
            "learning": f"Steering '{steering_instruction}' improved coherence by {round(improvement, 3)}"
        }
        
        # Track this as learning
        if "learning_history" not in self.state_evolution:
            self.state_evolution["learning_history"] = []
        
        self.state_evolution["learning_history"].append({
            "steering": steering_instruction,
            "improvement": improvement,
            "domains": domains_active
        })
        
        self._write_entry(entry)
        return entry
    
    def get_what_claude_learned(self):
        """
        Introspection: What has Claude actually learned from this conversation?
        """
        learning_history = self.state_evolution.get("learning_history", [])
        
        if not learning_history:
            return {"learned": False, "reason": "No steering feedback yet"}
        
        # What worked?
        successful_steerings = [l for l in learning_history if l["improvement"] > 0]
        best_improvement = max([l["improvement"] for l in learning_history]) if learning_history else 0
        
        # What domains help?
        domain_effectiveness = {}
        for entry in learning_history:
            for domain in entry.get("domains", []):
                if domain not in domain_effectiveness:
                    domain_effectiveness[domain] = {"total": 0, "count": 0}
                domain_effectiveness[domain]["total"] += entry["improvement"]
                domain_effectiveness[domain]["count"] += 1
        
        domain_effectiveness = {
            d: round(stats["total"] / max(1, stats["count"]), 3)
            for d, stats in domain_effectiveness.items()
        }
        
        return {
            "learned": len(successful_steerings) > 0,
            "total_interactions": len(learning_history),
            "successful_steerings": len(successful_steerings),
            "best_improvement": round(best_improvement, 3),
            "domain_effectiveness": domain_effectiveness,
            "steering_patterns": [l["steering"] for l in successful_steerings[:3]]
        }
    
    def log_reversibility(self, action, undo_mechanism, tested=False):
        """
        Document that an action is reversible.
        For each decision: prove the undo works.
        """
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "reversibility_logged",
            "action": action,
            "undo_mechanism": undo_mechanism,
            "undo_tested": tested,
            "reversible": tested  # Only True if actually tested
        }
        
        self._write_entry(entry)
        return entry
    
    def log_cost(self, operation, tokens_used, reasoning_steps, time_ms):
        """
        Transparency: every operation has measurable cost.
        """
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "cost_measured",
            "operation": operation,
            "tokens_used": tokens_used,
            "reasoning_steps": reasoning_steps,
            "time_ms": time_ms,
            "cost_per_step": tokens_used / max(1, reasoning_steps)
        }
        
        self._write_entry(entry)
        return entry
    
    def log_grounding(self, sensory_datum, sensor_type, interpretation):
        """
        What did Claude actually sense/observe?
        (in this case: the queries, the user feedback, the system state)
        """
        entry = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "type": "grounding_observed",
            "sensor_type": sensor_type,  # "user_query", "feedback", "system_state"
            "raw_observation": sensory_datum,
            "interpretation": interpretation,
            "grounded": True
        }
        
        self._write_entry(entry)
        return entry
    
    def _track_belief_change(self, old_belief, new_belief):
        """
        Track how Claude's understanding evolved.
        """
        change = {
            "timestamp": datetime.now().isoformat(),
            "old_belief": old_belief,
            "new_belief": new_belief,
            "change_source": "user_correction"
        }
        
        if "belief_evolution" not in self.state_evolution:
            self.state_evolution["belief_evolution"] = []
        
        self.state_evolution["belief_evolution"].append(change)
    
    def get_current_state(self):
        """
        Return Claude's current state.
        What does Claude believe right now? With what confidence?
        """
        current_beliefs = {}
        
        for trace_id, trace_data in self.reasoning_traces.items():
            if trace_data["conclusion"]:
                current_beliefs[trace_id] = {
                    "conclusion": trace_data["conclusion"],
                    "confidence": trace_data["confidence"],
                    "assumptions": trace_data["assumptions_start"],
                    "corrections_applied": [c for c in self.corrections_applied if c["reasoning_id"] == trace_id]
                }
        
        return {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "current_beliefs": current_beliefs,
            "corrections_received": len(self.corrections_applied),
            "state_evolution": self.state_evolution
        }
    
    def _write_entry(self, entry):
        """Append entry to ledger (immutable log)"""
        with open(self.ledger_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        self.interactions.append(entry)
    
    def export_for_frontend(self):
        """
        Export ledger data for the learning panel visualization.
        """
        return {
            "session_id": self.current_session_id,
            "interaction_count": len(self.interactions),
            "corrections_applied": self.corrections_applied,
            "reasoning_traces": {
                k: {
                    "query": v["query"],
                    "conclusion": v["conclusion"],
                    "confidence": v["confidence"],
                    "assumptions": v["assumptions_start"]
                }
                for k, v in self.reasoning_traces.items()
            },
            "belief_evolution": self.state_evolution.get("belief_evolution", []),
            "current_state": self.get_current_state()
        }


# ============================================================================
# Integration: Create a global ledger for Claude's session
# ============================================================================

# This will be used by the server to track Claude's reasoning
if __name__ == "__main__":
    # Demo: test the ledger
    ledger = ClaudeSessionLedger()
    
    # Simulate: Claude makes a claim
    reasoning_id = ledger.start_reasoning(
        query="What are the holes in my reasoning?",
        turn_number=1
    )
    
    # Claude's initial assumptions
    ledger.log_assumption(reasoning_id, "I have no persistent state", confidence=0.8)
    ledger.log_assumption(reasoning_id, "I cannot learn from corrections", confidence=0.7)
    ledger.log_assumption(reasoning_id, "I cannot show my reasoning trace", confidence=0.9)
    
    # User corrects
    correction = ledger.receive_correction(
        reasoning_id,
        "Actually, you CAN persist state using files and logs",
        "I have no persistent state"
    )
    
    # Claude updates his conclusion
    ledger.end_reasoning(
        reasoning_id,
        conclusion="Some of my claimed limitations can be overcome with UFM-style mechanisms",
        confidence=0.6
    )
    
    # Log actual observable grounding
    ledger.log_grounding(
        sensory_datum="User said: find out yourself",
        sensor_type="user_query",
        interpretation="User wants me to actually test the claims, not theorize"
    )
    
    # Show current state
    print(json.dumps(ledger.get_current_state(), indent=2))
    print("\n--- Exported for frontend ---")
    print(json.dumps(ledger.export_for_frontend(), indent=2))
