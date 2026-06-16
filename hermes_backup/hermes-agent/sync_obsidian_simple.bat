@echo off
echo ======================================
echo   Obsidian GitHub Sync
echo ======================================
echo.

cd /d "D:\Program Files\obsidian\xiaodemi\medical-tourism-notes"

echo Fetching latest files...
git fetch origin

echo.
echo Updating to latest version...
git reset --hard origin/master

echo.
echo ======================================
echo   Sync Complete!
echo ======================================
pause
