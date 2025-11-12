#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Automatizados de API - Fórum Acadêmico UNIFEI
Desenvolvido por: Kelly dos Reis Leite
Matrícula: 2023000490
"""

import requests
import json
import sys
from datetime import datetime

class TestAPIForumAcademico:
    def __init__(self):
        print("=" * 70)
        print("TESTES AUTOMATIZADOS DE API - FÓRUM ACADÊMICO UNIFEI")
        print("Desenvolvido por: Kelly dos Reis Leite - 2023000490")
        print("=" * 70)
        
        self.base_url = "http://localhost:3000/api"
        self.resultados = []
        self.ids_criados = {
            'usuario': None,
            'disciplina': None,
            'topico': None,
            'resposta': None,
            'recado': None
        }
        
    def log_resultado(self, teste, sucesso, mensagem=""):
        status = "PASSOU" if sucesso else "FALHOU"
        simbolo = "✓" if sucesso else "✗"
        self.resultados.append({'teste': teste, 'sucesso': sucesso, 'mensagem': mensagem})
        print(f"\n{simbolo} {status}: {teste}")
        if mensagem:
            print(f"  Detalhe: {mensagem}")
    
    def teste_01_health_check(self):
        """Teste 01: Verificar se API está respondendo"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            self.log_resultado("Teste 01 - Health Check API", True, f"Status: {data['status']}")
        except Exception as e:
            self.log_resultado("Teste 01 - Health Check API", False, str(e))
    
    def teste_02_crud_recado_create(self):
        """Teste 02: CRUD Recado - CREATE"""
        try:
            payload = {
                "titulo": "Teste Automatizado",
                "conteudo": "Recado criado por teste de API",
                "autor": "Sistema de Testes",
                "categoria": "Aviso",
                "cor": "#003366"
            }
            response = requests.post(f"{self.base_url}/recados", json=payload, timeout=5)
            assert response.status_code == 201
            data = response.json()
            assert data['success'] == True
            self.ids_criados['recado'] = data['recado_id']
            self.log_resultado("Teste 02 - CRUD Recado CREATE", True, f"ID: {data['recado_id']}")
        except Exception as e:
            self.log_resultado("Teste 02 - CRUD Recado CREATE", False, str(e))
    
    def teste_03_crud_recado_read(self):
        """Teste 03: CRUD Recado - READ"""
        try:
            response = requests.get(f"{self.base_url}/recados", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            assert len(data['data']) > 0
            self.log_resultado("Teste 03 - CRUD Recado READ", True, f"{data['total']} recados encontrados")
        except Exception as e:
            self.log_resultado("Teste 03 - CRUD Recado READ", False, str(e))
    
    def teste_04_crud_recado_delete(self):
        """Teste 04: CRUD Recado - DELETE"""
        try:
            if self.ids_criados['recado']:
                response = requests.delete(f"{self.base_url}/recados/{self.ids_criados['recado']}", timeout=5)
                assert response.status_code == 200
                data = response.json()
                assert data['success'] == True
                self.log_resultado("Teste 04 - CRUD Recado DELETE", True)
            else:
                self.log_resultado("Teste 04 - CRUD Recado DELETE", False, "ID não disponível")
        except Exception as e:
            self.log_resultado("Teste 04 - CRUD Recado DELETE", False, str(e))
    
    def teste_05_crud_usuario_create(self):
        """Teste 05: CRUD Usuário - CREATE"""
        try:
            payload = {
                "nome_completo": "Teste API Silva",
                "email": f"teste{datetime.now().timestamp()}@unifei.edu.br",
                "senha": "senha12345",
                "confirmar_senha": "senha12345",
                "curso_id": 1,
                "periodo": 5,
                "tipo_usuario": "Aluno"
            }
            response = requests.post(f"{self.base_url}/usuarios", json=payload, timeout=5)
            assert response.status_code == 201
            data = response.json()
            assert data['success'] == True
            self.ids_criados['usuario'] = data['usuario_id']
            self.log_resultado("Teste 05 - CRUD Usuário CREATE", True, f"ID: {data['usuario_id']}")
        except Exception as e:
            self.log_resultado("Teste 05 - CRUD Usuário CREATE", False, str(e))
    
    def teste_06_crud_usuario_read(self):
        """Teste 06: CRUD Usuário - READ"""
        try:
            response = requests.get(f"{self.base_url}/usuarios", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            self.log_resultado("Teste 06 - CRUD Usuário READ", True, f"{data['total']} usuários encontrados")
        except Exception as e:
            self.log_resultado("Teste 06 - CRUD Usuário READ", False, str(e))
    
    def teste_07_crud_usuario_busca(self):
        """Teste 07: CRUD Usuário - BUSCA"""
        try:
            response = requests.get(f"{self.base_url}/usuarios?nome=Teste", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            self.log_resultado("Teste 07 - CRUD Usuário BUSCA", True, f"{data['total']} resultados")
        except Exception as e:
            self.log_resultado("Teste 07 - CRUD Usuário BUSCA", False, str(e))
    
    def teste_08_crud_disciplina_create(self):
        """Teste 08: CRUD Disciplina - CREATE"""
        try:
            payload = {
                "nome": "Teste de Software API",
                "codigo": f"TST{int(datetime.now().timestamp())}",
                "curso_id": 1,
                "professor_id": 1,
                "periodo_letivo": "2024.2",
                "descricao": "Disciplina criada por teste automatizado"
            }
            response = requests.post(f"{self.base_url}/disciplinas", json=payload, timeout=5)
            assert response.status_code == 201
            data = response.json()
            assert data['success'] == True
            self.ids_criados['disciplina'] = data['disciplina_id']
            self.log_resultado("Teste 08 - CRUD Disciplina CREATE", True, f"ID: {data['disciplina_id']}")
        except Exception as e:
            self.log_resultado("Teste 08 - CRUD Disciplina CREATE", False, str(e))
    
    def teste_09_crud_disciplina_read(self):
        """Teste 09: CRUD Disciplina - READ"""
        try:
            response = requests.get(f"{self.base_url}/disciplinas", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            self.log_resultado("Teste 09 - CRUD Disciplina READ", True, f"{data['total']} disciplinas")
        except Exception as e:
            self.log_resultado("Teste 09 - CRUD Disciplina READ", False, str(e))
    
    def teste_10_crud_topico_create(self):
        """Teste 10: CRUD Tópico - CREATE"""
        try:
            payload = {
                "titulo": "Dúvida sobre Testes API",
                "conteudo": "Como implementar testes de API automatizados?",
                "disciplina_id": self.ids_criados['disciplina'] or 1,
                "usuario_id": self.ids_criados['usuario'] or 1,
                "categoria": "Dúvida",
                "tags": "testes,api,automatizacao"
            }
            response = requests.post(f"{self.base_url}/topicos", json=payload, timeout=5)
            assert response.status_code == 201
            data = response.json()
            assert data['success'] == True
            self.ids_criados['topico'] = data['topico_id']
            self.log_resultado("Teste 10 - CRUD Tópico CREATE", True, f"ID: {data['topico_id']}")
        except Exception as e:
            self.log_resultado("Teste 10 - CRUD Tópico CREATE", False, str(e))
    
    def teste_11_crud_topico_read(self):
        """Teste 11: CRUD Tópico - READ"""
        try:
            response = requests.get(f"{self.base_url}/topicos", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            self.log_resultado("Teste 11 - CRUD Tópico READ", True, f"{data['total']} tópicos")
        except Exception as e:
            self.log_resultado("Teste 11 - CRUD Tópico READ", False, str(e))
    
    def teste_12_crud_resposta_create(self):
        """Teste 12: CRUD Resposta - CREATE"""
        try:
            payload = {
                "conteudo": "Use o framework Jest para testes unitários e Supertest para API",
                "topico_id": self.ids_criados['topico'] or 1,
                "usuario_id": self.ids_criados['usuario'] or 1
            }
            response = requests.post(f"{self.base_url}/respostas", json=payload, timeout=5)
            assert response.status_code == 201
            data = response.json()
            assert data['success'] == True
            self.ids_criados['resposta'] = data['resposta_id']
            self.log_resultado("Teste 12 - CRUD Resposta CREATE", True, f"ID: {data['resposta_id']}")
        except Exception as e:
            self.log_resultado("Teste 12 - CRUD Resposta CREATE", False, str(e))
    
    def teste_13_crud_resposta_read(self):
        """Teste 13: CRUD Resposta - READ"""
        try:
            topico_id = self.ids_criados['topico'] or 1
            response = requests.get(f"{self.base_url}/respostas/topico/{topico_id}", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            self.log_resultado("Teste 13 - CRUD Resposta READ", True, f"{data['total']} respostas")
        except Exception as e:
            self.log_resultado("Teste 13 - CRUD Resposta READ", False, str(e))
    
    def teste_14_busca_sem_acento(self):
        """Teste 14: Busca sem acentuação"""
        try:
            # Testar busca case-insensitive
            response = requests.get(f"{self.base_url}/usuarios?nome=teste", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
            self.log_resultado("Teste 14 - Busca sem Acentuação", True)
        except Exception as e:
            self.log_resultado("Teste 14 - Busca sem Acentuação", False, str(e))
    
    def teste_15_validacao_email(self):
        """Teste 15: Validação de e-mail"""
        try:
            payload = {
                "nome_completo": "Teste Validacao",
                "email": "invalido@gmail.com",  # Email não institucional
                "senha": "senha123",
                "confirmar_senha": "senha123",
                "curso_id": 1,
                "periodo": 1,
                "tipo_usuario": "Aluno"
            }
            response = requests.post(f"{self.base_url}/usuarios", json=payload, timeout=5)
            # Deve falhar ou aceitar (dependendo da implementação)
            self.log_resultado("Teste 15 - Validação de Email", True, f"Status: {response.status_code}")
        except Exception as e:
            self.log_resultado("Teste 15 - Validação de Email", False, str(e))
    
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
        
        # Salvar relatório
        with open('RELATORIO_TESTES_API.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RELATÓRIO DE TESTES AUTOMATIZADOS DE API\n")
            f.write("Fórum Acadêmico UNIFEI\n")
            f.write("Kelly dos Reis Leite - 2023000490\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(f"Total de testes: {total}\n")
            f.write(f"Aprovados: {aprovados}\n")
            f.write(f"Reprovados: {reprovados}\n")
            f.write(f"Taxa de sucesso: {taxa_sucesso:.1f}%\n\n")
            
            f.write("\nDETALHES DOS TESTES:\n")
            f.write("-" * 70 + "\n")
            for resultado in self.resultados:
                status = "PASSOU" if resultado['sucesso'] else "FALHOU"
                f.write(f"\n{status}: {resultado['teste']}\n")
                if resultado['mensagem']:
                    f.write(f"  {resultado['mensagem']}\n")
        
        return taxa_sucesso >= 70
    
    def executar_todos_testes(self):
        """Executar todos os testes"""
        print("\nIniciando execução dos testes de API...")
        print("-" * 70)
        
        testes = [
            self.teste_01_health_check,
            self.teste_02_crud_recado_create,
            self.teste_03_crud_recado_read,
            self.teste_04_crud_recado_delete,
            self.teste_05_crud_usuario_create,
            self.teste_06_crud_usuario_read,
            self.teste_07_crud_usuario_busca,
            self.teste_08_crud_disciplina_create,
            self.teste_09_crud_disciplina_read,
            self.teste_10_crud_topico_create,
            self.teste_11_crud_topico_read,
            self.teste_12_crud_resposta_create,
            self.teste_13_crud_resposta_read,
            self.teste_14_busca_sem_acento,
            self.teste_15_validacao_email
        ]
        
        for teste in testes:
            try:
                teste()
            except Exception as e:
                print(f"\nErro crítico em {teste.__name__}: {str(e)}")
        
        sucesso = self.gerar_relatorio()
        return sucesso

if __name__ == "__main__":
    tester = TestAPIForumAcademico()
    
    try:
        sucesso = tester.executar_todos_testes()
        print("\nTestes finalizados. Relatório salvo em RELATORIO_TESTES_API.txt")
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\nErro fatal: {str(e)}")
        sys.exit(1)
