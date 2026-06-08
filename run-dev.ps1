# Start Kalinabis Development Environment (Windows PowerShell)

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   KALINABIS FASE 1 — DESARROLLO        ║" -ForegroundColor Cyan
Write-Host "╠════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║ Iniciando servicios...                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Start Flask backend in background
Write-Host "🔮 Backend Flask en puerto 5000..." -ForegroundColor Green
$flaskProcess = Start-Process -FilePath "python" -ArgumentList "servidor.py" -PassThru -NoNewWindow
Write-Host "   PID: $($flaskProcess.Id)" -ForegroundColor Gray

# Wait for Flask to start
Start-Sleep -Seconds 2

# Start Next.js frontend in background
Write-Host "🌙 Frontend Next.js en puerto 3001..." -ForegroundColor Green
$nextProcess = Start-Process -FilePath "npm" -ArgumentList "run dev" -PassThru -NoNewWindow
Write-Host "   PID: $($nextProcess.Id)" -ForegroundColor Gray

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         SERVICIOS ACTIVOS              ║" -ForegroundColor Cyan
Write-Host "╠════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║ Backend:  http://localhost:5000        ║" -ForegroundColor Yellow
Write-Host "║ Frontend: http://localhost:3001        ║" -ForegroundColor Yellow
Write-Host "║                                        ║" -ForegroundColor Gray
Write-Host "║ Presiona Ctrl+C para detener.          ║" -ForegroundColor Gray
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Wait for processes
$flaskProcess.WaitForExit()
$nextProcess.WaitForExit()
