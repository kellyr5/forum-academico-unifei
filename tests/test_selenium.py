#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("ERRO: Bibliotecas nao instaladas!")
    print("Execute: pip3 install selenium webdriver-manager --break-system-packages")
    sys.exit(1)

class TestForumAcademico:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.driver = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def setup(self):
        """Configurar navegador Chrome"""
        print("Configurando Selenium WebDriver...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--remote-debugging-port=9222')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            print("WebDriver configurado!\n")
            return True
        except Exception as e:
            print(f"ERRO ao configurar WebDriver: {e}")
            return False
    
    def teardown(self):
        """Fechar navegador"""
        if self.driver:
            self.driver.quit()
            print("\nNavegador fechado")
    
    def test_resultado(self, nome_teste, passou, detalhe=""):
        """Registrar resultado do teste"""
        if passou:
            print(f"PASSOU: {nome_teste}")
            if detalhe:
                print(f"  Detalhe: {detalhe}")
            self.tests_passed += 1
        else:
            print(f"FALHOU: {nome_teste}")
            if detalhe:
                print(f"  Erro: {detalhe}")
            self.tests_failed += 1
    
    def test_01_carregar_pagina(self):
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            sucesso = "Forum" in self.driver.title or "UNIFEI" in self.driver.page_source
            self.test_resultado("Teste 01 - Carregar pagina principal", sucesso)
        except Exception as e:
            self.test_resultado("Teste 01 - Carregar pagina principal", False, str(e))
    
    def test_02_verificar_header(self):
        try:
            header = self.driver.find_element(By.TAG_NAME, "header")
            sucesso = header.is_displayed()
            self.test_resultado("Teste 02 - Verificar header", sucesso, "Header presente")
        except Exception as e:
            self.test_resultado("Teste 02 - Verificar header", False, str(e))
    
    def test_03_verificar_abas(self):
        try:
            abas = self.driver.find_elements(By.CLASS_NAME, "tab-btn")
            sucesso = len(abas) >= 5
            self.test_resultado("Teste 03 - Verificar 5 abas", sucesso, f"{len(abas)} abas encontradas")
        except Exception as e:
            self.test_resultado("Teste 03 - Verificar 5 abas", False, str(e))
    
    def test_04_aba_mural_funciona(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-recados")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 04 - Aba Mural funciona", sucesso, "Lista de recados visivel")
        except Exception as e:
            self.test_resultado("Teste 04 - Aba Mural funciona", False, str(e))
    
    def test_05_aba_usuarios_funciona(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="usuarios"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-usuarios")
            sucesso = lista.is_displayed() and len(lista.text) > 50
            self.test_resultado("Teste 05 - Aba Usuarios funciona", sucesso, "Lista de usuarios carregada")
        except Exception as e:
            self.test_resultado("Teste 05 - Aba Usuarios funciona", False, str(e))
    
    def test_06_aba_disciplinas_funciona(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="disciplinas"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-disciplinas")
            sucesso = lista.is_displayed() and len(lista.text) > 50
            self.test_resultado("Teste 06 - Aba Disciplinas funciona", sucesso, "Lista de disciplinas carregada")
        except Exception as e:
            self.test_resultado("Teste 06 - Aba Disciplinas funciona", False, str(e))
    
    def test_07_aba_topicos_funciona(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="topicos"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-topicos")
            sucesso = lista.is_displayed() and len(lista.text) > 50
            self.test_resultado("Teste 07 - Aba Topicos funciona", sucesso, "Lista de topicos carregada")
        except Exception as e:
            self.test_resultado("Teste 07 - Aba Topicos funciona", False, str(e))
    
    def test_08_ver_respostas_funciona(self):
        try:
            # Já está na aba topicos
            time.sleep(1)
            botao = self.driver.find_element(By.CSS_SELECTOR, ".topico-card .btn-primary")
            botao.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-respostas")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 08 - Ver respostas funciona", sucesso, "Lista de respostas visivel")
        except Exception as e:
            self.test_resultado("Teste 08 - Ver respostas funciona", False, str(e))
    
    def test_09_voltar_mural(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            aba.click()
            time.sleep(1)
            lista = self.driver.find_element(By.ID, "lista-recados")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 09 - Voltar para mural", sucesso, "Navegacao funcionando")
        except Exception as e:
            self.test_resultado("Teste 09 - Voltar para mural", False, str(e))
    
    def test_10_botao_atualizar(self):
        try:
            botao = self.driver.find_element(By.CSS_SELECTOR, "#mural .btn")
            botao.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-recados")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 10 - Botao atualizar", sucesso, "Atualizacao funcionando")
        except Exception as e:
            self.test_resultado("Teste 10 - Botao atualizar", False, str(e))
    
    def test_11_verificar_rodape(self):
        try:
            footer = self.driver.find_element(By.TAG_NAME, "footer")
            sucesso = footer.is_displayed() and "2025" in footer.text
            self.test_resultado("Teste 11 - Verificar rodape", sucesso, "Rodape presente com ano")
        except Exception as e:
            self.test_resultado("Teste 11 - Verificar rodape", False, str(e))
    
    def test_12_cards_disponiveis(self):
        try:
            # Ir para usuarios
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="usuarios"]')
            aba.click()
            time.sleep(2)
            cards = self.driver.find_elements(By.CLASS_NAME, "usuario-card")
            sucesso = len(cards) > 0
            self.test_resultado("Teste 12 - Cards de usuarios", sucesso, f"{len(cards)} usuarios encontrados")
        except Exception as e:
            self.test_resultado("Teste 12 - Cards de usuarios", False, str(e))
    
    def test_13_disciplinas_tem_dados(self):
        try:
            # Ir para disciplinas
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="disciplinas"]')
            aba.click()
            time.sleep(2)
            cards = self.driver.find_elements(By.CLASS_NAME, "disciplina-card")
            sucesso = len(cards) > 0
            self.test_resultado("Teste 13 - Disciplinas tem dados", sucesso, f"{len(cards)} disciplinas encontradas")
        except Exception as e:
            self.test_resultado("Teste 13 - Disciplinas tem dados", False, str(e))
    
    def test_14_topicos_tem_dados(self):
        try:
            # Ir para topicos
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="topicos"]')
            aba.click()
            time.sleep(2)
            cards = self.driver.find_elements(By.CLASS_NAME, "topico-card")
            sucesso = len(cards) > 0
            self.test_resultado("Teste 14 - Topicos tem dados", sucesso, f"{len(cards)} topicos encontrados")
        except Exception as e:
            self.test_resultado("Teste 14 - Topicos tem dados", False, str(e))
    
    def test_15_screenshot_final(self):
        try:
            self.driver.save_screenshot("screenshot_final.png")
            self.test_resultado("Teste 15 - Screenshot final", True, "Salvo em tests/screenshot_final.png")
        except Exception as e:
            self.test_resultado("Teste 15 - Screenshot final", False, str(e))
    
    def executar_todos_testes(self):
        """Executar todos os testes"""
        print("TESTES AUTOMATIZADOS SELENIUM - FORUM ACADEMICO UNIFEI")
        print("Iniciando execucao dos testes Selenium...\n")
        
        if not self.setup():
            return False
        
        self.test_01_carregar_pagina()
        self.test_02_verificar_header()
        self.test_03_verificar_abas()
        self.test_04_aba_mural_funciona()
        self.test_05_aba_usuarios_funciona()
        self.test_06_aba_disciplinas_funciona()
        self.test_07_aba_topicos_funciona()
        self.test_08_ver_respostas_funciona()
        self.test_09_voltar_mural()
        self.test_10_botao_atualizar()
        self.test_11_verificar_rodape()
        self.test_12_cards_disponiveis()
        self.test_13_disciplinas_tem_dados()
        self.test_14_topicos_tem_dados()
        self.test_15_screenshot_final()
        
        self.teardown()
        
        total = self.tests_passed + self.tests_failed
        taxa_sucesso = (self.tests_passed / total * 100) if total > 0 else 0
        
        print("\nRELATORIO FINAL DOS TESTES")
        print(f"\nTotal de testes: {total}")
        print(f"Aprovados: {self.tests_passed}")
        print(f"Reprovados: {self.tests_failed}")
        print(f"Taxa de sucesso: {taxa_sucesso:.1f}%")
        
        if self.tests_failed > 0:
            print(f"\nTestes que falharam: {self.tests_failed}")
        
        print("\n")
        
        with open("RELATORIO_SELENIUM.txt", "w") as f:
            f.write("RELATORIO DE TESTES SELENIUM\n")
            f.write("Forum Academico UNIFEI\n")
            f.write(f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            f.write("RESULTADOS\n\n")
            f.write(f"Total de testes: {total}\n")
            f.write(f"Aprovados: {self.tests_passed}\n")
            f.write(f"Reprovados: {self.tests_failed}\n")
            f.write(f"Taxa de sucesso: {taxa_sucesso:.1f}%\n\n")
            
            f.write("TESTES REALIZADOS\n\n")
            f.write("1. Carregar pagina principal\n")
            f.write("2. Verificar header\n")
            f.write("3. Verificar 5 abas presentes\n")
            f.write("4. Aba Mural funciona\n")
            f.write("5. Aba Usuarios funciona\n")
            f.write("6. Aba Disciplinas funciona\n")
            f.write("7. Aba Topicos funciona\n")
            f.write("8. Ver respostas funciona\n")
            f.write("9. Voltar para mural\n")
            f.write("10. Botao atualizar\n")
            f.write("11. Verificar rodape\n")
            f.write("12. Cards de usuarios presentes\n")
            f.write("13. Disciplinas tem dados\n")
            f.write("14. Topicos tem dados\n")
            f.write("15. Screenshot final\n\n")
            
            if self.tests_failed == 0:
                f.write("TODOS OS TESTES PASSARAM\n")
            else:
                f.write(f"TESTES QUE FALHARAM\n\nTotal: {self.tests_failed}\n")
        
        print("Relatorio salvo em RELATORIO_SELENIUM.txt")
        
        return taxa_sucesso == 100.0

if __name__ == "__main__":
    teste = TestForumAcademico()
    teste.executar_todos_testes()
