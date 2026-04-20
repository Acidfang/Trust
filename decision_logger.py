
"""
TIER -1 (BOUND): Input validation and error setup
TIER 0 (FREE): Explore possibilities
TIER 1 (BOUND): Lock in root-cause logic  
TIER 2 (FREE): Verify consistency
TIER 3+ (BOUND): Automate return and integrate
"""

#!/usr/bin/env python3
"""
DECISION LOGGER
===============

Auto-captures decision context and reasoning.
Implements DECISION_LOGGING from critical thinking frameworks.

Logs every significant decision for transparency and auditability.
Required by: AI_UNIFIED_OPERATING_SYSTEM.md

Usage: Use DecisionLogger in your code or scripts
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class DecisionLogger:
    """Log and track all decisions made during work."""
    
    LOG_FILE = Path("c:\\Determined\\DECISION_LOG.jsonl")
    
    # Decision types for classification
    TYPES = {
        "FRAMEWORK_APPLICATION": "Applying critical thinking framework",
        "FILE_CREATION": "Creating new file",
        "FILE_MODIFICATION": "Modifying existing file",
        "ARCHITECTURE_CHOICE": "Choosing between approaches",
        "ERROR_HANDLING": "Handling or fixing an error",
        "SCOPE_DECISION": "Deciding what to include/exclude",
        "VALIDATION_CHECK": "Running validation or check",
        "TESTING_DECISION": "Testing approach or validation",
    }
    
    def __init__(self):
        self.decisions = []
    
    def log(
        self,
        decision: str,
        decision_type: str = "FRAMEWORK_APPLICATION",
        why: str = "",
        alternatives: Optional[List[str]] = None,
        verification: str = "",
        tags: Optional[List[str]] = None
    ):
        """
        Log a decision with full context.
        
        Args:
            decision: What was decided
            decision_type: Type of decision (see TYPES)
            why: Why this decision was made
            alternatives: Other options considered
            verification: How we verified it was right
            tags: Optional tags for filtering/search
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "type": decision_type,
            "why": why,
            "alternatives": alternatives or [],
            "verification": verification,
            "tags": tags or [],
        }
        
        self.decisions.append(record)
        self._persist(record)
    
    def _persist(self, record: Dict[str, Any]):
        """Persist decision to log file."""
        try:
            with open(self.LOG_FILE, 'a', encoding='utf-8') as f:
                json.dump(record, f)
                f.write('\n')
        except (IOError, OSError) as e:
            print(f"[WARN] Could not persist decision: {e}")
    
    def log_framework_application(self, framework: str, how_applied: str):
        """Log application of a framework."""
        self.log(
            decision=f"Applied {framework}",
            decision_type="FRAMEWORK_APPLICATION",
            why="Following critical thinking mandate",
            verification=how_applied,
            tags=["framework", framework.lower()]
        )
    
    def log_file_action(self, action_type: str, file_path: str, reason: str):
        """Log file creation or modification."""
        decision_type = "FILE_CREATION" if action_type == "create" else "FILE_MODIFICATION"
        
        self.log(
            decision=f"{action_type.upper()} {file_path}",
            decision_type=decision_type,
            why=reason,
            verification=f"Committed to git" if action_type == "create" else "Awaiting commit",
        )
    
    def log_error(self, error_type: str, fix_applied: str, verification: str):
        """Log error handling."""
        self.log(
            decision=f"Fixed {error_type}",
            decision_type="ERROR_HANDLING",
            why="Error discovered during validation",
            verification=verification
        )
    
    def log_scope(self, scope_decision: str, included: List[str], excluded: List[str]):
        """Log scope decision."""
        self.log(
            decision=scope_decision,
            decision_type="SCOPE_DECISION",
            why="Determining what needs to be done",
            verification=f"Included: {included}; Excluded: {excluded}"
        )
    
    def get_summary(self, hours: int = 24):
        """Get summary of recent decisions."""
        if not self.LOG_FILE.exists():
            return []
        
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent = []
        
        try:
            with open(self.LOG_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    ts = datetime.fromisoformat(record['timestamp']).timestamp()
                    if ts >= cutoff:
                        recent.append(record)
        except (IOError, OSError, ValueError, json.JSONDecodeError):
            pass
        
        return recent
    
    def report(self):
        """Print decision summary."""
        recent = self.get_summary()
        
        if not recent:
            print("[DECISION LOG] No decisions logged in last 24 hours.")
            return
        
        print("\n" + "="*70)
        print("DECISION LOG - Last 24 Hours")
        print("="*70 + "\n")
        
        by_type = {}
        for decision in recent:
            dtype = decision['type']
            if dtype not in by_type:
                by_type[dtype] = []
            by_type[dtype].append(decision)
        
        for dtype, decisions in sorted(by_type.items()):
            print(f"[{dtype}] ({len(decisions)} decisions)")
            for d in decisions:
                timestamp = d['timestamp'].split('T')[1][:8]  # HH:MM:SS
                print(f"  {timestamp}: {d['decision']}")
                if d['why']:
                    print(f"    WHY: {d['why']}")
            print()


# Global instance for convenience
_logger = None


def get_logger() -> DecisionLogger:
    """Get or create global decision logger."""
    global _logger
    if _logger is None:
        _logger = DecisionLogger()
    return _logger


def log_decision(
    decision: str,
    decision_type: str = "FRAMEWORK_APPLICATION",
    why: str = "",
    alternatives: Optional[List[str]] = None,
    verification: str = "",
    tags: Optional[List[str]] = None
):
    """Convenience function for logging decisions."""
    get_logger().log(
        decision=decision,
        decision_type=decision_type,
        why=why,
        alternatives=alternatives,
        verification=verification,
        tags=tags
    )


if __name__ == "__main__":
    # Show recent decisions
    logger = get_logger()
    logger.report()
