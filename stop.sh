#!/bin/bash

echo ""
echo "🛑 Parando Fórum Acadêmico..."
echo ""

# Parar processos pelos PIDs salvos
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        echo "✅ Backend parado (PID: $BACKEND_PID)"
    fi
    rm .backend.pid
fi

if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        echo "✅ Frontend parado (PID: $FRONTEND_PID)"
    fi
    rm .frontend.pid
fi

# Garantir que todos os processos foram parados
pkill -f "node server.js" 2>/dev/null
pkill -f "python3 -m http.server 8000" 2>/dev/null

echo ""
echo "✅ Sistema parado com sucesso!"
echo ""
