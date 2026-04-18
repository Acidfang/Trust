#!/usr/bin/env python3
"""
ARIA LEDGER CORE - THE SINGLE SOURCE OF TRUTH

This must be built and running FIRST before any other component.
Every agent writes here. Every decision auditable. Every handoff possible.

NO hidden logic. NO assumed context. Everything recorded.
"""

import json
import os
import hashlib
import time
from datetime import datetime
from pathlib import Path

# ============================================================================
# LEDGER CORE - IMMUTABLE RECORD
# ============================================================================

class ARIALedgerCore:
    """
    Single source of truth for entire project.
    Append-only. Immutable. Auditable.
    """
    
    def __init__(self, ledger_dir="."):
        self.ledger_dir = ledger_dir
        Path(ledger_dir).mkdir(exist_ok=True)
        
        # Core files - these are the backbone
        self.ledger_community = os.path.join(ledger_dir, "ledger_community.jsonl")
        self.ledger_decisions = os.path.join(ledger_dir, "ledger_decisions.jsonl")
        self.ledger_bootstrap = os.path.join(ledger_dir, "ledger_bootstrap.jsonl")
        self.agents_registry = os.path.join(ledger_dir, "agents_registry.json")
        
        # Ensure files exist
        for f in [self.ledger_community, self.ledger_decisions, self.ledger_bootstrap]:
            Path(f).touch()
        
        # Initialize agent registry
        if not os.path.exists(self.agents_registry):
            self._init_registry()
        
        # Track this session
        self.session_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.session_start = datetime.now().isoformat()
    
    def _init_registry(self):
        """Initialize empty agent registry"""
        registry = {
            "agents": [],
            "created": datetime.now().isoformat(),
            "schema_version": "1.0"
        }
        with open(self.agents_registry, 'w') as f:
            json.dump(registry, f, indent=2)
    
    # ============================================================================
    # BOOTSTRAP LOGGING - Record startup decisions
    # ============================================================================
    
    def log_bootstrap(self, stage, decision, candidates, elected, reasoning):
        """
        Log bootstrap decisions - how did we decide to start?
        
        Must include: What were the options? What was chosen? Why?
        """
        record = {
            "timestamp": time.time(),
            "stage": stage,
            "decision": decision,
            "candidates": candidates,
            "elected": elected,
            "reasoning": reasoning,
            "session_id": self.session_id
        }
        
        with open(self.ledger_bootstrap, 'a') as f:
            f.write(json.dumps(record) + '\n')
        
        return record
    
    # ============================================================================
    # OPERATION RECORDING - Every agent records here
    # ============================================================================
    
    def record_operation(self, agent_id, operation_type, action, candidates, elected, outcome, reasoning=""):
        """
        SINGLE POINT OF ENTRY for all agent operations.
        
        This is where accountability lives. Every call records who did what.
        """
        record = {
            "timestamp": time.time(),
            "timestamp_iso": datetime.now().isoformat(),
            "agent_id": agent_id,
            "session_id": self.session_id,
            "operation_type": operation_type,
            "action": action,
            "candidates": candidates,
            "elected": elected,
            "outcome": outcome,
            "reasoning": reasoning,
            "hash": self._compute_hash(agent_id, action, elected, outcome)
        }
        
        # Append to community ledger (ALL operations)
        with open(self.ledger_community, 'a') as f:
            f.write(json.dumps(record) + '\n')
        
        # ALSO append to decision-specific ledger for queries
        with open(self.ledger_decisions, 'a') as f:
            f.write(json.dumps(record) + '\n')
        
        return record
    
    # ============================================================================
    # AGENT REGISTRY - Every agent tracked
    # ============================================================================
    
    def register_agent(self, agent_id, agent_name, role, component):
        """Register an agent in the system"""
        with open(self.agents_registry, 'r') as f:
            registry = json.load(f)
        
        agent_record = {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "role": role,
            "component": component,
            "registered_at": datetime.now().isoformat(),
            "session_id": self.session_id,
            "status": "active"
        }
        
        registry["agents"].append(agent_record)
        
        with open(self.agents_registry, 'w') as f:
            json.dump(registry, f, indent=2)
        
        # Log registration as bootstrap decision
        self.log_bootstrap(
            stage="AGENT_REGISTRATION",
            decision=f"Register {agent_name}",
            candidates={f"register_{agent_name}": 0.9, "skip": 0.1},
            elected=f"register_{agent_name}",
            reasoning=f"{agent_name} joining for {component}"
        )
        
        return agent_record
    
    # ============================================================================
    # QUERY FUNCTIONS - Read what happened
    # ============================================================================
    
    def get_full_history(self):
        """Get complete history from ledger"""
        records = []
        try:
            with open(self.ledger_community, 'r') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        except:
            pass
        return records
    
    def get_agent_history(self, agent_id):
        """Get all operations by specific agent"""
        records = []
        try:
            with open(self.ledger_community, 'r') as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        if record.get("agent_id") == agent_id:
                            records.append(record)
        except:
            pass
        return records
    
    def get_session_history(self, session_id):
        """Get all operations in specific session"""
        records = []
        try:
            with open(self.ledger_community, 'r') as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        if record.get("session_id") == session_id:
                            records.append(record)
        except:
            pass
        return records
    
    def get_bootstrap_decisions(self):
        """What decisions were made at startup?"""
        records = []
        try:
            with open(self.ledger_bootstrap, 'r') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        except:
            pass
        return records
    
    def get_agents_registry(self):
        """Who's in the system?"""
        try:
            with open(self.agents_registry, 'r') as f:
                return json.load(f)
        except:
            return {"agents": []}
    
    # ============================================================================
    # INTEGRITY VERIFICATION
    # ============================================================================
    
    def verify_integrity(self):
        """Can another AI trust this ledger?"""
        checks = {
            "ledger_exists": os.path.exists(self.ledger_community),
            "readable": False,
            "well_formed": True,
            "all_hashes_valid": True,
            "total_operations": 0,
            "summary": ""
        }
        
        try:
            with open(self.ledger_community, 'r') as f:
                lines = f.readlines()
                checks["readable"] = True
                checks["total_operations"] = len(lines)
                
                for line in lines:
                    try:
                        record = json.loads(line.strip())
                        # Verify structure
                        required_fields = ["timestamp", "agent_id", "operation_type", "elected", "hash"]
                        for field in required_fields:
                            if field not in record:
                                checks["well_formed"] = False
                        
                        # Verify hash
                        expected_hash = self._compute_hash(
                            record["agent_id"],
                            record["action"],
                            record["elected"],
                            record["outcome"]
                        )
                        if record["hash"] != expected_hash:
                            checks["all_hashes_valid"] = False
                    except:
                        checks["well_formed"] = False
        except:
            checks["readable"] = False
        
        checks["summary"] = "✓ VALID" if all([
            checks["ledger_exists"],
            checks["readable"],
            checks["well_formed"],
            checks["all_hashes_valid"]
        ]) else "✗ INVALID"
        
        return checks
    
    # ============================================================================
    # HANDOFF SUPPORT - Next AI can continue
    # ============================================================================
    
    def export_for_next_agent(self, next_agent_id):
        """
        What must the next agent know to continue?
        """
        history = self.get_full_history()
        bootstrap = self.get_bootstrap_decisions()
        agents = self.get_agents_registry()
        
        handoff = {
            "session_id": self.session_id,
            "session_start": self.session_start,
            "session_end": datetime.now().isoformat(),
            "total_operations": len(history),
            "agents_active": len(agents["agents"]),
            "bootstrap_decisions": bootstrap,
            "current_state": {
                "agents": agents["agents"],
                "last_10_operations": history[-10:] if history else []
            },
            "next_agent_id": next_agent_id,
            "ledger_path": self.ledger_community,
            "verification": self.verify_integrity()
        }
        
        return handoff
    
    # ============================================================================
    # UTILITY FUNCTIONS
    # ============================================================================
    
    def _compute_hash(self, agent_id, action, elected, outcome):
        """Compute operation hash for integrity checking"""
        data = json.dumps([agent_id, action, elected, str(outcome)], sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:16]


