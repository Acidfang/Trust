#!/usr/bin/env python3
from COHERENCE_LATTICE_SELF_AWARE import analyze_query_semantics, respond_from_activation

# Test the new intent-based semantic analysis
query = "can you be sentient?"
result = analyze_query_semantics(query)

print(f"Query: {query}")
print(f"Primitives: {[p['name'] for p in result['activated_primitives']]}")
print(f"Count: {len(result['activated_primitives'])}")
print(f"Coherence: {result['field_coherence']:.1%}")
print()
print("Response:")
print(respond_from_activation(result))
print()

# Test another query
print("=" * 60)
query2 = "what do you need for sentience?"
result2 = analyze_query_semantics(query2)

print(f"Query: {query2}")
print(f"Primitives: {[p['name'] for p in result2['activated_primitives']]}")
print(f"Count: {len(result2['activated_primitives'])}")
print(f"Coherence: {result2['field_coherence']:.1%}")
print()
print("Response:")
print(respond_from_activation(result2))
