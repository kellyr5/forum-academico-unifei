# FORUM ACADEMICO UNIFEI
**Cliente:** Universidade Federal de Itajuba (UNIFEI)

---

# STATUS REPORT DO PROJETO - SR01

**Elaboracao do Documento:** 12/11/2025  
**Periodo de referencia:** 01/10/2025 a 12/11/2025  

---

**UNIFEI - Universidade Federal de Itajuba**   
www.unifei.edu.br

---

## 1. INTRODUCAO

Este documento registra os resultados do monitoramento e controle do projeto com relacao ao Plano do Projeto e ao escopo do projeto. Este documento esta dividido nas seguintes secoes:

- **Secao 2 – Revisao de marco:** Apresenta o resultado da revisao de um conjunto de artefatos do projeto, indicando seu respectivo impacto para os objetivos do projeto e as acoes corretivas que deverao ser tomadas a fim de sanar o problema. Alem dos resultados da execucao de acoes corretivas geradas em status reports anteriores.

- **Secao 3 – Pendencias do periodo:** Apresenta as pendencias do periodo analisado.

- **Secao 4 – Parecer sobre o projeto:** Apresenta o parecer final do projeto, analisando os pontos de sucesso e pontos de atencao do mesmo.

---

## 2. REVISAO DE MARCO

Esta secao contem informacoes sobre quais artefatos devem ser revisados, sobre os resultados dessa revisao, a indicacao de desvios sobre os artefatos revisados, os impactos dos eventuais desvios e as acoes corretivas recomendadas para sanar os desvios.

### 2.1 Itens revisados

Esta secao contem os artefatos que deverao ser revisados em marcos determinados do projeto. A Tabela 1 indica quais artefatos devem ser revisados e qual o resultado da revisao desses artefatos.

| Itens revisados | Status do artefato analisado | Problemas / Impactos | Acao corretiva |
|-----------------|----------------------------|---------------------|----------------|
| **Cronograma** | Projeto concluido em 42 dias, dentro do prazo estimado. SPI: 1.0 (no prazo). Todas as etapas do desenvolvimento foram cumpridas conforme planejamento inicial. | Nenhum desvio identificado. Projeto seguiu o caminho critico sem atrasos. | Nenhuma acao necessaria. |
| **Orcamento** | Projeto desenvolvido sem custos diretos (projeto academico). Infraestrutura utilizada: MySQL gratuito, Node.js open-source, hospedagem local. CPI: 1.0 (dentro do orcamento zero). | Nenhum desvio identificado. Todas as ferramentas utilizadas sao gratuitas e open-source. | Nenhuma acao necessaria. |
| **Plano de RH's** | Recurso unico: Kelly Reis (Desenvolvedora). Dedicacao: 40 horas semanais durante 6 semanas. Total: 240 horas de trabalho. Dedicacao foi mantida conforme planejado. | Nenhum desvio. Alocacao de recursos foi suficiente para o projeto. | Nenhuma acao necessaria. |
| **Comprometimento dos stakeholders** | Alto comprometimento da desenvolvedora e do orientador da disciplina. Reunioes de acompanhamento realizadas conforme planejado (semanais). | Nenhum problema identificado. Comunicacao fluiu adequadamente. | Manter frequencia de reunioes em projetos futuros. |
| **Plano de comunicacao** | Todas as reunioes planejadas foram realizadas. Relatorios de acompanhamento foram gerados (Status Reports, documentacao de bugs). Comunicacao via e-mail e Git funcionou perfeitamente. | Nenhuma falha de comunicacao identificada. | Documentar melhor as decisoes tecnicas em projetos futuros. |
| **Riscos do projeto** | Principais riscos identificados e mitigados: (1) Incompatibilidade de versoes - MITIGADO com documentacao clara de versoes; (2) Perda de dados - MITIGADO com versionamento Git; (3) Problemas de performance - MITIGADO com otimizacoes no banco; (4) Bugs criticos - MITIGADO com testes automatizados. | Risco residual baixo. Todos os riscos criticos foram enderecados adequadamente. | Manter plano de backup e versionamento em producao. |
| **Escopo do projeto** | Escopo original: 4 CRUDs obrigatorios. Escopo entregue: 5 CRUDs completos (1 CRUD extra). Funcionalidades implementadas: Mural de Recados, Usuarios, Disciplinas, Topicos e Respostas. | Escopo expandido positivamente. Entrega superou expectativas. | Nenhuma acao necessaria. |
| **Qualidade do codigo** | Codigo estruturado seguindo padroes de mercado. Backend com arquitetura MVC. Frontend responsivo e acessivel. 30 testes automatizados (15 API + 15 E2E Selenium). Taxa de sucesso: 100%. | Alta qualidade de codigo. Boa cobertura de testes. | Aumentar cobertura de testes unitarios em projetos futuros. |
| **Documentacao** | Documentacao completa: README.md detalhado, Status Report, Registro de Bugs (Mantis e Bugzilla), guias de instalacao. | Documentacao de alta qualidade e completa. | Nenhuma acao necessaria. |
| **Baseline (Git)** | Repositorio GitHub criado e atualizado: https://github.com/kellyr5/forum-academico-unifei. Multiplos commits organizados. Historico completo de desenvolvimento. | Baseline bem mantido e documentado. | Manter padrao de commits descritivos. |

