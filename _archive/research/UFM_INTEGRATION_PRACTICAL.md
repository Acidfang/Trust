# UFM API PRACTICAL INTEGRATION GUIDE
**How to Actually Use UFM in Your Project Workflow**

---

## PART 1: SETTING UP UFM CLIENT

### 1.1 Python Integration

The project includes `UFM_CLIENT.py` with a singleton pattern:

```python
from UFM_CLIENT import get_ufm_client

# Get client (lazy-loaded singleton)
client = get_ufm_client()

# Health check before making calls
health = client.health()
if health.get('status') == 'online':
    print(f"UFM online, version: {health.get('engine_version')}")
else:
    print(f"UFM offline: {health}")
```

### 1.2 API Key Management

**Production Key** (stored in UFM_CLIENT.py):
```
ufm_live_8f430fc7.Psl_W4LR5Y_4C1EVmdIgQWrtoNyv65Rx4jvmYW2H2DA
```

**Base URL**:
```
https://ufm-engine.onrender.com
```

---

## PART 2: DECISION WORKFLOW IN PRACTICE

### 2.1 Basic Decision Validation

```python
import json
import base64
from UFM_CLIENT import get_ufm_client

def validate_ai_decision(choice_description, tree_path, reasoning, risk_score):
    """
    Validate AI decision through UFM pipeline
    
    Args:
        choice_description: What are you choosing? (string)
        tree_path: A1, A2, B1, C1, or D1 (string)
        reasoning: Why this path? (string)
        risk_score: 0.0-1.0 assessment (float)
    
    Returns:
        {
            "valid": True/False,
            "quality_score": 0.0-1.0,
            "recommendation": "proceed" or "reconsider",
            "causal_principles": [...]
        }
    """
    
    # Build decision object
    decision = {
        "timestamp": "2026-04-05T10:30:00Z",  # Use actual timestamp
        "choice": choice_description,
        "framework_alignment": "YES",  # Assuming framework-aligned
        "risk_score": risk_score,
        "causal_tree_path": tree_path,
        "reasoning": reasoning,
        "classification": tree_path[0]  # A/B/C/D from path like "A1"
    }
    
    # Encode as base64
    json_str = json.dumps(decision)
    b64_encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    # Call UFM API
    client = get_ufm_client()
    result = client.process_universal(json_str.encode('utf-8'), verify=True)
    
    # Extract validation result
    quality_score = result.get('quality_score', 0.0)
    is_valid = result.get('is_valid', False)
    
    # Determine recommendation
    if quality_score > 0.75 and is_valid:
        recommendation = "proceed"
    else:
        recommendation = "reconsider"
    
    return {
        "valid": is_valid,
        "quality_score": quality_score,
        "recommendation": recommendation,
        "causal_principles": result.get('causal_principles', []),
        "full_result": result
    }

# Usage example:
result = validate_ai_decision(
    choice_description="Add /api/statistics endpoint to UNIFIED_API_SERVER",
    tree_path="A1",
    reasoning="Framework-aligned pattern, existing precedent for endpoints",
    risk_score=0.15
)

if result['recommendation'] == 'proceed':
    print(f"✓ Decision approved (quality: {result['quality_score']:.2f})")
    # Proceed with implementation
else:
    print(f"✗ Decision needs review (quality: {result['quality_score']:.2f})")
    # Reconsider and build different tree
```

---

### 2.2 Comparing Two Possible Paths

```python
def compare_two_paths(path_a_desc, path_b_desc):
    """
    Use UFM to compare two possible decision paths
    
    Returns recommendation for which path is better
    """
    
    # Encode both paths
    path_a_b64 = base64.b64encode(path_a_desc.encode()).decode()
    path_b_b64 = base64.b64encode(path_b_desc.encode()).decode()
    
    # Call comparison endpoint
    client = get_ufm_client()
    result = client.compare(
        path_a_desc.encode(),
        path_b_desc.encode(),
        symbol_length_mode="auto_curve"
    )
    
    # Parse result
    overlap = result.get('overlap', 0)
    distance = result.get('distance', 1.0)
    recommendation = result.get('recommendation', 'different_category')
    
    return {
        "path_a_vs_b_overlap": overlap,
        "structural_distance": distance,
        "recommendation": recommendation,  # "choice_a", "choice_b", or "different_category"
        "result": result
    }

# Usage:
comparison = compare_two_paths(
    "Add endpoint directly to UNIFIED_API_SERVER",
    "Create new lightweight API handler module"
)

if comparison['recommendation'] == 'choice_a':
    print("✓ Path A is structurally better")
elif comparison['recommendation'] == 'choice_b':
    print("✓ Path B is structurally better")
else:
    print("⚠ Paths are fundamentally different - need different tree analysis")
```

