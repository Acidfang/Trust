#!/usr/bin/env python3
"""
JARVIS Health Verification Script

BIDIRECTIONAL CHAIN VERIFICATION:
- Forward: "Is server running?" → check /api/health
- Backward: "Before starting, is it already running?" → check /api/health

This script prevents duplicate server processes by checking if server
is already running before attempting to start a new instance.
"""

import requests
import sys
import time
from pathlib import Path

JARVIS_HOST = "127.0.0.1"
JARVIS_PORT = 8081
JARVIS_HEALTH_URL = f"http://{JARVIS_HOST}:{JARVIS_PORT}/api/health"
BOOT_LOG = Path(__file__).parent / "jarvis_v3_boot.log"


def check_server_health(timeout=2):
    """
    Check if JARVIS server is already running and healthy.
    
    FORWARD CHAIN: "Is server running?"
    → Calls /api/health endpoint
    → Returns True if healthy, False if not running/degraded
    
    BACKWARD CHAIN: "Before starting, is it already running?"
    → Calls same endpoint
    → If True: don't start (already running)
    → If False: OK to start fresh
    """
    try:
        response = requests.get(JARVIS_HEALTH_URL, timeout=timeout)
        
        if response.status_code == 200:
            # Server healthy
            data = response.json()
            return {
                "running": True,
                "healthy": True,
                "status": data.get("status", "unknown"),
                "uptime": data.get("uptime_seconds", 0),
                "components": data.get("components", {}),
                "buttons": data.get("buttons_count", 0),
                "dashboards": data.get("dashboards_count", 0)
            }
        elif response.status_code == 503:
            # Server running but degraded
            data = response.json()
            return {
                "running": True,
                "healthy": False,
                "status": data.get("status", "degraded"),
                "error": data.get("error", "Unknown error"),
                "uptime": data.get("uptime_seconds", 0)
            }
        else:
            # Unexpected response
            return {
                "running": False,
                "healthy": False,
                "status": f"HTTP {response.status_code}",
                "error": response.text[:100]
            }
    
    except requests.ConnectionError:
        # Can't connect - server not running
        return {
            "running": False,
            "healthy": False,
            "status": "connection_refused",
            "error": "No server listening on port 8081"
        }
    
    except requests.Timeout:
        # Server took too long to respond
        return {
            "running": False,
            "healthy": False,
            "status": "timeout",
            "error": f"No response from {JARVIS_HEALTH_URL} after {timeout}s"
        }
    
    except Exception as e:
        # Unknown error
        return {
            "running": False,
            "healthy": False,
            "status": "error",
            "error": f"{type(e).__name__}: {str(e)}"
        }


def print_health_status(health):
    """Print health check results"""
    
    if health["running"] and health["healthy"]:
        print("\n" + "="*70)
        print("✓ JARVIS v3 SERVER ALREADY RUNNING")
        print("="*70)
        print(f"Status:      {health['status']}")
        print(f"Uptime:      {health['uptime']} seconds")
        print(f"Buttons:     {health['buttons']}")
        print(f"Dashboards:  {health['dashboards']}")
        print("\nComponents:")
        for comp, status in health.get('components', {}).items():
            print(f"  • {comp}: {status}")
        print("="*70)
        print("\n✓ Server is healthy - no need to start another instance!")
        return True
    
    elif health["running"] and not health["healthy"]:
        print("\n" + "="*70)
        print("⚠️  JARVIS v3 SERVER RUNNING BUT DEGRADED")
        print("="*70)
        print(f"Status:  {health['status']}")
        print(f"Error:   {health.get('error', 'Unknown')}")
        print(f"Uptime:  {health['uptime']} seconds")
        print("="*70)
        print("\n✓ Server is running (stop it before restarting)")
        return True
    
    else:
        print("\n" + "="*70)
        print("ℹ️  JARVIS v3 SERVER NOT RUNNING")
        print("="*70)
        print(f"Status: {health['status']}")
        print(f"Error:  {health.get('error', 'Unknown')}")
        print("="*70)
        print("\n✓ OK to start fresh instance")
        return False


def main():
    """
    Main verification routine.
    
    USAGE:
        python verify_jarvis_health.py
    
    EXIT CODES:
        0 = Server is already running (don't start)
        1 = Server not running (OK to start)
        2 = Error checking health
    """
    
    print(f"\n[VERIFY] Checking JARVIS v3 health at {JARVIS_HEALTH_URL}...")
    
    health = check_server_health(timeout=2)
    is_running = print_health_status(health)
    
    if is_running:
        print("\n[DECISION] Exit code 0 - Server already running")
        sys.exit(0)
    else:
        print("\n[DECISION] Exit code 1 - Safe to start server")
        sys.exit(1)


if __name__ == "__main__":
    main()
