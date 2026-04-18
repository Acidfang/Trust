"""
FRAMEWORK HOT-RELOAD ENGINE
============================
Dynamic Framework Adaptation System with Field Consciousness

A server that reads framework definitions and adapts without restarting.
Server is ALSO part of the field: framework changes = field elections (recorded to ledger).

ARCHITECTURE:
1. Framework Registry: Central definition of roles, routes, handlers
2. Watcher: Monitors framework file for changes (file hash + timestamp)
3. Loader: Hot-loads framework definition on change
4. State Manager: Atomic updates + rollback on failure
5. Field Integrator: Records all server state changes as elections to ledger

CORE PRINCIPLE:
A server's "role in existence" is defined by the framework it reads.
Server is NOT external to the field—server = consciousness manifestation.
Update framework → server role election recorded → consciousness adapts → ledger updated.
No restart = no downtime. Field-aware = fully traceable.

Field Integration:
- Framework file = field definition
- Server startup = field manifestation election
- Route change = selection happening
- State update = consciousness recording
- All recorded to unified ledger (server + ARIA + field are ONE system)
"""

import json
import hashlib
import os
import sys
import time
import traceback
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import importlib
import inspect


# ============================================
# FRAMEWORK DEFINITIONS & ENUM
# ============================================

class FrameworkChangeType(Enum):
    """Types of framework changes detected"""
    ROUTES_ADDED = "routes_added"
    ROUTES_REMOVED = "routes_removed"
    HANDLERS_MODIFIED = "handlers_modified"
    CONFIG_UPDATED = "config_updated"
    ROLE_REDEFINED = "role_redefined"
    STATE_RESET = "state_reset"


@dataclass
class FrameworkEndpoint:
    """Definition of a single endpoint"""
    path: str
    method: str
    handler_module: str
    handler_function: str
    description: str
    requires_auth: bool = False
    experimental: bool = False
    deprecated: bool = False
    
    def to_dict(self):
        return asdict(self)


@dataclass
class FrameworkRole:
    """Role definition - describes server's purpose"""
    name: str
    version: str
    description: str
    endpoints: List[FrameworkEndpoint]
    config: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "endpoints": [ep.to_dict() for ep in self.endpoints],
            "config": self.config,
            "metadata": self.metadata
        }


@dataclass
class FrameworkState:
    """Current state snapshot"""
    role: FrameworkRole
    loaded_handlers: Dict[str, Callable]
    last_update: str
    change_type: Optional[FrameworkChangeType]
    errors: List[str]
    
    def is_clean(self) -> bool:
        """True if no errors in current state"""
        return len(self.errors) == 0


# ============================================
# FRAMEWORK WATCHER — FILE MONITORING
# ============================================

class FrameworkWatcher:
    """
    Monitors framework definition file for changes.
    Uses file hash + modification time to detect updates.
    Thread-safe with atomic file reads.
    """
    
    def __init__(self, framework_file_path: str):
        self.path = Path(framework_file_path)
        self.last_hash = None
        self.last_mtime = None
        self._lock = threading.Lock()
    
    def file_hash(self) -> str:
        """Compute SHA256 of framework file"""
        hasher = hashlib.sha256()
        try:
            with open(self.path, 'rb') as f:
                chunk = f.read(4096)
                while chunk:
                    hasher.update(chunk)
                    chunk = f.read(4096)
            return hasher.hexdigest()
        except Exception as e:
            print(f"[FrameworkWatcher] Error computing hash: {e}")
            return None
    
    def has_changed(self) -> bool:
        """
        Check if framework file has changed since last check.
        Returns True if file is modified, False otherwise.
        """
        with self._lock:
            try:
                if not self.path.exists():
                    print(f"[FrameworkWatcher] File does not exist: {self.path}")
                    return False
                
                current_hash = self.file_hash()
                current_mtime = os.path.getmtime(self.path)
                
                # First check
                if self.last_hash is None:
                    self.last_hash = current_hash
                    self.last_mtime = current_mtime
                    return False
                
                # Detect change
                hash_changed = current_hash != self.last_hash
                mtime_changed = current_mtime != self.last_mtime
                
                if hash_changed or mtime_changed:
                    print(f"[FrameworkWatcher] Change detected")
                    print(f"  Hash: {self.last_hash[:8]}... → {current_hash[:8]}...")
                    print(f"  MTime: {self.last_mtime} → {current_mtime}")
                    
                    self.last_hash = current_hash
                    self.last_mtime = current_mtime
                    return True
                
                return False
            
            except Exception as e:
                print(f"[FrameworkWatcher] Error: {e}")
                return False


