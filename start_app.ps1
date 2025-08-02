Write-Host "Starting Google Search Trends Application..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Start Python backend server
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn server:app --host 0.0.0.0 --port 8000" -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Next.js frontend server
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd webapp; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "Application starting..." -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 