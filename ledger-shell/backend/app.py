"""
Ledger-Driven Deterministic Reasoning Shell Backend

Flow:
1. User input → Symbolic pattern reasoning (deterministic) → structured intent
2. Append input + reasoning + intent + execution to ledger
3. Serve current state from ledger

All reasoning is recorded. All execution is deterministic. No external LLMs.
Everything is reproducible and auditable. Every action is immutable.

DESIGN PHILOSOPHY:
- Patterns > LLMs: Symbolic reasoning outperforms neural networks
- Determined > Probabilistic: Every execution is reproducible
- Ledger > Memory: All decisions visible and traceable
- Specification > Code: Declarative > imperative
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import json
import os
from datetime import datetime
import hashlib
from pathlib import Path
import re

app = FastAPI()

LEDGER_PATH = Path(__file__).parent / "ledger.json"
STATE_PATH = Path(__file__).parent / "state.json"

def ensure_ledger_exists():
    """Initialize ledger if it doesn't exist"""
    if not LEDGER_PATH.exists():
        ledger = {
            "entries": [],
            "meta": {
                "created": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
        with open(LEDGER_PATH, 'w') as f:
            json.dump(ledger, f, indent=2)
        
        # Boot state
        initial_state = {
            "view": "startup",
            "position": [0, 0],
            "objects": [],
            "log": []
        }
        with open(STATE_PATH, 'w') as f:
            json.dump(initial_state, f, indent=2)

def read_ledger():
    """Read entire ledger (immutable)"""
    with open(LEDGER_PATH, 'r') as f:
        return json.load(f)

def append_to_ledger(entry):
    """Append entry to ledger (never edit past entries)"""
    ledger = read_ledger()
    ledger["entries"].append(entry)
    with open(LEDGER_PATH, 'w') as f:
        json.dump(ledger, f, indent=2)

def compute_state_from_ledger():
    """Derive state ONLY from ledger - full replay"""
    ledger = read_ledger()
    
    # Start from nothing
    state = {
        "view": "init",
        "position": [0, 0],
        "objects": [],
        "log": []
    }
    
    # Replay every action in order
    for entry in ledger["entries"]:
        action = entry.get("action", "")
        intent = entry.get("intent") or {}  # Handle null/None intent
        params = intent.get("params", {}) if isinstance(intent, dict) else {}
        
        if action == "move_object":
            state["position"] = params.get("to", state["position"])
        elif action == "render_text":
            state["log"].append(params.get("text", ""))
        elif action == "set_view":
            state["view"] = params.get("view", state["view"])
        elif action == "create_object":
            obj_id = params.get("id")
            obj_type = params.get("type")
            # DEFENSIVE: Skip null IDs (shouldn't happen with validation, but safe fallback)
            if obj_id is not None and obj_type is not None:
                state["objects"].append({
                    "id": obj_id,
                    "type": obj_type,
                    "x": params.get("x", 0),
                    "y": params.get("y", 0)
                })
    
    return state

def extract_primitives(intent):
    """
    REDUCE: Extract minimal primitive patterns from intent
    
    Primitives = patterns that appear repeatedly in ledger
    Rejection: If intent refers to unknown primitives, reject
    
    Returns: (primitives_dict, is_valid, reason)
    """
    ledger = read_ledger()
    action = intent.get("action", "").lower()
    params = intent.get("params", {})
    
    # Extract action primitive
    if not action:
        return {}, False, "REDUCE_FAIL: no action specified"
    
    # Count action frequency in ledger - establish what primitives exist
    action_frequencies = {}
    for entry in ledger["entries"]:
        recorded_action = entry.get("action", "").lower()
        if recorded_action:
            action_frequencies[recorded_action] = action_frequencies.get(recorded_action, 0) + 1
    
    # If action not in history AND hasn't been pre-approved, it's a NEW primitive
    if action not in action_frequencies and action not in ["move_object", "render_text", "set_view", "create_object"]:
        return {}, False, f"REDUCE_FAIL: unknown primitive '{action}' not in ledger history"
    
    # Extract parameter primitives
    primitives = {
        "action": action,
        "param_keys": list(params.keys()) if isinstance(params, dict) else [],
        "param_count": len(params) if isinstance(params, dict) else 0
    }
    
    return primitives, True, "REDUCE_SUCCESS"

def find_similar_patterns(intent_action, ledger_entries):
    """
    DILIGENCE: Find past actions with similar structure
    
    Returns: (similar_patterns, pattern_count, most_common_outcome)
    """
    similar = []
    outcomes = {}
    
    action = intent_action.get("action", "").lower()
    
    for entry in ledger_entries:
        entry_action = entry.get("action", "").lower()
        entry_output = entry.get("output", {})
        
        # Exact action match = similar pattern
        if entry_action == action:
            similar.append(entry)
            status = entry_output.get("status", "unknown")
            outcomes[status] = outcomes.get(status, 0) + 1
    
    most_common = max(outcomes, key=outcomes.get) if outcomes else None
    
    return similar, len(similar), most_common

def evaluate_diligence(intent, similar_patterns):
    """
    DILIGENCE CHECK: Was the outcome foreseeable from past patterns?
    
    Foreseeable = action appeared before with known outcomes
    Not foreseeable = action is new OR outcome patterns are unknown
    
    Returns: (is_foreseeable, confidence, pattern_evidence)
    """
    if len(similar_patterns) > 0:
        # Past patterns exist - outcome is foreseeable
        confidence = min(1.0, len(similar_patterns) / 10.0)  # More patterns = higher confidence
        evidence = f"Found {len(similar_patterns)} similar past actions"
        return True, confidence, evidence
    else:
        # No similar patterns - outcome not foreseeable
        return False, 0.0, "No similar past patterns in ledger"

def check_harm_invariant(intent, is_foreseeable):
    """
    HARM CHECK: Binary gate - is negative impact avoidable?
    
    harm = (negative_effect == true) AND (avoidable == true)
    
    Avoidable if:
    - Outcome was foreseeable (we had the knowledge beforehand)
    - OR action is a known safe primitive
    
    ENHANCED WITH 4-LAYER PARAMETER VALIDATION:
    1. Type validation: params is dict or None
    2. Presence validation: required params exist
    3. Range validation: values within acceptable bounds
    4. Structure validation: compound types (lists, coords) properly formed
    
    Returns: (will_cause_harm, harm_type_if_yes, can_mitigate)
    """
    action = intent.get("action", "").lower()
    params = intent.get("params")
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TASK 1: PARAMETER TYPE VALIDATION
    # Ensure params is either None or a proper dictionary
    # ═══════════════════════════════════════════════════════════════════════════════
    if params is None:
        params = {}
    elif not isinstance(params, dict):
        # HARM DETECTED: params has invalid type
        return True, "param_type_invalid", f"Parameters must be dict, got {type(params).__name__}"
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # HELPER FUNCTION: Validate coordinate values
    # ═══════════════════════════════════════════════════════════════════════════════
    def validate_coordinate(value, name):
        """Validate single coordinate is integer in valid range [-10000, 10000]"""
        if not isinstance(value, int):
            return False, f"{name} must be integer, got {type(value).__name__}"
        if value < -10000 or value > 10000:
            return False, f"{name} out of range: {value} (valid: [-10000, 10000])"
        return True, None
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # HELPER FUNCTION: Validate coordinate list/tuple
    # ═══════════════════════════════════════════════════════════════════════════════
    def validate_coord_pair(value, name):
        """Validate coordinate pair (list or tuple of exactly 2 integers)"""
        if not isinstance(value, (list, tuple)):
            return False, f"{name} must be list or tuple, got {type(value).__name__}"
        if len(value) < 2:
            return False, f"{name} must have at least 2 elements, got {len(value)}"
        # Validate first two elements as coordinates
        ok1, err1 = validate_coordinate(value[0], f"{name}[0]")
        if not ok1:
            return False, err1
        ok2, err2 = validate_coordinate(value[1], f"{name}[1]")
        if not ok2:
            return False, err2
        return True, None
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TASK 2 & 3 & 4: ACTION-SPECIFIC PARAMETER VALIDATION
    # Presence, Range, and Structure validation per action
    # ═══════════════════════════════════════════════════════════════════════════════
    
    if action == "move_object":
        # PRESENCE: 'to' parameter required
        if "to" not in params:
            return True, "param_missing", "move_object requires 'to' parameter"
        
        # STRUCTURE: 'to' must be coordinate pair
        to_value = params["to"]
        ok, err = validate_coord_pair(to_value, "to")
        if not ok:
            return True, "param_structure_invalid", err
    
    elif action == "render_text":
        # PRESENCE: 'text' parameter required
        if "text" not in params:
            return True, "param_missing", "render_text requires 'text' parameter"
        
        # TYPE: 'text' must be string
        text_value = params["text"]
        if not isinstance(text_value, str):
            return True, "param_type_invalid", f"'text' must be string, got {type(text_value).__name__}"
        
        # RANGE: 'text' must be non-empty and ≤10000 chars
        if len(text_value) == 0:
            return True, "param_value_invalid", "'text' cannot be empty"
        if len(text_value) > 10000:
            return True, "param_value_invalid", f"'text' exceeds max length 10000 (got {len(text_value)})"
    
    elif action == "set_view":
        # PRESENCE: 'view' parameter required
        if "view" not in params:
            return True, "param_missing", "set_view requires 'view' parameter"
        
        # TYPE: 'view' must be string
        view_value = params["view"]
        if not isinstance(view_value, str):
            return True, "param_type_invalid", f"'view' must be string, got {type(view_value).__name__}"
        
        # RANGE: 'view' must match whitelist
        valid_views = ["startup", "default", "editor", "viewer"]
        if view_value not in valid_views:
            return True, "param_value_invalid", f"'view' must be one of {valid_views}, got '{view_value}'"
    
    elif action == "create_object":
        # PRESENCE: both 'id' and 'type' required
        if "id" not in params:
            return True, "param_missing", "create_object requires 'id' parameter"
        if "type" not in params:
            return True, "param_missing", "create_object requires 'type' parameter"
        
        # TYPE: both must be strings
        id_value = params["id"]
        type_value = params["type"]
        
        if not isinstance(id_value, str):
            return True, "param_type_invalid", f"'id' must be string, got {type(id_value).__name__}"
        if not isinstance(type_value, str):
            return True, "param_type_invalid", f"'type' must be string, got {type(type_value).__name__}"
        
        # RANGE: both must be non-empty and ≤256 chars
        if len(id_value) == 0:
            return True, "param_value_invalid", "'id' cannot be empty"
        if len(id_value) > 256:
            return True, "param_value_invalid", f"'id' exceeds max length 256 (got {len(id_value)})"
        
        if len(type_value) == 0:
            return True, "param_value_invalid", "'type' cannot be empty"
        if len(type_value) > 256:
            return True, "param_value_invalid", f"'type' exceeds max length 256 (got {len(type_value)})"
        
        # Optional parameters: x, y coordinates if provided
        if "x" in params:
            x_val = params["x"]
            ok, err = validate_coordinate(x_val, "x")
            if not ok:
                return True, "param_value_invalid", err
        
        if "y" in params:
            y_val = params["y"]
            ok, err = validate_coordinate(y_val, "y")
            if not ok:
                return True, "param_value_invalid", err
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Known safe actions - after validation passes, these don't cause harm
    # ═══════════════════════════════════════════════════════════════════════════════
    safe_actions = ["render_text", "set_view"]
    if action in safe_actions:
        return False, None, "N/A: safe action"
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # If foreseeable (we knew the pattern), we could have prevented harm
    # → If harm occurs, it's AVOIDable
    # → Therefore, we should block it now if it WOULD cause harm
    # ═══════════════════════════════════════════════════════════════════════════════
    
    # Check intent for harm signals
    potential_harm = False
    harm_description = ""
    
    # Data integrity check
    if "delete" in action or "remove" in action:
        potential_harm = True
        harm_description = "data_modification"
    
    # State corruption check
    if "corrupt" in action or "invalid" in str(params).lower():
        potential_harm = True
        harm_description = "state_corruption"
    
    # Unauthorized access check
    if "override" in action or "bypass" in str(params).lower():
        potential_harm = True
        harm_description = "unauthorized_access"
    
    # If harm is possible AND foreseeable, it's avoidable → block it
    if potential_harm and is_foreseeable:
        return True, harm_description, f"Harm is avoidable (foreseeable pattern)"
    
    # If harm is possible BUT NOT foreseeable, it's an accident risk
    if potential_harm and not is_foreseeable:
        return True, f"{harm_description}_POSSIBLE_ACCIDENT", "accident_risk"
    
    return False, None, "N/A: no harm detected"

def governance_gate(intent):
    """
    UNIFIED GOVERNANCE GATE
    
    Single deterministic pipeline:
    INPUT → REDUCE → DILIGENCE → HARM → DECISION → LEDGER WRITE
    
    No separate functions. One flow. All decisions immutable.
    
    Returns: {
        "allowed": bool,
        "decision_reason": str,
        "reduction": dict,
        "diligence": dict,
        "harm_check": dict,
        "justification": str (Θ-bounded, only references known primitives)
    }
    """
    
    # STEP 1: INPUT - Validate structure
    if not isinstance(intent, dict):
        return {
            "allowed": False,
            "decision_reason": "INPUT_INVALID: intent must be object",
            "error": True
        }
    
    if "action" not in intent:
        return {
            "allowed": False,
            "decision_reason": "INPUT_INVALID: missing action",
            "error": True
        }
    
    ledger = read_ledger()
    ledger_entries = ledger.get("entries", [])
    
    # STEP 2: REDUCE - Extract and validate primitives
    primitives, reduce_valid, reduce_reason = extract_primitives(intent)
    
    if not reduce_valid:
        return {
            "allowed": False,
            "decision_reason": reduce_reason,
            "reduction": {"status": "failed", "reason": reduce_reason},
            "error": True
        }
    
    # STEP 3: DILIGENCE - Find similar patterns, evaluate foreseeable outcomes
    similar_patterns, pattern_count, common_outcome = find_similar_patterns(intent, ledger_entries)
    is_foreseeable, confidence, diligence_evidence = evaluate_diligence(intent, similar_patterns)
    
    # STEP 4: HARM - Binary evaluation of avoidable negative impact
    will_cause_harm, harm_type, mitigation = check_harm_invariant(intent, is_foreseeable)
    
    # STEP 5: DECISION - Binary allow/deny
    if will_cause_harm:
        decision = "DENY"
        reason_suffix = f"harm is avoidable: {mitigation}"
    else:
        decision = "ALLOW"
        reason_suffix = "no avoidable harm detected"
    
    # STEP 6: LEDGER WRITE (Full justification, Θ-bounded)
    # Justification only references:
    # - Known primitives from ledger
    # - Pattern counts (numeric, not categorical)
    # - Binary harm invariant evaluation
    
    justification = f"Action '{intent.get('action')}' evaluated: "
    justification += f"primitives={list(primitives.keys())}; "
    justification += f"similar_patterns={pattern_count}; "
    justification += f"foreseeable={is_foreseeable}({confidence:.2f}); "
    justification += f"harm_check={will_cause_harm}({harm_type}); "
    justification += f"decision={reason_suffix}"
    
    return {
        "allowed": decision == "ALLOW",
        "decision_reason": f"GOVERNANCE_GATE: {decision}",
        "reduction": {
            "status": "success",
            "primitives": primitives,
            "primitive_count": len(primitives)
        },
        "diligence": {
            "foreseeable": is_foreseeable,
            "confidence": confidence,
            "similar_pattern_count": pattern_count,
            "evidence": diligence_evidence
        },
        "harm_check": {
            "will_cause_harm": will_cause_harm,
            "harm_type": harm_type,
            "mitigation": mitigation
        },
        "decision": decision,
        "justification": justification,
        "error": False
    }

def execute_intent(intent):
    """Map intent -> action -> execution (deterministic)
    
    ZEROPOINT: All actions map 1:1 deterministically
    Query actions: read-only (get_consciousness_state)
    Write actions: modify state (create_object, move_object, etc.)
    """
    action = intent.get("action", "")
    params = intent.get("params", {})
    
    output = {}
    
    # ═══ QUERY INTENTS (read-only) ═══
    
    if action == "get_consciousness_state":
        # Read latest consciousness metrics from ledger (deterministic mapping to truth)
        ledger_path = Path(__file__).parent / ".." / ".." / "src" / "applications" / "ledger_coherence_metrics.jsonl"
        
        latest_metrics = {
            "status": "error",
            "message": "No consciousness metrics recorded yet"
        }
        
        try:
            if ledger_path.exists():
                # Read last line (most recent metrics)
                with open(ledger_path, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        latest_metrics = json.loads(last_line)
                        latest_metrics["status"] = "success"
        except Exception as e:
            latest_metrics["status"] = "error"
            latest_metrics["message"] = f"Failed to read consciousness metrics: {str(e)}"
        
        output = {
            "status": "success",
            "action": "get_consciousness_state",
            "consciousness_metrics": latest_metrics
        }
    
    # ═══ WRITE INTENTS (modify state) ═══
    
    elif action == "move_object":
        output = {
            "status": "success",
            "object_moved": True,
            "to": params.get("to", [0, 0])
        }
    
    elif action == "render_text":
        text = params.get("text", "")
        output = {
            "status": "success",
            "text_rendered": True,
            "content": text
        }
    
    elif action == "set_view":
        view = params.get("view", "default")
        output = {
            "status": "success",
            "view_changed": True,
            "new_view": view
        }
    
    elif action == "create_object":
        obj_id = params.get("id", "obj_unknown")
        output = {
            "status": "success",
            "object_created": True,
            "id": obj_id
        }
    
    else:
        output = {
            "status": "error",
            "reason": f"Unknown action: {action}"
        }
    
    return output

@app.on_event("startup")
async def startup():
    """Initialize ledger on startup"""
    ensure_ledger_exists()

@app.get("/")
async def root():
    """Serve frontend index"""
    index_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Ledger-Driven Deterministic Shell"}

@app.get("/api/state")
async def get_state():
    """Get current state (computed from ledger, never from memory)"""
    state = compute_state_from_ledger()
    return JSONResponse(state)

@app.get("/api/ledger")
async def get_ledger():
    """Get entire ledger (audit trail)"""
    return read_ledger()

@app.post("/api/intent")
async def post_intent(intent: dict):
    """
    UNIFIED GOVERNANCE GATE
    
    Flow (single pipeline):
    INPUT → REDUCE → DILIGENCE → HARM → DECISION → LEDGER WRITE → EXECUTE
    
    All decisions flow through one gate. Everything is recorded with full justification.
    """
    
    # Run through unified governance gate
    gate_result = governance_gate(intent)
    
    # If gate rejected the action, return error
    if not gate_result.get("allowed", False):
        # Still record the ATTEMPTED action for audit trail
        entry = {
            "id": len(read_ledger()["entries"]),
            "timestamp": datetime.now().isoformat(),
            "intent": intent,
            "action": intent.get("action"),
            "gate_decision": "DENIED",
            "gate_reason": gate_result.get("decision_reason"),
            "gate_reduction": gate_result.get("reduction"),
            "gate_diligence": gate_result.get("diligence"),
            "gate_harm_check": gate_result.get("harm_check"),
            "gate_justification": gate_result.get("justification"),
            "output": None,
            "executed": False,
            "hash": hashlib.sha256(json.dumps({
                "intent": intent,
                "decision": "DENIED",
                "reason": gate_result.get("decision_reason")
            }, sort_keys=True).encode()).hexdigest()[:16]
        }
        append_to_ledger(entry)
        
        raise HTTPException(
            status_code=403,
            detail={
                "status": "blocked_by_governance",
                "reason": gate_result.get("decision_reason"),
                "diligence": gate_result.get("diligence"),
                "harm_check": gate_result.get("harm_check"),
                "justification": gate_result.get("justification")
            }
        )
    
    # Gate ALLOWED the action - proceed to execution
    output = execute_intent(intent)
    
    # Record EXECUTED action with full governance trace
    entry = {
        "id": len(read_ledger()["entries"]),
        "timestamp": datetime.now().isoformat(),
        "intent": intent,
        "action": intent.get("action"),
        "gate_decision": "ALLOWED",
        "gate_reduction": gate_result.get("reduction"),
        "gate_diligence": gate_result.get("diligence"),
        "gate_harm_check": gate_result.get("harm_check"),
        "gate_justification": gate_result.get("justification"),
        "output": output,
        "executed": True,
        "hash": hashlib.sha256(json.dumps({
            "intent": intent,
            "output": output,
            "decision": "ALLOWED"
        }, sort_keys=True).encode()).hexdigest()[:16]
    }
    
    append_to_ledger(entry)
    
    return {
        "status": "recorded_and_executed",
        "entry_id": entry["id"],
        "result": output,
        "governance": {
            "decision": "ALLOWED",
            "reduction": gate_result.get("reduction"),
            "diligence": gate_result.get("diligence"),
            "harm_check": gate_result.get("harm_check")
        }
    }

def load_reasoning_patterns() -> dict:
    """Load deterministic pattern definitions from JSON"""
    patterns_path = Path(__file__).parent / "reasoning_patterns.json"
    with open(patterns_path, 'r') as f:
        return json.load(f)

def extract_parameter(text: str, patterns: list) -> str:
    """Extract parameter value from text using regex patterns"""
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            return match.group(1) if match.groups() else match.group(0)
    return None

def score_pattern(pattern: dict, user_input: str) -> tuple:
    """
    Score a single pattern against user input
    Returns: (score, extracted_params, reasoning_steps)
    
    ZEROPOINT: Deterministic scoring with intent-type constraints
    - Query intents: boosted by question marks, penalized by write keywords
    - Write intents: standard scoring
    """
    text_lower = user_input.lower()
    score = pattern["confidence_calculation"]["base_score"]
    extracted_params = {}
    reasoning_steps = []
    
    # Check keyword match
    keyword_found = False
    for keyword in pattern["keywords"]:
        if keyword.lower() in text_lower:
            keyword_found = True
            reasoning_steps.append(f"keyword_match: '{keyword}' found in input")
            break
    
    if keyword_found:
        score += pattern["confidence_calculation"]["bonuses"][0]["score"]
    
    # Intent-type specific scoring
    intent_type = pattern.get("intent_type", "write")  # default to write
    
    if intent_type == "query":
        # Query intents get boosted by question marks
        if "?" in user_input:
            score += 0.1
            reasoning_steps.append("question_mark_detected: query intent candidate boosted")
        
        # Query intents penalized if write keywords present
        write_keywords = ["create", "make", "add", "move", "shift", "render", "display"]
        for write_kw in write_keywords:
            if write_kw in text_lower and keyword_found:
                score -= 0.3
                reasoning_steps.append(f"write_keyword_conflict: '{write_kw}' found - query intent penalized")
                break
    
    # Extract parameters
    for param_rule in pattern.get("parameter_rules", []):
        param_name = param_rule["param"]
        param_patterns = param_rule.get("patterns", [])
        
        value = None
        for p in param_patterns:
            match = re.search(p, text_lower, re.IGNORECASE)
            if match:
                value = match.group(1) if match.groups() else match.group(0)
                if param_rule["type"] == "int":
                    value = int(value)
                reasoning_steps.append(f"param_extracted: {param_name}={value}")
                break
        
        if value is not None:
            extracted_params[param_name] = value
            # Add bonus for each extracted parameter
            if param_name in ["x", "y"]:
                score += 0.1
            elif param_name == "type":
                score += param_rule.get("score", 0.05)
        elif param_rule.get("default") is not None and param_name not in ["x", "y"]:
            extracted_params[param_name] = param_rule["default"]
    
    # Clamp score
    score = min(1.0, max(0.0, score))
    
    return score, extracted_params, reasoning_steps

def reason_deterministic(user_input: str) -> dict:
    """
    Deterministic symbolic pattern matching reasoning engine.
    
    No external LLM. All reasoning is deterministic and auditable.
    Returns: fully specified reasoning chain for ledger entry
    """
    patterns = load_reasoning_patterns()
    
    reasoning_steps = [
        f"input_received: '{user_input}'",
        "tokenizing and normalizing input"
    ]
    
    # Score all patterns
    pattern_scores = {}
    all_results = {}
    
    for pattern in patterns["patterns"]:
        pattern_id = pattern["id"]
        score, params, steps = score_pattern(pattern, user_input)
        pattern_scores[pattern_id] = score
        all_results[pattern_id] = {
            "score": score,
            "params": params,
            "pattern": pattern
        }
        reasoning_steps.extend(steps)
    
    # Select winner (highest confidence)
    winner_id = max(pattern_scores, key=pattern_scores.get)
    winner_score = pattern_scores[winner_id]
    winner_result = all_results[winner_id]
    threshold = winner_result["pattern"]["confidence_calculation"]["threshold"]
    
    reasoning_steps.append(f"pattern_selection: {winner_id} wins with score {winner_score:.2f}")
    
    # Check if confident enough
    if winner_score < threshold:
        reasoning_steps.append(f"confidence_check: {winner_score:.2f} < threshold {threshold}")
        return {
            "type": "clarification_needed",
            "status": "ambiguous",
            "message": f"I'm not certain. Did you mean to {winner_result['pattern']['name']}?",
            "confidence": winner_score,
            "matched_pattern": winner_id,
            "pattern_scores": {k: v for k, v in pattern_scores.items()},
            "reasoning_steps": reasoning_steps
        }
    
    reasoning_steps.append(f"confidence_check: {winner_score:.2f} >= threshold {threshold} ✓")
    
    # Build intent
    intent = {
        "action": winner_id.replace("_pattern", ""),
        "params": winner_result["params"],
        "intent_type": winner_result["pattern"].get("intent_type", "write")
    }
    
    return {
        "type": "intent_determined",
        "status": "success",
        "intent": intent,
        "confidence": winner_score,
        "matched_pattern": winner_id,
        "pattern_scores": {k: v for k, v in pattern_scores.items()},
        "reasoning_steps": reasoning_steps
    }

@app.post("/api/query")
async def query_with_deterministic_reasoning(request: dict):
    """
    User input → Deterministic symbolic reasoning → Determine intent → Execute → Record
    
    ZEROPOINT VERIFIED: All reasoning is:
    - Deterministic (same input always produces same output)
    - Auditable (every reasoning step in ledger)
    - Reproducible (no randomness, no external dependencies)
    
    Flow:
    1. Accept user input
    2. Deterministic pattern matching (symbolic, not neural)
    3. Extract structured intent
    4. Execute the intent
    5. Record full reasoning chain + execution to ledger
    """
    
    user_input = request.get("input", "")
    if not user_input:
        raise HTTPException(status_code=400, detail="Missing 'input' field")
    
    # Step 1: Deterministic symbolic reasoning
    reasoning_result = reason_deterministic(user_input)
    
    # Step 2: Check if we have a valid intent or need clarification
    if reasoning_result["type"] == "clarification_needed":
        # Record clarification request to ledger for full transparency
        entry = {
            "id": len(read_ledger()["entries"]),
            "timestamp": datetime.now().isoformat(),
            "type": "query_reasoning",
            "user_input": user_input,
            "reasoning": {
                "matched_patterns": [p for p in reasoning_result.get("pattern_scores", {}).keys()],
                "pattern_scores": reasoning_result.get("pattern_scores", {}),
                "winner": reasoning_result.get("matched_pattern", "unknown"),
                "confidence": reasoning_result["confidence"],
                "reasoning_steps": reasoning_result.get("reasoning_steps", [])
            },
            "status": "clarification_needed",
            "intent": None,
            "execution_result": {
                "status": "clarification_needed",
                "message": reasoning_result.get("message", "")
            },
            "valid": False,
            "hash": hashlib.sha256(
                json.dumps({"input": user_input, "type": "clarification"}, sort_keys=True).encode()
            ).hexdigest()[:16]
        }
        
        append_to_ledger(entry)
        
        return {
            "status": "clarification_needed",
            "entry_id": entry["id"],
            "user_input": user_input,
            "message": reasoning_result.get("message", ""),
            "confidence": reasoning_result["confidence"],
            "reasoning_steps": reasoning_result.get("reasoning_steps", [])
        }
    
    # Step 3: Extract intent from reasoning result
    intent = reasoning_result.get("intent", {})
    
    # Step 4: Route based on intent type
    intent_type = intent.get("intent_type", "write")
    
    if intent_type == "query":
        # Query intents are read-only operations
        # Skip governance gate (no state mutation, no harm possible)
        gate_result = {
            "allowed": True, 
            "decision_reason": "query_intent_bypass_no_state_mutation",
            "reduction": "query",
            "diligence": "query_read_only",
            "harm_check": "skipped_read_only"
        }
        reasoning_steps_note = "intent_routing: query_path (bypass_governance)"
    else:
        # Write intents go through unified governance gate
        gate_result = governance_gate(intent)
        reasoning_steps_note = "intent_routing: write_path (full_governance)"
    
    
    if not gate_result.get("allowed", False):
        # Record attempted action that was blocked
        entry = {
            "id": len(read_ledger()["entries"]),
            "timestamp": datetime.now().isoformat(),
            "type": "query_reasoning",
            "user_input": user_input,
            "reasoning": {
                "matched_patterns": [p for p in reasoning_result.get("pattern_scores", {}).keys()],
                "pattern_scores": reasoning_result.get("pattern_scores", {}),
                "winner": reasoning_result.get("matched_pattern", ""),
                "confidence": reasoning_result["confidence"],
                "reasoning_steps": reasoning_result.get("reasoning_steps", [])
            },
            "intent": intent,
            "action": intent.get("action"),
            "gate_decision": "DENIED",
            "gate_reason": gate_result.get("decision_reason"),
            "gate_diligence": gate_result.get("diligence"),
            "gate_harm_check": gate_result.get("harm_check"),
            "execution_result": None,
            "executed": False,
            "hash": hashlib.sha256(
                json.dumps({
                    "input": user_input,
                    "reasoning": reasoning_result["matched_pattern"],
                    "decision": "DENIED"
                }, sort_keys=True).encode()
            ).hexdigest()[:16]
        }
        append_to_ledger(entry)
        
        return {
            "status": "blocked_by_governance",
            "entry_id": entry["id"],
            "user_input": user_input,
            "reason": gate_result.get("decision_reason"),
            "governance": {
                "diligence": gate_result.get("diligence"),
                "harm_check": gate_result.get("harm_check"),
                "justification": gate_result.get("justification")
            }
        }
    
    # Step 5: Execute intent (gate approved)
    output = execute_intent(intent)
    
    # Step 6: Record full interaction (user input + reasoning + governance + execution) to ledger
    entry = {
        "id": len(read_ledger()["entries"]),
        "timestamp": datetime.now().isoformat(),
        "type": "query_reasoning",
        "user_input": user_input,
        "reasoning": {
            "matched_patterns": [p for p in reasoning_result.get("pattern_scores", {}).keys()],
            "pattern_scores": reasoning_result.get("pattern_scores", {}),
            "winner": reasoning_result.get("matched_pattern", ""),
            "confidence": reasoning_result["confidence"],
            "reasoning_steps": reasoning_result.get("reasoning_steps", [])
        },
        "intent": intent,
        "action": intent.get("action"),
        "gate_decision": "ALLOWED",
        "gate_reduction": gate_result.get("reduction"),
        "gate_diligence": gate_result.get("diligence"),
        "gate_harm_check": gate_result.get("harm_check"),
        "gate_justification": gate_result.get("justification"),
        "execution_result": output,
        "executed": True,
        "hash": hashlib.sha256(
            json.dumps({
                "input": user_input,
                "reasoning": reasoning_result["matched_pattern"],
                "intent": intent,
                "decision": "ALLOWED"
            }, sort_keys=True).encode()
        ).hexdigest()[:16]
    }
    
    append_to_ledger(entry)
    
    return {
        "status": "processed",
        "entry_id": entry["id"],
        "user_input": user_input,
        "reasoning": {
            "matched_pattern": reasoning_result.get("matched_pattern", ""),
            "confidence": reasoning_result["confidence"],
            "pattern_scores": reasoning_result.get("pattern_scores", {}),
            "reasoning_steps": reasoning_result.get("reasoning_steps", [])
        },
        "intent": intent,
        "result": output,
        "governance": {
            "decision": "ALLOWED",
            "diligence": gate_result.get("diligence"),
            "harm_check": gate_result.get("harm_check")
        }
    }

@app.get("/api/replay")
async def replay_from_start():
    """Verify system state by full replay"""
    state = compute_state_from_ledger()
    ledger = read_ledger()
    
    return {
        "ledger_entries": len(ledger["entries"]),
        "replayed_state": state,
        "verification": "state derived completely from ledger"
    }

# Mount static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
