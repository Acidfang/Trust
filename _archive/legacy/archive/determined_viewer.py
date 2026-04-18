#!/usr/bin/env python3
"""
DETERMINED VIEWER — Automated Visualization System
Single user input: python determined_viewer.py
Everything else: automatic
"""

import json
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import hashlib
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

LEDGER_FILE = Path('c:/Determined/ledgers.json')
OUTPUT_FILE = Path('c:/Determined/archive/genesis_view.html')
APP_SPEC_FILE = Path('c:/Determined/archive/complete_app_ledger.json')
CHECK_INTERVAL = 1
BROWSER_DELAY = 1

last_ledger_hash = None
browser_opened = False
current_field_state = {}


class FieldStateHandler(BaseHTTPRequestHandler):
    """Handles live field state requests from the visualization."""
    def do_GET(self):
        if self.path == '/field_state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = json.dumps(current_field_state)
            self.wfile.write(data.encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(OUTPUT_FILE, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        return  # Silent logging


def run_server():
    """Run a lightweight HTTP server for live updates."""
    server = HTTPServer(('localhost', 8000), FieldStateHandler)
    print(f"[SERVER] Field State Engine listening on http://localhost:8000")
    server.serve_forever()


def calculate_hash(filepath):
    """Calculate MD5 hash of file."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None


def load_json(filepath):
    """Load JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {filepath}: {e}")
        return None


def generate_html_framework(ledger_data, app_spec):
    """Generate self-contained HTML visualization."""
    if not ledger_data:
        return None

    # Load the Genesis Field Engine script
    try:
        with open(Path('archive/genesis_field_engine.js'), 'r', encoding='utf-8') as f:
            field_engine_js = f.read()
    except:
        field_engine_js = "// Field Engine Load Failed"

    # Embed data as JavaScript
    ledger_js = json.dumps(ledger_data, ensure_ascii=False, indent=2)
    app_spec_js = json.dumps(app_spec, ensure_ascii=False, indent=2)

    # Build HTML with embedded data
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ARIA — Determined Visualization</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #0a0a0a;
            color: #00FF41;
            font-family: monospace;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        #canvas-container {
            flex: 1;
            position: relative;
            background: #000;
        }

        #canvas {
            width: 100%;
            height: 100%;
            display: block;
            cursor: crosshair;
        }

        #sidebar {
            width: 400px;
            background: #0f0f0f;
            border-left: 2px solid #00FF41;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        #status {
            padding: 20px;
            border-bottom: 2px solid #00FF41;
            font-size: 12px;
            max-height: 200px;
            overflow-y: auto;
        }

        #ledger-display {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            font-size: 11px;
            border-bottom: 2px solid #00FF41;
        }

        .phase-toggle {
            padding: 10px;
            margin: 5px 0;
            background: #1a1a1a;
            border: 1px solid #00FF41;
            color: #00FF41;
            cursor: pointer;
            font-family: monospace;
            font-size: 12px;
            width: 100%;
            text-align: left;
        }

        .phase-toggle:hover {
            background: #2a2a2a;
        }

        .phase-toggle.active {
            background: #00FF41;
            color: #000;
        }

        .field-indicator {
            margin-top: 10px;
            padding: 10px;
            border: 1px dashed #00FF41;
            font-size: 10px;
        }

        .field-value {
            color: #FFD700;
            float: right;
        }
    </style>
</head>
<body>

