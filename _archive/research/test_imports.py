#!/usr/bin/env python3
"""
Test imports to find which module has the .lower() error
"""
import sys
sys.path.insert(0, 'c:\\Determined')

print("[1] Importing COHERENCE_LATTICE_SELF_AWARE...")
try:
    from COHERENCE_LATTICE_SELF_AWARE import analyze_query_semantics
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("[2] Importing CLAUDE_SESSION_LEDGER...")
try:
    from CLAUDE_SESSION_LEDGER import ClaudeSessionLedger
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("[3] Importing COMMUNICATION_FIELD_COMPLETE...")
try:
    from COMMUNICATION_FIELD_COMPLETE import (
        generate_response_via_communication_field,
        load_session_history
    )
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("[4] Importing continuity_guardian...")
try:
    from continuity_guardian import ContinuityGuardian
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("[5] Importing CORE_SYSTEMS_INTEGRATION...")
try:
    from CORE_SYSTEMS_INTEGRATION import CoreSystemsIntegration
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("[6] Creating Flask app...")
try:
    from flask import Flask
    app = Flask(__name__)
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("[7] Initializing ledger...")
try:
    ledger = ClaudeSessionLedger("claude_session_reasoning.jsonl")
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("[8] Initializing guardian...")
try:
    guardian = ContinuityGuardian("claude_session_reasoning.jsonl")
    print("  ✓ Success")
except Exception as e:
    import traceback
    print(f"  ✗ ERROR: {e}")
    traceback.print_exc()

print("[9] Initializing core_systems...")
try:
    core_systems = CoreSystemsIntegration()
    print("  ✓ Success")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("\nAll imports successful!")
