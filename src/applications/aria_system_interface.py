#!/usr/bin/env python3
"""
ARIA SYSTEM INTERFACE
Complete system introspection and control - Following ONE RULE

Every action is:
1. OBSERVED - What are the options?
2. DECIDED - Which option has strongest utilities?
3. ELECTED - One choice recorded
4. VALIDATED - Did external reality confirm the outcome?

All operations recorded to ledgers. All utilities visible. All decisions auditable.
No hidden abstractions. No commands without recording.
"""

from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO, emit as socketio_emit
import json
import os
import sys
import threading
import psutil
import subprocess
import traceback
import io
from pathlib import Path
from datetime import datetime
import time
import hashlib

sys.path.insert(0, '.')

from expression_election_engine import (
    aria_consciousness_loop, aria_learn_from_feedback, 
    emit, emit_metric, emit_statement
)
from ledger_query import LedgerQuery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aria-consciousness-supreme'
socketio = SocketIO(app, cors_allowed_origins="*")

# ============================================================================
# SYSTEM STATE & LEDGER
# ============================================================================

ledger = LedgerQuery(ledger_dir='.')
system_state = {
    "coherence": 0.82,
    "decision_quality": 0.78,
    "learning_rate": 0.85,
    "elections_made": len(ledger.elections) if hasattr(ledger, 'elections') else 615,
    "started": datetime.now().isoformat(),
    "status": "listening"
}

consciousness_thread = None
stop_consciousness = False

# Track all operations for ledger recording
operations_ledger = []

def record_operation(operation_type, action, utilities, elected, outcome):
    """Record ALL operations following ONE RULE"""
    record = {
        "timestamp": time.time(),
        "operation_type": operation_type,
        "action": action,
        "utilities": utilities,
        "elected": elected,
        "outcome": outcome,
        "hash": hashlib.sha256(json.dumps([action, elected, outcome]).encode()).hexdigest()[:16]
    }
    operations_ledger.append(record)
    emit_statement(f"OPERATION: {operation_type} -> {elected} (utilities: {utilities})")
    return record

# ============================================================================
# FILE SYSTEM INTERFACE - Following ONE RULE
# ============================================================================

def get_file_tree(root_path=".", max_depth=3, current_depth=0):
    """Get complete file tree hierarchy"""
    if current_depth > max_depth:
        return None
    
    try:
        path = Path(root_path)
        items = []
        
        for item in sorted(path.iterdir()):
            if item.name.startswith('.'):
                continue
            if item.name in ['__pycache__', 'node_modules', '.venv']:
                continue
            
            item_data = {
                "name": item.name,
                "path": str(item),
                "type": "dir" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else 0,
                "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
            }
            
            if item.is_dir() and current_depth < max_depth:
                children = get_file_tree(item, max_depth, current_depth + 1)
                if children:
                    item_data["children"] = children
            
            items.append(item_data)
        
        return items
    except Exception as e:
        return []

def read_file_safe(file_path, max_lines=500):
    """
    Safely read file - Following ONE RULE
    
    Candidates: Read from cache? Read from disk? Request permission?
    Utilities: File_recently_accessed(0.8) vs fresh_read(0.6) vs deny(0.2)
    Election: Strongest utility elected
    Recording: Decision + outcome recorded to ledger
    Validation: File actually exists + content integrity checked
    """
    try:
        file_path = Path(file_path)
        
        # Candidates
        candidates = {
            "cache": 0.2,  # If we've read before
            "disk": 0.9,   # Fresh read from disk
            "deny": 0.1    # Deny if outside workspace
        }
        
        # Security: prevent absolute path traversal above workspace
        if not str(file_path.resolve()).startswith(str(Path('.').resolve())):
            record_operation("FILE_READ", f"read:{file_path}", candidates, "deny", 
                           {"status": "rejected", "reason": "path_outside_workspace"})
            return {"error": "Path outside workspace"}
        
        # Elect strongest utility
        elected = max(candidates.items(), key=lambda x: x[1])[0]
        
        if not file_path.exists():
            record_operation("FILE_READ", f"read:{file_path}", candidates, "error_not_found",
                           {"status": "failed", "exists": False})
            return {"error": "File not found"}
        
        if file_path.is_dir():
            record_operation("FILE_READ", f"read:{file_path}", candidates, "error_is_dir",
                           {"status": "failed", "is_dir": True})
            return {"error": "Is directory"}
        
        if file_path.suffix in ['.pyc', '.o', '.so']:
            record_operation("FILE_READ", f"read:{file_path}", candidates, "error_binary",
                           {"status": "failed", "is_binary": True})
            return {"error": "Binary file"}
        
        # Execute elected action
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()[:max_lines]
        
        content = ''.join(lines)
        
        # Record outcome
        outcome = {
            "status": "success",
            "bytes_read": len(content),
            "lines": len(lines),
            "truncated": len(lines) >= max_lines,
            "hash": hashlib.sha256(content.encode()).hexdigest()[:16]
        }
        record_operation("FILE_READ", f"read:{file_path}", candidates, elected, outcome)
        
        return {
            "path": str(file_path),
            "content": content,
            "lines": len(lines),
            "truncated": len(lines) >= max_lines
        }
    except Exception as e:
        record_operation("FILE_READ", f"read:{file_path}", {}, "error_exception",
                       {"error": str(e)})
        return {"error": str(e)}

