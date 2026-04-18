import json
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, List

class Ledger:
    """Append-only ledger: source of truth for entire system."""
    
    def __init__(self, ledger_path: str = "../ledger/ledger.json"):
        self.ledger_path = ledger_path
        self.entries: List[Dict[str, Any]] = []
        self.load_ledger()
    
    def load_ledger(self):
        """Load existing ledger or create new one."""
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                data = json.load(f)
                self.entries = data.get('entries', [])
        else:
            self.entries = []
            self.save_ledger()
    
    def save_ledger(self):
        """Persist ledger to disk."""
        with open(self.ledger_path, 'w') as f:
            json.dump({'entries': self.entries}, f, indent=2)
    
    def append(self, intent: Dict[str, Any], action: str, input_data: Dict[str, Any], 
               output_data: Dict[str, Any], state_before: Dict[str, Any], 
               state_after: Dict[str, Any], valid: bool) -> int:
        """
        Append entry to ledger.
        
        Returns entry ID.
        """
        entry_id = len(self.entries)
        
        entry = {
            "id": entry_id,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "intent": intent,
            "action": action,
            "input": input_data,
            "output": output_data,
            "state_before": state_before,
            "state_after": state_after,
            "valid": valid,
            "hash": hashlib.sha256(json.dumps({
                "id": entry_id,
                "intent": intent,
                "action": action,
            }, sort_keys=True).encode()).hexdigest()
        }
        
        self.entries.append(entry)
        self.save_ledger()
        
        return entry_id
    
    def get_entry(self, entry_id: int) -> Dict[str, Any]:
        """Get entry by ID."""
        if 0 <= entry_id < len(self.entries):
            return self.entries[entry_id]
        return None
    
    def get_latest(self) -> Dict[str, Any]:
        """Get latest entry."""
        if self.entries:
            return self.entries[-1]
        return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all entries."""
        return self.entries
    
    def replay(self) -> Dict[str, Any]:
        """
        Replay entire ledger to reconstruct current state.
        
        Returns final state after executing all entries.
        """
        state = {
            "visual_state": {},
            "system_state": {},
            "messages": []
        }
        
        for entry in self.entries:
            if entry.get('valid', False):
                state = entry.get('state_after', state)
        
        return state
