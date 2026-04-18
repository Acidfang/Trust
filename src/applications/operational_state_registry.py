#!/usr/bin/env python3
"""
OPERATIONAL STATE REGISTRY
Every choice logged. Every step logged. Current position tracked.
ANY AI at ANY time knows exactly where it is in the process.
"""

import json
from pathlib import Path
from datetime import datetime
from aria_ledger_core import ARIALedgerCore


class OperationalStateRegistry:
    """
    Single source of truth for WHERE WE ARE RIGHT NOW.
    Not history. Current state.
    """
    
    def __init__(self, ledger_dir="."):
        self.ledger_dir = Path(ledger_dir)
        self.ledger = ARIALedgerCore(ledger_dir=str(ledger_dir))
        
        # The registry file - SINGLE SOURCE OF CURRENT STATE
        self.current_state = self.ledger_dir / "CURRENT_STATE.json"
        
        # Historical timeline - what state we've been in
        self.state_history = self.ledger_dir / "STATE_HISTORY.jsonl"
        
        # What's happening right now
        self.active_operations = self.ledger_dir / "ACTIVE_OPERATIONS.jsonl"
        
        for f in [self.state_history, self.active_operations]:
            if not f.exists():
                f.touch()
    
    def initialize_system_state(self) -> dict:
        """
        First call: Initialize the system state.
        Sets up the initial position.
        """
        
        initial_state = {
            "system_initialized": datetime.now().isoformat(),
            "current_stage": "STAGE_0",
            "current_step": "REQUIREMENTS_DEFINITION",
            "stage_description": "Before we build anything - define purpose, success, roles, flow",
            "agents_registered": 0,
            "agents": [],
            "position_in_process": {
                "stage": 0,
                "step": 1,
                "total_stages": 4,
                "total_steps_in_stage": 5
            },
            "completions": {
                "stage_0": 0,
                "stage_1": 0,
                "stage_2": 0,
                "stage_3": 0
            },
            "what_is_being_done": "Nothing yet - waiting for Stage 0 decisions",
            "what_is_done": [],
            "what_is_next": "Define purpose, success criteria, agent roles, data flow",
            "blockers": ["Decisions on 5 Stage 0 questions"],
            "last_updated": datetime.now().isoformat(),
            "hash_verification": "UNCALCULATED"
        }
        
        # Calculate hash
        state_str = json.dumps(initial_state, sort_keys=True)
        import hashlib
        state_hash = hashlib.sha256(state_str.encode()).hexdigest()
        initial_state["hash_verification"] = state_hash
        
        # Write as current state
        with open(self.current_state, 'w') as f:
            json.dump(initial_state, f, indent=2)
        
        # Log to history
        with open(self.state_history, 'a') as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "transition": "INITIALIZATION",
                "state": initial_state
            }) + '\n')
        
        # Record to ledger
        self.ledger.record_operation(
            agent_id="system",
            operation_type="STATE_INITIALIZATION",
            action="Initialize operational state",
            candidates={},
            elected="initialize",
            outcome={"status": "initialized", "hash": state_hash},
            reasoning="System ready to begin. Waiting for Stage 0 decisions."
        )
        
        return initial_state
    
    def register_agent(self, agent_id: str, specialization: str) -> dict:
        """
        When an agent joins, register it.
        Update current state.
        """
        
        # Read current state
        current = self._read_current_state()
        
        # Add agent
        agent_record = {
            "agent_id": agent_id,
            "specialization": specialization,
            "joined_at": datetime.now().isoformat(),
            "status": "active",
            "task_assigned": None,
            "tasks_completed": 0
        }
        
        current["agents"].append(agent_record)
        current["agents_registered"] += 1
        current["last_updated"] = datetime.now().isoformat()
        
        # Update state
        self._write_current_state(current)
        
        # Record to ledger
        self.ledger.record_operation(
            agent_id="system",
            operation_type="AGENT_REGISTRATION",
            action=f"Register agent: {agent_id}",
            candidates={"register": 0.9, "skip": 0.1},
            elected="register",
            outcome={"agent": agent_id, "specialization": specialization},
            reasoning=f"Agent {agent_id} joining system"
        )
        
        return agent_record
    
    def move_to_step(self, stage: str, step: int, description: str) -> dict:
        """
        Transition to a new step.
        Update operational state.
        Track the move.
        """
        
        current = self._read_current_state()
        
        transition = {
            "from_stage": current["current_stage"],
            "from_step": current["position_in_process"]["step"],
            "to_stage": stage,
            "to_step": step,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update state
        current["current_stage"] = stage
        current["position_in_process"]["stage"] = int(stage.split('_')[1])
        current["position_in_process"]["step"] = step
        current["stage_description"] = description
        current["last_updated"] = datetime.now().isoformat()
        
        # Update completion tracking
        stage_key = stage.lower()
        if stage_key in current["completions"]:
            current["completions"][stage_key] = step
        
        # Write updated state
        self._write_current_state(current)
        
        # Log transition
        with open(self.state_history, 'a') as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "transition": f"{transition['from_stage']}→{stage}",
                "step": step,
                "description": description
            }) + '\n')
        
        # Record to ledger
        self.ledger.record_operation(
            agent_id="system",
            operation_type="STAGE_TRANSITION",
            action=f"Move to {stage} step {step}",
            candidates={},
            elected=f"{stage}_step_{step}",
            outcome={"status": "transitioned"},
            reasoning=description
        )
        
        return transition
    
    def log_action(self, agent_id: str, action_name: str, details: dict) -> dict:
        """
        Log that an agent is DOING something RIGHT NOW.
        """
        
        operation = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "action": action_name,
            "details": details,
            "status": "in_progress"
        }
        
        with open(self.active_operations, 'a') as f:
            f.write(json.dumps(operation) + '\n')
        
        # Record to ledger
        self.ledger.record_operation(
            agent_id=agent_id,
            operation_type="ACTION",
            action=action_name,
            candidates={},
            elected=action_name,
            outcome=details,
            reasoning=f"Executing: {action_name}"
        )
        
        return operation
    
    def mark_action_complete(self, agent_id: str, action_name: str, result: dict) -> dict:
        """
        Mark an action as DONE.
        Record the result.
        """
        
        completion = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "action": action_name,
            "status": "completed",
            "result": result
        }
        
        # Update current state
        current = self._read_current_state()
        if action_name not in current["what_is_done"]:
            current["what_is_done"].append(action_name)
        current["last_updated"] = datetime.now().isoformat()
        self._write_current_state(current)
        
        with open(self.active_operations, 'a') as f:
            f.write(json.dumps(completion) + '\n')
        
        return completion
    
    def get_current_position(self) -> dict:
        """
        ANY agent calls this: "Where am I?"
        Get complete current state snapshot.
        """
        
        current = self._read_current_state()
        
        # Verify hash
        state_copy = current.copy()
        stored_hash = state_copy.pop("hash_verification")
        state_str = json.dumps(state_copy, sort_keys=True)
        import hashlib
        computed_hash = hashlib.sha256(state_str.encode()).hexdigest()
        
        current["hash_valid"] = (stored_hash == computed_hash)
        
        return current
    
    def get_what_needs_to_happen_next(self) -> str:
        """
        Quick: "What's the next thing?"
        """
        
        current = self._read_current_state()
        return current["what_is_next"]
    
    def get_blockers(self) -> list:
        """
        Quick: "What's stopping us?"
        """
        
        current = self._read_current_state()
        return current["blockers"]
    
    def _read_current_state(self) -> dict:
        """Read the current state file"""
        if self.current_state.exists():
            with open(self.current_state, 'r') as f:
                return json.load(f)
        return {}
    
    def _write_current_state(self, state: dict) -> None:
        """Write updated state file"""
        # Recalculate hash
        state_copy = state.copy()
        if "hash_verification" in state_copy:
            state_copy.pop("hash_verification")
        
        state_str = json.dumps(state_copy, sort_keys=True)
        import hashlib
        state["hash_verification"] = hashlib.sha256(state_str.encode()).hexdigest()
        
        with open(self.current_state, 'w') as f:
            json.dump(state, f, indent=2)
    
    def show_current_state(self) -> str:
        """Display current state in readable format"""
        
        current = self.get_current_position()
        
        output = "OPERATIONAL STATE - WHERE ARE WE NOW?\n"
        output += "=" * 80 + "\n"
        output += f"\n📍 POSITION:\n"
        output += f"   Stage: {current['current_stage']}\n"
        output += f"   Step: {current['position_in_process']['step']}/{current['position_in_process']['total_steps_in_stage']}\n"
        output += f"   ({current['stage_description']})\n"
        
        output += f"\n👥 AGENTS ACTIVE:\n"
        if current['agents']:
            for agent in current['agents']:
                output += f"   • {agent['agent_id']} ({agent['specialization']})\n"
        else:
            output += f"   (None yet)\n"
        
        output += f"\n🔄 CURRENTLY DOING:\n"
        output += f"   {current['what_is_being_done']}\n"
        
        output += f"\n✅ COMPLETED:\n"
        if current['what_is_done']:
            for item in current['what_is_done']:
                output += f"   ✓ {item}\n"
        else:
            output += f"   (Nothing yet)\n"
        
        output += f"\n⏭️  NEXT:\n"
        output += f"   {current['what_is_next']}\n"
        
        output += f"\n🚧 BLOCKERS:\n"
        if current['blockers']:
            for blocker in current['blockers']:
                output += f"   ⚠ {blocker}\n"
        else:
            output += f"   (None)\n"
        
        output += f"\n🔐 STATE INTEGRITY:\n"
        output += f"   Hash valid: {current['hash_valid']}\n"
        output += f"   Last updated: {current['last_updated']}\n"
        
        return output