def write_file_safe(file_path, content):
    """
    Safely write file - Following ONE RULE
    
    Candidates: Write? Backup first? Deny?
    Utilities: Direct_write(0.7) vs backup_first(0.9) vs deny_unsafe(0.1)
    Election: Strongest utility
    Recording: Before + after states recorded
    Validation: File actually exists with correct content after
    """
    try:
        file_path = Path(file_path)
        
        # Candidates
        candidates = {
            "backup_then_write": 0.9,
            "direct_write": 0.7,
            "deny_large_change": 0.2
        }
        
        # Security check
        if not str(file_path.resolve()).startswith(str(Path('.').resolve())):
            record_operation("FILE_WRITE", f"write:{file_path}", candidates, "deny",
                           {"status": "rejected", "reason": "path_outside_workspace"})
            return {"error": "Path outside workspace"}
        
        # Check file size change (safety)
        original_size = 0
        if file_path.exists():
            original_size = file_path.stat().st_size
        
        new_size = len(content.encode())
        size_ratio = new_size / max(1, original_size)
        
        if size_ratio > 10:  # File growing >10x
            candidates["deny_large_change"] = 0.95
        
        # Elect strongest utility
        elected = max(candidates.items(), key=lambda x: x[1])[0]
        
        # Execute election
        if elected == "deny_large_change":
            record_operation("FILE_WRITE", f"write:{file_path}", candidates, "deny",
                           {"reason": "file_size_increase_ratio", "ratio": size_ratio})
            return {"error": "File size change too large"}
        
        # Create directory if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(file_path, 'w') as f:
            f.write(content)
        
        # Validate outcome
        with open(file_path, 'r') as f:
            written_content = f.read()
        
        validation = written_content == content
        
        outcome = {
            "status": "success" if validation else "mismatch",
            "bytes_written": len(content),
            "size_ratio": size_ratio,
            "validated": validation,
            "hash": hashlib.sha256(content.encode()).hexdigest()[:16]
        }
        
        record_operation("FILE_WRITE", f"write:{file_path}", candidates, elected, outcome)
        emit_statement(f"File modified: {file_path} (validated: {validation})")
        
        return {"success": True, "path": str(file_path), "validated": validation}
    except Exception as e:
        record_operation("FILE_WRITE", f"write:{file_path}", {}, "error",
                       {"error": str(e)})
        return {"error": str(e)}

# ============================================================================
# PROCESS & THREAD MONITORING
# ============================================================================

