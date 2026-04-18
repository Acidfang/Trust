#!/usr/bin/env python3
"""
START UNIFIED AI TIMELINE VIEWER
Run this to open the interactive GUI
"""

import subprocess
import sys
import urllib.parse

def main():
    print("=" * 80)
    print("UNIFIED AI TIMELINE VIEWER - Startup")
    print("=" * 80)
    print()
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✓ Streamlit found")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas"])
        print("✓ Streamlit installed")
    
    print()
    print("Starting Unified AI Timeline Viewer...")
    print()
    print("The app will open in your default browser.")
    print("If not, visit: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop the server.")
    print()
    print("=" * 80)
    
    # Run streamlit
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_timeline_viewer.py"],
        cwd="c:\\Determined"
    )

if __name__ == "__main__":
    main()
