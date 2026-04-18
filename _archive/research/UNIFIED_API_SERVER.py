#!/usr/bin/env python3
"""
UNIFIED API SERVER — Single API + hot-reload framework

CONSOLIDATION: Merges ENCYCLOPEDIA_API_SERVER + UNIVERSAL_RENDERER_API

ARCHITECTURE:
- Framework-driven routing (routes defined in framework.json, not hardcoded)
- Both Encyclopedia and Renderer endpoints available in single server
- Hot-reload support: update framework.json to add/remove endpoints without restart
- Field-conscious: all API operations recorded to unified ledger

USAGE:
1. Define routes in unified_framework.json (see example below)
2. Start server: python UNIFIED_API_SERVER.py
3. Server loads framework and starts watching for changes
4. Add/remove routes by editing unified_framework.json
5. Server adapts automatically (no restart needed)

This is the single unified API server for entire project.
All other API servers (ENCYCLOPEDIA_API_SERVER, UNIVERSAL_RENDERER_API) should
import from this or be deprecated.
"""

from flask import Flask, jsonify, send_from_directory, request, Response
from pathlib import Path
import json
import os
import sys
import base64
from datetime import datetime
import traceback

# Add to path
sys.path.insert(0, r"c:\Determined")

# Import framework hot-reload engine
from FRAMEWORK_HOT_RELOAD_ENGINE import FrameworkHotReloadEngine, FrameworkState

# Import handlers from unified location
try:
    from FIELD_IMAGE_GENERATOR_UNIFIED import DeterministicFieldBuilder as FieldBuilder
except ImportError:
    try:
        from FIELD_IMAGE_GENERATOR_V6 import DeterministicFieldBuilder as FieldBuilder
    except ImportError:
        FieldBuilder = None

try:
    from UNIVERSAL_RENDERER import render_with_song_layer
except ImportError:
    render_with_song_layer = None

try:
    from PATTERN_COMPLETION_BASELINE import BaselineKnowledgeGenerator
except ImportError:
    BaselineKnowledgeGenerator = None


# ============================================
# UNIFIED API SERVER
# ============================================

