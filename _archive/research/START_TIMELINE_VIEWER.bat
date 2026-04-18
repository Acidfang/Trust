@echo off
REM START UNIFIED AI TIMELINE VIEWER
REM Windows batch script to launch the GUI

echo.
echo ================================================================================
echo UNIFIED AI TIMELINE VIEWER - Startup
echo ================================================================================
echo.

cd /d c:\Determined

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found in PATH
    pause
    exit /b 1
)

echo.
echo Installing/verifying dependencies...
python -m pip install streamlit pandas -q

echo.
echo Starting Unified AI Timeline Viewer...
echo.
echo Opening browser to http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

python -m streamlit run streamlit_timeline_viewer.py

pause