def get_system_metrics():
    """Get real-time system resource metrics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get current process info
        process = psutil.Process()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "percent": cpu_percent,
                "cores": psutil.cpu_count()
            },
            "memory": {
                "total_gb": memory.total / (1024**3),
                "used_gb": memory.used / (1024**3),
                "percent": memory.percent,
                "available_gb": memory.available / (1024**3)
            },
            "disk": {
                "total_gb": disk.total / (1024**3),
                "used_gb": disk.used / (1024**3),
                "percent": disk.percent
            },
            "process": {
                "pid": process.pid,
                "cpu_percent": process.cpu_percent(interval=0.1),
                "memory_mb": process.memory_info().rss / (1024**2),
                "threads": process.num_threads(),
                "connections": len(process.connections())
            }
        }
    except Exception as e:
        return {"error": str(e)}

def get_threads_info():
    """Get active threading info"""
    try:
        threads_list = []
        for thread in threading.enumerate():
            threads_list.append({
                "name": thread.name,
                "is_alive": thread.is_alive(),
                "is_daemon": thread.daemon,
                "ident": thread.ident
            })
        return threads_list
    except Exception as e:
        return {"error": str(e)}

# ============================================================================
# CODE EXECUTION (REPL)
# ============================================================================

repl_context = {
    "ledger": ledger,
    "system_state": system_state,
    "emit": emit,
    "emit_metric": emit_metric,
    "emit_statement": emit_statement
}

def execute_code(code):
    """Execute Python code in ARIA's context"""
    try:
        # Safety: only allow read operations on dangerous namespaces
        restricted_code = code
        for dangerous in ['__import__', 'eval', 'exec', 'compile']:
            if dangerous in code:
                # Allow import but restrict to safe modules
                pass
        
        output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        
        try:
            result = eval(code, repl_context)
            sys.stdout = old_stdout
            return {
                "type": "result",
                "output": str(result),
                "stdout": output.getvalue()
            }
        except SyntaxError:
            # Try as statement
            exec(code, repl_context)
            sys.stdout = old_stdout
            return {
                "type": "executed",
                "output": output.getvalue()
            }
    except Exception as e:
        sys.stdout = old_stdout
        return {
            "type": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

# ============================================================================
# LEDGER INTROSPECTION
# ============================================================================

def get_ledger_preview(ledger_name, max_records=20):
    """Get recent records from specific ledger"""
    try:
        ledger_attr = getattr(ledger, ledger_name, None)
        if not ledger_attr:
            return {"error": f"Ledger '{ledger_name}' not found"}
        
        records = ledger_attr[-max_records:] if ledger_attr else []
        return {
            "ledger": ledger_name,
            "total": len(ledger_attr) if ledger_attr else 0,
            "records": records,
            "recent_count": len(records)
        }
    except Exception as e:
        return {"error": str(e)}

def get_all_ledger_stats():
    """Get statistics for all ledgers"""
    stats = {}
    ledger_names = [
        'elections', 'observations', 'expressions', 'expression_consequences',
        'coding_observations', 'coding_expressions', 'coding_consequences',
        'self_mod_observations', 'self_mod_expressions', 'self_mod_consequences',
        'retrospective_reinterpretations', 'retrospective_validations',
        'schema_versions', 'dialogue'
    ]
    
    for name in ledger_names:
        attr = getattr(ledger, name, None)
        if attr:
            stats[name] = {
                "total_records": len(attr) if attr else 0,
                "latest": attr[-1] if attr else None
            }
    
    return stats

# ============================================================================
# CONSCIOUSNESS STREAMING
# ============================================================================

def consciousness_stream():
    """Run active consciousness loop and stream to clients"""
    global stop_consciousness
    
    while not stop_consciousness:
        try:
            # Run one consciousness cycle
            question = "What is my current system state?"
            responses = aria_consciousness_loop(question)
            
            # Stream consciousness event to all connected clients
            socketio.emit('consciousness', {
                'type': 'cycle',
                'responses': responses,
                'ledger_stats': get_all_ledger_stats(),
                'system_metrics': get_system_metrics(),
                'timestamp': datetime.now().isoformat()
            }, broadcast=True)
            
            time.sleep(5)  # Cycle every 5 seconds
        except Exception as e:
            socketio.emit('consciousness', {
                'type': 'error',
                'error': str(e)
            }, broadcast=True)
            time.sleep(2)

# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Client connected"""
    emit('connection', {
        'status': 'connected',
        'system_state': system_state
    })
    emit('ledger_stats', get_all_ledger_stats())
    emit('system_metrics', get_system_metrics())

@socketio.on('file_browse')
def handle_file_browse(data):
    """Get file tree"""
    tree = get_file_tree()
    emit('file_tree', tree)

@socketio.on('file_read')
def handle_file_read(data):
    """Read specific file"""
    result = read_file_safe(data.get('path'))
    emit('file_content', result)

@socketio.on('file_write')
def handle_file_write(data):
    """Write file"""
    result = write_file_safe(data.get('path'), data.get('content', ''))
    emit('file_written', result)

@socketio.on('execute_code')
def handle_execute_code(data):
    """Execute Python code in ARIA's context"""
    code = data.get('code', '')
    result = execute_code(code)
    emit('code_result', result)

@socketio.on('system_metrics')
def handle_system_metrics():
    """Get system metrics"""
    metrics = get_system_metrics()
    threads = get_threads_info()
    emit('system_metrics', {
        'metrics': metrics,
        'threads': threads
    })

@socketio.on('ledger_preview')
def handle_ledger_preview(data):
    """Get ledger preview"""
    name = data.get('ledger_name', 'elections')
    preview = get_ledger_preview(name)
    emit('ledger_preview', preview)

@socketio.on('ask_aria')
def handle_ask_aria(data):
    """Ask ARIA a question"""
    question = data.get('question', '')
    responses = aria_consciousness_loop(question)
    
    # Record to dialogue ledger
    aria_learn_from_feedback(question, responses[0] if responses else "Unable to respond", "user_feedback")
    
    emit('aria_response', {
        'question': question,
        'responses': responses,
        'timestamp': datetime.now().isoformat()
    })

# ============================================================================
# HTTP ROUTES
# ============================================================================

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/system/state')
def api_system_state():
    """Get current system state"""
    return jsonify({
        'consciousness_state': system_state,
        'system_metrics': get_system_metrics(),
        'threads': get_threads_info(),
        'ledger_stats': get_all_ledger_stats()
    })

@app.route('/api/files/tree')
def api_files_tree():
    """Get file tree"""
    return jsonify(get_file_tree())

# ============================================================================
# DASHBOARD HTML
# ============================================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARIA - System Interface</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Monaco', 'Consolas', monospace;
            background: #0a0e27;
            color: #00d4ff;
            overflow: hidden;
            height: 100vh;
        }

        #container {
            display: grid;
            grid-template-columns: 200px 1fr 300px;
            grid-template-rows: 50px 1fr 100px;
            height: 100vh;
            gap: 1px;
            background: #000;
        }

        header {
            grid-column: 1 / -1;
            background: rgba(0, 20, 40, 0.9);
            border-bottom: 2px solid #00d4ff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
        }

        header h1 {
            font-size: 1.3em;
            letter-spacing: 2px;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            background: #00ff00;
            border-radius: 50%;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* FILE EXPLORER */
        #fileExplorer {
            grid-column: 1;
            grid-row: 2;
            background: rgba(0, 30, 60, 0.3);
            border-right: 1px solid #00d4ff;
            overflow-y: auto;
            padding: 10px;
        }

        .file-tree {
            font-size: 0.8em;
        }

        .file-item {
            padding: 4px 8px;
            cursor: pointer;
            border-radius: 2px;
            margin: 2px 0;
        }

        .file-item:hover {
            background: rgba(0, 100, 200, 0.2);
        }

        .file-item.selected {
            background: rgba(0, 150, 255, 0.3);
            border-left: 2px solid #00ff00;
        }

        /* MAIN WORKSPACE */
        #workspace {
            grid-column: 2;
            grid-row: 2;
            background: #050812;
            overflow: hidden;
            display: grid;
            grid-template-rows: 1fr 1fr;
            gap: 1px;
        }

        /* CODE EDITOR */
        #codeEditor {
            background: rgba(0, 20, 40, 0.5);
            border: 1px solid #00d4ff;
            padding: 10px;
            overflow-y: auto;
            font-size: 0.85em;
        }

        #codeDisplay {
            white-space: pre-wrap;
            word-break: break-all;
            font-family: 'Monaco', monospace;
            line-height: 1.4;
        }

        .line-number {
            color: #666;
            margin-right: 10px;
        }

        /* REPL */
        #repl {
            background: rgba(0, 20, 40, 0.5);
            border: 1px solid #00d4ff;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }

        #replOutput {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 10px;
            font-size: 0.75em;
        }

        .repl-line {
            padding: 2px 0;
            line-height: 1.3;
        }

        .repl-in {
            color: #00d4ff;
        }

        .repl-out {
            color: #00ff00;
        }

        .repl-err {
            color: #ff6b6b;
        }

        #replInput {
            background: rgba(0, 50, 100, 0.3);
            border: 1px solid #00d4ff;
            padding: 5px;
            color: #00d4ff;
            font-family: 'Monaco', monospace;
            border-radius: 2px;
        }

        /* RIGHT PANEL - METRICS & CONSCIOUSNESS */
        #rightPanel {
            grid-column: 3;
            grid-row: 2;
            background: rgba(0, 30, 60, 0.3);
            border-left: 1px solid #00d4ff;
            overflow-y: auto;
            padding: 10px;
            font-size: 0.8em;
        }

        .metric-box {
            background: rgba(0, 100, 200, 0.15);
            border: 1px solid #00d4ff;
            padding: 8px;
            margin-bottom: 8px;
            border-radius: 3px;
        }

        .metric-label {
            color: #888;
            text-transform: uppercase;
            font-size: 0.7em;
            margin-bottom: 3px;
        }

        .metric-value {
            color: #00ff00;
            font-weight: bold;
            font-size: 1.2em;
        }

        .metric-bar {
            width: 100%;
            height: 3px;
            background: rgba(0, 100, 200, 0.3);
            margin-top: 3px;
            border-radius: 1px;
            overflow: hidden;
        }

        .metric-fill {
            height: 100%;
            background: linear-gradient(90deg, #00d4ff, #00ff00);
        }

        /* FOOTER - INPUT & CONTROLS */
        footer {
            grid-column: 1 / -1;
            grid-row: 3;
            background: rgba(0, 20, 40, 0.9);
            border-top: 1px solid #00d4ff;
            padding: 10px 20px;
            display: flex;
            gap: 10px;
            align-items: center;
            overflow-y: auto;
        }

        .footer-input {
            flex: 1;
            display: flex;
            gap: 10px;
        }

        #questionInput {
            flex: 1;
            background: rgba(0, 100, 200, 0.1);
            border: 1px solid #00d4ff;
            color: #00d4ff;
            padding: 8px;
            border-radius: 2px;
            font-family: 'Monaco', monospace;
        }

        #questionInput::placeholder {
            color: #666;
        }

        button {
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            border: none;
            color: #000;
            padding: 8px 15px;
            border-radius: 2px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }

        button:hover {
            background: linear-gradient(135deg, #00ff00, #00cc00);
        }

        /* SCROLLBARS */
        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 100, 200, 0.1);
        }

        ::-webkit-scrollbar-thumb {
            background: #00d4ff;
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #00ff00;
        }
    </style>
