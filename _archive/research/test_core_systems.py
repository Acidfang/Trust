#!/usr/bin/env python3
"""
Quick test of core systems integration
"""
import sys
sys.path.insert(0, 'c:\\Determined')

from COHERENCE_LATTICE_SELF_AWARE import analyze_query_semantics
from CORE_SYSTEMS_INTEGRATION import CoreSystemsIntegration

# Test query
query = "What is consciousness?"

# Test L1 activation
print("[TEST] L1: Primitive Activation")
try:
    analysis = analyze_query_semantics(query)
    activated_primitives = analysis["activated_primitives"]
    print(f"✓ Activated {len(activated_primitives)} primitives")
    print(f"  Sample primitive: {activated_primitives[0] if activated_primitives else 'NONE'}")
except Exception as e:
    print(f"✗ ERROR in L1: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test L7+L5+L4
print("\n[TEST] L7+L5+L4: Core Systems Integration")
try:
    core_systems = CoreSystemsIntegration()
    core_systems.set_conversation_context("test_conv_001")
    
    response_text = "Consciousness is a property of the unified field becoming self-aware..."
    guardian_metadata = {"action": "PASS", "confidence": 0.85}
    
    coherence_score, quality_metadata, detected_patterns = core_systems.process_response(
        response_text=response_text,
        activated_primitives=activated_primitives,
        guardian_metadata=guardian_metadata,
        field_coherence=0.8
    )
    
    print(f"✓ Core systems processed successfully")
    print(f"  Coherence Score: {coherence_score}")
    print(f"  Quality Metadata: {quality_metadata}")
    print(f"  Detected Patterns: {detected_patterns}")
except Exception as e:
    print(f"✗ ERROR in core systems: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ ALL TESTS PASSED")
