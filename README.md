# Forum Academico UNIFEI

Sistema web completo de forum academico para a Universidade Federal de Itajuba.

**Disciplina:** Gerencia de Projeto de Software  
**Ano:** 2025

---

## Sobre o Projeto

O Forum Academico UNIFEI e uma plataforma web que facilita a comunicacao e colaboracao entre alunos, professores e monitores. O sistema permite:

- Mural de recados institucional
- Gerenciamento de usuarios (alunos, professores, monitores)
- Cadastro de disciplinas por curso
- Criacao de topicos de discussao
- Sistema de respostas com votacao
- Marcacao de melhores respostas

---

## Tecnologias Utilizadas

### Backend
- Node.js v18+
- Express.js 4.18
- MySQL 8.0
- bcryptjs (criptografia de senhas)

### Frontend
- HTML5 (estrutura semantica)
- CSS3 (design responsivo)
- JavaScript ES6+ (Fetch API)
- Material Icons (Google)

### Testes
- Python 3.10+
- Requests (testes de API)
- Selenium (testes E2E)

---

## Estrutura do Projeto
```
forum-academico/
├── backend/
│   ├── config/
│   │   ├── database.js
│   │   └── init.sql
│   ├── routes/
│   │   ├── auth.js
│   │   ├── usuarios.js
│   │   ├── disciplinas.js
│   │   ├── topicos.js
│   │   ├── respostas.js
│   │   └── recados.js
│   ├── server.js
│   └── package.json
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── index.html
├── tests/
│   ├── test_api.py
│   └── test_selenium.py
├── docs/
│   ├── STATUS_REPORT.md
│   ├── REGISTRO_DE_BUGS.md
│   ├── BUGS_MANTIS_EXPORT.csv
│   └── BUGS_BUGZILLA_EXPORT.xml
├── start.sh
└── README.md
```

---

## Instalacao e Configuracao

### Pre-requisitos

- Node.js 18+
- MySQL 8.0+
- Python 3.10+

### Passo 1: Clonar o Repositorio
```bash
git clone https://github.com/kellyr5/forum-academico-unifei.git
cd forum-academico-unifei
```

### Passo 2: Configurar Banco de Dados
```bash
mysql -u root -p < backend/config/init.sql
```

### Passo 3: Instalar Dependencias Backend
```bash
cd backend
npm install
```

### Passo 4: Configurar Variaveis de Ambiente

Crie arquivo `.env` no diretorio `backend/`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=forum_academico
PORT=3000
```

---

## Como Executar

### Opcao 1: Script Automatico (Recomendado)
```bash
./start.sh
```

### Opcao 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
npm start
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python3 -m http.server 8000
```

**Acesse:** http://localhost:8000

---

## Executar Testes

### Testes de API
```bash
cd tests
python3 test_api.py
```

### Testes E2E com Selenium
```bash
cd tests
python3 test_selenium.py
```

**Resultado esperado:** 30 testes, taxa de sucesso 100%

---

## Funcionalidades Implementadas

### CRUD 1: Mural de Recados
- Create: Publicar recados
- Read: Visualizar todos os recados
- Update: Editar recados (backend)
- Delete: Excluir recados

### CRUD 2: Usuarios
- Create: Cadastrar usuarios com validacao
- Read: Buscar e listar usuarios
- Update: Editar perfil
- Delete: Exclusao logica

### CRUD 3: Disciplinas
- Create: Cadastrar disciplinas
- Read: Listar por curso/professor
- Update: Editar informacoes
- Delete: Remover disciplinas

### CRUD 4: Topicos
- Create: Criar topicos de discussao
- Read: Visualizar com filtros
- Update: Editar conteudo
- Delete: Remover topicos

### CRUD 5: Respostas (BONUS)
- Create: Responder topicos
- Read: Ver respostas ordenadas
- Update: Editar respostas
- Delete: Remover respostas

---

## Seguranca

- Senhas criptografadas com bcrypt
- Validacao de entrada no backend
- Protecao contra SQL Injection
- Protecao contra XSS
- E-mail institucional obrigatorio (@unifei.edu.br)

---

## Estatisticas do Projeto

- **Linhas de codigo:** ~4,500
- **Arquivos:** 28
- **Tabelas no BD:** 10
- **Testes automatizados:** 30
- **Taxa de sucesso:** 100%
- **Bugs corrigidos:** 5

---

## Documentacao

- **Status Report:** `docs/STATUS_REPORT.md`
- **Registro de Bugs:** `docs/REGISTRO_DE_BUGS.md`
- **Bugs Mantis:** `docs/BUGS_MANTIS_EXPORT.csv`
- **Bugs Bugzilla:** `docs/BUGS_BUGZILLA_EXPORT.xml`

---

## Rastreamento de Bugs

Os bugs deste projeto foram registrados e rastreados usando os formatos padrao:

### Mantis Bug Tracker
**Arquivo:** `docs/BUGS_MANTIS_EXPORT.csv`
- Formato: CSV (compativel com Mantis)
- Total de bugs: 5
- Status: Todos resolvidos

### Bugzilla
**Arquivo:** `docs/BUGS_BUGZILLA_EXPORT.xml`
- Formato: XML (formato padrao Bugzilla)
- Total de bugs: 5
- Status: Todos resolvidos (FIXED)

### Estatisticas de Bugs

| Severidade | Quantidade | Resolvidos |
|------------|------------|------------|
| Critica    | 1          | 1 (100%)   |
| Alta       | 2          | 2 (100%)   |
| Media      | 1          | 1 (100%)   |
| Baixa      | 1          | 1 (100%)   |
| **TOTAL**  | **5**      | **5 (100%)**|

---

## Melhorias Futuras

1. Sistema de autenticacao JWT
2. Notificacoes em tempo real (WebSockets)
3. Upload de arquivos em topicos
4. Sistema de busca avancada
5. Dashboard administrativo
6. API REST documentada (Swagger)

---

## Desenvolvedor

**Kelly Reis**  
Estudante de Engenharia de Computacao  
Universidade Federal de Itajuba (UNIFEI)  
Matricula: 2023000490

---

## Licenca

Este projeto foi desenvolvido para fins academicos como parte da disciplina de Gerencia de Projeto de Software.

---

## Agradecimentos

- Professor orientador da disciplina
- UNIFEI - Infraestrutura
- Colegas de turma - Feedback e testes

---

**Copyright 2025 Kelly Reis - Todos os direitos reservados**
