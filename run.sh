#!/bin/bash
cd /mnt/c/Users/kelly/Desktop/forum-academico

echo "🔍 Verificando MySQL..."
sudo service mysql status | grep -q "running" || sudo service mysql start
sleep 2

echo "🚀 Iniciando Backend..."
cd backend
npm start > /dev/null 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
cd ..
sleep 3

echo "🌐 Iniciando Frontend..."
cd frontend
python3 -m http.server 8000 > /dev/null 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
cd ..
sleep 2

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ SISTEMA RODANDO!                               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 ACESSE: http://localhost:8000"
echo ""
echo "Para parar: pkill -f 'node server.js'; pkill -f 'python3 -m http.server'"
echo ""
