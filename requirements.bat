@echo off

echo Checking Is Python installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not installed.
    set "python_install=true"
) else (
    echo Python installed.
    set "python_install=false"
)

echo.
echo Checking Is Tkinter installed...
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo tkinter not installed.
    set "tkinter_install=true"
) else (
    echo tkinter installed.
    set "tkinter_install=false"
)

echo.
echo Checked the status of the requirements.
echo.

if "%python_install%"=="true" (
    set /p install_python="Python is not installed, do you want to install it? (Y/N): "
    if /i "%install_python%"=="Y" (
        echo Loading Python...
        start https://www.python.org/downloads/
    ) else (
        echo Python is not installed.
    )
)

if "%tkinter_install%"=="true" (
    set /p install_tkinter="tkinter is not installed, do you want to install it? (Y/N): "
    if /i "%install_tkinter%"=="Y" (
        echo Loading tkinter...
        pip install tk
    ) else (
        echo tkinter is not installed.
    )
)

pause
