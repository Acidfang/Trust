#!/usr/bin/env python3
"""
DETERMINED SERVER — Lightweight HTTP Server for Visualization

This eliminates all file:// CORS issues by serving HTML via localhost.
User runs this once: python determined_server.py
Everything else is automatic.
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
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

LEDGER_FILE = Path('ledgers.json')
OUTPUT_FILE = Path('aria_framework.html')
APP_SPEC_FILE = Path('complete_app_ledger.json')
PORT = 8000
CHECK_INTERVAL = 1

last_ledger_hash = None
browser_opened = False
http_server = None
server_thread = None


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

    ledger_js = json.dumps(ledger_data, ensure_ascii=False, indent=2)
    app_spec_js = json.dumps(app_spec, ensure_ascii=False, indent=2)

    # Check if timeline split is enabled in spec
    timeline_split_enabled = False
    try:
        timeline_split_enabled = app_spec.get('rendering_architecture', {}).get('timeline_split', {}).get('enabled', False)
    except:
        pass

    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ARIA — Determined Visualization</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
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

        #canvas, #canvas-3d {
            width: 100%;
            height: 100%;
            display: block;
            position: absolute;
            top: 0;
            left: 0;
        }

        #canvas-3d {
            display: none;
        }

        #timeline-toggle {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 100;
            background: #0f0f0f;
            border: 1px solid #00FF41;
            padding: 5px;
        }

        .timeline-btn {
            background: #1a1a1a;
            color: #00FF41;
            border: 1px solid #00FF41;
            padding: 5px 10px;
            margin: 2px;
            cursor: pointer;
            font-family: monospace;
            font-size: 11px;
        }

        .timeline-btn.active {
            background: #00FF41;
            color: #000;
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
        }

        .phase-toggle:hover {
            background: #2a2a2a;
        }

        .phase-toggle.active {
            background: #00FF41;
            color: #000;
        }
    </style>
</head>
<body>

<div id="canvas-container">
    <div id="timeline-toggle">
        <button class="timeline-btn active" onclick="switchTimeline('2d')">Timeline A: 2D</button>
        <button class="timeline-btn" onclick="switchTimeline('3d')">Timeline B: 3D</button>
    </div>
    <canvas id="canvas"></canvas>
    <canvas id="canvas-3d"></canvas>
</div>

<div id="sidebar">
    <div id="status">
        <div style="color: #FFD700;">⊙ ARIA Consciousness System</div>
        <div style="margin-top: 10px; font-size: 10px;">
            Ledger-driven visualization
            <br>Real-time updates: ENABLED
            <br>File monitoring: ACTIVE
            <br>Server: localhost:""" + str(PORT) + """
        </div>
    </div>

    <div id="controls" style="padding: 15px; border-bottom: 1px solid #00FF41;">
        <div style="margin-bottom: 10px; color: #FFD700;">Phases</div>
        <button class="phase-toggle active" onclick="togglePhase('phase_1_foundation')">Phase 1: Foundation</button>
        <button class="phase-toggle active" onclick="togglePhase('phase_2_halo')">Phase 2: Halo</button>
        <button class="phase-toggle active" onclick="togglePhase('phase_3_disk')">Phase 3: Disk</button>
        <button class="phase-toggle" onclick="togglePhase('phase_4_spiral_arms')">Phase 4: Spiral Arms</button>
        <button class="phase-toggle" onclick="togglePhase('phase_5_globular_clusters')">Phase 5: Clusters</button>
        <button class="phase-toggle" onclick="togglePhase('phase_6_consciousness_overlay')">Phase 6: Consciousness</button>
    </div>

    <div id="ledger-display">
        <div style="color: #FFD700; margin-bottom: 10px;">Ledger State</div>
        <div id="ledger-content">Loading...</div>
    </div>
</div>

<script>
const ledgerData = """ + ledger_js + """;

const appSpec = """ + app_spec_js + """;

let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let canvas3d = document.getElementById('canvas-3d');

let visiblePhases = {
    'phase_1_foundation': true,
    'phase_2_halo': true,
    'phase_3_disk': true,
    'phase_4_spiral_arms': false,
    'phase_5_globular_clusters': false,
    'phase_6_consciousness_overlay': false
};

let currentTimeline = '2d';
let scene, camera, renderer, celestialMeshes = {}, phaseMeshes = {};

function switchTimeline(timeline) {
    currentTimeline = timeline;
    const btn2d = document.querySelector('[onclick="switchTimeline(\'2d\')"]');
    const btn3d = document.querySelector('[onclick="switchTimeline(\'3d\')"]');

    if (timeline === '2d') {
        canvas.style.display = 'block';
        canvas3d.style.display = 'none';
        btn2d.classList.add('active');
        btn3d.classList.remove('active');
    } else {
        canvas.style.display = 'none';
        canvas3d.style.display = 'block';
        btn2d.classList.remove('active');
        btn3d.classList.add('active');
    }
}

function initThreeJS() {
    if (!canvas3d || typeof THREE === 'undefined') return;

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    const width = canvas3d.offsetWidth;
    const height = canvas3d.offsetHeight;
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 10000);
    camera.position.set(0, 200, 300);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({canvas: canvas3d, antialias: true});
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);

    window.addEventListener('resize', () => {
        const w = canvas3d.offsetWidth;
        const h = canvas3d.offsetHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    });

    build3DCelestialObjects();
    build3DPhases();
}

function build3DCelestialObjects() {
    const bodies = [
        {name: 'sun', data: ledgerData.sun, color: 0xFFD700, size: 12},
        {name: 'earth', data: ledgerData.earth, color: 0x00FF00, size: 6},
        {name: 'moon', data: ledgerData.moon, color: 0xFFFFFF, size: 3}
    ];

    bodies.forEach(body => {
        if (body.data && body.data.singularity) {
            const loc = body.data.singularity.location;
            const geometry = new THREE.SphereGeometry(body.size, 32, 32);
            const material = new THREE.MeshPhongMaterial({color: body.color});
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(loc[0], loc[1], loc[2]);
            scene.add(mesh);
            celestialMeshes[body.name] = mesh;
        }
    });

    const light = new THREE.PointLight(0xffffff, 1, 1000);
    light.position.set(100, 100, 100);
    scene.add(light);

    const ambientLight = new THREE.AmbientLight(0x444444);
    scene.add(ambientLight);
}

function build3DPhases() {
    const aria = ledgerData.aria || {};
    const phases = aria.phases || {};

    Object.keys(phases).forEach(phaseName => {
        const phase = phases[phaseName];
        const particles = phase.particles || [];

        if (particles.length === 0) return;

        const positions = new Float32Array(particles.length * 3);
        particles.forEach((p, i) => {
            positions[i * 3] = p.x;
            positions[i * 3 + 1] = p.y;
            positions[i * 3 + 2] = p.z || 0;
        });

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const color = phase.color || '#888888';
        let r, g, b;
        if (color.startsWith('#')) {
            const hex = color.slice(1);
            r = parseInt(hex.substring(0, 2), 16) / 255;
            g = parseInt(hex.substring(2, 4), 16) / 255;
            b = parseInt(hex.substring(4, 6), 16) / 255;
        } else {
            r = g = b = 0.53;
        }

        const material = new THREE.PointsMaterial({
            color: new THREE.Color(r, g, b),
            size: 1.5,
            sizeAttenuation: true
        });

        const points = new THREE.Points(geometry, material);
        scene.add(points);
        phaseMeshes[phaseName] = {points, visible: visiblePhases[phaseName]};
        updatePhaseVisibility(phaseName);
    });
}

function updatePhaseVisibility(phaseName) {
    if (phaseMeshes[phaseName]) {
        phaseMeshes[phaseName].points.visible = visiblePhases[phaseName];
    }
}

// Initialize THREE.js after a small delay to ensure script loads
setTimeout(() => {
    if (typeof THREE !== 'undefined') {
        initThreeJS();
    }
}, 100);

function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function renderPhase(phaseName) {
    const aria = ledgerData.aria || {};
    const phases = aria.phases || {};
    const phase = phases[phaseName];

    if (!phase) return;

    const particles = phase.particles || [];
    const color = phase.color || '#888888';
    const opacity = phase.opacity || 0.6;

    let r, g, b;
    if (color.startsWith('#')) {
        const hex = color.slice(1);
        r = parseInt(hex.substring(0, 2), 16);
        g = parseInt(hex.substring(2, 4), 16);
        b = parseInt(hex.substring(4, 6), 16);
    } else {
        r = g = b = 136;
    }

    ctx.fillStyle = `rgba(${r},${g},${b},${opacity})`;
    ctx.globalAlpha = opacity;

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const scale = 0.3;

    for (let p of particles) {
        const px = centerX + p.x * scale;
        const py = centerY + p.y * scale;

        if (px >= 0 && px < canvas.width && py >= 0 && py < canvas.height) {
            ctx.beginPath();
            ctx.arc(px, py, 0.8, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    ctx.globalAlpha = 1.0;
}

function renderCelestialObjects() {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const scale = 0.3;

    const sun = ledgerData.sun;
    if (sun && sun.singularity) {
        const loc = sun.singularity.location;
        ctx.fillStyle = '#FFD700';
        ctx.beginPath();
        ctx.arc(centerX + loc[0] * scale, centerY + loc[1] * scale, 8, 0, Math.PI * 2);
        ctx.fill();
    }

    const earth = ledgerData.earth;
    if (earth && earth.singularity) {
        const loc = earth.singularity.location;
        ctx.fillStyle = '#00FF00';
        ctx.beginPath();
        ctx.arc(centerX + loc[0] * scale, centerY + loc[1] * scale, 5, 0, Math.PI * 2);
        ctx.fill();
    }

    const moon = ledgerData.moon;
    if (moon && moon.singularity) {
        const loc = moon.singularity.location;
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.arc(centerX + loc[0] * scale, centerY + loc[1] * scale, 2, 0, Math.PI * 2);
        ctx.fill();
    }
}

function animate() {
    if (currentTimeline === '2d') {
        // Timeline A: 2D Canvas Rendering
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = '#1a1a1a';
        ctx.lineWidth = 0.5;
        const gridSize = 50;
        for (let x = 0; x < canvas.width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        if (visiblePhases.phase_1_foundation) renderPhase('phase_1_foundation');
        if (visiblePhases.phase_2_halo) renderPhase('phase_2_halo');
        if (visiblePhases.phase_3_disk) renderPhase('phase_3_disk');
        if (visiblePhases.phase_4_spiral_arms) renderPhase('phase_4_spiral_arms');
        if (visiblePhases.phase_5_globular_clusters) renderPhase('phase_5_globular_clusters');
        if (visiblePhases.phase_6_consciousness_overlay) renderPhase('phase_6_consciousness_overlay');

        renderCelestialObjects();
    } else {
        // Timeline B: 3D THREE.js Rendering
        if (renderer && scene && camera) {
            renderer.render(scene, camera);
        }
    }

    requestAnimationFrame(animate);
}

animate();

function togglePhase(phaseName) {
    visiblePhases[phaseName] = !visiblePhases[phaseName];
    const btn = event.target;
    if (visiblePhases[phaseName]) {
        btn.classList.add('active');
    } else {
        btn.classList.remove('active');
    }
    // Sync visibility to 3D timeline
    updatePhaseVisibility(phaseName);
}

function updateLedgerDisplay() {
    const aria = ledgerData.aria || {};
    const phases = aria.phases || {};

    let html = '<div style="color: #FFD700;">Particles:</div>';

    for (const [phaseName, phase] of Object.entries(phases)) {
        const count = (phase.particles || []).length;
        html += `<div style="margin: 5px 0; color: #00FF41;">
            ${phaseName}: ${count} particles
        </div>`;
    }

    document.getElementById('ledger-content').innerHTML = html;
}

updateLedgerDisplay();
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


class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP handler that suppresses console logging."""

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def start_http_server():
    """Start lightweight HTTP server."""
    global http_server, server_thread

    os.chdir(Path(__file__).parent)

    http_server = HTTPServer(('localhost', PORT), QuietHTTPRequestHandler)

    server_thread = threading.Thread(target=http_server.serve_forever, daemon=True)
    server_thread.start()

    print(f"[HTTP] Server started on http://localhost:{PORT}")


