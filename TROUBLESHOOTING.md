# 🔧 TROUBLESHOOTING - Fórum Acadêmico

## Problema: "ECONNREFUSED 127.0.0.1:3306"

### Causa
MySQL não está rodando.

### Solução
```bash
sudo service mysql start
```

Verificar se iniciou:
```bash
sudo service mysql status
```

---

## Problema: "Port 3000 already in use"

### Causa
Já existe um processo rodando na porta 3000.

### Solução
```bash
lsof -i :3000
kill -9 <PID>
```

Ou use o script de parada:
```bash
./stop.sh
```

---

## Problema: "Cannot find module"

### Causa
Dependências do Node.js não instaladas.

### Solução
```bash
cd backend
rm -rf node_modules
npm install
cd ..
```

---

## Problema: Login não funciona

### Verificações
1. MySQL está rodando?
```bash
sudo service mysql status
```

2. Banco existe?
```bash
mysql -u root -psenha123 -e "SHOW DATABASES LIKE 'forum_academico';"
```

3. Usuários existem?
```bash
mysql -u root -psenha123 -e "USE forum_academico; SELECT email FROM usuarios;"
```

### Recriar banco
```bash
mysql -u root -psenha123 < backend/config/init.sql
```

---

## Problema: Frontend não carrega

### Verificações
1. Python está instalado?
```bash
python3 --version
```

2. Porta 8000 está livre?
```bash
lsof -i :8000
```

3. Está no diretório correto?
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico/frontend
python3 -m http.server 8000
```

---

## Reiniciar Tudo do Zero
```bash
# Parar tudo
./stop.sh

# Limpar processos
pkill -f mysql
pkill -f node
pkill -f python3

# Iniciar MySQL
sudo service mysql start

# Recriar banco
mysql -u root -psenha123 < backend/config/init.sql

# Iniciar sistema
./start.sh
```

---

## Verificar Logs

### Backend
```bash
tail -f backend/logs/*.log
```

### MySQL
```bash
sudo tail -f /var/log/mysql/error.log
```

---

## Contato

Se nenhuma solução funcionar:
- **Desenvolvedor:** Kelly dos Reis Leite
- **Matrícula:** 2023000490
- **E-mail:** 2023000490@unifei.edu.br
