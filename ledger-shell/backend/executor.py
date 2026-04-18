from typing import Dict, Any, Tuple

class Executor:
    """Deterministic action executor: maps intent to action."""
    
    def __init__(self):
        self.action_map = {
            "render_object": self._render_object,
            "log_message": self._log_message,
            "move_object": self._move_object,
            "update_state": self._update_state,
            "clear_canvas": self._clear_canvas,
            "set_color": self._set_color,
        }
    
    def execute(self, intent: Dict[str, Any], current_state: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """
        Execute intent deterministically.
        
        Returns: (output, is_valid)
        """
        action = intent.get('action')
        
        if action not in self.action_map:
            return {"error": f"Unknown action: {action}"}, False
        
        try:
            output = self.action_map[action](intent, current_state)
            return output, True
        except Exception as e:
            return {"error": str(e)}, False
    
    def _render_object(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Render object to visual state."""
        obj = intent.get('params', {})
        obj_id = obj.get('id', 'object_unknown')
        
        if 'visual_state' not in state:
            state['visual_state'] = {}
        
        if 'objects' not in state['visual_state']:
            state['visual_state']['objects'] = []
        
        state['visual_state']['objects'].append({
            "id": obj_id,
            "type": obj.get('type', 'cube'),
            "position": obj.get('position', [0, 0, 0]),
            "color": obj.get('color', [1, 1, 1]),
            "scale": obj.get('scale', [1, 1, 1]),
        })
        
        return {
            "action": "render_object",
            "object_id": obj_id,
            "status": "rendered"
        }
    
    def _log_message(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Log message to system."""
        message = intent.get('params', {}).get('message', '')
        
        if 'messages' not in state:
            state['messages'] = []
        
        state['messages'].append({
            "message": message,
            "timestamp": intent.get('timestamp', 0)
        })
        
        return {
            "action": "log_message",
            "message": message,
            "status": "logged"
        }
    
    def _move_object(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Move object in visual state."""
        params = intent.get('params', {})
        obj_id = params.get('id')
        new_pos = params.get('position', [0, 0, 0])
        
        if 'visual_state' in state and 'objects' in state['visual_state']:
            for obj in state['visual_state']['objects']:
                if obj['id'] == obj_id:
                    obj['position'] = new_pos
                    return {
                        "action": "move_object",
                        "object_id": obj_id,
                        "new_position": new_pos,
                        "status": "moved"
                    }
        
        return {
            "action": "move_object",
            "object_id": obj_id,
            "status": "object_not_found"
        }
    
    def _update_state(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Update arbitrary state."""
        updates = intent.get('params', {})
        
        for key, value in updates.items():
            state[key] = value
        
        return {
            "action": "update_state",
            "keys_updated": list(updates.keys()),
            "status": "updated"
        }
    
    def _clear_canvas(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Clear all visual objects."""
        if 'visual_state' in state:
            state['visual_state'] = {}
        
        return {
            "action": "clear_canvas",
            "status": "cleared"
        }
    
    def _set_color(self, intent: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Set color of object."""
        params = intent.get('params', {})
        obj_id = params.get('id')
        color = params.get('color', [1, 1, 1])
        
        if 'visual_state' in state and 'objects' in state['visual_state']:
            for obj in state['visual_state']['objects']:
                if obj['id'] == obj_id:
                    obj['color'] = color
                    return {
                        "action": "set_color",
                        "object_id": obj_id,
                        "color": color,
                        "status": "updated"
                    }
        
        return {
            "action": "set_color",
            "object_id": obj_id,
            "status": "object_not_found"
        }
