# Server Health Polling Documentation

## Overview

The `poll_server_health` method in `LedgerQuery` provides real-time monitoring of application health status. It continuously checks server heartbeats and makes visibility determinations about whether apps are alive, stale, or dead.

## Method Signature

```python
def poll_server_health(self, app_name: str, poll_timeout: float = 5.0) -> Dict[str, Any]
```

## Parameters

- **app_name** (str): The name of the application to poll (e.g., "tkinter_canvas", "html_browser")
- **poll_timeout** (float): Maximum time in seconds for the polling operation (default: 5.0)

## Return Value

Returns a dictionary containing:

```python
{
    "is_alive": bool,              # True if app has recent heartbeat
    "last_update": str,            # ISO timestamp of last heartbeat
    "status": str,                 # One of: "running", "stale", "dead", "error"
    "health_score": float,         # 0.0-1.0 (1.0 = perfect, 0.0 = dead)
    "record_id": str               # Unique ID of health record written to ledger
}
```

## Status Values

| Status | Meaning | Condition |
|--------|---------|-----------|
| `running` | App is healthy and responding | Heartbeat < 10× refresh interval |
| `stale` | App exists but not responding | Heartbeat between 10-100× refresh interval |
| `dead` | App not responding or disabled | No heartbeat or > 100× refresh interval |
| `error` | Polling error | Invalid timestamp format or other error |

## Health Score Calculation

The health_score is calculated based on time since last heartbeat:

```
running:  health_score = max(0.0, 1.0 - (time_since_ms / stale_threshold_ms) * 0.5)
stale:    health_score = max(0.0, 1.0 - (time_since_ms / dead_threshold_ms))
dead:     health_score = 0.0
```

Where:
- `stale_threshold = refresh_interval × 10`
- `dead_threshold = refresh_interval × 100`

## Usage Examples

### Basic Health Check

```python
from ledger_query import LedgerQuery

ledger = LedgerQuery("./ledger")
ledger.load_all()

# Poll an app
result = ledger.poll_server_health("tkinter_canvas")

print(f"App Status: {result['status']}")
print(f"Is Alive: {result['is_alive']}")
print(f"Health: {result['health_score']:.2f}")
```

### Monitoring Multiple Apps

```python
apps_to_monitor = ["tkinter_canvas", "html_browser", "api_server"]

for app_name in apps_to_monitor:
    result = ledger.poll_server_health(app_name)
    print(f"{app_name}: {result['status']} ({result['health_score']:.2f})")
```

### Continuous Monitoring Loop

```python
import time
import json

def monitor_servers(ledger, app_names, interval: float = 1.0):
    """Monitor multiple servers continuously."""
    while True:
        print(f"\n[{datetime.now().isoformat()}] Health Check")
        
        for app_name in app_names:
            result = ledger.poll_server_health(app_name)
            
            # Alert on state changes
            if result['status'] == 'dead':
                print(f"  ⚠️  {app_name}: DEAD")
            elif result['status'] == 'stale':
                print(f"  ⚠️  {app_name}: STALE")
            else:
                print(f"  ✓ {app_name}: {result['status']}")
        
        time.sleep(interval)

# Usage
apps = ["tkinter_canvas", "html_browser"]
monitor_servers(ledger, apps, interval=2.0)
```

### Dashboard Integration

```python
# Get health status for dashboard display
health_statuses = {}
for app_name in ["tkinter_canvas", "html_browser"]:
    health = ledger.poll_server_health(app_name)
    health_statuses[app_name] = {
        "status": health['status'],
        "score": health['health_score'],
        "alive": health['is_alive']
    }

# Pass to dashboard renderer
dashboard_data = {
    "title": "Server Health",
    "servers": health_statuses,
    "timestamp": datetime.now().isoformat()
}
```

## Ledger Storage

### Health Records (ledger_server_health.jsonl)

Each poll creates an entry in `ledger_server_health.jsonl`:

```json
{
  "id": "health:tkinter_canvas:2025-01-15T10:30:45.123456",
  "timestamp": "2025-01-15T10:30:45.123456",
  "app": "tkinter_canvas",
  "status": "running",
  "is_alive": true,
  "health_score": 0.99,
  "last_update": "2025-01-15T10:30:44.000000",
  "poll_duration_ms": 0.51
}
```

### Audit Trail (ledger_audit.jsonl)

Each health poll is also recorded in the audit trail:

```json
{
  "id": "audit:app:tkinter_canvas:2025-01-15T10:30:45.123456",
  "timestamp": "2025-01-15T10:30:45.123456",
  "user": "system:health_monitor",
  "operation": "server_health_poll",
  "target_type": "app",
  "target_id": "tkinter_canvas",
  "action": "health_check: running",
  "new_state": {
    "status": "running",
    "health_score": 0.99
  }
}
```

