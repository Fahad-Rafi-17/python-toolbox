@echo off
echo Starting Python Toolbox GUI...
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe python_toolbox_gui.py
) else (
    python python_toolbox_gui.py
)
pause
