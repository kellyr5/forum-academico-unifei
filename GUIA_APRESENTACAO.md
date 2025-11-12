# GUIA DE APRESENTAÇÃO - FÓRUM ACADÊMICO UNIFEI

**Aluno:** Kelly dos Reis Leite  
**Matrícula:** 2023000490  
**Disciplina:** Engenharia de Software  

---

## ROTEIRO DE DEMONSTRAÇÃO (15 minutos)

### 1. INTRODUÇÃO (2 min)

**O que falar:**
- "Bom dia, Professor. Desenvolvi o Fórum Acadêmico da UNIFEI"
- "É um sistema web para comunicação acadêmica entre alunos, professores e monitores"
- "Implementei 5 CRUDs completos, testes automatizados, versionamento Git e documentação"

### 2. ARQUITETURA DO SISTEMA (2 min)

**Mostrar no terminal:**
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico
tree -L 2 -I 'node_modules'
```

**O que explicar:**
- "Backend em Node.js + Express + MySQL"
- "Frontend em HTML5, CSS3 e JavaScript puro"
- "10 tabelas no banco de dados com relacionamentos"
- "Testes automatizados com Selenium"

### 3. DEMONSTRAÇÃO DOS CRUDs (8 min)

#### 3.1 Iniciar o Sistema
```bash
# Terminal 1
cd /mnt/c/Users/kelly/Desktop/forum-academico/backend
npm start

# Terminal 2
cd /mnt/c/Users/kelly/Desktop/forum-academico/frontend
python3 -m http.server 8000
```

**Acessar:** http://localhost:8000

#### 3.2 CRUD 1: Mural de Recados (1.5 min)
- Criar recado: "Palestra sobre IA"
- Mostrar listagem
- Excluir recado
- **Destacar:** Sistema de categorias e cores

#### 3.3 CRUD 2: Usuários (1.5 min)
- Cadastrar usuário: "João Silva", "joao@unifei.edu.br"
- Buscar usuário por nome
- Mostrar resultado
- **Destacar:** Validação de e-mail institucional, criptografia de senha

#### 3.4 CRUD 3: Disciplinas (1.5 min)
- Cadastrar: "Engenharia de Software", código "ES001"
- Usar ID=1 como professor
- Buscar disciplinas
- **Destacar:** Associação com cursos e professores

#### 3.5 CRUD 4: Tópicos (1.5 min)
- Criar tópico: "Dúvida sobre MVC"
- Usar IDs da disciplina e usuário criados
- Buscar tópicos
- **Destacar:** Categorização, tags, status

#### 3.6 CRUD 5: Respostas (1.5 min)
- Criar resposta para o tópico
- Buscar respostas do tópico
- **Destacar:** Sistema de votação, melhor resposta, respostas hierárquicas

### 4. TESTES AUTOMATIZADOS (2 min)
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico/tests
python3 test_selenium.py
```

**O que explicar:**
- "10 testes automatizados com Selenium"
- "Testam navegação, formulários, CRUDs e responsividade"
- "Taxa de sucesso: 100%"
- "Relatório salvo em RELATORIO_TESTES.txt"

### 5. VERSIONAMENTO GIT (1 min)
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico
git log --oneline -10
git remote -v
```

**O que explicar:**
- "Projeto versionado com Git"
- "Commits organizados e descritivos"
- "Disponível no GitHub: [mostrar link]"

**Abrir GitHub no navegador:** https://github.com/[SEU_USUARIO]/forum-academico-unifei

### 6. DOCUMENTAÇÃO (30 seg)

**Mostrar arquivos:**
- `docs/README.md` - Guia completo
- `docs/STATUS_REPORT.md` - Relatório de status
- `docs/REGISTRO_DE_BUGS.md` - Bugs identificados e corrigidos

### 7. ENCERRAMENTO (30 seg)

**O que falar:**
- "Sistema completo e funcional"
- "Todos os requisitos atendidos + funcionalidades extras"
- "Código documentado e versionado"
- "Pronto para uso em ambiente de produção"

---

## CHECKLIST ANTES DA APRESENTAÇÃO

### Dia Anterior
- [ ] Testar sistema completo
- [ ] Executar testes Selenium
- [ ] Verificar se GitHub está atualizado
- [ ] Preparar dados de exemplo
- [ ] Revisar documentação

### 30 Minutos Antes
- [ ] Iniciar MySQL: `sudo service mysql start`
- [ ] Testar acesso ao GitHub
- [ ] Verificar navegador atualizado
- [ ] Ter terminais prontos
- [ ] Verificar internet funcionando

### Durante Apresentação
- [ ] Falar claramente
- [ ] Mostrar confiança no código
- [ ] Estar preparado para perguntas
- [ ] Demonstrar conhecimento técnico
- [ ] Destacar diferenciais do projeto

---

## PERGUNTAS FREQUENTES (ANTECIPADAS)

### Q1: "Por que escolheu essas tecnologias?"
**R:** "Escolhi Node.js pela performance e JavaScript no backend e frontend, facilitando manutenção. MySQL pela robustez e relacionamentos complexos."

### Q2: "Como garante a segurança?"
**R:** "Senhas criptografadas com bcrypt, validações no backend, proteção SQL Injection e XSS, e-mail institucional obrigatório."

### Q3: "E se houver muitos usuários simultâneos?"
**R:** "Arquitetura suporta escalonamento horizontal. Banco otimizado com índices. Possibilidade de implementar cache Redis."

### Q4: "Como corrige bugs?"
**R:** "Processo estruturado: identificação, registro, análise de causa raiz, implementação da correção, testes e documentação. Veja docs/REGISTRO_DE_BUGS.md"

### Q5: "Próximos passos?"
**R:** "Autenticação JWT, notificações em tempo real, upload de arquivos, dashboard administrativo e API REST documentada."

---

## DOCUMENTOS PARA MOSTRAR

1. **Código-fonte:** GitHub
2. **Testes:** Executar ao vivo
3. **Status Report:** `docs/STATUS_REPORT.md`
4. **Registro de Bugs:** `docs/REGISTRO_DE_BUGS.md`
5. **README:** `docs/README.md`

---

## COMANDOS RÁPIDOS

### Iniciar Sistema
```bash
# Terminal 1
cd /mnt/c/Users/kelly/Desktop/forum-academico/backend && npm start

# Terminal 2
cd /mnt/c/Users/kelly/Desktop/forum-academico/frontend && python3 -m http.server 8000
```

### Executar Testes
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico/tests
python3 test_selenium.py
```

### Ver Commits
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico
git log --oneline
```

### Parar Sistema
```bash
pkill -f "node server.js"
pkill -f "python3 -m http.server"
```

---

## BOA SORTE NA APRESENTAÇÃO! 🎓
