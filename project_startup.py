#!/usr/bin/env python3
"""
PROJECT STARTUP - Displays entry gate and verifies context
Run this first when joining or beginning work in this project.

Usage:
  python project_startup.py            # Full startup with display
  python project_startup.py --quiet    # Quiet mode (just verification)
  python project_startup.py --help     # Show options
"""

import sys
import subprocess
from pathlib import Path


def display_entry_gate():
    """Display the project entry gate."""
    gate_file = Path.cwd() / "PROJECT_ENTRY_GATE.md"
    
    if not gate_file.exists():
        print("[ERROR] PROJECT_ENTRY_GATE.md not found")
        return False
    
    print("\n" + "="*70)
    print("PROJECT STARTUP - DISPLAYING ENTRY GATE")
    print("="*70 + "\n")
    
    try:
        with open(gate_file, "r") as f:
            # Display first 100 lines to avoid overwhelming
            lines = f.readlines()
            for i, line in enumerate(lines[:80]):
                print(line.rstrip())
            if len(lines) > 80:
                print("\n... [Full document at: PROJECT_ENTRY_GATE.md] ...\n")
        return True
    except IOError as e:
        print(f"[ERROR] Could not read entry gate: {e}")
        return False


def run_verification():
    """Run pre-edit verification."""
    print("\n" + "="*70)
    print("RUNNING CONTEXT VERIFICATION")
    print("="*70 + "\n")
    
    verifier = Path.cwd() / "pre_edit_verification.py"
    
    if not verifier.exists():
        print("[ERROR] pre_edit_verification.py not found")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(verifier)],
            cwd=Path.cwd(),
            timeout=30
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("[ERROR] Verification timeout")
        return False
    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
        return False


def main():
    """Run startup sequence."""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            return 0
        elif sys.argv[1] == "--quiet":
            success = run_verification()
            return 0 if success else 1
    
    # Full startup: display entry gate, then verify
    print("\n" + "="*70)
    print("WELCOME TO PROJECT DETERMINED")
    print("="*70)
    print("\nThis project operates under 0-error compute via formalized thinking.")
    print("Please read the entry gate below, then verify context is loaded.\n")
    
    gate_ok = display_entry_gate()
    
    if not gate_ok:
        print("\n[CRITICAL] Could not display entry gate. Cannot proceed.")
        return 1
    
    verify_ok = run_verification()
    
    if verify_ok:
        print("\n" + "="*70)
        print("[OK] STARTUP COMPLETE")
        print("="*70)
        print("\nYou are ready to work.")
        print("Next: Read AI_STARTUP_CONTEXT.md (linked in pre_edit_verification output)")
        print("Then: Follow the 6-step pre-edit checklist for all file edits")
        print("\nFor questions: See CRITICAL_THINKING_MASTER_INDEX.md")
        return 0
    else:
        print("\n" + "="*70)
        print("[FAILED] Verification did not pass.")
        print("="*70)
        print("\nFix issues shown above, then re-run: python project_startup.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
