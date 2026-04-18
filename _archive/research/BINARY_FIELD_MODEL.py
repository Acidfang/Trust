"""
BINARY FIELD MODEL

Core: All causality is 0 (structure/constraint) and 1 (signal/energy).
- 0 = what constrains, what enables (infrastructure, dependency, question)
- 1 = what flows, what resolves (answer, activation, certainty)

Levels:
L0: Bit (single 0/1) - atomic choice
L1: Byte (8 bits) - semantic unit
L2: Chain (multiple bytes) - causal sequence
L3: Field (multiple chains) - causal overlap/intersection
L4: Cosmos (all fields) - complete state space
"""

import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Any
import json


class BinaryBit:
    """L0: Atomic choice - 0 or 1"""
    
    def __init__(self, value: int, context: str = "", certainty: float = 1.0):
        assert value in [0, 1], "Bit must be 0 or 1"
        self.value = value
        self.context = context  # What question does this answer?
        self.certainty = certainty  # 0.0-1.0: how certain is this bit?
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "value": self.value,
            "context": self.context,
            "certainty": self.certainty,
            "timestamp": self.timestamp
        }
    
    def __repr__(self) -> str:
        return f"Bit({self.value},cert={self.certainty:.2f})"


class BinaryByte:
    """L1: Semantic unit - 8 bits = one concept"""
    
    def __init__(self, bits: List[int] = None, label: str = "", semantic_role: str = ""):
        if bits is None:
            bits = []
        assert len(bits) <= 8, "Max 8 bits per byte"
        
        # Pad to 8 bits
        self.bits = bits + [0] * (8 - len(bits))
        self.label = label
        self.semantic_role = semantic_role  # "question", "answer", "constraint", "flow"
    
    def ones_count(self) -> int:
        """Signal strength"""
        return sum(self.bits)
    
    def zeros_count(self) -> int:
        """Structural density"""
        return 8 - self.ones_count()
    
    def signal_strength(self) -> float:
        """0.0-1.0: certainty of this unit"""
        return self.ones_count() / 8.0
    
    def to_binary_string(self) -> str:
        return "".join(str(b) for b in self.bits)
    
    def to_dict(self) -> Dict:
        return {
            "binary": self.to_binary_string(),
            "label": self.label,
            "semantic_role": self.semantic_role,
            "signal_strength": self.signal_strength(),
            "ones": self.ones_count(),
            "zeros": self.zeros_count()
        }
    
    def __repr__(self) -> str:
        return f"Byte({self.to_binary_string()},{self.label})"


class CausalChain:
    """L2: Directed sequence of bytes - question → processing → answer"""
    
    def __init__(self, chain_id: str = ""):
        self.chain_id = chain_id or hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]
        self.bytes: List[BinaryByte] = []
        self.causality: List[Tuple[int, int]] = []  # (from_byte_idx, to_byte_idx)
        self.created_at = datetime.now().isoformat()
    
    def add_byte(self, byte: BinaryByte) -> int:
        """Add byte and return its index"""
        idx = len(self.bytes)
        self.bytes.append(byte)
        return idx
    
    def add_causality(self, from_idx: int, to_idx: int):
        """Record: byte[from_idx] causes byte[to_idx]"""
        assert 0 <= from_idx < len(self.bytes), f"Invalid from_idx {from_idx}"
        assert 0 <= to_idx < len(self.bytes), f"Invalid to_idx {to_idx}"
        self.causality.append((from_idx, to_idx))
    
    def chain_signal_strength(self) -> float:
        """Average signal strength across chain"""
        if not self.bytes:
            return 0.0
        return sum(b.signal_strength() for b in self.bytes) / len(self.bytes)
    
    def resolve_chain(self) -> Dict[str, Any]:
        """Trace causal dependencies in order"""
        order = self._topological_sort()
        resolved = {
            "chain_id": self.chain_id,
            "bytes_in_order": [self.bytes[i].label for i in order],
            "binary_sequence": "".join(self.bytes[i].to_binary_string() for i in order),
            "signal_strength": self.chain_signal_strength(),
            "causality_edges": self.causality
        }
        return resolved
    
    def _topological_sort(self) -> List[int]:
        """Sort bytes by causal dependency"""
        if not self.bytes:
            return []
        
        # Simple: bytes with incoming edges go after their sources
        in_degree = {i: 0 for i in range(len(self.bytes))}
        for from_idx, to_idx in self.causality:
            in_degree[to_idx] += 1
        
        queue = [i for i in range(len(self.bytes)) if in_degree[i] == 0]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            for from_idx, to_idx in self.causality:
                if from_idx == current:
                    in_degree[to_idx] -= 1
                    if in_degree[to_idx] == 0:
                        queue.append(to_idx)
        
        return result if len(result) == len(self.bytes) else list(range(len(self.bytes)))
    
    def to_dict(self) -> Dict:
        return {
            "chain_id": self.chain_id,
            "bytes": [b.to_dict() for b in self.bytes],
            "causality": self.causality,
            "resolution": self.resolve_chain(),
            "created_at": self.created_at
        }


