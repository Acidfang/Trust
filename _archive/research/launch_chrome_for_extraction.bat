@echo off
REM Launch Chrome with remote debugging enabled for Playwright connection
REM This allows us to extract data from the already-logged-in session

echo.
echo ========================================
echo GEMINI EXTRACTOR - Chrome Launcher
echo ========================================
echo.
echo Starting Chrome with remote debugging enabled...
echo Port: 9222
echo.

REM Find Chrome.exe path
for /f "delims=" %%A in ('where chrome.exe 2^>nul') do (
    set CHROME_PATH=%%A
    goto found
)

REM If not found in PATH, try common locations
if errorlevel 1 (
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
        goto found
    )
    if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        set CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
        goto found
    )
    echo ERROR: Could not find Chrome.exe
    echo Please install Chrome or add it to PATH
    pause
    exit /b 1
)

:found
echo Found Chrome at: %CHROME_PATH%
echo.
echo Instructions:
echo 1. Chrome will open in a moment
echo 2. Make sure you're logged into Gemini
echo 3. Keep this window open while extracting
echo 4. In another terminal, run: python gemini_existing_chrome_extractor.py
echo.
pause

REM Launch Chrome with remote debugging
"%CHROME_PATH%" --remote-debugging-port=9222 "https://gemini.google.com/app"

echo.
echo Chrome closed. You can close this window.
pause
