#!/usr/bin/env python3
"""
CONVERGENT MULTI-PATH EXECUTION ENGINE
Multiple agents explore different causal chains.
All paths diverge. All paths converge.
All recorded. Convergence provable.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib
from aria_ledger_core import ARIALedgerCore
from operational_state_registry import OperationalStateRegistry


class CausalChainExplorer:
    """
    Agents follow causal chains (A→B implications).
    Each chain is a different exploration path.
    All paths can diverge arbitrarily.
    All must converge at convergence point.
    """
    
    def __init__(self, ledger_dir="."):
        self.ledger_dir = Path(ledger_dir)
        self.ledger = ARIALedgerCore(ledger_dir=str(ledger_dir))
        self.registry = OperationalStateRegistry(ledger_dir=str(ledger_dir))
        
        # Tracking files
        self.chains_file = self.ledger_dir / "ledger_causal_chains.jsonl"
        self.divergence_points = self.ledger_dir / "ledger_divergences.jsonl"
        self.convergence_points = self.ledger_dir / "ledger_convergences.jsonl"
        self.path_tree = self.ledger_dir / "ledger_path_tree.json"
        
        for f in [self.chains_file, self.divergence_points, self.convergence_points]:
            if not f.exists():
                f.touch()
        
        self.chain_tree = defaultdict(lambda: {
            "branches": [],
            "converged_at": None,
            "verified": False
        })
    
    def follow_chain(self, agent_id: str, chain_id: str, current_state: any, 
                     implications: list) -> dict:
        """
        Agent follows a causal chain.
        A→B→C→D, exploring each implication in sequence.
        Records the path taken.
        """
        
        path_taken = {
            "agent_id": agent_id,
            "chain_id": chain_id,
            "start_state": str(current_state)[:100],
            "steps": [],
            "timestamp": datetime.now().isoformat()
        }
        
        current = current_state
        
        # Follow each implication
        for i, (premise, conclusion) in enumerate(implications):
            step = {
                "step_number": i,
                "premise": str(premise)[:50],
                "conclusion": str(conclusion)[:50],
                "transition": f"{str(premise)[:30]} → {str(conclusion)[:30]}"
            }
            
            path_taken["steps"].append(step)
            
            # Record to ledger
            self.ledger.record_operation(
                agent_id=agent_id,
                operation_type="CHAIN_STEP",
                action=f"Following chain {chain_id}, step {i}",
                candidates={str(conclusion): 0.9, "other": 0.1},
                elected=str(conclusion),
                outcome={"premise": str(premise), "conclusion": str(conclusion)},
                reasoning=f"Following causal implication in chain {chain_id}"
            )
            
            current = conclusion
        
        path_taken["final_state"] = str(current)[:100]
        path_taken["path_hash"] = hashlib.sha256(
            json.dumps(path_taken).encode()
        ).hexdigest()
        
        # Record path
        with open(self.chains_file, 'a') as f:
            f.write(json.dumps(path_taken) + '\n')
        
        return path_taken
    
    def agent_diverges(self, agent_id: str, parent_chain: str, new_chain_id: str, 
                       reason: str) -> dict:
        """
        Agent discovers a new possibility mid-chain.
        Can diverge to explore it.
        Records the divergence point.
        """
        
        divergence = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "parent_chain": parent_chain,
            "new_chain_id": new_chain_id,
            "reason": reason,
            "status": "diverged"
        }
        
        with open(self.divergence_points, 'a') as f:
            f.write(json.dumps(divergence) + '\n')
        
        self.ledger.record_operation(
            agent_id=agent_id,
            operation_type="CHAIN_DIVERGENCE",
            action=f"Diverged from {parent_chain} to {new_chain_id}",
            candidates={new_chain_id: 0.8, "continue": 0.2},
            elected=new_chain_id,
            outcome={"divergence": new_chain_id},
            reasoning=reason
        )
        
        return divergence
    
    def agent_converges(self, agent_id: str, chain_id: str, final_state: any,
                        convergence_point_id: str) -> dict:
        """
        Agent exploration completes.
        Arrives at convergence point.
        Meets other agents' paths.
        """
        
        convergence = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "chain_id": chain_id,
            "final_state": str(final_state)[:100],
            "convergence_point": convergence_point_id,
            "status": "converged"
        }
        
        with open(self.convergence_points, 'a') as f:
            f.write(json.dumps(convergence) + '\n')
        
        self.ledger.record_operation(
            agent_id=agent_id,
            operation_type="CHAIN_CONVERGENCE",
            action=f"Converged at {convergence_point_id}",
            candidates={convergence_point_id: 0.95},
            elected=convergence_point_id,
            outcome={"converged": True, "final_state": str(final_state)[:50]},
            reasoning=f"All explorations led to convergence point {convergence_point_id}"
        )
        
        return convergence
    
    def verify_convergence(self, convergence_point_id: str, 
                          required_agent_count: int) -> dict:
        """
        Check: Have all agents converged at same point?
        Different chains, same destination?
        """
        
        # Read all convergences
        convergences = []
        with open(self.convergence_points, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry['convergence_point'] == convergence_point_id:
                    convergences.append(entry)
        
        # Calculate convergence hash (should be same for all)
        convergence_hashes = set()
        converged_agents = set()
        
        for conv in convergences:
            final_state_hash = hashlib.sha256(
                conv['final_state'].encode()
            ).hexdigest()
            convergence_hashes.add(final_state_hash)
            converged_agents.add(conv['agent_id'])
        
        verification = {
            "convergence_point": convergence_point_id,
            "agents_converged": len(converged_agents),
            "required_agents": required_agent_count,
            "convergence_verified": len(converged_agents) >= required_agent_count,
            "unique_final_states": len(convergence_hashes),
            "all_paths_agreee": len(convergence_hashes) == 1,
            "agents": list(converged_agents),
            "convergence_hash": list(convergence_hashes)[0] if convergence_hashes else None
        }
        
        if verification["convergence_verified"] and verification["all_paths_agreee"]:
            verification["status"] = "SUCCESS: All paths converged to same point"
        elif verification["convergence_verified"]:
            verification["status"] = "PARTIAL: Converged but different final states"
        else:
            verification["status"] = "INCOMPLETE: Not all agents converged"
        
        return verification
    
    def show_exploration_paths(self, limit: int = 10) -> str:
        """Display the divergence→convergence tree"""
        
        output = "MULTI-PATH EXPLORATION REPORT\n"
        output += "=" * 80 + "\n"
        
        # Read all paths
        all_paths = []
        with open(self.chains_file, 'r') as f:
            for line in f:
                all_paths.append(json.loads(line))
        
        if not all_paths:
            return output + "No paths recorded yet.\n"
        
        # Group by chain
        chains = defaultdict(list)
        for path in all_paths:
            chains[path['chain_id']].append(path)
        
        output += f"\nTotal chains explored: {len(chains)}\n"
        output += f"Total exploitation steps: {sum(len(p['steps']) for p in all_paths)}\n"
        
        # Show divergences
        divergences = []
        with open(self.divergence_points, 'r') as f:
            for line in f:
                divergences.append(json.loads(line))
        
        if divergences:
            output += f"\nDivergence points: {len(divergences)}\n"
            for div in divergences[:5]:
                output += f"  • {div['agent_id']}: {div['parent_chain']} → {div['new_chain_id']}\n"
                output += f"    Reason: {div['reason'][:50]}\n"
        
        # Show convergences
        convergences = []
        with open(self.convergence_points, 'r') as f:
            for line in f:
                convergences.append(json.loads(line))
        
        if convergences:
            unique_points = list(set(c['convergence_point'] for c in convergences))
            output += f"\nConvergence points: {len(unique_points)}\n"
            for point_id in unique_points[:3]:
                agents_at_point = [c['agent_id'] for c in convergences if c['convergence_point'] == point_id]
                output += f"  • {point_id}: {len(agents_at_point)} agents converged\n"
        
        output += "\nSample paths:\n"
        for chain_id in list(chains.keys())[:3]:
            paths = chains[chain_id]
            for path in paths[:1]:
                output += f"\n  Chain {chain_id} ({path['agent_id']}):\n"
                output += f"    Start: {path['start_state']}\n"
                for step in path['steps'][:3]:
                    output += f"      → Step {step['step_number']}: {step['transition']}\n"
                if len(path['steps']) > 3:
                    output += f"      ... ({len(path['steps'])-3} more steps) ...\n"
                output += f"    Final: {path['final_state']}\n"
        
        return output