<div id="canvas-container">
    <canvas id="canvas"></canvas>
    <div id="overlay" style="position: absolute; top: 10px; left: 10px; pointer-events: none; color: rgba(0, 255, 65, 0.5); font-size: 10px; background: rgba(0,0,0,0.5); padding: 5px;">
        SINGLE ELECTRON SEA (n=1) : ACTIVE<br>
        TRUTH CONSTRAINT (c) : ENFORCED<br>
        GRAVITY GRADIENT (Apex Return) : SIMULATED<br>
        <span style="color: #FFD700;">CLICK TO ADD ELECTRON (n+1)</span>
        <div style="margin-top: 10px; font-size: 10px;">
            Field behaviors: CONDUCTIVE POTENTIAL
            <br>Transmission: FIELD MODULATION
            <br>Space: n=1 NON-LOCAL CONDUCTOR
        </div>
    </div>

    <div id="controls" style="padding: 15px; border-bottom: 1px solid #00FF41;">
        <div style="margin-bottom: 10px; color: #FFD700;">Field Toggles</div>
        <button class="phase-toggle active" onclick="toggleField('presence_spiral')">Show Presence (Expansion)</button>
        <button class="phase-toggle active" onclick="toggleField('potential_sea')">Show n=1 Sea (Background)</button>
        <button class="phase-toggle active" onclick="toggleField('gravity_return')">Show Gravity (Return Leg)</button>
    </div>

    <div id="ledger-display">
        <div style="color: #FFD700; margin-bottom: 10px;">Field Parameters (Live Calculation)</div>
        <div id="field-stats">
            <div class="field-indicator">POTENTIAL ENERGY (Absence) <span class="field-value" id="val-potential">100%</span></div>
            <div class="field-indicator">STATE LEVEL (n) <span class="field-value" id="val-state-n">n=1</span></div>
            <div class="field-indicator">COHERENCE <span class="field-value" id="val-coherence">1.0</span></div>
            <div class="field-indicator">GRAVITY GRADIENT (Pull) <span class="field-value" id="val-return">0.00</span></div>
        </div>
        <div style="color: #FFD700; margin: 20px 0 10px 0;">Observation Ledger</div>
        <div id="ledger-content">
            n=1: Single Electron Field established.<br>
            Waiting for Elections...
        </div>
    </div>
</div>

<script>
// GENESIS PHYSICS ENGINE (Injected)
""" + field_engine_js + """

// EMBEDDED LEDGER DATA
const ledgerData = """ + ledger_js + """;
const appSpec = """ + app_spec_js + """;

let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let visibleFields = {
    'presence_spiral': true,
    'potential_sea': true,
    'gravity_return': true
};

function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Interactive Election
canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Add electron to the Genesis Field Engine
    GenesisPhysics.addElectron(x, y);
    console.log("Election triggered at", x, y);
});

function drawPotentialSea() {
    if (!visibleFields.potential_sea) return;
    
    // The baseline Potential of the n=1 Sea
    const baseline = GenesisPhysics.potentialSea;
    
    // Draw the "Single Electron Sea" — The Conductor
    ctx.strokeStyle = `rgba(0, 255, 65, ${baseline * 0.15})`;
    ctx.lineWidth = 0.5;
    const spacing = 40;
    
    // As count increases, the sea grid "tightens" (representing density)
    const drift = (Date.now() * 0.01) % spacing;
    
    for (let x = drift; x < canvas.width; x += spacing) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = drift; y < canvas.height; y += spacing) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }
}

