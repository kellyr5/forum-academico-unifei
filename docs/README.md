# FÓRUM ACADÊMICO - UNIFEI

Sistema de gerenciamento de discussões acadêmicas para universidades.

**Desenvolvido por:** Kelly dos Reis Leite  
**Matrícula:** 2023000490  
**Universidade:** UNIFEI - Universidade Federal de Itajubá  

---

## 📋 SOBRE O PROJETO

O Fórum Acadêmico é uma plataforma web completa que facilita a comunicação entre alunos, professores e monitores através de um sistema organizado de tópicos e respostas por disciplinas.

### Funcionalidades Principais:
- ✅ Gerenciamento completo de usuários (CRUD)
- ✅ Cadastro e organização de disciplinas (CRUD)
- ✅ Criação de tópicos de discussão (CRUD)
- ✅ Sistema de respostas aninhadas (CRUD)
- ✅ Sistema de votação em respostas
- ✅ Marcação de melhor resposta
- ✅ Sistema de permissões por tipo de usuário
- ✅ Verificação automática de conteúdo inadequado
- ✅ Log de auditoria completo
- ✅ Interface responsiva e profissional

---

## 🚀 TECNOLOGIAS UTILIZADAS

### Backend
- Node.js v18+
- Express.js 4.18
- MySQL 8.0
- bcryptjs (criptografia)
- express-validator

### Frontend
- HTML5
- CSS3 (Design responsivo e gradientes)
- JavaScript ES6+ (Fetch API)

### Testes
- Selenium WebDriver 4.0
- Python 3.8+

### Ferramentas
- Git (Controle de versão)
- npm (Gerenciador de pacotes)

---

## �� INSTALAÇÃO E CONFIGURAÇÃO

### Pré-requisitos
Certifique-se de ter instalado:
- Node.js e npm
- MySQL Server
- Python 3 e pip3
- Git
- Chromium Browser

### Passo 1: Instalar Dependências do Sistema
```bash
sudo apt update
sudo apt install -y nodejs npm mysql-server git python3 python3-pip chromium-browser
pip3 install selenium webdriver-manager
```

### Passo 2: Configurar o Banco de Dados
```bash
# Iniciar MySQL
sudo service mysql start

# Configurar senha do root
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'senha123';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Criar banco de dados
cd /mnt/c/Users/kelly/Desktop/forum-academico
mysql -u root -psenha123 < backend/config/init.sql
```

### Passo 3: Instalar Dependências do Backend
```bash
cd backend
npm install
cd ..
```

### Passo 4: Inicializar Git
```bash
git init
git config user.name "Kelly dos Reis Leite"
git config user.email "2023000490@unifei.edu.br"
git add .
git commit -m "Initial commit - Fórum Acadêmico"
```

---

## ▶️ EXECUTANDO O SISTEMA

Você precisará de **3 terminais** abertos simultaneamente:

### Terminal 1: Backend (API)
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico/backend
npm start
```
**Aguarde a mensagem:** "Servidor rodando na porta 3000"

### Terminal 2: Frontend (Interface)
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico/frontend
python3 -m http.server 8000
```
**Aguarde a mensagem:** "Serving HTTP on 0.0.0.0 port 8000"

### Terminal 3: Testes (Opcional)
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico/tests
python3 test_selenium.py
```

### Acessar o Sistema
Abra seu navegador e acesse: **http://localhost:8000**

---

## 🧪 EXECUTAR TESTES

Com o sistema rodando (terminais 1 e 2), execute:
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico/tests
python3 test_selenium.py
```

**15 testes serão executados automaticamente:**
1. Carregamento da página
2. Navegação entre seções
3. Formulário de usuário
4. Validação de senha
5. Seleção de universidade
6. Formulário de disciplina
7. Validação de período letivo
8. Formulário de tópico
9. Opções de categoria
10. Formulário de resposta
11. Limite de caracteres
12. Responsividade básica
13. Validação de e-mail
14. Botões de ação
15. Estrutura HTML

---

## 📖 COMO USAR O SISTEMA

