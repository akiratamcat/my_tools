@echo off
echo.
echo Python ���z���Ńr���h����K�v������܂��B
echo �����͂����ł����H
pause
echo off

cd /d "%~dp0"

pyinstaller  --onefile  --clean  --noconsole  search_excel_gui.py  utility.py  excel_oldtype.py  excel_newtype.py
rem pyinstaller search_excel_gui.spec

pause
