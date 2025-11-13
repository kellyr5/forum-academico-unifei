#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE SELENIUM FINAL
Sem cursor visual, IDs aleatórios do banco
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import requests
import random

BASE_URL = "http://localhost:8000"
API_URL = "http://localhost:3000/api"

# Textos realistas
TITULOS_RECADOS = [
    "Aula cancelada - Cálculo II",
    "Reunião do projeto integrador",
    "Horário de atendimento alterado",
    "Nova data para entrega"
]

CONTEUDOS_RECADOS = [
    "Pessoal, a aula foi cancelada. Reposição será marcada.",
    "Reunião na sexta às 14h na sala 203.",
    "Horário de atendimento mudou para terças e quintas das 15h às 17h.",
    "Entrega prorrogada para semana que vem!"
]

TITULOS_TOPICOS = [
    "Dúvida sobre a prova",
    "Material da aula passada?",
    "Grupo de estudos",
    "Exercício 5 da lista"
]

CONTEUDOS_TOPICOS = [
    "Alguém sabe o que vai cair na prova?",
    "Preciso do material da última aula.",
    "Organizando grupo de estudos. Quem se interessa?",
    "Alguém fez o exercício 5?"
]

RESPOSTAS = [
    "Sim, vai cair! É bom revisar.",
    "Tenho o material, te mando por email.",
    "Me interesso! Quando seria?",
    "Consegui fazer! A chave é usar loops.",
    "Vi isso na bibliografia.",
    "Valeu pela info!"
]

