@echo off
cd /d "%~dp0"

echo Installing required packages...
if exist ".venv\Scripts\pip.exe" (
    .venv\Scripts\pip.exe install rich pyinstaller
) else (
    pip install rich pyinstaller
)

echo.
echo Creating executable...
if exist ".venv\Scripts\pyinstaller.exe" (
    .venv\Scripts\pyinstaller.exe --onefile --windowed --name "Python-Toolbox-GUI" python_toolbox_gui.py
) else (
    pyinstaller --onefile --windowed --name "Python-Toolbox-GUI" python_toolbox_gui.py
)

echo.
echo Build complete! The executable will be in the 'dist' folder.
pause
