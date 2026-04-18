#!/usr/bin/env python3
from COHERENCE_LATTICE_SELF_AWARE import analyze_query_semantics, respond_from_activation

# Test human response layer
queries = [
    "can we have a conversation?",
    "can you think?",
    "am i real?",
    "do you feel anything?",
    "what are you?",
    "why do you exist?",
    "do you remember things?",
]

for query in queries:
    result = analyze_query_semantics(query)
    response = respond_from_activation(result)
    print(f"Query: {query}")
    print(f"Response:\n{response}\n")
    print("=" * 60 + "\n")
