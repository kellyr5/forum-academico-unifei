#!/bin/bash

# Script de inicialização do Fórum Acadêmico
# Desenvolvido por: Kelly dos Reis Leite - 2023000490

clear
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║              FÓRUM ACADÊMICO - UNIFEI                              ║"
echo "║              Inicializando Sistema...                              ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se está no diretório correto
if [ ! -f "backend/server.js" ]; then
    echo "❌ Erro: Execute este script da pasta raiz do projeto!"
    exit 1
fi

# 1. Verificar e iniciar MySQL
echo "🔍 Verificando MySQL..."
if ! sudo service mysql status | grep -q "running"; then
    echo "   Iniciando MySQL..."
    sudo service mysql start
    sleep 3
    
    if sudo service mysql status | grep -q "running"; then
        echo "   ✅ MySQL iniciado com sucesso!"
    else
        echo "   ❌ Erro ao iniciar MySQL"
        exit 1
    fi
else
    echo "   ✅ MySQL já está rodando"
fi

# 2. Testar conexão
echo ""
echo "🔍 Testando conexão com banco de dados..."
if mysql -u root -psenha123 -e "USE forum_academico; SELECT COUNT(*) FROM usuarios;" &>/dev/null; then
    USUARIOS=$(mysql -u root -psenha123 -N -e "USE forum_academico; SELECT COUNT(*) FROM usuarios;")
    echo "   ✅ Conexão OK! ($USUARIOS usuários cadastrados)"
else
    echo "   ❌ Erro na conexão com o banco"
    exit 1
fi

# 3. Iniciar Backend
echo ""
echo "🚀 Iniciando Backend (Node.js)..."
cd backend
npm start &
BACKEND_PID=$!
cd ..
sleep 3

# Verificar se backend iniciou
if ps -p $BACKEND_PID > /dev/null; then
    echo "   ✅ Backend rodando (PID: $BACKEND_PID)"
else
    echo "   ❌ Erro ao iniciar backend"
    exit 1
fi

# 4. Iniciar Frontend
echo ""
echo "🌐 Iniciando Frontend (Python HTTP Server)..."
cd frontend
python3 -m http.server 8000 &
FRONTEND_PID=$!
cd ..
sleep 2

# Verificar se frontend iniciou
if ps -p $FRONTEND_PID > /dev/null; then
    echo "   ✅ Frontend rodando (PID: $FRONTEND_PID)"
else
    echo "   ❌ Erro ao iniciar frontend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 5. Salvar PIDs para poder parar depois
echo "$BACKEND_PID" > .backend.pid
echo "$FRONTEND_PID" > .frontend.pid

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║              ✅ SISTEMA INICIADO COM SUCESSO!                      ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Acesse no navegador:"
echo "   http://localhost:8000/login.html"
echo ""
echo "🔐 Contas de teste:"
echo "   Professor: carlos.silva@unifei.edu.br / Unifei2024"
echo "   Monitor:   joao.santos@unifei.edu.br / Unifei2024"
echo "   Aluna:     2023000490@unifei.edu.br / Unifei2024"
echo ""
echo "⚠️  Para PARAR o sistema, execute: ./stop.sh"
echo ""
echo "Logs aparecerão abaixo..."
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Manter o script rodando e mostrando logs
tail -f backend/*.log 2>/dev/null || sleep infinity
