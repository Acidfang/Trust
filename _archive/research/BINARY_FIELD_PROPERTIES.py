"""
BINARY FIELD PROPERTIES CATALOG

All 256 possible byte patterns and their field characteristics.
This is the complete property space for binary navigation.
"""

import json
from typing import Dict, List, Any


class BinaryFieldProperties:
    """Enumerate and characterize all 256 byte patterns"""
    
    def __init__(self):
        self.patterns = {}
        self.generate_all_patterns()
    
    def generate_all_patterns(self):
        """Generate properties for all 256 byte patterns"""
        for i in range(256):
            binary = format(i, '08b')
            self.patterns[binary] = self.calculate_properties(binary, i)
    
    def calculate_properties(self, binary: str, decimal: int) -> Dict[str, Any]:
        """Calculate all properties for a single byte pattern"""
        bits = [int(b) for b in binary]
        ones = sum(bits)
        zeros = 8 - ones
        
        return {
            "binary": binary,
            "decimal": decimal,
            "hex": format(decimal, '02x'),
            
            # SIGNAL PROPERTIES
            "ones_count": ones,
            "zeros_count": zeros,
            "signal_strength": ones / 8.0,  # 0.0-1.0
            "structure_density": zeros / 8.0,  # 0.0-1.0
            
            # PATTERN CHARACTERISTICS
            "pattern_type": self._classify_pattern(bits),
            "symmetry": self._detect_symmetry(bits),
            "clustering": self._detect_clustering(bits),
            "alternation": self._detect_alternation(bits),
            "regions": self._find_regions(bits),
            
            # SEMANTIC ROLE
            "semantic_role": self._assign_role(ones),
            "confidence": self._calculate_confidence(bits),
            "flow_potential": self._calculate_flow_potential(ones),
            
            # COLOR & VISUAL
            "color_hex": self._signal_to_color(ones / 8.0),
            "emissive_intensity": (ones / 8.0),
            
            # NAVIGATION PROPERTIES
            "traversal_cost": self._traversal_cost(ones, zeros),
            "causality_direction": self._causality_direction(ones),
            "energy_state": self._energy_state(bits),
            
            # FIELD RELATIONSHIPS
            "hamming_distance_to_all_zeros": self._hamming_distance(bits, [0]*8),
            "hamming_distance_to_all_ones": self._hamming_distance(bits, [1]*8),
            "nearest_neighbors": self._find_neighbors(bits),
        }
    
    def _classify_pattern(self, bits: List[int]) -> str:
        """Classify pattern type"""
        ones = sum(bits)
        
        if ones == 0:
            return "void"  # No signal
        elif ones == 8:
            return "saturated"  # Complete signal
        elif bits == bits[::-1]:
            return "palindrome"  # Symmetric
        elif all(bits[i] == bits[i-1] for i in range(1, len(bits))):
            return "uniform"  # All same
        elif ones <= 2:
            return "sparse"  # Very few 1s
        elif ones >= 6:
            return "dense"  # Very many 1s
        elif ones == 4:
            return "balanced"  # Half and half
        else:
            return "mixed"
    
    def _detect_symmetry(self, bits: List[int]) -> bool:
        """Detect mirror symmetry"""
        return bits == bits[::-1]
    
    def _detect_clustering(self, bits: List[int]) -> int:
        """Count contiguous clusters of 1s"""
        clusters = 0
        in_cluster = False
        for bit in bits:
            if bit == 1:
                if not in_cluster:
                    clusters += 1
                    in_cluster = True
            else:
                in_cluster = False
        return clusters
    
    def _detect_alternation(self, bits: List[int]) -> float:
        """Measure alternation (bit flips / max possible)"""
        flips = sum(1 for i in range(len(bits)-1) if bits[i] != bits[i+1])
        return flips / 7.0  # Max 7 flips in 8 bits
    
    def _find_regions(self, bits: List[int]) -> List[Dict]:
        """Find contiguous regions of 0s and 1s"""
        regions = []
        if not bits:
            return regions
        
        current_bit = bits[0]
        start = 0
        
        for i in range(1, len(bits)):
            if bits[i] != current_bit:
                regions.append({
                    "type": "ones" if current_bit == 1 else "zeros",
                    "start": start,
                    "length": i - start
                })
                current_bit = bits[i]
                start = i
        
        regions.append({
            "type": "ones" if current_bit == 1 else "zeros",
            "start": start,
            "length": len(bits) - start
        })
        
        return regions
    
    def _assign_role(self, ones: int) -> str:
        """Assign semantic role based on signal strength"""
        ratio = ones / 8.0
        
        if ratio == 0.0:
            return "void"
        elif ratio <= 0.125:
            return "question"  # Rare event, anomaly
        elif ratio <= 0.375:
            return "constraint"  # Mostly structured
        elif ratio <= 0.625:
            return "processing"  # Balanced
        elif ratio <= 0.875:
            return "flow"  # Mostly signal
        else:
            return "answer"  # Complete clarity
    
    def _calculate_confidence(self, bits: List[int]) -> float:
        """Confidence = how certain/defined is this state"""
        ones = sum(bits)
        # Extremes (all 0s or all 1s) have high confidence
        # Midpoints have lower confidence
        mid = 4
        distance_from_mid = abs(ones - mid)
        return distance_from_mid / 4.0  # 0.0 at center, 1.0 at extremes
    
    def _calculate_flow_potential(self, ones: int) -> float:
        """Flow potential = readiness to transition"""
        # More 0s = potential to fill (become 1s)
        # More 1s = potential to contract (become 0s)
        return 1.0 - abs(ones - 4) / 4.0
    
    def _signal_to_color(self, signal: float) -> str:
        """Map signal strength to color"""
        if signal < 0.33:
            r, g = 255, int(signal * 3 * 255)
            return f"#{r:02x}{g:02x}00"
        elif signal < 0.66:
            r, g = int((1 - (signal - 0.33) / 0.33) * 255), 255
            return f"#{r:02x}{g:02x}00"
        else:
            g, b = 255, int((1 - signal) * 255)
            return f"#00{g:02x}{b:02x}"
    
    def _traversal_cost(self, ones: int, zeros: int) -> float:
        """Cost to traverse this pattern in field navigation"""
        # Extreme patterns (all 0s or all 1s) have lower traversal cost
        # Balanced patterns are harder to traverse
        balance = min(ones, zeros)
        return (balance / 4.0)  # 0.0 for extremes, 1.0 for perfect balance
    
    def _causality_direction(self, ones: int) -> str:
        """Which direction does causality flow through this byte?"""
        if ones < 4:
            return "convergent"  # Flows toward 0s, structure
        elif ones > 4:
            return "divergent"  # Flows toward 1s, signal
        else:
            return "balanced"  # No preferred direction
    
    def _energy_state(self, bits: List[int]) -> Dict[str, float]:
        """Calculate field energy state"""
        ones = sum(bits)
        
        return {
            "kinetic": ones / 8.0,  # Energy in motion (1s)
            "potential": (8 - ones) / 8.0,  # Energy stored (0s)
            "total": 1.0,
            "gradient": abs(ones - 4) / 4.0  # Energy differential
        }
    
    def _hamming_distance(self, bits1: List[int], bits2: List[int]) -> int:
        """Count bit differences"""
        return sum(1 for b1, b2 in zip(bits1, bits2) if b1 != b2)
    
    def _find_neighbors(self, bits: List[int]) -> List[str]:
        """Find patterns that differ by 1 bit (hamming distance = 1)"""
        neighbors = []
        for flip_pos in range(8):
            neighbor_bits = bits.copy()
            neighbor_bits[flip_pos] = 1 - neighbor_bits[flip_pos]
            neighbor_str = "".join(str(b) for b in neighbor_bits)
            neighbors.append(neighbor_str)
        return neighbors


