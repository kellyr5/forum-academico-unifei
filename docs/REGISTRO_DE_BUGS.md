# REGISTRO DE BUGS - FORUM ACADEMICO UNIFEI

**Projeto:** Fórum Acadêmico UNIFEI  
**Desenvolvedor:** Kelly Reis (2023000490)  
**Período:** Outubro - Novembro 2025  
**Total de bugs:** 5  
**Bugs resolvidos:** 5 (100%)

---

## BUG #001 - Porta 3000 já em uso (EADDRINUSE)

**Categoria:** Backend  
**Severidade:** Alta  
**Prioridade:** Alta  
**Status:** Resolvido  
**Data identificação:** 12/11/2025  
**Data resolução:** 12/11/2025

### Descrição
Ao tentar iniciar o servidor Node.js, o sistema retorna erro "Address already in use" na porta 3000. Isso ocorre quando o processo anterior não foi encerrado corretamente.

### Passos para Reproduzir
1. Executar `npm start` no diretório backend
2. Executar `npm start` novamente sem parar o processo anterior
3. Observar erro: `Error: listen EADDRINUSE: address already in use :::3000`

### Causa Raiz
Processos Node.js anteriores não estavam sendo encerrados corretamente ao reiniciar o sistema. O comando `npm start` não verificava se a porta já estava em uso.

### Solução Implementada
Criado script `start.sh` que:
- Verifica se a porta 3000 está em uso
- Encerra processos existentes usando `fuser -k 3000/tcp`
- Aguarda 2 segundos para liberar a porta
- Inicia o servidor backend
- Inicia o servidor frontend na porta 8000

### Impacto
- **Antes:** Desenvolvedor tinha que matar processos manualmente
- **Depois:** Script automatizado resolve o problema

---

## BUG #002 - Formulário não cadastra dados

**Categoria:** Backend  
**Severidade:** Crítica  
**Prioridade:** Urgente  
**Status:** Resolvido  
**Data identificação:** 12/11/2025  
**Data resolução:** 12/11/2025

### Descrição
Ao preencher formulários de cadastro (usuários, disciplinas), o sistema não salva os dados no banco e retorna erro genérico.

### Passos para Reproduzir
1. Acessar http://localhost:8000
2. Preencher formulário de cadastro de usuário
3. Clicar em "Cadastrar"
4. Observar mensagem de erro sem detalhes

### Causa Raiz
- Validações muito restritivas no backend
- Campos obrigatórios não estavam sendo verificados corretamente
- Erro na query SQL de inserção
- Falta de logs detalhados para debug

### Solução Implementada
1. Simplificadas validações no backend
2. Adicionados logs de erro detalhados no console
3. Corrigida query SQL com parâmetros corretos
4. Implementado tratamento de erro com mensagens claras

### Impacto
- **Antes:** Sistema não funcionava, impossível cadastrar dados
- **Depois:** Cadastros funcionam 100%

---

## BUG #003 - Logo UNIFEI não carrega

**Categoria:** Frontend  
**Severidade:** Baixa  
**Prioridade:** Baixa  
**Status:** Resolvido  
**Data identificação:** 12/11/2025  
**Data resolução:** 12/11/2025

### Descrição
Logo da UNIFEI não é exibida no header do sistema. A imagem não carrega deixando um espaço vazio.

### Passos para Reproduzir
1. Acessar http://localhost:8000
2. Observar header da página
3. Logo não aparece

### Causa Raiz
URL da imagem externa estava incorreta ou servidor externo indisponível.

### Solução Implementada
- Implementado fallback para imagem local
- Se a imagem externa não carregar, sistema usa logo local
- Adicionado tratamento de erro de carregamento de imagem

### Impacto
- **Antes:** Identidade visual comprometida
- **Depois:** Logo sempre visível

---

## BUG #004 - CSS não carrega (404)

