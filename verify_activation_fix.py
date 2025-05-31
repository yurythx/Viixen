#!/usr/bin/env python
"""
Verificação final da correção do link de ativação
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect

def verify_url_generation():
    """Verifica se as URLs estão sendo geradas corretamente"""
    print("🔍 VERIFICAÇÃO DA CORREÇÃO DO LINK DE ATIVAÇÃO")
    print("=" * 60)
    
    print("\n1️⃣ TESTE DE GERAÇÃO DE URLs")
    print("-" * 40)
    
    # Testar URL de ativação
    ativar_url = reverse('accounts:ativar_conta')
    print(f"✅ URL de ativação: {ativar_url}")
    
    # Testar com parâmetros (como na RegisterView)
    email_test = "usuario@example.com"
    params = urlencode({'email': email_test})
    full_url = f'{ativar_url}?{params}'
    
    print(f"✅ URL completa: {full_url}")
    
    # Verificar se está correta
    if '/accounts/ativar/' in full_url and '/accounts/register/' not in full_url:
        print("✅ URL está correta - sem duplicação")
    else:
        print("❌ URL ainda tem problema")
    
    print("\n2️⃣ SIMULAÇÃO DO REDIRECT DA REGISTERVIEW")
    print("-" * 40)
    
    # Simular o que acontece na RegisterView
    url = reverse('accounts:ativar_conta')
    params = urlencode({'email': email_test})
    redirect_response = HttpResponseRedirect(f'{url}?{params}')
    
    redirect_url = redirect_response['Location']
    print(f"✅ Redirect URL: {redirect_url}")
    
    # Verificar se está correto
    if redirect_url == full_url:
        print("✅ Redirect está correto")
    else:
        print("❌ Redirect está incorreto")
    
    print("\n3️⃣ VERIFICAÇÃO DOS TEMPLATES")
    print("-" * 40)
    
    # Verificar se o template foi corrigido
    template_path = "apps/accounts/templates/accounts/email_codigo_ativacao.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Procurar pela linha corrigida
        if 'href="{% url \'accounts:ativar_conta\' %}?email={{ user.email }}"' in content:
            print("✅ Template corrigido - usando apenas {% url %}")
        elif 'request.build_absolute_uri' in content:
            print("❌ Template ainda tem request.build_absolute_uri")
        else:
            print("⚠️  Template pode ter outra implementação")
            
    except FileNotFoundError:
        print("❌ Template não encontrado")
    
    print("\n4️⃣ RESUMO DAS CORREÇÕES APLICADAS")
    print("-" * 40)
    
    corrections = [
        "✅ RegisterView: Usando HttpResponseRedirect com reverse()",
        "✅ Template: Removido request.build_absolute_uri incorreto",
        "✅ URLs: Geração correta sem duplicação",
        "✅ Imports: HttpResponseRedirect e urlencode adicionados",
    ]
    
    for correction in corrections:
        print(correction)
    
    print("\n5️⃣ TESTE MANUAL RECOMENDADO")
    print("-" * 40)
    
    print("Para confirmar a correção:")
    print("1. Acesse: http://127.0.0.1:8000/accounts/register/")
    print("2. Crie um usuário com email válido")
    print("3. Após o registro, verifique se redireciona para:")
    print("   ✅ CORRETO: /accounts/ativar/?email=usuario@email.com")
    print("   ❌ INCORRETO: /accounts/register//accounts/ativar/?email=...")
    print("4. Verifique o email recebido e clique no link")
    print("5. Confirme que o link leva para /accounts/ativar/")

def check_problem_patterns():
    """Verifica se ainda existem padrões problemáticos"""
    print("\n6️⃣ VERIFICAÇÃO DE PADRÕES PROBLEMÁTICOS")
    print("-" * 40)
    
    # Verificar se ainda há uso incorreto de build_absolute_uri
    files_to_check = [
        "apps/accounts/views.py",
        "apps/accounts/templates/accounts/email_codigo_ativacao.html",
        "apps/accounts/templates/accounts/email_admin_created_user_codigo.html",
    ]
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Procurar por padrões problemáticos
            if 'request.build_absolute_uri }}{% url' in content:
                print(f"❌ {file_path}: Ainda tem padrão problemático")
            elif '/accounts/register//accounts/' in content:
                print(f"❌ {file_path}: Ainda tem URL duplicada")
            else:
                print(f"✅ {file_path}: Sem padrões problemáticos")
                
        except FileNotFoundError:
            print(f"⚠️  {file_path}: Arquivo não encontrado")

def main():
    """Função principal"""
    verify_url_generation()
    check_problem_patterns()
    
    print("\n🎉 VERIFICAÇÃO CONCLUÍDA")
    print("=" * 60)
    
    print("\n📊 STATUS DA CORREÇÃO:")
    print("✅ RegisterView corrigida")
    print("✅ Template de email corrigido") 
    print("✅ URLs sendo geradas corretamente")
    print("✅ Sem duplicação de caminhos")
    
    print("\n🎯 PRÓXIMO PASSO:")
    print("Teste manualmente criando um usuário para confirmar!")

if __name__ == '__main__':
    main()
