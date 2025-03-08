@echo off
echo.
echo Python 仮想環境でビルドする必要があります。
echo 準備はいいですか？
pause
echo off

cd /d "%~dp0"

pyinstaller  --onefile  --clean  --noconsole  search_excel_gui.py  utility.py  excel_oldtype.py  excel_newtype.py
rem pyinstaller search_excel_gui.spec

pause
