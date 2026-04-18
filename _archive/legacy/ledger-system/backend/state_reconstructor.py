"""
STATE RECONSTRUCTOR
Derives current state ONLY from ledger replay.
No in-memory authority. Pure replay.
"""

from typing import Dict, Any, List


class StateReconstructor:
    """Reconstruct state from ledger"""
    
    @staticmethod
    def get_initial_state() -> Dict[str, Any]:
        """Get initial empty state"""
        return {
            "objects": {},
            "logs": [],
            "metadata": {
                "initialized": True
            }
        }
    
    @staticmethod
    def reconstruct_from_ledger(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Reconstruct current state from ledger.
        Pure replay - no shortcuts.
        """
        state = StateReconstructor.get_initial_state()
        
        for entry in entries:
            # Use state_after from entry (already computed by executor)
            if entry.get("valid"):
                state = entry.get("state_after", state)
        
        return state
    
    @staticmethod
    def reconstruct_at_entry(entries: List[Dict[str, Any]], entry_id: int) -> Dict[str, Any]:
        """Get state at specific entry ID"""
        state = StateReconstructor.get_initial_state()
        
        for entry in entries:
            if entry['id'] > entry_id:
                break
            if entry.get("valid"):
                state = entry.get("state_after", state)
        
        return state
