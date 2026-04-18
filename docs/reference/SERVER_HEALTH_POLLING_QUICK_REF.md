# Server Health Polling - Quick Reference

## 30-Second Overview

```python
# Poll an app's health
result = ledger.poll_server_health("tkinter_canvas")

# Results: running (great), stale (slowing down), dead (not responding)
print(result['status'])        # "running" | "stale" | "dead" | "error"
print(result['health_score'])  # 0.0-1.0 (1.0 = healthy, 0.0 = dead)
print(result['is_alive'])      # True | False
```

---

## Status Reference

| Status | What It Means | What To Do |
|--------|--------------|-----------|
| `running` | ✓ App is healthy and responsive | Monitor for degradation |
| `stale` | ⚠️ App not responding but not dead | Check logs, may recover |
| `dead` | ✗ App not responding or disabled | Alert user, investigate |
| `error` | ? Polling failed | Check ledger config |

---

## Health Score Interpretation

```
0.90-1.00 ✓ Excellent  (recent heartbeat)
0.70-0.89 ✓ Good       (slightly delayed)
0.50-0.69 ⚠ Degraded   (becoming stale)
0.20-0.49 ✗ Poor       (seriously failing)
0.00-0.19 ✗ Critical   (about to die)
```

---

## One-Line Examples

```python
# Is app alive?
if ledger.poll_server_health("app_name")['is_alive']:
    print("✓ App is running")

# Get status string
status = ledger.poll_server_health("app_name")['status']

# Dashboard data
for app in ["server1", "server2"]:
    health = ledger.poll_server_health(app)
    print(f"{app}: {health['status']} ({health['health_score']:.0%})")

# Alert if dead
result = ledger.poll_server_health("app_name")
if result['status'] == 'dead':
    send_alert(f"App is dead: {result}")
```

---

## Integration Patterns

### Background Monitoring
```python
from health_monitoring_utils import HealthMonitor

# Start monitor
monitor = HealthMonitor(ledger, apps=["app1", "app2", "app3"])
monitor.start()

# Get dashboard update anytime
dashboard_data = monitor.get_dashboard_data()
```

### Alert Handling
```python
def on_app_down(event):
    print(f"🚨 {event['app']} died!")

monitor.register_alert(on_app_down)
```

### Uptime Analysis
```python
from health_monitoring_utils import HealthAnalyzer

history = monitor.get_history("app_name", lookback_minutes=60)
uptime_pct = HealthAnalyzer.calculate_uptime(history)
print(f"Uptime (1h): {uptime_pct:.1f}%")
```

---

## Configuration

**What does polling use?**  
→ `ledger_sync_config.json` (the sync config for your apps)

**What should be in sync_config?**
```json
{
  "apps": {
    "my_app": {
      "enabled": true,                    # App is running?
      "refresh_interval_ms": 100,         # How often app updates
      "last_update": "2025-01-15T..."     # When did it last update?
    }
  }
}
```

**Where do results go?**  
→ Two ledger files (automatically):
- `ledger_server_health.jsonl` - Health records
- `ledger_audit.jsonl` - Audit trail

---

## Common Tasks

### Monitor 3 Apps Every 2 Seconds
```python
monitor = HealthMonitor(ledger, ["app1", "app2", "app3"], poll_interval=2.0)
monitor.start()
```

### Get Current Status of All Apps
```python
status = monitor.get_all_status()
for app_name, result in status.items():
    print(f"{app_name}: {result['status']}")
```

### Track Status History (Last 5 Minutes)
```python
history = monitor.get_history("app_name", lookback_minutes=5)
for record in history:
    print(f"{record['timestamp']}: {record['status']}")
```

### Alert Only on Dead Apps
```python
def my_alert(event):
    if event['new_status'] == 'dead':
        notify_oncall(f"CRITICAL: {event['app']} is down")

monitor.register_alert(my_alert)
```

### Generate Dashboard JSON
```python
dashboard = monitor.get_dashboard_data()

# Includes:
# - dashboard['servers'] - status of each app
# - dashboard['summary'] - totals (running/stale/dead)
# - dashboard['metrics'] - polling stats

import json
print(json.dumps(dashboard, indent=2))
```

---

## Troubleshooting

**Q: App shows "dead" but is actually running**  
A: Check that `last_update` is being updated in sync_config by your app

**Q: All apps show "error"**  
A: Verify `ledger_sync_config.json` exists and has correct format

**Q: Health score not changing**  
A: App isn't updating `last_update` timestamp - check app code

**Q: Monitor thread not working**  
A: Can manually poll: `ledger.poll_server_health(app_name)` in loop

---

## Return Value Reference

```python
result = ledger.poll_server_health("app_name")

# Fields returned:
result['is_alive']      # bool: True if responding
result['status']        # str: "running" | "stale" | "dead" | "error"
result['health_score']  # float: 0.0-1.0 (1.0 = perfect)
result['last_update']   # str: ISO timestamp of last heartbeat
result['record_id']     # str: ID of ledger health record
```

---

## Performance

- **Poll time**: < 1 millisecond
- **Ledger write**: 1-5 milliseconds
- **Memory per app**: ~1 KB
- **CPU idle**: < 1% (background thread)

---

## API Quick Ref

**Main Method:**
```python
ledger.poll_server_health(app_name: str, poll_timeout: float = 5.0) → Dict
```

**Monitor Class:**
```python
monitor = HealthMonitor(ledger, apps: List[str], poll_interval: float = 2.0)
monitor.start()              # Begin background monitoring
monitor.poll_once()          # Poll all apps once
monitor.get_status(app)      # Get current status
monitor.get_dashboard_data() # Get formatted dashboard data
```

**Analyzer Class:**
```python
HealthAnalyzer.calculate_uptime(history)        # Get % uptime
HealthAnalyzer.calculate_avg_health_score(...)  # Average health
HealthAnalyzer.get_status_transitions(...)      # Status changes
HealthAnalyzer.predict_next_failure(...)        # Simple prediction
```

---

## Examples Repository

```
test_server_health_polling.py    - Full test examples (all passing)
health_monitoring_utils.py       - Production code and utilities
SERVER_HEALTH_POLLING.md         - Complete documentation
```

---

## Still Need Help?

1. **How to use it?** → See [SERVER_HEALTH_POLLING.md](SERVER_HEALTH_POLLING.md)
2. **How to configure?** → Check your `ledger_sync_config.json`
3. **See examples?** → Look at [test_server_health_polling.py](test_server_health_polling.py)
4. **Need utilities?** → Use [health_monitoring_utils.py](src/applications/health_monitoring_utils.py)

---

**Version:** 1.0  
**Status:** ✓ Production Ready  
**Tests:** ✓ All Passing  
**Last Updated:** 2025-01-15
