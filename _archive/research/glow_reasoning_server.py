#!/usr/bin/env python3
"""
Test the server endpoint by creating a minimal Flask app
"""
import sys
sys.path.insert(0, 'c:\\Determined')

# Mimic the server code exactly
from flask import Flask, request, jsonify
from COHERENCE_LATTICE_SELF_AWARE import analyze_query_semantics
from CLAUDE_SESSION_LEDGER import ClaudeSessionLedger
from COMMUNICATION_FIELD_COMPLETE import (
    generate_response_via_communication_field,
    load_session_history
)
from continuity_guardian import ContinuityGuardian
from CORE_SYSTEMS_INTEGRATION import CoreSystemsIntegration

app = Flask(__name__)
ledger = ClaudeSessionLedger("claude_session_reasoning.jsonl")
guardian = ContinuityGuardian("claude_session_reasoning.jsonl")
core_systems = CoreSystemsIntegration()
counter = 0

@app.route('/query', methods=['POST'])
def handle_query():
    global counter
    
    data = request.json
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        counter += 1
        reasoning_id = ledger.start_reasoning(query, counter)
        
        # Set conversation context for telemetry
        core_systems.set_conversation_context(reasoning_id)
        
        analysis = analyze_query_semantics(query)
        activated_primitives = analysis["activated_primitives"]
        
        # LOAD FULL SESSION HISTORY for communication field response
        session_id = ledger.current_session_id
        history = load_session_history("claude_session_reasoning.jsonl", session_id)
        
        # Generate response via COMMUNICATION FIELD (no templates, pure field expression)
        response_text = generate_response_via_communication_field(
            query, 
            activated_primitives,
            history,
            analysis["field_coherence"]
        )
        
        # ─────────────────────────────────────────────────────────
        # CONTINUITY GUARDIAN: Block or rewrite bad interactions
        # ─────────────────────────────────────────────────────────
        
        candidate_response = {
            "response": response_text,
            "primitives": [p["name"] for p in activated_primitives[:5]],
            "confidence": analysis["field_coherence"]
        }
        
        # Convert history to guardian format
        guardian_history = [
            {"query": h.get("query"), "response": h.get("response")}
            for h in history
        ]
        
        # Apply guardian
        guardian_action, guarded_response, guardian_reason = guardian.guard_response(
            candidate_response,
            query,
            ledger.current_session_id,
            guardian_history
        )
        
        # Extract the guarded response
        response_text = guarded_response.get("response", response_text)
        confidence = guarded_response.get("confidence", analysis["field_coherence"])
        
        # ─────────────────────────────────────────────────────────
        # L7 + L5 + L4: PROCESS THROUGH CORE SYSTEMS
        # ─────────────────────────────────────────────────────────
        
        guardian_metadata = {
            "action": guardian_action,
            "confidence": confidence
        }
        
        coherence_score, quality_metadata, detected_patterns = core_systems.process_response(
            response_text=response_text,
            activated_primitives=activated_primitives,
            guardian_metadata=guardian_metadata,
            field_coherence=analysis["field_coherence"]
        )
        
        return jsonify({
            "query": query,
            "response": response_text,
            "coherence_score": coherence_score,
            "guardian_action": guardian_action,
            "detected_patterns": detected_patterns,
            "quality_metrics": {
                "reversible": quality_metadata["reversibility"],
                "transparent": quality_metadata["transparency"],
                "causally_grounded": quality_metadata["causal_grounding"],
                "domain_isolated": quality_metadata["domain_isolation"],
                "monotonic": quality_metadata["application_monotonicity"]
            }
        })
    
    except Exception as e:
        import traceback
        print(f"[ERROR] Exception occurred:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=False)
