pause

cd /d "%~dp0"

pyinstaller  --onefile  --clean  --noconsole  main.py  delete_pdf.py  merge_pdf.py  rotate_pdf.py  split_pdf.py

pause
