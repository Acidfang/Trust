"""
Export binary field properties catalog to CSV and JSON
"""

from BINARY_FIELD_PROPERTIES import FieldPropertyAnalyzer

analyzer = FieldPropertyAnalyzer()

# Export as CSV
csv_data = analyzer.export_catalog_csv()
with open("c:\\Determined\\BINARY_FIELD_PROPERTIES.csv", "w") as f:
    f.write(csv_data)

print("✓ Exported CSV: BINARY_FIELD_PROPERTIES.csv")
print(f"  Lines: {len(csv_data.split(chr(10)))}")

# Export as JSON
json_data = analyzer.export_catalog_json()
with open("c:\\Determined\\BINARY_FIELD_PROPERTIES.json", "w") as f:
    f.write(json_data)

print("✓ Exported JSON: BINARY_FIELD_PROPERTIES.json")
print(f"  Patterns: 256")

# Export causal graph
graph = analyzer.get_causal_graph()
import json
with open("c:\\Determined\\BINARY_CAUSAL_GRAPH.json", "w") as f:
    json.dump(graph, f, indent=2)

print("✓ Exported Causal Graph: BINARY_CAUSAL_GRAPH.json")
print(f"  Nodes: 256")
print(f"  Edges per node: 8 (hamming distance 1)")

# Export hierarchy
hierarchy = analyzer.get_pattern_hierarchy()
hierarchy_data = {
    k: v for k, v in hierarchy.items()
}
with open("c:\\Determined\\BINARY_HIERARCHY.json", "w") as f:
    json.dump(hierarchy_data, f, indent=2)

print("✓ Exported Hierarchy: BINARY_HIERARCHY.json")
print(f"  Levels: {len(hierarchy_data)}")

# Print summary statistics
print("\n" + "="*60)
print("BINARY FIELD STATISTICS")
print("="*60)

roles = ["void", "question", "constraint", "processing", "flow", "answer", "saturated"]
for role in roles:
    patterns = analyzer.get_patterns_by_role(role)
    if patterns:
        print(f"{role.upper():15} {len(patterns):3} patterns")

print(f"\nTotal patterns:  256 bytes (0-255)")
print(f"Signal range:    0.0 (void) → 1.0 (answer)")
print(f"Neighbors:       Each pattern has 8 neighbors (hamming distance 1)")
print(f"Graph edges:     256 nodes × 8 neighbors = 2048 directed edges")
