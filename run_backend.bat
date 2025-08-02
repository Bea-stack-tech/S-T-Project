@echo off
echo Starting Python Backend...
call .venv\Scripts\Activate.ps1
python -m uvicorn server:app --host 0.0.0.0 --port 8000
pause 