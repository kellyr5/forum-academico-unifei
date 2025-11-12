# REGISTRO DE BUGS - FORUM ACADEMICO UNIFEI

**Projeto:** Forum Academico UNIFEI  
**Periodo:** Outubro - Novembro 2025  
**Total de bugs:** 5  
**Bugs resolvidos:** 5 (100%)

---

## BUG #001 - Porta 3000 ja em uso (EADDRINUSE)

**Categoria:** Backend  
**Severidade:** Alta  
**Prioridade:** Alta  
**Status:** Resolvido  
**Data identificacao:** 12/11/2025  
**Data resolucao:** 12/11/2025

### Descricao
Ao tentar iniciar o servidor Node.js, o sistema retorna erro "Address already in use" na porta 3000. Isso ocorre quando o processo anterior nao foi encerrado corretamente.

### Passos para Reproduzir
1. Executar `npm start` no diretorio backend
2. Executar `npm start` novamente sem parar o processo anterior
3. Observar erro: `Error: listen EADDRINUSE: address already in use :::3000`

### Causa Raiz
Processos Node.js anteriores nao estavam sendo encerrados corretamente ao reiniciar o sistema. O comando `npm start` nao verificava se a porta ja estava em uso.

### Solucao Implementada
Criado script `start.sh` que:
- Verifica se a porta 3000 esta em uso
- Encerra processos existentes usando `fuser -k 3000/tcp`
- Aguarda 2 segundos para liberar a porta
- Inicia o servidor backend
- Inicia o servidor frontend na porta 8000

### Impacto
- **Antes:** Desenvolvedor tinha que matar processos manualmente
- **Depois:** Script automatizado resolve o problema

---

## BUG #002 - Formulario nao cadastra dados

**Categoria:** Backend  
**Severidade:** Critica  
**Prioridade:** Urgente  
**Status:** Resolvido  
**Data identificacao:** 12/11/2025  
**Data resolucao:** 12/11/2025

### Descricao
Ao preencher formularios de cadastro (usuarios, disciplinas), o sistema nao salva os dados no banco e retorna erro generico.

### Passos para Reproduzir
1. Acessar http://localhost:8000
2. Preencher formulario de cadastro de usuario
3. Clicar em "Cadastrar"
4. Observar mensagem de erro sem detalhes

### Causa Raiz
- Validacoes muito restritivas no backend
- Campos obrigatorios nao estavam sendo verificados corretamente
- Erro na query SQL de insercao
- Falta de logs detalhados para debug

### Solucao Implementada
1. Simplificadas validacoes no backend
2. Adicionados logs de erro detalhados no console
3. Corrigida query SQL com parametros corretos
4. Implementado tratamento de erro com mensagens claras

### Impacto
- **Antes:** Sistema nao funcionava, impossivel cadastrar dados
- **Depois:** Cadastros funcionam 100%

---

## BUG #003 - Logo UNIFEI nao carrega

**Categoria:** Frontend  
**Severidade:** Baixa  
**Prioridade:** Baixa  
**Status:** Resolvido  
**Data identificacao:** 12/11/2025  
**Data resolucao:** 12/11/2025

### Descricao
Logo da UNIFEI nao e exibida no header do sistema. A imagem nao carrega deixando um espaco vazio.

### Passos para Reproduzir
1. Acessar http://localhost:8000
2. Observar header da pagina
3. Logo nao aparece

### Causa Raiz
URL da imagem externa estava incorreta ou servidor externo indisponivel.

### Solucao Implementada
- Implementado fallback para imagem local
- Se a imagem externa nao carregar, sistema usa logo local
- Adicionado tratamento de erro de carregamento de imagem

### Impacto
- **Antes:** Identidade visual comprometida
- **Depois:** Logo sempre visivel

---

## BUG #004 - CSS nao carrega (404)