class FieldPropertyAnalyzer:
    """Analyze and query field properties"""
    
    def __init__(self):
        self.catalog = BinaryFieldProperties()
    
    def get_patterns_by_role(self, role: str) -> List[str]:
        """Get all patterns with a specific semantic role"""
        return [
            p for p, props in self.catalog.patterns.items()
            if props["semantic_role"] == role
        ]
    
    def get_patterns_by_signal_range(self, min_sig: float, max_sig: float) -> List[str]:
        """Get patterns within signal strength range"""
        return [
            p for p, props in self.catalog.patterns.items()
            if min_sig <= props["signal_strength"] <= max_sig
        ]
    
    def get_pattern_hierarchy(self) -> Dict[str, List[str]]:
        """Organize all patterns by signal strength levels"""
        hierarchy = {}
        
        for percentage in range(0, 101, 12):  # 0%, 12%, 25%, 37%, 50%, etc.
            min_sig = (percentage - 6) / 100.0
            max_sig = (percentage + 6) / 100.0
            patterns = self.get_patterns_by_signal_range(max(0, min_sig), min(1, max_sig))
            if patterns:
                label = f"{percentage}% signal"
                hierarchy[label] = patterns
        
        return hierarchy
    
    def get_causal_graph(self) -> Dict[str, Any]:
        """Build graph of causal transitions (hamming distance 1)"""
        graph = {}
        
        for binary, props in self.catalog.patterns.items():
            graph[binary] = {
                "neighbors": props["nearest_neighbors"],
                "direction": props["causality_direction"],
                "flow_potential": props["flow_potential"]
            }
        
        return graph
    
    def export_catalog_json(self) -> str:
        """Export full catalog as JSON"""
        return json.dumps(self.catalog.patterns, indent=2)
    
    def export_catalog_csv(self) -> str:
        """Export full catalog as CSV"""
        lines = [
            "binary,decimal,hex,signal,structure,role,pattern_type,symmetry,color,causality_direction"
        ]
        
        for binary, props in sorted(self.catalog.patterns.items(), key=lambda x: x[1]["decimal"]):
            lines.append(
                f"{binary},{props['decimal']},{props['hex']},"
                f"{props['signal_strength']:.3f},{props['structure_density']:.3f},"
                f"{props['semantic_role']},{props['pattern_type']},"
                f"{props['symmetry']},{props['color_hex']},{props['causality_direction']}"
            )
        
        return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 70)
    print("BINARY FIELD PROPERTIES CATALOG")
    print("=" * 70)
    
    analyzer = FieldPropertyAnalyzer()
    
    # Show organized by role
    print("\n[PATTERNS BY SEMANTIC ROLE]")
    roles = ["void", "question", "constraint", "processing", "flow", "answer", "saturated"]
    for role in roles:
        patterns = analyzer.get_patterns_by_role(role)
        if patterns:
            print(f"\n{role.upper()} ({len(patterns)} patterns):")
            for p in patterns[:5]:  # Show first 5
                props = analyzer.catalog.patterns[p]
                print(f"  {p} (signal={props['signal_strength']:.2f}, color={props['color_hex']})")
            if len(patterns) > 5:
                print(f"  ... and {len(patterns) - 5} more")
    
    # Show hierarchy
    print("\n[SIGNAL STRENGTH HIERARCHY]")
    hierarchy = analyzer.get_pattern_hierarchy()
    for level, patterns in sorted(hierarchy.items(), key=lambda x: len(x[1])):
        print(f"\n{level}: {len(patterns)} patterns")
        for p in patterns[:3]:
            print(f"  {p}")
        if len(patterns) > 3:
            print(f"  ... and {len(patterns) - 3} more")
    
    # Sample detailed properties
    print("\n[SAMPLE PATTERN ANALYSIS]")
    sample_patterns = ["00000000", "11111111", "00000001", "10101010", "11001100", "01010101"]
    for binary in sample_patterns:
        if binary in analyzer.catalog.patterns:
            props = analyzer.catalog.patterns[binary]
            print(f"\n{binary}:")
            print(f"  Role: {props['semantic_role']}")
            print(f"  Signal: {props['signal_strength']:.2%}")
            print(f"  Pattern: {props['pattern_type']}")
            print(f"  Causality: {props['causality_direction']}")
            print(f"  Color: {props['color_hex']}")
            print(f"  Confidence: {props['confidence']:.2f}")
            print(f"  Clustering: {props['clustering']} regions")
            print(f"  Neighbors: {props['nearest_neighbors'][:3]}...")
    
    # Export options
    print("\n[EXPORT OPTIONS]")
    print("Full JSON available via: analyzer.export_catalog_json()")
    print("Full CSV available via: analyzer.export_catalog_csv()")
