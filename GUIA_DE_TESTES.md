# GUIA DE TESTES - Fórum Acadêmico UNIFEI

## 1. MURAL DE RECADOS

### Teste 1.1 - Criar Recado
1. Acesse a aba "Mural"
2. Preencha:
   - Título: "Bem-vindo ao Fórum"
   - Autor: "Administração"
   - Conteúdo: "Sistema está funcionando"
   - Categoria: "Aviso"
3. Clique em "Publicar"
4. Verificar: Mensagem de sucesso + Recado aparece na lista

### Teste 1.2 - Atualizar Lista
1. Clique em "Atualizar Lista"
2. Verificar: Lista é recarregada

### Teste 1.3 - Excluir Recado
1. Clique em "Excluir" em um recado
2. Confirmar exclusão
3. Verificar: Recado removido da lista

## 2. USUÁRIOS

### Teste 2.1 - Cadastrar Usuário
1. Acesse aba "Usuários"
2. Preencha:
   - Nome: "Teste Silva"
   - Email: "teste@unifei.edu.br"
   - Senha: "senha123"
   - Confirmar Senha: "senha123"
   - Curso: Selecione um
   - Período: 5º
   - Tipo: Aluno
3. Clique em "Cadastrar"
4. Verificar: ID do usuário criado

### Teste 2.2 - Buscar Usuário
1. Digite nome parcial
2. Clique em "Buscar"
3. Verificar: Resultados aparecem

## 3. DISCIPLINAS

### Teste 3.1 - Cadastrar Disciplina
1. Acesse aba "Disciplinas"
2. Preencha:
   - Nome: "Teste de Software"
   - Código: "TST001"
   - Curso: Selecione um
   - Professor ID: 1
   - Período: "2024.2"
   - Descrição: "Disciplina de teste"
3. Clique em "Cadastrar"
4. Verificar: ID da disciplina criada

## 4. TÓPICOS

### Teste 4.1 - Criar Tópico
1. Acesse aba "Tópicos"
2. Preencha:
   - Título: "Dúvida sobre Testes"
   - Conteúdo: "Como fazer testes unitários?"
   - Disciplina ID: 1
   - Usuário ID: 1
   - Categoria: Dúvida
   - Tags: "testes,unitários"
3. Clique em "Criar"
4. Verificar: ID do tópico criado

## 5. RESPOSTAS

### Teste 5.1 - Criar Resposta
1. Acesse aba "Respostas"
2. Preencha:
   - Conteúdo: "Use o framework Jest"
   - Tópico ID: 1
   - Usuário ID: 1
3. Clique em "Enviar"
4. Verificar: ID da resposta criada

### Teste 5.2 - Buscar Respostas
1. Digite ID do tópico
2. Clique em "Buscar"
3. Verificar: Respostas aparecem

## CHECKLIST GERAL

- [ ] Sistema carrega sem erros
- [ ] Navegação entre abas funciona
- [ ] Formulários validam campos
- [ ] CRUD de Recados funciona
- [ ] CRUD de Usuários funciona
- [ ] CRUD de Disciplinas funciona
- [ ] CRUD de Tópicos funciona
- [ ] CRUD de Respostas funciona
- [ ] Mensagens de sucesso/erro aparecem
- [ ] Design responsivo funciona
