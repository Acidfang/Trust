#!/usr/bin/env python3
"""
GLOW REASONING SERVER - Integrated L1/L7/L5/L4 Pipeline
═══════════════════════════════════════════════════════════════════════════════

Full integration of all core systems:
  L1: Primitive field activation (COHERENCE_LATTICE)
  L7: Meta-coherence pattern detection (EMERGENT PATTERNS)
  L5: Coherence validation (UNIVERSAL PRINCIPLES)
  L4: Emergence telemetry logging (PATTERN TRACKING)
"""

from flask import Flask, request, jsonify, send_file
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from COHERENCE_LATTICE_SELF_AWARE import analyze_query_semantics
from CLAUDE_SESSION_LEDGER import ClaudeSessionLedger
from COMMUNICATION_FIELD_COMPLETE import (
    generate_response_via_communication_field,
    load_session_history
)
from continuity_guardian import ContinuityGuardian
from CORE_SYSTEMS_INTEGRATION import CoreSystemsIntegration
import json

app = Flask(__name__)
ledger = ClaudeSessionLedger("claude_session_reasoning.jsonl")
guardian = ContinuityGuardian("claude_session_reasoning.jsonl")
core_systems = CoreSystemsIntegration()
counter = 0


@app.route('/', methods=['GET'])
def root():
    try:
        return send_file('glow_interface.html')
    except:
        return jsonify({"error": "Interface not available"}), 404


@app.route('/cors', methods=['OPTIONS'])
def cors():
    response = jsonify({"status": "ready"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response


@app.route('/query', methods=['POST', 'OPTIONS'])
def handle_query():
    global counter
    
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.json
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        counter += 1
        reasoning_id = ledger.start_reasoning(query, counter)
        
        # Set conversation context for telemetry
        core_systems.set_conversation_context(reasoning_id)
        
        # ─────────────────────────────────────────────────────────
        # L1: PRIMITIVE ACTIVATION
        # ─────────────────────────────────────────────────────────
        
        analysis = analyze_query_semantics(query)
        activated_primitives = analysis["activated_primitives"]
        
        # LOAD FULL SESSION HISTORY for communication field response
        session_id = ledger.current_session_id
        history = load_session_history("claude_session_reasoning.jsonl", session_id)
        
        # Generate response via COMMUNICATION FIELD
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
        
        # ─────────────────────────────────────────────────────────
        # LOG TO LEDGER
        # ─────────────────────────────────────────────────────────
        
        ledger.end_reasoning(
            reasoning_id,
            conclusion=response_text,
            confidence=coherence_score,
            metadata={
                "guardian_action": guardian_action,
                "coherence_score": coherence_score,
                "principle_checks": quality_metadata["principle_checks"],
                "detected_patterns": detected_patterns,
                "primitives_count": len(activated_primitives)
            }
        )
        
        for prim in activated_primitives[:5]:
            ledger.log_assumption(
                reasoning_id,
                f"Primitive '{prim['name']}' (domain: {prim['domain']})",
                confidence=min(1.0, prim.get("match_weight", 1.0) / 3.0)
            )
        
        # ─────────────────────────────────────────────────────────
        # RETURN RESPONSE WITH FULL METADATA
        # ─────────────────────────────────────────────────────────
        
        return jsonify({
            "query": query,
            "response": response_text,
            "reasoning_id": reasoning_id,
            "primitives": [p["name"] for p in activated_primitives[:5]],
            "domains": analysis["activated_domains"],
            "confidence": confidence,
            "coherence_score": coherence_score,
            "guardian_action": guardian_action,
            "state_6d": analysis["query_6d"],
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
        error_msg = traceback.format_exc()
        print(f"\n[ERROR TRACEBACK]\n{error_msg}")
        with open("error.log", "a") as f:
            f.write(f"\n[{counter}] {error_msg}\n")
        return jsonify({"error": str(e), "traceback": error_msg}), 500


@app.route('/ledger/state', methods=['GET'])
def get_ledger_state():
    return jsonify(ledger.export_for_frontend())


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "active",
        "queries_processed": counter
    })


@app.route('/telemetry/stats', methods=['GET'])
def get_telemetry_stats():
    """Get pattern activation statistics across all conversations"""
    stats = core_systems.get_telemetry_stats()
    return jsonify(stats)


@app.route('/telemetry/conversation/<conversation_id>', methods=['GET'])
def get_conversation_arc(conversation_id):
    """Get pattern emergence arc for specific conversation"""
    core_systems.set_conversation_context(conversation_id)
    arc = core_systems.get_conversation_arc()
    return jsonify(arc) if arc else (jsonify({"error": "Conversation not found"}), 404)


if __name__ == '__main__':
    app.run(debug=False, port=5555, host='localhost')
