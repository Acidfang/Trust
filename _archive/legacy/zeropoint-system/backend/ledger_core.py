"""
LEDGER CORE - Append-only immutable record store

Single responsibility: Record every decision immutably.
No decisions made here. Only write operations.

Entry format:
{
  "id": int,
  "timestamp": int,
  "intent": object,
  "action": string,
  "input": object,
  "output": object,
  "state_before": object,
  "state_after": object,
  "valid": boolean
}
"""

import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List


class LedgerCore:
    """Append-only ledger - immutable record of all decisions."""
    
    def __init__(self, ledger_path: str = "ledger/ledger.json"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._entries = []
        self._load()
    
    def _load(self):
        """Load existing ledger from disk."""
        if self.ledger_path.exists():
            with open(self.ledger_path, 'r') as f:
                self._entries = json.load(f)
        else:
            self._entries = []
    
    def append(self, entry: Dict[str, Any]) -> int:
        """
        Append a new entry to ledger.
        Entry ID is auto-assigned.
        Returns the entry ID.
        
        Entry MUST contain:
        - action: what was done
        - input: what was provided
        - output: what was produced
        - intent: what was requested
        - state_before: snapshot before
        - state_after: snapshot after
        - valid: was this valid?
        """
        entry_id = len(self._entries)
        
        record = {
            "id": entry_id,
            "timestamp": int(time.time() * 1000),  # milliseconds
            "action": entry.get("action", "UNKNOWN"),
            "input": entry.get("input", {}),
            "output": entry.get("output", {}),
            "intent": entry.get("intent", {}),
            "state_before": entry.get("state_before", {}),
            "state_after": entry.get("state_after", {}),
            "valid": entry.get("valid", False),
            "hash": ""  # Will be filled below
        }
        
        # Create deterministic hash of this entry (for verification)
        record["hash"] = self._hash_entry(record)
        
        # Write immediately (immutable)
        self._entries.append(record)
        self._save()
        
        return entry_id
    
    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        """Create deterministic hash of entry."""
        hashable = json.dumps({
            "id": entry["id"],
            "timestamp": entry["timestamp"],
            "action": entry["action"],
            "input": entry["input"],
            "output": entry["output"]
        }, sort_keys=True)
        return hashlib.sha256(hashable.encode()).hexdigest()[:16]
    
    def _save(self):
        """Persist ledger to disk."""
        with open(self.ledger_path, 'w') as f:
            json.dump(self._entries, f, indent=2)
    
    def replay(self, until_id: int = None) -> List[Dict[str, Any]]:
        """
        Replay ledger from start.
        Optionally limit to specific entry ID.
        """
        if until_id is None:
            return self._entries
        return self._entries[:until_id + 1]
    
    def get_state_at(self, entry_id: int) -> Dict[str, Any]:
        """Get the state after a specific entry was recorded."""
        if entry_id < 0 or entry_id >= len(self._entries):
            return {}
        return self._entries[entry_id].get("state_after", {})
    
    def get_latest_state(self) -> Dict[str, Any]:
        """Get the most recent state."""
        if not self._entries:
            return {}
        return self._entries[-1].get("state_after", {})
    
    def get_last_entry_id(self) -> int:
        """Get ID of last recorded entry."""
        return len(self._entries) - 1
    
    def get_entry(self, entry_id: int) -> Dict[str, Any]:
        """Get specific entry by ID."""
        if entry_id < 0 or entry_id >= len(self._entries):
            return {}
        return self._entries[entry_id]
    
    def all_entries(self) -> List[Dict[str, Any]]:
        """Return all entries."""
        return self._entries.copy()
