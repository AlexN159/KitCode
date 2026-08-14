@echo off
setlocal
title KitCode Interview Studio
cd /d "%~dp0"

where powershell.exe >nul 2>nul
if errorlevel 1 (
  echo KitCode needs Windows PowerShell, but it could not be found.
  echo Press any key to close.
  pause >nul
  exit /b 1
)

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\launch.ps1" %*
set "KITCODE_EXIT=%ERRORLEVEL%"

if not "%KITCODE_EXIT%"=="0" (
  echo.
  echo KitCode could not start. The message above explains what to try next.
  echo Press any key to close.
  pause >nul
)

exit /b %KITCODE_EXIT%
