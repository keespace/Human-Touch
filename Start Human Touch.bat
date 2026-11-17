@echo off
title Human Touch
cd /d "%~dp0"

rem --- 1. Python installed? ---
where python >nul 2>nul
if errorlevel 1 (
  echo Python is not installed.
  echo Install it from https://www.python.org/downloads/  ^(tick "Add python.exe to PATH" during setup^),
  echo then double-click this file again.
  pause
  exit /b 1
)

rem --- 2. Libraries installed? (only slow the first time) ---
python -c "import anthropic" >nul 2>nul
if errorlevel 1 (
  echo First run: installing the Anthropic library...
  python -m pip install --quiet -r requirements.txt
  if errorlevel 1 ( echo Installing failed - check your internet connection. & pause & exit /b 1 )
)

rem --- 3. API key: a Windows user variable ANTHROPIC_API_KEY, or a .env file in this folder ---
if defined ANTHROPIC_API_KEY goto key_ok
if not exist ".env" (
  copy /y ".env.example" ".env" >nul
  echo.
  echo A file called .env has been created in this folder.
  echo Open it with Notepad, paste your Anthropic API key after ANTHROPIC_API_KEY= and save.
  echo ^(Without a key the app still works, but only the free quick check is available.^)
  echo.
  start "" notepad ".env"
  pause
)
:key_ok

echo Starting Human Touch...  Keep this window open while you use the app.
echo Close this window to stop it.
echo.
start "" cmd /c "timeout /t 3 >nul & start http://localhost:8765"
python server.py
echo.
echo The server stopped. If it says the address is already in use, Human Touch is probably already running -
echo just open http://localhost:8765 in your browser.
pause