## Integration with Sync Config

The method reads from `ledger_sync_config.json`:

```json
{
  "apps": {
    "tkinter_canvas": {
      "enabled": true,
      "refresh_interval_ms": 100,
      "last_update": "2025-01-15T10:30:44.000000"
    }
  }
}
```

For each app, it uses:
- `enabled`: Whether app is active
- `refresh_interval_ms`: Heartbeat frequency (for calculating staleness thresholds)
- `last_update`: Most recent heartbeat timestamp

## Architecture

The health polling system follows the **intent-first principle**:

1. **Intent**: Query app heartbeat status
2. **Input**: App name and sync config from ledger
3. **Processing**: Calculate health based on time since last update
4. **Output**: Health status dict
5. **Recording**: Write records to ledger for audit trail
6. **Effect**: System observers can monitor app health

### Timeouts and Thresholds

```
App Config (sync_config):
  ├─ refresh_interval_ms: How often heartbeat updates
  └─ last_update: Most recent heartbeat

Health Thresholds (derived):
  ├─ stale_threshold = refresh_interval × 10 (10 missed beats)
  ├─ dead_threshold = refresh_interval × 100 (100 missed beats)
  └─ Disabled apps = always dead

Status Determination:
  ├─ time < stale_threshold → running
  ├─ stale_threshold ≤ time < dead_threshold → stale
  ├─ time ≥ dead_threshold → dead
  └─ !enabled → dead
```

## Error Handling

The method handles various error conditions gracefully:

```python
# App not in config
result = ledger.poll_server_health("unknown_app")
# → status: "error", health_score: 0.0

# Invalid timestamp format
# → status: "error", health_score: 0.0

# File I/O error writing to ledger
# → Printed to console but poll still succeeds
```

## Performance

- **Poll Duration**: Typically < 1ms
- **Ledger Write**: ~1-5ms depending on disk I/O
- **Memory**: Minimal (reads only last_update timestamp)

## Best Practices

1. **Regular Polling**: Poll every 1-5 seconds for responsive monitoring
2. **Batch Polling**: Check multiple apps in one loop to reduce overhead
3. **Alert on Status Changes**: Track previous status and alert on transitions
4. **Dashboard Integration**: Display health in real-time dashboards
5. **Cleanup**: Periodically rotate health ledger to prevent unbounded growth

## Example: Full Monitoring Setup

```python
import time
import threading
from datetime import datetime

class ServerMonitor:
    def __init__(self, ledger, apps_to_monitor):
        self.ledger = ledger
        self.apps = apps_to_monitor
        self.status_cache = {}
        self.running = False
    
    def start_monitoring(self, interval: float = 2.0):
        """Start background monitoring thread."""
        self.running = True
        thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        thread.start()
        return thread
    
    def _monitor_loop(self, interval: float):
        """Background monitoring loop."""
        while self.running:
            for app_name in self.apps:
                try:
                    result = self.ledger.poll_server_health(app_name)
                    
                    # Detect status changes
                    old_status = self.status_cache.get(app_name)
                    new_status = result['status']
                    
                    if old_status != new_status:
                        print(f"[ALERT] {app_name}: {old_status} → {new_status}")
                    
                    self.status_cache[app_name] = new_status
                    
                except Exception as e:
                    print(f"[ERROR] Failed to poll {app_name}: {e}")
            
            time.sleep(interval)
    
    def get_status(self, app_name: str) -> str:
        """Get current cached status."""
        return self.status_cache.get(app_name, "unknown")
    
    def stop_monitoring(self):
        """Stop monitoring thread."""
        self.running = False

# Usage
ledger = LedgerQuery("./ledger")
ledger.load_all()

monitor = ServerMonitor(
    ledger,
    apps_to_monitor=["tkinter_canvas", "html_browser", "api_server"]
)

monitor_thread = monitor.start_monitoring(interval=2.0)

# Main app continues running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    monitor.stop_monitoring()
    monitor_thread.join()
```

## Troubleshooting

### App Shows "dead" But Should Be Alive

1. Check `last_update` timestamp in sync_config
2. Verify app is actually running and updating heartbeat
3. Check `refresh_interval_ms` is set correctly
4. Look for errors in `poll_duration_ms` (suggests I/O lag)

### Health Score Not Updating

1. Ensure `ledger_sync_config.json` exists
2. Check app is enabled in config
3. Verify heartbeat is being updated by the app
4. Check file permissions on ledger directory

### Ledger File Growing Too Large

1. Implement rolling cleanup of old records
2. Archive health records to separate storage
3. Adjust polling interval to reduce frequency