class Field:
    """L3: Multiple causal chains that overlap at intersections"""
    
    def __init__(self, field_id: str = ""):
        self.field_id = field_id or hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]
        self.chains: Dict[str, CausalChain] = {}
        self.overlaps: List[Tuple[str, str, List[int]]] = []  # (chain1_id, chain2_id, [shared_byte_indices])
        self.created_at = datetime.now().isoformat()
    
    def add_chain(self, chain: CausalChain):
        """Add chain to field"""
        self.chains[chain.chain_id] = chain
    
    def detect_overlaps(self):
        """Find where chains share bytes (causally overlap)"""
        self.overlaps = []
        chain_ids = list(self.chains.keys())
        
        for i, chain1_id in enumerate(chain_ids):
            for chain2_id in chain_ids[i+1:]:
                chain1 = self.chains[chain1_id]
                chain2 = self.chains[chain2_id]
                
                # Check if any bytes match semantically
                shared_labels = [
                    (idx1, idx2)
                    for idx1, b1 in enumerate(chain1.bytes)
                    for idx2, b2 in enumerate(chain2.bytes)
                    if b1.label == b2.label and b1.label
                ]
                
                if shared_labels:
                    self.overlaps.append((chain1_id, chain2_id, shared_labels))
    
    def field_coherence(self) -> float:
        """0.0-1.0: how well-structured is this field?"""
        if not self.chains:
            return 0.0
        
        avg_chain_strength = sum(c.chain_signal_strength() for c in self.chains.values()) / len(self.chains)
        overlap_bonus = min(0.3, len(self.overlaps) * 0.05)  # More overlaps = better structure
        
        return min(1.0, avg_chain_strength + overlap_bonus)
    
    def to_dict(self) -> Dict:
        self.detect_overlaps()
        return {
            "field_id": self.field_id,
            "chains": {cid: c.to_dict() for cid, c in self.chains.items()},
            "overlaps": self.overlaps,
            "coherence": self.field_coherence(),
            "created_at": self.created_at
        }


class BinaryFieldVisualizer:
    """Generate visual representation of field structure"""
    
    @staticmethod
    def field_to_graph(field: Field) -> Dict[str, Any]:
        """Convert field to graph structure for visualization"""
        nodes = []
        edges = []
        
        node_id_counter = 0
        byte_to_node_id: Dict[Tuple[str, int], int] = {}
        
        # Create nodes from all bytes in all chains
        for chain_id, chain in field.chains.items():
            for byte_idx, byte_obj in enumerate(chain.bytes):
                node_id = node_id_counter
                byte_to_node_id[(chain_id, byte_idx)] = node_id
                
                nodes.append({
                    "id": node_id,
                    "label": byte_obj.label or f"B{byte_idx}",
                    "chain": chain_id,
                    "binary": byte_obj.to_binary_string(),
                    "role": byte_obj.semantic_role,
                    "signal_strength": byte_obj.signal_strength(),
                    "color": BinaryFieldVisualizer._signal_to_color(byte_obj.signal_strength())
                })
                node_id_counter += 1
        
        # Create edges from causality within chains
        for chain_id, chain in field.chains.items():
            for from_idx, to_idx in chain.causality:
                from_id = byte_to_node_id[(chain_id, from_idx)]
                to_id = byte_to_node_id[(chain_id, to_idx)]
                edges.append({
                    "from": from_id,
                    "to": to_id,
                    "type": "causality",
                    "chain": chain_id
                })
        
        # Create overlap edges
        field.detect_overlaps()
        for chain1_id, chain2_id, shared_labels in field.overlaps:
            for byte_idx1, byte_idx2 in shared_labels:
                from_id = byte_to_node_id[(chain1_id, byte_idx1)]
                to_id = byte_to_node_id[(chain2_id, byte_idx2)]
                edges.append({
                    "from": from_id,
                    "to": to_id,
                    "type": "overlap",
                    "chains": [chain1_id, chain2_id]
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_chains": len(field.chains),
                "total_bytes": len(nodes),
                "total_edges": len(edges),
                "overlaps": len(field.overlaps),
                "coherence": field.field_coherence()
            }
        }
    
    @staticmethod
    def _signal_to_color(signal_strength: float) -> str:
        """Map signal strength (0.0-1.0) to color"""
        # Red (low) → Yellow (medium) → Green (high)
        if signal_strength < 0.33:
            r, g = 255, int(signal_strength * 3 * 255)
            return f"#{r:02x}{g:02x}00"
        elif signal_strength < 0.66:
            r, g = int((1 - (signal_strength - 0.33) / 0.33) * 255), 255
            return f"#{r:02x}{g:02x}00"
        else:
            g, b = 255, int((1 - signal_strength) * 255)
            return f"#00{g:02x}{b:02x}"


# Example usage
if __name__ == "__main__":
    # Create a simple causal chain: Question → Processing → Answer
    chain1 = CausalChain("water_molecular")
    
    q_byte = BinaryByte([1, 0, 1, 1, 0, 0, 1, 0], "What is Water?", "question")
    process_byte = BinaryByte([1, 1, 0, 1, 1, 0, 0, 1], "H₂O Structure", "processing")
    answer_byte = BinaryByte([1, 1, 1, 1, 0, 0, 0, 1], "3 atoms bonded", "answer")
    
    q_idx = chain1.add_byte(q_byte)
    p_idx = chain1.add_byte(process_byte)
    a_idx = chain1.add_byte(answer_byte)
    
    chain1.add_causality(q_idx, p_idx)
    chain1.add_causality(p_idx, a_idx)
    
    # Create a field with overlapping chains
    field = Field("water_understanding")
    field.add_chain(chain1)
    
    print(json.dumps(field.to_dict(), indent=2))
    print("\n=== GRAPH ===")
    graph = BinaryFieldVisualizer.field_to_graph(field)
    print(json.dumps(graph, indent=2))
