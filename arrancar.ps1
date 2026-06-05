# Kalinabis - Arrancar servidor
# $env:GROQ_API_KEY = "tu_key_aqui"
Set-Location C:\grimorio
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  KALINABIS - Servidor con Groq" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Abre http://localhost:5000 en tu navegador" -ForegroundColor Yellow
Write-Host ""
python servidor.py
Read-Host "Presiona Enter para cerrar"
