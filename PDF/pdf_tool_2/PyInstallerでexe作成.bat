@echo off
echo.
echo Python 仮想環境でビルドする必要があります。
echo 準備はいいですか？
pause
echo off

cd /d "%~dp0"

pyinstaller  --onefile  --clean  --noconsole  main.py  utility.py  merge_pdf.py  split_pdf.py  rotate_page_pdf.py  delete_page_pdf.py  insert_pdf.py  extract_text_and_image_pdf.py


pause
