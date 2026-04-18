#!/usr/bin/env python3
"""
═════════════════════════════════════════════════════════════════════════════════
GLOW REASONING SERVER - INTEGRATED L1 + L7 + L5 + L4 PIPELINE
═════════════════════════════════════════════════════════════════════════════════

SYSTEM ARCHITECTURE
┌─────────────────────────────────────────────────────────────────────────────┐
│ [L1] PRIMITIVE ACTIVATION                                                   │
│     Parse query → Activate matching field modes across 12 domains           │
│     Input markers → 6D field representation                                  │
│                                                                              │
│ [COMMUNICATION FIELD] RESPONSE GENERATION                                   │
│     Use activated primitives + session history → Natural language response   │
│                                                                              │
│ [CONTINUITY GUARDIAN] RESPONSE PROTECTION                                   │
│     Block/rewrite responses that violate coherence constraints              │
│                                                                              │
│ [L7] META-COHERENCE DETECTION                                              │
│     Detect 4 emergent patterns + authenticity loop                          │
│     COHERENCE_GRAVITY, LEARNING_ACCELERATION, TRUST_EMERGENCE, CREATIVE_FRD │
│                                                                              │
│ [L5] COHERENCE VALIDATION                                                  │
│     Validate response against 5 universal principles (0.0-1.0 score)        │
│     REVERSIBILITY, TRANSPARENCY, CAUSAL_GROUNDING, DOMAIN_ISOLATION,        │
│     APPLICATION_MONOTONICITY                                               │
│                                                                              │
│ [L4] EMERGENCE TELEMETRY                                                   │
│     Log pattern activations per turn for conversation arc                   │
───────────────────────────────────────────────────────────────────────────────
"""

from flask import Flask, request, jsonify
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

app = Flask(__name__)
ledger = ClaudeSessionLedger("claude_session_reasoning.jsonl")
guardian = ContinuityGuardian("claude_session_reasoning.jsonl")
core_systems = CoreSystemsIntegration()
counter = 0


@app.route('/query', methods=['POST'])
def handle_query():
    """
    Main query endpoint
    
    Returns:
    {
      "query": str,
      "response": str (the generated response),
      "coherence_score": float (0.0-1.0),
      "guardian_action": str ("PASS", "REWRITE_APPLIED", "BLOCKED"),
      "detected_patterns": list (which L7 patterns fired),
      "quality_metrics": dict (which L5 principles passed),
      ... (other metadata)
    }
    """
    
    global counter
    
    data = request.json
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        counter += 1
        reasoning_id = ledger.start_reasoning(query, counter)
        
        # ─────────────────────────────────────────────────────────
        # STEP 1: L1 - PRIMITIVE ACTIVATION
        # ─────────────────────────────────────────────────────────
        core_systems.set_conversation_context(reasoning_id)
        analysis = analyze_query_semantics(query)
        activated_primitives = analysis["activated_primitives"]
        
        # ─────────────────────────────────────────────────────────
        # STEP 2: COMMUNICATION FIELD RESPONSE GENERATION
        # ─────────────────────────────────────────────────────────
        session_id = ledger.current_session_id
        history = load_session_history("claude_session_reasoning.jsonl", session_id)
        
        response_text = generate_response_via_communication_field(
            query, 
            activated_primitives,
            history,
            analysis["field_coherence"]
        )
        
        # ─────────────────────────────────────────────────────────
        # STEP 3: CONTINUITY GUARDIAN
        # ─────────────────────────────────────────────────────────
        candidate_response = {
            "response": response_text,
            "primitives": [p["name"] for p in activated_primitives[:5]],
            "confidence": analysis["field_coherence"]
        }
        
        guardian_history = [
            {"query": h.get("query"), "response": h.get("response")}
            for h in history
        ]
        
        guardian_action, guarded_response, guardian_reason = guardian.guard_response(
            candidate_response,
            query,
            ledger.current_session_id,
            guardian_history
        )
        
        response_text = guarded_response.get("response", response_text)
        confidence = guarded_response.get("confidence", analysis["field_coherence"])
        
        # ─────────────────────────────────────────────────────────
        # STEP 4: L7 + L5 + L4 - CORE SYSTEMS INTEGRATION
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
            confidence=coherence_score
        )
        
        for prim in activated_primitives[:5]:
            try:
                ledger.log_assumption(
                    reasoning_id,
                    f"Primitive '{prim.get('name', 'UNKNOWN')}' (domain: {prim.get('domain', 'UNKNOWN')})",
                    confidence=min(1.0, prim.get("match_weight", 1.0) / 3.0)
                )
            except:
                pass  # Ignore logging errors
        
        # ─────────────────────────────────────────────────────────
        # RETURN FULL RESPONSE METADATA
        # ─────────────────────────────────────────────────────────
        return jsonify({
            "query": query,
            "response": response_text,
            "reasoning_id": reasoning_id,
            "primitives": [p["name"] for p in activated_primitives[:5]],
            "domains": analysis.get("activated_domains", []),
            "confidence": confidence,
            "coherence_score": coherence_score,
            "guardian_action": guardian_action,
            "state_6d": analysis.get("query_6d", {}),
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
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "active",
        "queries_processed": counter,
        "server": "Glow Reasoning Server",
        "pipeline": "L1 → L7 → L5 → L4"
    })


if __name__ == '__main__':
    print("""
    ════════════════════════════════════════════════════════════════════════════════
    GLOW REASONING SERVER - INTEGRATED PIPELINE
    ════════════════════════════════════════════════════════════════════════════════
    
    Systems:
      ✓ L1: Primitive field activation (COHERENCE_LATTICE_SELF_AWARE)
      ✓ L7: Meta-coherence pattern detection (EMERGENT_PATTERNS)
      ✓ L5: Coherence validation (5 UNIVERSAL PRINCIPLES)
      ✓ L4: Emergence telemetry (PATTERN_TRACKING)
    
    Endpoints:
      POST /query               - Main reasoning endpoint
      GET  /health              - Server status
    
    Starting on http://127.0.0.1:5556
    Press Ctrl+C to stop
    ════════════════════════════════════════════════════════════════════════════════
    """)
    app.run(port=5556, debug=False)
