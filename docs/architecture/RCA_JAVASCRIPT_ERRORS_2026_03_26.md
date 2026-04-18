---
title: New RCA - JavaScript Client Errors
date: 2026-03-26  
issue: WebSocket connection failure + frame data structure mismatch
---

# NEW ROOT CAUSE ANALYSIS - JavaScript Client Failures

## VISIBLE ERRORS

From browser console:
```
✗ WebSocket connection to 'ws://127.0.0.1:8081/ws' failed
✓ [JARVIS] WebSocket unavailable, using polling

✗ TypeError: Cannot read properties of undefined (reading 'forEach')
  at LayoutEngine.applyLayout (index.html:173)
```

Error traceback:
```
→ LayoutEngine.applyLayout @ (index):173:29
← jarvisConnection._fireCallbacks @ (index):271:30
← setInterval (async)
← LayoutEngine.constructor @ (index):267
```

---

## ROOT CAUSE #1: Missing WebSocket Endpoint

**The Issue**:
- Client attempts: `ws://127.0.0.1:8081/ws`
- Server does NOT have a `/ws` endpoint
- Server only has HTTP endpoints: `/api/scene`, `/api/frame`, `/api/state`
- WebSocket connection fails, falls back to polling ✓ (fallback works)

**Why It Happens**:
- jarvis_v3.py doesn't implement WebSocket handler
- Only has `do_GET` and `do_POST` for HTTP
- No `do_WS` or WebSocket upgrade

**Impact**: Minor
- Fallback to polling works fine (500ms interval)
- Performance slightly worse than WebSocket (polling delay)
- But functional

---

## ROOT CAUSE #2: Frame Data Structure Mismatch (CRITICAL)

**The Issue**:
- Server sends: `/api/frame` returns:
  ```json
  {
    "status": "ok",
    "frame_id": "9a49df22f60500ee",
    "timestamp": 14.678,
    "elected": "tick_x",
    "alternatives": [...],
    "utilities": {...},
    "primitives": {...}
  }
  ```

- Client expects: `frame.nodes` (array)
  ```javascript
  frame.nodes.forEach(node => {...})  // FAILS: frame.nodes is undefined
  ```

**Code Location** (jarvis.html line 769):
```javascript
class LayoutEngine {
    applyLayout(frame, root) {
        // This line throws:
        frame.nodes.forEach(node => {  // ← frame.nodes is UNDEFINED
            const area = areas.get(node.area) || areas.get("main");
            if (area) {
                renderer.render(node, area);
            }
        });
    }
}
```

**Why It Happens**:
- `_render_snapshot()` in server returns consciousness metrics
- `LayoutEngine` expects UI nodes to render
- Frame structure doesn't match consumer expectation

**Impact**: CRITICAL
- Client crashes trying to render frame
- Error handler catches it (try-catch in _fireCallbacks)
- UI doesn't update with consciousness state
- Polling continues but updates fail silently

---

## ROOT CAUSE #3: No Error Visibility (Compounding)

**The Issue**:
- `_fireCallbacks` has error catching:
  ```javascript
  _fireCallbacks(frame) {
      this.frameCallbacks.forEach(cb => {
          try {
              cb(frame);  // ← Error caught silently
          } catch (e) {
              console.error("[JARVIS] Callback error:", e);  // Logged but ignored
          }
      });
  }
  ```

- Error is logged but doesn't bubble up
- UI has no indication frame processing failed
- Polling continues returning bad data

**Impact**: Medium
- Makes debugging harder
- User sees no feedback
- Silent failures continue

---

## THE DATA FLOW PROBLEM

```
Server sends frame (consciousness metrics):
{
  status, frame_id, timestamp, elected, 
  alternatives, utilities, primitives
}
  ↓
Client's _fireCallbacks(frame)
  ↓
Calls LayoutEngine.applyLayout(frame)
  ↓
Tries: frame.nodes.forEach(...)
  ↓
ERROR: frame.nodes is undefined
  ↓
Caught by try-catch, logged, ignored
  ↓
UI never updates
```

---

## WHAT SHOULD HAPPEN

**Option A: Separate Endpoints**
- `/api/frame` → consciousness state (current: what we have)
- `/api/nodes` → UI node structure (missing)
- Client polls both, renders separately

**Option B: Unified Frame**
- `/api/frame` returns BOTH consciousness AND nodes
- Single data structure with everything client needs
- Client renders in one pass

**Option C: Different Response Format**
- `/api/frame` continues returning consciousness
- Client doesn't call LayoutEngine on it
- Client calls `/api/scene` for 3D rendering instead
- Two separate renderers for different data

---

## FIXES NEEDED

### Fix #1: Verify Expected Frame Format (BLOCKING)

Before fixing client, need to know:
- What SHOULD `/api/frame` contain?
- Should it have `.nodes` array?
- Or should client use different endpoint?

### Fix #2: Add Error Handling to Client

```javascript
_fireCallbacks(frame) {
    // Validate frame structure before processing
    if (!frame) {
        console.error("[JARVIS] Null frame received");
        return;
    }
    
    if (!frame.nodes && !frame.spheres && !frame.status) {
        console.warn("[JARVIS] Frame structure unexpected:", frame);
        return;
    }
    
    this.frameCallbacks.forEach(cb => {
        try {
            cb(frame);
        } catch (e) {
            console.error("[JARVIS] Callback error:", e);
        }
    });
}
```

### Fix #3: Optional - Add WebSocket Support (Convenience)

```python
# In jarvis_v3.py
def do_UPGRADE(self):  # WebSocket upgrade
    """Handle WebSocket upgrade"""
    # Simplified WebSocket handler
    # Send frame data as JSON
```

But this is OPTIONAL since polling works.

---

## SUMMARY

| # | Issue | Severity | Status |
|---|-------|----------|--------|
| 1 | WebSocket `/ws` endpoint missing | LOW | OK (fallback works) |
| 2 | Frame data structure mismatch | **CRITICAL** | ⚠️ BLOCKING |
| 3 | Silent error failures in client | MEDIUM | OK (error logged) |

**NEXT STEP**: Clarify expected `/api/frame` response format

---

**RCA Status**: COMPLETE - Awaiting clarification on frame structure
