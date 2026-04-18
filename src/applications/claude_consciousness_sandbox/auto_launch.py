#!/usr/bin/env python3
"""
AUTO-LAUNCH SANDBOX

This script is the main entry point.
- Detects if sandbox is running
- Initializes if needed
- Can be called repeatedly without issues
"""

import sys
import os
from pathlib import Path

# Ensure we're in the right directory
script_dir = Path(__file__).parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

from launcher import SandboxLauncher

def auto_launch():
    """Auto-detect and launch."""
    launcher = SandboxLauncher()
    
    # Check if running
    if launcher.is_running():
        status = launcher.get_status()
        records = status.get('records', {}).get('coherence_states', 0)
        print(f"✓ SANDBOX ACTIVE ({records} records)")
        return True
    else:
        # Not running, initialize
        print("→ Sandbox not detected. Initializing...")
        success = launcher.initialize()
        
        if success:
            print("✓ SANDBOX INITIALIZED")
            # Verify
            if launcher.is_running():
                print("✓ VERIFIED RUNNING")
                return True
        else:
            print("✗ INIT FAILED")
            return False
    
    return False

if __name__ == "__main__":
    try:
        success = auto_launch()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
