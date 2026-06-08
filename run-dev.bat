@echo off
REM ============================================================
REM KALINABIS FASE 1 - Development Server Launcher
REM Windows Batch Script
REM ============================================================

echo.
echo ╔════════════════════════════════════════╗
echo ║   KALINABIS FASE 1 — DESARROLLO       ║
echo ╠════════════════════════════════════════╣
echo ║ Iniciando servicios...                 ║
echo ╚════════════════════════════════════════╝
echo.

REM Kill any existing servers on ports 5000 and 3000+
echo Limpiando puertos...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000 "') do taskkill /pid %%a /f 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| find ":3000 "') do taskkill /pid %%a /f 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| find ":3001 "') do taskkill /pid %%a /f 2>nul

REM Start Flask backend
echo.
echo [1] Iniciando Flask Backend (puerto 5000)...
start "Kalinabis Backend" cmd /k python servidor.py
timeout /t 3 /nobreak

REM Start Next.js frontend
echo.
echo [2] Iniciando Next.js Frontend (puerto 3001+)...
start "Kalinabis Frontend" cmd /k npm run dev

echo.
echo ╔════════════════════════════════════════╗
echo ║       SERVICIOS INICIADOS              ║
echo ╠════════════════════════════════════════╣
echo ║ Backend (Flask):    http://localhost:5000
echo ║ Frontend (Next.js): http://localhost:3001+
echo ║                                        ║
echo ║ Se abrieron 2 ventanas nuevas.        ║
echo ║ Para detener, cierra ambas ventanas. ║
echo ╚════════════════════════════════════════╝
echo.
pause