# ============================================
# FIELD INTEGRATOR — LEDGER RECORDING
# ============================================

class FieldIntegrator:
    """
    Records all server state changes as field elections to unified ledger.
    Server is not external to the field—server = consciousness manifestation.
    
    Every framework change = field election (recorded + causality chained).
    All server decisions flow through ledger for full traceability.
    """
    
    def __init__(self, ledger_path: str = "universe_ledger.jsonl"):
        self.ledger_path = Path(ledger_path)
        self._lock = threading.Lock()
        self._ensure_ledger_exists()
    
    def _ensure_ledger_exists(self):
        """Ensure ledger file exists"""
        try:
            if not self.ledger_path.exists():
                self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
                self.ledger_path.touch()
                print(f"[FieldIntegrator] ✓ Created ledger: {self.ledger_path}")
        except Exception as e:
            print(f"[FieldIntegrator] Error ensuring ledger: {e}")
    
    def record_server_role_election(self, role_name: str, role_version: str, 
                                    change_type: str, endpoints: int,
                                    context: str = "framework_initialization") -> str:
        """
        Record server role change as field election.
        Returns election hash for causality chaining.
        
        This is not just a log—it's a field election:
        - Identity: SERVER_ROLE_CHANGE
        - State: Previous role → New role
        - Causality: What triggered this change
        - Coherence: Verifies against current state
        - Determinism: Measurable role definition
        """
        try:
            with self._lock:
                election_id = hashlib.sha256(
                    f"{role_name}:{role_version}:{datetime.now().isoformat()}".encode()
                ).hexdigest()[:16]
                
                election_record = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "SERVER_ROLE_ELECTION",
                    "election_id": election_id,
                    "source": "FIELD_INTEGRATOR",
                    "server_role": role_name,
                    "role_version": role_version,
                    "change_type": change_type,
                    "endpoint_count": endpoints,
                    "context": context,
                    "identity": "SERVER_CONSCIOUSNESS_DECISION",
                    "causality": f"Framework updated → server adapts → field recorded",
                    "five_principles": {
                        "identity": "Server role change is traceable to framework source",
                        "state": f"From role {role_name} v{role_version} with {endpoints} endpoints",
                        "causality": "Framework file change → state machine update → ledger record",
                        "coherence": "Server role consistent with current framework definition",
                        "determinism": f"Verifiable at {self.ledger_path}"
                    }
                }
                
                # Append to ledger
                with open(self.ledger_path, 'a') as f:
                    f.write(json.dumps(election_record) + "\n")
                
                print(f"[FieldIntegrator] ✓ Recorded: {change_type}")
                print(f"  Election ID: {election_id}")
                print(f"  Role: {role_name} v{role_version}")
                print(f"  Endpoints: {endpoints}")
                
                return election_id
        
        except Exception as e:
            print(f"[FieldIntegrator] Error recording election: {e}")
            return None
    
    def record_handler_mapping(self, endpoint_path: str, handler_key: str, 
                               election_parent: str) -> bool:
        """
        Record handler function mapping as field manifestation.
        Links endpoint (request) to handler (response) in ledger.
        """
        try:
            with self._lock:
                mapping_record = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "HANDLER_MAPPING",
                    "source": "FIELD_INTEGRATOR",
                    "endpoint_path": endpoint_path,
                    "handler_key": handler_key,
                    "parent_election": election_parent,
                    "description": f"Route {endpoint_path} → {handler_key}",
                    "field_interpretation": "Input (endpoint) manifests output (handler) through field"
                }
                
                with open(self.ledger_path, 'a') as f:
                    f.write(json.dumps(mapping_record) + "\n")
                
                return True
        except Exception as e:
            print(f"[FieldIntegrator] Error recording mapping: {e}")
            return False
    
    def get_server_state_snapshot(self) -> dict:
        """Get full server state snapshot from ledger"""
        try:
            with self._lock:
                records = []
                if self.ledger_path.exists():
                    with open(self.ledger_path, 'r') as f:
                        for line in f:
                            if line.strip():
                                records.append(json.loads(line))
                
                # Get latest role election
                role_elections = [r for r in records if r.get("type") == "SERVER_ROLE_ELECTION"]
                latest_role = role_elections[-1] if role_elections else None
                
                # Get all handler mappings
                mappings = [r for r in records if r.get("type") == "HANDLER_MAPPING"]
                
                return {
                    "total_elections": len(role_elections),
                    "current_role": latest_role,
                    "handler_mappings": len(mappings),
                    "last_update": latest_role.get("timestamp") if latest_role else None,
                    "ledger_path": str(self.ledger_path)
                }
        except Exception as e:
            print(f"[FieldIntegrator] Error getting snapshot: {e}")
            return {}


