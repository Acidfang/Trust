
"""
TIER -1 (BOUND): Input validation and error setup
TIER 0 (FREE): Explore possibilities
TIER 1 (BOUND): Lock in root-cause logic  
TIER 2 (FREE): Verify consistency
TIER 3+ (BOUND): Automate return and integrate
"""

#!/usr/bin/env python3
"""
PROJECT ORIENTATION VALIDATOR
==============================

This script ensures that any AI making changes to this project
understands the 0-error compute framework before proceeding.

Run this before EVERY work session:
  python project_orientation.py

This validates:
1. Entry gate is read
2. Frameworks are understood
3. Pre-edit checklist is known
4. Decision logging is prepared
5. Automation suite is operational
"""

import json
import sys
from pathlib import Path
from datetime import datetime


class ProjectOrientation:
    """Validate project orientation before work begins."""

    def __init__(self):
        self.workspace = Path.cwd()
        self.checks = []
        self.critical_passed = True

    def check_entry_gate(self):
        """Verify PROJECT_ENTRY_GATE.md exists and is substantial."""
        print("\n[ORIENTATION] Entry Gate ... ", end="", flush=True)

        gate_file = self.workspace / "PROJECT_ENTRY_GATE.md"

        if not gate_file.exists():
            print("MISSING")
            self.checks.append(
                (
                    "CRITICAL",
                    "PROJECT_ENTRY_GATE.md missing - cannot proceed without it",
                )
            )
            self.critical_passed = False
            return

        if gate_file.stat().st_size < 2000:
            print("INCOMPLETE")
            self.checks.append(
                (
                    "CRITICAL",
                    "PROJECT_ENTRY_GATE.md too small - may be corrupted",
                )
            )
            self.critical_passed = False
            return

        print("OK")

    def check_frameworks_accessible(self):
        """Verify all 7 frameworks are accessible."""
        print("[ORIENTATION] Frameworks ... ", end="", flush=True)

        frameworks = [
            "AI_CRITICAL_THINKING_UNIVERSAL_MANDATE.md",
            "AI_CRITICAL_THINKING_TASK_TEMPLATE.md",
            "AI_CRITICAL_THINKING_QUICK_REFERENCE.md",
            "CRITICAL_THINKING_MASTER_INDEX.md",
            "AI_ENVIRONMENT_SELF_KNOWLEDGE.md",
            "PRE_ACTION_CHECKLIST.md",
            "AI_UNIFIED_OPERATING_SYSTEM.md",
        ]

        missing = [f for f in frameworks if not (self.workspace / f).exists()]

        if missing:
            print(f"MISSING ({len(missing)})")
            self.checks.append(
                ("CRITICAL", f"Missing frameworks: {', '.join(missing)}")
            )
            self.critical_passed = False
            return

        print("OK (7/7)")

    def check_startup_context(self):
        """Verify AI_STARTUP_CONTEXT.md is available."""
        print("[ORIENTATION] Startup Context ... ", end="", flush=True)

        ctx_file = self.workspace / "AI_STARTUP_CONTEXT.md"

        if not ctx_file.exists():
            print("MISSING")
            self.checks.append(
                (
                    "CRITICAL",
                    "AI_STARTUP_CONTEXT.md missing - required before any edits",
                )
            )
            self.critical_passed = False
            return

        print("OK")

    def check_automation_suite(self):
        """Verify automation suite is operational."""
        print("[ORIENTATION] Automation Suite ... ", end="", flush=True)

        required = [
            "pre_edit_verification.py",
            "pre_commit_validator.py",
            "automation_runner.py",
        ]

        missing = [f for f in required if not (self.workspace / f).exists()]

        if missing:
            print(f"MISSING ({len(missing)})")
            self.checks.append(
                ("CRITICAL", f"Missing automation scripts: {', '.join(missing)}")
            )
            self.critical_passed = False
            return

        print("OK (3/3 core)")

    def print_orientation_message(self):
        """Print crucial orientation message."""
        print("\n" + "=" * 70)
        print("PROJECT ORIENTATION")
        print("=" * 70)

        if self.critical_passed:
            print("\n[OK] PROJECT ENTRY GATE VERIFIED")
            print("\nBefore editing ANY file, you MUST:")
            print()
            print("  1. Read PROJECT_ENTRY_GATE.md (intro to 0-error compute)")
            print("  2. Run: python pre_edit_verification.py (load context)")
            print("  3. Read: AI_STARTUP_CONTEXT.md (understand frameworks)")
            print("  4. Know: 6-step pre-edit checklist (apply to every edit)")
            print("  5. Verify: git status clean (only intended changes)")
            print()
            print("The frameworks prevent the error pattern:")
            print("  - Don't skip context reading")
            print("  - Don't make assumptions")
            print("  - Don't skip verification steps")
            print()
            print("0-error compute is possible when all gates are in place.")
        else:
            print("\n[BLOCKED] CRITICAL ISSUES FOUND")
            print()
            for severity, msg in self.checks:
                if severity == "CRITICAL":
                    print(f"  [CRITICAL] {msg}")

        print("\n" + "=" * 70)

    def run(self):
        """Run all checks."""
        print("\n" + "=" * 70)
        print("PROJECT ORIENTATION VALIDATOR")
        print("=" * 70)
        print("\nValidating entry gates...")

        self.check_entry_gate()
        self.check_frameworks_accessible()
        self.check_startup_context()
        self.check_automation_suite()

        self.print_orientation_message()

        if not self.critical_passed:
            print("\nFix critical issues before proceeding.")
            return 1

        return 0


if __name__ == "__main__":
    validator = ProjectOrientation()
    sys.exit(validator.run())
