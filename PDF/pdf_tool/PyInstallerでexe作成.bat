@echo off
echo.
echo Python ���z���Ńr���h����K�v������܂��B
echo �����͂����ł����H
pause
echo off

cd /d "%~dp0"

rem pyinstaller  -n PDF_tool.exe  --onefile  --clean  --noconsole  pdf_tool.py
pyinstaller  PDF_tool.exe.spec

pause
