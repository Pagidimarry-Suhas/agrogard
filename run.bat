@echo off
title AgroGard AI System Launcher
echo ==============================================
echo       🌿 AgroGard AI System Launcher
echo ==============================================

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment 'venv' not found!
    echo Please make sure you have run 'python -m venv venv' and installed 'requirements.txt'.
    pause
    exit /b 1
)

echo Starting FastAPI Backend Processing Engine...
start "AgroGard Backend Server" cmd /c "call venv\Scripts\activate.bat && uvicorn backend.app:app --host 0.0.0.0 --port 8000"

echo Waiting for backend model to initialize into memory...
timeout /t 3 /nobreak >nul

echo Starting Streamlit Web Dashboard...
start "AgroGard Frontend Dashboard" cmd /c "call venv\Scripts\activate.bat && streamlit run frontend/streamlit_app.py"

echo.
echo Both systems have successfully launched in the background!
echo You can use your dashboard now. Have a great day farming!
echo.
pause
