#!/usr/bin/env python3
"""
Create Windows Desktop Shortcut for Reddit Tracker GUI
Run this once to create a desktop shortcut
"""

import os
import sys
from pathlib import Path

def create_shortcut():
    """Create desktop shortcut"""
    
    # Desktop path
    desktop = Path.home() / "Desktop"
    
    # VBS script to create shortcut (works on Windows)
    vbs_script = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop}\\Reddit Tracker.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "python.exe"
oLink.Arguments = "c:\\Determined\\reddit_tracker_gui.py"
oLink.WorkingDirectory = "c:\\Determined"
oLink.Description = "Reddit Post Tracker GUI"
oLink.Save
"""
    
    # Write VBS file
    vbs_file = "create_shortcut.vbs"
    with open(vbs_file, 'w') as f:
        f.write(vbs_script)
    
    # Execute
    os.system(f'cscript.exe {vbs_file}')
    
    # Clean up
    os.remove(vbs_file)
    
    print(f"[✓] Shortcut created on Desktop")
    print(f"[✓] Name: Reddit Tracker.lnk")

if __name__ == '__main__':
    try:
        create_shortcut()
    except Exception as e:
        print(f"[!] Error: {e}")
        print("Note: You may need to run this as Administrator")
