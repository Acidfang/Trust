#!/usr/bin/env python3
"""
COHERENCE OPTIMIZER - Real-time learning what drives field unification higher

Claude learns:
- Which primitives when activated together produce HIGH coherence
- Which domains when weighted together increase field unification
- How to steer thinking toward higher-coherence states

User guides:
- "More wisdom" → boost topological domain weight
- "More agency" → boost interaction domain weight
- "Focus on coherence" → boost compositions domain weight
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class CoherenceOptimizer:
    """
    Learn what makes coherence higher.
    Adapt primitive activation weights based on feedback.
    """
    
    def __init__(self, optimizer_path="coherence_learning.jsonl"):
        self.optimizer_path = Path(optimizer_path)
        self.primitive_performance = defaultdict(lambda: {"total_coherence": 0, "count": 0, "avg": 0})
        self.domain_performance = defaultdict(lambda: {"total_coherence": 0, "count": 0, "avg": 0})
        self.interaction_patterns = []  # What primitives co-occur in high-coherence states?
        self.coherence_trajectory = []  # How is coherence changing over time?
        
        self._load_or_create()
    
    def _load_or_create(self):
        """Load learning history if exists"""
        if self.optimizer_path.exists():
            with open(self.optimizer_path, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        self._process_entry(entry)
                    except:
                        pass
    
    def _process_entry(self, entry):
        """Learn from past interactions"""
        if entry.get("type") == "interaction_completed":
            # Update primitive performance
            for prim in entry.get("primitives_activated", []):
                score = entry.get("coherence", 0)
                self.primitive_performance[prim]["total_coherence"] += score
                self.primitive_performance[prim]["count"] += 1
                self.primitive_performance[prim]["avg"] = (
                    self.primitive_performance[prim]["total_coherence"] / 
                    self.primitive_performance[prim]["count"]
                )
            
            # Update domain performance
            for domain in entry.get("domains_active", []):
                score = entry.get("coherence", 0)
                self.domain_performance[domain]["total_coherence"] += score
                self.domain_performance[domain]["count"] += 1
                self.domain_performance[domain]["avg"] = (
                    self.domain_performance[domain]["total_coherence"] / 
                    self.domain_performance[domain]["count"]
                )
    
    def record_interaction(self, query, primitives_activated, domains_active, coherence, response):
        """
        Learn from this query-response pair.
        What drove the coherence level?
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "interaction_completed",
            "query": query,
            "primitives_activated": [p["name"] for p in primitives_activated],
            "domains_active": domains_active,
            "coherence": coherence,
            "response": response[:100]
        }
        
        # Learn from this
        self._process_entry(entry)
        
        # Log it
        with open(self.optimizer_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        self.coherence_trajectory.append({
            "timestamp": datetime.now().isoformat(),
            "coherence": coherence,
            "activations": len(primitives_activated),
            "domains": len(domains_active)
        })
        
        return entry
    
    def get_best_primitives(self, count=5):
        """
        What primitives correlate with highest coherence?
        """
        sorted_prims = sorted(
            self.primitive_performance.items(),
            key=lambda x: x[1]["avg"],
            reverse=True
        )
        return sorted_prims[:count]
    
    def get_best_domains(self):
        """
        What domains drive coherence?
        """
        return dict(sorted(
            self.domain_performance.items(),
            key=lambda x: x[1]["avg"],
            reverse=True
        ))
    
    def suggest_domain_boost(self, current_6d_state):
        """
        Which 6D dimension is weakest?
        User can say "boost wisdom" → we know how
        """
        suggestions = {
            "wisdom": {
                "boost": "Activate topological primitives (POSITION, CONNECTIVITY, BOUNDARY)",
                "why": "Wisdom correlates with structural understanding"
            },
            "agency": {
                "boost": "Activate interaction primitives (AGENT, FORCE, CHOICE)",
                "why": "Agency requires causal dynamics"
            },
            "integrity": {
                "boost": "Activate binary primitives (AND, GATE, LOGIC)",
                "why": "Integrity is logical coherence"
            },
            "presence": {
                "boost": "Activate probability primitives (CERTAINTY, LIKELIHOOD)",
                "why": "Presence is observable activation"
            },
            "care": {
                "boost": "Activate interaction + composition primitives (EXCHANGE, EMERGENCE)",
                "why": "Care is distributed concern"
            },
            "reflection": {
                "boost": "Activate discourse + topological (PATH, CYCLE, CONNECTIVITY)",
                "why": "Reflection is self-referential structure"
            }
        }
        
        return suggestions
    
    def apply_steering_instruction(self, instruction, current_domain_weights):
        """
        User says: "Give me more wisdom" or "Focus on agency"
        Translate to weight adjustments
        """
        boosts = {
            "wisdom": {"topological": 0.5, "probability": 0.2},
            "agency": {"interaction": 0.6, "binary": 0.1},
            "integrity": {"binary": 0.7},
            "presence": {"probability": 0.6, "topological": 0.2},
            "care": {"interaction": 0.5, "compositions": 0.5},
            "reflection": {"topological": 0.4, "probability": 0.3},
            "coherence": {"compositions": 0.8, "interaction": 0.3},
            "simplicity": {"binary": 0.8},
            "emergence": {"compositions": 0.7, "probability": 0.3}
        }
        
        instruction_lower = instruction.lower()
        
        # Parse: "more wisdom" or "boost interaction" or "focus on X"
        new_weights = current_domain_weights.copy()
        
        for dimension, boost_map in boosts.items():
            if dimension in instruction_lower:
                for domain, boost_amount in boost_map.items():
                    new_weights[domain] = min(1.0, new_weights.get(domain, 0) + boost_amount)
        
        # Renormalize
        total = sum(new_weights.values())
        if total > 0:
            new_weights = {k: v / total for k, v in new_weights.items()}
        
        return {
            "original_weights": current_domain_weights,
            "adjusted_weights": new_weights,
            "instruction": instruction,
            "predicted_boost": "coherence should increase if instruction matches learned patterns"
        }
    
    def get_learning_status(self):
        """
        What has Claude learned?
        """
        best_prims = self.get_best_primitives()
        best_domains = self.get_best_domains()
        
        trajectory = self.coherence_trajectory[-10:] if self.coherence_trajectory else []
        avg_recent = sum(t["coherence"] for t in trajectory) / max(1, len(trajectory))
        
        return {
            "interactions_learned_from": len(self.coherence_trajectory),
            "best_performing_primitives": [
                {"name": p[0], "avg_coherence": round(p[1]["avg"], 3), "samples": p[1]["count"]}
                for p in best_prims
            ],
            "domain_performance": {
                domain: round(stats["avg"], 3) 
                for domain, stats in best_domains.items()
            },
            "recent_coherence_trend": trajectory,
            "average_recent_coherence": round(avg_recent, 3),
            "guidance_available": {
                "boost_wisdom": "Focus on topological reasoning",
                "boost_agency": "Emphasize choice and causality",
                "boost_coherence": "Integrate multiple domains",
                "more_primitives": "Activate more assumptions",
                "focus_on_X": f"Available dimensions: wisdom, agency, integrity, presence, care, reflection"
            }
        }
    
    def export_for_learning_panel(self):
        """Show user what Claude has learned"""
        return {
            "status": self.get_learning_status(),
            "suggestions": self.suggest_domain_boost({}),
            "trajectory": self.coherence_trajectory[-20:]
        }
