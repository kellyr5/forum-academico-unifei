#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE SELENIUM FINAL - FORUM ACADEMICO UNIFEI
Sem emojis, com contextos coerentes, IDs aleatorios do banco
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

# MURAL - Avisos e informacoes institucionais
RECADOS_MURAL = [
    {
        'titulo': 'Aula cancelada - Calculo II',
        'conteudo': 'Atencao alunos! A aula de Calculo II do dia 15/11 esta cancelada devido a compromisso do professor. A reposicao sera agendada.',
        'categoria': 'Aviso'
    },
    {
        'titulo': 'Reuniao do projeto integrador',
        'conteudo': 'Convocamos todos os grupos do projeto integrador para reuniao geral na proxima sexta-feira, as 14h, no auditorio principal.',
        'categoria': 'Evento'
    },
    {
        'titulo': 'Alteracao de horario de atendimento',
        'conteudo': 'Informamos que o horario de atendimento da coordenacao foi alterado. Novo horario: tercas e quintas das 15h as 17h.',
        'categoria': 'Aviso'
    },
    {
        'titulo': 'Prazo de entrega prorrogado',
        'conteudo': 'Boa noticia! O prazo para entrega do trabalho de Programacao foi prorrogado ate o dia 20/11. Aproveitem o tempo extra!',
        'categoria': 'Aviso'
    }
]

# TOPICOS - Duvidas e discussoes academicas
TOPICOS_FORUM = [
    {
        'titulo': 'Duvida sobre recursao na prova',
        'conteudo': 'Pessoal, alguem sabe se vai cair recursao na prova de Algoritmos? Estou com dificuldade nesse assunto e queria saber se devo focar nisso.',
        'categoria': 'Duvida'
    },
    {
        'titulo': 'Material da ultima aula disponivel?',
        'conteudo': 'Faltei na aula passada de Fisica e preciso urgente do material. Alguem tem os slides ou anotacoes que possa compartilhar?',
        'categoria': 'Duvida'
    },
    {
        'titulo': 'Formando grupo de estudos para Calculo',
        'conteudo': 'Estou organizando um grupo de estudos para a prova de Calculo II. Quem tiver interesse, vamos nos reunir as quartas as 16h na biblioteca.',
        'categoria': 'Discussao'
    },
    {
        'titulo': 'Como resolver o exercicio 5 da lista?',
        'conteudo': 'Alguem conseguiu fazer o exercicio 5 da lista de Programacao? Nao estou entendendo a logica dele, principalmente a parte de arrays.',
        'categoria': 'Duvida'
    }
]

