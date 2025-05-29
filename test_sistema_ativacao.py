#!/usr/bin/env python
"""
Script de Testes Completos para o Sistema de Ativação por Código
================================================================

Este script testa todas as funcionalidades do novo sistema de ativação:
- Geração de códigos
- Validação de códigos
- Expiração de códigos
- Limite de tentativas
- Solicitação de novos códigos
- Integração com views
- Formulários
- Templates
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Configurar ALLOWED_HOSTS para testes
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import Group
from apps.accounts.forms import CodigoAtivacaoForm, SolicitarCodigoForm
import time

User = get_user_model()

class TesteSistemaAtivacao:
    """Classe principal de testes do sistema de ativação"""

    def __init__(self):
        self.client = Client()
        self.resultados = []
        self.total_testes = 0
        self.testes_passaram = 0

    def log_resultado(self, teste, passou, detalhes=""):
        """Registrar resultado de um teste"""
        self.total_testes += 1
        if passou:
            self.testes_passaram += 1
            status = "✅ PASSOU"
        else:
            status = "❌ FALHOU"

        resultado = f"{status} - {teste}"
        if detalhes:
            resultado += f" | {detalhes}"

        self.resultados.append(resultado)
        print(resultado)

    def setup_test_data(self):
        """Configurar dados de teste"""
        print("\n🔧 Configurando dados de teste...")

        # Limpar usuários de teste existentes
        User.objects.filter(email__contains='teste').delete()

        # Criar grupo Usuario se não existir
        Group.objects.get_or_create(name='Usuario')

        print("✅ Dados de teste configurados")

    def teste_1_geracao_codigo(self):
        """Teste 1: Geração de código de ativação"""
        print("\n📝 Teste 1: Geração de código de ativação")

        try:
            # Criar usuário de teste
            user = User.objects.create_user(
                username='teste_geracao',
                email='teste_geracao@example.com',
                password='senha123',
                is_active=False
            )

            # Gerar código
            codigo = user.gerar_codigo_ativacao()

            # Verificações
            passou = True
            detalhes = []

            if not codigo:
                passou = False
                detalhes.append("Código não foi gerado")

            if len(codigo) != 6:
                passou = False
                detalhes.append(f"Código tem {len(codigo)} dígitos, esperado 6")

            if not codigo.isdigit():
                passou = False
                detalhes.append("Código contém caracteres não numéricos")

            if not user.codigo_ativacao_criado_em:
                passou = False
                detalhes.append("Data de criação não foi definida")

            if user.tentativas_codigo != 0:
                passou = False
                detalhes.append(f"Tentativas = {user.tentativas_codigo}, esperado 0")

            self.log_resultado(
                "Geração de código",
                passou,
                f"Código: {codigo}" if passou else "; ".join(detalhes)
            )

        except Exception as e:
            self.log_resultado("Geração de código", False, f"Erro: {str(e)}")

    def teste_2_validacao_codigo(self):
        """Teste 2: Validação de código correto"""
        print("\n📝 Teste 2: Validação de código correto")

        try:
            user = User.objects.create_user(
                username='teste_validacao',
                email='teste_validacao@example.com',
                password='senha123',
                is_active=False
            )

            codigo = user.gerar_codigo_ativacao()
            valido, mensagem = user.verificar_codigo_ativacao(codigo)

            passou = valido and "válido" in mensagem.lower()

            self.log_resultado(
                "Validação código correto",
                passou,
                f"Mensagem: {mensagem}"
            )

        except Exception as e:
            self.log_resultado("Validação código correto", False, f"Erro: {str(e)}")

    def teste_3_codigo_incorreto(self):
        """Teste 3: Validação de código incorreto"""
        print("\n📝 Teste 3: Validação de código incorreto")

        try:
            user = User.objects.create_user(
                username='teste_incorreto',
                email='teste_incorreto@example.com',
                password='senha123',
                is_active=False
            )

            user.gerar_codigo_ativacao()
            valido, mensagem = user.verificar_codigo_ativacao("000000")

            passou = not valido and "incorreto" in mensagem.lower()

            self.log_resultado(
                "Validação código incorreto",
                passou,
                f"Mensagem: {mensagem}"
            )

        except Exception as e:
            self.log_resultado("Validação código incorreto", False, f"Erro: {str(e)}")

    def teste_4_limite_tentativas(self):
        """Teste 4: Limite de tentativas"""
        print("\n📝 Teste 4: Limite de tentativas")

        try:
            user = User.objects.create_user(
                username='teste_tentativas',
                email='teste_tentativas@example.com',
                password='senha123',
                is_active=False
            )

            user.gerar_codigo_ativacao()

            # Fazer 5 tentativas incorretas
            for i in range(5):
                valido, mensagem = user.verificar_codigo_ativacao("000000")

            # 6ª tentativa deve ser bloqueada
            valido, mensagem = user.verificar_codigo_ativacao("000000")

            passou = not valido and "muitas tentativas" in mensagem.lower()

            self.log_resultado(
                "Limite de tentativas",
                passou,
                f"Tentativas: {user.tentativas_codigo}, Mensagem: {mensagem}"
            )

        except Exception as e:
            self.log_resultado("Limite de tentativas", False, f"Erro: {str(e)}")

    def teste_5_expiracao_codigo(self):
        """Teste 5: Expiração de código"""
        print("\n📝 Teste 5: Expiração de código")

        try:
            user = User.objects.create_user(
                username='teste_expiracao',
                email='teste_expiracao@example.com',
                password='senha123',
                is_active=False
            )

            codigo = user.gerar_codigo_ativacao()

            # Simular código expirado (31 minutos atrás)
            user.codigo_ativacao_criado_em = timezone.now() - timedelta(minutes=31)
            user.save()

            valido, mensagem = user.verificar_codigo_ativacao(codigo)

            passou = not valido and "expirado" in mensagem.lower()

            self.log_resultado(
                "Expiração de código",
                passou,
                f"Mensagem: {mensagem}"
            )

        except Exception as e:
            self.log_resultado("Expiração de código", False, f"Erro: {str(e)}")

    def teste_6_formulario_codigo(self):
        """Teste 6: Formulário de código de ativação"""
        print("\n📝 Teste 6: Formulário de código de ativação")

        try:
            # Teste com dados válidos
            form_data = {
                'codigo': '123456',
                'email': 'teste@example.com'
            }
            form = CodigoAtivacaoForm(data=form_data)

            passou = form.is_valid()
            detalhes = []

            if not passou:
                detalhes = [f"{field}: {errors}" for field, errors in form.errors.items()]

            # Teste com código inválido
            form_data_invalido = {
                'codigo': '12345a',  # Contém letra
                'email': 'teste@example.com'
            }
            form_invalido = CodigoAtivacaoForm(data=form_data_invalido)

            passou_invalido = not form_invalido.is_valid()

            passou_final = passou and passou_invalido

            self.log_resultado(
                "Formulário código ativação",
                passou_final,
                "; ".join(detalhes) if detalhes else "Validações OK"
            )

        except Exception as e:
            self.log_resultado("Formulário código ativação", False, f"Erro: {str(e)}")

    def teste_7_formulario_solicitar(self):
        """Teste 7: Formulário de solicitar novo código"""
        print("\n📝 Teste 7: Formulário de solicitar novo código")

        try:
            # Criar usuário inativo
            user = User.objects.create_user(
                username='teste_solicitar',
                email='teste_solicitar@example.com',
                password='senha123',
                is_active=False
            )

            # Teste com email válido (usuário inativo existe)
            form_data = {
                'email': 'teste_solicitar@example.com'
            }
            form = SolicitarCodigoForm(data=form_data)

            passou = form.is_valid()

            # Teste com email que não existe
            form_data_inexistente = {
                'email': 'naoexiste@example.com'
            }
            form_inexistente = SolicitarCodigoForm(data=form_data_inexistente)

            passou_inexistente = not form_inexistente.is_valid()

            passou_final = passou and passou_inexistente

            self.log_resultado(
                "Formulário solicitar código",
                passou_final,
                "Validações OK" if passou_final else "Falha na validação"
            )

        except Exception as e:
            self.log_resultado("Formulário solicitar código", False, f"Erro: {str(e)}")

    def teste_8_view_ativacao(self):
        """Teste 8: View de ativação"""
        print("\n📝 Teste 8: View de ativação")

        try:
            # Criar usuário inativo
            user = User.objects.create_user(
                username='teste_view',
                email='teste_view@example.com',
                password='senha123',
                is_active=False
            )

            codigo = user.gerar_codigo_ativacao()

            # Teste GET - deve retornar página
            response = self.client.get(reverse('accounts:ativar_conta'))
            passou_get = response.status_code == 200

            # Teste POST com código correto
            response = self.client.post(reverse('accounts:ativar_conta'), {
                'email': 'teste_view@example.com',
                'codigo': codigo
            })

            # Verificar se usuário foi ativado
            user.refresh_from_db()
            passou_post = user.is_active and user.email_verificado

            passou_final = passou_get and passou_post

            self.log_resultado(
                "View de ativação",
                passou_final,
                f"GET: {response.status_code}, Ativado: {user.is_active}"
            )

        except Exception as e:
            self.log_resultado("View de ativação", False, f"Erro: {str(e)}")

    def teste_9_registro_publico(self):
        """Teste 9: Registro público com código"""
        print("\n📝 Teste 9: Registro público com código")

        try:
            # Limpar emails anteriores
            mail.outbox = []

            # Registrar novo usuário
            response = self.client.post(reverse('accounts:register'), {
                'username': 'teste_registro',
                'email': 'teste_registro@example.com',
                'password1': 'senha123456',
                'password2': 'senha123456'
            })

            # Verificar se usuário foi criado inativo
            user = User.objects.get(email='teste_registro@example.com')
            passou_criacao = not user.is_active and user.codigo_ativacao

            # Verificar se email foi enviado
            passou_email = len(mail.outbox) > 0

            passou_final = passou_criacao and passou_email

            self.log_resultado(
                "Registro público",
                passou_final,
                f"Usuário inativo: {not user.is_active}, Email enviado: {passou_email}"
            )

        except Exception as e:
            self.log_resultado("Registro público", False, f"Erro: {str(e)}")

    def teste_10_limite_tempo_novo_codigo(self):
        """Teste 10: Limite de tempo para novo código"""
        print("\n📝 Teste 10: Limite de tempo para novo código")

        try:
            user = User.objects.create_user(
                username='teste_limite_tempo',
                email='teste_limite_tempo@example.com',
                password='senha123',
                is_active=False
            )

            # Gerar primeiro código
            user.gerar_codigo_ativacao()

            # Tentar gerar novo código imediatamente (deve falhar)
            response = self.client.post(reverse('accounts:solicitar_codigo'), {
                'email': 'teste_limite_tempo@example.com'
            })

            # Verificar se foi redirecionado (limite de tempo)
            passou = response.status_code == 302

            self.log_resultado(
                "Limite tempo novo código",
                passou,
                f"Status: {response.status_code}"
            )

        except Exception as e:
            self.log_resultado("Limite tempo novo código", False, f"Erro: {str(e)}")

    def executar_todos_testes(self):
        """Executar todos os testes"""
        print("🚀 INICIANDO TESTES DO SISTEMA DE ATIVAÇÃO POR CÓDIGO")
        print("=" * 60)

        self.setup_test_data()

        # Executar testes
        self.teste_1_geracao_codigo()
        self.teste_2_validacao_codigo()
        self.teste_3_codigo_incorreto()
        self.teste_4_limite_tentativas()
        self.teste_5_expiracao_codigo()
        self.teste_6_formulario_codigo()
        self.teste_7_formulario_solicitar()
        self.teste_8_view_ativacao()
        self.teste_9_registro_publico()
        self.teste_10_limite_tempo_novo_codigo()

        # Relatório final
        self.gerar_relatorio()

    def gerar_relatorio(self):
        """Gerar relatório final dos testes"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print("=" * 60)

        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   Total de testes: {self.total_testes}")
        print(f"   Testes que passaram: {self.testes_passaram}")
        print(f"   Testes que falharam: {self.total_testes - self.testes_passaram}")
        print(f"   Taxa de sucesso: {(self.testes_passaram/self.total_testes)*100:.1f}%")

        print(f"\n📋 RESULTADOS DETALHADOS:")
        for resultado in self.resultados:
            print(f"   {resultado}")

        if self.testes_passaram == self.total_testes:
            print(f"\n🎉 TODOS OS TESTES PASSARAM! Sistema funcionando perfeitamente.")
        else:
            print(f"\n⚠️  ALGUNS TESTES FALHARAM. Verifique os detalhes acima.")

        print("=" * 60)

if __name__ == "__main__":
    teste = TesteSistemaAtivacao()
    teste.executar_todos_testes()