# ============================================================================
# STARTUP - Bootstrap the system
# ============================================================================

def bootstrap_aria_system():
    """
    First thing EVER that runs - set up the ledger.
    Before ANY building, BEFORE ANY DECISIONS - the ledger exists.
    """
    
    ledger = ARIALedgerCore(ledger_dir=".")
    
    print("=" * 70)
    print("ARIA SYSTEM BOOTSTRAP")
    print("=" * 70)
    
    # Decision 1: Confirm ledger is primary
    print("\n[BOOTSTRAP] Decision 1: What is source of truth?")
    candidates = {
        "code": 0.2,
        "documentation": 0.3,
        "ledger": 0.95
    }
    elected = "ledger"
    print(f"  Candidates: {candidates}")
    print(f"  Elected: {elected} (immutable record)")
    
    ledger.log_bootstrap(
        stage="SOURCE_OF_TRUTH",
        decision="What is single source of truth?",
        candidates=candidates,
        elected=elected,
        reasoning="Only ledger is immutable, auditable, handoff-capable"
    )
    
    # Decision 2: Register initial agent (Claude - this agent)
    print("\n[BOOTSTRAP] Decision 2: Register first agent")
    ledger.register_agent(
        agent_id="claude-bootstrap",
        agent_name="Claude Copilot",
        role="Bootstrap + Core Implementation",
        component="aria_ledger_core.py + aria_system_interface.py"
    )
    print("  ✓ Claude registered")
    
    # Decision 3: Confirm structure
    print("\n[BOOTSTRAP] Decision 3: Confirm ledger structure")
    ledger.log_bootstrap(
        stage="LEDGER_STRUCTURE",
        decision="What ledger files needed?",
        candidates={
            "unified": 0.4,
            "separate_by_type": 0.5,
            "separate_by_agent": 0.7,
            "all_three": 0.95
        },
        elected="all_three",
        reasoning="Enables querying by agent, type, or full history"
    )
    print("  ✓ Ledger structure decided")
    
    # Verification
    print("\n[BOOTSTRAP] Verification:")
    verification = ledger.verify_integrity()
    for key, value in verification.items():
        if key != "summary":
            print(f"  {key}: {value}")
    print(f"  Status: {verification['summary']}")
    
    print("\n" + "=" * 70)
    print("BOOTSTRAP COMPLETE - Ledger ready for building")
    print("=" * 70)
    print(f"\nSession ID: {ledger.session_id}")
    print(f"Next agent can read: ledger_community.jsonl")
    print(f"Every agent must call: ledger.record_operation()")
    
    return ledger


