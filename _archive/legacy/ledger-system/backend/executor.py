"""
EXECUTOR
Deterministic intent → action mapping.
No randomness. No decision making beyond direct mapping.
"""

from typing import Dict, Any


class Executor:
    """Execute intent deterministically"""
    
    @staticmethod
    def execute(intent: Dict[str, Any], current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute intent. Pure mapping.
        
        Returns: {
            "action": str,
            "output": dict,
            "state_after": dict,
            "valid": bool,
            "error": str or None
        }
        """
        
        action_type = intent.get("type")
        
        # Route to handler
        if action_type == "render_object":
            return Executor._handle_render_object(intent, current_state)
        
        elif action_type == "log_message":
            return Executor._handle_log_message(intent, current_state)
        
        elif action_type == "move_object":
            return Executor._handle_move_object(intent, current_state)
        
        elif action_type == "set_state":
            return Executor._handle_set_state(intent, current_state)
        
        elif action_type == "query_state":
            return Executor._handle_query_state(intent, current_state)
        
        else:
            return {
                "action": "unknown",
                "output": {},
                "state_after": current_state,
                "valid": False,
                "error": f"Unknown action type: {action_type}"
            }
    
    @staticmethod
    def _handle_render_object(intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Render object to visual_state"""
        obj_id = intent.get("object_id")
        obj_data = intent.get("data", {})
        
        if not obj_id:
            return {
                "action": "render_object",
                "output": {"error": "object_id required"},
                "state_after": state,
                "valid": False,
                "error": "object_id required"
            }
        
        # Update state
        new_state = dict(state)
        if "objects" not in new_state:
            new_state["objects"] = {}
        
        new_state["objects"][obj_id] = obj_data
        
        return {
            "action": "render_object",
            "output": {"object_id": obj_id, "data": obj_data},
            "state_after": new_state,
            "valid": True,
            "error": None
        }
    
    @staticmethod
    def _handle_log_message(intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Log message"""
        message = intent.get("message", "")
        
        # Update state
        new_state = dict(state)
        if "logs" not in new_state:
            new_state["logs"] = []
        
        new_state["logs"].append(message)
        
        # Keep last 100 logs
        if len(new_state["logs"]) > 100:
            new_state["logs"] = new_state["logs"][-100:]
        
        return {
            "action": "log_message",
            "output": {"message": message},
            "state_after": new_state,
            "valid": True,
            "error": None
        }
    
    @staticmethod
    def _handle_move_object(intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Move object in 3D space"""
        obj_id = intent.get("object_id")
        x = intent.get("x")
        y = intent.get("y")
        z = intent.get("z")
        
        if not obj_id:
            return {
                "action": "move_object",
                "output": {"error": "object_id required"},
                "state_after": state,
                "valid": False,
                "error": "object_id required"
            }
        
        # Update state
        new_state = dict(state)
        if "objects" not in new_state:
            new_state["objects"] = {}
        
        if obj_id not in new_state["objects"]:
            new_state["objects"][obj_id] = {}
        
        if x is not None:
            new_state["objects"][obj_id]["x"] = x
        if y is not None:
            new_state["objects"][obj_id]["y"] = y
        if z is not None:
            new_state["objects"][obj_id]["z"] = z
        
        return {
            "action": "move_object",
            "output": {"object_id": obj_id, "x": x, "y": y, "z": z},
            "state_after": new_state,
            "valid": True,
            "error": None
        }
    
    @staticmethod
    def _handle_set_state(intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Set arbitrary state key"""
        key = intent.get("key")
        value = intent.get("value")
        
        if not key:
            return {
                "action": "set_state",
                "output": {"error": "key required"},
                "state_after": state,
                "valid": False,
                "error": "key required"
            }
        
        # Update state
        new_state = dict(state)
        new_state[key] = value
        
        return {
            "action": "set_state",
            "output": {"key": key, "value": value},
            "state_after": new_state,
            "valid": True,
            "error": None
        }
    
    @staticmethod
    def _handle_query_state(intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Query state (read-only)"""
        key = intent.get("key")
        
        if key:
            value = state.get(key)
        else:
            value = state
        
        return {
            "action": "query_state",
            "output": {"key": key, "value": value},
            "state_after": state,
            "valid": True,
            "error": None
        }