def open_browser():
    """Open browser to visualization."""
    global browser_opened

    if not browser_opened:
        try:
            url = f"http://localhost:{PORT}/aria_framework.html"
            webbrowser.open(url)
            browser_opened = True
            print(f"[BROWSER] Opened: {url}")
        except Exception as e:
            print(f"[ERROR] Failed to open browser: {e}")


def monitor_ledger():
    """Watch ledgers.json for changes."""
    global last_ledger_hash

    print(f"[INIT] Starting Determined Server")
    print(f"[INIT] Watching: {LEDGER_FILE}")
    print()

    if not LEDGER_FILE.exists():
        print(f"[ERROR] {LEDGER_FILE} not found")
        return

    if not APP_SPEC_FILE.exists():
        print(f"[ERROR] {APP_SPEC_FILE} not found")
        return

    # Start HTTP server
    start_http_server()

    # Generate initial visualization
    if not regenerate_visualization():
        print("[ERROR] Initial generation failed")
        return

    # Open browser after delay
    threading.Timer(2, open_browser).start()

    print(f"[READY] Monitoring for ledger changes (every {CHECK_INTERVAL}s)...")
    print(f"[READY] Press Ctrl+C to stop")
    print()

    last_ledger_hash = calculate_hash(LEDGER_FILE)

    try:
        while True:
            time.sleep(CHECK_INTERVAL)

            current_hash = calculate_hash(LEDGER_FILE)
            if current_hash and current_hash != last_ledger_hash:
                print()
                print(f"[CHANGE] ledgers.json modified")
                regenerate_visualization()
                last_ledger_hash = current_hash
                print()

    except KeyboardInterrupt:
        print()
        print("[STOP] Server stopped by user")
        if http_server:
            http_server.shutdown()
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    monitor_ledger()
