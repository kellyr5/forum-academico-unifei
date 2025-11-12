#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Automatizados - Fórum Acadêmico
Desenvolvido por: Kelly dos Reis Leite
Matrícula: 2023000490
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys

class TestForumAcademico:
    def __init__(self):
        print("=" * 60)
        print("TESTES AUTOMATIZADOS - FÓRUM ACADÊMICO")
        print("=" * 60)
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"
        self.resultados = []
        
    def log_resultado(self, teste, sucesso, mensagem=""):
        status = "✓ PASSOU" if sucesso else "✗ FALHOU"
        self.resultados.append({
            'teste': teste,
            'sucesso': sucesso,
            'mensagem': mensagem
        })
        print(f"\n{status}: {teste}")
        if mensagem:
            print(f"  Detalhe: {mensagem}")
    
    def teste_01_carregar_pagina(self):
        """Teste 01: Verificar se a página principal carrega"""
        try:
            self.driver.get(self.base_url)
            assert "Fórum Acadêmico" in self.driver.title
            self.log_resultado("Teste 01 - Carregar Página Principal", True)
        except Exception as e:
            self.log_resultado("Teste 01 - Carregar Página Principal", False, str(e))
    
    def teste_02_navegacao_secoes(self):
        """Teste 02: Verificar navegação entre seções"""
        try:
            self.driver.get(self.base_url)
            secoes = ['usuarios', 'disciplinas', 'topicos', 'respostas']
            for secao in secoes:
                elemento = self.driver.find_element(By.ID, secao)
                assert elemento is not None
            self.log_resultado("Teste 02 - Navegação entre Seções", True)
        except Exception as e:
            self.log_resultado("Teste 02 - Navegação entre Seções", False, str(e))
    
    def teste_03_formulario_usuario(self):
        """Teste 03: Verificar campos do formulário de usuário"""
        try:
            self.driver.get(self.base_url)
            campos = [
                'nome_completo', 'email', 'senha', 'confirmar_senha',
                'universidade_id', 'curso_id', 'periodo', 'tipo_usuario'
            ]
            for campo in campos:
                elemento = self.driver.find_element(By.ID, campo)
                assert elemento is not None
                assert elemento.is_displayed()
            self.log_resultado("Teste 03 - Formulário de Usuário", True)
        except Exception as e:
            self.log_resultado("Teste 03 - Formulário de Usuário", False, str(e))
    
    def teste_04_validacao_senha(self):
        """Teste 04: Verificar validação de senha"""
        try:
            self.driver.get(self.base_url)
            senha_input = self.driver.find_element(By.ID, 'senha')
            validacao = senha_input.get_attribute('minlength')
            assert validacao == '8'
            self.log_resultado("Teste 04 - Validação de Senha", True)
        except Exception as e:
            self.log_resultado("Teste 04 - Validação de Senha", False, str(e))
    
    def teste_05_selecao_universidade(self):
        """Teste 05: Verificar carregamento de universidades"""
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            select_univ = Select(self.driver.find_element(By.ID, 'universidade_id'))
            opcoes = select_univ.options
            assert len(opcoes) > 1
            self.log_resultado("Teste 05 - Seleção de Universidade", True, 
                             f"Encontradas {len(opcoes)-1} universidades")
        except Exception as e:
            self.log_resultado("Teste 05 - Seleção de Universidade", False, str(e))
    
    def teste_06_formulario_disciplina(self):
        """Teste 06: Verificar campos do formulário de disciplina"""
        try:
            self.driver.get(self.base_url)
            campos = ['disc_nome', 'disc_codigo', 'disc_universidade', 
                     'disc_curso', 'disc_professor', 'disc_periodo']
            for campo in campos:
                elemento = self.driver.find_element(By.ID, campo)
                assert elemento is not None
            self.log_resultado("Teste 06 - Formulário de Disciplina", True)
        except Exception as e:
            self.log_resultado("Teste 06 - Formulário de Disciplina", False, str(e))
    
    def teste_07_validacao_periodo_letivo(self):
        """Teste 07: Verificar validação de formato de período letivo"""
        try:
            self.driver.get(self.base_url)
            periodo_input = self.driver.find_element(By.ID, 'disc_periodo')
            pattern = periodo_input.get_attribute('pattern')
            assert pattern == r'^\d{4}\.[12]$'
            self.log_resultado("Teste 07 - Validação Período Letivo", True)
        except Exception as e:
            self.log_resultado("Teste 07 - Validação Período Letivo", False, str(e))
    
    def teste_08_formulario_topico(self):
        """Teste 08: Verificar campos do formulário de tópico"""
        try:
            self.driver.get(self.base_url)
            campos = ['top_titulo', 'top_conteudo', 'top_disciplina',
                     'top_usuario', 'top_categoria']
            for campo in campos:
                elemento = self.driver.find_element(By.ID, campo)
                assert elemento is not None
            self.log_resultado("Teste 08 - Formulário de Tópico", True)
        except Exception as e:
            self.log_resultado("Teste 08 - Formulário de Tópico", False, str(e))
    
    def teste_09_opcoes_categoria(self):
        """Teste 09: Verificar opções de categoria de tópico"""
        try:
            self.driver.get(self.base_url)
            select_cat = Select(self.driver.find_element(By.ID, 'top_categoria'))
            opcoes_texto = [opt.text for opt in select_cat.options if opt.text != 'Selecione...']
            categorias_esperadas = ['Dúvida', 'Discussão', 'Anúncio']
            assert set(opcoes_texto) == set(categorias_esperadas)
            self.log_resultado("Teste 09 - Opções de Categoria", True)
        except Exception as e:
            self.log_resultado("Teste 09 - Opções de Categoria", False, str(e))
    
    def teste_10_formulario_resposta(self):
        """Teste 10: Verificar campos do formulário de resposta"""
        try:
            self.driver.get(self.base_url)
            campos = ['resp_conteudo', 'resp_topico', 'resp_usuario']
            for campo in campos:
                elemento = self.driver.find_element(By.ID, campo)
                assert elemento is not None
            self.log_resultado("Teste 10 - Formulário de Resposta", True)
        except Exception as e:
            self.log_resultado("Teste 10 - Formulário de Resposta", False, str(e))
    
    def teste_11_limite_caracteres(self):
        """Teste 11: Verificar limites de caracteres nos campos"""
        try:
            self.driver.get(self.base_url)
            limites = {
                'nome_completo': '100',
                'top_titulo': '150',
                'top_conteudo': '5000',
                'resp_conteudo': '3000'
            }
            for campo_id, max_length in limites.items():
                elemento = self.driver.find_element(By.ID, campo_id)
                limite_real = elemento.get_attribute('maxlength')
                assert limite_real == max_length
            self.log_resultado("Teste 11 - Limite de Caracteres", True)
        except Exception as e:
            self.log_resultado("Teste 11 - Limite de Caracteres", False, str(e))
    
    def teste_12_responsividade_basica(self):
        """Teste 12: Verificar responsividade básica"""
        try:
            resolucoes = [(1920, 1080), (768, 1024), (375, 667)]
            for largura, altura in resolucoes:
                self.driver.set_window_size(largura, altura)
                self.driver.get(self.base_url)
                time.sleep(1)
                header = self.driver.find_element(By.CLASS_NAME, 'header')
                assert header.is_displayed()
            self.log_resultado("Teste 12 - Responsividade Básica", True)
        except Exception as e:
            self.log_resultado("Teste 12 - Responsividade Básica", False, str(e))
    
    def teste_13_validacao_email(self):
        """Teste 13: Verificar validação de formato de e-mail"""
        try:
            self.driver.get(self.base_url)
            email_input = self.driver.find_element(By.ID, 'email')
            tipo = email_input.get_attribute('type')
            assert tipo == 'email'
            self.log_resultado("Teste 13 - Validação de E-mail", True)
        except Exception as e:
            self.log_resultado("Teste 13 - Validação de E-mail", False, str(e))
    
    def teste_14_botoes_acao(self):
        """Teste 14: Verificar presença de botões de ação"""
        try:
            self.driver.get(self.base_url)
            botoes = self.driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')
            assert len(botoes) >= 4
            self.log_resultado("Teste 14 - Botões de Ação", True, 
                             f"Encontrados {len(botoes)} botões")
        except Exception as e:
            self.log_resultado("Teste 14 - Botões de Ação", False, str(e))
    
    def teste_15_estrutura_html(self):
        """Teste 15: Verificar estrutura HTML básica"""
        try:
            self.driver.get(self.base_url)
            elementos = ['header', 'main', 'footer']
            for tag in elementos:
                elemento = self.driver.find_element(By.TAG_NAME, tag)
                assert elemento is not None
            self.log_resultado("Teste 15 - Estrutura HTML", True)
        except Exception as e:
            self.log_resultado("Teste 15 - Estrutura HTML", False, str(e))
    
    def gerar_relatorio(self):
        """Gerar relatório final dos testes"""
        print("\n" + "=" * 60)
        print("RELATÓRIO FINAL DOS TESTES")
        print("=" * 60)
        
        total = len(self.resultados)
        aprovados = sum(1 for r in self.resultados if r['sucesso'])
        reprovados = total - aprovados
        taxa_sucesso = (aprovados / total * 100) if total > 0 else 0
        
        print(f"\nTotal de testes executados: {total}")
        print(f"Testes aprovados: {aprovados}")
        print(f"Testes reprovados: {reprovados}")
        print(f"Taxa de sucesso: {taxa_sucesso:.1f}%")
        
        if reprovados > 0:
            print("\n" + "-" * 60)
            print("TESTES QUE FALHARAM:")
            print("-" * 60)
            for resultado in self.resultados:
                if not resultado['sucesso']:
                    print(f"\n✗ {resultado['teste']}")
                    print(f"  Erro: {resultado['mensagem']}")
        
        print("\n" + "=" * 60)
        return taxa_sucesso >= 80
    
    def executar_todos_testes(self):
        """Executar todos os testes"""
        print("\nIniciando execução dos testes...")
        print("-" * 60)
        
        testes = [
            self.teste_01_carregar_pagina,
            self.teste_02_navegacao_secoes,
            self.teste_03_formulario_usuario,
            self.teste_04_validacao_senha,
            self.teste_05_selecao_universidade,
            self.teste_06_formulario_disciplina,
            self.teste_07_validacao_periodo_letivo,
            self.teste_08_formulario_topico,
            self.teste_09_opcoes_categoria,
            self.teste_10_formulario_resposta,
            self.teste_11_limite_caracteres,
            self.teste_12_responsividade_basica,
            self.teste_13_validacao_email,
            self.teste_14_botoes_acao,
            self.teste_15_estrutura_html
        ]
        
        for teste in testes:
            try:
                teste()
            except Exception as e:
                print(f"\nErro crítico ao executar {teste.__name__}: {str(e)}")
            time.sleep(1)
        
        sucesso = self.gerar_relatorio()
        return sucesso
    
    def fechar(self):
        """Fechar o navegador"""
        self.driver.quit()
        print("\nTestes finalizados.")

if __name__ == "__main__":
    tester = TestForumAcademico()
    
    try:
        sucesso = tester.executar_todos_testes()
        tester.fechar()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\nErro fatal: {str(e)}")
        tester.fechar()
        sys.exit(1)