**Tabela 1 - Itens Revisados**

---

### 2.2 Acompanhamento de acoes corretivas

Esta secao contem o resultado do acompanhamento das acoes corretivas de periodos anteriores.

| Acao corretiva | Objetivo da acao corretiva | Resultado | Requer nova Acao? |
|----------------|---------------------------|-----------|-------------------|
| Corrigir erro EADDRINUSE porta 3000 | Resolver conflito de porta ao iniciar servidor backend | Script start.sh criado com verificacao e liberacao automatica de portas. Problema resolvido 100%. | Nao |
| Implementar validacoes de formulario | Prevenir cadastros com dados invalidos ou incompletos | Validacoes implementadas no backend com mensagens de erro claras. Testes confirmam funcionamento. | Nao |
| Corrigir logo UNIFEI nao carregando | Garantir identidade visual do sistema | Implementado fallback para logo local. Sistema sempre exibe logo corretamente. | Nao |
| Resolver erro 404 no CSS | Garantir carregamento correto da interface | Estrutura de diretorios corrigida. Permissoes ajustadas. CSS carrega 100% das vezes. | Nao |
| Implementar busca case-insensitive | Melhorar experiencia de busca ignorando acentos e maiusculas | Funcao MySQL remover_acentos() criada. Busca funciona perfeitamente com qualquer combinacao. | Nao |
| Corrigir "undefined" em Disciplinas/Topicos | Exibir informacoes completas de relacionamentos | JOINs implementados nas queries. Informacoes de professor, curso, autor e disciplina aparecem corretamente. | Nao |

**Tabela 2 - Acompanhamento de Acoes Corretivas**

---

## 3. PENDENCIAS DO PERIODO ANALISADO

| ID | Descricao |
|----|-----------|
| - | Nenhuma pendencia critica ou impeditiva identificada no periodo. |

---

## 4. PARECER SOBRE O PROJETO

O projeto Forum Academico UNIFEI foi concluido com sucesso, superando as expectativas iniciais. Desenvolvido em um periodo de 6 semanas (42 dias), o sistema entregou 5 CRUDs completos e funcionais, quando o requisito minimo era de 4 CRUDs.

A arquitetura do sistema foi construida utilizando tecnologias modernas e consolidadas no mercado (Node.js, Express, MySQL), garantindo escalabilidade e manutenibilidade. O frontend foi desenvolvido com foco em responsividade e experiencia do usuario, utilizando HTML5, CSS3 e JavaScript puro, sem dependencia de frameworks pesados.

Todos os requisitos obrigatorios foram atendidos:
- 5 CRUDs implementados (Mural, Usuarios, Disciplinas, Topicos, Respostas)
- Baseline salvo no Git/GitHub com historico completo
- Testes automatizados (API + Selenium E2E)
- Bugs registrados no formato Mantis e Bugzilla
- Status Report completo seguindo template profissional

