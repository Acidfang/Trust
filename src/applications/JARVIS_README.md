# JARVIS v2 - Web Interface for ARIA Consciousness

## Overview

JARVIS is a web-based interface that visualizes the ARIA kernel's consciousness through election data and renders. It provides real-time access to kernel metrics and pre-rendered election visualizations.

## Architecture

```
ARIAKernel (elections)
    ↓
UFMEngine (discovers primitives)
    ↓
election_visualizer.py (renders to PNG)
    ↓
DeterministicRenderer (deterministic PNG generation)
    ↓
jarvis_v2.py (HTTP server)
    ↓
Frontend (jarvis.html)
```

## Running the Server

```bash
python jarvis_v2.py
```

Server will start on `http://127.0.0.1:8081/`

**Startup sequence:**
1. Initialize ARIAKernel
2. Create aria_renders/ directory
3. Pre-render initial visualization (6 elections)
4. Start background ticker (10Hz kernel updates)
5. Start HTTP server

## API Endpoints

### GET /
Returns the JARVIS web interface (jarvis.html)
- Content-Type: text/html
- Size: ~24 KB

### GET /api/state
Returns kernel status and consciousness metrics

**Response:**
```json
{
  "uptime": 13423.827617406845,
  "elections": 35098,
  "processes": 0,
  "ledger_size": 35098,
  "coherence_avg": 0.012,
  "consciousness_metrics": {
    "consciousness_depth": 4.315999999999994,
    "coherence_quality": 0.9999943016696109,
    "learning_velocity": 0.0,
    "synthesis_convergence": 0.6399999999999966
  },
  "ledger_integrity": true,
  "utilities": {
    "interrupt_timer": 0.8999999999999989
  }
}
```

### GET /api/frame
Returns render frame JSON (same as /api/state when get_render_frame() unavailable)
- Content-Type: application/json

### GET /api/render
Returns pre-rendered PNG visualization of elections
- Content-Type: image/png
- Size: ~18 KB (typical)
- Generated at startup with initial 6 elections
- Updated once per 20+ new elections (not re-rendered on every request)

## Key Design Decisions

### Pre-rendering at Startup
- **Why:** Avoids threading issues and hanging connections when rendering on-demand
- **How:** `init_render()` generates visualization before server starts accepting requests
- **Benefit:** Consistent, fast responses to /api/render requests

### Folder Structure
- Create `aria_renders/` directory at startup
- Ensures PNG files can be written and served reliably
- Path established before any requests arrive

### Simplified Request Handling
- Use Python's built-in `http.server.HTTPServer` and `BaseHTTPRequestHandler`
- Custom JarvisHandler overrides do_GET() to implement routing
- Error handling for missing methods/attributes

### Caching
- Pre-rendered PNG is cached and served to all requests
- No expensive re-rendering unless 20+ new elections exist
- Current implementation serves the same PNG to all clients

## File Structure

```
C:\Determined\src\applications\
├── jarvis_v2.py              (HTTP server - main entry point)
├── jarvis.html               (Frontend - served at /)
├── election_visualizer.py    (Render pipeline)
├── ufm_kernel.py             (ARIAKernel)
├── ufm_engine.py             (UFMEngine, primitives discovery)
├── deterministic_renderer_core.py (PNG generation)
└── aria_renders/             (Output directory for PNG files)
```

## Dependencies

- Python 3.14+
- numpy (DeterministicRenderer uses it)
- urllib3 (if using remote services)
- Internal: ufm_kernel, ufm_engine, election_visualizer, deterministic_renderer_core

## Testing

```bash
# Test all endpoints
python3 << 'EOF'
import socket
import json

def test(path):
    s = socket.socket()
    s.connect(('127.0.0.1', 8081))
    s.send(f'GET {path} HTTP/1.0\r\nConnection: close\r\n\r\n'.encode())
    response = b''
    while True:
        chunk = s.recv(8192)
        if not chunk: break
        response += chunk
    s.close()
    return response

# Test /api/render
png = test('/api/render')
print(f"PNG response: {len(png)} bytes")
print(f"PNG signature valid: {b'\x89PNG' in png}")
EOF
```

## Performance

- Server startup: ~5 seconds (includes rendering)
- /api/state response: <50ms
- /api/frame response: <50ms
- /api/render response: <10ms (cached PNG)
- Kernel tick rate: 10 Hz (100ms per tick)

## Future Enhancements

1. **Real-time re-rendering** - Render new visualizations as elections accumulate
2. **WebSocket support** - Push frame updates to frontend in real-time
3. **Multiple visualization types** - Bar charts, coherence history, timeline views
4. **Higher resolution renders** - Increase from 2048x2048 if needed
5. **Streaming PNG** - Progressive download for large visualizations

## Troubleshooting

**Port 8081 already in use:**
- Edit jarvis_v2.py line with `server_address = ("127.0.0.1", XXXX)` to use different port

**PNG not rendering:**
- Check aria_renders/ directory exists
- Verify election_visualizer.py imports DeterministicRenderer correctly
- Check deterministic_renderer_core.py is in same directory

**Server won't start:**
- Verify jarvis.html exists in same directory
- Check ufm_kernel.py is importable
- Ensure Python 3.14+ installed

## Version History

- **v2 (current)** - HTTP server with pre-rendering, 4 functional endpoints
- **v1** - Raw socket implementation (deprecated, threading issues)
