"""
Parameter Form Controls — ZEROPOINT UI for System Parameter Tuning

This module generates ZEROPOINT-compliant form controls for all tunable parameters.
Each parameter gets a control matching its type:
- Boolean → Checkbox button
- Integer → Number input with +/- buttons
- Float → Slider with text input
- Enum → Radio buttons or dropdown

Controls are rendered as nodes for the canvas app.
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime


class ParameterForm:
    """Generates form controls for system parameters."""

    def __init__(self, ledger_dir: str):
        self.ledger_dir = ledger_dir
        self.parameters = self._load_parameters()

    def _load_parameters(self) -> List[Dict[str, Any]]:
        """Load parameters from ledger."""
        parameters = []
        params_file = os.path.join(self.ledger_dir, "ledger_parameters.jsonl")

        try:
            with open(params_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            param = json.loads(line)
                            parameters.append(param)
                        except json.JSONDecodeError:
                            continue
        except Exception:
            pass

        return parameters

    def get_form_nodes(self) -> List[Dict[str, Any]]:
        """
        Generate form control nodes for all parameters.

        Returns: List of node dicts ready for canvas rendering
        """
        nodes = []
        y_offset = 10  # Start below header

        for param in self.parameters:
            name = param.get("name", "?")
            ptype = param.get("type", "string")
            
            # Handle both "value" and "default" fields from ledger
            value = param.get("value", param.get("default"))
            
            # Extract min/max from "range" array or individual fields
            param_range = param.get("range", [None, None])
            min_val = param.get("min", param_range[0] if isinstance(param_range, list) and len(param_range) > 0 else None)
            max_val = param.get("max", param_range[1] if isinstance(param_range, list) and len(param_range) > 1 else None)

            # Label for parameter
            nodes.append({
                "id": f"param-label:{name}",
                "type": "TEXT",
                "area": "main",
                "y_offset": y_offset,
                "payload": {
                    "text": f"{name}:",
                    "size": "normal",
                    "color": "text"
                }
            })
            y_offset += 30

            # Control based on type
            if ptype == "boolean":
                nodes.append(self._get_boolean_control(name, value, y_offset))
                y_offset += 40

            elif ptype == "integer":
                nodes.append(self._get_integer_control(name, value, min_val, max_val, y_offset))
                y_offset += 50

            elif ptype == "float":
                nodes.append(self._get_float_control(name, value, min_val, max_val, y_offset))
                y_offset += 50

            elif ptype == "enum":
                options = param.get("options", [])
                nodes.extend(self._get_enum_controls(name, value, options, y_offset))
                y_offset += 40 + (len(options) * 25)

            nodes.append({
                "id": f"spacer:{name}",
                "type": "TEXT",
                "area": "main",
                "y_offset": y_offset,
                "payload": {
                    "text": "",
                    "size": "normal",
                    "color": "text"
                }
            })
            y_offset += 20

        return nodes

    def _get_boolean_control(self, name: str, current_value: bool, y_offset: int) -> Dict[str, Any]:
        """Generate checkbox/toggle button for boolean parameter."""
        # Handle None values (default to False)
        if current_value is None:
            current_value = False

        state = "ON" if current_value else "OFF"
        bg_color = "success_bg" if current_value else "neutral_bg"

        return {
            "id": f"param-control:{name}",
            "type": "BUTTON",
            "area": "main",
            "y_offset": y_offset,
            "payload": {
                "label": f"[{state}] Toggle",
                "bg": bg_color,
                "text": "button_text",
                "param_name": name,
                "param_type": "boolean",
                "current_value": current_value
            }
        }

    def _get_integer_control(self, name: str, current_value: int, min_val: int, max_val: int,
                             y_offset: int) -> Dict[str, Any]:
        """Generate +/- buttons and text display for integer parameter."""
        # Handle None values
        if current_value is None:
            current_value = min_val if min_val else 0
        if min_val is None:
            min_val = 0
        if max_val is None:
            max_val = 100

        return {
            "id": f"param-control:{name}",
            "type": "TEXT",
            "area": "main",
            "y_offset": y_offset,
            "payload": {
                "text": f"Value: {current_value}   [Min: {min_val}  Max: {max_val}]",
                "size": "normal",
                "color": "text",
                "param_name": name,
                "param_type": "integer",
                "current_value": current_value,
                "min": min_val,
                "max": max_val
            }
        }

    def _get_float_control(self, name: str, current_value: float, min_val: float, max_val: float,
                           y_offset: int) -> Dict[str, Any]:
        """Generate slider-like control for float parameter."""
        # Handle None values
        if current_value is None:
            current_value = min_val if min_val else 0.5
        if min_val is None:
            min_val = 0.0
        if max_val is None:
            max_val = 1.0

        return {
            "id": f"param-control:{name}",
            "type": "TEXT",
            "area": "main",
            "y_offset": y_offset,
            "payload": {
                "text": f"Value: {current_value:.2f}   [Range: {min_val} - {max_val}]",
                "size": "normal",
                "color": "text",
                "param_name": name,
                "param_type": "float",
                "current_value": current_value,
                "min": min_val,
                "max": max_val
            }
        }

    def _get_enum_controls(self, name: str, current_value: str, options: List[str],
                           y_offset: int) -> List[Dict[str, Any]]:
        """Generate radio buttons for enum parameter."""
        controls = []

        for option in options:
            is_selected = option == current_value
            bg = "success_bg" if is_selected else "neutral_bg"

            controls.append({
                "id": f"param-option:{name}:{option}",
                "type": "BUTTON",
                "area": "main",
                "y_offset": y_offset,
                "payload": {
                    "label": f"{'[X]' if is_selected else '[ ]'} {option}",
                    "bg": bg,
                    "text": "button_text",
                    "param_name": name,
                    "param_type": "enum",
                    "param_value": option
                }
            })
            y_offset += 25

        return controls

    def handle_parameter_change(self, param_name: str, new_value: Any) -> bool:
        """
        Handle parameter change from form control.

        Writes updated parameter value back to ledger.

        Args:
            param_name: Name of parameter to change
            new_value: New value (will be type-converted)

        Returns: True if successful, False otherwise
        """
        # Find parameter spec
        param_spec = None
        for param in self.parameters:
            if param.get("name") == param_name:
                param_spec = param
                break

        if not param_spec:
            return False

        # Type-convert value
        ptype = param_spec.get("type", "string")
        try:
            if ptype == "boolean":
                converted = isinstance(new_value, bool) and new_value or new_value in [True, "true", 1, "1"]
            elif ptype == "integer":
                converted = int(new_value)
            elif ptype == "float":
                converted = float(new_value)
            else:
                converted = str(new_value)
        except (ValueError, TypeError):
            return False

        # Validate against constraints
        if ptype in ["integer", "float"]:
            min_val = param_spec.get("min")
            max_val = param_spec.get("max")
            if min_val is not None and converted < min_val:
                converted = min_val
            if max_val is not None and converted > max_val:
                converted = max_val

        # Update parameter in ledger
        params_file = os.path.join(self.ledger_dir, "ledger_parameters.jsonl")

        try:
            # Read all parameters
            params = {}
            if os.path.exists(params_file):
                with open(params_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            param = json.loads(line)
                            params[param.get("name")] = param

            # Update the changed parameter
            if param_name in params:
                params[param_name]["value"] = converted
                params[param_name]["last_changed"] = datetime.utcnow().isoformat() + "Z"

            # Write back
            with open(params_file, 'w', encoding='utf-8') as f:
                for param in params.values():
                    f.write(json.dumps(param) + "\n")

            # Update in-memory cache
            for param in self.parameters:
                if param.get("name") == param_name:
                    param["value"] = converted
                    break

            return True

        except Exception as e:
            print(f"[ParameterForm] Error updating parameter: {e}")
            return False


# Public interface for canvas app
def get_parameter_form_nodes(ledger_dir: str) -> List[Dict[str, Any]]:
    """
    Get all form control nodes for the Utilities dashboard.

    Called by Utilities dashboard renderer to generate interactive controls.

    Args:
        ledger_dir: Path to ledger directory

    Returns: List of node specifications for canvas rendering
    """
    form = ParameterForm(ledger_dir)
    return form.get_form_nodes()