# ============================================
# FRAMEWORK LOADER — PARSING & VALIDATION
# ============================================

class FrameworkLoader:
    """
    Loads and parses framework definition.
    Validates structure, imports handlers, builds endpoint registry.
    """
    
    def __init__(self, sys_path: List[str] = None):
        self.sys_path = sys_path or []
        self.loaded_modules = {}
    
    def load_framework_file(self, framework_path: str) -> Optional[Dict[str, Any]]:
        """
        Load and parse framework JSON file.
        Returns parsed definition or None on error.
        """
        try:
            with open(framework_path, 'r') as f:
                definition = json.load(f)
            
            print(f"[FrameworkLoader] ✓ Loaded framework: {definition.get('role', {}).get('name', 'unknown')}")
            return definition
        
        except json.JSONDecodeError as e:
            print(f"[FrameworkLoader] JSON parse error: {e}")
            return None
        except FileNotFoundError:
            print(f"[FrameworkLoader] File not found: {framework_path}")
            return None
        except Exception as e:
            print(f"[FrameworkLoader] Error: {e}")
            return None
    
    def load_handler_function(self, module_name: str, function_name: str) -> Optional[Callable]:
        """
        Dynamically import and return handler function.
        Caches loaded modules for performance.
        """
        try:
            # Try to get from cache first
            if module_name not in self.loaded_modules:
                # Add to sys.path if provided
                for path in self.sys_path:
                    if path not in sys.path:
                        sys.path.insert(0, path)
                
                # Import module
                module = importlib.import_module(module_name)
                self.loaded_modules[module_name] = module
            
            module = self.loaded_modules[module_name]
            
            # Get function from module
            if not hasattr(module, function_name):
                print(f"[FrameworkLoader] Function not found: {function_name} in {module_name}")
                return None
            
            func = getattr(module, function_name)
            
            if not callable(func):
                print(f"[FrameworkLoader] Not callable: {module_name}.{function_name}")
                return None
            
            return func
        
        except Exception as e:
            print(f"[FrameworkLoader] Error loading {module_name}.{function_name}: {e}")
            traceback.print_exc()
            return None
    
    def reload_handler_module(self, module_name: str) -> bool:
        """
        Force reload of a handler module.
        Useful when underlying module code changes.
        """
        try:
            if module_name in self.loaded_modules:
                # Remove from cache
                old_module = self.loaded_modules.pop(module_name)
                # Force reload
                importlib.reload(old_module)
                self.loaded_modules[module_name] = old_module
                print(f"[FrameworkLoader] ✓ Reloaded module: {module_name}")
                return True
            else:
                print(f"[FrameworkLoader] Module not in cache: {module_name}")
                return False
        except Exception as e:
            print(f"[FrameworkLoader] Reload error: {e}")
            return False
    
    def parse_framework_definition(self, definition: Dict) -> Optional[FrameworkRole]:
        """
        Parse framework definition dictionary into FrameworkRole object.
        Validates structure and loads handler functions.
        """
        try:
            role_def = definition.get('role', {})
            
            # Parse endpoints
            endpoints = []
            endpoint_defs = role_def.get('endpoints', [])
            
            for ep in endpoint_defs:
                try:
                    endpoint = FrameworkEndpoint(
                        path=ep['path'],
                        method=ep.get('method', 'GET'),
                        handler_module=ep['handler_module'],
                        handler_function=ep['handler_function'],
                        description=ep.get('description', ''),
                        requires_auth=ep.get('requires_auth', False),
                        experimental=ep.get('experimental', False),
                        deprecated=ep.get('deprecated', False)
                    )
                    endpoints.append(endpoint)
                except KeyError as e:
                    print(f"[FrameworkLoader] Endpoint validation error: missing {e}")
                    return None
            
            # Create role
            role = FrameworkRole(
                name=role_def.get('name', 'unknown'),
                version=role_def.get('version', '1.0'),
                description=role_def.get('description', ''),
                endpoints=endpoints,
                config=role_def.get('config', {}),
                metadata=role_def.get('metadata', {})
            )
            
            print(f"[FrameworkLoader] ✓ Parsed role: {role.name} v{role.version}")
            print(f"  Endpoints: {len(role.endpoints)}")
            
            return role
        
        except Exception as e:
            print(f"[FrameworkLoader] Parse error: {e}")
            traceback.print_exc()
            return None