**Categoria:** Frontend  
**Severidade:** Alta  
**Prioridade:** Alta  
**Status:** Resolvido  
**Data identificação:** 12/11/2025  
**Data resolução:** 12/11/2025

### Descrição
Ao acessar a página, o arquivo style.css retorna erro 404 Not Found. A página fica sem formatação.

### Passos para Reproduzir
1. Acessar http://localhost:8000
2. Verificar console do navegador (F12)
3. Observar erro 404 em style.css

### Causa Raiz
- Estrutura de diretórios incorreta
- Permissões inadequadas nos arquivos
- Caminho relativo errado no HTML

### Solução Implementada
1. Recriada estrutura correta de diretórios
2. Ajustadas permissões com `chmod 644` em todos os arquivos CSS
3. Verificado e corrigido caminho relativo no HTML
4. Testado em múltiplos navegadores

### Impacto
- **Antes:** Interface completamente quebrada
- **Depois:** CSS carrega 100% das vezes

---

## BUG #005 - Busca não encontra palavras com acento

**Categoria:** Backend  
**Severidade:** Média  
**Prioridade:** Normal  
**Status:** Resolvido  
**Data identificação:** 12/11/2025  
**Data resolução:** 12/11/2025

### Descrição
Sistema não encontra resultados ao buscar palavras com acentuação. Exemplo: buscar "fisica" não encontra disciplina "Física".

### Passos para Reproduzir
1. Cadastrar disciplina com nome "Física I"
2. Na busca, digitar "fisica" (sem acento)
3. Observar que nenhum resultado é retornado
4. Mesmo problema com maiúsculas/minúsculas

### Causa Raiz
- Busca era case-sensitive
- Busca não ignorava acentuação
- Comparação direta de strings sem normalização

### Solução Implementada
1. Criada função MySQL `remover_acentos()` que remove acentos
2. Query de busca atualizada para usar `LOWER()` em ambos os lados
3. Busca normaliza tanto o termo buscado quanto os registros no banco
4. Sistema agora é completamente case-insensitive e ignora acentos
```sql
SELECT * FROM disciplinas 
WHERE LOWER(remover_acentos(nome)) LIKE LOWER(remover_acentos('%termo%'))
```

### Impacto
- **Antes:** Usuário tinha que digitar exatamente com acentos
- **Depois:** Busca funciona com qualquer variação

---

## RESUMO ESTATISTICO

| Categoria | Quantidade | Percentual |
|-----------|------------|------------|
| Backend   | 3          | 60%        |
| Frontend  | 2          | 40%        |

| Severidade | Quantidade | Percentual |
|------------|------------|------------|
| Crítica    | 1          | 20%        |
| Alta       | 2          | 40%        |
| Média      | 1          | 20%        |
| Baixa      | 1          | 20%        |

| Status     | Quantidade | Percentual |
|------------|------------|------------|
| Resolvido  | 5          | 100%       |
| Aberto     | 0          | 0%         |

---

## LICOES APRENDIDAS

1. **Validação rigorosa causa problemas:** Validações muito restritivas dificultam o uso do sistema

2. **Testes automatizados detectam bugs:** Bugs #2 e #4 poderiam ter sido detectados com testes

3. **Logs detalhados são essenciais:** Debug é muito mais rápido com logs adequados

4. **Normalização de busca é fundamental:** Usuários esperam busca inteligente, sem se preocupar com acentos

5. **Gerenciamento de processos:** Scripts automatizados evitam erros manuais

---

## FERRAMENTAS DE RASTREAMENTO

Os bugs foram registrados nos seguintes formatos:

- **Mantis Bug Tracker:** BUGS_MANTIS_EXPORT.csv
- **Bugzilla:** BUGS_BUGZILLA_EXPORT.xml
- **Markdown:** REGISTRO_DE_BUGS.md (este arquivo)

---

**Documento gerado por:** Kelly Reis  
**Data:** 12/11/2025  
**Versão:** 1.0
