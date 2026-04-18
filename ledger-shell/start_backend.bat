@echo off
cd /d "%~dp0backend"
pip install -r requirements.txt
echo.
echo Starting Backend Server...
echo Ledger Shell Backend running at http://127.0.0.1:8000
echo.
python app.py
pause