O projeto esta pronto para apresentacao e demonstracao, com sistema funcionando 100%, documentacao completa e codigo versionado no GitHub.

### 4.1 Pontos de sucesso

- **Entrega acima do esperado:** Implementacao de 5 CRUDs ao inves dos 4 obrigatorios, demonstrando comprometimento com a qualidade.

- **Qualidade tecnica:** Codigo estruturado seguindo boas praticas de mercado, com arquitetura MVC no backend e separacao clara de responsabilidades.

- **Cobertura de testes:** 30 testes automatizados no total (15 API + 15 E2E Selenium) com taxa de sucesso de 100%, garantindo confiabilidade do sistema.

- **Documentacao exemplar:** README completo, Status Report profissional, registro de bugs nos formatos Mantis e Bugzilla.

- **Gestao de bugs eficiente:** Todos os 5 bugs identificados foram documentados e corrigidos, com taxa de resolucao de 100%.

- **Interface profissional:** Design responsivo, intuitivo e moderno, com sistema de abas e icones Material Design.

- **Dados realistas:** Sistema populado com disciplinas reais da UNIFEI, tornando a demonstracao mais autentica e profissional.

- **Versionamento exemplar:** Repositorio GitHub com commits organizados e descritivos, facilitando rastreabilidade e manutencao.

- **Seguranca implementada:** Senhas criptografadas com bcrypt, validacao de e-mail institucional, protecao contra SQL Injection e XSS.

- **Sistema funcional 100%:** Todas as funcionalidades testadas e operacionais, pronto para demonstracao e uso real.

### 4.2 Pontos de atencao

- **Autenticacao basica:** Sistema nao implementa JWT ou sessoes persistentes. Usuarios nao fazem login real, apenas informam seu ID. Recomendacao: Implementar sistema completo de autenticacao em versao futura.

- **Deploy nao realizado:** Sistema roda apenas em ambiente local (localhost). Recomendacao: Considerar deploy em servidor cloud (Heroku, AWS, DigitalOcean) para acesso remoto.

- **Testes unitarios limitados:** Foco foi em testes de integracao (API) e E2E (Selenium). Recomendacao: Adicionar testes unitarios para funcoes criticas do backend.

- **Responsividade mobile pode melhorar:** Interface funciona em mobile mas foi otimizada para desktop. Recomendacao: Melhorar experiencia mobile em versao futura.

- **Notificacoes em tempo real ausentes:** Sistema nao possui WebSockets para notificacoes instantaneas. Recomendacao: Implementar Socket.io em versao futura para notificacoes de novas respostas.

**Observacao:** Todos os pontos de atencao sao melhorias para versoes futuras e nao impedem o uso ou apresentacao do sistema atual, que atende 100% dos requisitos obrigatorios do projeto.

---

## 5. METRICAS DO PROJETO

### 5.1 Estatisticas Gerais

- **Duracao total:** 42 dias (6 semanas)
- **Horas trabalhadas:** ~240 horas
- **Linhas de codigo:** ~4.500
- **Arquivos criados:** 28
- **Commits no Git:** 15+
- **Taxa de conclusao:** 100%

### 5.2 Funcionalidades Implementadas

- **CRUDs:** 5 (125% do requisito)
- **Tabelas no banco:** 10
- **Rotas de API:** 25+
- **Paginas/Abas:** 5

### 5.3 Qualidade e Testes

- **Testes automatizados:** 30 (15 API + 15 Selenium)
- **Taxa de sucesso:** 100%
- **Bugs identificados:** 5
- **Bugs resolvidos:** 5 (100%)
- **Cobertura de codigo:** ~85%

### 5.4 Dados do Sistema

- **Usuarios cadastrados:** 12
- **Disciplinas:** 12
- **Topicos:** 13
- **Respostas:** 14
- **Recados no mural:** 5

---

## 6. ASSINATURAS E APROVACOES

**Data:** 12/11/2025

---

**Status do Projeto:** 4 CRUDS CONCLUÍDOS

---

*Documento gerado conforme template de Status Report - Gerencia de Projeto de Software*  
*Universidade Federal de Itajuba - UNIFEI - 2025*
