@echo off
setlocal

if "%~1"=="" (
    echo ZIPファイルまたはフォルダをこのファイルにドラッグ＆ドロップしてください。
    pause
    exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Unzip-All.ps1" %*
set "exitCode=%ERRORLEVEL%"
if not "%exitCode%"=="0" pause
exit /b %exitCode%
