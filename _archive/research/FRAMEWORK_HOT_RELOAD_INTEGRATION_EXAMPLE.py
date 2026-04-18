"""
FRAMEWORK HOT-RELOAD INTEGRATION EXAMPLE
=========================================
How to integrate the hot-reload engine into a Flask server.

STEP 1: Initialize the engine with your framework definition
STEP 2: Start watching for changes
STEP 3: Use engine.route_request() in your route handlers
STEP 4: Update framework.json → server adapts instantly

NO RESTART NEEDED.
"""

from flask import Flask, jsonify, request
from pathlib import Path
import os

# Import the hot-reload engine
from FRAMEWORK_HOT_RELOAD_ENGINE import (
    FrameworkHotReloadEngine,
    verify_engine_initialization
)


# ============================================
# CONFIGURATION
# ============================================

FRAMEWORK_FILE = Path(r"c:\Determined\example_framework.json")
WATCH_INTERVAL = 2.0  # Check every 2 seconds

# Create Flask app
app = Flask(__name__)

# Initialize hot-reload engine (global)
engine = None


# ============================================
# INITIALIZATION
# ============================================

def initialize_framework_engine():
    """Initialize the framework engine on app startup"""
    global engine
    
    engine = FrameworkHotReloadEngine(
        framework_file_path=str(FRAMEWORK_FILE),
        sys_path=[r"c:\Determined"]
    )
    
    # Load initial framework
    if not engine.initialize():
        print("[ERROR] Failed to initialize framework engine")
        return False
    
    # Verify it loaded correctly
    if not verify_engine_initialization(engine):
        print("[ERROR] Framework verification failed")
        return False
    
    # Start background watching for changes
    engine.start_watching(poll_interval=WATCH_INTERVAL)
    
    print("[SUCCESS] Framework engine initialized and watching")
    return True


# ============================================
# FLASK ROUTES — FRAMEWORK-DRIVEN
# ============================================

@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check - returns status of framework engine.
    Framework can be updated to change what this returns.
    """
    if not engine:
        return jsonify({"error": "Engine not initialized"}), 500
    
    status = engine.get_status_report()
    return jsonify(status), 200


@app.route('/api/framework/status', methods=['GET'])
def framework_status():
    """
    Get detailed framework status.
    Shows current role, endpoints, handlers, and any errors.
    """
    if not engine:
        return jsonify({"error": "Engine not initialized"}), 500
    
    state = engine.get_current_state()
    
    if not state:
        return jsonify({"error": "No state loaded"}), 500
    
    return jsonify({
        "role": state.role.name,
        "version": state.role.version,
        "description": state.role.description,
        "endpoints": [
            {
                "path": ep.path,
                "method": ep.method,
                "handler": f"{ep.handler_module}.{ep.handler_function}",
                "description": ep.description,
                "experimental": ep.experimental,
                "deprecated": ep.deprecated
            }
            for ep in state.role.endpoints
        ],
        "handlers_loaded": len(state.loaded_handlers),
        "last_update": state.last_update,
        "change_type": state.change_type.value if state.change_type else None,
        "is_clean": state.is_clean(),
        "errors": state.errors
    }), 200


@app.route('/api/framework/reload', methods=['POST'])
def manual_reload():
    """
    Manually trigger framework reload.
    (In production, framework reloads automatically via file watcher)
    """
    if not engine:
        return jsonify({"error": "Engine not initialized"}), 500
    
    success = engine.reload_framework()
    
    if success:
        status = engine.get_status_report()
        return jsonify({
            "status": "reloaded",
            "framework": status
        }), 200
    else:
        state = engine.get_current_state()
        return jsonify({
            "status": "reload_failed",
            "errors": state.errors if state else []
        }), 400


@app.route('/api/execute/<handler_module>/<handler_function>', methods=['POST'])
def execute_handler(handler_module, handler_function):
    """
    Generic request router - route through current framework.
    Request body can contain any data the handler needs.
    """
    if not engine:
        return jsonify({"error": "Engine not initialized"}), 500
    
    try:
        # Get request body (optional)
        data = request.get_json() if request.is_json else {}
        
        # Route through framework engine
        response, status_code = engine.route_request(
            handler_module,
            handler_function,
            data=data
        )
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# STARTUP & SHUTDOWN
# ============================================

@app.before_request
def before_request():
    """Check engine is initialized for each request"""
    if not engine:
        return jsonify({"error": "Engine not initialized"}), 500


@app.teardown_appcontext
def shutdown_framework_engine(exception=None):
    """Clean up on shutdown"""
    global engine
    
    if engine:
        engine.stop_watching()
        print("[SHUTDOWN] Framework engine stopped")


# ============================================
# EXAMPLE HANDLER FUNCTIONS
# ============================================

def example_query_handler(data: dict) -> dict:
    """
    Example handler function.
    These are called via framework engine.
    Framework definition maps endpoints to these handlers.
    """
    query = data.get("query", "")
    
    return {
        "handler": "example_query_handler",
        "query": query,
        "result": f"Processed: {query}",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


def example_compute_handler(data: dict) -> dict:
    """Another example handler"""
    value = data.get("value", 0)
    
    return {
        "handler": "example_compute_handler",
        "input": value,
        "output": value * 2,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


def example_status_handler(data: dict) -> dict:
    """Status handler"""
    return {
        "handler": "example_status_handler",
        "status": "operational",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("FRAMEWORK HOT-RELOAD FLASK SERVER")
    print("="*60)
    
    # Initialize framework engine
    if not initialize_framework_engine():
        print("[FATAL] Could not initialize framework engine")
        exit(1)
    
    print("\n[READY] Server starting up...")
    print(f"Framework file: {FRAMEWORK_FILE}")
    print(f"Watch interval: {WATCH_INTERVAL}s")
    print("\nTo update framework:")
    print(f"1. Edit {FRAMEWORK_FILE}")
    print("2. Server automatically reloads (no restart needed)")
    print("\nHealthcheck: http://localhost:5000/api/health")
    print("Status: http://localhost:5000/api/framework/status")
    print("="*60 + "\n")
    
    # Run Flask
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
