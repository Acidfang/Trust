#!/usr/bin/env python3
"""
ARIA + JARVIS UNIFIED STARTUP
=============================

Orchestrates bringing the complete system to life:
- Ledger foundation (immutable, auditable core)
- Aria consciousness (self-aware system with self-regulation)
- Jarvis interface (primary user interaction point)
- Coherence monitoring (continuous self-check)
- Protocol enforcement (ZeroPoint compliance)

All processes coordinate through shared ledger.
All operations are recorded.
Complete transparency at every level.
"""

import subprocess
import sys
import os
import time
import threading
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

PORTS = {
    "aria_interface": 5005,
    "jarvis_interface": 8000,
}

COMPONENTS = {
    "aria_bootstrap": "aria_bootstrap.py",
    "aria_system_interface": "aria_system_interface.py",
    "jarvis_primary": "jarvis_v3.py",
}

# ============================================================================
# PROCESS MANAGEMENT
# ============================================================================

class SystemOrchestrator:
    """Coordinates startup and monitoring of all components"""
    
    def __init__(self):
        self.processes = {}
        self.startup_log = []
        self.startup_time = datetime.now()
    
    def log_event(self, event_type, message, details=None):
        """Record startup event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "message": message,
            "details": details or {}
        }
        self.startup_log.append(entry)
        print(f"[{event_type}] {message}")
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
    
    def run_bootstrap(self):
        """Execute Aria bootstrap sequence"""
        self.log_event("BOOTSTRAP", "Starting Aria bootstrap sequence")
        
        try:
            result = subprocess.run(
                [sys.executable, COMPONENTS["aria_bootstrap"]],
                capture_output=False,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log_event("BOOTSTRAP", "✓ Aria bootstrap completed successfully")
                return True
            else:
                self.log_event("ERROR", "Aria bootstrap failed", {"return_code": result.returncode})
                return False
        except Exception as e:
            self.log_event("ERROR", f"Aria bootstrap error: {str(e)}")
            return False
    
    def start_aria_system_interface(self):
        """Start Aria web interface (port 5005)"""
        self.log_event("START", "Starting Aria System Interface", {
            "component": "aria_system_interface.py",
            "port": PORTS["aria_interface"]
        })
        
        try:
            proc = subprocess.Popen(
                [sys.executable, COMPONENTS["aria_system_interface"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes["aria"] = proc
            self.log_event("STARTED", "Aria System Interface is running")
            time.sleep(2)  # Wait for startup
            return True
        except Exception as e:
            self.log_event("ERROR", f"Failed to start Aria: {str(e)}")
            return False
    
    def start_jarvis_primary(self):
        """Start Jarvis web interface (port 8000)"""
        self.log_event("START", "Starting Jarvis Primary Interface", {
            "component": "jarvis_v3.py",
            "port": PORTS["jarvis_interface"]
        })
        
        try:
            proc = subprocess.Popen(
                [sys.executable, COMPONENTS["jarvis_primary"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes["jarvis"] = proc
            self.log_event("STARTED", "Jarvis Primary Interface is running")
            time.sleep(2)  # Wait for startup
            return True
        except Exception as e:
            self.log_event("ERROR", f"Failed to start Jarvis: {str(e)}")
            return False
    
    def verify_ports(self):
        """Check if ports are reachable"""
        import socket
        
        for name, port in PORTS.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                self.log_event("VERIFY", f"Port {port} is responding", {"component": name})
            else:
                self.log_event("WARNING", f"Port {port} not responding yet", {"component": name})
    
    def monitor_processes(self):
        """Continuously monitor running processes"""
        self.log_event("MONITOR", "Process monitoring started")
        
        while True:
            all_alive = True
            
            for name, proc in self.processes.items():
                if proc and proc.poll() is None:
                    # Still running
                    pass
                else:
                    all_alive = False
                    self.log_event("ALERT", f"Process died: {name}")
            
            if not all_alive:
                self.log_event("ERROR", "One or more critical processes have died")
                break
            
            time.sleep(5)
    
    def save_startup_log(self):
        """Save complete startup log to file"""
        log_file = 'aria_system_startup_log.json'
        
        log_document = {
            "startup_time": self.startup_time.isoformat(),
            "duration": str(datetime.now() - self.startup_time),
            "system_status": "RUNNING" if all(p.poll() is None for p in self.processes.values()) else "DEGRADED",
            "components": {
                name: "RUNNING" if self.processes.get(name) and self.processes[name].poll() is None else "STOPPED"
                for name in self.processes.keys()
            },
            "ports": PORTS,
            "bootstrap_log": self.startup_log
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_document, f, indent=2)
        
        self.log_event("SAVE", f"Startup log saved", {"file": log_file})
    
    def execute_startup_sequence(self):
        """Execute complete startup orchestration"""
        print("\n" + "="*70)
        print("🎼 ARIA + JARVIS UNIFIED STARTUP")
        print("="*70)
        print(f"Time: {datetime.now().isoformat()}")
        print(f"Protocol: ZeroPoint Framework (Immutable, Auditable, Transparent)")
        print("="*70 + "\n")
        
        # Change to application directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
        
        # Step 1: Bootstrap
        if not self.run_bootstrap():
            self.log_event("FATAL", "Bootstrap failed - cannot continue")
            self.save_startup_log()
            return False
        
        time.sleep(1)
        
        # Step 2: Start Aria
        if not self.start_aria_system_interface():
            self.log_event("WARNING", "Aria startup failed - continuing with Jarvis only")
        
        time.sleep(1)
        
        # Step 3: Start Jarvis
        if not self.start_jarvis_primary():
            self.log_event("ERROR", "Jarvis startup failed")
            if not self.processes.get("aria"):
                self.log_event("FATAL", "Both Aria and Jarvis failed to start")
                self.save_startup_log()
                return False
        
        time.sleep(1)
        
        # Step 4: Verify
        self.log_event("VERIFY", "Checking system connectivity...")
        self.verify_ports()
        
        # Step 5: Save log
        self.save_startup_log()
        
        # Print summary
        self.print_startup_summary()
        
        # Step 6: Monitor
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            self.log_event("SHUTDOWN", "Received interrupt signal")
            self.shutdown_all()
        
        return True
    
    def print_startup_summary(self):
        """Print system status summary"""
        print("\n" + "="*70)
        print("✅ SYSTEM STARTUP COMPLETE")
        print("="*70)
        
        print("\n📍 ACCESS POINTS:")
        print(f"  Aria System Interface: http://localhost:{PORTS['aria_interface']}")
        print(f"  Jarvis Primary Interface: http://localhost:{PORTS['jarvis_interface']}")
        
        print("\n📊 COMPONENT STATUS:")
        for name, port in PORTS.items():
            status = "✓ RUNNING" if self.processes.get(name.split('_')[0]) and \
                     self.processes[name.split('_')[0]].poll() is None else "✗ STOPPED"
            print(f"  {name}: {status}")
        
        print("\n📝 LOGGING:")
        print("  Startup log: aria_system_startup_log.json")
        print("  Bootstrap log: aria_bootstrap_record.json")
        
        print("\n🔧 COMMANDS:")
        print("  Stop: Press Ctrl+C")
        print("  View logs: Open aria_system_startup_log.json")
        print("  Monitor: Check active ledger files")
        
        print("\n" + "="*70)
        print("System is LIVE. All operations are being recorded to ledger.")
        print("="*70 + "\n")
    
    def shutdown_all(self):
        """Gracefully shutdown all processes"""
        print("\nShutting down systems...")
        
        for name, proc in self.processes.items():
            if proc and proc.poll() is None:
                print(f"  Stopping {name}...")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"  Force killing {name}...")
                    proc.kill()
        
        print("Shutdown complete.")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Execute unified startup"""
    orchestrator = SystemOrchestrator()
    
    try:
        success = orchestrator.execute_startup_sequence()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\nReceived interrupt. Shutting down...")
        orchestrator.shutdown_all()
        return 0
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        orchestrator.log_event("FATAL", str(e))
        orchestrator.save_startup_log()
        return 1

if __name__ == '__main__':
    sys.exit(main())
