@echo off
echo Starting Google Search Trends Application...
echo.

REM Activate virtual environment
call .venv\Scripts\Activate.ps1

REM Start Python backend server
start "Python Backend" cmd /k "python -m uvicorn server:app --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start Next.js frontend server
start "Next.js Frontend" cmd /k "cd webapp && npm run dev"

echo.
echo Application starting...
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
pause > nul 