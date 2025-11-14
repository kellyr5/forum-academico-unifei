# Como Restaurar o Checkpoint stable-v1.0

Este documento explica como voltar ao ponto de checkpoint `stable-v1.0` criado antes de modificações futuras.

## Estado do Checkpoint

- ✅ Frontend completo e funcional
- ✅ Backend com API REST
- ✅ Banco de dados SQLite
- ✅ Teste Selenium com contextos coerentes
- ✅ IDs aleatórios do banco de dados
- ✅ Busca de respostas por tópico
- ✅ Todas as funcionalidades testadas

## Métodos de Restauração

### 1. Visualizar apenas (não altera nada)
```bash
git checkout stable-v1.0
```

Para voltar ao estado atual depois:
```bash
git checkout main
```

### 2. Restaurar permanentemente (CUIDADO: descarta mudanças)
```bash
# Voltar ao checkpoint
git reset --hard stable-v1.0

# Forçar push (se já tinha mudanças remotas)
git push origin main --force
```

### 3. Criar novo branch a partir do checkpoint
```bash
git checkout -b meu-novo-branch stable-v1.0
```

### 4. Usar o branch de backup
```bash
# Ver o branch de backup
git checkout backup-stable-v1.0

# Fazer merge no main se quiser
git checkout main
git merge backup-stable-v1.0
```

## Ver Todos os Checkpoints
```bash
# Ver todas as tags
git tag -l

# Ver detalhes de uma tag
git show stable-v1.0

# Ver todos os branches
git branch -a
```

## Comparar Versões
```bash
# Ver diferenças entre agora e o checkpoint
git diff stable-v1.0

# Ver arquivos modificados
git diff --name-only stable-v1.0
```

## Emergência: Algo Deu Muito Errado!
```bash
# RESETAR TUDO para o checkpoint
git reset --hard stable-v1.0
git clean -fd  # Remove arquivos não rastreados
git push origin main --force
```

## Informações

- **Tag**: `stable-v1.0`
- **Branch de backup**: `backup-stable-v1.0`
- **Data de criação**: $(date)
- **Commit**: $(git rev-parse stable-v1.0)
