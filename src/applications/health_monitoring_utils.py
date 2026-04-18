"""
Server health monitoring utilities for real-world integration.

Provides ready-to-use patterns for integrating server health polling
into applications, dashboards, and monitoring systems.
"""

import json
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path


class HealthMonitor:
    """
    Continuous server health monitor with alerting and metrics collection.
    
    Provides:
    - Background monitoring thread
    - Alert callbacks on status changes
    - Metrics aggregation
    - Dashboard data generation
    """
    
    def __init__(self, ledger, apps: List[str], poll_interval: float = 2.0):
        """
        Initialize health monitor.
        
        Args:
            ledger: LedgerQuery instance
            apps: List of app names to monitor
            poll_interval: Polling frequency in seconds
        """
        self.ledger = ledger
        self.apps = apps
        self.poll_interval = poll_interval
        
        # State tracking
        self.current_status = {}
        self.previous_status = {}
        self.status_history = {app: [] for app in apps}
        self.running = False
        self.thread = None
        
        # Alerts
        self.alert_callbacks = []
        self.metrics = {
            "polls_total": 0,
            "status_changes": 0,
            "errors": 0
        }
    
    def start(self):
        """Start background monitoring thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print(f"[MONITOR] Started monitoring {len(self.apps)} apps")
    
    def stop(self):
        """Stop monitoring thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        print("[MONITOR] Stopped")
    
    def _monitor_loop(self):
        """Background monitoring loop."""
        while self.running:
            try:
                self.poll_once()
            except Exception as e:
                print(f"[MONITOR] Error: {e}")
                self.metrics["errors"] += 1
            
            time.sleep(self.poll_interval)
    
    def poll_once(self):
        """Perform one round of polling for all apps."""
        self.metrics["polls_total"] += 1
        
        for app_name in self.apps:
            try:
                result = self.ledger.poll_server_health(app_name)
                
                # Update status
                self.current_status[app_name] = result
                
                # Detect changes
                old_status = self.previous_status.get(app_name, {}).get("status")
                new_status = result["status"]
                
                if old_status != new_status:
                    self._handle_status_change(app_name, old_status, new_status, result)
                    self.metrics["status_changes"] += 1
                
                # Track history
                self.status_history[app_name].append({
                    "timestamp": datetime.now().isoformat(),
                    "status": new_status,
                    "health_score": result["health_score"]
                })
                
                self.previous_status[app_name] = result
                
            except Exception as e:
                print(f"[MONITOR] Failed to poll {app_name}: {e}")
    
    def _handle_status_change(self, app_name: str, old_status: Optional[str], 
                              new_status: str, result: Dict[str, Any]):
        """Handle status change event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "app": app_name,
            "old_status": old_status,
            "new_status": new_status,
            "health_score": result["health_score"]
        }
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"[MONITOR] Alert callback error: {e}")
    
    def register_alert(self, callback: Callable[[Dict], None]):
        """Register alert callback."""
        self.alert_callbacks.append(callback)
    
    def get_status(self, app_name: str) -> Optional[Dict[str, Any]]:
        """Get current status for app."""
        return self.current_status.get(app_name)
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get current status for all apps."""
        return self.current_status.copy()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data formatted for dashboard display."""
        return {
            "timestamp": datetime.now().isoformat(),
            "servers": [
                {
                    "name": app,
                    "status": self.current_status.get(app, {}).get("status", "unknown"),
                    "health_score": self.current_status.get(app, {}).get("health_score", 0),
                    "is_alive": self.current_status.get(app, {}).get("is_alive", False)
                }
                for app in self.apps
            ],
            "summary": {
                "total_apps": len(self.apps),
                "running": sum(1 for s in self.current_status.values() if s.get("status") == "running"),
                "stale": sum(1 for s in self.current_status.values() if s.get("status") == "stale"),
                "dead": sum(1 for s in self.current_status.values() if s.get("status") == "dead")
            },
            "metrics": self.metrics
        }
    
    def get_history(self, app_name: str, lookback_minutes: int = 5) -> List[Dict]:
        """Get status history for an app."""
        cutoff = datetime.now() - timedelta(minutes=lookback_minutes)
        history = self.status_history.get(app_name, [])
        
        return [
            h for h in history
            if datetime.fromisoformat(h["timestamp"]) > cutoff
        ]


class AlertManager:
    """Smart alert management with threshold and escalation."""
    
    def __init__(self, ledger_dir: str = "."):
        self.ledger_dir = ledger_dir
        self.alerts_log = []
        self.alert_config = {}
    
    def load_config(self, config_file: str):
        """Load alert config from file."""
        if Path(config_file).exists():
            with open(config_file, 'r') as f:
                self.alert_config = json.load(f)
    
    def save_config(self, config_file: str):
        """Save alert config to file."""
        with open(config_file, 'w') as f:
            json.dump(self.alert_config, f, indent=2)
    
    def handle_alert(self, event: Dict[str, Any]):
        """Handle alert event."""
        app = event["app"]
        new_status = event["new_status"]
        
        # Log the alert
        alert_record = {
            "id": f"alert:{app}:{datetime.now().isoformat()}",
            "timestamp": datetime.now().isoformat(),
            **event
        }
        self.alerts_log.append(alert_record)
        
        # Get alert config for app
        app_config = self.alert_config.get(app, {})
        
        # Check if we should alert
        if new_status == "dead":
            print(f"🚨 CRITICAL: {app} is DEAD")
            self._trigger_alert("critical", event)
        elif new_status == "stale":
            print(f"⚠️  WARNING: {app} is STALE")
            self._trigger_alert("warning", event)
        elif new_status == "running":
            print(f"✓ RECOVERED: {app} is running again")
            self._trigger_alert("recovered", event)
    
    def _trigger_alert(self, level: str, event: Dict[str, Any]):
        """Trigger alert (can be overridden for external integrations)."""
        # Log to alert ledger
        alert_file = Path(self.ledger_dir) / "ledger_alerts.jsonl"
        try:
            with open(alert_file, 'a') as f:
                f.write(json.dumps({"level": level, **event}) + "\n")
        except:
            pass


class HealthAnalyzer:
    """Analyze health trends and provide insights."""
    
    @staticmethod
    def calculate_uptime(history: List[Dict]) -> float:
        """Calculate uptime percentage from history."""
        if not history:
            return 0.0
        
        running_count = sum(1 for h in history if h["status"] == "running")
        return (running_count / len(history)) * 100
    
    @staticmethod
    def calculate_avg_health_score(history: List[Dict]) -> float:
        """Calculate average health score."""
        if not history:
            return 0.0
        
        scores = [h["health_score"] for h in history]
        return sum(scores) / len(scores)
    
    @staticmethod
    def get_status_transitions(history: List[Dict]) -> List[Dict]:
        """Get list of status transitions."""
        if not history:
            return []
        
        transitions = []
        for i in range(1, len(history)):
            old = history[i-1]["status"]
            new = history[i]["status"]
            
            if old != new:
                transitions.append({
                    "from": old,
                    "to": new,
                    "time": history[i]["timestamp"]
                })
        
        return transitions
    
    @staticmethod
    def predict_next_failure(history: List[Dict], threshold: float = 0.2) -> Optional[Dict]:
        """Simple prediction: flag if health score is declining toward threshold."""
        if len(history) < 3:
            return None
        
        recent_scores = [h["health_score"] for h in history[-3:]]
        
        # Check if trending downward
        if recent_scores[0] > recent_scores[1] > recent_scores[2]:
            if recent_scores[-1] < threshold:
                return {
                    "risk": "high",
                    "current_score": recent_scores[-1],
                    "trend": "declining"
                }
        
        return None


def create_default_config() -> Dict[str, Any]:
    """Create default alert configuration."""
    return {
        "global": {
            "poll_interval": 2.0,
            "history_retention_hours": 24
        },
        "apps": {
            "tkinter_canvas": {
                "alert_on_dead": True,
                "alert_on_stale": True,
                "alert_on_recovery": True
            },
            "html_browser": {
                "alert_on_dead": True,
                "alert_on_stale": False,
                "alert_on_recovery": True
            }
        },
        "escalation": {
            "dead": ["log", "console", "alert"],
            "stale": ["log", "console"],
            "recovered": ["log", "console"]
        }
    }


# Example usage patterns
if __name__ == "__main__":
    print("Server Health Monitoring Utilities")
    print("==================================\n")
    
    print("This module provides:")
    print("- HealthMonitor: Background monitoring with alerts")
    print("- AlertManager: Smart alert routing and logging")
    print("- HealthAnalyzer: Trend analysis and predictions")
    print("\nSee SERVER_HEALTH_POLLING.md for integration examples")
