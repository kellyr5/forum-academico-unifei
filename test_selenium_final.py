#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE SELENIUM FINAL
Textos coerentes por contexto, IDs aleatórios do banco
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

# MURAL - Avisos e informações institucionais
RECADOS_MURAL = [
    {
        'titulo': 'Aula cancelada - Cálculo II',
        'conteudo': 'Atenção alunos! A aula de Cálculo II do dia 15/11 está cancelada devido a compromisso do professor. A reposição será agendada.',
        'categoria': 'Aviso'
    },
    {
        'titulo': 'Reunião do projeto integrador',
        'conteudo': 'Convocamos todos os grupos do projeto integrador para reunião geral na próxima sexta-feira, às 14h, no auditório principal.',
        'categoria': 'Evento'
    },
    {
        'titulo': 'Alteração de horário de atendimento',
        'conteudo': 'Informamos que o horário de atendimento da coordenação foi alterado. Novo horário: terças e quintas das 15h às 17h.',
        'categoria': 'Aviso'
    },
    {
        'titulo': 'Prazo de entrega prorrogado',
        'conteudo': 'Boa notícia! O prazo para entrega do trabalho de Programação foi prorrogado até o dia 20/11. Aproveitem o tempo extra!',
        'categoria': 'Aviso'
    }
]

# TÓPICOS - Dúvidas e discussões acadêmicas
TOPICOS_FORUM = [
    {
        'titulo': 'Dúvida sobre recursão na prova',
        'conteudo': 'Pessoal, alguém sabe se vai cair recursão na prova de Algoritmos? Estou com dificuldade nesse assunto e queria saber se devo focar nisso.',
        'categoria': 'Dúvida'
    },
    {
        'titulo': 'Material da última aula disponível?',
        'conteudo': 'Faltei na aula passada de Física e preciso urgente do material. Alguém tem os slides ou anotações que possa compartilhar?',
        'categoria': 'Dúvida'
    },
    {
        'titulo': 'Formando grupo de estudos para Cálculo',
        'conteudo': 'Estou organizando um grupo de estudos para a prova de Cálculo II. Quem tiver interesse, vamos nos reunir às quartas às 16h na biblioteca.',
        'categoria': 'Discussão'
    },
    {
        'titulo': 'Como resolver o exercício 5 da lista?',
        'conteudo': 'Alguém conseguiu fazer o exercício 5 da lista de Programação? Não estou entendendo a lógica dele, principalmente a parte de arrays.',
        'categoria': 'Dúvida'
    }
]