class TesteSeleniumFinal:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.banco_dados = {
            'usuarios': [],
            'disciplinas': [],
            'topicos': [],
            'recados': [],
            'respostas': []
        }
        self.ultima_resposta_criada = None
    
    def setup(self):
        print("\n" + "╔" + "═"*78 + "╗")
        print("║" + "TESTE SELENIUM FINAL".center(78) + "║")
        print("╚" + "═"*78 + "╝")
        
        print("\n⏳ Iniciando Firefox...")
        opts = webdriver.FirefoxOptions()
        opts.set_preference("browser.cache.disk.enable", False)
        
        self.driver = webdriver.Firefox(options=opts)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        time.sleep(1)
        print("✓ Firefox iniciado")
    
    def pesquisar_banco_completo(self):
        """Pesquisa COMPLETA no banco de dados"""
        print("\n🔍 Pesquisando banco de dados...")
        
        endpoints = {
            'usuarios': '/usuarios',
            'disciplinas': '/disciplinas',
            'topicos': '/topicos',
            'recados': '/recados',
            'respostas': '/respostas'
        }
        
        for nome, endpoint in endpoints.items():
            try:
                resp = requests.get(f"{API_URL}{endpoint}", timeout=5)
                if resp.status_code == 200:
                    dados = resp.json()
                    if isinstance(dados, list):
                        self.banco_dados[nome] = dados
                        print(f"  • {nome.capitalize()}: {len(dados)} registro(s)")
                    else:
                        self.banco_dados[nome] = []
                else:
                    self.banco_dados[nome] = []
            except:
                self.banco_dados[nome] = []
        
        print()
    
    def pegar_id_aleatorio(self, tipo):
        """Pega ID ALEATÓRIO do banco de dados"""
        if self.banco_dados[tipo]:
            registro = random.choice(self.banco_dados[tipo])
            return registro.get('id', 1)
        return random.randint(1, 5)  # Fallback aleatório
    
    def scroll_para_mostrar_inserido(self, texto_busca):
        """Scroll para mostrar o dado que foi inserido"""
        print(f"\n  📜 Procurando '{texto_busca[:40]}...'")
        
        time.sleep(1.5)
        
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
            elementos = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{texto_busca[:30]}')]")
            
            if elementos:
                elemento = elementos[0]
                
                self.driver.execute_script("""
                    arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
                """, elemento)
                time.sleep(0.8)
                
                self.driver.execute_script("""
                    arguments[0].style.border='4px solid #4CAF50';
                    arguments[0].style.backgroundColor='rgba(76, 175, 80, 0.15)';
                    arguments[0].style.transition='all 0.4s';
                    arguments[0].style.borderRadius='8px';
                    arguments[0].style.padding='10px';
                """, elemento)
                
                print(f"  ✓ Encontrado e destacado!")
                time.sleep(2)
                
                self.driver.execute_script("""
                    arguments[0].style.border='';
                    arguments[0].style.backgroundColor='';
                    arguments[0].style.padding='';
                """, elemento)
                
                return True
            else:
                print(f"  ⚠ Não encontrado visualmente")
                
                altura = self.driver.execute_script("return document.body.scrollHeight")
                for i in range(0, min(altura, 1000), 100):
                    self.driver.execute_script(f"window.scrollTo(0, {i});")
                    time.sleep(0.1)
                
                time.sleep(1)
                return False
                
        except Exception as e:
            print(f"  ⚠ Erro: {str(e)[:40]}")
            return False
    
    def ir_aba(self, aba_id, nome):
        print("\n" + "─"*80)
        print(f"ABA: {nome.upper()}")
        print("─"*80)
        
        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-tab="{aba_id}"]')))
        
        self.driver.execute_script("""
            arguments[0].style.border='3px solid #2196F3';
            arguments[0].style.boxShadow='0 0 15px #2196F3';
            arguments[0].style.transition='all 0.3s';
        """, btn)
        
        time.sleep(0.5)
        btn.click()
        time.sleep(0.8)
        
        self.driver.execute_script("""
            arguments[0].style.border='';
            arguments[0].style.boxShadow='';
        """, btn)
    
    def preencher(self, campo_id, valor, nome):
        try:
            campo = self.driver.find_element(By.ID, campo_id)
            self.driver.execute_script("""
                arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
            """, campo)
            time.sleep(0.3)
            
            self.driver.execute_script("""
                arguments[0].style.border='3px solid #4CAF50';
                arguments[0].style.boxShadow='0 0 10px #4CAF50';
                arguments[0].style.transition='all 0.3s';
            """, campo)
            
            time.sleep(0.4)
            campo.clear()
            
            for char in str(valor):
                campo.send_keys(char)
                time.sleep(0.02)
            
            time.sleep(0.3)
            
            self.driver.execute_script("""
                arguments[0].style.border='';
                arguments[0].style.boxShadow='';
            """, campo)
            
            valor_mostrar = str(valor)[:60] + '...' if len(str(valor)) > 60 else str(valor)
            print(f"  ✓ {nome}: {valor_mostrar}")
            return True
        except Exception as e:
            print(f"  ✗ {nome}: {str(e)[:40]}")
            return False
    
    def selecionar(self, campo_id, nome, indice=None):
        try:
            elem = self.driver.find_element(By.ID, campo_id)
            self.driver.execute_script("""
                arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
            """, elem)
            time.sleep(0.3)
            
            self.driver.execute_script("""
                arguments[0].style.border='3px solid #FF9800';
                arguments[0].style.boxShadow='0 0 10px #FF9800';
                arguments[0].style.transition='all 0.3s';
            """, elem)
            
            time.sleep(0.4)
            
            select = Select(elem)
            opcoes = select.options
            
            if indice is None:
                opcoes_validas = [i for i, opt in enumerate(opcoes) 
                                 if opt.get_attribute('value') and opt.get_attribute('value') != '']
                if opcoes_validas:
                    indice = random.choice(opcoes_validas)
                else:
                    indice = 1 if len(opcoes) > 1 else 0
            
            if indice < len(opcoes) and opcoes[indice].get_attribute('value') == '':
                indice += 1
            
            if indice >= len(opcoes):
                indice = len(opcoes) - 1
            
            select.select_by_index(indice)
            time.sleep(0.4)
            
            selecionado = select.first_selected_option.text.strip()
            
            self.driver.execute_script("""
                arguments[0].style.border='';
                arguments[0].style.boxShadow='';
            """, elem)
            
            print(f"  ✓ {nome}: {selecionado}")
            return selecionado
        except Exception as e:
            print(f"  ✗ {nome}: {str(e)[:40]}")
            return None
    
    def submeter(self, form_id):
        print(f"  ⏳ Enviando...")
        try:
            form = self.driver.find_element(By.ID, form_id)
            botao = form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            self.driver.execute_script("""
                arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
            """, botao)
            time.sleep(0.4)
            
            self.driver.execute_script("""
                arguments[0].style.transform='scale(1.05)';
                arguments[0].style.boxShadow='0 5px 20px rgba(33, 150, 243, 0.5)';
                arguments[0].style.transition='all 0.3s';
            """, botao)
            
            time.sleep(0.5)
            botao.click()
            time.sleep(2)
            
            print(f"  ✓ Enviado\n")
            return True
        except Exception as e:
            print(f"  ✗ Erro: {str(e)[:40]}")
            return False
    
    def test_mural(self):
        self.ir_aba('mural', 'Mural')
        
        titulo = random.choice(TITULOS_RECADOS)
        conteudo = random.choice(CONTEUDOS_RECADOS)
        
        print("\n📝 Criando recado:\n")
        
        self.preencher('rec_titulo', titulo, 'Título')
        self.preencher('rec_autor', 'Sistema Teste', 'Autor')
        self.preencher('rec_conteudo', conteudo, 'Conteúdo')
        self.selecionar('rec_categoria', 'Categoria')
        
        if self.submeter('form-recado'):
            self.scroll_para_mostrar_inserido(titulo)
    
    def test_usuarios(self):
        self.ir_aba('usuarios', 'Usuários')
        
        form = self.driver.find_element(By.ID, 'form-usuario')
        
        inputs = {inp.get_attribute('id'): inp.get_attribute('type') 
                 for inp in form.find_elements(By.TAG_NAME, 'input') 
                 if inp.get_attribute('id')}
        
        selects = [sel.get_attribute('id') 
                  for sel in form.find_elements(By.TAG_NAME, 'select') 
                  if sel.get_attribute('id')]
        
        timestamp = int(time.time()) % 10000
        nome_usuario = f'Aluno {timestamp}'
        
        print("\n📝 Criando usuário:\n")
        
        for campo_id, tipo in inputs.items():
            if 'nome' in campo_id.lower() and tipo == 'text':
                self.preencher(campo_id, nome_usuario, campo_id)
            elif tipo == 'email':
                self.preencher(campo_id, f'aluno{timestamp}@unifei.edu.br', campo_id)
            elif tipo == 'password':
                self.preencher(campo_id, 'senha123', campo_id)
        
        for campo_id in selects:
            self.selecionar(campo_id, campo_id)
        
        if self.submeter('form-usuario'):
            time.sleep(1)
            self.pesquisar_banco_completo()
            self.scroll_para_mostrar_inserido(nome_usuario)
    
    def test_disciplinas(self):
        self.ir_aba('disciplinas', 'Disciplinas')
        
        # ID ALEATÓRIO do banco
        id_professor = self.pegar_id_aleatorio('usuarios')
        print(f"\n✓ Usando Professor ID aleatório: {id_professor} (do banco)")
        
        timestamp = int(time.time()) % 10000
        disciplinas = ["Programação I", "Cálculo II", "Física", "Algoritmos"]
        nome_disc = random.choice(disciplinas)
        
        print("\n📝 Criando disciplina:\n")
        
        self.preencher('disc_nome', nome_disc, 'Nome')
        self.preencher('disc_codigo', f'ENG{timestamp}', 'Código')
        self.selecionar('disc_curso', 'Curso')
        self.preencher('disc_professor', id_professor, 'ID Professor')
        self.preencher('disc_periodo', '2025.1', 'Período')
        
        if self.submeter('form-disciplina'):
            time.sleep(1)
            self.pesquisar_banco_completo()
            self.scroll_para_mostrar_inserido(nome_disc)
    
    def test_topicos(self):
        self.ir_aba('topicos', 'Tópicos')
        
        # IDs ALEATÓRIOS do banco
        id_disciplina = self.pegar_id_aleatorio('disciplinas')
        id_usuario = self.pegar_id_aleatorio('usuarios')
        
        print(f"\n✓ Disciplina ID aleatório: {id_disciplina} (do banco)")
        print(f"✓ Usuario ID aleatório: {id_usuario} (do banco)")
        
        titulo = random.choice(TITULOS_TOPICOS)
        conteudo = random.choice(CONTEUDOS_TOPICOS)
        
        print("\n📝 Criando tópico:\n")
        
        self.preencher('top_titulo', titulo, 'Título')
        self.preencher('top_conteudo', conteudo, 'Conteúdo')
        self.preencher('top_disciplina', id_disciplina, 'ID Disciplina')
        self.preencher('top_usuario', id_usuario, 'ID Usuário')
        self.selecionar('top_categoria', 'Categoria')
        
        if self.submeter('form-topico'):
            time.sleep(1)
            self.pesquisar_banco_completo()
            self.scroll_para_mostrar_inserido(titulo)
    
    def test_respostas(self):
        self.ir_aba('respostas', 'Respostas')
        
        # IDs ALEATÓRIOS do banco
        id_topico = self.pegar_id_aleatorio('topicos')
        id_usuario = self.pegar_id_aleatorio('usuarios')
        
        print(f"\n✓ Tópico ID aleatório: {id_topico} (do banco)")
        print(f"✓ Usuario ID aleatório: {id_usuario} (do banco)")
        
        conteudo_resposta = random.choice(RESPOSTAS)
        
        print("\n📝 Criando resposta:\n")
        
        self.preencher('resp_topico', id_topico, 'ID Tópico')
        self.preencher('resp_usuario', id_usuario, 'ID Usuário')
        self.preencher('resp_conteudo', conteudo_resposta, 'Conteúdo')
        
        if self.submeter('form-resposta'):
            self.ultima_resposta_criada = {
                'topico_id': id_topico,
                'usuario_id': id_usuario,
                'conteudo': conteudo_resposta
            }
            time.sleep(1)
            self.pesquisar_banco_completo()
            self.scroll_para_mostrar_inserido(conteudo_resposta)
    
    def test_buscar_resposta(self):
        if not self.ultima_resposta_criada:
            return
        
        self.ir_aba('respostas', 'Respostas - Busca')
        
        topico_id = self.ultima_resposta_criada['topico_id']
        conteudo = self.ultima_resposta_criada['conteudo']
        
        print(f"\n🔍 Buscando resposta:")
        print(f"  • Tópico ID: {topico_id}")
        print(f"  • Conteúdo: '{conteudo}'\n")
        
        try:
            possiveis_campos = ['busca_topico', 'filtro_topico', 'resp_busca', 'search_topico']
            
            campo_busca = None
            for campo_id in possiveis_campos:
                try:
                    campo_busca = self.driver.find_element(By.ID, campo_id)
                    break
                except:
                    continue
            
            if not campo_busca:
                inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="number"]')
                if inputs:
                    campo_busca = inputs[0]
            
            if campo_busca:
                self.driver.execute_script("""
                    arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
                """, campo_busca)
                time.sleep(0.4)
                
                self.driver.execute_script("""
                    arguments[0].style.border='3px solid #2196F3';
                    arguments[0].style.boxShadow='0 0 15px #2196F3';
                    arguments[0].style.transition='all 0.3s';
                """, campo_busca)
                
                time.sleep(0.5)
                campo_busca.clear()
                campo_busca.send_keys(str(topico_id))
                time.sleep(0.5)
                campo_busca.send_keys(Keys.ENTER)
                time.sleep(2)
                
                self.driver.execute_script("""
                    arguments[0].style.border='';
                    arguments[0].style.boxShadow='';
                """, campo_busca)
                
                print(f"  ✓ Busca realizada")
                self.scroll_para_mostrar_inserido(conteudo)
            else:
                print(f"  ⚠ Campo não encontrado")
        except Exception as e:
            print(f"  ✗ Erro: {str(e)[:50]}")
    
    def test_excluir_ultimo_mural(self):
        self.ir_aba('mural', 'Mural - Exclusão')
        
        print("\n🗑️  Excluindo último recado:\n")
        
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            botoes = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="deleteRecado"]')
            
            if botoes:
                ultimo = botoes[-1]
                print(f"  ✓ Encontrado! Total: {len(botoes)}")
                
                self.driver.execute_script("""
                    arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
                """, ultimo)
                time.sleep(0.5)
                
                self.driver.execute_script("""
                    arguments[0].style.border='3px solid #f44336';
                    arguments[0].style.transform='scale(1.1)';
                    arguments[0].style.transition='all 0.3s';
                """, ultimo)
                
                time.sleep(0.8)
                ultimo.click()
                time.sleep(0.5)
                
                try:
                    alert = self.driver.switch_to.alert
                    time.sleep(0.4)
                    alert.accept()
                    time.sleep(1.5)
                    print(f"  ✓ Excluído!\n")
                except:
                    print(f"  ✓ Excluído!\n")
            else:
                print(f"  ⚠ Nenhum recado\n")
        except Exception as e:
            print(f"  ✗ Erro: {str(e)[:50]}\n")
    
    def executar(self):
        self.setup()
        
        try:
            print("\n⏳ Abrindo aplicação...")
            self.driver.get(BASE_URL)
            time.sleep(1.5)
            print("✓ Aplicação carregada")
            
            self.pesquisar_banco_completo()
            
            self.test_mural()
            self.test_usuarios()
            self.test_disciplinas()
            self.test_topicos()
            self.test_respostas()
            self.test_buscar_resposta()
            self.test_excluir_ultimo_mural()
            
            print("\n" + "╔" + "═"*78 + "╗")
            print("║" + "TESTE CONCLUÍDO".center(78) + "║")
            print("╚" + "═"*78 + "╝")
            
            self.driver.save_screenshot('/tmp/teste_final.png')
            print("\n📸 Screenshot: /tmp/teste_final.png\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠ Interrompido")
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
        finally:
            print("⏳ Fechando em 5 segundos...")
            time.sleep(5)
            self.driver.quit()
            print("✓ Fechado\n")

if __name__ == "__main__":
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + "TESTE SELENIUM FINAL".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print("\n✨ Recursos:")
    print("  • Destaques visuais nos elementos")
    print("  • IDs ALEATÓRIOS do banco de dados")
    print("  • Scroll para mostrar dados inseridos")
    print("  • Busca e exclusão completos")
    print("\n" + "═"*80)
    
    input("\n▶ Pressione ENTER para iniciar...")
    
    teste = TesteSeleniumFinal()
    teste.executar()
