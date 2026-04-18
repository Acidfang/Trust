#!/usr/bin/env python3
"""Simple test of launcher."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from launcher import SandboxLauncher
    
    launcher = SandboxLauncher()
    
    # Check if running
    print("Checking sandbox status...")
    if launcher.is_running():
        print("✓ Already running")
    else:
        print("✗ Not running. Initializing...")
        launcher.initialize()
    
    # Print status
    print("\n" + launcher.report())
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
