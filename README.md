# Fórum Acadêmico UNIFEI

Sistema web completo de fórum acadêmico para a Universidade Federal de Itajubá.

**Desenvolvido por:** Kelly Reis  
**Matrícula:** 2023000490  
**Disciplina:** Engenharia de Software  
**Ano:** 2025

---

## Sobre o Projeto

O Fórum Acadêmico UNIFEI é uma plataforma web que facilita a comunicação e colaboração entre alunos, professores e monitores. O sistema permite:

- Mural de recados institucional
- Gerenciamento de usuários (alunos, professores, monitores)
- Cadastro de disciplinas por curso
- Criação de tópicos de discussão
- Sistema de respostas com votação
- Marcação de melhores respostas

---

## Tecnologias Utilizadas

### Backend
- **Node.js** v18+
- **Express.js** 4.18
- **MySQL** 8.0
- **bcryptjs** (criptografia de senhas)

### Frontend
- **HTML5** (estrutura semântica)
- **CSS3** (design responsivo)
- **JavaScript ES6+** (Fetch API)
- **Material Icons** (Google)

### Testes
- **Python** 3.10+
- **Requests** (testes de API)

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
│   └── test_api.py
├── docs/
│   ├── STATUS_REPORT.md
│   ├── REGISTRO_DE_BUGS.md
│   └── TROUBLESHOOTING.md
├── start.sh
└── README.md
```

---

##  Instalação e Configuração

### Pré-requisitos

- Node.js 18+
- MySQL 8.0+
- Python 3.10+

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/forum-academico-unifei.git
cd forum-academico-unifei
```

### Passo 2: Configurar Banco de Dados
```bash
mysql -u root -p < backend/config/init.sql
```

### Passo 3: Instalar Dependências Backend
```bash
cd backend
npm install
```

### Passo 4: Configurar Variáveis de Ambiente

Crie arquivo `.env` no diretório `backend/`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=forum_academico
PORT=3000
```

---

## Como Executar

### Opção 1: Script Automático (Recomendado)
```bash
./start.sh
```

### Opção 2: Manual

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

**Resultado esperado:** 15 testes, taxa de sucesso 100%

---

## Funcionalidades Implementadas

### CRUD 1: Mural de Recados
- Create: Publicar recados
- Read: Visualizar todos os recados
- Update: Editar recados (backend)
- Delete: Excluir recados

### CRUD 2: Usuários
- Create: Cadastrar usuários com validação
- Read: Buscar e listar usuários
- Update: Editar perfil
- Delete: Exclusão lógica

### CRUD 3: Disciplinas
- Create: Cadastrar disciplinas
- Read: Listar por curso/professor
- Update: Editar informações
- Delete: Remover disciplinas

### CRUD 4: Tópicos
- Create: Criar tópicos de discussão
- Read: Visualizar com filtros
- Update: Editar conteúdo
- Delete: Remover tópicos

### CRUD 5: Respostas (BÔNUS)
- Create: Responder tópicos
- Read: Ver respostas ordenadas
- Update: Editar respostas
- Delete: Remover respostas

---

## Segurança

- Senhas criptografadas com bcrypt
- Validação de entrada no backend
- Proteção contra SQL Injection
- Proteção contra XSS
- E-mail institucional obrigatório (@unifei.edu.br)

---

## Estatísticas do Projeto

- **Linhas de código:** ~4,500
- **Arquivos:** 25+
- **Tabelas no BD:** 10
- **Testes automatizados:** 15
- **Taxa de sucesso:** 100%
- **Bugs corrigidos:** 5

---

## Documentação

- **Status Report:** `docs/STATUS_REPORT.md`
- **Registro de Bugs:** `docs/REGISTRO_DE_BUGS.md`
- **Troubleshooting:** `docs/TROUBLESHOOTING.md`

---

## Bugs Conhecidos

Nenhum bug crítico no momento. Veja `docs/REGISTRO_DE_BUGS.md` para histórico.

---

## Melhorias Futuras

1. Sistema de autenticação JWT
2. Notificações em tempo real (WebSockets)
3. Upload de arquivos em tópicos
4. Sistema de busca avançada
5. Dashboard administrativo
6. API REST documentada (Swagger)

---

## Desenvolvedor

**Kelly Reis**  
Estudante de Engenharia de Computação  
Universidade Federal de Itajubá (UNIFEI)  
Matrícula: 2023000490

---

## Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina de Engenharia de Software.

---

**© 2025 Kelly Reis - Todos os direitos reservados**
