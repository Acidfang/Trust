#!/usr/bin/env python3
"""
Launch the Coherence Laboratory Dashboard

Initializes sandbox, checks dependencies, and launches the interactive GUI.
Spans all connected monitors for unified coherence field visualization.
"""

import sys
import subprocess
from pathlib import Path


def check_pygame():
    """Check if pygame is installed, install if needed"""
    try:
        import pygame
        print(f"✓ pygame {pygame.version.ver} found")
        return True
    except ImportError:
        print("✗ pygame not found, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print("✓ pygame installed successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to install pygame: {e}")
            print("  Try manually: pip install pygame")
            return False


def initialize_sandbox():
    """Initialize coherence sandbox if needed"""
    sandbox_dir = Path(__file__).parent
    db_path = sandbox_dir / "claude_coherence.db"
    
    try:
        from sandbox_interface import get_sandbox
        sandbox = get_sandbox()
        
        if sandbox.health_check():
            print("✓ Sandbox initialized and healthy")
            return True
        else:
            print("✗ Sandbox health check failed")
            return False
    except Exception as e:
        print(f"✗ Failed to initialize sandbox: {e}")
        return False


def launch_dashboard(use_multi_monitor: bool = True):
    """Launch the coherence laboratory dashboard"""
    try:
        from gui_dashboard import launch_laboratory
        
        print("\n" + "="*60)
        print("COHERENCE LABORATORY - LAUNCHING")
        print("="*60)
        print()
        print("Controls:")
        print("  • Clarity Slider: Adjust dialogue clarity (0.0-1.0)")
        print("  • Tier Buttons: Select tier to focus on")
        print("  • Record Button: Record current state to database")
        print("  • Learn Button: Toggle learning mode")
        print("  • Compare Button: Open comparison view")
        print("  • Quit Button: Exit laboratory")
        print()
        print("Features:")
        print("  • Real-time database binding")
        print("  • Tier progression tracking")
        print("  • Dialogue clarity trends")
        print("  • Multi-monitor spanning (if available)")
        print()
        
        # Launch
        launch_laboratory(use_multi_monitor=use_multi_monitor)
        
        print("\n✓ Dashboard closed cleanly")
        return True
    
    except ImportError as e:
        print(f"\n✗ Failed to import dashboard: {e}")
        print("  Make sure all module dependencies are available")
        return False
    
    except Exception as e:
        print(f"\n✗ Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    print("COHERENCE LABORATORY - INITIALIZATION\n")
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_pygame():
        print("\n⚠ pygame is required for GUI. Cannot proceed.")
        return 1
    
    # Initialize sandbox
    print("\nInitializing sandbox...")
    if not initialize_sandbox():
        print("\n⚠ Sandbox initialization failed. Some features may not work.")
    
    # Launch dashboard
    print()
    if launch_dashboard(use_multi_monitor=True):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
