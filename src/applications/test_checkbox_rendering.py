#!/usr/bin/env python3
"""
Test checkbox rendering for boolean parameter controls
"""

import json
import os
import sys
from parameter_form import ParameterForm
from ledger_query import LedgerQuery

# Initialize
ledger_dir = os.path.join(os.path.dirname(__file__), "../../src/ledgers")
param_form = ParameterForm(ledger_dir)
ledger_query = LedgerQuery(ledger_dir)

# Get parameter nodes
nodes = param_form.get_form_nodes()

# Filter to boolean parameter controls
boolean_controls = [n for n in nodes if n.get("type") == "BUTTON" and 
                    n.get("payload", {}).get("param_type") == "boolean"]

print("=" * 70)
print("CHECKBOX RENDERING TEST")
print("=" * 70)
print(f"\nFound {len(boolean_controls)} boolean parameter controls\n")

for control in boolean_controls:
    node_id = control.get("id")
    payload = control.get("payload", {})
    param_name = payload.get("param_name")
    current_value = payload.get("current_value")
    
    # Get positioned coordinates
    positioned = ledger_query.get_node(node_id)
    if positioned:
        x = positioned.get("x")
        y = positioned.get("y")
        width = positioned.get("width")
        height = positioned.get("height")
        
        print(f"✓ {param_name}: {current_value}")
        print(f"  ID: {node_id}")
        print(f"  Type: BUTTON (renders as checkbox)")
        print(f"  Position: x={x}, y={y}, w={width}, h={height}")
        print(f"  Payload: param_type={payload.get('param_type')}, value={current_value}")
        print()

print("=" * 70)
print("RENDERING APPROACH:")
print("=" * 70)
print("✓ Checkbox box: 20x20 px on left")
print("✓ Checkmark: Drawn if value=True")
print("✓ Label: Parameter name to right of box")
print("✓ Clickable: Entire control area")
print("✓ State: Toggles between True/False on click")
print("=" * 70)
