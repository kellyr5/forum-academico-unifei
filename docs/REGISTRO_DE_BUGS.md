# REGISTRO DE BUGS - Fórum Acadêmico UNIFEI

**Projeto:** Sistema de Fórum Acadêmico  
**Desenvolvedor:** Kelly dos Reis Leite  
**Matrícula:** 2023000490  
**Data:** Novembro 2024

---

## BUG #001 - Porta 8000 já em uso

**Severidade:** Alta  
**Status:** RESOLVIDO  
**Data Identificação:** 12/11/2024  
**Data Resolução:** 12/11/2024

**Descrição:**
Ao tentar iniciar o servidor frontend, o sistema retornava erro "Address already in use" na porta 8000.

**Passos para Reproduzir:**
1. Executar `python3 -m http.server 8000`
2. Tentar executar novamente sem parar o processo anterior

**Causa Raiz:**
Processos anteriores não estavam sendo encerrados corretamente ao reiniciar o sistema.

**Solução Implementada:**
- Adicionado comando `fuser -k 8000/tcp` no script de inicialização
- Criado script `start-persistent.sh` que verifica e mata processos antes de iniciar

**Como Testar:**
```bash
./start-persistent.sh
```

---

## BUG #002 - Formulário não cadastra dados

**Severidade:** Crítica  
**Status:** RESOLVIDO  
**Data Identificação:** 12/11/2024  
**Data Resolução:** 12/11/2024

**Descrição:**
Ao preencher formulários de cadastro (usuários, disciplinas, etc), o sistema não salvava os dados e retornava erro genérico.

**Passos para Reproduzir:**
1. Acessar http://localhost:8000
2. Preencher formulário de usuário
3. Clicar em "Cadastrar"
4. Mensagem de erro aparece

**Causa Raiz:**
- Validações muito restritivas no backend
- Campos obrigatórios não estavam sendo verificados corretamente
- Erro na conexão com banco de dados

**Solução Implementada:**
- Simplificadas validações no backend
- Adicionados logs de erro detalhados
- Corrigida query SQL para inserção

**Como Testar:**
1. Acessar http://localhost:8000
2. Ir em aba "Mural"
3. Preencher e submeter formulário
4. Verificar mensagem de sucesso

---

## BUG #003 - Logo da UNIFEI não carrega

**Severidade:** Baixa  
**Status:** RESOLVIDO  
**Data Identificação:** 12/11/2024  
**Data Resolução:** 12/11/2024

**Descrição:**
Logo da UNIFEI não era exibida no header do sistema.

**Causa Raiz:**
URL da imagem externa estava incorreta ou indisponível.

**Solução Implementada:**
Adicionado fallback para quando imagem externa não carregar.

---

## BUG #004 - CSS não carrega (404)

**Severidade:** Alta  
**Status:** RESOLVIDO  
**Data Identificação:** 12/11/2024  
**Data Resolução:** 12/11/2024

**Descrição:**
Arquivo CSS retornava erro 404 ao acessar a página.

**Passos para Reproduzir:**
1. Acessar http://localhost:8000
2. Verificar console do navegador (F12)
3. Erro 404 em style.css

**Causa Raiz:**
Estrutura de diretórios incorreta ou permissões inadequadas.

**Solução Implementada:**
- Recriada estrutura correta de diretórios
- Ajustadas permissões com `chmod 644`
- Verificado caminho relativo no HTML

---

## BUG #005 - Busca não encontra palavras com acento

**Severidade:** Média  
**Status:** RESOLVIDO  
**Data Identificação:** 12/11/2024  
**Data Resolução:** 12/11/2024

**Descrição:**
Sistema não encontrava resultados ao buscar palavras com acentuação (ex: "Física").

**Solução Implementada:**
- Criada função MySQL `remover_acentos()`
- Atualizada query de busca para usar LOWER() e remover acentos
- Busca agora é case-insensitive e ignora acentuação

**Como Testar:**
1. Cadastrar disciplina "Física"
2. Buscar por "fisica" (sem acento)
3. Resultado deve aparecer

---

## ESTATÍSTICAS

- **Total de bugs:** 5
- **Críticos:** 1
- **Altos:** 2
- **Médios:** 1
- **Baixos:** 1
- **Resolvidos:** 5 (100%)
- **Pendentes:** 0 (0%)

---

## MELHORIAS FUTURAS

1. Adicionar sistema de autenticação JWT
2. Implementar paginação nas listagens
3. Adicionar upload de arquivos em tópicos
4. Notificações em tempo real
5. Sistema de busca avançada com filtros

---

**Documento gerado em:** 12/11/2024  
**Última atualização:** 12/11/2024