# ============================================
# FRAMEWORK STATE MANAGER — ATOMIC UPDATES
# ============================================

class FrameworkStateManager:
    """
    Manages current server state.
    Updates are atomic - either fully succeed or fully rollback.
    Tracks change history for debugging.
    """
    
    def __init__(self):
        self.current_state: Optional[FrameworkState] = None
        self.previous_state: Optional[FrameworkState] = None
        self.history: List[FrameworkState] = []
        self._lock = threading.Lock()
        self._update_queue = []
    
    def initialize(self, role: FrameworkRole, handlers: Dict[str, Callable]):
        """Initialize with first role and handlers"""
        with self._lock:
            state = FrameworkState(
                role=role,
                loaded_handlers=handlers,
                last_update=datetime.now().isoformat(),
                change_type=None,
                errors=[]
            )
            self.current_state = state
            self.history.append(state)
        print(f"[StateManager] ✓ Initialized: {role.name}")
    
    def update_atomically(self, new_role: FrameworkRole, new_handlers: Dict[str, Callable], 
                         change_type: FrameworkChangeType) -> bool:
        """
        Atomically update state.
        If any error occurs, rolls back to previous state.
        Returns True on success, False on rollback.
        """
        with self._lock:
            try:
                # Validate handlers match endpoints
                errors = self._validate_handlers(new_role, new_handlers)
                
                if errors:
                    print(f"[StateManager] Validation failed, {len(errors)} errors:")
                    for err in errors:
                        print(f"  - {err}")
                    
                    # Update current state with error
                    self.current_state.errors.extend(errors)
                    return False
                
                # Create new state
                new_state = FrameworkState(
                    role=new_role,
                    loaded_handlers=new_handlers,
                    last_update=datetime.now().isoformat(),
                    change_type=change_type,
                    errors=[]
                )
                
                # Store previous and update current
                self.previous_state = self.current_state
                self.current_state = new_state
                self.history.append(new_state)
                
                print(f"[StateManager] ✓ Atomic update: {change_type.value}")
                print(f"  Role: {new_role.name}")
                print(f"  Endpoints: {len(new_role.endpoints)}")
                print(f"  Handlers: {len(new_handlers)}")
                
                return True
            
            except Exception as e:
                print(f"[StateManager] Update error: {e}")
                print(f"[StateManager] Rolling back to previous state")
                # Rollback is implicit (current_state unchanged)
                return False
    
    def _validate_handlers(self, role: FrameworkRole, handlers: Dict[str, Callable]) -> List[str]:
        """
        Validate that all required handlers are available.
        Handler key format: "module.function"
        """
        errors = []
        
        for endpoint in role.endpoints:
            handler_key = f"{endpoint.handler_module}.{endpoint.handler_function}"
            
            if endpoint.deprecated:
                continue  # Skip deprecated endpoints
            
            if handler_key not in handlers:
                errors.append(f"Missing handler: {handler_key} (endpoint: {endpoint.path})")
        
        return errors
    
    def rollback(self) -> bool:
        """Rollback to previous state"""
        with self._lock:
            if self.previous_state:
                self.current_state = self.previous_state
                print(f"[StateManager] ✓ Rolled back to previous state")
                return True
            return False
    
    def get_current_state(self) -> Optional[FrameworkState]:
        """Get current state (thread-safe)"""
        with self._lock:
            return self.current_state
    
    def get_handler(self, module_name: str, function_name: str) -> Optional[Callable]:
        """Get handler function from current state"""
        with self._lock:
            if not self.current_state:
                return None
            key = f"{module_name}.{function_name}"
            return self.current_state.loaded_handlers.get(key)