**Categoria:** Frontend  
**Severidade:** Alta  
**Prioridade:** Alta  
**Status:** Resolvido  
**Data identificacao:** 12/11/2025  
**Data resolucao:** 12/11/2025

### Descricao
Ao acessar a pagina, o arquivo style.css retorna erro 404 Not Found. A pagina fica sem formatacao.

### Passos para Reproduzir
1. Acessar http://localhost:8000
2. Verificar console do navegador (F12)
3. Observar erro 404 em style.css

### Causa Raiz
- Estrutura de diretorios incorreta
- Permissoes inadequadas nos arquivos
- Caminho relativo errado no HTML

### Solucao Implementada
1. Recriada estrutura correta de diretorios
2. Ajustadas permissoes com `chmod 644` em todos os arquivos CSS
3. Verificado e corrigido caminho relativo no HTML
4. Testado em multiplos navegadores

### Impacto
- **Antes:** Interface completamente quebrada
- **Depois:** CSS carrega 100% das vezes

---

## BUG #005 - Busca nao encontra palavras com acento

**Categoria:** Backend  
**Severidade:** Media  
**Prioridade:** Normal  
**Status:** Resolvido  
**Data identificacao:** 12/11/2025  
**Data resolucao:** 12/11/2025

### Descricao
Sistema nao encontra resultados ao buscar palavras com acentuacao. Exemplo: buscar "fisica" nao encontra disciplina "Fisica".

### Passos para Reproduzir
1. Cadastrar disciplina com nome "Fisica I"
2. Na busca, digitar "fisica" (sem acento)
3. Observar que nenhum resultado e retornado
4. Mesmo problema com maiusculas/minusculas

### Causa Raiz
- Busca era case-sensitive
- Busca nao ignorava acentuacao
- Comparacao direta de strings sem normalizacao

### Solucao Implementada
1. Criada funcao MySQL `remover_acentos()` que remove acentos
2. Query de busca atualizada para usar `LOWER()` em ambos os lados
3. Busca normaliza tanto o termo buscado quanto os registros no banco
4. Sistema agora e completamente case-insensitive e ignora acentos
```sql
SELECT * FROM disciplinas 
WHERE LOWER(remover_acentos(nome)) LIKE LOWER(remover_acentos('%termo%'))
```

### Impacto
- **Antes:** Usuario tinha que digitar exatamente com acentos
- **Depois:** Busca funciona com qualquer variacao

---

## RESUMO ESTATISTICO

| Categoria | Quantidade | Percentual |
|-----------|------------|------------|
| Backend   | 3          | 60%        |
| Frontend  | 2          | 40%        |

| Severidade | Quantidade | Percentual |
|------------|------------|------------|
| Critica    | 1          | 20%        |
| Alta       | 2          | 40%        |
| Media      | 1          | 20%        |
| Baixa      | 1          | 20%        |

| Status     | Quantidade | Percentual |
|------------|------------|------------|
| Resolvido  | 5          | 100%       |
| Aberto     | 0          | 0%         |

---

## LICOES APRENDIDAS

1. **Validacao rigorosa causa problemas:** Validacoes muito restritivas dificultam o uso do sistema

2. **Testes automatizados detectam bugs:** Bugs #2 e #4 poderiam ter sido detectados com testes

3. **Logs detalhados sao essenciais:** Debug e muito mais rapido com logs adequados

4. **Normalizacao de busca e fundamental:** Usuarios esperam busca inteligente, sem se preocupar com acentos

5. **Gerenciamento de processos:** Scripts automatizados evitam erros manuais

---

## FERRAMENTAS DE RASTREAMENTO

Os bugs foram registrados nos seguintes formatos:

- **Mantis Bug Tracker:** BUGS_MANTIS_EXPORT.csv
- **Bugzilla:** BUGS_BUGZILLA_EXPORT.xml
- **Markdown:** REGISTRO_DE_BUGS.md (este arquivo)

---
**Data:** 12/11/2025  
**Versao:** 1.0
