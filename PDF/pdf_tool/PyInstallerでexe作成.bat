@echo off
echo.
echo Python 仮想環境でビルドする必要があります。
echo 準備はいいですか？
pause
echo off

cd /d "%~dp0"

rem pyinstaller  -n PDF_tool.exe  --onefile  --clean  --noconsole  pdf_tool.py
pyinstaller  PDF_tool.exe.spec

pause
