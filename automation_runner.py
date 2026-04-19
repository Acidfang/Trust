#!/usr/bin/env python3
"""
AUTOMATION RUNNER & SCHEDULER
==============================

Central hub for running all automated checks and discovery.
Ties together gate discovery, validation, compliance checking.

Can be run:
  - Manually: python automation_runner.py
  - At startup: Add to shell profile
  - Periodically: Via task scheduler or cron
  - Pre-commit: Via git hook

Usage: python automation_runner.py [--full] [--quiet]
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


class AutomationRunner:
    """Run all workspace automations."""
    
    AUTOMATIONS = {
        "gate_discovery": {
            "script": "gate_discovery_system.py",
            "description": "Find gaps and missing functions",
            "required": True,
        },
        "duplicate_check": {
            "script": "duplicate_detector.py",
            "description": "Find duplicate definitions and content",
            "required": False,
        },
        "framework_compliance": {
            "script": "framework_compliance_checker.py",
            "description": "Verify frameworks are applied",
            "required": True,
        },
        "decision_log": {
            "script": "decision_logger.py",
            "description": "Show recent decision log",
            "required": False,
        },
    }
    
    def __init__(self, workspace=None, full_mode=False, quiet=False):
        self.workspace = Path(workspace or "c:\\Determined")
        self.full_mode = full_mode
        self.quiet = quiet
        self.results = {}
    
    def run(self):
        """Run all automations."""
        if not self.quiet:
            self._header()
        
        critical_passed = True
        
        for name, config in self.AUTOMATIONS.items():
            script = self.workspace / config["script"]
            
            if not script.exists():
                self.results[name] = ("MISSING", f"{config['script']} not found")
                continue
            
            success = self._run_script(name, script, config)
            self.results[name] = ("OK" if success else "FAIL", "")
            
            if config["required"] and not success:
                critical_passed = False
        
        if not self.quiet:
            self._summary(critical_passed)
        
        return critical_passed
    
    def _run_script(self, name, script, config):
        """Run a single automation script."""
        if not self.quiet:
            print(f"\n[RUN] {name}: {config['description']}")
            print("-" * 70)
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=self.workspace,
                capture_output=self.quiet,
                text=True,
                timeout=30
            )
            
            if not self.quiet and result.stdout:
                # Print last N lines only (avoid clutter)
                lines = result.stdout.split('\n')
                for line in lines[-30:]:
                    if line:
                        print(line)
            
            return result.returncode == 0
        
        except subprocess.TimeoutExpired:
            if not self.quiet:
                print(f"[TIMEOUT] {name} took too long")
            return False
        
        except Exception as e:
            if not self.quiet:
                print(f"[ERROR] {name}: {str(e)}")
            return False
    
    def _header(self):
        """Print header."""
        print("\n" + "="*70)
        print("AUTOMATION RUNNER")
        print("="*70)
        print(f"Workspace: {self.workspace}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def _summary(self, critical_passed):
        """Print summary."""
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70 + "\n")
        
        for name, (status, msg) in self.results.items():
            config = self.AUTOMATIONS[name]
            required = "[REQUIRED]" if config["required"] else "[OPTIONAL]"
            print(f"  {status:6}  {name:20}  {required}")
        
        print("\n" + "-"*70)
        
        if critical_passed:
            print("[OK] All required automations passed.")
            print("\nNext actions:")
            print("  - Review gate discoveries (GATES_DISCOVERED.json)")
            print("  - Review duplicate findings")
            print("  - Address framework compliance issues")
        else:
            print("[ALERT] Some required automations failed.")
            print("Review output above for details.")
        
        print()


def main():
    """Run automation suite."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run all workspace automations"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run all automations including optional ones"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output (only return exit code)"
    )
    
    args = parser.parse_args()
    
    runner = AutomationRunner(full_mode=args.full, quiet=args.quiet)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
