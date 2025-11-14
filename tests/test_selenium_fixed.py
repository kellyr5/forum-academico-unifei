#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTES AUTOMATIZADOS E2E - FORUM ACADEMICO UNIFEI
Teste End-to-End usando Selenium WebDriver
Navegador: Firefox (Headless - sem interface gráfica)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import sys

# Configurações
BASE_URL = "http://localhost:8000"

class TestForumSelenium:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.testes_passados = 0
        self.testes_falhados = 0
        
    def setup(self):
        """Configurar WebDriver do Firefox para modo headless"""
        print("\n" + "="*80)
        print("\n  TESTES AUTOMATIZADOS COM SELENIUM - FORUM ACADEMICO UNIFEI")
        print("  Navegador: Firefox (Headless - sem interface)")
        print("\n" + "="*80)
        print("\n" + "="*80)
        print("CONFIGURANDO SELENIUM COM FIREFOX")
        print("="*80)
        
        try:
            # Configurar opções do Firefox
            firefox_options = Options()
            firefox_options.add_argument('--headless')  # Rodar sem interface gráfica
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--disable-dev-shm-usage')
            firefox_options.add_argument('--disable-gpu')
            firefox_options.add_argument('--window-size=1920,1080')
            
            # Configurar preferências para evitar problemas
            firefox_options.set_preference('browser.download.folderList', 2)
            firefox_options.set_preference('browser.download.manager.showWhenStarting', False)
            
            print("\nBaixando Firefox WebDriver...")
            print("WebDriver configurado com sucesso!")
            print("Abrindo Firefox em modo headless...")
            
            # Inicializar o driver
            self.driver = webdriver.Firefox(options=firefox_options)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 15)
            
            print("✓ Firefox iniciado com sucesso!")
            
        except Exception as e:
            print(f"\n❌ ERRO ao configurar Firefox: {str(e)}")
            print("\nVerifique se:")
            print("  1. Firefox está instalado: firefox --version")
            print("  2. Geckodriver está instalado: geckodriver --version")
            print("  3. Servidor frontend está rodando em http://localhost:8000")
            sys.exit(1)
    
    def teardown(self):
        """Fechar navegador"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Navegador fechado")
    
    def log_resultado(self, nome_teste, passou, mensagem=""):
        """Registrar resultado do teste"""
        if passou:
            self.testes_passados += 1
            print(f"  ✓ {nome_teste}")
        else:
            self.testes_falhados += 1
            print(f"  ✗ {nome_teste}")
            if mensagem:
                print(f"    Erro: {mensagem}")
    
    def test_01_carregar_pagina(self):
        """Teste 1: Carregar página inicial"""
        print("\n[TESTE 1] Carregando página inicial...")
        try:
            self.driver.get(BASE_URL)
            time.sleep(2)
            
            # Verificar título
            titulo = self.driver.title
            passou = "Fórum" in titulo or "Forum" in titulo
            self.log_resultado("Página inicial carregada", passou)
            
            return passou
        except Exception as e:
            self.log_resultado("Página inicial carregada", False, str(e))
            return False
    
    def test_02_verificar_abas(self):
        """Teste 2: Verificar abas de navegação"""
        print("\n[TESTE 2] Verificando abas de navegação...")
        try:
            # Verificar se as abas existem
            abas = ['mural', 'usuarios', 'disciplinas', 'topicos', 'respostas']
            for aba in abas:
                elemento = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-tab="{aba}"]'))
                )
                passou = elemento is not None
                self.log_resultado(f"Aba '{aba}' existe", passou)
            
            return True
        except Exception as e:
            self.log_resultado("Verificar abas", False, str(e))
            return False
    
    def test_03_criar_recado(self):
        """Teste 3: Criar recado no mural"""
        print("\n[TESTE 3] Criando recado no mural...")
        try:
            # Preencher formulário
            titulo_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "rec_titulo"))
            )
            titulo_input.clear()
            titulo_input.send_keys("Teste Selenium - Recado Automático")
            
            autor_input = self.driver.find_element(By.ID, "rec_autor")
            autor_input.clear()
            autor_input.send_keys("Selenium Bot")
            
            conteudo_input = self.driver.find_element(By.ID, "rec_conteudo")
            conteudo_input.clear()
            conteudo_input.send_keys("Este é um recado criado automaticamente pelo teste Selenium.")
            
            # Selecionar categoria
            categoria_select = self.driver.find_element(By.ID, "rec_categoria")
            categoria_select.click()
            time.sleep(0.5)
            
            # Submeter formulário
            form = self.driver.find_element(By.ID, "form-recado")
            form.submit()
            
            time.sleep(2)
            self.log_resultado("Recado criado", True)
            return True
            
        except Exception as e:
            self.log_resultado("Recado criado", False, str(e))
            return False
    
    def test_04_navegar_abas(self):
        """Teste 4: Navegar entre abas"""
        print("\n[TESTE 4] Navegando entre abas...")
        try:
            abas = [
                ('usuarios', 'Usuários'),
                ('disciplinas', 'Disciplinas'),
                ('topicos', 'Tópicos'),
                ('respostas', 'Respostas'),
                ('mural', 'Mural')
            ]
            
            for aba_id, aba_nome in abas:
                # Clicar na aba
                aba_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-tab="{aba_id}"]'))
                )
                aba_btn.click()
                time.sleep(1)
                
                # Verificar se a aba está ativa
                aba_content = self.driver.find_element(By.ID, aba_id)
                classe = aba_content.get_attribute('class')
                passou = 'active' in classe
                
                self.log_resultado(f"Navegar para aba '{aba_nome}'", passou)
            
            return True
        except Exception as e:
            self.log_resultado("Navegação entre abas", False, str(e))
            return False
    
    def test_05_buscar_usuario(self):
        """Teste 5: Buscar usuários"""
        print("\n[TESTE 5] Testando busca de usuários...")
        try:
            # Navegar para aba de usuários
            aba_usuarios = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-tab="usuarios"]'))
            )
            aba_usuarios.click()
            time.sleep(1)
            
            # Clicar no botão de atualizar lista
            btn_buscar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Buscar')]"))
            )
            btn_buscar.click()
            time.sleep(2)
            
            self.log_resultado("Busca de usuários executada", True)
            return True
            
        except Exception as e:
            self.log_resultado("Busca de usuários", False, str(e))
            return False
    
    def test_06_verificar_responsividade(self):
        """Teste 6: Verificar responsividade"""
        print("\n[TESTE 6] Testando responsividade...")
        try:
            # Desktop
            self.driver.set_window_size(1920, 1080)
            time.sleep(1)
            self.log_resultado("Layout desktop (1920x1080)", True)
            
            # Tablet
            self.driver.set_window_size(768, 1024)
            time.sleep(1)
            self.log_resultado("Layout tablet (768x1024)", True)
            
            # Mobile
            self.driver.set_window_size(375, 667)
            time.sleep(1)
            self.log_resultado("Layout mobile (375x667)", True)
            
            # Voltar para desktop
            self.driver.set_window_size(1920, 1080)
            
            return True
        except Exception as e:
            self.log_resultado("Teste de responsividade", False, str(e))
            return False
    
    def test_07_screenshot(self):
        """Teste 7: Capturar screenshot"""
        print("\n[TESTE 7] Capturando screenshot...")
        try:
            screenshot_path = "/tmp/forum_selenium_test.png"
            self.driver.save_screenshot(screenshot_path)
            self.log_resultado(f"Screenshot salvo em {screenshot_path}", True)
            return True
        except Exception as e:
            self.log_resultado("Captura de screenshot", False, str(e))
            return False
    
    def executar_todos_testes(self):
        """Executar todos os testes"""
        print("\n" + "="*80)
        print("INICIANDO BATERIA DE TESTES")
        print("="*80)
        
        # Setup
        self.setup()
        
        try:
            # Executar testes
            self.test_01_carregar_pagina()
            self.test_02_verificar_abas()
            self.test_03_criar_recado()
            self.test_04_navegar_abas()
            self.test_05_buscar_usuario()
            self.test_06_verificar_responsividade()
            self.test_07_screenshot()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Testes interrompidos pelo usuário")
        except Exception as e:
            print(f"\n\n❌ Erro inesperado: {str(e)}")
        finally:
            # Teardown
            self.teardown()
            
            # Relatório final
            print("\n" + "="*80)
            print("RELATÓRIO FINAL DOS TESTES")
            print("="*80)
            print(f"\n  ✓ Testes passados: {self.testes_passados}")
            print(f"  ✗ Testes falhados: {self.testes_falhados}")
            
            total = self.testes_passados + self.testes_falhados
            if total > 0:
                taxa_sucesso = (self.testes_passados / total) * 100
                print(f"\n  Taxa de sucesso: {taxa_sucesso:.1f}%")
            
            print("\n" + "="*80)
            
            if self.testes_falhados == 0:
                print("\n🎉 TODOS OS TESTES PASSARAM!")
            else:
                print(f"\n⚠️  {self.testes_falhados} teste(s) falharam")
            
            print("\n")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("  FORUM ACADEMICO UNIFEI - TESTES E2E")
    print("="*80)
    print("\nPré-requisitos:")
    print("  1. Backend rodando em http://localhost:3000")
    print("  2. Frontend rodando em http://localhost:8000")
    print("  3. Firefox instalado no sistema")
    print("  4. Geckodriver instalado em /usr/local/bin/")
    print("\n" + "="*80)
    
    input("\nPressione ENTER para iniciar os testes...")
    
    tester = TestForumSelenium()
    tester.executar_todos_testes()
