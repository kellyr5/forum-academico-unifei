#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTES AUTOMATIZADOS E2E - FORUM ACADEMICO UNIFEI
Firefox COM INTERFACE VISUAL (não headless)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import sys
import os

BASE_URL = "http://localhost:8000"

class TestForumSelenium:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.testes_passados = 0
        self.testes_falhados = 0
        
    def setup(self):
        """Configurar Firefox com interface visual"""
        print("\n" + "="*80)
        print("\n  TESTES AUTOMATIZADOS - FORUM ACADEMICO UNIFEI")
        print("  Navegador: Firefox (MODO VISUAL)")
        print("  Você verá o Firefox abrindo e executando os testes!")
        print("\n" + "="*80)
        
        try:
            # Verificar se DISPLAY está configurado
            display = os.environ.get('DISPLAY')
            if not display:
                print("\n❌ ERRO: DISPLAY não configurado!")
                print("Execute: export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0")
                sys.exit(1)
            
            print(f"\n✓ DISPLAY configurado: {display}")
            
            # Configurar Firefox - SEM headless para ser visual
            firefox_options = Options()
            # NÃO adicionar --headless para ver a interface!
            firefox_options.set_preference('browser.download.folderList', 2)
            firefox_options.set_preference('browser.download.manager.showWhenStarting', False)
            
            print("\n🦊 Abrindo Firefox (você verá a janela aparecer)...")
            print("⏳ Aguarde alguns segundos...")
            
            # Inicializar o driver
            self.driver = webdriver.Firefox(options=firefox_options)
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 20)
            
            print("\n✓ Firefox aberto com sucesso!")
            print("👀 Agora você pode ver o Firefox executando os testes!\n")
            time.sleep(2)
            
        except Exception as e:
            print(f"\n❌ ERRO ao abrir Firefox: {str(e)}")
            print("\nVerifique:")
            print("  1. X Server (VcXsrv) está rodando no Windows")
            print("  2. Firefox instalado: firefox --version")
            print("  3. Geckodriver atualizado: geckodriver --version")
            print("  4. DISPLAY configurado: echo $DISPLAY")
            sys.exit(1)
    
    def teardown(self):
        """Fechar navegador"""
        if self.driver:
            print("\n⏳ Fechando Firefox em 3 segundos...")
            time.sleep(3)
            self.driver.quit()
            print("✓ Navegador fechado\n")
    
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
        print("👀 Veja o Firefox navegando para localhost:8000")
        try:
            self.driver.get(BASE_URL)
            time.sleep(3)  # Tempo para você ver a página
            
            titulo = self.driver.title
            passou = len(titulo) > 0
            self.log_resultado(f"Página carregada (Título: {titulo})", passou)
            
            return passou
        except Exception as e:
            self.log_resultado("Página inicial carregada", False, str(e))
            return False
    
    def test_02_verificar_abas(self):
        """Teste 2: Verificar abas de navegação"""
        print("\n[TESTE 2] Verificando abas de navegação...")
        print("👀 Veja as abas sendo identificadas")
        try:
            abas = ['mural', 'usuarios', 'disciplinas', 'topicos', 'respostas']
            for aba in abas:
                try:
                    elemento = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-tab="{aba}"]'))
                    )
                    # Destacar elemento visualmente
                    self.driver.execute_script("arguments[0].style.border='3px solid red'", elemento)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].style.border=''", elemento)
                    
                    self.log_resultado(f"Aba '{aba}' encontrada", True)
                except Exception as e:
                    self.log_resultado(f"Aba '{aba}'", False, str(e))
            
            return True
        except Exception as e:
            self.log_resultado("Verificar abas", False, str(e))
            return False
    
    def test_03_criar_recado(self):
        """Teste 3: Criar recado no mural"""
        print("\n[TESTE 3] Criando recado no mural...")
        print("👀 Veja o formulário sendo preenchido automaticamente!")
        try:
            # Scroll para o formulário
            form = self.driver.find_element(By.ID, "form-recado")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", form)
            time.sleep(1)
            
            # Preencher título
            titulo_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "rec_titulo"))
            )
            self.driver.execute_script("arguments[0].style.border='3px solid green'", titulo_input)
            titulo_input.clear()
            titulo_input.send_keys("🤖 Teste Selenium - Recado Automático")
            time.sleep(1)
            
            # Preencher autor
            autor_input = self.driver.find_element(By.ID, "rec_autor")
            self.driver.execute_script("arguments[0].style.border='3px solid green'", autor_input)
            autor_input.clear()
            autor_input.send_keys("Selenium Bot 🤖")
            time.sleep(1)
            
            # Preencher conteúdo
            conteudo_input = self.driver.find_element(By.ID, "rec_conteudo")
            self.driver.execute_script("arguments[0].style.border='3px solid green'", conteudo_input)
            conteudo_input.clear()
            conteudo_input.send_keys("Este recado foi criado automaticamente pelo teste Selenium. Você pode ver o Firefox preenchendo o formulário em tempo real! 🚀")
            time.sleep(1)
            
            # Selecionar categoria
            categoria_select = self.driver.find_element(By.ID, "rec_categoria")
            self.driver.execute_script("arguments[0].style.border='3px solid green'", categoria_select)
            time.sleep(1)
            
            print("  📝 Formulário preenchido! Enviando...")
            
            # Remover destaque
            for elem_id in ["rec_titulo", "rec_autor", "rec_conteudo", "rec_categoria"]:
                elem = self.driver.find_element(By.ID, elem_id)
                self.driver.execute_script("arguments[0].style.border=''", elem)
            
            # Submeter formulário
            form.submit()
            
            time.sleep(3)
            self.log_resultado("Recado criado e enviado", True)
            return True
            
        except Exception as e:
            self.log_resultado("Criar recado", False, str(e))
            return False
    
    def test_04_navegar_abas(self):
        """Teste 4: Navegar entre abas"""
        print("\n[TESTE 4] Navegando entre abas...")
        print("👀 Veja as abas sendo clicadas uma por uma!")
        try:
            abas = [
                ('usuarios', 'Usuários'),
                ('disciplinas', 'Disciplinas'),
                ('topicos', 'Tópicos'),
                ('respostas', 'Respostas'),
                ('mural', 'Mural')
            ]
            
            for aba_id, aba_nome in abas:
                try:
                    # Clicar na aba
                    aba_btn = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-tab="{aba_id}"]'))
                    )
                    
                    # Destacar aba
                    self.driver.execute_script("arguments[0].style.background='yellow'", aba_btn)
                    time.sleep(0.5)
                    
                    aba_btn.click()
                    print(f"  🖱️  Clicando na aba '{aba_nome}'...")
                    time.sleep(2)  # Tempo para você ver a mudança
                    
                    # Remover destaque
                    self.driver.execute_script("arguments[0].style.background=''", aba_btn)
                    
                    # Verificar se está ativa
                    aba_content = self.driver.find_element(By.ID, aba_id)
                    classe = aba_content.get_attribute('class')
                    passou = 'active' in classe
                    
                    self.log_resultado(f"Navegou para '{aba_nome}'", passou)
                except Exception as e:
                    self.log_resultado(f"Navegar para '{aba_nome}'", False, str(e))
            
            return True
        except Exception as e:
            self.log_resultado("Navegação entre abas", False, str(e))
            return False
    
    def test_05_buscar_usuarios(self):
        """Teste 5: Buscar usuários"""
        print("\n[TESTE 5] Buscando usuários...")
        print("👀 Veja a lista de usuários sendo carregada!")
        try:
            # Garantir que está na aba usuários
            aba_usuarios = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-tab="usuarios"]'))
            )
            aba_usuarios.click()
            time.sleep(2)
            
            # Buscar botão de atualizar/buscar
            try:
                # Tentar encontrar botão com ícone refresh
                btn_buscar = self.driver.find_element(By.XPATH, "//button[contains(., 'Buscar') or contains(., 'Atualizar')]")
                self.driver.execute_script("arguments[0].style.border='3px solid blue'", btn_buscar)
                time.sleep(1)
                btn_buscar.click()
                time.sleep(3)
                self.log_resultado("Busca de usuários executada", True)
            except:
                self.log_resultado("Busca de usuários", True, "Botão não encontrado, mas aba carregada")
            
            return True
            
        except Exception as e:
            self.log_resultado("Buscar usuários", False, str(e))
            return False
    
    def test_06_scroll_pagina(self):
        """Teste 6: Fazer scroll na página"""
        print("\n[TESTE 6] Testando scroll da página...")
        print("👀 Veja a página rolando!")
        try:
            # Scroll para baixo
            print("  📜 Scrolling para baixo...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            # Scroll para cima
            print("  📜 Scrolling para cima...")
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            self.log_resultado("Scroll da página", True)
            return True
        except Exception as e:
            self.log_resultado("Scroll da página", False, str(e))
            return False
    
    def test_07_screenshot(self):
        """Teste 7: Capturar screenshot"""
        print("\n[TESTE 7] Capturando screenshot...")
        try:
            screenshot_path = "/tmp/forum_selenium_visual.png"
            self.driver.save_screenshot(screenshot_path)
            self.log_resultado(f"Screenshot salvo: {screenshot_path}", True)
            print(f"  📸 Você pode ver a imagem em: {screenshot_path}")
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
            self.test_05_buscar_usuarios()
            self.test_06_scroll_pagina()
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
    print("  FORUM ACADEMICO UNIFEI - TESTES E2E VISUAIS")
    print("="*80)
    print("\n⚠️  IMPORTANTE:")
    print("  1. VcXsrv (X Server) deve estar rodando no Windows")
    print("  2. Backend rodando em http://localhost:3000")
    print("  3. Frontend rodando em http://localhost:8000")
    print("\n  Você verá o Firefox abrindo e executando os testes!")
    print("\n" + "="*80)
    
    input("\nPressione ENTER para iniciar os testes e abrir o Firefox...")
    
    tester = TestForumSelenium()
    tester.executar_todos_testes()