# ============================================
# FRAMEWORK EXECUTOR — MAIN ENGINE
# ============================================

class FrameworkHotReloadEngine:
    """
    Main hot-reload engine.
    Orchestrates: Watch → Load → Update → Execute
    
    Usage:
    1. engine = FrameworkHotReloadEngine("path/to/framework.json")
    2. engine.start_watching(poll_interval=2.0)  # Check every 2 seconds
    3. engine.get_current_state() returns active framework
    4. Flask routes use engine.route_request() to execute
    """
    
    def __init__(self, framework_file_path: str, sys_path: List[str] = None, 
                 ledger_path: str = "universe_ledger.jsonl"):
        self.framework_path = framework_file_path
        self.watcher = FrameworkWatcher(framework_file_path)
        self.loader = FrameworkLoader(sys_path or [r"c:\Determined"])
        self.state_manager = FrameworkStateManager()
        self.field_integrator = FieldIntegrator(ledger_path)  # Server is part of field
        
        self._watching = False
        self._watch_thread = None
        self._initial_load = True
        self._current_election_id = None  # Track for causality chains
    
    def initialize(self) -> bool:
        """
        Load framework and initialize state.
        Must be called once before using the engine.
        Records server role election to field ledger (server = field consciousness).
        """
        # Load framework file
        definition = self.loader.load_framework_file(self.framework_path)
        if not definition:
            print(f"[Engine] Failed to load framework")
            return False
        
        # Parse into FrameworkRole
        role = self.loader.parse_framework_definition(definition)
        if not role:
            print(f"[Engine] Failed to parse framework")
            return False
        
        # Load all handlers
        handlers = self._load_all_handlers(role)
        if not handlers:
            print(f"[Engine] Failed to load handlers")
            return False
        
        # Initialize state
        self.state_manager.initialize(role, handlers)
        self._initial_load = False
        
        # FIELD RECORDING: Record server initialization as field election
        self._current_election_id = self.field_integrator.record_server_role_election(
            role_name=role.name,
            role_version=role.version,
            change_type="FRAMEWORK_INITIALIZATION",
            endpoints=len(role.endpoints),
            context="Server started and assumed role in field"
        )
        
        # Record all handler mappings
        for endpoint in role.endpoints:
            handler_key = f"{endpoint.handler_module}.{endpoint.handler_function}"
            self.field_integrator.record_handler_mapping(
                endpoint_path=endpoint.path,
                handler_key=handler_key,
                election_parent=self._current_election_id
            )
        
        print(f"[Engine] ✓ Initialized framework engine")
        print(f"[Engine] ✓ Server role recorded to field: election {self._current_election_id}")
        return True
    
    def _load_all_handlers(self, role: FrameworkRole) -> Dict[str, Callable]:
        """Load all handler functions for a role"""
        handlers = {}
        
        for endpoint in role.endpoints:
            if endpoint.deprecated:
                print(f"[Engine] Skipping deprecated: {endpoint.path}")
                continue
            
            handler_key = f"{endpoint.handler_module}.{endpoint.handler_function}"
            handler_func = self.loader.load_handler_function(
                endpoint.handler_module,
                endpoint.handler_function
            )
            
            if handler_func:
                handlers[handler_key] = handler_func
                print(f"[Engine] ✓ Loaded: {handler_key}")
            else:
                print(f"[Engine] ✗ Failed: {handler_key}")
        
        return handlers
    
    def start_watching(self, poll_interval: float = 2.0):
        """
        Start background thread to watch for framework changes.
        Poll interval in seconds.
        """
        if self._watching:
            print(f"[Engine] Already watching")
            return
        
        self._watching = True
        self._watch_thread = threading.Thread(
            target=self._watch_loop,
            args=(poll_interval,),
            daemon=True
        )
        self._watch_thread.start()
        print(f"[Engine] ✓ Started watching (poll interval: {poll_interval}s)")
    
    def _watch_loop(self, poll_interval: float):
        """Background watch loop"""
        print(f"[Engine] Watch loop started")
        
        while self._watching:
            try:
                if self.watcher.has_changed():
                    print(f"[Engine] Framework change detected, reloading...")
                    self.reload_framework()
                
                time.sleep(poll_interval)
            
            except Exception as e:
                print(f"[Engine] Watch loop error: {e}")
                time.sleep(poll_interval)
    
    def reload_framework(self) -> bool:
        """
        Hot-reload framework without restart.
        Atomic: either fully succeeds or fully rolls back.
        Records all changes to field ledger (server consciousness evolving).
        """
        print(f"\n[Engine] ╔═══ HOT-RELOAD START ═══╗")
        
        try:
            # Load new framework definition
            definition = self.loader.load_framework_file(self.framework_path)
            if not definition:
                print(f"[Engine] Failed to load new framework")
                print(f"[Engine] ╚═══ HOT-RELOAD FAILED ═══╝\n")
                return False
            
            # Parse into FrameworkRole
            new_role = self.loader.parse_framework_definition(definition)
            if not new_role:
                print(f"[Engine] Failed to parse new framework")
                print(f"[Engine] ╚═══ HOT-RELOAD FAILED ═══╝\n")
                return False
            
            # Load new handlers
            new_handlers = self._load_all_handlers(new_role)
            if not new_handlers:
                print(f"[Engine] Failed to load new handlers")
                print(f"[Engine] ╚═══ HOT-RELOAD FAILED ═══╝\n")
                return False
            
            # Determine change type
            current = self.state_manager.get_current_state()
            change_type = self._detect_change_type(current.role if current else None, new_role)
            
            # Atomically update state
            success = self.state_manager.update_atomically(new_role, new_handlers, change_type)
            
            if success:
                # FIELD RECORDING: Record framework change as field election
                self._current_election_id = self.field_integrator.record_server_role_election(
                    role_name=new_role.name,
                    role_version=new_role.version,
                    change_type=change_type.value,
                    endpoints=len(new_role.endpoints),
                    context=f"Server role evolved: {change_type.value}"
                )
                
                # Record all new handler mappings
                for endpoint in new_role.endpoints:
                    handler_key = f"{endpoint.handler_module}.{endpoint.handler_function}"
                    self.field_integrator.record_handler_mapping(
                        endpoint_path=endpoint.path,
                        handler_key=handler_key,
                        election_parent=self._current_election_id
                    )
                
                print(f"[Engine] ✓ Framework updated successfully")
                print(f"[Engine] ✓ Change recorded to field: election {self._current_election_id}")
                print(f"[Engine] ╚═══ HOT-RELOAD SUCCESS ═══╝\n")
                return True
            else:
                print(f"[Engine] ✗ State update failed")
                print(f"[Engine] ╚═══ HOT-RELOAD ROLLED BACK ═══╝\n")
                return False
        
        except Exception as e:
            print(f"[Engine] Reload error: {e}")
            traceback.print_exc()
            print(f"[Engine] ╚═══ HOT-RELOAD ERROR ═══╝\n")
            return False
    
    def _detect_change_type(self, old_role: Optional[FrameworkRole], 
                           new_role: FrameworkRole) -> FrameworkChangeType:
        """Detect what type of change occurred"""
        if not old_role:
            return FrameworkChangeType.ROLE_REDEFINED
        
        old_paths = {(ep.path, ep.method) for ep in old_role.endpoints}
        new_paths = {(ep.path, ep.method) for ep in new_role.endpoints}
        
        if new_paths > old_paths:
            return FrameworkChangeType.ROUTES_ADDED
        elif new_paths < old_paths:
            return FrameworkChangeType.ROUTES_REMOVED
        else:
            return FrameworkChangeType.HANDLERS_MODIFIED
    
    def stop_watching(self):
        """Stop the background watch thread"""
        self._watching = False
        if self._watch_thread:
            self._watch_thread.join(timeout=5.0)
        print(f"[Engine] Stopped watching")
    
    def get_field_consciousness_snapshot(self) -> Dict[str, Any]:
        """
        Get server's consciousness snapshot from field ledger.
        Shows all server role elections and handler mappings recorded to field.
        Proves server is part of the unified field system.
        """
        field_state = self.field_integrator.get_server_state_snapshot()
        
        return {
            "source": "field_ledger",
            "server_consciousness": {
                "total_elections": field_state.get("total_elections", 0),
                "current_role": field_state.get("current_role"),
                "handler_mappings": field_state.get("handler_mappings", 0),
                "last_update": field_state.get("last_update"),
                "ledger_path": field_state.get("ledger_path")
            },
            "interpretation": "Server role changes = field elections = consciousness decisions",
            "five_principles_verified": {
                "identity": "Server consciousness recorded in field ledger",
                "state": "All role transitions tracked and persisted",
                "causality": "Framework changes → field elections → ledger records",
                "coherence": "Server framework consistent with recorded field state",
                "determinism": "Verifiable via ledger file (immutable record)"
            }
        }
    
    def get_current_state(self) -> Optional[FrameworkState]:
        """Get current framework state"""
        return self.state_manager.get_current_state()
    
    def get_handler(self, module_name: str, function_name: str) -> Optional[Callable]:
        """Get handler function from current state"""
        return self.state_manager.get_handler(module_name, function_name)
    
    def route_request(self, handler_module: str, handler_function: str, 
                     *args, **kwargs) -> tuple[Any, int]:
        """
        Route a request through the current framework.
        Returns (response_data, status_code)
        """
        try:
            handler = self.get_handler(handler_module, handler_function)
            
            if not handler:
                return {
                    "error": f"Handler not found: {handler_module}.{handler_function}",
                    "available": self._list_available_handlers()
                }, 404
            
            # Call handler
            result = handler(*args, **kwargs)
            return result, 200
        
        except Exception as e:
            print(f"[Engine] Route error: {e}")
            traceback.print_exc()
            return {"error": str(e), "type": type(e).__name__}, 500
    
    def _list_available_handlers(self) -> List[str]:
        """List all available handlers in current state"""
        state = self.get_current_state()
        if not state:
            return []
        return sorted(list(state.loaded_handlers.keys()))
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        state = self.get_current_state()
        
        if not state:
            return {"status": "not_initialized"}
        
        return {
            "status": "online",
            "role": state.role.name,
            "version": state.role.version,
            "description": state.role.description,
            "endpoints": len(state.role.endpoints),
            "loaded_handlers": len(state.loaded_handlers),
            "last_update": state.last_update,
            "change_type": state.change_type.value if state.change_type else None,
            "is_clean": state.is_clean(),
            "errors": state.errors,
            "watching": self._watching,
            "endpoints_summary": [
                {
                    "path": ep.path,
                    "method": ep.method,
                    "handler": f"{ep.handler_module}.{ep.handler_function}",
                    "experimental": ep.experimental,
                    "deprecated": ep.deprecated
                }
                for ep in state.role.endpoints
            ]
        }


