# Forum Academico UNIFEI

Sistema de forum para comunicacao academica entre alunos, professores e monitores da UNIFEI.

Disciplina: Gerencia de Projeto de Software - 2025

## Funcionalidades

### Sistema de Comunicacao
- **Mural de Recados:** Publicacao de avisos e comunicados institucionais
- **Topicos de Discussao:** Criacao e participacao em discussoes academicas organizadas por disciplina
- **Sistema de Respostas:** Resposta a topicos com sistema de votacao
- **Melhor Resposta:** Marcacao da resposta mais util em cada topico

### Gerenciamento de Dados
- **Usuarios:** Cadastro completo de alunos, professores e monitores
- **Disciplinas:** Organizacao de disciplinas por curso e periodo
- **Busca Inteligente:** Sistema de busca que ignora acentuacao e maiusculas/minusculas
- **Permissoes:** Controle de acesso baseado no tipo de usuario

### Recursos Tecnicos
- Interface responsiva e moderna
- Sistema de validacao de dados
- Seguranca com criptografia de senhas
- API REST completa

## Tecnologias

- Backend: Node.js + Express + MySQL
- Frontend: HTML + CSS + JavaScript
- Testes: Python

## Como rodar

### Backend
```bash
cd backend
npm install
npm start
```

### Frontend
```bash
cd frontend
python3 -m http.server 8000
```

Acesse: http://localhost:8000

## Testes

### Testes de API
```bash
cd tests
python3 test_api.py
```

### Testes Selenium (E2E)
```bash
cd tests
python3 test_selenium.py
```

## Estrutura do Projeto
```
forum-academico/
├── backend/       # API Node.js
├── frontend/      # Interface web
├── tests/         # Testes automatizados
├── docs/          # Documentacao
└── README.md
```

## Bugs Corrigidos

1. Porta 3000 travando
2. Formulario nao cadastrava
3. Logo UNIFEI sumindo
4. CSS nao carregava (404)
5. Busca com acento

Ver detalhes em: docs/REGISTRO_DE_BUGS.md

## Documentacao

- Status Report: docs/STATUS_REPORT.md
- Cronograma: docs/CRONOGRAMA_PROJETO.md
- Bugs (Mantis CSV): docs/BUGS_MANTIS_EXPORT.csv
- Bugs (Bugzilla XML): docs/BUGS_BUGZILLA_EXPORT.xml

## Estatisticas do Projeto

- 5 CRUDs implementados
- 30 testes (100% sucesso)
- 5 bugs identificados e corrigidos
- 4500 linhas de codigo
- 42 dias de desenvolvimento

## Licenca

Projeto academico desenvolvido para a disciplina de Gerencia de Projeto de Software.
Universidade Federal de Itajuba (UNIFEI) - 2025