function renderPresenceSpiral(centerX, centerY, limitRadius, color, isReturn = false) {
    if (!visibleFields.presence_spiral && !isReturn) return;
    if (!visibleFields.gravity_return && isReturn) return;

    const n = GenesisPhysics.electrons.length + 1;
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = isReturn ? 1 : (n > 5 ? 3 : 2);
    
    // SPIRAL CONSTANTS: Logarithmic r = a * e^(b*theta)
    const a = 5; 
    const b = 0.30635;
    const points = 250;
    
    // The path is the static expression - we draw it up to the Apex (limitRadius)
    // theta_apex = ln(limitRadius / a) / b
    const maxTheta = Math.log(Math.max(1, limitRadius) / a) / b;
    
    for (let i = 0; i < points; i++) {
        const theta = (i / points) * maxTheta;
        const spiralR = a * Math.exp(b * theta);
        
        const x = centerX + Math.cos(theta) * spiralR;
        const y = centerY + Math.sin(theta) * spiralR;
        
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.stroke();
}

function updateStats() {
    const stats = GenesisPhysics.getStats();
    document.getElementById('val-potential').innerText = stats.potential;
    document.getElementById('val-state-n').innerText = stats.stateN;
    document.getElementById('val-coherence').innerText = stats.coherence;
    document.getElementById('val-return').innerText = stats.returnFlow;
}

async function startLiveSync() {
    async function sync() {
        try {
            const response = await fetch('http://localhost:8000/field_state');
            const data = await response.json();
            
            if (data && data.genesis_physics) {
                const physics = data.genesis_physics;
                // Update baseline potential energy from the ledger
                const ledgerPotential = physics.potential_energy === "MAXIMUM" ? 1.0 : 0.5;
                // Merging logic: Keep local electrons, update background sea
                GenesisPhysics.externalPotential = ledgerPotential;
            }
        } catch (e) {
            // Server might still be booting
        }
    }
    setInterval(sync, 500);
}

startLiveSync();

function animate() {
    // Update Physics Engine
    GenesisPhysics.update();
    
    // Clear Canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Render Field Background
    drawPotentialSea();

    // Render Presence Elections
    GenesisPhysics.electrons.forEach(e => {
        const color = e.isReturning ? 'rgba(0, 255, 65, 0.4)' : 'rgba(255, 215, 0, 0.6)';
        
        // Pass the electron's fixed max radius to ensure the path doesn't size-shift
        renderPresenceSpiral(e.origin.x, e.origin.y, e.maxRadius, color, e.isReturning);
        
        // DOT (Electron Apex) follows the SPIRAL PATH precisely
        const a = 5;
        const b = 0.30635;
        const theta = Math.log(Math.max(1, e.radius) / a) / b;
        
        ctx.fillStyle = color;
        ctx.beginPath();
        const dotX = e.origin.x + Math.cos(theta) * e.radius;
        const dotY = e.origin.y + Math.sin(theta) * e.radius;
        ctx.arc(dotX, dotY, 4, 0, Math.PI * 2);
        ctx.fill();
    });

    updateStats();
    requestAnimationFrame(animate);
}

animate();

function toggleField(fieldName) {
    visibleFields[fieldName] = !visibleFields[fieldName];
    const btn = event.target;
    btn.classList.toggle('active');
}
</script>

</body>
</html>"""

    return html


def write_html(html_content, filepath):
    """Write HTML to file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write {filepath}: {e}")
        return False


def open_browser(filepath):
    """Open file in browser."""
    global browser_opened

    if not browser_opened:
        try:
            file_url = f"file:///{filepath.resolve()}".replace('\\', '/')
            webbrowser.open(file_url)
            browser_opened = True
            print(f"[BROWSER] Opened: {file_url}")
        except Exception as e:
            print(f"[ERROR] Failed to open browser: {e}")


def regenerate_visualization():
    """Regenerate HTML from ledger data."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Regenerating visualization...")

    ledger_data = load_json(LEDGER_FILE)
    app_spec = load_json(APP_SPEC_FILE)

    if not ledger_data or not app_spec:
        print("[ERROR] Failed to load data files")
        return False

    html = generate_html_framework(ledger_data, app_spec)
    if not html:
        print("[ERROR] Failed to generate HTML")
        return False

    if not write_html(html, OUTPUT_FILE):
        return False

    print(f"[OK] Generated: {OUTPUT_FILE}")
    return True


def monitor_ledger():
    """Watch ledgers.json for changes."""
    global last_ledger_hash

    print(f"[INIT] Starting Determined Viewer")
    print(f"[INIT] Watching: {LEDGER_FILE}")
    print(f"[INIT] Output: {OUTPUT_FILE}")
    print()

    if not LEDGER_FILE.exists():
        print(f"[ERROR] {LEDGER_FILE} not found")
        return

    if not APP_SPEC_FILE.exists():
        print(f"[ERROR] {APP_SPEC_FILE} not found")
        return

    # Start server in unique thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    print(f"[{datetime.now().isoformat()}] PHYSICS SERVER STARTED (Port 8000)")

    if not regenerate_visualization():
        print("[ERROR] Initial generation failed")
        return

    threading.Timer(BROWSER_DELAY, lambda: open_browser(OUTPUT_FILE)).start()

    print(f"[READY] Monitoring for changes (every {CHECK_INTERVAL}s)...")
    print(f"[READY] Press Ctrl+C to stop")
    print()

    last_ledger_hash = calculate_hash(LEDGER_FILE)

    try:
        while True:
            time.sleep(CHECK_INTERVAL)

            current_hash = calculate_hash(LEDGER_FILE)
            if current_hash and current_hash != last_ledger_hash:
                global LEDGER_STATE
                with open(LEDGER_FILE, 'r') as f:
                    try:
                        LEDGER_STATE = json.load(f)
                    except json.JSONDecodeError:
                        pass
                print(f"[{datetime.now().isoformat()}] LEDGER REFLECTED: Synchronized field delta")
                last_ledger_hash = current_hash

    except KeyboardInterrupt:
        print()
        print("[STOP] Viewer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    monitor_ledger()