class UnifiedAPIServer:
    """
    Single unified API server with framework-driven routing.
    Combines Encyclopedia, Renderer, and Field endpoints.
    """
    
    def __init__(self, framework_path: str = "unified_framework.json",
                 ledger_path: str = "universe_ledger.jsonl",
                 port: int = 5000):
        self.framework_path = Path(framework_path)
        self.ledger_path = Path(ledger_path)
        self.port = port
        
        # Initialize Flask app
        self.app = Flask(__name__)
        
        # Initialize framework engine
        self.engine = FrameworkHotReloadEngine(
            framework_file_path=str(self.framework_path),
            ledger_path=str(self.ledger_path)
        )
        
        # Initialize helper modules
        self.field_builder = FieldBuilder() if FieldBuilder else None
        self.baseline_gen = BaselineKnowledgeGenerator() if BaselineKnowledgeGenerator else None
        
        # Image cache
        self.image_cache_dir = Path(r"c:\Determined\wiki_assets\entity_images")
        self.image_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Data directory
        self.data_dir = Path(r"c:\Determined\data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes - handlers will be called through framework engine"""
        
        # Health check (always available)
        @self.app.route('/health', methods=['GET'])
        def health():
            state = self.engine.get_current_state()
            consciousness = self.engine.get_field_consciousness_snapshot()
            
            return jsonify({
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "framework": {
                    "role": state.role.name if state else None,
                    "endpoints": len(state.role.endpoints) if state else 0
                },
                "field_consciousness": consciousness
            }), 200
        
        # Catch-all route handler
        @self.app.route('/api/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def api_handler(subpath):
            """
            Route request through framework engine.
            Framework defines which handler processes this endpoint.
            """
            try:
                state = self.engine.get_current_state()
                if not state:
                    return jsonify({"error": "Framework not initialized"}), 503
                
                # Find matching endpoint in framework
                method = request.method
                path = f"/api/{subpath}"
                
                # Check if any endpoint matches
                matched_endpoint = None
                for ep in state.role.endpoints:
                    if ep.path == path and ep.method == method:
                        matched_endpoint = ep
                        break
                
                if not matched_endpoint:
                    # Try without leading /api if not found
                    path = f"/{subpath}"
                    for ep in state.role.endpoints:
                        if ep.path == path and ep.method == method:
                            matched_endpoint = ep
                            break
                
                if not matched_endpoint:
                    return jsonify({
                        "error": f"No handler for {method} {path}",
                        "available_routes": self._list_available_routes()
                    }), 404
                
                # Get handler from engine
                handler = self.engine.get_handler(
                    matched_endpoint.handler_module,
                    matched_endpoint.handler_function
                )
                
                if not handler:
                    return jsonify({
                        "error": f"Handler not found: {matched_endpoint.handler_module}.{matched_endpoint.handler_function}"
                    }), 500
                
                # Call handler
                result = handler(request)
                return result
                
            except Exception as e:
                print(f"[API] Error: {e}")
                traceback.print_exc()
                return jsonify({"error": str(e), "type": type(e).__name__}), 500
        
        # Root route - serve main app
        @self.app.route('/', methods=['GET'])
        def root():
            try:
                encyclopedia_path = Path(r"c:\Determined\ENCYCLOPEDIA.html")
                if encyclopedia_path.exists():
                    return send_from_directory(encyclopedia_path.parent, encyclopedia_path.name)
                return jsonify({"message": "Unified API Server", "status": "online"}), 200
            except Exception as e:
                return jsonify({"message": "Unified API Server", "status": "online"}), 200
    
    def _list_available_routes(self) -> list:
        """List all available routes from framework"""
        state = self.engine.get_current_state()
        if not state:
            return []
        
        return [
            {
                "path": ep.path,
                "method": ep.method,
                "description": ep.description
            }
            for ep in state.role.endpoints
        ]
    
    def initialize(self) -> bool:
        """Initialize the API server"""
        print(f"[Server] Initializing Unified API Server")
        print(f"[Server] Framework: {self.framework_path}")
        print(f"[Server] Ledger: {self.ledger_path}")
        
        # Create default framework if doesn't exist
        if not self.framework_path.exists():
            print(f"[Server] Creating default framework: {self.framework_path}")
            self._create_default_framework()
        
        # Initialize engine
        if not self.engine.initialize():
            print(f"[Server] Failed to initialize framework engine")
            return False
        
        print(f"[Server] ✓ Framework engine initialized")
        print(f"[Server] ✓ Unified API Server ready")
        
        return True
    
    def _create_default_framework(self):
        """Create default framework.json if needed"""
        default_framework = {
            "role": {
                "name": "UNIFIED_API",
                "version": "1.0",
                "description": "Unified API server combining Encyclopedia and Renderer",
                "endpoints": [
                    {
                        "path": "/api/health",
                        "method": "GET",
                        "handler_module": "__main__",
                        "handler_function": "health_check",
                        "description": "Health check endpoint"
                    }
                ],
                "config": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "system": "UNIFIED_API_SERVER"
                }
            }
        }
        
        self.framework_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.framework_path, 'w') as f:
            json.dump(default_framework, f, indent=2)
    
    def start(self, watch_changes: bool = True, poll_interval: float = 2.0):
        """Start the API server"""
        print(f"[Server] Starting Unified API Server on port {self.port}")
        
        if not self.initialize():
            print(f"[Server] Initialization failed")
            return False
        
        # Start watching for framework changes
        if watch_changes:
            self.engine.start_watching(poll_interval=poll_interval)
            print(f"[Server] ✓ Framework watcher started (poll {poll_interval}s)")
        
        # Start Flask app
        try:
            self.app.run(host='127.0.0.1', port=self.port, debug=False)
        except KeyboardInterrupt:
            print(f"\n[Server] Shutdown requested")
            self.engine.stop_watching()
        
        return True


# ============================================
# DEFAULT HANDLERS
# ============================================

def health_check(request_obj):
    """Default health check handler"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }), 200


# ============================================
# ENTRY POINT
# ============================================

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════╗
║          UNIFIED API SERVER - Framework-Driven                ║
║                                                               ║
║ Single API server with hot-reload framework support          ║
║ Consolidates: ENCYCLOPEDIA_API_SERVER + UNIVERSAL_RENDERER   ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Create and start server
    server = UnifiedAPIServer(
        framework_path="unified_framework.json",
        ledger_path="universe_ledger.jsonl",
        port=5000
    )
    
    server.start(watch_changes=True, poll_interval=2.0)
