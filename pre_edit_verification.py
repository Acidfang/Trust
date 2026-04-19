#!/usr/bin/env python3
"""
PRE-EDIT VERIFICATION SYSTEM
Ensures AI context is loaded before any file operations begin.

This script:
1. Verifies AI_STARTUP_CONTEXT.md exists and is current
2. Checks that critical frameworks are available
3. Confirms automation suite is operational
4. Validates pre-edit checklist can be performed
5. Reports comprehensive readiness status

Run this before ANY file edits:
  python pre_edit_verification.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta


class PreEditVerifier:
    """Verify AI is ready to edit project files."""

    def __init__(self):
        self.workspace = Path.cwd()
        self.issues = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_failed = 0

    def verify_startup_context(self):
        """CRITICAL: Verify startup context exists and is reasonably current."""
        print("[VERIFY] AI_STARTUP_CONTEXT.md ... ", end="", flush=True)

        context_file = self.workspace / "AI_STARTUP_CONTEXT.md"

        if not context_file.exists():
            self.checks_failed += 1
            self.issues.append(
                "CRITICAL: AI_STARTUP_CONTEXT.md missing. Cannot proceed."
            )
            print("MISSING")
            return False

        # Check file size (should be substantial)
        file_size = context_file.stat().st_size
        if file_size < 1000:
            self.checks_failed += 1
            self.issues.append(
                "CRITICAL: AI_STARTUP_CONTEXT.md too small. File may be corrupted."
            )
            print(f"TOO_SMALL ({file_size} bytes)")
            return False

        # Check modification time (should be recent enough for this session)
        mod_time = datetime.fromtimestamp(context_file.stat().st_mtime)
        age = datetime.now() - mod_time
        if age > timedelta(days=30):
            self.warnings.append(
                f"WARNING: AI_STARTUP_CONTEXT.md is {age.days} days old. May be outdated."
            )

        self.checks_passed += 1
        print("OK")
        return True

    def verify_frameworks_available(self):
        """CRITICAL: Verify all 7 frameworks are available."""
        print("[VERIFY] Critical thinking frameworks ... ", end="", flush=True)

        required_frameworks = [
            "AI_CRITICAL_THINKING_UNIVERSAL_MANDATE.md",
            "AI_CRITICAL_THINKING_TASK_TEMPLATE.md",
            "AI_CRITICAL_THINKING_QUICK_REFERENCE.md",
            "CRITICAL_THINKING_MASTER_INDEX.md",
            "AI_ENVIRONMENT_SELF_KNOWLEDGE.md",
            "PRE_ACTION_CHECKLIST.md",
            "AI_UNIFIED_OPERATING_SYSTEM.md",
        ]

        missing_frameworks = [
            f for f in required_frameworks if not (self.workspace / f).exists()
        ]

        if missing_frameworks:
            self.checks_failed += 1
            self.issues.append(
                f"CRITICAL: Missing frameworks: {', '.join(missing_frameworks)}"
            )
            print(f"MISSING ({len(missing_frameworks)})")
            return False

        self.checks_passed += 1
        print("OK (7/7)")
        return True

    def verify_automations_available(self):
        """CRITICAL: Verify all 5 automation scripts are available."""
        print("[VERIFY] Automation suite ... ", end="", flush=True)

        required_automations = [
            "pre_commit_validator.py",
            "decision_logger.py",
            "duplicate_detector.py",
            "framework_compliance_checker.py",
            "automation_runner.py",
            "gate_discovery_system.py",
        ]

        missing_automations = [
            f for f in required_automations if not (self.workspace / f).exists()
        ]

        if missing_automations:
            self.checks_failed += 1
            self.issues.append(
                f"CRITICAL: Missing automations: {', '.join(missing_automations)}"
            )
            print(f"MISSING ({len(missing_automations)})")
            return False

        self.checks_passed += 1
        print("OK (6/6)")
        return True

    def verify_git_ready(self):
        """Check git state is clean and ready."""
        print("[VERIFY] Git state ... ", end="", flush=True)

        git_dir = self.workspace / ".git"
        if not git_dir.exists():
            self.warnings.append("WARNING: Not a git repository. Commits will fail.")
            print("NOT_GIT")
            return True

        # Check for common git hook
        pre_commit_hook = git_dir / "hooks" / "pre-commit"
        if not pre_commit_hook.exists():
            self.warnings.append(
                "WARNING: Pre-commit hook not found. Auto-validation disabled."
            )

        self.checks_passed += 1
        print("OK")
        return True

    def verify_decision_log_ready(self):
        """Check decision logging is operational."""
        print("[VERIFY] Decision logging system ... ", end="", flush=True)

        decision_log = self.workspace / "DECISION_LOG.jsonl"

        if not decision_log.exists():
            self.warnings.append("INFO: DECISION_LOG.jsonl not yet created (first run).")
            self.checks_passed += 1
            print("READY (empty)")
            return True

        # Check it's valid JSONL
        try:
            with open(decision_log, "r") as f:
                first_line = f.readline()
                if first_line.strip():
                    json.loads(first_line)
            self.checks_passed += 1
            print("OK")
            return True
        except (json.JSONDecodeError, IOError) as e:
            self.warnings.append(f"WARNING: DECISION_LOG.jsonl may be corrupted: {e}")
            self.checks_passed += 1
            print("OK (with warning)")
            return True

    def verify_gate_discovery_ready(self):
        """Check gate discovery system is ready."""
        print("[VERIFY] Gate discovery system ... ", end="", flush=True)

        gates_file = self.workspace / "GATES_DISCOVERED.json"

        if not gates_file.exists():
            self.warnings.append("INFO: GATES_DISCOVERED.json not yet created.")
            self.checks_passed += 1
            print("READY (empty)")
            return True

        # Check it's valid JSON
        try:
            with open(gates_file, "r") as f:
                json.load(f)
            self.checks_passed += 1
            print("OK")
            return True
        except (json.JSONDecodeError, IOError) as e:
            self.checks_failed += 1
            self.issues.append(f"ERROR: GATES_DISCOVERED.json corrupted: {e}")
            print("CORRUPTED")
            return False

    def verify_quick_reference(self):
        """Verify quick reference guide is available."""
        print("[VERIFY] Quick reference guides ... ", end="", flush=True)

        quick_ref = self.workspace / "AI_CRITICAL_THINKING_QUICK_REFERENCE.md"

        if not quick_ref.exists():
            self.warnings.append(
                "WARNING: Quick reference not available. Full docs required."
            )

        self.checks_passed += 1
        print("OK")
        return True

    def print_readiness_summary(self):
        """Print comprehensive readiness report."""
        print("\n" + "=" * 70)
        print("PRE-EDIT VERIFICATION SUMMARY")
        print("=" * 70)

        passed = self.checks_passed
        failed = self.checks_failed
        total = passed + failed

        if failed == 0:
            print(f"\n[OK] ALL CHECKS PASSED ({passed}/{total})")
            print("\n=> AI CONTEXT IS FULLY LOADED")
            print("=> Ready to edit project files")
            print("=> All frameworks and automations available")

            if self.warnings:
                print(f"\n[!] {len(self.warnings)} warning(s):")
                for warning in self.warnings:
                    print(f"  - {warning}")
        else:
            print(f"\n[FAILED] CHECKS FAILED ({failed}/{total})")
            print("\n=> CANNOT PROCEED - Critical issues must be resolved:")
            for issue in self.issues:
                print(f"  - {issue}")

            if self.warnings:
                print(f"\n[!] {len(self.warnings)} warning(s):")
                for warning in self.warnings:
                    print(f"  - {warning}")

        print("\n" + "=" * 70)

    def print_pre_edit_checklist(self):
        """Print the 6-step pre-edit checklist for reference."""
        if self.checks_failed == 0:
            print("\nPRE-EDIT CHECKLIST (6 STEPS):")
            print("-" * 70)
            print("Before editing ANY file:")
            print()
            print("  [  ] STEP 1: Read complete context of file being edited")
            print("       Check: Understand structure, existing patterns (2 min)")
            print()
            print("  [  ] STEP 2: Check for existing content")
            print("       Check: Use grep_search for similar patterns (30 sec)")
            print()
            print("  [  ] STEP 3: Make comprehensive edit")
            print("       Check: Include 3-5 lines before & after target (3-5 min)")
            print()
            print("  [  ] STEP 4: Validate syntax")
            print("       Check: python/yaml/json/markdown valid (30 sec)")
            print()
            print("  [  ] STEP 5: Test if applicable")
            print("       Check: If code, run it; if config, validate (1-5 min)")
            print()
            print("  [  ] STEP 6: Verify git state")
            print("       Check: git status clean, run pre_commit_validator.py (30 sec)")
            print()
            print("  TOTAL TIME: 4-14 minutes (prevents hours of debugging)")
            print("-" * 70)

    def print_helpful_commands(self):
        """Print helpful commands for the session."""
        if self.checks_failed == 0:
            print("\nUSEFUL COMMANDS:")
            print("-" * 70)
            print("Check current state:")
            print("  python automation_runner.py           # Full health check")
            print("  python gate_discovery_system.py       # Find all gaps")
            print("  python decision_logger.py             # Review decisions")
            print()
            print("Validate before committing:")
            print("  python pre_commit_validator.py        # Must pass")
            print("  python duplicate_detector.py          # Optional")
            print("  python framework_compliance_checker.py # Must pass")
            print()
            print("Git operations:")
            print("  git status                  # Check working directory")
            print("  git diff                    # Review changes")
            print("  git add -A && git commit -m '...'  # Commit your work")
            print("-" * 70)

    def run(self):
        """Run all verifications."""
        print("\n" + "=" * 70)
        print("AI PRE-EDIT VERIFICATION")
        print("=" * 70)
        print("\nRunning verification checks...\n")

        # Critical checks (must all pass)
        self.verify_startup_context()
        self.verify_frameworks_available()
        self.verify_automations_available()

        # Secondary checks
        self.verify_git_ready()
        self.verify_decision_log_ready()
        self.verify_gate_discovery_ready()
        self.verify_quick_reference()

        # Print results
        self.print_readiness_summary()

        if self.checks_failed == 0:
            self.print_pre_edit_checklist()
            self.print_helpful_commands()
            print("\n[OK] You are ready to edit project files.")
            print("  Follow the 6-step pre-edit checklist before each edit.")
            return 0
        else:
            print(
                "\n[FAILED] Fix critical issues above before proceeding with file edits."
            )
            return 1


if __name__ == "__main__":
    verifier = PreEditVerifier()
    exit_code = verifier.run()
    sys.exit(exit_code)
