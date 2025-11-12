#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Automatizados com Selenium - Fórum Acadêmico UNIFEI
Desenvolvido por: Kelly dos Reis Leite
Matrícula: 2023000490
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class TestForumAcademico:
    def __init__(self):
        print("=" * 70)
        print("TESTES AUTOMATIZADOS - FÓRUM ACADÊMICO UNIFEI")
        print("Desenvolvido por: Kelly dos Reis Leite - 2023000490")
        print("=" * 70)
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"
        self.resultados = []
        
    def log_resultado(self, teste, sucesso, mensagem=""):
        status = "PASSOU" if sucesso else "FALHOU"
        simbolo = "✓" if sucesso else "✗"
        self.resultados.append({'teste': teste, 'sucesso': sucesso, 'mensagem': mensagem})
        print(f"\n{simbolo} {status}: {teste}")
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
    
    def teste_02_navegacao_abas(self):
        """Teste 02: Verificar navegação entre abas"""
        try:
            self.driver.get(self.base_url)
            abas = ['mural', 'usuarios', 'disciplinas', 'topicos', 'respostas']
            for aba in abas:
                btn = self.driver.find_element(By.CSS_SELECTOR, f'button[data-tab="{aba}"]')
                btn.click()
                time.sleep(1)
                elemento = self.driver.find_element(By.ID, aba)
                assert elemento.is_displayed()
            self.log_resultado("Teste 02 - Navegação entre Abas", True)
        except Exception as e:
            self.log_resultado("Teste 02 - Navegação entre Abas", False, str(e))
    
    def teste_03_crud_mural_create(self):
        """Teste 03: CRUD Mural - CREATE"""
        try:
            self.driver.get(self.base_url)
            
            self.driver.find_element(By.ID, 'rec_titulo').send_keys('Teste Selenium')
            self.driver.find_element(By.ID, 'rec_autor').send_keys('Teste Automatizado')
            self.driver.find_element(By.ID, 'rec_conteudo').send_keys('Recado criado por teste automatizado')
            
            self.driver.find_element(By.CSS_SELECTOR, '#form-recado button[type="submit"]').click()
            time.sleep(2)
            
            mensagem = self.driver.find_element(By.ID, 'mensagem')
            assert 'criado' in mensagem.text.lower() or 'sucesso' in mensagem.text.lower()
            
            self.log_resultado("Teste 03 - CRUD Mural CREATE", True)
        except Exception as e:
            self.log_resultado("Teste 03 - CRUD Mural CREATE", False, str(e))
    
    def teste_04_crud_mural_read(self):
        """Teste 04: CRUD Mural - READ"""
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            
            lista = self.driver.find_element(By.ID, 'lista-recados')
            recados = lista.find_elements(By.CLASS_NAME, 'resultado-item')
            assert len(recados) > 0
            
            self.log_resultado("Teste 04 - CRUD Mural READ", True, f"{len(recados)} recados encontrados")
        except Exception as e:
            self.log_resultado("Teste 04 - CRUD Mural READ", False, str(e))
    
    def teste_05_crud_usuarios(self):
        """Teste 05: Verificar formulário de usuários"""
        try:
            self.driver.get(self.base_url)
            
            btn_usuarios = self.driver.find_element(By.CSS_SELECTOR, 'button[data-tab="usuarios"]')
            btn_usuarios.click()
            time.sleep(1)
            
            form = self.driver.find_element(By.ID, 'form-usuario')
            assert form.is_displayed()
            
            campos = ['nome_completo', 'email', 'senha', 'confirmar_senha', 'curso_id', 'periodo', 'tipo_usuario']
            for campo in campos:
                elemento = self.driver.find_element(By.ID, campo)
                assert elemento is not None
            
            self.log_resultado("Teste 05 - CRUD Usuários - Formulário", True)
        except Exception as e:
            self.log_resultado("Teste 05 - CRUD Usuários - Formulário", False, str(e))
    
    def teste_06_crud_disciplinas(self):
        """Teste 06: Verificar formulário de disciplinas"""
        try:
            self.driver.get(self.base_url)
            
            btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-tab="disciplinas"]')
            btn.click()
            time.sleep(1)
            
            form = self.driver.find_element(By.ID, 'form-disciplina')
            assert form.is_displayed()
            
            self.log_resultado("Teste 06 - CRUD Disciplinas - Formulário", True)
        except Exception as e:
            self.log_resultado("Teste 06 - CRUD Disciplinas - Formulário", False, str(e))
    
    def teste_07_crud_topicos(self):
        """Teste 07: Verificar formulário de tópicos"""
        try:
            self.driver.get(self.base_url)
            
            btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-tab="topicos"]')
            btn.click()
            time.sleep(1)
            
            form = self.driver.find_element(By.ID, 'form-topico')
            assert form.is_displayed()
            
            self.log_resultado("Teste 07 - CRUD Tópicos - Formulário", True)
        except Exception as e:
            self.log_resultado("Teste 07 - CRUD Tópicos - Formulário", False, str(e))
    
    def teste_08_crud_respostas(self):
        """Teste 08: Verificar formulário de respostas"""
        try:
            self.driver.get(self.base_url)
            
            btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-tab="respostas"]')
            btn.click()
            time.sleep(1)
            
            form = self.driver.find_element(By.ID, 'form-resposta')
            assert form.is_displayed()
            
            self.log_resultado("Teste 08 - CRUD Respostas - Formulário", True)
        except Exception as e:
            self.log_resultado("Teste 08 - CRUD Respostas - Formulário", False, str(e))
    
    def teste_09_responsividade(self):
        """Teste 09: Verificar responsividade"""
        try:
            resolucoes = [(1920, 1080), (768, 1024), (375, 667)]
            for largura, altura in resolucoes:
                self.driver.set_window_size(largura, altura)
                self.driver.get(self.base_url)
                time.sleep(1)
                header = self.driver.find_element(By.CLASS_NAME, 'header')
                assert header.is_displayed()
            
            self.log_resultado("Teste 09 - Responsividade", True)
        except Exception as e:
            self.log_resultado("Teste 09 - Responsividade", False, str(e))
    
    def teste_10_validacao_formularios(self):
        """Teste 10: Verificar validação de campos obrigatórios"""
        try:
            self.driver.get(self.base_url)
            
            btn_submit = self.driver.find_element(By.CSS_SELECTOR, '#form-recado button[type="submit"]')
            btn_submit.click()
            time.sleep(1)
            
            # HTML5 validation deve impedir submit
            titulo = self.driver.find_element(By.ID, 'rec_titulo')
            assert titulo.get_attribute('required') == 'true'
            
            self.log_resultado("Teste 10 - Validação de Formulários", True)
        except Exception as e:
            self.log_resultado("Teste 10 - Validação de Formulários", False, str(e))
    
    def gerar_relatorio(self):
        """Gerar relatório final dos testes"""
        print("\n" + "=" * 70)
        print("RELATÓRIO FINAL DOS TESTES")
        print("=" * 70)
        
        total = len(self.resultados)
        aprovados = sum(1 for r in self.resultados if r['sucesso'])
        reprovados = total - aprovados
        taxa_sucesso = (aprovados / total * 100) if total > 0 else 0
        
        print(f"\nTotal de testes: {total}")
        print(f"Aprovados: {aprovados}")
        print(f"Reprovados: {reprovados}")
        print(f"Taxa de sucesso: {taxa_sucesso:.1f}%")
        
        if reprovados > 0:
            print("\n" + "-" * 70)
            print("TESTES QUE FALHARAM:")
            print("-" * 70)
            for resultado in self.resultados:
                if not resultado['sucesso']:
                    print(f"\n✗ {resultado['teste']}")
                    if resultado['mensagem']:
                        print(f"  Erro: {resultado['mensagem']}")
        
        print("\n" + "=" * 70)
        
        # Salvar relatório em arquivo
        with open('RELATORIO_TESTES.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RELATÓRIO DE TESTES AUTOMATIZADOS\n")
            f.write("Fórum Acadêmico UNIFEI\n")
            f.write("Kelly dos Reis Leite - 2023000490\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total de testes: {total}\n")
            f.write(f"Aprovados: {aprovados}\n")
            f.write(f"Reprovados: {reprovados}\n")
            f.write(f"Taxa de sucesso: {taxa_sucesso:.1f}%\n\n")
            
            for resultado in self.resultados:
                status = "PASSOU" if resultado['sucesso'] else "FALHOU"
                f.write(f"{status}: {resultado['teste']}\n")
                if resultado['mensagem']:
                    f.write(f"  {resultado['mensagem']}\n")
        
        return taxa_sucesso >= 70
    
    def executar_todos_testes(self):
        """Executar todos os testes"""
        print("\nIniciando execução dos testes...")
        print("-" * 70)
        
        testes = [
            self.teste_01_carregar_pagina,
            self.teste_02_navegacao_abas,
            self.teste_03_crud_mural_create,
            self.teste_04_crud_mural_read,
            self.teste_05_crud_usuarios,
            self.teste_06_crud_disciplinas,
            self.teste_07_crud_topicos,
            self.teste_08_crud_respostas,
            self.teste_09_responsividade,
            self.teste_10_validacao_formularios
        ]
        
        for teste in testes:
            try:
                teste()
            except Exception as e:
                print(f"\nErro crítico em {teste.__name__}: {str(e)}")
            time.sleep(1)
        
        sucesso = self.gerar_relatorio()
        return sucesso
    
    def fechar(self):
        """Fechar o navegador"""
        self.driver.quit()
        print("\nTestes finalizados. Relatório salvo em RELATORIO_TESTES.txt")

if __name__ == "__main__":
    import sys
    tester = TestForumAcademico()
    
    try:
        sucesso = tester.executar_todos_testes()
        tester.fechar()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\nErro fatal: {str(e)}")
        tester.fechar()
        sys.exit(1)
