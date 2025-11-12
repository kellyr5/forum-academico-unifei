# GUIA DE APRESENTAÇÃO - PROFESSOR

**Projeto:** Fórum Acadêmico UNIFEI  
**Aluno:** Kelly Reis  
**Matrícula:** 2023000490  
**Data:** Novembro 2025

---

## 📋 CHECKLIST DE ENTREGA

### ✅ Requisitos Obrigatórios

- [x] **4 CRUDs implementados** (5 CRUDs feitos)
  - CRUD 1: Mural de Recados ✅
  - CRUD 2: Usuários ✅
  - CRUD 3: Disciplinas ✅
  - CRUD 4: Tópicos ✅
  - CRUD 5: Respostas (BÔNUS) ✅

- [x] **Baseline no GIT** ✅
  - Repositório: https://github.com/kellyr5/forum-academico-unifei
  - Commits: Múltiplos commits organizados
  - .gitignore configurado

- [x] **Testes Automatizados** ✅
  - Framework: Python + Requests (API Testing)
  - Total: 15 testes automatizados
  - Taxa de sucesso: 100%
  - Relatório: `RELATORIO_TESTES_API.txt`

- [x] **Registro de Bugs** ✅
  - Documento: `docs/REGISTRO_DE_BUGS.md`
  - Total de bugs: 5
  - Todos corrigidos: 100%

- [x] **Status Report** ✅
  - Documento: `docs/STATUS_REPORT.md`
  - Completo com métricas e estatísticas

---

## 🎯 ROTEIRO DE DEMONSTRAÇÃO (10 minutos)

### 1. INTRODUÇÃO (1 min)

**Dizer:**
"Bom dia, Professor. Desenvolvi o Fórum Acadêmico da UNIFEI, um sistema web completo para comunicação acadêmica. Implementei 5 CRUDs funcionais, testes automatizados e toda a documentação solicitada."

### 2. MOSTRAR REPOSITÓRIO GITHUB (1 min)

**Acessar:** https://github.com/kellyr5/forum-academico-unifei

**Mostrar:**
- README completo
- Estrutura organizada de pastas
- Commits com mensagens descritivas
- Documentação na pasta `docs/`

### 3. DEMONSTRAÇÃO DO SISTEMA (5 min)

**Iniciar o sistema:**
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico
./start.sh
```

**Acessar:** http://localhost:8000

**Demonstrar cada CRUD:**

#### 3.1 Mural de Recados (30s)
- Mostrar recados existentes
- Criar novo recado
- Excluir recado

#### 3.2 Usuários (30s)
- Buscar usuários
- Mostrar lista completa
- Destacar: Kelly Reis (ID: 2023000490)

#### 3.3 Disciplinas (30s)
- Mostrar disciplinas da UNIFEI
- Destacar organização por curso
- 12 disciplinas reais cadastradas

#### 3.4 Tópicos (1 min)
- Mostrar tópicos de discussão
- Demonstrar categorização
- Clicar em "Ver Respostas" de um tópico

#### 3.5 Respostas (1 min)
- Mostrar respostas aos tópicos
- Destacar "Melhor Resposta"
- Sistema de votação implementado

### 4. TESTES AUTOMATIZADOS (2 min)

**Executar:**
```bash
cd tests
python3 test_api.py
```

**Mostrar:**
- 15 testes executados
- Taxa de sucesso: 100%
- Relatório gerado automaticamente

**Explicar:**
"Implementei testes de API que validam todos os 5 CRUDs. São mais confiáveis que Selenium no ambiente WSL."

### 5. DOCUMENTAÇÃO (1 min)

**Mostrar arquivos:**
- `docs/STATUS_REPORT.md` - Relatório completo do projeto
- `docs/REGISTRO_DE_BUGS.md` - 5 bugs identificados e corrigidos
- `README.md` - Documentação técnica

**Destacar:**
- Todos os bugs foram documentados e corrigidos
- Status Report com métricas detalhadas
- Código versionado no GitHub

---

## 💻 COMANDOS PARA DEMONSTRAÇÃO

### Iniciar Sistema
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico
./start.sh
```

### Executar Testes
```bash
cd tests
python3 test_api.py
```

### Ver Commits
```bash
git log --oneline
```

### Parar Sistema
```bash
sudo killall -9 node python3
```

---

## 📊 MÉTRICAS DO PROJETO

- **CRUDs:** 5 (requerido: 4)
- **Linhas de código:** ~4,500
- **Testes:** 15 (100% sucesso)
- **Bugs corrigidos:** 5 (100%)
- **Commits:** Múltiplos organizados
- **Tempo de desenvolvimento:** ~40 horas
- **Documentação:** 100% completa

---

## 🔐 CREDENCIAIS DE TESTE

**Usuário principal:**
- ID: 2023000490
- Nome: Kelly Reis
- Email: kelly.reis@unifei.edu.br

**Dados de teste disponíveis:**
- 5 Usuários
- 12 Disciplinas
- 13 Tópicos
- 14 Respostas
- 3 Recados

---

## 🎓 DIFERENCIAIS DO PROJETO

1. **5 CRUDs ao invés de 4** (requisito extra)
2. **Interface profissional** com abas e ícones
3. **Dados reais da UNIFEI** (disciplinas por curso)
4. **Sistema de votação** nas respostas
5. **Melhor resposta** destacada
6. **Busca inteligente** (ignora acentos e maiúsculas)
7. **Design responsivo** (mobile, tablet, desktop)
8. **Segurança robusta** (criptografia, validações)

---

## 🚀 TECNOLOGIAS

**Backend:** Node.js + Express + MySQL  
**Frontend:** HTML5 + CSS3 + JavaScript  
**Testes:** Python + Requests  
**Versionamento:** Git + GitHub

---

## 📝 LINKS IMPORTANTES

- **GitHub:** https://github.com/kellyr5/forum-academico-unifei
- **Sistema:** http://localhost:8000 (após `./start.sh`)
- **API:** http://localhost:3000/api

---

## ✅ CONCLUSÃO

Projeto completo e funcional, atendendo 100% dos requisitos:
- ✅ 5 CRUDs implementados
- ✅ Versionado no Git/GitHub
- ✅ Testes automatizados
- ✅ Bugs documentados e corrigidos
- ✅ Status Report completo
- ✅ Pronto para apresentação

**Status:** APROVADO PARA ENTREGA
