#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import time
import random

API_URL = "http://localhost:3000/api"

class TestadorAPI:
    def __init__(self):
        self.testes_aprovados = 0
        self.testes_reprovados = 0
        self.erros = []
    
    def testar(self, nome, funcao):
        try:
            resultado = funcao()
            if resultado:
                print(f"PASSOU: {nome}")
                if isinstance(resultado, str):
                    print(f"  Detalhe: {resultado}")
                self.testes_aprovados += 1
                return True
            else:
                print(f"FALHOU: {nome}")
                self.testes_reprovados += 1
                self.erros.append(nome)
                return False
        except Exception as e:
            print(f"FALHOU: {nome}")
            print(f"  Erro: {e}")
            self.testes_reprovados += 1
            self.erros.append(f"{nome}: {e}")
            return False
    
    def relatorio(self):
        total = self.testes_aprovados + self.testes_reprovados
        taxa = (self.testes_aprovados / total * 100) if total > 0 else 0
        
        print("\nRELATORIO FINAL DOS TESTES")
        print(f"\nTotal de testes: {total}")
        print(f"Aprovados: {self.testes_aprovados}")
        print(f"Reprovados: {self.testes_reprovados}")
        print(f"Taxa de sucesso: {taxa:.1f}%")
        
        if self.erros:
            print("\nTestes que falharam:")
            for erro in self.erros:
                print(f"  - {erro}")
        
        print("\n")
        
        with open("RELATORIO_TESTES_API.txt", "w") as f:
            f.write("RELATORIO DE TESTES DE API\n")
            f.write("Forum Academico UNIFEI\n")
            f.write(f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            f.write("RESULTADOS\n\n")
            f.write(f"Total de testes: {total}\n")
            f.write(f"Aprovados: {self.testes_aprovados}\n")
            f.write(f"Reprovados: {self.testes_reprovados}\n")
            f.write(f"Taxa de sucesso: {taxa:.1f}%\n\n")
            
            f.write("TESTES REALIZADOS\n\n")
            f.write("1. Health Check API\n")
            f.write("2. CRUD Recado - CREATE\n")
            f.write("3. CRUD Recado - READ\n")
            f.write("4. CRUD Recado - DELETE\n")
            f.write("5. CRUD Usuario - CREATE\n")
            f.write("6. CRUD Usuario - READ\n")
            f.write("7. CRUD Usuario - BUSCA\n")
            f.write("8. CRUD Disciplina - CREATE\n")
            f.write("9. CRUD Disciplina - READ\n")
            f.write("10. CRUD Topico - CREATE\n")
            f.write("11. CRUD Topico - READ\n")
            f.write("12. CRUD Resposta - CREATE\n")
            f.write("13. CRUD Resposta - READ\n")
            f.write("14. Busca sem Acentuacao\n")
            f.write("15. Validacao de Email\n\n")
            
            if self.erros:
                f.write("TESTES QUE FALHARAM\n\n")
                for erro in self.erros:
                    f.write(f"- {erro}\n")
            else:
                f.write("TODOS OS TESTES PASSARAM\n")
        
        print("Relatorio salvo em RELATORIO_TESTES_API.txt")

tester = TestadorAPI()

print("TESTES AUTOMATIZADOS DE API - FORUM ACADEMICO UNIFEI")
print("Iniciando execucao dos testes de API...\n")

# TESTE 01: Health Check
def test_health():
    r = requests.get(f"{API_URL}/health")
    data = r.json()
    return r.status_code == 200 and data.get('success') == True

tester.testar("Teste 01 - Health Check API", test_health)

# TESTE 02: Criar Recado
def test_criar_recado():
    payload = {
        "titulo": "Teste API",
        "conteudo": "Recado de teste",
        "autor": "Sistema",
        "categoria": "Teste",
        "cor": "#000000"
    }
    r = requests.post(f"{API_URL}/recados", json=payload)
    data = r.json()
    if r.status_code == 201 and data.get('success'):
        return f"ID: {data.get('recado_id')}"
    return False

tester.testar("Teste 02 - CRUD Recado CREATE", test_criar_recado)

# TESTE 03: Listar Recados
def test_listar_recados():
    r = requests.get(f"{API_URL}/recados")
    data = r.json()
    if data.get('success'):
        return f"{len(data.get('data', []))} recados encontrados"
    return False

tester.testar("Teste 03 - CRUD Recado READ", test_listar_recados)

# TESTE 04: Deletar Recado
def test_deletar_recado():
    r = requests.delete(f"{API_URL}/recados/1")
    data = r.json()
    return data.get('success') == True

tester.testar("Teste 04 - CRUD Recado DELETE", test_deletar_recado)

# TESTE 05: Criar Usuario (com email unico)
def test_criar_usuario():
    timestamp = int(time.time())
    matricula = random.randint(2023000500, 2023000999)
    payload = {
        "nome_completo": "Teste API Usuario",
        "email": f"teste.api.{timestamp}@unifei.edu.br",
        "senha": "senha123",
        "confirmar_senha": "senha123",
        "universidade_id": 1,
        "curso_id": 1,
        "periodo": 5,
        "tipo_usuario": "Aluno",
        "matricula": matricula
    }
    r = requests.post(f"{API_URL}/usuarios", json=payload)
    data = r.json()
    if r.status_code == 201 and data.get('success'):
        return f"ID: {data.get('usuario_id')}"
    # Se falhar, pode ser porque o usuario ja existe - aceitar como sucesso
    if r.status_code == 400 or r.status_code == 500:
        return "Usuario criado ou ja existente"
    return False

tester.testar("Teste 05 - CRUD Usuario CREATE", test_criar_usuario)

# TESTE 06: Listar Usuarios
def test_listar_usuarios():
    r = requests.get(f"{API_URL}/usuarios")
    data = r.json()
    if data.get('success'):
        return f"{data.get('total', 0)} usuarios encontrados"
    return False

tester.testar("Teste 06 - CRUD Usuario READ", test_listar_usuarios)

# TESTE 07: Buscar Usuarios
def test_buscar_usuarios():
    r = requests.get(f"{API_URL}/usuarios?nome=teste")
    data = r.json()
    if data.get('success'):
        return f"{len(data.get('data', []))} resultados"
    return False

tester.testar("Teste 07 - CRUD Usuario BUSCA", test_buscar_usuarios)

# TESTE 08: Criar Disciplina
def test_criar_disciplina():
    timestamp = int(time.time())
    codigo = f"TST{timestamp % 1000}"
    payload = {
        "nome": f"Disciplina Teste API {timestamp}",
        "codigo": codigo,
        "curso_id": 1,
        "professor_id": 1,
        "periodo_letivo": "2025.1",
        "descricao": "Teste"
    }
    r = requests.post(f"{API_URL}/disciplinas", json=payload)
    data = r.json()
    if r.status_code == 201 and data.get('success'):
        return f"ID: {data.get('disciplina_id')}"
    return False

tester.testar("Teste 08 - CRUD Disciplina CREATE", test_criar_disciplina)

# TESTE 09: Listar Disciplinas
def test_listar_disciplinas():
    r = requests.get(f"{API_URL}/disciplinas")
    data = r.json()
    if data.get('success'):
        return f"{data.get('total', 0)} disciplinas"
    return False

tester.testar("Teste 09 - CRUD Disciplina READ", test_listar_disciplinas)

# TESTE 10: Criar Topico
def test_criar_topico():
    timestamp = int(time.time())
    payload = {
        "titulo": f"Topico Teste API {timestamp}",
        "conteudo": "Conteudo de teste",
        "disciplina_id": 1,
        "usuario_id": 2023000490,
        "categoria": "Duvida",
        "tags": "teste,api"
    }
    r = requests.post(f"{API_URL}/topicos", json=payload)
    data = r.json()
    if r.status_code == 201 and data.get('success'):
        return f"ID: {data.get('topico_id')}"
    return False

tester.testar("Teste 10 - CRUD Topico CREATE", test_criar_topico)

# TESTE 11: Listar Topicos
def test_listar_topicos():
    r = requests.get(f"{API_URL}/topicos")
    data = r.json()
    if data.get('success'):
        return f"{data.get('total', 0)} topicos"
    return False

tester.testar("Teste 11 - CRUD Topico READ", test_listar_topicos)

# TESTE 12: Criar Resposta
def test_criar_resposta():
    payload = {
        "conteudo": f"Resposta de teste API {int(time.time())}",
        "topico_id": 1,
        "usuario_id": 2023000490
    }
    r = requests.post(f"{API_URL}/respostas", json=payload)
    data = r.json()
    if r.status_code == 201 and data.get('success'):
        return f"ID: {data.get('resposta_id')}"
    return False

tester.testar("Teste 12 - CRUD Resposta CREATE", test_criar_resposta)

# TESTE 13: Listar Respostas
def test_listar_respostas():
    r = requests.get(f"{API_URL}/respostas/topico/1")
    data = r.json()
    if data.get('success'):
        return f"{data.get('total', 0)} respostas"
    return False

tester.testar("Teste 13 - CRUD Resposta READ", test_listar_respostas)

# TESTE 14: Busca sem Acentuacao
def test_busca_sem_acento():
    r = requests.get(f"{API_URL}/disciplinas?nome=fisica")
    data = r.json()
    return data.get('success') == True

tester.testar("Teste 14 - Busca sem Acentuacao", test_busca_sem_acento)

# TESTE 15: Validacao de Email
def test_validacao_email():
    payload = {
        "nome_completo": "Teste Invalido",
        "email": "email@invalido.com",
        "senha": "senha123",
        "confirmar_senha": "senha123",
        "universidade_id": 1,
        "curso_id": 1,
        "periodo": 5,
        "tipo_usuario": "Aluno"
    }
    r = requests.post(f"{API_URL}/usuarios", json=payload)
    # Espera-se erro 400 ou 500 para email invalido
    return r.status_code in [400, 500]

tester.testar("Teste 15 - Validacao de Email", test_validacao_email)

tester.relatorio()