---

### 2.3 Verifying Reversibility (Undo Path)

```python
def verify_undo_reversibility(action_description):
    """
    Verify that an action can be reversed without data loss
    
    Uses UFM's round-trip integrity check
    """
    
    # Encode action description
    action_bytes = action_description.encode()
    
    # Test round-trip (encode → decode)
    client = get_ufm_client()
    result = client.reconstruct(action_bytes)
    
    # Check if lossless
    is_lossless = result.get('lossless', False)
    round_trip_error = result.get('round_trip_error', 1.0)
    reconstructed_b64 = result.get('reconstructed_b64', '')
    
    # Verify matches
    original_b64 = base64.b64encode(action_bytes).decode()
    matches = (original_b64 == reconstructed_b64)
    
    return {
        "reversible": is_lossless and matches,
        "lossless": is_lossless,
        "round_trip_error": round_trip_error,
        "matches_original": matches,
        "recommendation": "SAFE_TO_EXECUTE" if is_lossless else "VERIFY_UNDO_FIRST"
    }

# Usage:
undo_check = verify_undo_reversibility(
    "Add new endpoint + register in framework.json"
)

if undo_check['reversible']:
    print("✓ Change is completely reversible - safe to execute")
else:
    print(f"⚠ Round-trip error: {undo_check['round_trip_error']:.4f}")
    print("✓ Verify undo mechanism manually before executing")
```

---

## PART 3: DECISION LOGGING WORKFLOW

### 3.1 Logging to Decision Ledger

```python
def log_decision_to_ledger(
    decision_choice,
    tree_path,
    ufm_result,
    execution_status="PENDING"
):
    """
    Log decision to persistent ledger for audit trail
    
    Files written to:
    - /memories/session/DECISIONS_LOG_CURRENT.md (current session)
    - src/ledgers/ai_decision_ledger.jsonl (persistent)
    """
    
    import os
    from datetime import datetime
    
    # Create session log entry
    session_entry = f"""
### Decision: {decision_choice}
**Timestamp**: {datetime.now().isoformat()}
**Tree Path**: {tree_path}
**UFM Quality**: {ufm_result['quality_score']:.2f}
**UFM Valid**: {ufm_result['is_valid']}
**Causal Principles**: {len(ufm_result.get('causal_principles', []))} verified
**Status**: {execution_status}
---
"""
    
    # Append to session log
    session_dir = "/memories/session/"
    os.makedirs(session_dir, exist_ok=True)
    
    with open(f"{session_dir}DECISIONS_LOG_CURRENT.md", "a") as f:
        f.write(session_entry)
    
    # Create persistent ledger entry (JSONL format)
    ledger_entry = {
        "timestamp": datetime.now().isoformat(),
        "decision": decision_choice,
        "tree_path": tree_path,
        "ufm_quality_score": ufm_result['quality_score'],
        "ufm_valid": ufm_result['is_valid'],
        "ufm_causal_principles_count": len(ufm_result.get('causal_principles', [])),
        "execution_status": execution_status
    }
    
    import json
    ledger_file = "src/ledgers/ai_decision_ledger.jsonl"
    os.makedirs(os.path.dirname(ledger_file), exist_ok=True)
    
    with open(ledger_file, "a") as f:
        f.write(json.dumps(ledger_entry) + "\n")
    
    return True

# Usage:
log_decision_to_ledger(
    "Add /api/statistics endpoint",
    "A1",
    ufm_result={
        'quality_score': 0.89,
        'is_valid': True,
        'causal_principles': [1, 1, 1, 1, 1, 1, 1]
    },
    execution_status="APPROVED"
)
```

---

## PART 4: FULL WORKFLOW EXAMPLE

### 4.1 Complete Decision Flow (Template)

