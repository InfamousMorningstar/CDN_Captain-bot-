@echo off
echo ================================================
echo   CDN_Captain Bot - Setup
echo ================================================
echo.

:: ── Step 1: Check / Install Python ──────────────
echo [1/4] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing via winget...
    winget install -e --id Python.Python.3.13 --silent --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Automatic Python install failed.
        echo Please install Python manually from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during install.
        pause
        exit /b 1
    )
    echo Python installed. Restarting setup to apply PATH changes...
    echo Please run setup.bat again after this window closes.
    pause
    exit /b 0
) else (
    python --version
    echo Python found.
)

echo.

:: ── Step 2: Install Python packages ─────────────
echo [2/4] Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: pip install failed.
    pause
    exit /b 1
)

echo.

:: ── Step 3: Install Playwright Chromium ──────────
echo [3/4] Installing Playwright Chromium browser...
python -m playwright install chromium
if %errorlevel% neq 0 (
    echo ERROR: Playwright browser install failed.
    pause
    exit /b 1
)

echo.

:: ── Step 4: Check .env file ───────────────────────
echo [4/4] Checking for .env file...
if not exist .env (
    echo WARNING: .env file not found!
    echo.
    echo Create a file named .env in this folder with:
    echo.
    echo   DISCORD_TOKEN=your_discord_bot_token_here
    echo   ANTHROPIC_API_KEY=your_anthropic_api_key_here
    echo.
) else (
    echo .env file found.
)

echo.
echo ================================================
echo   Setup complete!
echo.
echo   To start the bot WITH auto-restart (recommended):
echo     python watchdog.py
echo.
echo   To start the bot directly (no auto-restart):
echo     python bot.py
echo ================================================
echo.
pause
