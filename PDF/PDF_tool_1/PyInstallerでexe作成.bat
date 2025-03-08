@echo off
echo.
echo Python 仮想環境でビルドする必要があります。
echo 準備はいいですか？
pause
echo off

cd /d "%~dp0"

pyinstaller  -n PDF_tool.exe  --onefile  --clean  --noconsole  main.py  delete_pdf.py  merge_pdf.py  rotate_pdf.py  split_pdf.py

pause