```python
"""
Complete workflow for making AI decisions in Determined project
"""

import json
import base64
from datetime import datetime
from UFM_CLIENT import get_ufm_client

class AIDecisionWorkflow:
    """Manages full decision workflow: Tree → Gate → UFM → Log → Execute"""
    
    def __init__(self):
        self.client = get_ufm_client()
        self.decision_log = []
    
    def step_1_build_tree(self, user_request):
        """Step 1: Build causal tree"""
        return {
            "request": user_request,
            "paths": {
                "A1": {"description": "...", "pros": [...], "cons": [...]},
                "A2": {"description": "...", "pros": [...], "cons": [...]},
                "C1": {"description": "...", "rejected_because": "..."}
            },
            "chosen_path": "A1",
            "chosen_because": "..."
        }
    
    def step_2_run_gate(self, tree):
        """Step 2: Run pre-action gate (5 questions)"""
        gate_checks = {
            "q1_framework": True,
            "q2_danger_patterns": False,
            "q3_reversible": True,
            "q4_clear": True,
            "q5_aligned": True
        }
        return all(gate_checks.values())  # All must be True
    
    def step_3_call_ufm(self, tree, gate_check):
        """Step 3: Call UFM API to validate decision"""
        
        decision = {
            "timestamp": datetime.now().isoformat(),
            "choice": tree["request"],
            "tree_path": tree["chosen_path"],
            "framework_alignment": "YES",
            "risk_score": 0.15,
            "gate_check_pass": gate_check,
            "classification": tree["chosen_path"][0]
        }
        
        # Call UFM
        result = self.client.process_universal(
            json.dumps(decision).encode(),
            verify=True
        )
        
        return {
            "valid": result.get('is_valid', False),
            "quality_score": result.get('quality_score', 0.0),
            "recommendation": "proceed" if result.get('quality_score', 0) > 0.75 else "reconsider"
        }
    
    def step_4_log_decision(self, tree, gate_result, ufm_result):
        """Step 4: Log to ledger"""
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tree": tree,
            "gate_passed": gate_result,
            "ufm_quality_score": ufm_result['quality_score'],
            "ufm_valid": ufm_result['valid'],
            "status": ufm_result['recommendation']
        }
        
        self.decision_log.append(entry)
        return entry
    
    def step_5_execute(self, decision_entry):
        """Step 5: Execute (only if all previous steps passed)"""
        
        if not decision_entry['gate_passed']:
            raise Exception("Gate check failed - cannot execute")
        
        if decision_entry['ufm_quality_score'] < 0.75:
            raise Exception("UFM quality too low - cannot execute")
        
        if decision_entry['status'] != 'proceed':
            raise Exception("UFM recommendation is not proceed")
        
        # All checks passed - safe to execute
        return True

# Usage example:
workflow = AIDecisionWorkflow()

# Step 1: Build tree
tree = workflow.step_1_build_tree("Add new statistics endpoint")

# Step 2: Run gate
gate_passed = workflow.step_2_run_gate(tree)
print(f"Gate check: {'PASS' if gate_passed else 'FAIL'}")

if not gate_passed:
    print("Cannot proceed - gate check failed")
    exit(1)

# Step 3: Call UFM
ufm_result = workflow.step_3_call_ufm(tree, gate_passed)
print(f"UFM quality: {ufm_result['quality_score']:.2f}")

if ufm_result['quality_score'] < 0.75:
    print("Cannot proceed - UFM quality too low, reconsider tree")
    exit(1)

# Step 4: Log
logged_entry = workflow.step_4_log_decision(tree, gate_passed, ufm_result)

# Step 5: Execute (only if reached here)
if workflow.step_5_execute(logged_entry):
    print("✓ All validations passed - proceeding with implementation")
    # Your actual implementation code here
```

---

## PART 5: INTEGRATION WITH EXISTING SYSTEMS

### 5.1 Integration with UNIFIED_API_SERVER

