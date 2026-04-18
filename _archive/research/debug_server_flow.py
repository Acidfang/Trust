#!/usr/bin/env python3
"""
Debug the server endpoint directly
"""
import sys
import json
sys.path.insert(0, 'c:\\Determined')

from COHERENCE_LATTICE_SELF_AWARE import analyze_query_semantics
from COMMUNICATION_FIELD_COMPLETE import generate_response_via_communication_field
from continuity_guardian import ContinuityGuardian
from CORE_SYSTEMS_INTEGRATION import CoreSystemsIntegration
from CLAUDE_SESSION_LEDGER import ClaudeSessionLedger

# Initialize components
print("[INIT] Initializing components...")
ledger = ClaudeSessionLedger("claude_session_reasoning.jsonl")
guardian = ContinuityGuardian()
core_systems = CoreSystemsIntegration()

query = "What is consciousness?"
print(f"\n[QUERY] Testing with: {query}")

try:
    # Step 1: L1 activation
    print("\n[STEP 1] L1: Primitive Activation")
    analysis = analyze_query_semantics(query)
    activated_primitives = analysis["activated_primitives"]
    print(f"  ✓ Got {len(activated_primitives)} primitives")
    
    # Step 2: Generate response
    print("\n[STEP 2] Communication Field Response")
    session_id = ledger.current_session_id
    
    # Load history
    try:
        from ledger import load_session_history
        history = load_session_history("claude_session_reasoning.jsonl", session_id)
    except:
        history = []
    
    print(f"  ✓ Got {len(history)} history entries")
    
    response_text = generate_response_via_communication_field(
        query, 
        activated_primitives,
        history,
        analysis["field_coherence"]
    )
    print(f"  ✓ Response: {response_text[:100]}...")
    
    # Step 3: Guardian
    print("\n[STEP 3] Continuity Guardian")
    candidate_response = {
        "response": response_text,
        "primitives": [p["name"] for p in activated_primitives[:5]],
        "confidence": analysis["field_coherence"]
    }
    
    guardian_history = [
        {"query": h.get("query"), "response": h.get("response")}
        for h in history
    ]
    
    print(f"  guardian_history type: {type(guardian_history)}")
    print(f"  guardian_history: {guardian_history[:2] if guardian_history else 'EMPTY'}")
    
    guardian_action, guarded_response, guardian_reason = guardian.guard_response(
        candidate_response,
        query,
        ledger.current_session_id,
        guardian_history
    )
    print(f"  ✓ Guardian action: {guardian_action}")
    print(f"  ✓ Guardian reason: {guardian_reason}")
    
    response_text = guarded_response.get("response", response_text)
    confidence = guarded_response.get("confidence", analysis["field_coherence"])
    
    # Step 4: Core systems
    print("\n[STEP 4] Core Systems Integration (L7+L5+L4)")
    guardian_metadata = {
        "action": guardian_action,
        "confidence": confidence
    }
    
    print(f"  Response text type: {type(response_text)}, len={len(response_text) if response_text else 'NONE'}")
    print(f"  Activated primitives: {len(activated_primitives)}")
    print(f"  Guardian metadata: {guardian_metadata}")
    
    coherence_score, quality_metadata, detected_patterns = core_systems.process_response(
        response_text=response_text,
        activated_primitives=activated_primitives,
        guardian_metadata=guardian_metadata,
        field_coherence=analysis["field_coherence"]
    )
    print(f"  ✓ Coherence score: {coherence_score}")
    print(f"  ✓ Patterns: {detected_patterns}")
    
    print("\n✓ ALL STEPS PASSED")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
