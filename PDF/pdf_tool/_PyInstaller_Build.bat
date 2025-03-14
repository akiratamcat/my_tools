pause

cd /d "%~dp0"

set OPT=--clean 

pyinstaller  _PyInstaller_Build.spec  %OPT%  
