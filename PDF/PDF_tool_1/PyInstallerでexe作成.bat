@echo off
echo.
echo Python ���z���Ńr���h����K�v������܂��B
echo �����͂����ł����H
pause
echo off

cd /d "%~dp0"

pyinstaller  -n PDF_tool.exe  --onefile  --clean  --noconsole  main.py  delete_pdf.py  merge_pdf.py  rotate_pdf.py  split_pdf.py

pause
