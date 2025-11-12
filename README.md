# Forum Academico UNIFEI

Sistema de forum para alunos, professores e monitores.

**Desenvolvido por:** Kelly Reis (2023000490)  
**Disciplina:** Gerencia de Projeto de Software

## O que faz

- Mural de recados
- Cadastro de usuarios, disciplinas, topicos, respostas
- Busca que ignora acentos
- Votacao em respostas

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
```bash
cd tests
python3 test_api.py
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

## Estatisticas

- 5 CRUDs implementados
- 30 testes (100% sucesso)
- 5 bugs corrigidos
- 4500 linhas de codigo
- 42 dias de desenvolvimento

## Sobre o Desenvolvimento

Este foi meu primeiro projeto full-stack completo. Aprendi muito sobre Node.js, MySQL e testes automatizados. Os principais desafios foram configurar o ambiente, fazer a busca funcionar com acentos e corrigir os bugs de porta travada.

Kelly Reis - 2023000490
