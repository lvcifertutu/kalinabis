#!/bin/bash

# Start Flask backend
echo "🔮 Starting Kalinabis Flask Backend..."
python servidor.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 2

# Start Next.js frontend
echo "🌙 Starting Kalinabis Next.js Frontend..."
npm run dev &
NEXT_PID=$!

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   KALINABIS FASE 1 — DESARROLLO        ║"
echo "╠════════════════════════════════════════╣"
echo "║ Backend (Flask):    http://localhost:5000"
echo "║ Frontend (Next.js): http://localhost:3001"
echo "║                                        ║"
echo "║ Presiona Ctrl+C para detener ambos.    ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Handle Ctrl+C
trap "kill $FLASK_PID $NEXT_PID" INT
wait
