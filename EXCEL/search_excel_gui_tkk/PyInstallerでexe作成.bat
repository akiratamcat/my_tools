pause

cd /d "%~dp0"

pyinstaller  --onefile  --clean  --noconsole  search_excel_gui.py  utility.py  excel_oldtype.py  excel_newtype.py
rem pyinstaller search_excel_gui.spec

pause
