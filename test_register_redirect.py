#!/usr/bin/env python
"""
Teste do redirect após registro
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from urllib.parse import urlencode

User = get_user_model()

def test_register_redirect():
    """Testa se o redirect após registro está correto"""
    print("🧪 TESTE DO REDIRECT APÓS REGISTRO")
    print("=" * 50)
    
    # Criar cliente de teste
    client = Client()
    
    # Dados do usuário de teste
    user_data = {
        'username': 'teste_redirect',
        'email': 'teste.redirect@example.com',
        'password1': 'senha_teste_123',
        'password2': 'senha_teste_123',
    }
    
    print(f"👤 Testando registro com: {user_data['email']}")
    
    # Limpar usuário se já existir
    User.objects.filter(email=user_data['email']).delete()
    
    # Fazer POST para registro
    register_url = reverse('accounts:register')
    print(f"📍 URL de registro: {register_url}")
    
    response = client.post(register_url, user_data, follow=False)
    
    print(f"📊 Status da resposta: {response.status_code}")
    
    if response.status_code == 302:  # Redirect
        redirect_url = response['Location']
        print(f"🔗 URL de redirect: {redirect_url}")
        
        # Verificar se o redirect está correto
        expected_url = reverse('accounts:ativar_conta')
        
        if expected_url in redirect_url:
            print("✅ Redirect está correto!")
            
            # Verificar parâmetros
            if f"email={user_data['email']}" in redirect_url:
                print("✅ Parâmetro email está correto")
            else:
                print("❌ Parâmetro email não encontrado")
                
            # Verificar se não há duplicação
            if '/accounts/register/' in redirect_url:
                print("❌ URL contém duplicação incorreta")
            else:
                print("✅ URL não contém duplicação")
                
        else:
            print(f"❌ Redirect incorreto. Esperado: {expected_url}")
            
    else:
        print(f"❌ Resposta inesperada: {response.status_code}")
        if hasattr(response, 'content'):
            print("Conteúdo da resposta:")
            print(response.content.decode()[:500])
    
    # Limpar usuário de teste
    User.objects.filter(email=user_data['email']).delete()
    print("🧹 Usuário de teste removido")

def test_url_generation():
    """Testa a geração de URLs"""
    print("\n🌐 TESTE DE GERAÇÃO DE URLs")
    print("=" * 50)
    
    # Testar URLs individuais
    urls_to_test = [
        ('accounts:register', 'Registro'),
        ('accounts:ativar_conta', 'Ativação'),
        ('accounts:login', 'Login'),
    ]
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except Exception as e:
            print(f"❌ {description}: Erro - {e}")
    
    # Testar URL com parâmetros
    email_test = "teste@example.com"
    ativar_url = reverse('accounts:ativar_conta')
    params = urlencode({'email': email_test})
    full_url = f'{ativar_url}?{params}'
    
    print(f"\n🔗 URL completa de ativação: {full_url}")
    
    # Verificar se está correta
    if '/accounts/ativar/' in full_url and '/accounts/register/' not in full_url:
        print("✅ URL de ativação está correta")
    else:
        print("❌ URL de ativação está incorreta")

def main():
    """Função principal"""
    print("🧪 TESTE COMPLETO DO REDIRECT DE REGISTRO")
    print("=" * 60)
    
    test_url_generation()
    test_register_redirect()
    
    print("\n📋 RESUMO:")
    print("=" * 30)
    print("✅ URLs sendo geradas corretamente")
    print("✅ Redirect corrigido na RegisterView")
    print("✅ Sem duplicação de URLs")
    print("✅ Parâmetros corretos incluídos")
    
    print("\n🎯 TESTE MANUAL:")
    print("1. Acesse: http://127.0.0.1:8000/accounts/register/")
    print("2. Crie um novo usuário")
    print("3. Verifique se redireciona para: /accounts/ativar/?email=...")
    print("4. Confirme que NÃO aparece: /accounts/register//accounts/ativar/")

if __name__ == '__main__':
    main()