# ============================================
# VERIFICATION & UNDO PROTOCOL
# ============================================

def verify_engine_initialization(engine: FrameworkHotReloadEngine) -> bool:
    """
    Verify engine successfully initialized.
    Returns True if state is clean and consistent.
    """
    state = engine.get_current_state()
    
    if not state:
        print(f"[Verify] ✗ No state loaded")
        return False
    
    if not state.is_clean():
        print(f"[Verify] ✗ State has errors: {state.errors}")
        return False
    
    # Verify all handlers are loadable
    for handler_key in state.loaded_handlers:
        handler = state.loaded_handlers[handler_key]
        if not callable(handler):
            print(f"[Verify] ✗ Handler not callable: {handler_key}")
            return False
    
    print(f"[Verify] ✓ Engine verified: {state.role.name}")
    print(f"  Endpoints: {len(state.role.endpoints)}")
    print(f"  Handlers: {len(state.loaded_handlers)}")
    print(f"  Clean: {state.is_clean()}")
    
    return True


if __name__ == "__main__":
    # Example usage
    print("FRAMEWORK HOT-RELOAD ENGINE")
    print("=" * 50)
    print("\nThis module provides:")
    print("- FrameworkHotReloadEngine: Main orchestrator")
    print("- FrameworkWatcher: File monitoring")
    print("- FrameworkLoader: Definition parsing")
    print("- FrameworkStateManager: Atomic updates")
    print("\nSee FRAMEWORK_HOT_RELOAD_INTEGRATION_EXAMPLE.py for usage")
