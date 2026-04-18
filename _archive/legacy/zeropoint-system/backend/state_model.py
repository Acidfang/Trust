"""
STATE MODEL - Derived entirely from ledger replay

Single responsibility: Reconstruct state from ledger.
No authority of its own. Mirror of what ledger records.

State is always: current state = replay ledger from start
"""

from typing import Dict, Any
from ledger_core import LedgerCore


class StateModel:
    """Reconstructs state by replaying ledger."""
    
    def __init__(self, ledger: LedgerCore):
        self.ledger = ledger
        self.state = self._reconstruct_state()
    
    def _reconstruct_state(self) -> Dict[str, Any]:
        """
        Rebuild state from complete ledger replay.
        Deterministic: same ledger always produces same state.
        """
        state = {
            "objects": {},
            "messages": [],
            "metadata": {
                "total_intents": 0,
                "total_valid_actions": 0,
                "last_action": None
            }
        }
        
        # Replay every entry
        for entry in self.ledger.all_entries():
            if entry.get("valid"):
                state["metadata"]["total_valid_actions"] += 1
                state["metadata"]["last_action"] = entry.get("action")
            
            state["metadata"]["total_intents"] += 1
            
            # Apply output to state
            output = entry.get("output", {})
            if "object_id" in output:
                state["objects"][output["object_id"]] = output
            
            if "message" in output:
                state["messages"].append(output["message"])
        
        return state
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state."""
        return self.state.copy()
    
    def refresh(self):
        """Refresh state from ledger (e.g., after new entry)."""
        self.state = self._reconstruct_state()