```python
# In UNIFIED_API_SERVER.py

from UFM_CLIENT import get_ufm_client
import json
from flask import request, jsonify

@app.route('/api/validate_ai_decision', methods=['POST'])
def validate_ai_decision():
    """
    Endpoint for UFM validation of AI decisions
    
    POST body:
    {
        "choice": "description of choice",
        "tree_path": "A1",
        "risk_score": 0.15,
        "reasoning": "why this path"
    }
    """
    
    data = request.json
    client = get_ufm_client()
    
    # Validate decision
    decision = {
        "choice": data.get('choice'),
        "tree_path": data.get('tree_path'),
        "risk_score": data.get('risk_score'),
        "reasoning": data.get('reasoning')
    }
    
    result = client.process_universal(
        json.dumps(decision).encode(),
        verify=True
    )
    
    return jsonify({
        "valid": result.get('is_valid'),
        "quality_score": result.get('quality_score'),
        "recommendation": "proceed" if result.get('quality_score', 0) > 0.75 else "reconsider"
    })

@app.route('/api/decision_log', methods=['POST'])
def log_ai_decision():
    """
    Endpoint for logging AI decisions to ledger
    """
    
    data = request.json
    # Log to ledger (see section 3.1)
    
    return jsonify({"status": "logged"})
```

### 5.2 Integration with Framework Hot-Reload

```python
# In FRAMEWORK_HOT_RELOAD_ENGINE.py

def reload_framework_with_ufm_validation(framework_config):
    """
    Reload framework with UFM validation of framework changes
    """
    
    client = get_ufm_client()
    
    # Encode framework change as decision
    decision = {
        "change": "framework configuration update",
        "old_config": self.current_framework,
        "new_config": framework_config,
        "field_consciousness_impact": "election recorded"
    }
    
    # Validate with UFM
    result = client.process_universal(
        json.dumps(decision).encode(),
        verify=True
    )
    
    if result.get('is_valid') and result.get('quality_score', 0) > 0.75:
        # Safe to reload
        self.reload_framework(framework_config)
        self.record_election("framework_reload", decision)
        return True
    else:
        # Risk - reconsider
        raise Exception(f"Framework change rejected by UFM: quality={result.get('quality_score')}")
```

---

## PART 6: ERROR HANDLING & RECOVERY

### 6.1 UFM API Failures

```python
def make_decision_with_fallback(decision_dict):
    """
    Make decision with fallback if UFM unavailable
    """
    
    client = get_ufm_client()
    
    try:
        # Try to call UFM
        result = client.process_universal(
            json.dumps(decision_dict).encode(),
            verify=True
        )
        
        # Check result
        if result.get('quality_score', 0) > 0.75:
            return {"status": "approved_by_ufm", "data": result}
        else:
            return {"status": "rejected_by_ufm", "data": result}
    
    except Exception as e:
        # UFM unavailable or error
        print(f"UFM error: {e}")
        print("Falling back to local pre-action gate")
        
        # Run local gate as fallback
        gate_result = run_local_pre_action_gate(decision_dict)
        
        if gate_result:
            print("⚠ Local gate passed, proceeding with caution (no UFM validation)")
            return {"status": "approved_by_local_gate_fallback", "data": gate_result}
        else:
            print("✗ Both UFM and local gate failed - DO NOT PROCEED")
            return {"status": "rejected", "data": gate_result}
```

---

## PART 7: QUICK COPY-PASTE SNIPPETS

### Validate Single Decision

```python
from UFM_CLIENT import get_ufm_client
import json
import base64

client = get_ufm_client()
decision = {"choice": "YOUR CHOICE", "tree_path": "A1"}
result = client.process_universal(json.dumps(decision).encode(), verify=True)
print(f"Quality: {result.get('quality_score'):.2f}, Valid: {result.get('is_valid')}")
```

### Compare Two Paths

```python
from UFM_CLIENT import get_ufm_client

client = get_ufm_client()
path_a = "Description of path A".encode()
path_b = "Description of path B".encode()
result = client.compare(path_a, path_b)
print(f"Better path: {result.get('recommendation')}")
```

### Check Reversibility

```python
from UFM_CLIENT import get_ufm_client

client = get_ufm_client()
action = "Your action description".encode()
result = client.reconstruct(action)
print(f"Reversible: {result.get('lossless')}, Error: {result.get('round_trip_error'):.4f}")
```

---

**Remember**: Every decision → Tree → Gate → UFM → Log → Execute

No shortcuts. UFM validates all decisions before implementation.

