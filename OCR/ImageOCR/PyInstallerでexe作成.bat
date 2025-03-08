@echo off
echo.
echo Python 仮想環境でビルドする必要があります。
echo 準備はいいですか？
pause
echo off

cd /d "%~dp0"

rem pyinstaller  --onefile  --clean  --noconsole  ImageOCR.py
pyinstaller  ImageOCR.spec

pause
