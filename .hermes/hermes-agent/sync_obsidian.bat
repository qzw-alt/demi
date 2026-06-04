@echo off
echo ======================================
echo   Obsidian GitHub Sync Script
echo ======================================
echo.

REM Set Obsidian vault path
set VAULT_PATH=D:\Program Files\obsidian\xiaodemi\medical-tourism-notes

cd /d "%VAULT_PATH%"

echo [1/3] Testing connection...
git config --global http.sslVerify false
git config --global --get http.proxy
git config --global --get https.proxy

echo.
echo [2/3] Pulling latest from GitHub...
git pull origin master

if %errorlevel% == 0 (
    echo.
    echo [3/3] Sync successful!
    git status --short
) else (
    echo.
    echo [3/3] Sync failed
    echo.
    echo Trying alternative method...
    git fetch origin
    git reset --hard origin/master
)

echo.
echo ======================================
echo   Press any key to close...
pause >nul