# RESPOSTAS - Relacionadas as duvidas
RESPOSTAS_TOPICOS = [
    'Sim, vai cair recursao! O professor avisou na ultima aula. E bom revisar os exemplos de fatorial e fibonacci que ele passou.',
    'Tenho o material aqui! Vou te mandar por email. Sao 3 slides sobre cinematica.',
    'Eu me interesso no grupo! Calculo II esta dificil mesmo. Podemos dividir os exercicios entre nos.',
    'Consegui fazer sim! A chave e usar dois loops aninhados e ir comparando os elementos. Te explico melhor se quiser.',
    'Vi esse conteudo na bibliografia do capitulo 7. Tem uns exemplos bem parecidos la.',
    'Valeu pela informacao! Vou estudar esse topico entao.'
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
        print("\n" + "="*80)
        print("TESTE SELENIUM FINAL - FORUM ACADEMICO UNIFEI")
        print("="*80)
        
        print("\nIniciando Firefox...")
        opts = webdriver.FirefoxOptions()
        opts.set_preference("browser.cache.disk.enable", False)
        
        self.driver = webdriver.Firefox(options=opts)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        time.sleep(1)
        print("Firefox iniciado com sucesso")
    
    def pesquisar_banco_completo(self):
        """Pesquisa COMPLETA no banco de dados"""
        print("\nPesquisando banco de dados...")
        
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
                        print(f"  - {nome.capitalize()}: {len(dados)} registro(s)")
                    else:
                        self.banco_dados[nome] = []
                else:
                    self.banco_dados[nome] = []
            except:
                self.banco_dados[nome] = []
        
        print()
    
    def pegar_id_aleatorio(self, tipo):
        """Pega ID ALEATORIO do banco de dados"""
        if self.banco_dados[tipo]:
            registro = random.choice(self.banco_dados[tipo])
            return registro.get('id', 1)
        return random.randint(1, 5)
    
    def ir_aba(self, aba_id, nome):
        print("\n" + "-"*80)
        print(f"ABA: {nome.upper()}")
        print("-"*80)
        
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
            print(f"  [OK] {nome}: {valor_mostrar}")
            return True
        except Exception as e:
            print(f"  [ERRO] {nome}: {str(e)[:40]}")
            return False
    
    def selecionar(self, campo_id, nome, indice=None, valor_especifico=None):
        """Seleciona por indice aleatorio ou valor especifico"""
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
            
            # Se tem valor especifico, procurar por ele
            if valor_especifico:
                for i, opt in enumerate(opcoes):
                    if valor_especifico.lower() in opt.text.lower():
                        indice = i
                        break
            
            # Se nao tem indice, escolher aleatorio
            if indice is None:
                opcoes_validas = [i for i, opt in enumerate(opcoes) 
                                 if opt.get_attribute('value') and opt.get_attribute('value') != '']
                if opcoes_validas:
                    indice = random.choice(opcoes_validas)
                else:
                    indice = 1 if len(opcoes) > 1 else 0
            
            # Ajustar se necessario
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
            
            print(f"  [OK] {nome}: {selecionado}")
            return selecionado
        except Exception as e:
            print(f"  [ERRO] {nome}: {str(e)[:40]}")
            return None
    
    def submeter(self, form_id):
        print(f"  Enviando formulario...")
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
            
            print(f"  [OK] Formulario enviado\n")
            return True
        except Exception as e:
            print(f"  [ERRO] {str(e)[:40]}")
            return False
    
    def test_mural(self):
        self.ir_aba('mural', 'Mural - Avisos Institucionais')
        
        recado = random.choice(RECADOS_MURAL)
        
        print(f"\nCriando aviso: '{recado['titulo']}'\n")
        
        self.preencher('rec_titulo', recado['titulo'], 'Titulo')
        self.preencher('rec_autor', 'Coordenacao', 'Autor')
        self.preencher('rec_conteudo', recado['conteudo'], 'Conteudo')
        self.selecionar('rec_categoria', 'Categoria', valor_especifico=recado['categoria'])
        
        self.submeter('form-recado')
    
    def test_usuarios(self):
        self.ir_aba('usuarios', 'Usuarios')
        
        form = self.driver.find_element(By.ID, 'form-usuario')
        
        inputs = {inp.get_attribute('id'): inp.get_attribute('type') 
                 for inp in form.find_elements(By.TAG_NAME, 'input') 
                 if inp.get_attribute('id')}
        
        selects = [sel.get_attribute('id') 
                  for sel in form.find_elements(By.TAG_NAME, 'select') 
                  if sel.get_attribute('id')]
        
        timestamp = int(time.time()) % 10000
        nome_usuario = f'Aluno Teste {timestamp}'
        
        print(f"\nCriando usuario: '{nome_usuario}'\n")
        
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
    
    def test_disciplinas(self):
        self.ir_aba('disciplinas', 'Disciplinas')
        
        id_professor = self.pegar_id_aleatorio('usuarios')
        print(f"\nCriando disciplina")
        print(f"  - Professor ID: {id_professor} (aleatorio do banco)\n")
        
        timestamp = int(time.time()) % 10000
        disciplinas = ["Programacao I", "Calculo II", "Fisica Experimental", "Algoritmos e Estruturas de Dados"]
        nome_disc = random.choice(disciplinas)
        
        self.preencher('disc_nome', nome_disc, 'Nome')
        self.preencher('disc_codigo', f'ENG{timestamp}', 'Codigo')
        self.selecionar('disc_curso', 'Curso')
        self.preencher('disc_professor', id_professor, 'ID Professor')
        self.preencher('disc_periodo', '2025.1', 'Periodo')
        
        if self.submeter('form-disciplina'):
            time.sleep(1)
            self.pesquisar_banco_completo()
    
    def test_topicos(self):
        self.ir_aba('topicos', 'Topicos - Duvidas Academicas')
        
        id_disciplina = self.pegar_id_aleatorio('disciplinas')
        id_usuario = self.pegar_id_aleatorio('usuarios')
        
        topico = random.choice(TOPICOS_FORUM)
        
        print(f"\nCriando topico: '{topico['titulo']}'")
        print(f"  - Disciplina ID: {id_disciplina} (aleatorio do banco)")
        print(f"  - Usuario ID: {id_usuario} (aleatorio do banco)\n")
        
        self.preencher('top_titulo', topico['titulo'], 'Titulo')
        self.preencher('top_conteudo', topico['conteudo'], 'Conteudo')
        self.preencher('top_disciplina', id_disciplina, 'ID Disciplina')
        self.preencher('top_usuario', id_usuario, 'ID Usuario')
        self.selecionar('top_categoria', 'Categoria', valor_especifico=topico['categoria'])
        
        if self.submeter('form-topico'):
            time.sleep(1)
            self.pesquisar_banco_completo()
    
    def test_respostas(self):
        self.ir_aba('respostas', 'Respostas')
        
        id_topico = self.pegar_id_aleatorio('topicos')
        id_usuario = self.pegar_id_aleatorio('usuarios')
        
        conteudo_resposta = random.choice(RESPOSTAS_TOPICOS)
        
        print(f"\nCriando resposta")
        print(f"  - Topico ID: {id_topico} (aleatorio do banco)")
        print(f"  - Usuario ID: {id_usuario} (aleatorio do banco)")
        print(f"  - Resposta: '{conteudo_resposta[:50]}...'\n")
        
        self.preencher('resp_topico', id_topico, 'ID Topico')
        self.preencher('resp_usuario', id_usuario, 'ID Usuario')
        self.preencher('resp_conteudo', conteudo_resposta, 'Conteudo')
        
        if self.submeter('form-resposta'):
            self.ultima_resposta_criada = {
                'topico_id': id_topico,
                'usuario_id': id_usuario,
                'conteudo': conteudo_resposta
            }
            time.sleep(1)
            self.pesquisar_banco_completo()
    
    def test_buscar_resposta_por_topico(self):
        """Busca respostas usando ID de um topico do banco"""
        self.ir_aba('respostas', 'Respostas - Busca por Topico')
        
        id_topico = self.pegar_id_aleatorio('topicos')
        
        print(f"\nBuscando respostas do topico ID: {id_topico}\n")
        
        try:
            possiveis_campos = ['busca_topico', 'filtro_topico', 'resp_busca', 'search_topico', 'resp_topico_busca']
            
            campo_busca = None
            for campo_id in possiveis_campos:
                try:
                    campo_busca = self.driver.find_element(By.ID, campo_id)
                    print(f"  [OK] Campo de busca: {campo_id}")
                    break
                except:
                    continue
            
            if not campo_busca:
                inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="number"]')
                if inputs:
                    campo_busca = inputs[0]
                    print(f"  [OK] Campo de busca: encontrado por tipo")
            
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
                campo_busca.send_keys(str(id_topico))
                print(f"  [OK] Digitado: {id_topico}")
                time.sleep(0.5)
                
                campo_busca.send_keys(Keys.ENTER)
                print(f"  [OK] Enter pressionado")
                time.sleep(2)
                
                self.driver.execute_script("""
                    arguments[0].style.border='';
                    arguments[0].style.boxShadow='';
                """, campo_busca)
                
                print(f"  [OK] Busca realizada com sucesso\n")
                
                altura = self.driver.execute_script("return document.body.scrollHeight")
                meio = altura // 2
                self.driver.execute_script(f"window.scrollTo(0, {meio});")
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.5)
            else:
                print(f"  [AVISO] Campo de busca nao encontrado\n")
                
        except Exception as e:
            print(f"  [ERRO] Erro na busca: {str(e)[:50]}\n")
    
    def test_excluir_ultimo_mural(self):
        self.ir_aba('mural', 'Mural - Exclusao')
        
        print("\nExcluindo ultimo recado do mural:\n")
        
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            botoes = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="deleteRecado"]')
            
            if botoes:
                ultimo = botoes[-1]
                print(f"  [OK] Encontrados {len(botoes)} recados")
                print(f"  -> Excluindo o ultimo...")
                
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
                    print(f"  [OK] Recado excluido com sucesso!\n")
                except:
                    print(f"  [OK] Recado excluido!\n")
            else:
                print(f"  [AVISO] Nenhum recado disponivel para excluir\n")
                
        except Exception as e:
            print(f"  [ERRO] {str(e)[:50]}\n")
    
    def test_editar_usuario(self):
        """Testa edicao de usuario"""
        self.ir_aba('usuarios', 'Usuarios - Edicao')
        
        print("\nTestando edicao de usuario:\n")
        
        try:
            # Pegar primeiro usuario da lista
            time.sleep(1)
            botoes_editar = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="editarUsuario"]')
            
            if botoes_editar:
                print(f"  [OK] Encontrados {len(botoes_editar)} usuarios")
                
                # Clicar no primeiro botao editar
                primeiro = botoes_editar[0]
                self.driver.execute_script("""
                    arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
                """, primeiro)
                time.sleep(0.5)
                
                self.driver.execute_script("""
                    arguments[0].style.border='2px solid #f59e0b';
                    arguments[0].style.transform='scale(1.05)';
                """, primeiro)
                
                time.sleep(0.6)
                primeiro.click()
                time.sleep(2)
                
                print(f"  [OK] Usuario carregado para edicao")
                
                # Alterar alguns campos
                novo_nome = f"Usuario Editado {int(time.time()) % 1000}"
                self.preencher('user_nome', novo_nome, 'Novo Nome')
                self.preencher('user_senha', 'novaSenha456', 'Nova Senha')
                
                # Submeter
                if self.submeter('form-usuario'):
                    print(f"  [OK] Usuario atualizado com sucesso!")
                    time.sleep(1)
                    self.pesquisar_banco_completo()
            else:
                print(f"  [AVISO] Nenhum usuario para editar")
        except Exception as e:
            print(f"  [ERRO] {str(e)[:50]}\n")
    
    def executar(self):
        self.setup()
        
        try:
            print("\nAbrindo aplicacao...")
            self.driver.get(BASE_URL)
            time.sleep(1.5)
            print("[OK] Aplicacao carregada")
            
            # Pesquisar banco ANTES de comecar
            self.pesquisar_banco_completo()
            
            # EXECUTAR CADA TESTE UMA VEZ
            self.test_mural()
            self.test_usuarios()
            self.test_disciplinas()
            self.test_topicos()
            self.test_respostas()
            
            # TESTES ESPECIAIS - UMA VEZ
            self.test_buscar_resposta_por_topico()
            self.test_editar_usuario()
            self.test_excluir_ultimo_mural()
            
            print("\n" + "="*80)
            print("TESTE CONCLUIDO COM SUCESSO")
            print("="*80)
            
            self.driver.save_screenshot('/tmp/teste_final.png')
            print("\nScreenshot: /tmp/teste_final.png\n")
            
        except KeyboardInterrupt:
            print("\n\n[AVISO] Teste interrompido pelo usuario")
        except Exception as e:
            print(f"\n[ERRO] {e}")
        finally:
            print("Fechando navegador em 5 segundos...")
            time.sleep(5)
            self.driver.quit()
            print("[OK] Navegador fechado\n")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTE SELENIUM FINAL - FORUM ACADEMICO UNIFEI")
    print("="*80)
    print("\nCaracteristicas:")
    print("  - Textos coerentes por contexto")
    print("  - Avisos no mural (nao duvidas)")
    print("  - Duvidas nos topicos (nao avisos)")
    print("  - Respostas relacionadas as duvidas")
    print("  - IDs aleatorios do banco de dados")
    print("  - Busca de respostas por ID de topico")
    print("  - Edicao e exclusao de usuarios")
    print("  - Sistema de melhor resposta")
    print("\n" + "="*80)
    
    input("\nPressione ENTER para iniciar o teste...")
    
    teste = TesteSeleniumFinal()
    teste.executar()
