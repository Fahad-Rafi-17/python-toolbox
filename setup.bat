@echo off
echo Setting up Python Toolbox...
cd /d "%~dp0"

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment and installing dependencies...
.venv\Scripts\pip.exe install -r requirements.txt

echo.
echo Setup complete! You can now run:
echo   - run_gui.bat (to start the GUI)
echo   - build_exe.bat (to create an executable)
pause
