# Como Subir o Projeto no GitHub

## Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Preencha:
   - **Nome:** `forum-academico-unifei`
   - **Descrição:** `Sistema de Fórum Acadêmico da UNIFEI - Engenharia de Software 2025`
   - **Visibilidade:** Público
3. **NÃO** marque "Initialize with README"
4. Clique em "Create repository"

## Passo 2: Conectar Repositório Local
```bash
cd /mnt/c/Users/kelly/Desktop/forum-academico

# Adicionar remote
git remote add origin https://github.com/SEU_USUARIO/forum-academico-unifei.git

# Verificar
git remote -v
```

## Passo 3: Fazer Commit e Push
```bash
# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Release Final: Sistema completo com 5 CRUDs, testes e documentação - Kelly Reis 2025"

# Renomear branch para main
git branch -M main

# Fazer push
git push -u origin main
```

## Passo 4: Verificar no GitHub

Acesse: `https://github.com/SEU_USUARIO/forum-academico-unifei`

Deve aparecer:
- ✅ Código completo
- ✅ README.md
- ✅ Documentação
- ✅ Testes
- ✅ Histórico de commits

## Comandos Úteis
```bash
# Ver status
git status

# Ver histórico
git log --oneline

# Fazer novo commit
git add .
git commit -m "Descrição da mudança"
git push

# Ver branches
git branch -a

# Clonar em outro lugar
git clone https://github.com/SEU_USUARIO/forum-academico-unifei.git
```

## Pronto!

Seu projeto está no GitHub e pode ser acessado por qualquer pessoa!

**Link para compartilhar:**
`https://github.com/SEU_USUARIO/forum-academico-unifei`
