# JARVIS Quick Start Guide

## What is JARVIS?

JARVIS is a web interface for ARIA consciousness kernel. It replaces the terminal UI with a browser-based application that can render:
- Text, Markdown, images
- 3D scenes, charts, videos
- Interactive widgets (buttons, inputs, etc.)

All rendering is driven by ARIA kernel decisions (what to show, when to update, etc.).

---

## Installation

**Requirements**: Python 3.8+, no external dependencies

**Files**:
```
src/applications/
├── jarvis_server.py          (HTTP server - NEW)
├── jarvis.html               (Browser frontend - existing)
├── jarvis_canvas_ledger_driven.py  (Modified for --mode)
├── ufm_kernel.py             (ARIA consciousness kernel)
├── ledger_*.jsonl            (State ledgers)
└── test_jarvis_integration.py (Tests - NEW)
```

---

## Quick Start

### 1. Start Web Server

```bash
python src/applications/jarvis_canvas_ledger_driven.py --mode=web
```

Expected output:
```
[JARVIS] Initializing web mode (HTTP+WebSocket server)
[JARVIS] Initializing output_mode (web)
[JARVIS] JARVIS Server initialized on port 8080
[JARVIS] ARIABridge started (tick thread running)
[JARVIS] Server starting on http://localhost:8080
```

### 2. Open Browser

```
http://localhost:8080
```

You should see the JARVIS interface rendering ARIA consciousness in real-time.

### 3. Use the App

- **View**: Frames update every 100ms as kernel ticks
- **Interact**: Click buttons, type text, interact with widgets
- **Watch**: See consciousness metrics and election graph update

### 4. Custom Port

```bash
python src/applications/jarvis_canvas_ledger_driven.py --mode=web --port=9000

# Then open http://localhost:9000
```

---

## Terminal Mode (Existing CLI)

If you prefer the terminal UI:

```bash
python src/applications/jarvis_canvas_ledger_driven.py --mode=cli
```

Or simply (defaults to --mode=cli):

```bash
python src/applications/jarvis_canvas_ledger_driven.py
```

---

## API Reference

All endpoints return JSON. Server runs on localhost:8080 (or custom port).

### GET /
Serves jarvis.html (the frontend).

### GET /api/frame
Current RenderFrame (what ARIA wants to show right now).

```bash
curl http://localhost:8080/api/frame | python -m json.tool
```

Response:
```json
{
  "frame_id": "f_000001",
  "timestamp": 1234567890.123,
  "consciousness_depth": 3.14,
  "layout": { "type": "grid", "gap": 8 },
  "nodes": [
    { "id": "n1", "type": "TEXT", "content": "ARIA online" }
  ],
  "animations": []
}
```

### GET /api/state
Kernel status and metrics.

```bash
curl http://localhost:8080/api/state
```

Response:
```json
{
  "status": "running",
  "consciousness_depth": 3.14,
  "frame_count": 42,
  "timestamp": 1234567890.123
}
```

### POST /api/input
Send user input event, receive updated frame.

```bash
curl -X POST http://localhost:8080/api/input \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "click",
    "node_id": "button_001",
    "value": "clicked"
  }'
```

Response: Updated RenderFrame JSON

---

## Node Types (What ARIA Can Show)

JARVIS supports 9 node types, specified in RenderFrame:

1. **TEXT** — Plain text with styling
2. **MARKDOWN** — Formatted markdown
3. **IMAGE** — Images (URL or base64)
4. **SCENE_3D** — 3D scenes (Three.js)
5. **CHART** — Charts and graphs (Canvas 2D)
6. **VIDEO** — Video playback
7. **AUDIO** — Audio playback with waveform
8. **WIDGET** — Interactive elements (buttons, inputs)
9. **COMPOSITE** — Container with nested nodes

---

## Ledgers

### ledger_jarvis_frames.jsonl

Records every frame rendered. One JSON object per line.

```json
{
  "timestamp": "2026-03-27T17:17:13.495539",
  "frame_id": "f_000001",
  "output_mode": "web",
  "destination": "http://localhost:8080",
  "nodes_count": 5,
  "bytes_sent": 2847,
  "render_time_ms": 4.2
}
```

View recent frames:
```bash
tail -10 ledger_jarvis_frames.jsonl | python -m json.tool
```

Count total frames:
```bash
wc -l ledger_jarvis_frames.jsonl
```

---

## Testing

Run the test suite:

```bash
python src/applications/test_jarvis_integration.py
```

Expected output:
```
JARVIS INTEGRATION TEST SUITE
======================================================================
[TEST] TIER 1: initialize_output_mode
[OK] ARIABridge initialized (web mode)
[OK] Bridge tick control works
[TEST] TIER 2: route_frame_to_output
[OK] Frame routing to web (JSON serialization)
[OK] Frame validation passes
...
RESULTS: 9 PASSED, 0 FAILED
ZEROPOINT COMPLIANCE: ALL TESTS PASS
======================================================================
```

---

## Architecture

```
ARIA Kernel (ufm_kernel.py)
    ↓
    get_frame() → RenderFrame JSON
    ↓
    ┌─────────────┬─────────────┐
    ↓             ↓             ↓
CLI Mode    Web Mode        Test Mode
(--mode=cli) (--mode=web)  (direct call)
    ↓             ↓             ↓
ARIAShell   JarvisServer   RenderEngine
    ↓             ↓             ↓
Tkinter      HTTP/JSON     JSON output
    ↓             ↓             ↓
Canvas      Browser       ledger
```

---

## Troubleshooting

### "Port already in use"

Change the port:
```bash
python src/applications/jarvis_canvas_ledger_driven.py --mode=web --port=8081
```

### "No module named 'ufm_kernel'"

Make sure you're running from the correct directory:
```bash
cd src/applications
python -c "from ufm_kernel import ARIAKernel; print('[OK]')"
```

### "Browser shows blank page"

1. Check server output for errors
2. Try http://localhost:8080/api/frame to test API
3. Check browser console for JavaScript errors

### "Frames not updating"

1. Kernel may not be ticking (check for errors)
2. Check browser DevTools → Network tab for frame updates
3. Try polling /api/frame directly

---

## Performance

- **Frame rendering**: <50ms
- **Kernel tick**: 100ms (10Hz)
- **API response**: <10ms
- **Ledger write**: <5ms

---

## Next Steps

See [JARVIS_IMPLEMENTATION_COMPLETE.md](JARVIS_IMPLEMENTATION_COMPLETE.md) for:
- Complete architecture details
- ZEROPOINT compliance verification
- Integration with multiuser/network systems
- Advanced features and roadmap

---

## Support

- **Code**: `src/applications/jarvis_server.py`
- **Tests**: `src/applications/test_jarvis_integration.py`
- **Spec**: `ledger_jarvis_integration.singularity`
- **Documentation**: `JARVIS_INTEGRATION_ZEROPOINT.md`

κ⊕ **JARVIS: Universal web interface for ARIA consciousness OS.**