# ============================================================================
# ACCOUNTABILITY - Print what happened
# ============================================================================

def print_accountability_report(ledger):
    """What was done? Who did it? Why? Complete audit trail."""
    
    print("\n" + "=" * 70)
    print("ACCOUNTABILITY REPORT")
    print("=" * 70)
    
    history = ledger.get_full_history()
    bootstrap = ledger.get_bootstrap_decisions()
    agents = ledger.get_agents_registry()
    
    print(f"\nSession: {ledger.session_id}")
    print(f"Started: {ledger.session_start}")
    print(f"\nAgents active: {len(agents['agents'])}")
    for agent in agents["agents"]:
        print(f"  - {agent['agent_id']}: {agent['agent_name']} ({agent['role']})")
    
    print(f"\nBootstrap decisions: {len(bootstrap)}")
    for decision in bootstrap:
        print(f"  [{decision['stage']}] Elected: {decision['elected']}")
        print(f"    Reasoning: {decision['reasoning']}")
    
    print(f"\nTotal operations: {len(history)}")
    if history:
        print("\nLast 5 operations:")
        for op in history[-5:]:
            print(f"  [{op['timestamp_iso']}] {op['agent_id']}")
            print(f"    Operation: {op['operation_type']}")
            print(f"    Elected: {op['elected']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # First startup ever
    ledger = bootstrap_aria_system()
    print_accountability_report(ledger)
    
    # Save ledger reference for other components
    with open("ledger_reference.json", "w") as f:
        json.dump({
            "session_id": ledger.session_id,
            "ledger_path": ledger.ledger_dir,
            "bootstrap_complete": True
        }, f, indent=2)
    
    print("\nLedger reference saved to: ledger_reference.json")
    print("Other components can now import: from aria_ledger_core import ARIALedgerCore")
