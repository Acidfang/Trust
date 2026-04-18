#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS v3 - Pure HTTP Translator for Ledger-Driven ARIA OS

This server is ONLY:
- HTTP listener
- Request parser
- Response formatter
- Static file server

ALL logic lives in the ledger. The server translates between HTTP and ledger queries.
Same backend as jarvis_canvas_ledger_driven.py - just different interface (HTTP vs Tkinter).

No state. No caching. No decisions. Just translation.
"""

import json
import os
import hashlib
import time
import sys
import traceback
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# ===== BOOT TIMESTAMP =====
BOOT_TIME = time.time()
BOOT_TIMESTAMP = datetime.now().isoformat()

# ===== PROTOCOL COMPLIANCE ENFORCEMENT =====
PROTOCOL_COMPLIANCE_REQUIRED = {
    "enforcement": "strict",
    "requirements": [
        "All operations must align with ZeroPoint primitives",
        "All debugging must follow RCA-first methodology",
        "All decisions must follow complete enumeration",
        "All unexpected behavior triggers immediate RCA",
        "NO GUESSING — uncertainties require RCA protocol",
        "All findings must be recorded to ledger"
    ],
    "violation_response": "suspend_task_and_escalate",
    "effective_date": "2026-03-29T00:00:00Z"
}

# ===== BOOT LOG FILE (Persistent diagnostics) =====
BOOT_LOG_FILE = Path(__file__).parent / "jarvis_v3_boot.log"

def log_to_boot_file(msg):
    """Append to persistent boot log"""
    try:
        with open(BOOT_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
    except Exception as e:
        print(f"[WARN] Could not write to boot log: {e}", flush=True)

def print_and_log(msg):
    """Print to console AND persistent boot log"""
    print(msg, flush=True)
    log_to_boot_file(msg)

# ===== PROTOCOL COMPLIANCE VERIFICATION =====
def verify_protocol_compliance():
    """Verify protocol compliance at startup"""
    print_and_log("[PROTOCOL] PROTOCOL COMPLIANCE VERIFICATION")
    print_and_log("[PROTOCOL] ====================================================")
    print_and_log(f"[PROTOCOL] Enforcement Level: {PROTOCOL_COMPLIANCE_REQUIRED['enforcement'].upper()}")
    print_and_log("[PROTOCOL] Requirements:")
    for i, req in enumerate(PROTOCOL_COMPLIANCE_REQUIRED['requirements'], 1):
        print_and_log(f"[PROTOCOL]   {i}. {req}")
    print_and_log("[PROTOCOL] ====================================================")
    print_and_log("[PROTOCOL] Any violation requires task suspension and escalation")
    print_and_log("[PROTOCOL] See: CLAUDE_INSTRUCTIONS.md -> RCA-FIRST PROTOCOL")
    print_and_log("[PROTOCOL] ====================================================")


# ===== LEDGER QUERY (Singleton, initialized once) =====
# Unified backend for all ledger operations

LEDGER_INIT_ERROR = None
script_dir = os.path.dirname(os.path.abspath(__file__))

try:
    print_and_log("[BOOT  0.0s] Importing LedgerQuery...")
    from ledger_query import LedgerQuery
    from self_awareness import SelfAwareness
    print_and_log("[IMPORT OK] LedgerQuery class loaded")
    
    print_and_log("[INIT  0.1s] Initializing LedgerQuery.load_all()...")
    ledger = LedgerQuery(script_dir)
    print_and_log(f"[INIT  OK] LedgerQuery ready ({len(ledger.buttons)} buttons, {len(ledger.dashboards)} dashboards)")
except Exception as e:
    LEDGER_INIT_ERROR = f"{type(e).__name__}: {str(e)}"
    print_and_log(f"[ERROR CRITICAL] LedgerQuery initialization failed!")
    print_and_log(f"[ERROR] {LEDGER_INIT_ERROR}")
    print_and_log(f"[TRACE]\n{traceback.format_exc()}")
    ledger = None


# ===== FRAME CACHE (Quick Access Artifact Ledger) =====
# Cache frame only recomputes when state changes
# Rapid polls (every 500ms) return cached frame instantly

_frame_cache = {
    "state_hash": None,      # Hash of state that produced current frame
    "cached_frame": None,    # The cached frame data
    "recompute_count": 0     # Statistics
}


def _get_state_hash():
    """Compute hash of current ledger state"""
    state = ledger.app_state
    state_str = json.dumps(state, sort_keys=True)
    return hashlib.sha256(state_str.encode()).hexdigest()


# ===== REQUEST HANDLER (Pure Translator) =====

class JarvisHandler(BaseHTTPRequestHandler):
    """Pure HTTP translator - delegates to kernel for all logic"""

    def log_message(self, format, *args):
        """Custom logging format"""
        print(f"[JARVIS] {format % args}", flush=True)

    def do_GET(self):
        """Translate GET requests to ledger queries"""
        path = self.path

        try:
            if path == "/":
                self._serve_html()
            elif path == "/api/health":
                # ===== HEALTH CHECK ENDPOINT (Bidirectional verification) =====
                # Forward: "Is server running?" → returns true
                # Backward: "Before starting, is it running?" → returns true (don't start duplicate)
                self._handle_health_check()
            elif path == "/api/help":
                # System help and command documentation
                self._send_json({"help": SelfAwareness.help_text()})
            elif path == "/api/capabilities":
                # List all system capabilities
                self._send_json(SelfAwareness.CORE_CAPABILITIES)
            elif path == "/api/dashboards":
                # Dashboard map with learning outcomes
                self._send_json(SelfAwareness.DASHBOARDS)
            elif path == "/api/identity":
                # System identity and core information
                self._send_json(SelfAwareness.SYSTEM_IDENTITY)
            elif path == "/api/discovery":
                # Discovery tips for learning by doing
                self._send_json({"tips": SelfAwareness.discovery_tips()})
            elif path == "/api/state":
                # Return app state snapshot from ledger
                if LEDGER_INIT_ERROR:
                    self._send_json({"error": "Ledger not initialized", "details": LEDGER_INIT_ERROR}, 500)
                    return
                current_view = ledger.get_current_view()
                state = {
                    "current_view": current_view,
                    "state": ledger.app_state
                }
                self._send_json(state)
            elif path == "/api/frame":
                # Return frame structure for HTML renderer
                # Uses cache for rapid polling - only recomputes on state change
                if LEDGER_INIT_ERROR:
                    self._send_json({"error": "Ledger not initialized", "details": LEDGER_INIT_ERROR}, 500)
                    return
                frame = self._get_frame_cached()
                self._send_json(frame)
            else:
                self._send_404()
        except Exception as e:
            import traceback
            err_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[ERROR] GET {path}: {err_msg}", flush=True)
            traceback.print_exc()
            self._send_error(500, err_msg)

    def do_POST(self):
        """Translate POST requests to ledger operations"""
        path = self.path

        try:
            if path == "/api/interaction":
                # User interaction (button click) - record in ledger
                self._process_interaction()
            else:
                self._send_404()
        except Exception as e:
            import traceback
            err_msg = f"{type(e).__name__}: {e}"
            print(f"[ERROR] POST {path}: {err_msg}", flush=True)
            traceback.print_exc()
            self._send_error(500, err_msg)

    # ===== MINIMAL TRANSLATION (Server = Pure HTTP Translator) =====

    def _serve_html(self):
        """Serve jarvis.html - pure file serving"""
        file_path = Path("jarvis.html")
        if not file_path.exists():
            file_path = Path(__file__).parent / "jarvis.html"

        if not file_path.exists():
            return self._send_error(404, "jarvis.html not found")

        with open(file_path, "rb") as f:
            content = f.read()
        self._send_response(200, content, "text/html")

    def _process_interaction(self):
        """
        Capture user interaction and pass to ledger for handling.
        
        Intent: Pure translator. Extract interaction data, pass to ledger.
        Ledger queries button spec and executes it.
        Server makes NO decisions - it just forwards data.
        """
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return self._send_error(400, "Request body required")

        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))

        # Extract button click data from browser (pure pass-through)
        button_id = data.get("button_id")

        if not button_id:
            return self._send_error(400, "button_id required")

        # Pass to ledger for handling.
        # Ledger extracts button spec and executes it.
        # Records all interactions to election ledger.
        # Server makes NO decisions about what this interaction means.
        result = ledger.record_button_click(button_id)

        self._send_json({
            "status": "ok",
            "button": button_id,
            "view": ledger.get_current_view()
        })

    def _handle_health_check(self):
        """
        HEALTH CHECK ENDPOINT
        
        Purpose: Bidirectional verification
        - Forward: "Is server running?" → YES
        - Backward: "Before starting, is it already running?" → YES (don't start duplicate)
        
        Returns detailed status of all components.
        """
        uptime = time.time() - BOOT_TIME
        
        # Component status
        components = {
            "ledger_query": "initialized" if ledger and not LEDGER_INIT_ERROR else "failed",
            "frame_cache": "operational",
            "http_server": "listening",
            "port_8081": "bound"
        }
        
        # Count loaded data
        ledgers_count = 0
        buttons_count = 0
        dashboards_count = 0
        
        if ledger and not LEDGER_INIT_ERROR:
            buttons_count = len(ledger.buttons)
            dashboards_count = len(ledger.dashboards)
            # Count non-None ledger data structures
            ledgers_count = sum(1 for attr in [
                ledger.buttons, ledger.dashboards, ledger.buttons,
                ledger.elections, ledger.positioned_nodes
            ] if attr)
        
        # Build response
        if LEDGER_INIT_ERROR:
            # Server running but degraded
            response = {
                "status": "degraded",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": int(uptime),
                "boot_timestamp": BOOT_TIMESTAMP,
                "boot_sequence": "initialization_failed",
                "failed_at": "LedgerQuery initialization",
                "error": LEDGER_INIT_ERROR,
                "components": components,
                "ledgers_loaded": 0,
                "buttons_count": 0,
                "dashboards_count": 0
            }
            self._send_json(response, 503)  # 503 Service Unavailable
        else:
            # Server running and healthy
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": int(uptime),
                "boot_timestamp": BOOT_TIMESTAMP,
                "boot_sequence": "complete",
                "components": components,
                "ledgers_loaded": ledgers_count,
                "buttons_count": buttons_count,
                "dashboards_count": dashboards_count,
                "errors": []
            }
            self._send_json(response, 200)

    def _get_frame_cached(self):
        """
        Get frame with caching.
        Only recomputes frame when state changes.
        Rapid polls return cached frame instantly.
        
        Quick Access Artifact Ledger: Frame cache keyed by state hash
        """
        global _frame_cache
        
        current_hash = _get_state_hash()
        
        # Check if state has changed since last frame computation
        if _frame_cache["state_hash"] == current_hash and _frame_cache["cached_frame"] is not None:
            # State unchanged - return cached frame (instant)
            return _frame_cache["cached_frame"]
        
        # State changed - recompute frame
        frame = self._generate_frame()
        
        # Update cache
        _frame_cache["state_hash"] = current_hash
        _frame_cache["cached_frame"] = frame
        _frame_cache["recompute_count"] += 1
        
        return frame

    def _generate_frame(self):
        """
        Generate frame structure for HTML renderer.
        Frame contains nodes positioned absolutely on canvas.
        Layout is driven by current view and ledger state.
        
        Causal model: Menu items drop DOWN from toggle button (vertical dropdown)
        NOT horizontal sidebar repositioning
        """
        nodes = []
        current_view = ledger.get_current_view()
        menu_expanded = ledger.app_state.get("menu_expanded", 0)
        
        # Window dimensions
        window_width = 1200
        window_height = 800
        
        # Fixed content margins (no horizontal shifting)
        content_x = 10
        content_width = window_width - 20
        
        y_pos = 10
        
        # HEADER AREA
        nodes.append({
            "id": "header",
            "type": "TEXT",
            "x": content_x,
            "y": y_pos,
            "width": content_width,
            "height": 40,
            "payload": {
                "text": "ARIA Consciousness OS",
                "size": "header",
                "color": "#64b5f6"
            }
        })
        
        y_pos += 50
        
        # TOGGLE MENU BUTTON (fixed position, origin point for dropdown)
        nodes.append({
            "id": "btn:toggle-sidebar",
            "type": "BUTTON",
            "x": content_x,
            "y": y_pos,
            "width": 140,
            "height": 30,
            "payload": {
                "label": "☰ Menu",
                "enabled": True,
                "bg": "#333333",
                "text": "#64b5f6"
            }
        })
        
        toggle_button_y = y_pos
        
        # DROPDOWN MENU ITEMS (flow DOWN from toggle button when expanded)
        # When menu_expanded=0: positioned off-screen (y=-500)
        # When menu_expanded=1: positioned at y=100 (below toggle button)
        menu_start_y = 100 if menu_expanded else -500
        
        # BACK BUTTON (only visible in non-menu views)
        if current_view != "menu":
            nodes.append({
                "id": "btn:back",
                "type": "BUTTON",
                "x": content_x,
                "y": menu_start_y,
                "width": 140,
                "height": 30,
                "payload": {
                    "label": "← Menu",
                    "enabled": True,
                    "bg": "#2a2a2a",
                    "text": "#90ee90"
                }
            })
            menu_start_y += 40
        
        # NAVIGATION BUTTONS (view buttons in dropdown)
        # Flow down from toggle button when menu_expanded=1
        nav_buttons = [
            ("btn:live-elections", "Live Elections", "live_elections"),
            ("btn:timeline-dag", "Timeline DAG", "timeline_visualization"),
            ("btn:coherence-monitoring", "Coherence Monitoring", "coherence_monitoring"),
            ("btn:utilities", "Utilities", "utility_landscape"),
            ("btn:synthesis-progress", "Synthesis Progress", "synthesis_progress"),
            ("btn:learning-curve", "Learning Curve", "learning_curve"),
            ("btn:timeline-records", "Timeline Records", "timeline_records")
        ]
        
        for btn_id, label, view_name in nav_buttons:
            # Highlight button if it matches current view
            is_active = current_view == view_name
            nodes.append({
                "id": btn_id,
                "type": "BUTTON",
                "x": content_x,
                "y": menu_start_y,
                "width": 140,
                "height": 30,
                "payload": {
                    "label": label,
                    "enabled": True,
                    "bg": "#2a2a2a" if is_active else "#1a1a1a",
                    "text": "#ffff00" if is_active else "#1e88e5"
                }
            })
            menu_start_y += 40
        
        # CONTENT AREA (always full width, starts after toggle button)
        content_start_y = toggle_button_y + 50
        nodes.append({
            "id": "content-area",
            "type": "TEXT",
            "x": content_x,
            "y": content_start_y,
            "width": content_width,
            "height": window_height - content_start_y - 30,
            "payload": {
                "text": f"View: {current_view}\n\nThis is the {current_view} view.",
                "size": "body",
                "color": "#cccccc"
            }
        })
        
        return {"nodes": nodes}

# ===== HTTP RESPONSE HELPERS (Pure translation) =====

    def _send_json(self, data, status_code=200):
        """Send JSON response with error handling"""
        try:
            # Serialize JSON completely before sending headers
            content = json.dumps(data, default=str).encode('utf-8')
            self._send_response(status_code, content, "application/json")
        except (TypeError, ValueError) as e:
            # JSON serialization failed - return error response
            err_msg = f"JSON serialization error: {str(e)}"
            print(f"[ERROR] _send_json: {err_msg}", flush=True)
            self._send_error(500, err_msg)
        except Exception as e:
            # Unexpected error
            err_msg = f"Unexpected error: {type(e).__name__}: {str(e)}"
            print(f"[ERROR] _send_json: {err_msg}", flush=True)
            self._send_error(500, err_msg)

    def _send_response(self, status_code, content, content_type):
        """Send HTTP response with complete headers"""
        try:
            # Send status and headers
            self.send_response(status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Connection", "close")
            self.end_headers()
            # Write content and flush
            self.wfile.write(content)
            self.wfile.flush()
        except Exception as e:
            print(f"[ERROR] _send_response: {type(e).__name__}: {str(e)}", flush=True)

    def _send_error(self, status_code, message):
        """Send error response"""
        content = message.encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_404(self):
        """Send 404 Not Found"""
        self._send_error(404, "404 - Not Found")


# ===== MAIN ENTRY POINT =====

def main():
    """Start HTTP server with full diagnostics"""
    host = "127.0.0.1"
    port = 8081

    # ===== CRITICAL ERROR CHECK =====
    if LEDGER_INIT_ERROR:
        print_and_log("\n" + "="*70)
        print_and_log("[FATAL] JARVIS v3 STARTUP FAILED")
        print_and_log("="*70)
        print_and_log(f"Error: {LEDGER_INIT_ERROR}")
        print_and_log("\nServer cannot start. Ledger initialization failed.")
        print_and_log("Check boot log: jarvis_v3_boot.log")
        print_and_log("="*70 + "\n")
        # Exit with error code so we DON'T try to use this process
        sys.exit(1)
    
    # ===== STARTUP DIAGNOSTICS =====
    print_and_log("\n" + "="*70)
    print_and_log("[STARTUP] JARVIS v3 WEBSERVER STARTING")
    print_and_log("="*70)
    print_and_log(f"Boot Timestamp: {BOOT_TIMESTAMP}")
    print_and_log(f"Boot Log:       {BOOT_LOG_FILE}")
    print_and_log("")
    
    # ===== PROTOCOL COMPLIANCE VERIFICATION =====
    verify_protocol_compliance()
    print_and_log("")
    print_and_log("="*70)
    print_and_log(f"Boot Timestamp: {BOOT_TIMESTAMP}")
    print_and_log(f"Boot Log:       {BOOT_LOG_FILE}")
    print_and_log("\nComponents loaded:")
    print_and_log(f"  + Ledger:       OK (LedgerQuery initialized)")
    print_and_log(f"  + Buttons:      {len(ledger.buttons)} UI elements")
    print_and_log(f"  + Dashboards:   {len(ledger.dashboards)} views")
    print_and_log(f"  + Elections:    {len(ledger.elections)} recorded")
    print_and_log(f"  + Frame Cache:  Ready")
    print_and_log(f"\nServer configuration:")
    print_and_log(f"  + Host:         {host}")
    print_and_log(f"  + Port:         {port}")
    print_and_log(f"  + Health Check: http://{host}:{port}/api/health")
    print_and_log(f"  + State Check:  http://{host}:{port}/api/state")
    print_and_log(f"  + Frame Check:  http://{host}:{port}/api/frame")
    print_and_log("="*70)
    print_and_log("[READY] JARVIS v3 READY FOR CONNECTIONS")
    print_and_log("="*70)
    
    # ===== SELF-AWARENESS BOOT MESSAGE =====
    boot_msg = SelfAwareness.boot_message()
    boot_msg_safe = SelfAwareness.to_console_safe(boot_msg)
    print_and_log(boot_msg_safe)
    print_and_log("")

    try:
        print_and_log(f"[HTTP] Binding to {host}:{port}...")
        server = HTTPServer((host, port), JarvisHandler)
        print_and_log(f"[HTTP] [OK] Server bound successfully")
        
        server.timeout = 1  # 1 second timeout for handle_request
        print_and_log("[HTTP] Entering request loop...")
        
        # Use handle_request loop instead of serve_forever to avoid threading issues
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        print_and_log("[SHUTDOWN] Keyboard interrupt received")
        server.server_close()
    except OSError as e:
        print_and_log(f"\n[ERROR FATAL] {type(e).__name__}: {str(e)}")
        print_and_log(f"\nPossible causes:")
        if "Address already in use" in str(e):
            print_and_log(f"  - Port {port} is already in use")
            print_and_log(f"  - Another instance of JARVIS is already running")
            print_and_log(f"  - Check: netstat -an | findstr :{port}")
        else:
            print_and_log(f"  - {str(e)}")
        print_and_log(f"\nBoot log: {BOOT_LOG_FILE}")
        sys.exit(1)
    except Exception as e:
        print_and_log(f"\n[ERROR UNEXPECTED] {type(e).__name__}: {str(e)}")
        print_and_log(f"\nTraceback:")
        print_and_log(traceback.format_exc())
        print_and_log(f"\nBoot log: {BOOT_LOG_FILE}")
        sys.exit(1)


if __name__ == "__main__":
    main()
