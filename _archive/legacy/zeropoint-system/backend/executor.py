"""
EXECUTOR - Deterministic action mapper

Single responsibility: Map intent → action, execute deterministically.
No decisions. Only direct mapping.

Every intent must map to exactly one action.
If intent is invalid → record failure, do not execute.
"""

from typing import Dict, Any, Tuple


class Executor:
    """Maps intents to deterministic actions."""
    
    def __init__(self):
        """Initialize executor with action map."""
        self.actions = {
            "render_object": self._render_object,
            "log_message": self._log_message,
            "move_object": self._move_object,
            "update_state": self._update_state,
            "noop": self._noop,
        }
    
    def execute(self, intent: Dict[str, Any], current_state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
        """
        Execute an intent.
        
        Returns:
        - valid: was the action valid?
        - output: what was produced
        - action_taken: which action was executed
        """
        
        # Get action name from intent
        action_name = intent.get("action")
        
        # Validate action exists
        if action_name not in self.actions:
            return False, {"error": f"Unknown action: {action_name}"}, "UNKNOWN"
        
        # Execute deterministically
        try:
            output = self.actions[action_name](intent, current_state)
            return True, output, action_name
        except Exception as e:
            return False, {"error": str(e)}, action_name
    
    def _render_object(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Render a visual object."""
        obj_id = intent.get("object_id")
        obj_type = intent.get("type", "cube")
        position = intent.get("position", [0, 0, 0])
        color = intent.get("color", [1, 1, 1])
        
        return {
            "object_id": obj_id,
            "type": obj_type,
            "position": position,
            "color": color,
            "rendered": True
        }
    
    def _log_message(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Log a message."""
        message = intent.get("message", "")
        level = intent.get("level", "INFO")
        
        return {
            "message": message,
            "level": level,
            "logged": True
        }
    
    def _move_object(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Move an object to a new position."""
        obj_id = intent.get("object_id")
        new_position = intent.get("position", [0, 0, 0])
        
        return {
            "object_id": obj_id,
            "new_position": new_position,
            "moved": True
        }
    
    def _update_state(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Update the application state."""
        key = intent.get("key")
        value = intent.get("value")
        
        new_state = state.copy()
        if key:
            new_state[key] = value
        
        return {
            "key": key,
            "value": value,
            "state_updated": True
        }
    
    def _noop(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """No operation - used for testing."""
        return {"action": "noop", "executed": True}
