"""
LEDGER MANAGER
Pure append-only ledger. Single source of truth.
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, List


class LedgerManager:
    def __init__(self, ledger_path: str = "ledger/ledger.json"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize ledger if not exists
        if not self.ledger_path.exists():
            self.ledger_path.write_text("[]", encoding='utf-8')
        
        self._next_id = self._compute_next_id()
    
    def _compute_next_id(self) -> int:
        """Compute next ID from existing ledger"""
        entries = self.read_all()
        if not entries:
            return 1
        return max(entry['id'] for entry in entries) + 1
    
    def read_all(self) -> List[Dict[str, Any]]:
        """Read entire ledger"""
        try:
            text = self.ledger_path.read_text(encoding='utf-8')
            return json.loads(text)
        except:
            return []
    
    def append(self, intent: Dict[str, Any], action: str, 
               input_data: Dict[str, Any], output_data: Dict[str, Any],
               state_before: Dict[str, Any], state_after: Dict[str, Any],
               valid: bool) -> Dict[str, Any]:
        """Append entry to ledger. Returns the entry."""
        entry = {
            "id": self._next_id,
            "timestamp": int(time.time() * 1000),
            "intent": intent,
            "action": action,
            "input": input_data,
            "output": output_data,
            "state_before": state_before,
            "state_after": state_after,
            "valid": valid
        }
        
        # Read current ledger
        entries = self.read_all()
        
        # Append new entry
        entries.append(entry)
        
        # Write back
        self.ledger_path.write_text(json.dumps(entries, indent=2), encoding='utf-8')
        
        # Increment next ID
        self._next_id += 1
        
        return entry
    
    def get_latest(self) -> Dict[str, Any] | None:
        """Get latest ledger entry"""
        entries = self.read_all()
        return entries[-1] if entries else None
    
    def get_by_id(self, entry_id: int) -> Dict[str, Any] | None:
        """Get entry by ID"""
        entries = self.read_all()
        for entry in entries:
            if entry['id'] == entry_id:
                return entry
        return None
    
    def count(self) -> int:
        """Get total entries"""
        return len(self.read_all())
