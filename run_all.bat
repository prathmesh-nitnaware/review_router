@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo  Starting Intelligent Review Router Services
echo ============================================================

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" run_all.py

pause