### 1. Cadastrar Usuário
1. Preencha o formulário "Cadastrar Novo Usuário"
2. Use e-mail institucional (@unifei.edu.br)
3. Senha mínima de 8 caracteres com letras e números
4. Clique em "Cadastrar Usuário"
5. **Anote o ID do usuário criado**

### 2. Cadastrar Disciplina
1. Preencha o formulário "Cadastrar Nova Disciplina"
2. Informe o ID de um professor cadastrado
3. Use formato AAAA.S para período (ex: 2024.2)
4. Clique em "Cadastrar Disciplina"
5. **Anote o ID da disciplina criada**

### 3. Criar Tópico
1. Preencha título e conteúdo
2. Informe ID da disciplina e do usuário
3. Selecione a categoria
4. Clique em "Criar Tópico"
5. **Anote o ID do tópico criado**

### 4. Criar Resposta
1. Escreva o conteúdo da resposta
2. Informe ID do tópico e do usuário
3. Clique em "Criar Resposta"

### 5. Consultar Dados
Use os formulários de busca em cada seção para visualizar os dados cadastrados.

---

## 🔗 ENDPOINTS DA API

### Base URL
`http://localhost:3000/api`

### Usuários
- `POST /usuarios` - Cadastrar
- `GET /usuarios` - Listar
- `GET /usuarios/:id` - Buscar
- `PUT /usuarios/:id` - Editar
- `DELETE /usuarios/:id` - Excluir

### Disciplinas
- `POST /disciplinas` - Cadastrar
- `GET /disciplinas` - Listar
- `GET /disciplinas/:id` - Buscar
- `PUT /disciplinas/:id` - Editar
- `DELETE /disciplinas/:id` - Excluir

### Tópicos
- `POST /topicos` - Criar
- `GET /topicos` - Listar
- `GET /topicos/:id` - Buscar
- `PUT /topicos/:id` - Editar
- `DELETE /topicos/:id` - Excluir

### Respostas
- `POST /respostas` - Criar
- `GET /respostas/topico/:id` - Listar
- `GET /respostas/:id` - Buscar
- `PUT /respostas/:id` - Editar
- `DELETE /respostas/:id` - Excluir
- `POST /respostas/:id/votar` - Votar
- `POST /respostas/:id/melhor-resposta` - Marcar melhor

---

## 🔒 SEGURANÇA IMPLEMENTADA

- ✅ Senhas criptografadas com bcrypt (salt 10)
- ✅ Validação de entrada em todas as rotas
- ✅ Proteção contra SQL Injection
- ✅ Proteção contra XSS
- ✅ Verificação de palavras inadequadas
- ✅ Log de auditoria para ações críticas
- ✅ Conformidade com LGPD
- ✅ E-mail institucional obrigatório
- ✅ Limites de taxa (rate limiting)

---

## 📊 ESTRUTURA DO BANCO DE DADOS

### Tabelas Principais
1. **universidades** - Cadastro de universidades
2. **cursos** - Cursos por universidade
3. **usuarios** - Usuários do sistema
4. **disciplinas** - Disciplinas oferecidas
5. **topicos** - Tópicos de discussão
6. **respostas** - Respostas aos tópicos
7. **votos** - Sistema de votação
8. **arquivos** - Arquivos anexados
9. **logs_auditoria** - Log de ações
10. **palavras_bloqueadas** - Filtro de conteúdo

---

## �� SOLUÇÃO DE PROBLEMAS

### Problema: "Cannot connect to MySQL"
```bash
sudo service mysql start
mysql -u root -psenha123 -e "SELECT 1;"
```

### Problema: "Port 3000 already in use"
```bash
lsof -i :3000
kill -9 <PID>
```

### Problema: "npm install fails"
```bash
npm cache clean --force
rm -rf node_modules
npm install
```

### Problema: "Selenium tests fail"
```bash
pip3 install --upgrade selenium webdriver-manager
```

---

## 📞 SUPORTE

Para dúvidas ou problemas:
- **Desenvolvedor:** Kelly dos Reis Leite
- **Matrícula:** 2023000490
- **E-mail:** 2023000490@unifei.edu.br

---

## 📄 LICENÇA

Este projeto foi desenvolvido como trabalho acadêmico para a UNIFEI.

---

**Última atualização:** Novembro 2024
