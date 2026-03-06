@echo off
cd /d "%~dp0"
echo === Tender RF Backend ===

if not exist venv (
    echo Creating virtual environment...
    "C:\Users\Mila\AppData\Local\Programs\Python\Launcher\py.exe" -3 -m venv venv
    if errorlevel 1 (
        echo ERROR: Python not found. Install from python.org and add to PATH.
        pause
        exit /b 1
    )
)

echo Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo Starting API server at http://localhost:8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
