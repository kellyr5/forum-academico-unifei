#!/bin/bash

clear
echo "=========================================="
echo "  FORUM ACADEMICO UNIFEI"
echo "=========================================="
echo ""

# Parar processos antigos
echo "Parando processos antigos..."
pkill -f "node server.js" 2>/dev/null
pkill -f "python3 -m http.server" 2>/dev/null
sleep 2

# Iniciar Backend
echo "Iniciando Backend..."
cd backend
node server.js &
BACKEND_PID=$!
cd ..
sleep 3

# Iniciar Frontend
echo "Iniciando Frontend..."
cd frontend
python3 -m http.server 8000 &
FRONTEND_PID=$!
cd ..
sleep 2

echo ""
echo "=========================================="
echo "  SERVIDORES INICIADOS COM SUCESSO"
echo "=========================================="
echo ""
echo "  Backend:  http://localhost:3000"
echo "  Frontend: http://localhost:8000"
echo ""
echo "  Abra o navegador em: http://localhost:8000"
echo ""
echo "=========================================="
echo ""
echo "Pressione Ctrl+C para parar os servidores"
echo ""

# Aguardar
trap "echo ''; echo 'Parando servidores...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
