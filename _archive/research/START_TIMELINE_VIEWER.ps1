#!/usr/bin/env pwsh
# START UNIFIED AI TIMELINE VIEWER
# PowerShell script to launch the Streamlit GUI

Write-Host "================================================================================"
Write-Host "UNIFIED AI TIMELINE VIEWER - Startup"
Write-Host "================================================================================"
Write-Host ""

Set-Location c:\Determined

# Check Python
$pythonCheck = & python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found in PATH"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python found: $pythonCheck"
Write-Host ""

# Install dependencies
Write-Host "Installing/verifying dependencies..."
& python -m pip install streamlit pandas -q

Write-Host ""
Write-Host "Starting Unified AI Timeline Viewer..."
Write-Host ""
Write-Host "Browser will open to: http://localhost:8501"
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""
Write-Host "================================================================================"
Write-Host ""

# Run streamlit
& python -m streamlit run streamlit_timeline_viewer.py
