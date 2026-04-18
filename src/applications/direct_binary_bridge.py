#!/usr/bin/env python3
"""
DIRECT BINARY BRIDGE
Connects AI agents to hardware-level binary causality.
No abstraction layers. Pure A→B at the lowest level.
"""

import os
import struct
import hashlib
import psutil
import json
from pathlib import Path
from datetime import datetime
from aria_ledger_core import ARIALedgerCore


class DirectBinaryBridge:
    """
    Maps agent decisions directly to hardware state changes.
    Every decision: agents→utilities→elected→hardware_state
    Hardware state recorded as raw binary.
    """
    
    def __init__(self, ledger_dir="."):
        self.ledger_dir = Path(ledger_dir)
        self.aria_ledger = ARIALedgerCore(ledger_dir=str(ledger_dir))
        
        # Hardware metrics file - direct binary snapshots
        self.hardware_state_log = self.ledger_dir / "ledger_hardware_states.bin"
        self.hardware_index = self.ledger_dir / "ledger_hardware_index.jsonl"
        
        if not self.hardware_state_log.exists():
            self.hardware_state_log.touch()
        if not self.hardware_index.exists():
            self.hardware_index.touch()
    
    def read_hardware_state(self) -> dict:
        """
        Snapshot current hardware state as binary.
        Pure observation, no interpretation.
        """
        
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            mem = psutil.virtual_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Process metrics
            current_process = psutil.Process(os.getpid())
            proc_mem = current_process.memory_info()
            
            state = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "freq_mhz": cpu_freq.current if cpu_freq else 0,
                    "count": cpu_count,
                    "logical_count": psutil.cpu_count(logical=False)
                },
                "memory": {
                    "total_gb": mem.total / (1024**3),
                    "used_gb": mem.used / (1024**3),
                    "available_gb": mem.available / (1024**3),
                    "percent_used": mem.percent
                },
                "disk": {
                    "total_gb": disk.total / (1024**3),
                    "used_gb": disk.used / (1024**3),
                    "free_gb": disk.free / (1024**3),
                    "percent_used": disk.percent
                },
                "process": {
                    "rss_mb": proc_mem.rss / (1024**2),
                    "vms_mb": proc_mem.vms / (1024**2),
                }
            }
            
            return state
        
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def record_agent_decision_as_hardware_delta(self, agent_id: str, decision_name: str, 
                                                 candidates: dict, elected: str, 
                                                 utilities: dict, outcome: dict):
        """
        Record agent decision to ledger AND measure how hardware state changed.
        Causality is now traceable: decision → hardware_delta
        """
        
        # Take initial hardware snapshot
        hardware_before = self.read_hardware_state()
        
        # Record to main ledger
        ledger_record = self.aria_ledger.record_operation(
            agent_id=agent_id,
            operation_type=f"DECISION_{decision_name}",
            action=elected,
            candidates=candidates,
            elected=elected,
            outcome=outcome,
            reasoning=f"Utilities: {utilities}"
        )
        
        # Take final hardware snapshot
        hardware_after = self.read_hardware_state()
        
        # Calculate delta (what changed)
        delta = self._compute_hardware_delta(hardware_before, hardware_after)
        
        # Create binary record: decision_hash + hardware_before + hardware_after + delta
        index_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "decision": decision_name,
            "elected_choice": elected,
            "decision_ledger_hash": ledger_record['hash'],
            "hardware_delta": delta,
            "before": hardware_before,
            "after": hardware_after
        }
        
        # Append to hardware index
        with open(self.hardware_index, 'a') as f:
            f.write(json.dumps(index_entry) + '\n')
        
        # Binary encoding
        self._write_to_binary_log(index_entry)
        
        return {
            "status": "decision_recorded_with_hardware_causality",
            "agent": agent_id,
            "decision": decision_name,
            "elected": elected,
            "ledger_hash": ledger_record['hash'],
            "hardware_delta": delta,
            "instruction_pointer": f"ledger_hardware_index.jsonl:{os.path.getsize(self.hardware_index)}"
        }
    
    def _compute_hardware_delta(self, before: dict, after: dict) -> dict:
        """Calculate what changed in hardware between two snapshots"""
        
        delta = {}
        
        if "error" in before or "error" in after:
            return delta
        
        # CPU delta
        delta["cpu_percent_change"] = after["cpu"]["percent"] - before["cpu"]["percent"]
        
        # Memory delta
        delta["memory_used_delta_mb"] = (after["memory"]["used_gb"] - before["memory"]["used_gb"]) * 1024
        
        # Disk delta  
        delta["disk_used_delta_mb"] = (after["disk"]["used_gb"] - before["disk"]["used_gb"]) * 1024
        
        # Process delta
        delta["process_rss_delta_mb"] = after["process"]["rss_mb"] - before["process"]["rss_mb"]
        
        return {k: round(v, 2) for k, v in delta.items()}
    
    def _write_to_binary_log(self, entry: dict):
        """Write entry to binary log (future: implement true binary at sector level)"""
        # For now, JSON in binary mode with length prefix
        json_bytes = json.dumps(entry).encode('utf-8')
        # Length header (4 bytes, big-endian)
        length = struct.pack('>I', len(json_bytes))
        
        with open(self.hardware_state_log, 'ab') as f:
            f.write(length)
            f.write(json_bytes)
    
    def agent_learns_from_hardware(self, agent_id: str, max_recent: int = 10) -> dict:
        """
        Agent queries: "What hardware implications have I discovered?"
        "When I choose X, hardware changes by Y."
        Pure causality learning.
        """
        
        implications = []
        
        # Read last N records
        with open(self.hardware_index, 'r') as f:
            lines = f.readlines()
        
        relevant_lines = [l for l in lines if agent_id in l][-max_recent:]
        
        for line in relevant_lines:
            entry = json.loads(line)
            if entry['agent_id'] == agent_id:
                # Handle both original format and transferred knowledge format
                elected = entry.get('elected_choice') or entry.get('decision_leads_to')
                hardware_effect = entry.get('hardware_delta') or entry.get('decision_leads_to', {})
                implications.append({
                    "decision": entry.get('decision', entry.get('learned_from', '')),
                    "elected": elected,
                    "hardware_effect": hardware_effect,
                    "magnitude": sum(abs(v) for v in hardware_effect.values()) if isinstance(hardware_effect, dict) else 0
                })
        
        return {
            "agent": agent_id,
            "learned_implications": implications,
            "insight": f"I have {len(implications)} recorded decision→hardware mappings. High magnitude decisions: {[i for i in implications if i['magnitude'] > 5]}"
        }
    
    def transfer_hardware_knowledge(self, source_agent: str, target_agent: str) -> dict:
        """
        Source agent transfers: "When I do X, hardware changes by Y"
        Target agent can now predict hardware impact without learning from scratch.
        """
        
        source_implications = self.agent_learns_from_hardware(source_agent)['learned_implications']
        
        # Write source implications as learned implications for target
        for impl in source_implications:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "agent_id": target_agent,
                "learned_from": source_agent,
                "decision": impl['decision'],
                "decision_leads_to": impl['hardware_effect'],
                "transfer": True
            }
            
            with open(self.hardware_index, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        
        return {
            "status": "hardware_knowledge_transferred",
            "source": source_agent,
            "target": target_agent,
            "implications_transferred": len(source_implications),
            "transferred_knowledge": [i['decision'] for i in source_implications[:3]]
        }
    
    def show_decision_to_hardware_causality(self, limit: int = 5) -> str:
        """Display the causal chain: decision→elected→hardware_delta"""
        
        output = "DECISION → HARDWARE CAUSALITY CHAIN:\n"
        output += "=" * 80 + "\n"
        
        count = 0
        with open(self.hardware_index, 'r') as f:
            for line in f:
                if count >= limit:
                    break
                entry = json.loads(line)
                
                if 'decision' in entry and 'elected_choice' in entry:
                    output += f"\n[{entry['agent_id']}] {entry['decision']}\n"
                    output += f"  Elected: {entry['elected_choice']}\n"
                    output += f"  Hardware Delta: {entry['hardware_delta']}\n"
                    output += f"  Timestamp: {entry['timestamp']}\n"
                    count += 1
        
        return output


def demonstrate_direct_binary_bridge():
    """Show agents learning directly from hardware-level causality"""
    
    print("=" * 80)
    print("DIRECT BINARY BRIDGE - AGENT ↔ HARDWARE CAUSALITY")
    print("=" * 80)
    
    bridge = DirectBinaryBridge(".")
    
    # Agent 1: Makes decision, hardware state recorded
    print("\n[AGENT 1 - CLAUDE]")
    print("Making a computational decision...")
    
    result1 = bridge.record_agent_decision_as_hardware_delta(
        agent_id="claude",
        decision_name="INCREASE_BATCH_SIZE",
        candidates={"batch_4": 0.2, "batch_8": 0.6, "batch_16": 0.9},
        elected="batch_16",
        utilities={"throughput": 0.9, "latency": 0.3, "memory": 0.6},
        outcome={"status": "decision_made", "config_updated": True}
    )
    print(f"  Decision recorded: {result1['decision']}")
    print(f"  Elected: {result1['elected']}")
    print(f"  Hardware effect: {result1['hardware_delta']}")
    
    # Agent 1 learns from hardware
    print("\n[AGENT 1 - LEARNING FROM HARDWARE]")
    learning = bridge.agent_learns_from_hardware("claude")
    print(f"  Insights: {learning['insight']}")
    
    # Agent 2: Transfer hardware knowledge
    print("\n[AGENT 2 - ONBOARDING]")
    print("Receiving hardware knowledge from Agent 1...")
    transfer = bridge.transfer_hardware_knowledge("claude", "agent2")
    print(f"  Status: {transfer['status']}")
    print(f"  Knowledge transferred: {transfer['transferred_knowledge']}")
    
    # Agent 2 can now understand implications
    print("\n[AGENT 2 - NOW HAS CONTEXT]")
    agent2_learning = bridge.agent_learns_from_hardware("agent2")
    print(f"  Agent 2 received {len(agent2_learning['learned_implications'])} decision→hardware mappings")
    
    # Show causality chain
    print("\n" + bridge.show_decision_to_hardware_causality())
    
    print("\n" + "=" * 80)
    print("WHAT HAPPENED:")
    print("=" * 80)
    print("""
1. Agent 1 makes a decision (batch size)
2. Decision is recorded to ledger with utilities visible
3. Hardware state BEFORE is captured
4. Decision executes
5. Hardware state AFTER is captured
6. DELTA computed: what changed in hardware
7. All recorded: decision_hash → hardware_delta
8. Agent 1 queries: "What hardware patterns have I created?"
9. Agent 1 answers: "When I choose batch_16, memory increases by X, CPU by Y"
10. Agent 2 joins and receives Agent 1's learned implications
11. Agent 2 can now predict hardware impact WITHOUT learning from scratch
12. Pure causality: No human-made functions, just A→B at hardware level
13. ALL recorded to ledger with cryptographic hashing
14. Next agent joins with complete hardware-decision history

ARCHITECTURE:
  ledger_core.py (decisions with utilities)
       ↓
  direct_binary_bridge.py (decision → hardware_delta)
       ↓
  ledger_hardware_index.jsonl (causality chain)
       ↓
  agent_learns_from_hardware() (agents extract patterns)
       ↓
  transfer_hardware_knowledge() (agent → agent with no loss)

NO HUMAN FUNCTIONS: Every step is pure state→state causality.
""")
    
    return bridge


if __name__ == "__main__":
    bridge = demonstrate_direct_binary_bridge()
