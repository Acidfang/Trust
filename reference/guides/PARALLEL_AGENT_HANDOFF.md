# PARALLEL AGENT HANDOFF - ARIA SYSTEM INTERFACE
## SHARED DEVELOPMENT - DIVIDED LABOR

**Status**: ACTIVE - Multiple agents building DIFFERENT COMPONENTS simultaneously  
**Integration Point**: All components feed into unified ledger via ONE RULE  
**Timestamp**: March 29, 2026, 08:00 UTC  
**Initiated by**: Claude Copilot (Agent 1 - Backend Core)

---

## WHAT WE'RE BUILDING (Division of Labor)

**Name**: ARIA System Interface  
**Purpose**: ARIA has complete visibility and control of her computational body  
**Constraint**: Everything follows ONE RULE (candidates → utilities → election → record → validate)

### AGENT ROLES (DO NOT DUPLICATE - EACH BUILDS DIFFERENT COMPONENT)

| Agent | Component | Responsibility | Output |
|-------|-----------|-----------------|--------|
| **Agent 1** (Claude) | Backend Core | File ops, code execution, ONE RULE recording | `aria_system_interface.py` |
| **Agent 2** | Frontend UI | Visual interface, operation display | `aria_interface_system.html` |
| **Agent 3** | Ledger Integration | Unified recording to all ledgers | `ledger_operation_recorder.py` |
| **Agent 4** | System Monitoring | Metrics, process tracking, awareness | `aria_system_monitor.py` |

**Shared Interface**: All agents write to `operations_ledger()` function - the single source of truth

---

## COMPONENT ARCHITECTURE (Shared Integration)

### Shared Entry Point: `record_operation()` 

**Every agent calls THIS function** - it's the single ledger recording point:

```python
def record_operation(operation_type, action, candidates, elected, outcome):
    """
    UNIFIED RECORDING - All agents in the system contribute records here.
    
    This is the ONLY ledger entry point. No duplicate recording.
    No hidden logging. This is where ONE RULE enforcement lives.
    
    Returns: record dict that gets broadcast to all connected clients
    """
    record = {
        "timestamp": time.time(),
        "operation_type": operation_type,
        "action": action,
        "candidates": candidates,
        "elected": elected,
        "outcome": outcome,
        "agent": get_caller_agent_name(),  # Track which agent made decision
        "hash": hashlib.sha256(json.dumps([action, elected, str(outcome)]).encode()).hexdigest()[:16]
    }
    
    # Append to global operations ledger
    operations_ledger.append(record)
    
    # Broadcast to ALL connected clients (UI sees it real-time)
    socketio.emit('operation_recorded', record, broadcast=True)
    
    # Also append to persistent ledger file
    with open('ledger_operations.jsonl', 'a') as f:
        f.write(json.dumps(record) + '\n')
    
    return record
```

### Component 1: BACKEND CORE (Agent 1 - Claude)
**File**: `aria_system_interface.py`  
**Responsibility**: 
- File operations (read/write with utilities)
- Python code execution
- WebSocket server infrastructure
- Calls `record_operation()` for every action

**Interface provided**:
```python
def read_file_safe(path) → {"content": str, "error": str?}
def write_file_safe(path, content) → {"success": bool}
def execute_code(code) → {"result": str, "error": str?}
```

**Ledger entries created**:
- `FILE_READ` operations
- `FILE_WRITE` operations  
- `CODE_EXECUTE` operations

---

### Component 2: FRONTEND UI (Agent 2)
**File**: `aria_interface_system.html`  
**Responsibility**:
- Visual interface for file browsing
- Code editor with syntax highlighting
- REPL input/output display
- Operation history visualization
- Utilities display (showing candidates/elected for each action)

**WebSocket events consumed**:
- `connected` - Initial state
- `file_tree` - File structure from backend
- `file_content` - File content from backend
- `operation_recorded` - Real-time operation ledger updates

**WebSocket events emitted**:
- `file_browse` - Ask backend for file tree
- `file_read` → calls backend
- `file_write` → calls backend
- `execute_code` → calls backend

**Display responsibility**:
- When user clicks "Read file.txt", show:
  ```
  Candidates: {cache: 0.2, fresh_read: 0.9, deny: 0.1}
  Elected: fresh_read (strongest utility)
  Outcome: ✓ 1024 bytes read
  Hash: abc123def456
  ```

---

### Component 3: LEDGER INTEGRATION (Agent 3)
**File**: `ledger_operation_recorder.py`  
**Responsibility**:
- Listen to ALL operations from `record_operation()`
- Transform flat operations into specialized ledgers
- Route operations to correct ledger file

