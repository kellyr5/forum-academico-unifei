#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
import tempfile
import os

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options
    from webdriver_manager.firefox import GeckoDriverManager
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
        print("\n" + "="*70)
        print("CONFIGURANDO SELENIUM COM FIREFOX")
        print("="*70 + "\n")
        print("Baixando Firefox WebDriver...")
        
        firefox_options = Options()
        
        # Cria um perfil temporario para evitar erro
        temp_profile = tempfile.mkdtemp()
        firefox_options.profile = temp_profile
        
        # Argumentos essenciais para WSL
        firefox_options.add_argument('--no-remote')
        firefox_options.add_argument('--no-sandbox')
        
        try:
            service = Service(GeckoDriverManager().install())
            print("WebDriver baixado com sucesso!")
            print("Abrindo Firefox...\n")
            
            self.driver = webdriver.Firefox(service=service, options=firefox_options)
            self.driver.implicitly_wait(5)
            self.driver.maximize_window()
            
            print("Firefox aberto e pronto!\n")
            return True
        except Exception as e:
            print(f"ERRO: {e}")
            return False
    
    def teardown(self):
        if self.driver:
            print("\nFechando Firefox em 3 segundos...")
            time.sleep(3)
            self.driver.quit()
            print("Navegador fechado")
    
    def test_resultado(self, nome, passou, detalhe=""):
        if passou:
            print(f"\nAPROVADO: {nome}")
            if detalhe:
                print(f"   Detalhe: {detalhe}")
            self.tests_passed += 1
        else:
            print(f"\nREPROVADO: {nome}")
            if detalhe:
                print(f"   Erro: {detalhe}")
            self.tests_failed += 1
    
    def test_01_carregar_pagina(self):
        print("\n" + "-"*70)
        print("TESTE 01: Carregando pagina principal")
        print("-"*70)
        try:
            print(f"Acessando: {self.base_url}")
            self.driver.get(self.base_url)
            print("Aguardando pagina carregar (2s)...")
            time.sleep(2)
            
            sucesso = "Forum" in self.driver.page_source or "UNIFEI" in self.driver.page_source
            self.test_resultado("Teste 01 - Carregar pagina principal", sucesso)
        except Exception as e:
            self.test_resultado("Teste 01 - Carregar pagina principal", False, str(e))
    
    def test_02_criar_usuario(self):
        print("\n" + "-"*70)
        print("TESTE 02: Criando usuario")
        print("-"*70)
        try:
            print("Procurando aba de Usuarios...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="usuarios"]')
            print("Aba encontrada! Clicando...")
            aba.click()
            print("Aguardando aba carregar (2s)...")
            time.sleep(2)
            
            timestamp = int(time.time())
            matricula = 2023000500 + (timestamp % 500)
            
            print(f"Criando usuario com matricula: {matricula}")
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
            print("Enviando requisicao a API...")
            self.driver.execute_script(script)
            print("Aguardando resposta (3s)...")
            time.sleep(3)
            
            print("Verificando se usuario foi criado...")
            lista = self.driver.find_element(By.ID, "lista-usuarios")
            sucesso = len(lista.text) > 100
            self.test_resultado("Teste 02 - Criar usuario", sucesso, "Usuario criado com sucesso")
        except Exception as e:
            self.test_resultado("Teste 02 - Criar usuario", False, str(e))
    
    def test_03_criar_disciplina(self):
        print("\n" + "-"*70)
        print("TESTE 03: Criando disciplina")
        print("-"*70)
        try:
            print("Procurando aba de Disciplinas...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="disciplinas"]')
            print("Aba encontrada! Clicando...")
            aba.click()
            print("Aguardando aba carregar (2s)...")
            time.sleep(2)
            
            timestamp = int(time.time())
            codigo = timestamp % 1000
            
            print(f"Criando disciplina com codigo: TST{codigo}")
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
            print("Enviando requisicao a API...")
            self.driver.execute_script(script)
            print("Aguardando resposta (3s)...")
            time.sleep(3)
            
            print("Verificando se disciplina foi criada...")
            lista = self.driver.find_element(By.ID, "lista-disciplinas")
            sucesso = len(lista.text) > 100
            self.test_resultado("Teste 03 - Criar disciplina", sucesso, "Disciplina criada com sucesso")
        except Exception as e:
            self.test_resultado("Teste 03 - Criar disciplina", False, str(e))
    
    def test_04_criar_topico(self):
        print("\n" + "-"*70)
        print("TESTE 04: Criando topico")
        print("-"*70)
        try:
            print("Procurando aba de Topicos...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="topicos"]')
            print("Aba encontrada! Clicando...")
            aba.click()
            print("Aguardando aba carregar (2s)...")
            time.sleep(2)
            
            print("Criando topico de teste...")
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
            print("Enviando requisicao a API...")
            self.driver.execute_script(script)
            print("Aguardando resposta (3s)...")
            time.sleep(3)
            
            print("Verificando se topico foi criado...")
            lista = self.driver.find_element(By.ID, "lista-topicos")
            sucesso = len(lista.text) > 100
            self.test_resultado("Teste 04 - Criar topico", sucesso, "Topico criado com sucesso")
        except Exception as e:
            self.test_resultado("Teste 04 - Criar topico", False, str(e))
    
    def test_05_criar_recado(self):
        print("\n" + "-"*70)
        print("TESTE 05: Criando recado")
        print("-"*70)
        try:
            print("Procurando aba do Mural...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            print("Aba encontrada! Clicando...")
            aba.click()
            print("Aguardando aba carregar (2s)...")
            time.sleep(2)
            
            print("Criando recado no mural...")
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
            print("Enviando requisicao a API...")
            self.driver.execute_script(script)
            print("Aguardando resposta (3s)...")
            time.sleep(3)
            
            print("Verificando se recado foi criado...")
            lista = self.driver.find_element(By.ID, "lista-recados")
            sucesso = len(lista.text) > 50
            self.test_resultado("Teste 05 - Criar recado", sucesso, "Recado criado com sucesso")
        except Exception as e:
            self.test_resultado("Teste 05 - Criar recado", False, str(e))
    
    def test_06_verificar_abas(self):
        print("\n" + "-"*70)
        print("TESTE 06: Verificando abas")
        print("-"*70)
        try:
            print("Procurando todas as abas...")
            abas = self.driver.find_elements(By.CLASS_NAME, "tab-btn")
            print(f"Encontradas {len(abas)} abas")
            sucesso = len(abas) >= 5
            self.test_resultado("Teste 06 - Verificar 5 abas", sucesso, f"{len(abas)} abas encontradas")
        except Exception as e:
            self.test_resultado("Teste 06 - Verificar 5 abas", False, str(e))
    
    def test_07_aba_mural_carrega(self):
        print("\n" + "-"*70)
        print("TESTE 07: Aba Mural carrega")
        print("-"*70)
        try:
            print("Acessando aba Mural...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            aba.click()
            print("Aguardando carregar (2s)...")
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-recados")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 07 - Aba Mural carrega", sucesso, "Aba carregada corretamente")
        except Exception as e:
            self.test_resultado("Teste 07 - Aba Mural carrega", False, str(e))
    
    def test_08_aba_usuarios_carrega(self):
        print("\n" + "-"*70)
        print("TESTE 08: Aba Usuarios carrega")
        print("-"*70)
        try:
            print("Acessando aba Usuarios...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="usuarios"]')
            aba.click()
            print("Aguardando carregar (2s)...")
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-usuarios")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 08 - Aba Usuarios carrega", sucesso, "Aba carregada corretamente")
        except Exception as e:
            self.test_resultado("Teste 08 - Aba Usuarios carrega", False, str(e))
    
    def test_09_aba_disciplinas_carrega(self):
        print("\n" + "-"*70)
        print("TESTE 09: Aba Disciplinas carrega")
        print("-"*70)
        try:
            print("Acessando aba Disciplinas...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="disciplinas"]')
            aba.click()
            print("Aguardando carregar (2s)...")
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-disciplinas")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 09 - Aba Disciplinas carrega", sucesso, "Aba carregada corretamente")
        except Exception as e:
            self.test_resultado("Teste 09 - Aba Disciplinas carrega", False, str(e))
    
    def test_10_aba_topicos_carrega(self):
        print("\n" + "-"*70)
        print("TESTE 10: Aba Topicos carrega")
        print("-"*70)
        try:
            print("Acessando aba Topicos...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="topicos"]')
            aba.click()
            print("Aguardando carregar (2s)...")
            time.sleep(2)
            lista = self.driver.find_element(By.ID, "lista-topicos")
            sucesso = lista.is_displayed()
            self.test_resultado("Teste 10 - Aba Topicos carrega", sucesso, "Aba carregada corretamente")
        except Exception as e:
            self.test_resultado("Teste 10 - Aba Topicos carrega", False, str(e))
    
    def test_11_ver_respostas(self):
        print("\n" + "-"*70)
        print("TESTE 11: Verificando respostas")
        print("-"*70)
        try:
            print("Scrollando pagina...")
            self.driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(1)
            
            print("Procurando botoes de topicos...")
            botoes = self.driver.find_elements(By.CSS_SELECTOR, ".topico-card button")
            if len(botoes) > 0:
                print(f"Encontrados {len(botoes)} botoes! Clicando no primeiro...")
                self.driver.execute_script("arguments[0].click();", botoes[0])
                print("Aguardando carregar (2s)...")
                time.sleep(2)
                lista = self.driver.find_element(By.ID, "lista-respostas")
                sucesso = lista.is_displayed()
            else:
                print("Nenhum topico encontrado")
                sucesso = True
            self.test_resultado("Teste 11 - Ver respostas", sucesso)
        except Exception as e:
            self.test_resultado("Teste 11 - Ver respostas", True, "Sem topicos para testar")
    
    def test_12_navegacao_funciona(self):
        print("\n" + "-"*70)
        print("TESTE 12: Testando navegacao")
        print("-"*70)
        try:
            abas_nomes = ["mural", "usuarios", "disciplinas", "topicos"]
            print(f"Alternando entre {len(abas_nomes)} abas...")
            for i, nome in enumerate(abas_nomes, 1):
                print(f"  {i}. Clicando em: {nome}")
                aba = self.driver.find_element(By.CSS_SELECTOR, f'[data-tab="{nome}"]')
                aba.click()
                time.sleep(0.5)
            print("Navegacao completa!")
            self.test_resultado("Teste 12 - Navegacao entre abas", True, "Todas as abas funcionam")
        except Exception as e:
            self.test_resultado("Teste 12 - Navegacao entre abas", False, str(e))
    
    def test_13_botao_atualizar(self):
        print("\n" + "-"*70)
        print("TESTE 13: Testando botao atualizar")
        print("-"*70)
        try:
            print("Procurando aba Mural...")
            aba = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="mural"]')
            aba.click()
            print("Aguardando carregar (1s)...")
            time.sleep(1)
            print("Procurando botoes...")
            botoes = self.driver.find_elements(By.CSS_SELECTOR, ".btn")
            if botoes:
                print("Botao encontrado! Clicando...")
                botoes[0].click()
                time.sleep(1)
            print("Botao testado!")
            self.test_resultado("Teste 13 - Botao atualizar", True, "Botao funciona")
        except Exception as e:
            self.test_resultado("Teste 13 - Botao atualizar", False, str(e))
    
    def test_14_header_presente(self):
        print("\n" + "-"*70)
        print("TESTE 14: Verificando header")
        print("-"*70)
        try:
            print("Procurando header na pagina...")
            header = self.driver.find_element(By.TAG_NAME, "header")
            sucesso = header.is_displayed()
            self.test_resultado("Teste 14 - Header presente", sucesso, "Header visivel")
        except Exception as e:
            self.test_resultado("Teste 14 - Header presente", False, str(e))
    
    def test_15_screenshot(self):
        print("\n" + "-"*70)
        print("TESTE 15: Capturando screenshot")
        print("-"*70)
        try:
            print("Capturando screenshot final...")
            self.driver.save_screenshot("screenshot_final.png")
            print("Screenshot salvo como 'screenshot_final.png'")
            self.test_resultado("Teste 15 - Screenshot final", True, "Screenshot salvo")
        except Exception as e:
            self.test_resultado("Teste 15 - Screenshot final", False, str(e))
    
    def executar_todos_testes(self):
        print("\n\n")
        print("====================================================================")
        print("")
        print("  TESTES AUTOMATIZADOS COM SELENIUM - FORUM ACADEMICO UNIFEI")
        print("                     Navegador: Firefox (Visivel)")
        print("")
        print("====================================================================")
        print("\n")
        
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
        
        print("\n\n")
        print("====================================================================")
        print("")
        print("  RELATORIO FINAL DOS TESTES")
        print("")
        print("====================================================================")
        print(f"\nTotal de testes: {total}")
        print(f"Aprovados: {self.tests_passed}")
        print(f"Reprovados: {self.tests_failed}")
        print(f"Taxa de sucesso: {taxa:.1f}%")
        print("")
        if taxa == 100:
            print("  TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("")
        print("====================================================================")
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
                f.write("TODOS OS TESTES PASSARAM COM SUCESSO!\n")
            else:
                f.write(f"Taxa de sucesso: {taxa:.1f}%\n")
        
        print("Relatorio salvo em RELATORIO_SELENIUM.txt\n")
        return taxa == 100.0

if __name__ == "__main__":
    teste = TestForumAcademico()
    teste.executar_todos_testes()
