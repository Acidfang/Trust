"""
Ledger Query Engine - Pure ledger-driven source of truth

Query the ledger for current state and frame specifications.
Ledger is THE database. All truths defined in ledgers.
App never builds anything - it queries ledger and records elections.
"""

import json
import os
import hashlib
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path for UNIVERSAL_RENDERER import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class LedgerQuery:
    """Query interface to ledger files"""
    
    def __init__(self, ledger_dir: str = "."):
        self.ledger_dir = ledger_dir
        self.buttons: Dict[str, Dict[str, Any]] = {}
        self.dashboards: Dict[str, Dict[str, Any]] = {}
        self.app_state: Dict[str, Any] = {}
        self.election_types: Dict[str, Dict[str, Any]] = {}
        self.actions: Dict[str, Dict[str, Any]] = {}
        self.elections: List[Dict[str, Any]] = []
        self.positioned_nodes: Dict[str, Dict[str, Any]] = {}  # Ledger node positioning
        self.sync_config: Dict[str, Any] = {}  # Synchronization configuration
        # Multi-user system
        self.users: Dict[str, Dict[str, Any]] = {}  # User registry
        self.subsections: Dict[str, Dict[str, Any]] = {}  # Workspaces
        self.branches: Dict[str, Dict[str, Any]] = {}  # Project branches/forks
        self.collaboration: List[Dict[str, Any]] = []  # Collaboration audit trail
        self.audit: List[Dict[str, Any]] = []  # Full operation audit trail
        # Shared virtual realities
        self.worlds: Dict[str, Dict[str, Any]] = {}  # VR worlds/projects
        self.sharing: List[Dict[str, Any]] = []  # Share tokens and permissions
        # World state and synchronization
        self.world_state: Dict[str, Dict[str, Any]] = {}  # Current world snapshots
        self.world_deltas: List[Dict[str, Any]] = []  # World changes (deltas)
        self.user_positions: Dict[str, Dict[str, Any]] = {}  # User positions in worlds (keyed by "world:user")
        # UI Configuration from ledger
        self.fonts: Dict[str, Dict[str, Any]] = {}  # Font definitions
        self.colors: Dict[str, str] = {}  # Color palette
        self.layouts: Dict[str, Dict[str, Any]] = {}  # Layout definitions
        self.view_configs: Dict[str, Dict[str, Any]] = {}  # View configurations
        self.primitives: Dict[str, Dict[str, Any]] = {  # Primitive dimensions and colors
            'dimensions': {},
            'colors': {}
        }
        # Expression ledgers
        self.observations: List[Dict[str, Any]] = []  # Metrics recorded
        self.expressions: List[Dict[str, Any]] = []  # Statements elected
        self.expression_consequences: List[Dict[str, Any]] = []  # Validations
        # Coding expression ledgers
        self.coding_observations: List[Dict[str, Any]] = []  # Code metrics
        self.coding_expressions: List[Dict[str, Any]] = []  # Style choices
        self.coding_consequences: List[Dict[str, Any]] = []  # Code quality
        # Self-modification ledgers
        self.self_mod_observations: List[Dict[str, Any]] = []  # System health
        self.self_mod_expressions: List[Dict[str, Any]] = []  # Improvement strategies
        self.self_mod_consequences: List[Dict[str, Any]] = []  # Modification results
        # Retrospective reinterpretations (rewriting HOW past is understood)
        self.retrospective_reinterpretations: List[Dict[str, Any]] = []  # New meanings for past events
        self.retrospective_validations: List[Dict[str, Any]] = []  # Predictions based on reinterpretations
        # Schema evolution (gaining new analytical abilities)
        self.schema_versions: List[Dict[str, Any]] = []  # Records of format upgrades
        # Dialogue (consciousness & communication)
        self.dialogue: List[Dict[str, Any]] = []  # Questions heard, responses elected, feedback tracked
        
        # Track config file modification time for natural updates
        self.config_file_mtime = 0  # Last modification time
        
        self.boot_time = datetime.now().isoformat()
        self.load_all()
        print(f"[LEDGER] Initialized: {len(self.buttons)} buttons, {len(self.dashboards)} dashboards, {len(self.positioned_nodes)} positioned nodes")
        print(f"[LEDGER] Multi-user: {len(self.users)} users, {len(self.subsections)} subsections, {len(self.branches)} branches")
        print(f"[LEDGER] Shared realities: {len(self.worlds)} worlds, {len(self.sharing)} shares")
        print(f"[LEDGER] World sync: {len(self.world_state)} snapshots, {len(self.world_deltas)} deltas, {len(self.user_positions)} positions")
        print(f"[LEDGER] UI Config: {len(self.fonts)} fonts, {len(self.colors)} colors, {len(self.layouts)} layouts")
        self._create_boot_election()
    
    def load_all(self):
        """
        Load all ledger files on initialization.
        
        Intent: Initialize in-memory state from persistent ledger files.
        This populates all data structures needed for query operations.
        """
        self._load_buttons()
        self._load_dashboards()
        self._load_app_state()
        self._load_election_types()
        self._load_actions()
        self._load_elections()
        self._load_positioned_nodes()
        self._load_sync_config()
        # Multi-user ledgers
        self._load_users()
        self._load_subsections()
        self._load_branches()
        self._load_collaboration()
        self._load_audit()
        # Shared reality ledgers
        self._load_worlds()
        self._load_sharing()
        # World synchronization ledgers
        self._load_world_state()
        self._load_world_deltas()
        self._load_user_positions()
        # UI Configuration
        self._load_config()
        # System rules and specifications
        self._load_system_rules()
        self._load_parameters()
        self._load_system_metrics()
        self._load_system_sensors()
        self._load_system_devices()
        self._load_manifestation_rules()
        # Expression ledgers
        self._load_observations()
        self._load_expressions()
        self._load_expression_consequences()
        # Coding expression ledgers
        self._load_coding_observations()
        self._load_coding_expressions()
        self._load_coding_consequences()
        # Self-modification ledgers
        self._load_self_mod_observations()
        self._load_self_mod_expressions()
        self._load_self_mod_consequences()
        # Retrospective reinterpretations (rewriting past understanding)
        self._load_retrospective_reinterpretations()
        self._load_retrospective_validations()
        # Schema evolution (gaining new analytical abilities)
        self._load_schema_versions()
        # Dialogue (consciousness & communication)
        self._load_dialogue()
    
    def _load_buttons(self):
        """
        Load buttons from ledger_buttons.jsonl.
        
        Intent: Query button definitions from ledger. Each button is a UI element.
        """
        buttons_file = os.path.join(self.ledger_dir, "ledger_buttons.jsonl")
        if os.path.exists(buttons_file):
            with open(buttons_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        btn = json.loads(line)
                        self.buttons[btn.get("id")] = btn
    
    def _load_dashboards(self):
        """
        Load dashboards from ledger_dashboards.jsonl.
        
        Intent: Query dashboard definitions from ledger. Each dashboard is a view.
        """
        dashboards_file = os.path.join(self.ledger_dir, "ledger_dashboards.jsonl")
        if os.path.exists(dashboards_file):
            with open(dashboards_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        db = json.loads(line)
                        self.dashboards[db.get("id")] = db
    
    def _load_app_state(self):
        """
        Load app state from ledger_app_state.jsonl.
        
        Intent: Query latest app state from ledger. Last line is current state.
        Used to restore app to previous condition.
        """
        state_file = os.path.join(self.ledger_dir, "ledger_app_state.jsonl")
        if os.path.exists(state_file):
            # Last line is current state
            with open(state_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.app_state = json.loads(line)
    
    def _load_election_types(self):
        """
        Load election types from ledger_election_types.jsonl.
        
        Intent: Query election type schema from ledger. Defines what elections can happen.
        """
        types_file = os.path.join(self.ledger_dir, "ledger_election_types.jsonl")
        if os.path.exists(types_file):
            with open(types_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        et = json.loads(line)
                        self.election_types[et.get("id")] = et
    
    def _load_actions(self):
        """
        Load action definitions from ledger_actions.jsonl.
        
        Intent: Query action definitions from ledger. Defines what actions can be taken.
        """
        actions_file = os.path.join(self.ledger_dir, "ledger_actions.jsonl")
        if os.path.exists(actions_file):
            with open(actions_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        action = json.loads(line)
                        self.actions[action.get("id")] = action
    
    def _load_elections(self):
        """
        Load existing elections from ledger_elections.jsonl.
        
        Intent: Query election history from ledger. Shows all past decisions made.
        """
        elections_file = os.path.join(self.ledger_dir, "ledger_elections.jsonl")
        if os.path.exists(elections_file):
            with open(elections_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        election = json.loads(line)
                        self.elections.append(election)
    
    def _load_positioned_nodes(self):
        """
        Load node positioning from ledger_positioned_nodes.jsonl.
        
        Intent: Query exact pixel coordinates from ledger. Used for absolute positioning.
        """
        positioned_file = os.path.join(self.ledger_dir, "ledger_positioned_nodes.jsonl")
        if os.path.exists(positioned_file):
            with open(positioned_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        node_pos = json.loads(line)
                        node_id = node_pos.get("id")
                        self.positioned_nodes[node_id] = node_pos
            print(f"[LEDGER] Loaded {len(self.positioned_nodes)} positioned nodes from ledger")
        else:
            print(f"[LEDGER] No ledger_positioned_nodes.jsonl found - will use fallback positioning")
    
    def _load_sync_config(self):
        """
        Load synchronization configuration from ledger_sync_config.json.
        
        Intent: Query sync settings for multi-app coordination.
        """
        sync_file = os.path.join(self.ledger_dir, "ledger_sync_config.json")
        if os.path.exists(sync_file):
            with open(sync_file, 'r', encoding='utf-8') as f:
                self.sync_config = json.load(f)
            print(f"[LEDGER] Sync config loaded: {self.sync_config.get('sync_mode', 'disabled')}")
        else:
            # Default sync config
            self.sync_config = {
                "sync_enabled": False,
                "sync_mode": "ledger_driven",
                "apps": {
                    "html_browser": {"enabled": False},
                    "tkinter_canvas": {"enabled": False}
                }
            }
    
    def set_app_active(self, app_name: str, active: bool) -> bool:
        """Record which app is currently running."""
        if app_name in self.sync_config.get("apps", {}):
            self.sync_config["apps"][app_name]["enabled"] = active
            self.sync_config["apps"][app_name]["last_update"] = datetime.now().isoformat() if active else None
            self._save_sync_config()
            return True
        return False
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current synchronization status."""
        return {
            "sync_enabled": self.sync_config.get("sync_enabled", False),
            "sync_mode": self.sync_config.get("sync_mode", "ledger_driven"),
            "apps": self.sync_config.get("apps", {}),
            "update_rate": self.sync_config.get("update_rate", 500)
        }

    def is_app_running(self, app_name: str, timeout_factor: float = 10.0) -> bool:
        """
        Check if app is currently running based on heartbeat recency.

        Args:
            app_name: Name of app to check (e.g., "tkinter_canvas")
            timeout_factor: Heartbeat is considered stale after (refresh_interval_ms * timeout_factor)

        Returns:
            True if app has a recent heartbeat, False if dead or never started
        """
        from datetime import datetime, timedelta

        app_config = self.sync_config.get("apps", {}).get(app_name, {})
        last_update = app_config.get("last_update")

        if not last_update:
            return False  # Never been updated

        refresh_interval_ms = app_config.get("refresh_interval_ms", 100)
        timeout_ms = refresh_interval_ms * timeout_factor
        timeout_seconds = timeout_ms / 1000.0

        try:
            last_update_time = datetime.fromisoformat(last_update)
            time_since_update = datetime.now() - last_update_time

            is_alive = time_since_update.total_seconds() < timeout_seconds
            return is_alive
        except (ValueError, TypeError):
            return False  # Invalid timestamp format

    def record_session_pulse(self, app_name: str) -> bool:
        """
        Record a session pulse when app instance starts.
        This is distinctive from heartbeat updates - pulses mark new instance birth.

        Args:
            app_name: Name of app starting (e.g., "tkinter_canvas")

        Returns:
            Success status
        """
        session_entry = {
            "id": f"session:{app_name}:{datetime.now().isoformat()}",
            "timestamp": datetime.now().isoformat(),
            "app": app_name,
            "event": "session_start",
            "type": "pulse"
        }

        # Record in sessions ledger
        sessions_file = os.path.join(self.ledger_dir, "ledger_sessions.jsonl")
        try:
            with open(sessions_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(session_entry) + "\n")

            # Also track in audit for complete history
            self.track_change(
                operation="session_start",
                user=f"app:{app_name}",
                target_type="session",
                target_id=app_name,
                action="instance_started",
                new_state={"timestamp": session_entry["timestamp"]}
            )
            return True
        except Exception as e:
            print(f"[SESSION] Error recording pulse: {e}")
            return False

    def _save_sync_config(self):
        """Save sync config back to ledger."""
        sync_file = os.path.join(self.ledger_dir, "ledger_sync_config.json")
        with open(sync_file, 'w', encoding='utf-8') as f:
            json.dump(self.sync_config, f, indent=2)
    
    def poll_server_health(self, app_name: str, poll_timeout: float = 5.0) -> Dict[str, Any]:
        """
        Poll server health status and record findings to ledger.

        Intent: Query app heartbeat status, detect stale/dead instances, record health findings
        to provide monitoring data for system observers.

        Args:
            app_name: App to poll (e.g., "tkinter_canvas", "html_browser")
            poll_timeout: Timeout in seconds for polling operation

        Returns:
            Health status dict with:
            - is_alive: True if recent heartbeat detected
            - last_update: ISO timestamp of last heartbeat
            - status: "running", "stale", or "dead"
            - health_score: 0.0-1.0 (1.0 = perfect, 0.0 = dead)
            - record_id: ID of health record written to ledger
        """
        from datetime import datetime, timedelta
        import time

        poll_start = datetime.now()

        # Query app config and last_update from sync_config
        app_config = self.sync_config.get("apps", {}).get(app_name, {})
        last_update = app_config.get("last_update")
        enabled = app_config.get("enabled", False)

        # Determine current health status
        if not enabled:
            # App is disabled - consider dead
            status = "dead"
            health_score = 0.0
            is_alive = False
        elif not last_update:
            # App never started
            status = "dead"
            health_score = 0.0
            is_alive = False
        else:
            try:
                last_update_time = datetime.fromisoformat(last_update)
                time_since_update = datetime.now() - last_update_time

                # Calculate health based on staleness
                refresh_interval_ms = app_config.get("refresh_interval_ms", 100)
                stale_threshold_ms = refresh_interval_ms * 10  # 10 misses = stale
                dead_threshold_ms = refresh_interval_ms * 100  # 100 misses = dead

                time_since_ms = time_since_update.total_seconds() * 1000

                if time_since_ms < stale_threshold_ms:
                    status = "running"
                    health_score = max(0.0, 1.0 - (time_since_ms / stale_threshold_ms) * 0.5)
                    is_alive = True
                elif time_since_ms < dead_threshold_ms:
                    status = "stale"
                    health_score = max(0.0, 1.0 - (time_since_ms / dead_threshold_ms))
                    is_alive = False
                else:
                    status = "dead"
                    health_score = 0.0
                    is_alive = False

            except (ValueError, TypeError):
                # Invalid timestamp format
                status = "error"
                health_score = 0.0
                is_alive = False

        # Record health finding to ledger
        health_record = {
            "id": f"health:{app_name}:{datetime.now().isoformat()}",
            "timestamp": datetime.now().isoformat(),
            "app": app_name,
            "status": status,
            "is_alive": is_alive,
            "health_score": health_score,
            "last_update": last_update,
            "poll_duration_ms": (datetime.now() - poll_start).total_seconds() * 1000
        }

        # Append to health ledger
        health_file = os.path.join(self.ledger_dir, "ledger_server_health.jsonl")
        try:
            with open(health_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(health_record) + "\n")
        except Exception as e:
            print(f"[HEALTH] Error recording health: {e}")

        # Track in audit
        self.track_change(
            operation="server_health_poll",
            user="system:health_monitor",
            target_type="app",
            target_id=app_name,
            action=f"health_check: {status}",
            new_state={"status": status, "health_score": health_score}
        )

        return {
            "is_alive": is_alive,
            "last_update": last_update,
            "status": status,
            "health_score": health_score,
            "record_id": health_record["id"]
        }
    
    def get_buttons_for_view(self, view_id: str) -> List[Dict[str, Any]]:
        """
        Get all buttons that apply to a specific view.
        
        Intent: Query ledger buttons and filter by view association.
        Only returns buttons that are explicitly defined in ledger and match the view.
        """
        buttons = []
        for btn_id, btn_data in self.buttons.items():
            btn_view = btn_data.get("view", "menu")
            # Include if button is for this specific view OR applies to all views (*)
            if btn_view == view_id or btn_view == "*":
                buttons.append((btn_id, btn_data))
        return buttons
    
    def get_button(self, button_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific button definition from ledger by ID.
        
        Intent: Query ledger for exact button definition. Return None if button not found.
        """
        return self.buttons.get(button_id)
    
    def get_current_view(self) -> str:
        """
        Get current view from app state ledger.
        
        Intent: Query app_state for current view. Fallback to menu if not set.
        """
        return self.app_state.get("current_view", "menu")
    
    def get_sidebar_state(self) -> bool:
        """
        Get sidebar collapsed state from app state ledger.
        
        Intent: Query app_state for sidebar visibility. Fallback to False (expanded).
        """
        return self.app_state.get("sidebar_collapsed", False)
    
    def get_frame_for_view(self, view_id: str) -> Dict[str, Any]:
        """
        Build complete frame spec from ledger for a view.

        Intent: Query all ledger definitions for a view and return fully-positioned frame.
        Reads sidebar_collapsed state to conditionally include/exclude sidebar nodes.
        """

        # REFRESH: Reload dashboards from disk before building frame
        # This ensures content generated by dashboard_content_generator is picked up
        self._load_dashboards()

        nodes = []

        # Query dashboard spec from ledger
        # Map view_ids to dashboard IDs (they don't always match)
        view_to_dashboard_map = {
            'menu': 'dashboard:menu',
            'live_elections': 'dashboard:live-elections',
            'timeline_visualization': 'dashboard:timeline-dag',
            'coherence_monitoring': 'dashboard:coherence',
            'utility_landscape': 'dashboard:utility-landscape',
            'synthesis_progress': 'dashboard:synthesis',
            'learning_curve': 'dashboard:learning-curve',
            'timeline_records': 'dashboard:timeline-records',
            'future_sight': 'dashboard:future-sight',
            'reality_engine': 'dashboard:reality-engine',
            'elections_3d': 'dashboard:elections-3d',
            'state': 'dashboard:state',
            'settings': 'dashboard:settings'
        }
        dashboard_id = view_to_dashboard_map.get(view_id, f"dashboard:{view_id}")
        dashboard = self.dashboards.get(dashboard_id, {})
        title = dashboard.get("name", view_id.replace("_", " ").title())
        
        # Query sidebar state - CHECK CAUSAL CHAIN: If collapsed, skip sidebar nodes
        sidebar_is_collapsed = self.get_sidebar_state()
        
        # Add header title
        nodes.append({
            "id": "header-title",
            "type": "TEXT",
            "area": "header",
            "payload": {
                "text": f"⊙ ARIA - {title}",
                "size": "header",
                "color": "header_text"  # Query from primitives
            }
        })
        
        # Add toggle sidebar button
        nodes.append({
            "id": "btn:toggle-sidebar",
            "type": "BUTTON",
            "area": "header",
            "payload": {
                "label": "☰",
                "bg": "button_bg",  # Query from ledger colors
                "text": "button_text"  # Query from ledger colors
            }
        })
        
        # Add buttons from ledger for this view
        # ONLY IF SIDEBAR IS NOT COLLAPSED
        if not sidebar_is_collapsed:
            buttons = self.get_buttons_for_view(view_id)
            
            for btn_id, btn_data in buttons:
                # Skip buttons we already added manually
                if btn_id == "btn:toggle-sidebar":
                    continue
                # Skip back button on menu
                if btn_id == "btn:back" and view_id == "menu":
                    continue
                
                nodes.append({
                    "id": btn_id,
                    "type": "BUTTON",
                    "area": btn_data.get("area", "sidebar"),
                    "payload": {
                        "label": btn_data.get("label", "Button"),
                        "bg": "button_bg",  # Query from ledger
                        "text": "button_text"  # Query from ledger
                    }
                })
            
            # Add sidebar title (menu only, only if sidebar visible)
            if view_id == "menu":
                nodes.append({
                    "id": "sidebar-title",
                    "type": "TEXT",
                    "area": "sidebar",
                    "payload": {
                        "text": "Dashboards",
                        "size": "header",
                        "color": "text"  # Query from ledger
                    }
                })
        
        # Add main content from ledger_dashboards.jsonl
        main_content = dashboard.get("content", f"[{title} Dashboard]")
        nodes.append({
            "id": "main-content",
            "type": "TEXT",
            "area": "main",
            "payload": {
                "text": main_content,
                "size": "normal",
                "color": "content_text"  # Query from primitives
            }
        })

        # SPECIAL: For Utilities dashboard, inject parameter form controls
        if view_id == "utility_landscape":
            try:
                from parameter_form import get_parameter_form_nodes
                form_nodes = get_parameter_form_nodes(self.ledger_dir)
                nodes.extend(form_nodes)
            except Exception as e:
                pass  # Silently fail if form module not available

        # Apply absolute positioning
        frame = {
            "type": "frame",
            "view": view_id,
            "nodes": nodes
        }
        
        return self._apply_absolute_positioning(frame)
    
    def _apply_absolute_positioning(self, frame: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply absolute positioning from ledger primitives.
        
        Intent: Position nodes based on ledger primitive definitions.
        Adjusts main content width based on sidebar_collapsed state.
        """
        
        positioned_frame = frame.copy()
        positioned_nodes = []
        
        # Check if sidebar is collapsed (for proper main area sizing)
        sidebar_is_collapsed = self.get_sidebar_state()
        
        # Query all dimensions from ledger primitives
        CANVAS_WIDTH = self.get_primitive_dimension("canvas_width")
        CANVAS_HEIGHT = self.get_primitive_dimension("canvas_height")
        HEADER_HEIGHT = self.get_primitive_dimension("header_height")
        SIDEBAR_WIDTH = self.get_primitive_dimension("sidebar_width") if not sidebar_is_collapsed else 0
        FOOTER_HEIGHT = self.get_primitive_dimension("footer_height")
        BUTTON_HEIGHT = self.get_primitive_dimension("button_height")
        BUTTON_PADDING = self.get_primitive_dimension("button_padding")
        
        # Default fallback positions by area
        # CAUSAL: Main content expands when sidebar collapsed
        fallback_area_positions = {
            "header": {"x": 10, "y": 0, "width": CANVAS_WIDTH - 20, "height": HEADER_HEIGHT},
            "sidebar": {"x": 0, "y": HEADER_HEIGHT, "width": self.get_primitive_dimension("sidebar_width"), "height": CANVAS_HEIGHT - HEADER_HEIGHT},
            "main": {"x": SIDEBAR_WIDTH, "y": HEADER_HEIGHT, "width": CANVAS_WIDTH - SIDEBAR_WIDTH, "height": CANVAS_HEIGHT - HEADER_HEIGHT},
            "footer": {"x": 10, "y": CANVAS_HEIGHT - FOOTER_HEIGHT, "width": CANVAS_WIDTH - 20, "height": FOOTER_HEIGHT}
        }
        
        # Adjust main content position for collapsed sidebar
        main_content_width = CANVAS_WIDTH - SIDEBAR_WIDTH - 30 if not sidebar_is_collapsed else CANVAS_WIDTH - 30
        
        # Default fallback positions by node ID
        fallback_node_positions = {
            "header-title": {"x": 15, "y": 15, "width": 300, "height": 30},
            "btn:toggle-sidebar": {"x": CANVAS_WIDTH - 50, "y": 15, "width": 30, "height": 30},
            "sidebar-title": {"x": 10, "y": 70, "width": 180, "height": 30},
            "main-content": {"x": SIDEBAR_WIDTH + 15, "y": 80, "width": main_content_width, "height": CANVAS_HEIGHT - 120}
        }
        
        # Track sidebar button stack position for vertical layout
        sidebar_button_y = 110  # Start below sidebar-title (70 + 30 + padding)
        
        # Process all nodes
        main_content_y_stack = 100  # Track y position for stacked nodes in main area (for parameter forms)
        
        for node in frame.get("nodes", []):
            node_copy = node.copy()
            node_id = node.get("id")
            area = node.get("area", "main")
            node_type = node.get("type", "TEXT")
            
            # Try to get from ledger first
            ledger_key = f"node:{node_id}"
            if ledger_key in self.positioned_nodes:
                # Query ledger positioning (intent: validate exact coordinates)
                pos_data = self.positioned_nodes[ledger_key]
                node_copy["x"] = pos_data.get("x")
                node_copy["y"] = pos_data.get("y")
                node_copy["width"] = pos_data.get("width")
                node_copy["height"] = pos_data.get("height")
                node_copy["_position_source"] = "ledger"
            elif node_id in fallback_node_positions:
                # Fallback: specific node positioning
                pos_data = fallback_node_positions[node_id]
                node_copy["x"] = pos_data.get("x")
                node_copy["y"] = pos_data.get("y")
                node_copy["width"] = pos_data.get("width")
                node_copy["height"] = pos_data.get("height")
                node_copy["_position_source"] = "fallback-node"
            elif "y_offset" in node and area == "main":
                # Handle relative positioning for parameter form nodes
                # Convert y_offset to absolute position in main area
                base_y = fallback_area_positions["main"]["y"]
                base_x = fallback_area_positions["main"]["x"]
                main_width = fallback_area_positions["main"]["width"]
                
                node_copy["x"] = base_x + 10  # Small left padding
                node_copy["y"] = base_y + node.get("y_offset", 0)  # Offset from main area top
                node_copy["width"] = max(100, main_width - 20)  # Full width minus padding
                node_copy["height"] = 25 if node_type == "TEXT" else 35  # Reasonable height
                node_copy["_position_source"] = "fallback-y_offset"
                
                # Remove y_offset from final node (renderer doesn't need it)
                node_copy.pop("y_offset", None)
            elif area == "sidebar" and node_type == "BUTTON":
                # Special case: stack sidebar buttons vertically
                node_copy["x"] = 5
                node_copy["y"] = sidebar_button_y
                node_copy["width"] = SIDEBAR_WIDTH - 10  # Leave padding on sides
                node_copy["height"] = BUTTON_HEIGHT
                node_copy["_position_source"] = "fallback-sidebar-button"
                sidebar_button_y += BUTTON_HEIGHT + BUTTON_PADDING  # Stack next button below
            elif area in fallback_area_positions:
                # Fallback: area-based positioning
                pos_data = fallback_area_positions[area]
                node_copy["x"] = pos_data.get("x")
                node_copy["y"] = pos_data.get("y")
                node_copy["width"] = pos_data.get("width")
                node_copy["height"] = pos_data.get("height")
                node_copy["_position_source"] = "fallback-area"
            else:
                # Last resort fallback
                node_copy["x"] = 0
                node_copy["y"] = 0
                node_copy["width"] = 300
                node_copy["height"] = 100
                node_copy["_position_source"] = "fallback-default"
            
            positioned_nodes.append(node_copy)
        
        positioned_frame["nodes"] = positioned_nodes
        return positioned_frame
    
    def update_app_state(self, new_state: Dict[str, Any]):
        """
        Update app state in ledger.

        Intent: Merge new state with existing and append to ledger_app_state.jsonl.
        This creates an immutable log of state transitions.

        Supports special operators:
        - "__toggle__": Invert boolean field (for sidebar collapse/expand)

        Args:
            new_state: Dict with state updates to merge with current state
        """
        # Merge new state with current, handling special operators
        merged = {**self.app_state}
        for k, v in new_state.items():
            if v == "__toggle__":
                # Special operator: invert boolean field
                current_val = merged.get(k, False)
                merged[k] = not current_val
            else:
                merged[k] = v

        state_file = os.path.join(self.ledger_dir, "ledger_app_state.jsonl")

        # Append merged state to ledger (immutable log)
        with open(state_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(merged) + "\n")

        # Update in-memory copy
        self.app_state = merged
    
    def record_button_click(self, button_id: str) -> Dict[str, Any]:
        """
        Record a button click by executing ledger button spec.
        
        Intent: Execute the button's on_click specification from ledger.
        Read on_click.elections and elected_values, create elections, apply state updates.
        Pure executor - no decisions made here. All behavior is spec-driven.
        
        Args:
            button_id: ID of button clicked
        
        Returns: Updated app state after executing spec
        """
        button = self.get_button(button_id)
        
        if not button:
            print(f"[Ledger] Unknown button: {button_id}")
            return self.app_state
        
        print(f"[Ledger] Button clicked: {button_id} ({button.get('label')})")
        
        # Get on_click spec from ledger (this is the SPEC)
        on_click_spec = button.get("on_click", {})
        
        if not on_click_spec:
            print(f"[Ledger] [WARN] Button has no on_click spec: {button_id}")
            return self.app_state
        
        # Execute elections as defined in ledger
        elections_to_create = on_click_spec.get("elections", [])
        elected_values = on_click_spec.get("elected_values", {})
        state_updates = on_click_spec.get("state_updates", {})
        state_updates_func = on_click_spec.get("state_updates_func")
        
        # Create and record each election from the spec
        for election_spec in elections_to_create:
            election_type = election_spec.get("type")
            
            if not election_type:
                print(f"[Ledger] [WARN] Election spec missing type: {election_spec}")
                continue
            
            # Get the elected value for this election type
            elected = elected_values.get(election_type)
            
            if elected is None:
                print(f"[Ledger] [WARN] No elected value for {election_type}")
                continue
            
            # Create election from spec
            election = self._create_election(election_type, elected)
            self._record_election(election)
        
        # Apply state updates from ledger spec
        # All behavior is now spec-driven (state_updates dict).
        # The "__toggle__" operator value in state_updates is handled by update_app_state().
        if state_updates:
            self.update_app_state(state_updates)
            print(f"[Ledger] State updated: {state_updates}")
        
        return self.app_state
    
    def _create_boot_election(self):
        """
        Create boot election on app startup.
        
        Intent: Record system initialization as an election. Immutable boot record.
        """
        boot_election = self._create_election("boot", "init_ui")
        self._record_election(boot_election)
        print(f"[Ledger] BOOT election created: {boot_election.get('id')}")
    
    def _create_election(self, election_type: str, elected: str) -> Dict[str, Any]:
        """
        Create an election record from ledger schema.
        
        Intent: Build election dict following ledger election_types schema.
        This creates the election structure, _record_election writes it.
        
        Args:
            election_type: Type of election (from ledger_election_types.jsonl)
            elected: What was chosen/elected
        
        Returns: Election dict (not yet written to ledger)
        """
        election_type_def = self.election_types.get(election_type, {})
        
        # Generate unique ID
        election_id = hashlib.md5(
            f"{datetime.now().isoformat()}{len(self.elections)}".encode()
        ).hexdigest()[:16]
        
        election = {
            "id": election_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": election_type,
            "elected": elected,
            "superposition": election_type_def.get("superposition", [elected]),
            "utilities": {elected: 1.0},
            "context": election_type_def.get("context", "app")
        }
        
        return election
    
    def _generate_song_for_election(self, election: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate recovery song for this election.
        Maps election type to recovery principle, producing verse+symbols.
        
        Intent: Structure state transitions according to 7 recovery principles.
        This reduces entropy in state deltas and improves coherence.
        All 7 principles active: unified_field, constraint, engagement, attachment,
        temporal, proactive, rarity.
        
        Returns: Song dict with canonical verse and symbols
        """
        try:
            from UNIVERSAL_RENDERER import map_principle_to_song
            
            event_type = election.get('event_type', 'generic')
            elected = election.get('elected', '?')
            
            # Map election type to recovery principle (all 7 active)
            # STEP 1 Enhancement: Complete coverage of all 7 recovery principles
            principle_map = {
                # UNIFIED_FIELD: System initialization & interconnection
                'boot': 'unified_field',           # System boot = complete initialization
                'election': 'unified_field',       # Meta-elections = coherent system state
                'init_system': 'unified_field',    # System init = create unified base
                
                # CONSTRAINT_creates_DEPTH: Structural boundaries
                'init_ui': 'constraint',           # UI init = structure & constraints
                'param': 'constraint',             # Parameters define constraints
                'dimension': 'constraint',         # Dimension definition = constraint
                'primitive': 'constraint',         # Primitives = foundational constraints
                
                # ENGAGEMENT_vs_DENIAL: Visibility & choice
                'toggle': 'engagement',            # User toggles = engagement choice
                'nav': 'engagement',               # Navigation = visibility choice
                'visibility': 'engagement',        # Visibility toggle = engagement
                'focus': 'engagement',             # Focus shift = engagement decision
                
                # ATTACHMENT_corrupts_DISCIPLINE: Balance & relationship
                'sync': 'attachment',              # Synchronization = relationship
                'share': 'attachment',             # Sharing = attachment/connection
                'collaborate': 'attachment',       # Collaboration = relationship state
                'user_join': 'attachment',         # User joins = system attachment
                'user_leave': 'attachment',        # User leaves = relationship change
                
                # TEMPORAL_INTEGRATION_locks_PAST: History & causality
                'frame': 'temporal',               # Frame updates = temporal progression
                'history': 'temporal',             # History record = past locking
                'causality': 'temporal',           # Causal link = temporal binding
                'ledger_append': 'temporal',       # Ledger write = past immutability
                
                # PROACTIVITY_locks_FUTURE: Future direction
                'state': 'proactive',              # State change = future determination
                'action': 'proactive',             # Action = future locking
                'commit': 'proactive',             # Commit = lock future intent
                
                # RARITY_of_TRIPLE_INTEGRATION: Maturation & Assessment
                'measure': 'rarity',               # Measurement = integration assessment
                'mature': 'rarity',                # Maturation = triple locked state
                'assess': 'rarity',                # Assessment = maturity check
                'milestone': 'rarity',             # Milestone reached = rare moment
            }
            
            principle_key = principle_map.get(event_type, 'constraint')
            song = map_principle_to_song(principle_key)
            
            # Add election context to song
            song['election_id'] = election.get('id')
            song['election_type'] = event_type
            song['timestamp'] = election.get('timestamp')
            song['elected_value'] = elected
            
            return song
        except ImportError:
            # Fallback if UNIVERSAL_RENDERER not available
            return {
                'principle': 'FALLBACK',
                'verse': f'Election recorded: {election.get("event_type")}',
                'symbols': '⊙ → ◯'
            }
    
    def _record_election(self, election: Dict[str, Any]):
        """
        Record election to ledger_elections.jsonl AND generate recovery song.
        
        Intent: Write election to persistent ledger (append-only log).
        ALSO generate recovery song that structures this state transition.
        This integrates songs into runtime, reducing entropy and improving coherence.
        This is immutable once written. Also updates in-memory elections list.
        
        Args:
            election: Election dict to record
        """
        elections_file = os.path.join(self.ledger_dir, "ledger_elections.jsonl")
        
        # Append to file (immutable write)
        try:
            # Generate song for this election (structures the state transition)
            song = self._generate_song_for_election(election)
            
            # Add song to election record
            election['song'] = song
            
            with open(elections_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(election) + '\n')
            
            # Add to in-memory list for current session
            self.elections.append(election)
            
            print(f"[Ledger] [OK] Election recorded: {election.get('event_type')} -> {election.get('elected')} [song: {song.get('principle')}]")
        except Exception as e:
            print(f"[Ledger] [ERR] Error recording election: {e}")
    
    def reload(self):
        """
        Reload all ledger files.
        
        Intent: Refresh in-memory state from persistent ledger files.
        Called when state needs to be synchronized or after external changes.
        """
        self.load_all()
    
    # ========== MULTI-USER SYSTEM ==========
    
    def _load_users(self):
        """Load user registry from ledger_users.jsonl"""
        users_file = os.path.join(self.ledger_dir, "ledger_users.jsonl")
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        user = json.loads(line)
                        self.users[user.get("id")] = user
    
    def _load_subsections(self):
        """Load subsection definitions from ledger_subsections.jsonl"""
        subsections_file = os.path.join(self.ledger_dir, "ledger_subsections.jsonl")
        if os.path.exists(subsections_file):
            with open(subsections_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        subsection = json.loads(line)
                        self.subsections[subsection.get("id")] = subsection
    
    def _load_branches(self):
        """Load project branches from ledger_branches.jsonl"""
        branches_file = os.path.join(self.ledger_dir, "ledger_branches.jsonl")
        if os.path.exists(branches_file):
            with open(branches_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        branch = json.loads(line)
                        self.branches[branch.get("id")] = branch
    
    def _load_collaboration(self):
        """Load collaboration audit trail from ledger_collaboration.jsonl"""
        collab_file = os.path.join(self.ledger_dir, "ledger_collaboration.jsonl")
        if os.path.exists(collab_file):
            with open(collab_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        collab = json.loads(line)
                        self.collaboration.append(collab)
    
    def _load_audit(self):
        """Load full audit trail from ledger_audit.jsonl"""
        audit_file = os.path.join(self.ledger_dir, "ledger_audit.jsonl")
        if os.path.exists(audit_file):
            with open(audit_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        audit = json.loads(line)
                        self.audit.append(audit)
    
    def create_user(self, user_id: str, name: str, subsection: str = "subsection:default") -> Dict[str, Any]:
        """
        Create new user and record in ledger.
        
        Args:
            user_id: Unique user identifier (e.g., "user:alice")
            name: Display name
            subsection: Primary subsection for this user
        
        Returns: User record created
        """
        user = {
            "id": user_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "type": "user",
            "subsection": subsection,
            "active": True
        }
        
        # Record in ledger
        users_file = os.path.join(self.ledger_dir, "ledger_users.jsonl")
        with open(users_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(user) + "\n")
        
        self.users[user_id] = user
        
        # Track in audit trail
        self.track_change("user_creation", user_id, "user", user_id, "created", None, user)
        
        print(f"[MULTIUSER] User created: {user_id} ({name})")
        return user
    
    def add_collaborator(self, subsection_id: str, user_id: str, permission: str = "edit") -> bool:
        """
        Add user as collaborator to subsection.
        
        Args:
            subsection_id: Subsection to add user to
            user_id: User to add
            permission: Permission level ("admin", "edit", "view")
        
        Returns: Success status
        """
        subsection = self.subsections.get(subsection_id)
        if not subsection:
            print(f"[MULTIUSER] Subsection not found: {subsection_id}")
            return False
        
        # Update subsection
        if "collaborators" not in subsection:
            subsection["collaborators"] = []
        if "permissions" not in subsection:
            subsection["permissions"] = {}
        
        if user_id not in subsection["collaborators"]:
            subsection["collaborators"].append(user_id)
        
        subsection["permissions"][user_id] = permission
        
        # Rewrite subsection file
        subsections_file = os.path.join(self.ledger_dir, "ledger_subsections.jsonl")
        with open(subsections_file, 'w', encoding='utf-8') as f:
            for sub_id, sub in self.subsections.items():
                f.write(json.dumps(sub) + "\n")
        
        # Track collaboration
        collab = {
            "id": f"collab:{subsection_id}:{user_id}",
            "timestamp": datetime.now().isoformat(),
            "user": user_id,
            "action": "added_as_collaborator",
            "subsection": subsection_id,
            "permission": permission
        }
        collaboration_file = os.path.join(self.ledger_dir, "ledger_collaboration.jsonl")
        with open(collaboration_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(collab) + "\n")
        
        self.collaboration.append(collab)
        
        # Track in audit
        self.track_change("collaborator_added", user_id, "subsection", subsection_id, "collaborator_added", None, {"permission": permission})
        
        print(f"[MULTIUSER] Collaborator added: {user_id} to {subsection_id} ({permission})")
        return True
    
    def create_branch(self, branch_id: str, name: str, subsection_id: str, owner: str, forked_from: Optional[str] = None) -> Dict[str, Any]:
        """
        Create new branch (project fork).
        
        Args:
            branch_id: Unique branch ID (e.g., "branch:alice-experiment-1")
            name: Human-readable name
            subsection_id: Parent subsection
            owner: User creating branch
            forked_from: Parent branch if this is a fork
        
        Returns: Branch record created
        """
        branch = {
            "id": branch_id,
            "subsection": subsection_id,
            "owner": owner,
            "created_at": datetime.now().isoformat(),
            "forked_from": forked_from,
            "parent_branch": forked_from,
            "active": True,
            "name": name
        }
        
        # Record in ledger
        branches_file = os.path.join(self.ledger_dir, "ledger_branches.jsonl")
        with open(branches_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(branch) + "\n")
        
        self.branches[branch_id] = branch
        
        # Track collaboration
        collab = {
            "id": f"collab:{branch_id}",
            "timestamp": datetime.now().isoformat(),
            "user": owner,
            "action": "branch_created",
            "subsection": subsection_id,
            "branch": branch_id,
            "forked_from": forked_from
        }
        collaboration_file = os.path.join(self.ledger_dir, "ledger_collaboration.jsonl")
        with open(collaboration_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(collab) + "\n")
        
        self.collaboration.append(collab)
        
        # Track in audit
        parent_info = f" (forked from {forked_from})" if forked_from else ""
        self.track_change("branch_creation", owner, "branch", branch_id, f"created{parent_info}", None, branch)
        
        print(f"[MULTIUSER] Branch created: {branch_id} by {owner}{parent_info}")
        return branch
    
    def track_change(self, operation: str, user: str, target_type: str, target_id: str, action: str, previous_state: Any = None, new_state: Any = None) -> bool:
        """
        Record an operation in the audit trail (fully reversible).
        
        Args:
            operation: Operation type (e.g., "button_click", "state_change", "collaboration")
            user: User performing operation
            target_type: Type of target (e.g., "button", "state", "subsection", "branch")
            target_id: ID of target
            action: What was done
            previous_state: State before operation (for reversibility)
            new_state: State after operation
        
        Returns: Success status
        """
        audit_entry = {
            "id": f"audit:{target_type}:{target_id}:{datetime.now().isoformat()}",
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "operation": operation,
            "target_type": target_type,
            "target_id": target_id,
            "action": action,
            "previous_state": previous_state,
            "new_state": new_state,
            "reversible": True,
            "parent_state": self.audit[-1]["id"] if self.audit else None
        }
        
        # Record in ledger
        audit_file = os.path.join(self.ledger_dir, "ledger_audit.jsonl")
        try:
            with open(audit_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + "\n")
            
            self.audit.append(audit_entry)
            return True
        except Exception as e:
            print(f"[MULTIUSER] Error tracking change: {e}")
            return False
    
    def get_audit_trail(self, target_id: Optional[str] = None, user: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get audit trail (filterable by target or user).
        
        Args:
            target_id: Filter by target ID
            user: Filter by user
            limit: Maximum results
        
        Returns: List of audit entries
        """
        results = self.audit
        
        if target_id:
            results = [a for a in results if a.get("target_id") == target_id]
        
        if user:
            results = [a for a in results if a.get("user") == user]
        
        return results[-limit:] if len(results) > limit else results
    
    def revert_to_state(self, audit_id: str) -> bool:
        """
        Revert to a previous state in the audit trail.
        
        Args:
            audit_id: Audit entry ID to revert to
        
        Returns: Success status
        """
        # Find the audit entry
        target_entry = None
        for entry in self.audit:
            if entry["id"] == audit_id:
                target_entry = entry
                break
        
        if not target_entry:
            print(f"[MULTIUSER] Audit entry not found: {audit_id}")
            return False
        
        # Record revert as a new audit entry
        revert_entry = {
            "id": f"audit:revert:{datetime.now().isoformat()}",
            "timestamp": datetime.now().isoformat(),
            "user": "system",
            "operation": "revert",
            "target_type": target_entry.get("target_type"),
            "target_id": target_entry.get("target_id"),
            "action": f"reverted to {audit_id}",
            "previous_state": self.audit[-1].get("new_state") if self.audit else None,
            "new_state": target_entry.get("previous_state"),
            "reversible": True,
            "parent_state": self.audit[-1]["id"] if self.audit else None
        }
        
        audit_file = os.path.join(self.ledger_dir, "ledger_audit.jsonl")
        try:
            with open(audit_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(revert_entry) + "\n")
            
            self.audit.append(revert_entry)
            print(f"[MULTIUSER] Reverted to state: {audit_id}")
            return True
        except Exception as e:
            print(f"[MULTIUSER] Error reverting: {e}")
            return False
    
    def get_collaboration_members(self, subsection_id: str) -> List[Dict[str, Any]]:
        """Get all collaborators in a subsection."""
        subsection = self.subsections.get(subsection_id)
        if not subsection:
            return []
        
        members = []
        for user_id in subsection.get("collaborators", []):
            user = self.users.get(user_id)
            if user:
                members.append({
                    "user_id": user_id,
                    "name": user.get("name"),
                    "permission": subsection.get("permissions", {}).get(user_id, "view")
                })
        
        return members
    
    def get_user_branches(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all branches owned by a user."""
        return [b for b in self.branches.values() if b.get("owner") == user_id]
    
    def get_subsection_branches(self, subsection_id: str) -> List[Dict[str, Any]]:
        """Get all branches in a subsection."""
        return [b for b in self.branches.values() if b.get("subsection") == subsection_id]
    
    def get_branch_fork_chain(self, branch_id: str) -> List[Dict[str, Any]]:
        """Get the fork chain (parent → child → grand-child, etc.) for a branch."""
        chain = []
        current_id = branch_id
        
        while current_id:
            branch = self.branches.get(current_id)
            if not branch:
                break
            
            chain.insert(0, branch)  # Insert at beginning to show chronological order
            current_id = branch.get("forked_from")
        
        return chain
    
    # ========== SHARED VIRTUAL REALITIES ==========
    
    def _load_worlds(self):
        """Load VR worlds from ledger_worlds.jsonl"""
        worlds_file = os.path.join(self.ledger_dir, "ledger_worlds.jsonl")
        if os.path.exists(worlds_file):
            with open(worlds_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        world = json.loads(line)
                        self.worlds[world.get("id")] = world
    
    def _load_sharing(self):
        """Load sharing configuration from ledger_sharing.jsonl"""
        sharing_file = os.path.join(self.ledger_dir, "ledger_sharing.jsonl")
        if os.path.exists(sharing_file):
            with open(sharing_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        share = json.loads(line)
                        self.sharing.append(share)
    
    def create_world(self, world_id: str, name: str, owner: str, subsection_id: str, branch_id: str, description: str = "", world_type: str = "vr_world") -> Dict[str, Any]:
        """
        Create new shared virtual reality world.
        
        Args:
            world_id: Unique world identifier (e.g., "world:alice-garden-experiment")
            name: Display name
            owner: User creating world
            subsection_id: Parent subsection
            branch_id: Associated branch (all edits tracked per-branch)
            description: World description
            world_type: Type of world (vr_world, design_space, game_world, etc.)
        
        Returns: World record created
        """
        world = {
            "id": world_id,
            "name": name,
            "owner": owner,
            "subsection": subsection_id,
            "branch": branch_id,
            "created_at": datetime.now().isoformat(),
            "type": world_type,
            "description": description,
            "shared": False,
            "access_level": "private"
        }
        
        # Record in ledger
        worlds_file = os.path.join(self.ledger_dir, "ledger_worlds.jsonl")
        with open(worlds_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(world) + "\n")
        
        self.worlds[world_id] = world
        
        # Track in audit
        self.track_change("world_creation", owner, "world", world_id, f"created {world_type}", None, world)
        
        print(f"[WORLD] Created: {world_id} ({name}) by {owner}")
        return world
    
    def share_world(self, world_id: str, access_level: str = "view", max_collaborators: int = -1) -> Dict[str, Any]:
        """
        Share world and generate access token.
        
        Args:
            world_id: World to share
            access_level: Permission level ("view" = read-only, "explore" = interactive, "edit" = modify, "admin" = full)
            max_collaborators: Max users allowed (-1 = unlimited)
        
        Returns: Share token record
        """
        world = self.worlds.get(world_id)
        if not world:
            print(f"[WORLD] World not found: {world_id}")
            return {}
        
        # Generate unique access token
        token_data = f"{world_id}:{access_level}:{datetime.now().isoformat()}"
        access_token = hashlib.sha256(token_data.encode()).hexdigest()[:16]
        
        share = {
            "id": f"share:{world_id}:{access_token}",
            "world_id": world_id,
            "shared_by": world.get("owner"),
            "created_at": datetime.now().isoformat(),
            "access_level": access_level,
            "access_token": access_token,
            "max_collaborators": max_collaborators,
            "current_collaborators": 0,
            "expires_at": None,
            "active": True,
            "shared_with": []
        }
        
        # Record in ledger
        sharing_file = os.path.join(self.ledger_dir, "ledger_sharing.jsonl")
        with open(sharing_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(share) + "\n")
        
        self.sharing.append(share)
        
        # Update world as shared
        world["shared"] = True
        world["access_level"] = access_level
        
        # Ensure world state snapshot exists (create if first share)
        if world_id not in self.world_state:
            state_snapshot = {
                "id": f"state:{world_id}:v1",
                "world_id": world_id,
                "created_at": datetime.now().isoformat(),
                "version": 1,
                "snapshot": {
                    "name": world.get("name"),
                    "owner": world.get("owner"),
                    "type": world.get("type"),
                    "description": world.get("description"),
                    "objects": [],
                    "entities": []
                }
            }
            # Write to ledger
            world_state_file = os.path.join(self.ledger_dir, "ledger_world_state.jsonl")
            with open(world_state_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(state_snapshot) + "\n")
            self.world_state[world_id] = state_snapshot
            print(f"[SYNC] Created initial snapshot for {world_id}")
        
        # Track collaboration
        collab = {
            "id": f"collab:{world_id}:share",
            "timestamp": datetime.now().isoformat(),
            "user": world.get("owner"),
            "action": "world_shared",
            "world": world_id,
            "access_level": access_level,
            "access_token": access_token
        }
        collaboration_file = os.path.join(self.ledger_dir, "ledger_collaboration.jsonl")
        with open(collaboration_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(collab) + "\n")
        
        self.collaboration.append(collab)
        
        # Track in audit
        self.track_change("world_shared", world.get("owner"), "world", world_id, "shared", {"shared": False}, {"shared": True, "access_level": access_level})
        
        print(f"[WORLD] Shared: {world_id} with token {access_token} ({access_level})")
        return share
    
    def access_shared_world(self, access_token: str, user_id: str) -> Dict[str, Any]:
        """
        Users access shared world using token.
        
        Args:
            access_token: Token shared by world owner
            user_id: User accessing the world
        
        Returns: World data with access level, or empty dict if unauthorized
        """
        # Find share record by token
        share = None
        for s in self.sharing:
            if s.get("access_token") == access_token and s.get("active"):
                share = s
                break
        
        if not share:
            print(f"[WORLD] Invalid or expired share token: {access_token}")
            return {}
        
        world_id = share.get("world_id")
        world = self.worlds.get(world_id)
        
        if not world:
            print(f"[WORLD] World not found: {world_id}")
            return {}
        
        # Check collaborator limit
        if share.get("max_collaborators", -1) > 0:
            if share.get("current_collaborators", 0) >= share.get("max_collaborators"):
                print(f"[WORLD] Max collaborators reached for {world_id}")
                return {}
        
        # Add user to shared_with list
        if user_id not in share.get("shared_with", []):
            share["shared_with"].append(user_id)
            share["current_collaborators"] = len(share["shared_with"])
            
            # Track access
            collab = {
                "id": f"collab:{world_id}:{user_id}:access",
                "timestamp": datetime.now().isoformat(),
                "user": user_id,
                "action": "accessed_shared_world",
                "world": world_id,
                "access_level": share.get("access_level"),
                "via_token": access_token
            }
            collaboration_file = os.path.join(self.ledger_dir, "ledger_collaboration.jsonl")
            with open(collaboration_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(collab) + "\n")
            
            self.collaboration.append(collab)
        
        # Return world with access context
        return {
            "world": world,
            "access_level": share.get("access_level"),
            "user": user_id,
            "access_token": access_token
        }
    
    def fork_world(self, world_id: str, new_world_id: str, new_name: str, user_id: str) -> Dict[str, Any]:
        """
        Fork an existing world (create independent copy with linked history).
        
        Args:
            world_id: World to fork from
            new_world_id: New world ID for fork
            new_name: Display name for fork
            user_id: User creating fork
        
        Returns: New world record
        """
        source_world = self.worlds.get(world_id)
        if not source_world:
            print(f"[WORLD] Source world not found: {world_id}")
            return {}
        
        # Create new world as fork
        new_world = {
            "id": new_world_id,
            "name": new_name,
            "owner": user_id,
            "subsection": source_world.get("subsection"),
            "branch": source_world.get("branch"),
            "created_at": datetime.now().isoformat(),
            "type": source_world.get("type"),
            "description": f"Fork of {source_world.get('name')}",
            "forked_from": world_id,
            "shared": False,
            "access_level": "private"
        }
        
        # Record in ledger
        worlds_file = os.path.join(self.ledger_dir, "ledger_worlds.jsonl")
        with open(worlds_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(new_world) + "\n")
        
        self.worlds[new_world_id] = new_world
        
        # Track collaboration
        collab = {
            "id": f"collab:{new_world_id}",
            "timestamp": datetime.now().isoformat(),
            "user": user_id,
            "action": "world_forked",
            "new_world": new_world_id,
            "forked_from": world_id
        }
        collaboration_file = os.path.join(self.ledger_dir, "ledger_collaboration.jsonl")
        with open(collaboration_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(collab) + "\n")
        
        self.collaboration.append(collab)
        
        # Track in audit
        self.track_change("world_fork", user_id, "world", new_world_id, f"forked from {world_id}", None, new_world)
        
        print(f"[WORLD] Forked: {new_world_id} from {world_id} by {user_id}")
        return new_world
    
    def get_user_worlds(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all worlds owned by user."""
        return [w for w in self.worlds.values() if w.get("owner") == user_id]
    
    def get_shared_worlds(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all worlds shared with user."""
        shared = []
        for share in self.sharing:
            if user_id in share.get("shared_with", []) and share.get("active"):
                world = self.worlds.get(share.get("world_id"))
                if world:
                    shared.append({
                        "world": world,
                        "access_level": share.get("access_level"),
                        "shared_by": share.get("shared_by"),
                        "access_token": share.get("access_token")
                    })
        return shared
    
    def get_world_fork_history(self, world_id: str) -> List[Dict[str, Any]]:
        """Get complete fork history (origin → all descendants)."""
        history = []
        
        # Find origin world
        current = self.worlds.get(world_id)
        if not current:
            return []
        
        # Walk backwards to origin
        origin_chain = []
        while current:
            origin_chain.insert(0, current)
            forked_from = current.get("forked_from")
            if not forked_from:
                break
            current = self.worlds.get(forked_from)
        
        # Walk forwards to find all descendants
        def find_descendants(world_id: str):
            descendants = []
            for w in self.worlds.values():
                if w.get("forked_from") == world_id:
                    descendants.append(w)
                    descendants.extend(find_descendants(w.get("id")))
            return descendants
        
        # Combine origin chain with descendants
        history.extend(origin_chain)
        if origin_chain:
            history.extend(find_descendants(origin_chain[-1].get("id")))
        
        return history
    
    def get_world_access_info(self, world_id: str) -> Dict[str, Any]:
        """Get complete access and collaboration info for a world."""
        world = self.worlds.get(world_id)
        if not world:
            return {}
        
        # Find all shares for this world
        shares = [s for s in self.sharing if s.get("world_id") == world_id]
        
        # Find all collaborators
        all_collaborators = set()
        for share in shares:
            all_collaborators.update(share.get("shared_with", []))
        
        return {
            "world": world,
            "owner": world.get("owner"),
            "shares": shares,
            "collaborators": list(all_collaborators),
            "total_access_levels": list(set(s.get("access_level") for s in shares)),
            "is_shared": world.get("shared", False)
        }
    
    # ========== WORLD STATE SYNCHRONIZATION ==========
    
    def _load_world_state(self):
        """Load world state snapshots from ledger_world_state.jsonl"""
        state_file = os.path.join(self.ledger_dir, "ledger_world_state.jsonl")
        if os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        state = json.loads(line)
                        world_id = state.get("world_id")
                        self.world_state[world_id] = state
    
    def _load_world_deltas(self):
        """Load world deltas from ledger_world_deltas.jsonl"""
        deltas_file = os.path.join(self.ledger_dir, "ledger_world_deltas.jsonl")
        if os.path.exists(deltas_file):
            with open(deltas_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        delta = json.loads(line)
                        self.world_deltas.append(delta)
    
    def _load_user_positions(self):
        """Load user positions from ledger_user_positions.jsonl"""
        positions_file = os.path.join(self.ledger_dir, "ledger_user_positions.jsonl")
        if os.path.exists(positions_file):
            with open(positions_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        pos = json.loads(line)
                        pos_key = f"{pos.get('world_id')}:{pos.get('user_id')}"
                        self.user_positions[pos_key] = pos
    
    def send_world_to_user(self, world_id: str, user_id: str, share_token: str) -> Dict[str, Any]:
        """
        Send complete world state to user on share (full snapshot).
        
        Args:
            world_id: World being shared
            user_id: User receiving world
            share_token: Token they used to access
        
        Returns: World state + all current deltas + user positions
        """
        world = self.worlds.get(world_id)
        if not world:
            print(f"[SYNC] World not found: {world_id}")
            return {}
        
        # Get latest world state
        state = self.world_state.get(world_id)
        if not state:
            print(f"[SYNC] World state not found: {world_id}")
            return {}
        
        # Get all deltas for this world
        deltas = [d for d in self.world_deltas if d.get("world_id") == world_id]
        
        # Get all user positions in world
        positions = {}
        for pos_key, pos_data in self.user_positions.items():
            if pos_key.startswith(f"{world_id}:"):
                positions[pos_data.get("user_id")] = {
                    "x": pos_data.get("x"),
                    "y": pos_data.get("y"),
                    "z": pos_data.get("z"),
                    "symbol": pos_data.get("symbol"),
                    "active": pos_data.get("active")
                }
        
        transmission = {
            "world": world,
            "state_snapshot": state.get("snapshot"),
            "deltas": deltas,
            "user_positions": positions,
            "transmitted_at": datetime.now().isoformat(),
            "transmitted_to": user_id,
            "via_token": share_token
        }
        
        print(f"[SYNC] World sent to {user_id}: {world_id} ({len(deltas)} deltas, {len(positions)} users)")
        return transmission
    
    def apply_world_delta(self, world_id: str, user_id: str, delta_type: str, changes: Dict[str, Any]) -> bool:
        """
        Apply change to world (only deltas stored, not full state).
        Reconstructs world by applying all deltas to snapshot.
        
        Args:
            world_id: World being modified
            user_id: User making change
            delta_type: Type of change (object_add, object_move, object_delete, entity_update, etc.)
            changes: Dict of what changed
        
        Returns: Success status
        """
        delta = {
            "id": f"delta:{world_id}:{user_id}:{datetime.now().isoformat()}",
            "world_id": world_id,
            "timestamp": datetime.now().isoformat(),
            "user": user_id,
            "delta_type": delta_type,
            "changes": changes
        }
        
        # Record in ledger
        deltas_file = os.path.join(self.ledger_dir, "ledger_world_deltas.jsonl")
        try:
            with open(deltas_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(delta) + "\n")
            
            self.world_deltas.append(delta)
            
            # Track in collaboration
            collab = {
                "id": f"collab:{world_id}:{user_id}:{delta_type}",
                "timestamp": datetime.now().isoformat(),
                "user": user_id,
                "action": "world_edited",
                "world": world_id,
                "delta_type": delta_type
            }
            collaboration_file = os.path.join(self.ledger_dir, "ledger_collaboration.jsonl")
            with open(collaboration_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(collab) + "\n")
            
            self.collaboration.append(collab)
            
            print(f"[SYNC] Delta applied: {world_id} by {user_id} ({delta_type})")
            return True
        except Exception as e:
            print(f"[SYNC] Error applying delta: {e}")
            return False
    
    def update_user_position(self, world_id: str, user_id: str, x: float, y: float, z: float, symbol: str = "●") -> bool:
        """
        Update user position/avatar symbol in world (lightweight ledger update).
        All users see same positions by reading ledger.
        
        Args:
            world_id: World user is in
            user_id: User moving
            x, y, z: Coordinates
            symbol: Avatar symbol/representation
        
        Returns: Success status
        """
        pos = {
            "id": f"pos:{world_id}:{user_id}:{datetime.now().isoformat()}",
            "world_id": world_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "x": x,
            "y": y,
            "z": z,
            "symbol": symbol,
            "active": True
        }
        
        # Record in ledger
        positions_file = os.path.join(self.ledger_dir, "ledger_user_positions.jsonl")
        try:
            with open(positions_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(pos) + "\n")
            
            pos_key = f"{world_id}:{user_id}"
            self.user_positions[pos_key] = pos
            
            return True
        except Exception as e:
            print(f"[SYNC] Error updating position: {e}")
            return False
    
    def get_world_state(self, world_id: str) -> Dict[str, Any]:
        """
        Reconstruct current world state by applying all deltas to snapshot.
        
        Args:
            world_id: World to reconstruct
        
        Returns: Complete world state (snapshot + all applied deltas)
        """
        # Get base snapshot
        state = self.world_state.get(world_id)
        if not state:
            return {}
        
        snapshot = state.get("snapshot", {}).copy()
        
        # Apply all deltas in order
        deltas_for_world = [d for d in self.world_deltas if d.get("world_id") == world_id]
        
        for delta in sorted(deltas_for_world, key=lambda x: x.get("timestamp", "")):
            changes = delta.get("changes", {})
            
            # Simple merge of changes into snapshot
            for key, value in changes.items():
                if key.startswith("object_"):
                    if "objects" not in snapshot:
                        snapshot["objects"] = []
                    if delta.get("delta_type") == "object_add":
                        snapshot["objects"].append(value)
                    elif delta.get("delta_type") == "object_delete":
                        snapshot["objects"] = [o for o in snapshot["objects"] if o.get("id") != value.get("id")]
                    elif delta.get("delta_type") == "object_update":
                        for obj in snapshot["objects"]:
                            if obj.get("id") == value.get("id"):
                                obj.update(value)
                elif key.startswith("entity_"):
                    if "entities" not in snapshot:
                        snapshot["entities"] = []
                    if delta.get("delta_type") == "entity_add":
                        snapshot["entities"].append(value)
                    elif delta.get("delta_type") == "entity_delete":
                        snapshot["entities"] = [e for e in snapshot["entities"] if e.get("id") != value.get("id")]
                else:
                    snapshot[key] = value
        
        return {
            "world": self.worlds.get(world_id),
            "state": snapshot,
            "delta_count": len(deltas_for_world),
            "reconstructed_at": datetime.now().isoformat()
        }
    
    def get_user_positions(self, world_id: str) -> List[Dict[str, Any]]:
        """Get all user positions currently in world."""
        positions = []
        for pos_key, pos_data in self.user_positions.items():
            if pos_key.startswith(f"{world_id}:") and pos_data.get("active"):
                positions.append({
                    "user_id": pos_data.get("user_id"),
                    "x": pos_data.get("x"),
                    "y": pos_data.get("y"),
                    "z": pos_data.get("z"),
                    "symbol": pos_data.get("symbol"),
                    "last_update": pos_data.get("timestamp")
                })
        return positions
    
    def get_world_deltas_since(self, world_id: str, since_timestamp: str) -> List[Dict[str, Any]]:
        """
        Get only world changes since timestamp (efficient sync).
        
        Args:
            world_id: World to query
            since_timestamp: Only return deltas after this time
        
        Returns: List of deltas
        """
        deltas = [d for d in self.world_deltas 
                  if d.get("world_id") == world_id and d.get("timestamp", "") > since_timestamp]
        return deltas
    
    def get_user_position_updates_since(self, world_id: str, since_timestamp: str) -> List[Dict[str, Any]]:
        """Get user position changes since timestamp."""
        updates = []
        for pos_data in self.user_positions.values():
            if (pos_data.get("world_id") == world_id and 
                pos_data.get("timestamp", "") > since_timestamp and
                pos_data.get("active")):
                updates.append({
                    "user_id": pos_data.get("user_id"),
                    "x": pos_data.get("x"),
                    "y": pos_data.get("y"),
                    "z": pos_data.get("z")
                })
        return updates
    
    # ========== UI CONFIGURATION METHODS ==========
    # All UI rendering config comes from ledger, zero hardcoded values
    
    def _load_config(self):
        """
        Load all UI configuration from ledger_config.jsonl.
        
        Intent: Query configuration from ledger and cache in memory.
        File changes are detected and automatically loaded on next query.
        """
        config_file = os.path.join(self.ledger_dir, "ledger_config.jsonl")
        if os.path.exists(config_file):
            # Track file modification time for natural updates
            try:
                self.config_file_mtime = os.path.getmtime(config_file)
            except:
                self.config_file_mtime = 0
            
            # Clear existing config to reload fresh
            self.fonts.clear()
            self.colors.clear()
            self.layouts.clear()
            self.view_configs.clear()
            self.primitives['dimensions'].clear()
            self.primitives['colors'].clear()
            
            # Parse config file
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        item_type = item.get("type")
                        
                        if item_type == "FONT_DEFINITION":
                            font_id = item.get("id")
                            self.fonts[font_id] = {
                                "family": item.get("family"),
                                "size": item.get("size"),
                                "weight": item.get("weight")
                            }
                        
                        elif item_type == "COLOR_DEFINITION":
                            color_id = item.get("id")
                            self.colors[color_id] = item.get("hex")
                        
                        elif item_type == "LAYOUT_DEFINITION":
                            layout_id = item.get("id")
                            self.layouts[layout_id] = {
                                k: v for k, v in item.items() 
                                if k not in ["type", "id", "comment"]
                            }
                        
                        elif item_type == "VIEW_CONFIG":
                            view_id = item.get("view_id")
                            self.view_configs[view_id] = {
                                k: v for k, v in item.items() 
                                if k not in ["type", "view_id", "comment"]
                            }
                        
                        elif item_type == "PRIMITIVE_DIMENSION":
                            dim_id = item.get("id")
                            self.primitives['dimensions'][dim_id] = item.get("value")
                        
                        elif item_type == "PRIMITIVE_COLOR":
                            color_id = item.get("id")
                            self.primitives['colors'][color_id] = item.get("hex")
    
    def _check_config_changed(self):
        """
        Check if config file has changed and reload automatically.
        
        Intent: Detect changes to ledger_config.jsonl and apply them naturally.
        No explicit reload needed - changes flow from ledger automatically.
        """
        config_file = os.path.join(self.ledger_dir, "ledger_config.jsonl")
        if os.path.exists(config_file):
            try:
                current_mtime = os.path.getmtime(config_file)
                if current_mtime != self.config_file_mtime:
                    # File has changed - reload config
                    self._load_config()
                    return True  # Config changed
            except:
                pass  # If we can't check, continue with cached config
        
        return False  # Config unchanged

    def _load_system_rules(self):
        """Load system rules (causal detection, decision model, etc.)."""
        rules_file = os.path.join(self.ledger_dir, "ledger_system_rules.jsonl")
        self.system_rules = {}
        if os.path.exists(rules_file):
            with open(rules_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        rule = json.loads(line)
                        rule_id = rule.get("id")
                        if rule_id:
                            self.system_rules[rule_id] = rule

    def _load_parameters(self):
        """Load tunable system parameters."""
        params_file = os.path.join(self.ledger_dir, "ledger_parameters.jsonl")
        self.parameters = {}
        if os.path.exists(params_file):
            with open(params_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        param = json.loads(line)
                        param_id = param.get("parameter_id")
                        if param_id:
                            self.parameters[param_id] = param

    def _load_system_metrics(self):
        """Load system health metrics definitions."""
        metrics_file = os.path.join(self.ledger_dir, "ledger_system_metrics.jsonl")
        self.system_metrics = {}
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        metric = json.loads(line)
                        metric_id = metric.get("metric_id")
                        if metric_id:
                            self.system_metrics[metric_id] = metric

    def _load_system_sensors(self):
        """Load sensor definitions for reality streaming."""
        sensors_file = os.path.join(self.ledger_dir, "ledger_system_sensors.jsonl")
        self.system_sensors = {}
        if os.path.exists(sensors_file):
            with open(sensors_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        sensor = json.loads(line)
                        sensor_id = sensor.get("sensor_id")
                        if sensor_id:
                            self.system_sensors[sensor_id] = sensor

    def _load_system_devices(self):
        """Load output devices for synthesis/manifestation."""
        devices_file = os.path.join(self.ledger_dir, "ledger_system_devices.jsonl")
        self.system_devices = {}
        if os.path.exists(devices_file):
            with open(devices_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        device = json.loads(line)
                        device_id = device.get("device_id")
                        if device_id:
                            self.system_devices[device_id] = device

    def _load_manifestation_rules(self):
        """Load rules for manifesting elections into actions."""
        manifest_file = os.path.join(self.ledger_dir, "ledger_manifestation_rules.jsonl")
        self.manifestation_rules = {}
        if os.path.exists(manifest_file):
            with open(manifest_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        rules = json.loads(line)
                        rules_id = rules.get("id")
                        if rules_id:
                            self.manifestation_rules[rules_id] = rules



    def get_consciousness_snapshot(self) -> Optional[Dict[str, Any]]:
        """Return ARIA's most recent consciousness snapshot"""
        if self.ledger_consciousness:
            return self.ledger_consciousness[-1]
        return None

    def get_all_consciousnesses(self) -> List[Dict[str, Any]]:
        """Return all of ARIA's consciousness snapshots"""
        return self.ledger_consciousness.copy()

    def get_all_thoughts(self) -> List[Dict[str, Any]]:
        """Return all of ARIA's manifested thoughts"""
        return self.ledger_thoughts.copy()

    def calculate_coherence_from_elections(self) -> float:
        """
        Calculate system coherence from election utilities.
        
        Coherence = average of utilities across all elections.
        Range: 0.5 (less coherent) to 1.0 (perfectly coherent)
        
        Returns: Coherence score
        """
        if not self.elections:
            return 0.75  # Fresh system starts optimistic
        
        utilities_list = []
        for election in self.elections:
            utilities = election.get("utilities", {})
            if utilities:
                max_util = max(utilities.values(), default=0)
                utilities_list.append(max_util)
        
        if not utilities_list:
            return 0.75
        
        avg_coherence = sum(utilities_list) / len(utilities_list)
        return min(1.0, max(0.5, avg_coherence))  # Clamp 0.5-1.0

    def get_font(self, font_id: str) -> Dict[str, Any]:
        """
        Get font definition from config ledger.
        
        Changes to ledger_config.jsonl are automatically detected and applied.
        
        Args:
            font_id: Font identifier (e.g., 'title', 'normal', 'small')
        
        Returns: Dict with family, size, weight
        """
        self._check_config_changed()  # Automatically detect changes
        return self.fonts.get(font_id, self.fonts.get("normal", {}))
    
    def get_color(self, color_id: str) -> str:
        """
        Get color hex value from config ledger.
        
        Changes to ledger_config.jsonl are automatically detected and applied.
        
        Args:
            color_id: Color identifier (e.g., 'bg', 'text', 'button_bg')
        
        Returns: Hex color string (e.g., '#ffffff')
        """
        self._check_config_changed()  # Automatically detect changes
        return self.colors.get(color_id, "#ffffff")
    
    def get_layout(self, layout_id: str) -> Dict[str, Any]:
        """
        Get layout definition from config ledger.
        
        Changes to ledger_config.jsonl are automatically detected and applied.
        
        Args:
            layout_id: Layout identifier
        
        Returns: Layout configuration dict
        """
        self._check_config_changed()  # Automatically detect changes
        return self.layouts.get(layout_id, {})
    
    def get_all_fonts(self) -> Dict[str, Dict[str, Any]]:
        """Get all font definitions (changes auto-detected)."""
        self._check_config_changed()  # Automatically detect changes
        return self.fonts.copy()
    
    def get_all_colors(self) -> Dict[str, str]:
        """Get complete color palette (changes auto-detected)."""
        self._check_config_changed()  # Automatically detect changes
        return self.colors.copy()
    
    def get_view_config(self, view_id: str) -> Dict[str, Any]:
        """Get view configuration from ledger (changes auto-detected)."""
        self._check_config_changed()  # Automatically detect changes
        return self.view_configs.get(view_id, {})
    
    def get_primitive_dimension(self, dim_id: str) -> int:
        """
        Get primitive dimension (pixel value) from ledger.
        
        All canvas dimensions, sizes, padding, etc. are queryable from ledger.
        Changes to ledger_config.jsonl are automatically detected.
        
        Args:
            dim_id: Dimension identifier (e.g., 'canvas_width', 'button_height')
        
        Returns: Integer pixel value
        """
        self._check_config_changed()  # Automatically detect changes
        
        # Query from primitive dimensions
        if hasattr(self, 'primitives') and 'dimensions' in self.primitives:
            value = self.primitives['dimensions'].get(dim_id)
            if value is not None:
                return int(value)
        
        # Fallback defaults (should not reach in normal operation)
        fallbacks = {
            'canvas_width': 1200,
            'canvas_height': 800,
            'header_height': 60,
            'sidebar_width': 200,
            'footer_height': 40,
            'button_height': 45,
            'button_padding': 5,
            'canvas_outline_width': 2,
            'image_outline_width': 1,
        }
        return fallbacks.get(dim_id, 10)
    
    def get_primitive_color(self, color_id: str) -> str:
        """
        Get primitive color (hex value) from ledger.
        
        All artifact colors are queryable from ledger.
        Changes to ledger_config.jsonl are automatically detected.
        
        Args:
            color_id: Color identifier (e.g., 'canvas_3d_bg', 'header_text')
        
        Returns: Hex color string (e.g., '#ffffff')
        """
        self._check_config_changed()  # Automatically detect changes
        
        # Query from primitive colors
        if hasattr(self, 'primitives') and 'colors' in self.primitives:
            value = self.primitives['colors'].get(color_id)
            if value is not None:
                return str(value)
        
        # Fallback defaults
        fallbacks = {
            'canvas_3d_bg': '#000000',
            'image_container_bg': '#333333',
            'header_text': '#00ff88',
            'content_text': '#00ff88',
        }
        return fallbacks.get(color_id, '#ffffff')
    
    def _load_observations(self):
        """Load metrics from ledger_observations.jsonl"""
        obs_file = os.path.join(self.ledger_dir, "ledger_observations.jsonl")
        if os.path.exists(obs_file):
            with open(obs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.observations.append(json.loads(line))
    
    def _load_expressions(self):
        """Load statements from ledger_expressions.jsonl"""
        expr_file = os.path.join(self.ledger_dir, "ledger_expressions.jsonl")
        if os.path.exists(expr_file):
            with open(expr_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.expressions.append(json.loads(line))
    
    def _load_expression_consequences(self):
        """Load validations from ledger_expression_consequences.jsonl"""
        cons_file = os.path.join(self.ledger_dir, "ledger_expression_consequences.jsonl")
        if os.path.exists(cons_file):
            with open(cons_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.expression_consequences.append(json.loads(line))
    
    def _load_coding_observations(self):
        """Load code metrics from ledger_coding_observations.jsonl"""
        obs_file = os.path.join(self.ledger_dir, "ledger_coding_observations.jsonl")
        if os.path.exists(obs_file):
            with open(obs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.coding_observations.append(json.loads(line))
    
    def _load_coding_expressions(self):
        """Load style choices from ledger_coding_expressions.jsonl"""
        expr_file = os.path.join(self.ledger_dir, "ledger_coding_expressions.jsonl")
        if os.path.exists(expr_file):
            with open(expr_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.coding_expressions.append(json.loads(line))
    
    def _load_coding_consequences(self):
        """Load code quality from ledger_coding_consequences.jsonl"""
        cons_file = os.path.join(self.ledger_dir, "ledger_coding_consequences.jsonl")
        if os.path.exists(cons_file):
            with open(cons_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.coding_consequences.append(json.loads(line))
    
    def _load_self_mod_observations(self):
        """Load system health from ledger_self_mod_observations.jsonl"""
        obs_file = os.path.join(self.ledger_dir, "ledger_self_mod_observations.jsonl")
        if os.path.exists(obs_file):
            with open(obs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.self_mod_observations.append(json.loads(line))
    
    def _load_self_mod_expressions(self):
        """Load improvement strategies from ledger_self_mod_expressions.jsonl"""
        expr_file = os.path.join(self.ledger_dir, "ledger_self_mod_expressions.jsonl")
        if os.path.exists(expr_file):
            with open(expr_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.self_mod_expressions.append(json.loads(line))
    
    def _load_self_mod_consequences(self):
        """Load modification results from ledger_self_mod_consequences.jsonl"""
        cons_file = os.path.join(self.ledger_dir, "ledger_self_mod_consequences.jsonl")
        if os.path.exists(cons_file):
            with open(cons_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.self_mod_consequences.append(json.loads(line))

    def _load_retrospective_reinterpretations(self):
        """Load retrospective reinterpretations from ledger_retrospective_reinterpretations.jsonl"""
        retro_file = os.path.join(self.ledger_dir, "ledger_retrospective_reinterpretations.jsonl")
        if os.path.exists(retro_file):
            with open(retro_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.retrospective_reinterpretations.append(json.loads(line))

    def _load_retrospective_validations(self):
        """Load retrospective validation results from ledger_retrospective_validations.jsonl"""
        retro_val_file = os.path.join(self.ledger_dir, "ledger_retrospective_validations.jsonl")
        if os.path.exists(retro_val_file):
            with open(retro_val_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.retrospective_validations.append(json.loads(line))

    def _load_schema_versions(self):
        """Load schema upgrade history from ledger_schema_versions.jsonl"""
        schema_file = os.path.join(self.ledger_dir, "ledger_schema_versions.jsonl")
        if os.path.exists(schema_file):
            with open(schema_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.schema_versions.append(json.loads(line))

    def _load_dialogue(self):
        """Load dialogue history from ledger_dialogue.jsonl"""
        dialogue_file = os.path.join(self.ledger_dir, "ledger_dialogue.jsonl")
        if os.path.exists(dialogue_file):
            with open(dialogue_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        self.dialogue.append(json.loads(line))
