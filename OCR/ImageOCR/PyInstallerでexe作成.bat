@echo off
echo.
echo Python ���z���Ńr���h����K�v������܂��B
echo �����͂����ł����H
pause
echo off

cd /d "%~dp0"

rem pyinstaller  --onefile  --clean  --noconsole  ImageOCR.py
pyinstaller  ImageOCR.spec

pause