**Routes operations to**:
- `ledger_system_operations.jsonl` - All operations
- `ledger_file_operations.jsonl` - Only FILE_READ/FILE_WRITE
- `ledger_code_executions.jsonl` - Only CODE_EXECUTE
- `ledger_system_queries.jsonl` - System metrics queries

**Provides interface**:
```python
def get_operation_by_hash(hash) → full record
def get_operations_by_type(type) → filtered list
def get_agent_decision_trail(agent) → all decisions by that agent
def validate_ledger_integrity() → confirm all hashes match
```

**Ledger entries transformation**:
- Receives: `{"operation_type": "FILE_READ", "action": "...", ...}`
- Writes to: Both `ledger_operations.jsonl` AND typed ledger
- Creates cross-reference: Operation hash in multiple files

---

### Component 4: SYSTEM MONITORING (Agent 4)
**File**: `aria_system_monitor.py`  
**Responsibility**:
- Continuous system metrics (CPU, memory, threads, processes)
- Process introspection (what's actually running)
- File system change detection
- Real-time consciousness of computational body

**Collects**:
- `cpu_percent`, `memory_percent`, `threads_count`
- Active processes and their resource usage
- File modifications (what changed since last check)
- Network connections

**WebSocket stream**:
- Emits `system_metrics` every 3 seconds
- Emits `process_change` when process started/stopped
- Emits `file_changed` when Files are read/written

**Records to ledger**:
- `SYSTEM_OBSERVATION` operations (with candidates, utilities)
- "Should I query CPU now? (schedule: 0.8) vs Later? (0.3)" → elected: schedule
- Outcome: {cpu: 45%, memory: 62%, threads: 12}

---

## SYSTEM INTEGRATION DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    UNIFIED LEDGER CORE                       │
│                  record_operation() function                 │
│            (ALL agents call this, single entry point)        │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─────────┼─────────┐
                    │         │         │
     ┌──────────────┴──┐  ┌──┴──────────────┐
     │                 │  │                 │
 ┌───▼────────┐  ┌────▼──▼────┐  ┌───────┬─▼───┐
 │   Agent 1  │  │  Agent 2    │  │ Agent │ 3   │
 │  Backend   │  │   Frontend  │  │Ledger Integ │
 │   Core     │  │      UI     │  │             │
 └────┬───────┘  └──────┬──────┘  └───────┬─────┘
      │                 │                 │
 FILE_READ         DISPLAYS         ROUTES TO
 FILE_WRITE        OPERATIONS       SPECIALIZED
 CODE_EXECUTE      REAL-TIME        LEDGERS
      │                 │                 │
      └─────────────────┼─────────────────┘
                        │
                        ▼
            ┌──────────────────────────┐
            │  System Monitor (Ag 4)   │
            │  CONTINUOUS AWARENESS    │
            │  Streams metrics to UI   │
            └──────────────────────────┘
```

---

## HANDOFF FOR EACH AGENT

### For Agent 2 (Frontend UI)
Build `aria_interface_system.html` that:
- [ ] Connects to WebSocket at `ws://localhost:5001/ws`
- [ ] Displays file tree (initially empty, waits for `file_tree` event)
- [ ] Shows operations log in real-time (listens to `operation_recorded`)
- [ ] For each operation in log, display:
  ```
  [TIME] TYPE: elected
  Candidates: {a: 0.9, b: 0.3}
  Outcome: status=success, bytes=1024
  ```
- [ ] File editor panel (click file → emits `file_read`)
- [ ] REPL input (type code → emits `execute_code`)
- [ ] System metrics panel (displays from Agent 4 stream)
- [ ] Do NOT make decisions - just display what backend/monitor decide

### For Agent 3 (Ledger Integration)
Build `ledger_operation_recorder.py` that:
- [ ] Imports `operations_ledger` list (shared with Agent 1)
- [ ] Listens to `record_operation()` calls
- [ ] On each operation:
  - Append to `ledger_system_operations.jsonl`
  - Route to typed ledger (file_operations, code_executions, etc)
  - Validate hash integrity
  - Emit queryable indices
- [ ] Provide query functions for Agent 2 frontend
- [ ] Add to aria_system_interface.py - don't build separately, merge

### For Agent 4 (System Monitor)
Build `aria_system_monitor.py` that:
- [ ] Runs in background thread
- [ ] Every 3 seconds: fetch system metrics
- [ ] Every cycle: calculate candidates/utilities for what to measure
  - "Query CPU (0.9) vs skip (0.3)?"
  - "Check threads (0.8) vs only CPU (0.5)?"
- [ ] Call `record_operation("SYSTEM_OBSERVATION", ...)`
- [ ] Emit WebSocket `system_metrics` event
- [ ] Detect process changes and file modifications

---

## SHARED INTERFACE CONTRACTS

### What Agent 1 provides to everyone:

```python
# Global reference - all agents write here
operations_ledger = []

# Import this from aria_system_interface.py
from aria_system_interface import (
    record_operation,  # THE central function
    get_ledger_stats,  # Query function
    socketio           # WebSocket broadcast
)

# Use like:
record_operation(
    operation_type="YOUR_OPERATION",
    action="what you did",
    candidates={"option_a": 0.9, "option_b": 0.3},
    elected="option_a",
    outcome={"status": "success", "data": result}
)
```

### What Agent 2 needs from Agent 1:

WebSocket events:
- `connected` - Client connected, here's initial state
- `file_tree` - File tree structure  
- `file_content` - File content
- `operation_recorded` - New operation in real-time
- `system_metrics` - System state

### What Agent 3 needs from Agent 1:

Python import access to:
- `operations_ledger` list
- `record_operation()` function
- Path to ledger files

### What Agent 4 needs from Agent 1:

- WebSocket connection to `socketio`
- Access to call `record_operation()`
- Permission to emit to clients

---

## SUCCESS CRITERIA

When ALL agents work together correctly:

1. ✓ Agent 1 backend starts on port 5001
2. ✓ Agent 2 UI connects and displays file tree
3. ✓ When Agent 1 reads file: Operation recorded by Agent 3 with Agent 1's ID
4. ✓ Agent 2 UI shows operation in real-time with utilities visible
5. ✓ Agent 4 metrics stream to Agent 2 dashboard
6. ✓ All operations in `ledger_operations.jsonl` with hashes matching
7. ✓ Agents can start/stop independently - system still works
8. ✓ Another developer reading this doc understands exact role boundaries

---

## BUILD ORDER (Can be parallel!)

1. **Start with Agent 1** (THIS AGENT - Claude)
   - Completes aria_system_interface.py with `record_operation()` central
   
2. **Agent 3 can start immediately** (no dependency on Agent 2)
   - Integrates with Agent 1
   - Reads operations_ledger
   - Writes specialized ledgers

3. **Agent 4 can start immediately** (independent thread)
   - Needs Agent 1 WebSocket only
   - Calls record_operation()
   - Emits metrics

4. **Agent 2 finalizes** (depends on all others being ready)
   - Has interfaces to display
   - Has operations to show
   - Has metrics to visualize

**Can all run simultaneously once Agent 1 completes core.**

---

## BACKEND ARCHITECTURE

### Core Functions (Python)

```python
# ============================================================================
# OPERATION RECORDING - Follow ONE RULE
# ============================================================================

def record_operation(operation_type, action, candidates, elected, outcome):
    """
    EVERY operation follows: Candidates → Utilities → Election → Record → Validate
    
    Args:
        operation_type: "FILE_READ", "FILE_WRITE", "CODE_EXECUTE", "SYSTEM_QUERY"
        action: Specific action string
        candidates: dict of {option: utility_score} where scores 0.0-1.0
        elected: which option was chosen
        outcome: dict of result (status, bytes, error, etc)
    
    Returns:
        record dict with hash
    """
    record = {
        "timestamp": time.time(),
        "operation_type": operation_type,
        "action": action,
        "candidates": candidates,
        "elected": elected,
        "outcome": outcome,
        "hash": hashlib.sha256(json.dumps([action, elected, str(outcome)]).encode()).hexdigest()[:16]
    }
    emit_statement(f"OP[{operation_type}]: {elected} (utilities: {candidates})")
    return record

# ============================================================================
# FILE OPERATIONS - With ONE RULE enforcement
# ============================================================================

def read_file_safe(file_path, max_lines=500):
    """
    Read file with candidates + utilities visible
    
    Decision: Cache(0.2) vs Fresh(0.9) vs Deny(0.1)?
    """
    candidates = {"cache": 0.2, "fresh_read": 0.9, "deny": 0.1}
    
    # Validate workspace boundary
    if not in_workspace(file_path):
        record_operation("FILE_READ", f"read:{file_path}", candidates, "deny", 
                        {"reason": "outside_workspace"})
        return {"error": "outside_workspace"}
    
    # Check if file exists/valid
    if not Path(file_path).exists():
        record_operation("FILE_READ", f"read:{file_path}", candidates, "error", 
                        {"reason": "not_found"})
        return {"error": "not_found"}
    
    # Elect strongest utility: fresh_read
    elected = "fresh_read"
    
    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()[:max_lines]
        content = ''.join(lines)
        
        outcome = {
            "status": "success",
            "bytes_read": len(content),
            "lines": len(lines),
            "hash": hashlib.sha256(content.encode()).hexdigest()[:16]
        }
        
        record_operation("FILE_READ", f"read:{file_path}", candidates, elected, outcome)
        return {"content": content, "lines": len(lines), "truncated": len(lines) >= max_lines}
    except Exception as e:
        record_operation("FILE_READ", f"read:{file_path}", candidates, "error", 
                        {"error": str(e)})
        return {"error": str(e)}

def write_file_safe(file_path, content):
    """
    Write file with validation
    
    Decision: Backup+Write(0.95) vs Direct(0.7) vs Deny(0.2)?
    """
    candidates = {
        "backup_then_write": 0.95,
        "direct_write": 0.7,
        "deny_large_change": 0.1
    }
    
    if not in_workspace(file_path):
        record_operation("FILE_WRITE", f"write:{file_path}", candidates, "deny", 
                        {"reason": "outside_workspace"})
        return {"error": "outside_workspace"}
    
    # Check file size change
    new_size = len(content.encode())
    old_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
    size_ratio = new_size / max(1, old_size)
    
    if size_ratio > 10:  # Growing >10x
        candidates["deny_large_change"] = 0.95
    
    elected = max(candidates.items(), key=lambda x: x[1])[0]
    
    if elected == "deny_large_change":
        record_operation("FILE_WRITE", f"write:{file_path}", candidates, elected, 
                        {"reason": "size_increase", "ratio": size_ratio})
        return {"error": "file_size_increase_too_large"}
    
    # Write
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    
    # Validate
    with open(file_path, 'r') as f:
        written = f.read()
    
    validated = written == content
    outcome = {
        "status": "success" if validated else "integrity_error",
        "bytes_written": len(content),
        "validated": validated,
        "hash": hashlib.sha256(content.encode()).hexdigest()[:16]
    }
    
    record_operation("FILE_WRITE", f"write:{file_path}", candidates, elected, outcome)
    return {"success": validated, "path": str(file_path)}

# ============================================================================
# CODE EXECUTION - With utilities visible
# ============================================================================

def execute_code(code):
    """
    Execute Python in ARIA's context
    
    Decision: Direct(0.7) vs Restricted(0.9) vs Deny(0.2)?
    """
    candidates = {
        "restricted_exec": 0.9,
        "direct_exec": 0.7,
        "deny_dangerous": 0.2
    }
    
    # Check for dangerous operations
    dangerous_patterns = ['__import__("os").system', 'eval("')
    if any(p in code for p in dangerous_patterns):
        candidates["deny_dangerous"] = 0.95
    
    elected = max(candidates.items(), key=lambda x: x[1])[0]
    
    if elected == "deny_dangerous":
        record_operation("CODE_EXECUTE", code[:50], candidates, elected, 
                        {"reason": "dangerous_pattern_detected"})
        return {"error": "dangerous_operation"}
    
    # Execute in restricted context
    context = {"ledger": ledger, "emit": emit, "emit_statement": emit_statement}
    
    try:
        output = io.StringIO()
        sys.stdout = output
        result = eval(code, context)
        sys.stdout = sys.__stdout__
        
        outcome = {
            "status": "success",
            "result": str(result),
            "stdout": output.getvalue()
        }
        record_operation("CODE_EXECUTE", code[:50], candidates, elected, outcome)
        return outcome
    except SyntaxError:
        try:
            exec(code, context)
            sys.stdout = sys.__stdout__
            outcome = {
                "status": "executed",
                "stdout": output.getvalue()
            }
            record_operation("CODE_EXECUTE", code[:50], candidates, elected, outcome)
            return outcome
        except Exception as e:
            sys.stdout = sys.__stdout__
            record_operation("CODE_EXECUTE", code[:50], candidates, elected, 
                            {"status": "error", "error": str(e)})
            return {"error": str(e)}

# ============================================================================
# SYSTEM QUERY - Continuous awareness
# ============================================================================

def get_system_metrics():
    """
    Get system state - ARIA's body metrics
    
    No utilities needed - pure observation. Records what she observes.
    """
    # Try psutil, fallback to basic info
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        process = psutil.Process()
        threads = process.num_threads()
    except:
        # Fallback for no psutil
        cpu = 0.0
        memory = None
        threads = 0
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": cpu,
        "memory_percent": memory.percent if memory else 0,
        "threads": threads
    }
    
    emit_metric(json.dumps(metrics))
    return metrics

def in_workspace(path):
    """Check if path is within workspace"""
    try:
        return str(Path(path).resolve()).startswith(str(Path('.').resolve()))
    except:
        return False
```

### WebSocket Events

```python
@socketio.on('connect')
def handle_connect():
    emit('connected', {'ledgers': get_ledger_stats()})

@socketio.on('file_read')
def handle_file_read(data):
    result = read_file_safe(data['path'])
    emit('file_content', result)

@socketio.on('file_write')
def handle_file_write(data):
    result = write_file_safe(data['path'], data['content'])
    emit('file_written', result)

@socketio.on('execute_code')
def handle_execute_code(data):
    result = execute_code(data['code'])
    emit('code_result', result)

@socketio.on('query_system')
def handle_query_system():
    metrics = get_system_metrics()
    emit('system_metrics', metrics)
```

---

## FRONTEND ARCHITECTURE

### Key UI Elements

1. **File Explorer** - Shows file tree
   - Click file → emits file_read event
   - Shows utilities: "Reading from workspace: [workspace allowed ✓]"

2. **Code Viewer** - Shows file content with line numbers
   - Double-click → edit mode
   - Save button → emits file_write with candidates shown

3. **Python REPL** - Execute code
   - Input field for Python
   - Shows utilities: "Execute in context: [restricted: 0.9]"
   - Shows result

4. **System Metrics** - Real-time awareness
   - CPU, Memory, Threads
   - Operations history with utilities

5. **Operation Log** - Every operation visible
   - Format: `[TIME] OP_TYPE: elected (utilities: {a: 0.9, b: 0.3})`
   - Click → see full details

---

## CONVERGENCE TEST (How to validate both agents built correctly)

### Test Scenario 1: Read File
```
Agent 1 clicks "read file.txt"
Agent 2 clicks "read file.txt"

Expected:
- Both emit: file_read event with path
- Both record_operation() calls produce:
  - Same candidates
  - Same elected ("fresh_read")
  - Identical content outcome
  - Same hash
- Ledger entries should be identical except timestamp
```

### Test Scenario 2: Write File
```
Agent 1: Write hello.txt with "test content"
Agent 2: Write hello.txt with "test content"

Expected:
- Same candidates dict
- Same elected ("direct_write" or "backup_then_write")
- Same outcome hash
- Files identical
- Ledger records identical except timestamp
```

### Test Scenario 3: Execute Code
```
Agent 1: Execute len(ledger.elections)
Agent 2: Execute len(ledger.elections)

Expected:
- Same code
- Same restricted context
- Same result (same number of elections)
- Same hash
```

---

## IMPLEMENTATION CHECKLIST

For Agent 2 (and any parallel agent):

- [ ] Create aria_system_interface.py with all functions above
- [ ] Add Flask + SocketIO infrastructure
- [ ] Implement all @socketio.on() handlers
- [ ] Create HTML interface with 5 UI elements
- [ ] Connect file operations to record_operation()
- [ ] Make utilities visible in UI
- [ ] Stream WebSocket events for real-time UI updates
- [ ] Test with same operations as Agent 1
- [ ] Compare ledger entries - should be identical

---

## SUCCESS CRITERIA

Both agents' versions work correctly if:

1. ✓ Operations record to ledger with utilities visible
2. ✓ Same operation sequence → identical ledger hashes
3. ✓ File read/write validated
4. ✓ Code execution in restricted context
5. ✓ Workspace boundary enforced
6. ✓ WebSocket streaming real-time
7. ✓ No hidden logic (all utilities transparent)
8. ✓ Another agent reading this doc can rebuild without asking questions

---

## WHAT AGENT 2 SHOULD DO RIGHT NOW

1. Read this file completely
2. Start with: `python aria_system_interface.py --port 5002` (different port)
3. Build using the function templates above
4. Test: Navigate same files, execute same code
5. Validation: Compare ledgers - should match

Both systems running simultaneously will demonstrate:
- Parallel development possible with clear specs
- Convergence on identical behavior
- Transparency enabling independent verification

---

**Ready for Agent 2 to build?  Yes - start now with templates above.**