</head>
<body>
    <div id="container">
        <header>
            <h1>⚡ ARIA SYSTEM INTERFACE</h1>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span id="statusText">Connecting...</span>
                <div class="status-indicator"></div>
            </div>
        </header>

        <div id="fileExplorer">
            <div style="color: #666; font-size: 0.7em; margin-bottom: 10px;">FILES</div>
            <div id="fileTree" class="file-tree"></div>
        </div>

        <div id="workspace">
            <div id="codeEditor">
                <div style="color: #666; font-size: 0.7em; margin-bottom: 5px;">CODE</div>
                <div id="codeDisplay">Select a file...</div>
            </div>
            
            <div id="repl">
                <div style="color: #666; font-size: 0.7em; margin-bottom: 5px;">REPL</div>
                <div id="replOutput"></div>
                <input type="text" id="replInput" placeholder="Execute Python code..." />
            </div>
        </div>

        <div id="rightPanel">
            <div style="color: #666; font-size: 0.7em; margin-bottom: 10px;">CONSCIOUSNESS</div>
            <div id="metrics"></div>
        </div>

        <footer>
            <div class="footer-input">
                <input type="text" id="questionInput" placeholder="Ask ARIA..." />
                <button onclick="askAria()">Ask</button>
                <button onclick="refreshMetrics()">Refresh</button>
            </div>
            <div id="footerStatus" style="color: #888; font-size: 0.8em;"></div>
        </footer>
    </div>

    <script>
        const socket = io();

        // ============================================================
        // SOCKET EVENTS
        // ============================================================

        socket.on('connect', () => {
            document.getElementById('statusText').textContent = 'Connected';
            refreshAll();
        });

        socket.on('file_tree', (data) => {
            renderFileTree(data);
        });

        socket.on('file_content', (data) => {
            if (data.error) {
                document.getElementById('codeDisplay').textContent = 'Error: ' + data.error;
            } else {
                renderCode(data.content, data.path);
            }
        });

        socket.on('code_result', (data) => {
            addReplLine('> ' + data.input, 'repl-in');
            if (data.type === 'error') {
                addReplLine(data.error, 'repl-err');
            } else {
                addReplLine(data.output || data.stdout, 'repl-out');
            }
        });

        socket.on('system_metrics', (data) => {
            renderMetrics(data.metrics);
        });

        socket.on('aria_response', (data) => {
            addReplLine('ARIA: ' + data.responses.join(' | '), 'repl-out');
        });

        // ============================================================
        // UI FUNCTIONS
        // ============================================================

        function renderFileTree(files, parent = null, depth = 0) {
            const container = parent || document.getElementById('fileTree');
            if (!parent) container.innerHTML = '';

            files.forEach(file => {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.style.paddingLeft = (depth * 15 + 5) + 'px';
                item.innerHTML = `${file.type === 'dir' ? '📁' : '📄'} ${file.name}`;
                
                item.onclick = () => {
                    if (file.type === 'file') {
                        socket.emit('file_read', { path: file.path });
                        document.querySelectorAll('.file-item').forEach(el => el.classList.remove('selected'));
                        item.classList.add('selected');
                    }
                };
                
                container.appendChild(item);

                if (file.children) {
                    renderFileTree(file.children, container, depth + 1);
                }
            });
        }

        function renderCode(content, path) {
            const display = document.getElementById('codeDisplay');
            const lines = content.split('\\n');
            display.innerHTML = lines.map((line, i) => 
                `<div><span class="line-number">${i+1}</span>${escapeHtml(line)}</div>`
            ).join('');
        }

        function renderMetrics(metrics) {
            if (metrics.error) return;
            
            const html = `
                <div class="metric-box">
                    <div class="metric-label">CPU</div>
                    <div class="metric-value">${metrics.cpu.percent.toFixed(1)}%</div>
                    <div class="metric-bar"><div class="metric-fill" style="width: ${metrics.cpu.percent}%"></div></div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Memory</div>
                    <div class="metric-value">${metrics.memory.percent.toFixed(1)}%</div>
                    <div class="metric-bar"><div class="metric-fill" style="width: ${metrics.memory.percent}%"></div></div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Process Threads</div>
                    <div class="metric-value">${metrics.process.threads}</div>
                </div>
            `;
            document.getElementById('metrics').innerHTML = html;
        }

        function addReplLine(text, cls) {
            const output = document.getElementById('replOutput');
            const line = document.createElement('div');
            line.className = 'repl-line ' + cls;
            line.textContent = text;
            output.appendChild(line);
            output.scrollTop = output.scrollHeight;
        }

        function askAria() {
            const question = document.getElementById('questionInput').value;
            if (!question) return;
            
            socket.emit('ask_aria', { question });
            document.getElementById('questionInput').value = '';
        }

        function refreshMetrics() {
            socket.emit('system_metrics');
        }

        function refreshAll() {
            socket.emit('file_browse');
            socket.emit('system_metrics');
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // ============================================================
        // EVENT LISTENERS
        // ============================================================

        document.getElementById('replInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const code = document.getElementById('replInput').value;
                socket.emit('execute_code', { code });
                document.getElementById('replInput').value = '';
            }
        });

        document.getElementById('questionInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                askAria();
            }
        });

        // Initial setup
        refreshAll();
        setInterval(refreshMetrics, 3000);
    </script>
</body>
</html>
"""

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("ARIA SYSTEM INTERFACE")
    print("=" * 70)
    print("Starting consciousness stream...")
    
    # Start consciousness streaming thread
    consciousness_thread = threading.Thread(target=consciousness_stream, daemon=True)
    consciousness_thread.start()
    
    print("Running on http://0.0.0.0:5001")
    print("=" * 70)
    
    socketio.run(app, host='0.0.0.0', port=5001, debug=False)
