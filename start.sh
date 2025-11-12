#!/bin/bash
cd /mnt/c/Users/kelly/Desktop/forum-academico

sudo killall -9 node python3 2>/dev/null
sudo fuser -k 3000/tcp 8000/tcp 2>/dev/null
sleep 2

echo "Iniciando Backend..."
cd backend
nohup npm start > backend.log 2>&1 &
sleep 5

echo "Iniciando Frontend..."
cd ../frontend
nohup python3 -m http.server 8000 > frontend.log 2>&1 &
sleep 2

echo ""
echo "✅ SISTEMA RODANDO!"
echo "   Backend: http://localhost:3000"
echo "   Frontend: http://localhost:8000"
echo ""