# RESPOSTAS - Relacionadas às dúvidas
RESPOSTAS_TOPICOS = [
    'Sim, vai cair recursão! O professor avisou na última aula. É bom revisar os exemplos de fatorial e fibonacci que ele passou.',
    'Tenho o material aqui! Vou te mandar por email. São 3 slides sobre cinemática.',
    'Eu me interesso no grupo! Cálculo II está difícil mesmo. Podemos dividir os exercícios entre nós.',
    'Consegui fazer sim! A chave é usar dois loops aninhados e ir comparando os elementos. Te explico melhor se quiser.',
    'Vi esse conteúdo na bibliografia do capítulo 7. Tem uns exemplos bem parecidos lá.',
    'Valeu pela informação! Vou estudar esse tópico então.'
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
        print("║" + "TESTE SELENIUM FINAL - CONTEXTOS COERENTES".center(78) + "║")
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
        return random.randint(1, 5)
    
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
    
    def selecionar(self, campo_id, nome, indice=None, valor_especifico=None):
        """Seleciona por índice aleatório ou valor específico"""
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
            
            # Se tem valor específico, procurar por ele
            if valor_especifico:
                for i, opt in enumerate(opcoes):
                    if valor_especifico.lower() in opt.text.lower():
                        indice = i
                        break
            
            # Se não tem índice, escolher aleatório
            if indice is None:
                opcoes_validas = [i for i, opt in enumerate(opcoes) 
                                 if opt.get_attribute('value') and opt.get_attribute('value') != '']
                if opcoes_validas:
                    indice = random.choice(opcoes_validas)
                else:
                    indice = 1 if len(opcoes) > 1 else 0
            
            # Ajustar se necessário
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
        self.ir_aba('mural', 'Mural - Avisos Institucionais')
        
        # Escolher recado coerente
        recado = random.choice(RECADOS_MURAL)
        
        print(f"\n📢 Criando aviso: '{recado['titulo']}'\n")
        
        self.preencher('rec_titulo', recado['titulo'], 'Título')
        self.preencher('rec_autor', 'Coordenação', 'Autor')
        self.preencher('rec_conteudo', recado['conteudo'], 'Conteúdo')
        
        # Selecionar categoria específica do recado
        self.selecionar('rec_categoria', 'Categoria', valor_especifico=recado['categoria'])
        
        self.submeter('form-recado')
    
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
        nome_usuario = f'Aluno Teste {timestamp}'
        
        print(f"\n👤 Criando usuário: '{nome_usuario}'\n")
        
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
        
        # ID ALEATÓRIO do banco
        id_professor = self.pegar_id_aleatorio('usuarios')
        print(f"\n📚 Criando disciplina")
        print(f"  • Professor ID: {id_professor} (aleatório do banco)\n")
        
        timestamp = int(time.time()) % 10000
        disciplinas = ["Programação I", "Cálculo II", "Física Experimental", "Algoritmos e Estruturas de Dados"]
        nome_disc = random.choice(disciplinas)
        
        self.preencher('disc_nome', nome_disc, 'Nome')
        self.preencher('disc_codigo', f'ENG{timestamp}', 'Código')
        self.selecionar('disc_curso', 'Curso')
        self.preencher('disc_professor', id_professor, 'ID Professor')
        self.preencher('disc_periodo', '2025.1', 'Período')
        
        if self.submeter('form-disciplina'):
            time.sleep(1)
            self.pesquisar_banco_completo()
    
    def test_topicos(self):
        self.ir_aba('topicos', 'Tópicos - Dúvidas Acadêmicas')
        
        # IDs ALEATÓRIOS do banco
        id_disciplina = self.pegar_id_aleatorio('disciplinas')
        id_usuario = self.pegar_id_aleatorio('usuarios')
        
        # Escolher tópico coerente
        topico = random.choice(TOPICOS_FORUM)
        
        print(f"\n💬 Criando tópico: '{topico['titulo']}'")
        print(f"  • Disciplina ID: {id_disciplina} (aleatório do banco)")
        print(f"  • Usuário ID: {id_usuario} (aleatório do banco)\n")
        
        self.preencher('top_titulo', topico['titulo'], 'Título')
        self.preencher('top_conteudo', topico['conteudo'], 'Conteúdo')
        self.preencher('top_disciplina', id_disciplina, 'ID Disciplina')
        self.preencher('top_usuario', id_usuario, 'ID Usuário')
        
        # Selecionar categoria específica do tópico
        self.selecionar('top_categoria', 'Categoria', valor_especifico=topico['categoria'])
        
        if self.submeter('form-topico'):
            time.sleep(1)
            self.pesquisar_banco_completo()
    
    def test_respostas(self):
        self.ir_aba('respostas', 'Respostas')
        
        # IDs ALEATÓRIOS do banco
        id_topico = self.pegar_id_aleatorio('topicos')
        id_usuario = self.pegar_id_aleatorio('usuarios')
        
        # Escolher resposta coerente
        conteudo_resposta = random.choice(RESPOSTAS_TOPICOS)
        
        print(f"\n💡 Criando resposta")
        print(f"  • Tópico ID: {id_topico} (aleatório do banco)")
        print(f"  • Usuário ID: {id_usuario} (aleatório do banco)")
        print(f"  • Resposta: '{conteudo_resposta[:50]}...'\n")
        
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
    
    def test_buscar_resposta_por_topico(self):
        """Busca respostas usando ID de um tópico do banco"""
        self.ir_aba('respostas', 'Respostas - Busca por Tópico')
        
        # Pegar um ID de tópico do banco
        id_topico = self.pegar_id_aleatorio('topicos')
        
        print(f"\n🔍 Buscando respostas do tópico ID: {id_topico}\n")
        
        try:
            # Tentar encontrar campo de busca
            possiveis_campos = ['busca_topico', 'filtro_topico', 'resp_busca', 'search_topico', 'resp_topico_busca']
            
            campo_busca = None
            for campo_id in possiveis_campos:
                try:
                    campo_busca = self.driver.find_element(By.ID, campo_id)
                    print(f"  ✓ Campo de busca: {campo_id}")
                    break
                except:
                    continue
            
            # Se não encontrou por ID, tentar por tipo
            if not campo_busca:
                inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="number"]')
                if inputs:
                    campo_busca = inputs[0]
                    print(f"  ✓ Campo de busca: encontrado por tipo")
            
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
                print(f"  ✓ Digitado: {id_topico}")
                time.sleep(0.5)
                
                campo_busca.send_keys(Keys.ENTER)
                print(f"  ✓ Enter pressionado")
                time.sleep(2)
                
                self.driver.execute_script("""
                    arguments[0].style.border='';
                    arguments[0].style.boxShadow='';
                """, campo_busca)
                
                print(f"  ✓ Busca realizada com sucesso\n")
                
                # Scroll para ver resultados
                altura = self.driver.execute_script("return document.body.scrollHeight")
                meio = altura // 2
                self.driver.execute_script(f"window.scrollTo(0, {meio});")
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.5)
            else:
                print(f"  ⚠ Campo de busca não encontrado\n")
                
        except Exception as e:
            print(f"  ✗ Erro na busca: {str(e)[:50]}\n")
    
    def test_excluir_ultimo_mural(self):
        self.ir_aba('mural', 'Mural - Exclusão')
        
        print("\n🗑️  Excluindo último recado do mural:\n")
        
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            botoes = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="deleteRecado"]')
            
            if botoes:
                ultimo = botoes[-1]
                print(f"  ✓ Encontrados {len(botoes)} recados")
                print(f"  → Excluindo o último...")
                
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
                    print(f"  ✓ Recado excluído com sucesso!\n")
                except:
                    print(f"  ✓ Recado excluído!\n")
            else:
                print(f"  ⚠ Nenhum recado disponível para excluir\n")
                
        except Exception as e:
            print(f"  ✗ Erro: {str(e)[:50]}\n")
    
    def executar(self):
        self.setup()
        
        try:
            print("\n⏳ Abrindo aplicação...")
            self.driver.get(BASE_URL)
            time.sleep(1.5)
            print("✓ Aplicação carregada")
            
            # Pesquisar banco antes de começar
            self.pesquisar_banco_completo()
            
            # Executar testes
            self.test_mural()
            self.test_usuarios()
            self.test_disciplinas()
            self.test_topicos()
            self.test_respostas()
            self.test_buscar_resposta_por_topico()
            self.test_excluir_ultimo_mural()
            
            print("\n" + "╔" + "═"*78 + "╗")
            print("║" + "TESTE CONCLUÍDO COM SUCESSO".center(78) + "║")
            print("╚" + "═"*78 + "╝")
            
            self.driver.save_screenshot('/tmp/teste_final.png')
            print("\n📸 Screenshot salvo: /tmp/teste_final.png\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠ Teste interrompido pelo usuário")
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
        finally:
            print("⏳ Fechando navegador em 5 segundos...")
            time.sleep(5)
            self.driver.quit()
            print("✓ Navegador fechado\n")

if __name__ == "__main__":
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + "TESTE SELENIUM FINAL - CONTEXTOS COERENTES".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print("\n✨ Características:")
    print("  • Textos coerentes por contexto")
    print("  • Avisos no mural (não dúvidas)")
    print("  • Dúvidas nos tópicos (não avisos)")
    print("  • Respostas relacionadas às dúvidas")
    print("  • IDs aleatórios do banco de dados")
    print("  • Busca de respostas por ID de tópico")
    print("  • Sem destaques de inserção")
    print("\n" + "═"*80)
    
    input("\n▶ Pressione ENTER para iniciar o teste...")
    
    teste = TesteSeleniumFinal()
    teste.executar()
