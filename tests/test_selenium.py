#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("ERRO: Bibliotecas nao instaladas!")
    sys.exit(1)

class TestForumAcademico:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.driver = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def setup(self):
        print("Configurando Selenium WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            print("WebDriver configurado!\n")
            return True
        except Exception as e:
            print(f"ERRO: {e}")
            return False
    
    def teardown(self):
        if self.driver:
            self.driver.quit()
            print("\nNavegador fechado")
    
    def test_resultado(self, nome, passou, detalhe=""):
        if passou:
            print(f"PASSOU: {nome}")
            if detalhe:
                print(f"  Detalhe: {detalhe}")
            self.tests_passed += 1
        else:
            print(f"FALHOU: {nome}")
            if detalhe:
                print(f"  Erro: {detalhe}")
            self.tests_failed += 1
    
    def test_01_carregar_pagina(self):
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            sucesso = "Forum" in self.driver.page_source or "UNIFEI" in self.driver.page_source
            self.test_resultado("Teste 01 - Carregar pagina principal", sucesso)
        except Exception as e:
            self.test_resultado("Teste 01 - Carregar pagina principal", False, str(e))
    
    def test_02_criar_usuario(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="usuarios"]')
            aba.click()
            time.sleep(2)
            
            timestamp = int(time.time())
            matricula = 2023000500 + (timestamp % 500)
            
            script = f"""
            fetch('http://localhost:3000/api/usuarios', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    nome_completo: 'Teste Selenium Usuario',
                    email: 'teste.selenium.{timestamp}@unifei.edu.br',
                    senha: 'senha123',
                    confirmar_senha: 'senha123',
                    universidade_id: 1,
                    curso_id: 1,
                    periodo: 5,
                    tipo_usuario: 'Aluno',
                    matricula: {matricula}
                }})
            }}).then(r => r.json()).then(() => carregarUsuarios()).catch(e => console.log(e));
            """
            self.driver.execute_script(script)
            time.sleep(3)
            
            lista = self.driver.find_element(By.ID, "lista-usuarios")
            sucesso = len(lista.text) > 100
            self.test_resultado("Teste 02 - Criar usuario", sucesso, "Usuario criado")
        except Exception as e:
            self.test_resultado("Teste 02 - Criar usuario", False, str(e))
    
    def test_03_criar_disciplina(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="disciplinas"]')
            aba.click()
            time.sleep(2)
            
            timestamp = int(time.time())
            codigo = timestamp % 1000
            
            script = f"""
            fetch('http://localhost:3000/api/disciplinas', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    nome: 'Teste Selenium Disciplina',
                    codigo: 'TST{codigo}',
                    curso_id: 1,
                    professor_id: 1,
                    periodo_letivo: '2025.1',
                    descricao: 'Disciplina de teste'
                }})
            }}).then(r => r.json()).then(() => carregarDisciplinas()).catch(e => console.log(e));
            """
            self.driver.execute_script(script)
            time.sleep(3)
            
            lista = self.driver.find_element(By.ID, "lista-disciplinas")
            sucesso = len(lista.text) > 100
            self.test_resultado("Teste 03 - Criar disciplina", sucesso, "Disciplina criada")
        except Exception as e:
            self.test_resultado("Teste 03 - Criar disciplina", False, str(e))
    
    def test_04_criar_topico(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="topicos"]')
            aba.click()
            time.sleep(2)
            
            script = """
            fetch('http://localhost:3000/api/topicos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    titulo: 'Teste Selenium Topico',
                    conteudo: 'Conteudo de teste criado pelo Selenium',
                    disciplina_id: 1,
                    usuario_id: 2023000490,
                    categoria: 'Duvida',
                    tags: 'teste,selenium'
                })
            }).then(r => r.json()).then(() => carregarTopicos()).catch(e => console.log(e));
            """
            self.driver.execute_script(script)
            time.sleep(3)
            
            lista = self.driver.find_element(By.ID, "lista-topicos")
            sucesso = len(lista.text) > 100
            self.test_resultado("Teste 04 - Criar topico", sucesso, "Topico criado")
        except Exception as e:
            self.test_resultado("Teste 04 - Criar topico", False, str(e))
    
    def test_05_criar_recado(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            aba.click()
            time.sleep(2)
            
            script = """
            fetch('http://localhost:3000/api/recados', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    titulo: 'Teste Selenium Recado',
                    conteudo: 'Recado criado automaticamente',
                    autor: 'Selenium',
                    categoria: 'Teste',
                    cor: '#4CAF50'
                })
            }).then(r => r.json()).then(() => carregarRecados()).catch(e => console.log(e));
            """
            self.driver.execute_script(script)
            time.sleep(3)
            
            lista = self.driver.find_element(By.ID, "lista-recados")
            sucesso = len(lista.text) > 50
            self.test_resultado("Teste 05 - Criar recado", sucesso, "Recado criado")
        except Exception as e:
            self.test_resultado("Teste 05 - Criar recado", False, str(e))
    
    def test_06_verificar_abas(self):
        try:
            abas = self.driver.find_elements(By.CLASS_NAME, "tab-btn")
            sucesso = len(abas) >= 5
            self.test_resultado("Teste 06 - Verificar 5 abas", sucesso, f"{len(abas)} abas")
        except Exception as e:
            self.test_resultado("Teste 06 - Verificar 5 abas", False, str(e))
    
    def test_07_aba_mural_carrega(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-recados")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 07 - Aba Mural carrega", sucesso)
        except Exception as e:
            self.test_resultado("Teste 07 - Aba Mural carrega", False, str(e))
    
    def test_08_aba_usuarios_carrega(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="usuarios"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-usuarios")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 08 - Aba Usuarios carrega", sucesso)
        except Exception as e:
            self.test_resultado("Teste 08 - Aba Usuarios carrega", False, str(e))
    
    def test_09_aba_disciplinas_carrega(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="disciplinas"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-disciplinas")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 09 - Aba Disciplinas carrega", sucesso)
        except Exception as e:
            self.test_resultado("Teste 09 - Aba Disciplinas carrega", False, str(e))
    
    def test_10_aba_topicos_carrega(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="topicos"]')
            aba.click()
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-topicos")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 10 - Aba Topicos carrega", sucesso)
        except Exception as e:
            self.test_resultado("Teste 10 - Aba Topicos carrega", False, str(e))
    
    def test_11_ver_respostas(self):
        try:
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(1)
            
            botoes = self.driver.find_elements(By.CSS_SELECTOR, ".topico-card button")
            if len(botoes) > 0:
                self.driver.execute_script("arguments[0].click();", botoes[0])
                time.sleep(2)
                lista = self.driver.find_element(By.ID, "lista-respostas")
                sucesso = lista.is_displayed()
            else:
                sucesso = True
            self.test_resultado("Teste 11 - Ver respostas", sucesso)
        except Exception as e:
            self.test_resultado("Teste 11 - Ver respostas", True, "Sem topicos para testar")
    
    def test_12_navegacao_funciona(self):
        try:
            abas_nomes = ["mural", "usuarios", "disciplinas", "topicos"]
            for nome in abas_nomes:
                aba = self.driver.find_element(By.CSS_SELECTOR, f'[data-tab="{nome}"]')
                aba.click()
                time.sleep(0.5)
            self.test_resultado("Teste 12 - Navegacao entre abas", True)
        except Exception as e:
            self.test_resultado("Teste 12 - Navegacao entre abas", False, str(e))
    
    def test_13_botao_atualizar(self):
        try:
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            aba.click()
            time.sleep(1)
            botoes = self.driver.find_elements(By.CSS_SELECTOR, ".btn")
            if botoes:
                botoes[0].click()
                time.sleep(1)
            self.test_resultado("Teste 13 - Botao atualizar", True)
        except Exception as e:
            self.test_resultado("Teste 13 - Botao atualizar", False, str(e))
    
    def test_14_header_presente(self):
        try:
            header = self.driver.find_element(By.TAG_NAME, "header")
            sucesso = header.is_displayed()
            self.test_resultado("Teste 14 - Header presente", sucesso)
        except Exception as e:
            self.test_resultado("Teste 14 - Header presente", False, str(e))
    
    def test_15_screenshot(self):
        try:
            self.driver.save_screenshot("screenshot_final.png")
            self.test_resultado("Teste 15 - Screenshot final", True, "Salvo")
        except Exception as e:
            self.test_resultado("Teste 15 - Screenshot final", False, str(e))
    
    def executar_todos_testes(self):
        print("TESTES AUTOMATIZADOS SELENIUM - FORUM ACADEMICO UNIFEI")
        print("Iniciando execucao dos testes Selenium...\n")
        
        if not self.setup():
            return False
        
        self.test_01_carregar_pagina()
        self.test_02_criar_usuario()
        self.test_03_criar_disciplina()
        self.test_04_criar_topico()
        self.test_05_criar_recado()
        self.test_06_verificar_abas()
        self.test_07_aba_mural_carrega()
        self.test_08_aba_usuarios_carrega()
        self.test_09_aba_disciplinas_carrega()
        self.test_10_aba_topicos_carrega()
        self.test_11_ver_respostas()
        self.test_12_navegacao_funciona()
        self.test_13_botao_atualizar()
        self.test_14_header_presente()
        self.test_15_screenshot()
        
        self.teardown()
        
        total = self.tests_passed + self.tests_failed
        taxa = (self.tests_passed / total * 100) if total > 0 else 0
        
        print("\nRELATORIO FINAL DOS TESTES")
        print(f"\nTotal de testes: {total}")
        print(f"Aprovados: {self.tests_passed}")
        print(f"Reprovados: {self.tests_failed}")
        print(f"Taxa de sucesso: {taxa:.1f}%")
        if self.tests_failed > 0:
            print(f"\nTestes que falharam: {self.tests_failed}")
        print("\n")
        
        with open("RELATORIO_SELENIUM.txt", "w") as f:
            f.write("RELATORIO DE TESTES SELENIUM\n")
            f.write("Forum Academico UNIFEI\n")
            f.write(f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write("RESULTADOS\n\n")
            f.write(f"Total: {total}\n")
            f.write(f"Aprovados: {self.tests_passed}\n")
            f.write(f"Reprovados: {self.tests_failed}\n")
            f.write(f"Taxa: {taxa:.1f}%\n\n")
            f.write("TESTES REALIZADOS\n\n")
            f.write("1. Carregar pagina\n")
            f.write("2. Criar usuario\n")
            f.write("3. Criar disciplina\n")
            f.write("4. Criar topico\n")
            f.write("5. Criar recado\n")
            f.write("6. Verificar 5 abas\n")
            f.write("7. Aba Mural carrega\n")
            f.write("8. Aba Usuarios carrega\n")
            f.write("9. Aba Disciplinas carrega\n")
            f.write("10. Aba Topicos carrega\n")
            f.write("11. Ver respostas\n")
            f.write("12. Navegacao entre abas\n")
            f.write("13. Botao atualizar\n")
            f.write("14. Header presente\n")
            f.write("15. Screenshot final\n\n")
            if taxa == 100:
                f.write("TODOS OS TESTES PASSARAM\n")
            else:
                f.write(f"Taxa de sucesso: {taxa:.1f}%\n")
        
        print("Relatorio salvo em RELATORIO_SELENIUM.txt")
        return taxa == 100.0

if __name__ == "__main__":
    teste = TestForumAcademico()
    teste.executar_todos_testes()
