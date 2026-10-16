@echo off
setlocal

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0Unblock-DownloadedFiles.ps1" %*
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
    echo Processing completed.
) else (
    echo An error occurred. Check the output and log file.
)
echo Press any key to close this window.
pause >nul

exit /b %RESULT%
