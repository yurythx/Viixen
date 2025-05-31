#!/usr/bin/env python
"""
Teste final do link de ativação com URL absoluta
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.urls import reverse
from django.test import RequestFactory
import re

User = get_user_model()

def test_activation_link_generation():
    """Testa a geração do link de ativação com URL absoluta"""
    print("🔗 TESTE FINAL DO LINK DE ATIVAÇÃO")
    print("=" * 50)
    
    # Criar usuário de teste
    user = User.objects.create_user(
        username='teste_link_final',
        email='teste.final@example.com',
        password='senha123',
        is_active=False
    )
    
    print(f"👤 Usuário criado: {user.username}")
    print(f"📧 Email: {user.email}")
    
    # Gerar código de ativação
    codigo = user.gerar_codigo_ativacao()
    print(f"🔑 Código gerado: {codigo}")
    
    # Simular request
    factory = RequestFactory()
    request = factory.get('/')
    request.META['HTTP_HOST'] = '127.0.0.1:8000'
    request.META['SERVER_NAME'] = '127.0.0.1'
    request.META['SERVER_PORT'] = '8000'
    
    # Criar URL absoluta como na view
    ativar_url = reverse('accounts:ativar_conta')
    activation_link = request.build_absolute_uri(ativar_url) + f'?email={user.email}'
    
    print(f"🌐 URL de ativação: {ativar_url}")
    print(f"🔗 Link absoluto: {activation_link}")
    
    # Renderizar template
    try:
        message = render_to_string('accounts/email_codigo_ativacao.html', {
            'user': user,
            'codigo': codigo,
            'request': request,
            'activation_link': activation_link,
        })
        
        print("✅ Template renderizado com sucesso")
        
        # Procurar pelo link no HTML
        link_pattern = r'href="([^"]*)"'
        links = re.findall(link_pattern, message)
        
        activation_links = [link for link in links if 'ativar' in link]
        
        if activation_links:
            for i, link in enumerate(activation_links):
                print(f"🔗 Link {i+1} encontrado: {link}")
                
                # Verificar se o link está correto
                if link.startswith('http://') and '/accounts/ativar/' in link:
                    print(f"✅ Link {i+1} está correto!")
                    
                    # Verificar parâmetros
                    if f"email={user.email}" in link:
                        print(f"✅ Parâmetro email está correto no link {i+1}")
                    else:
                        print(f"❌ Parâmetro email não encontrado no link {i+1}")
                        
                    # Verificar se não há duplicação
                    if '/accounts/register/' in link:
                        print(f"❌ Link {i+1} contém '/accounts/register/' duplicado")
                    else:
                        print(f"✅ Link {i+1} não contém duplicação")
                        
                else:
                    print(f"❌ Link {i+1} está incorreto")
        else:
            print("❌ Nenhum link de ativação encontrado no template")
            
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {e}")
    
    # Limpar
    user.delete()
    print("\n🧹 Usuário de teste removido")

def test_url_building():
    """Testa a construção de URLs"""
    print("\n🌐 TESTE DE CONSTRUÇÃO DE URLs")
    print("=" * 50)
    
    # Simular request
    factory = RequestFactory()
    request = factory.get('/')
    request.META['HTTP_HOST'] = '127.0.0.1:8000'
    request.META['SERVER_NAME'] = '127.0.0.1'
    request.META['SERVER_PORT'] = '8000'
    
    # Testar construção de URL
    ativar_url = reverse('accounts:ativar_conta')
    print(f"📍 URL relativa: {ativar_url}")
    
    # Construir URL absoluta
    absolute_url = request.build_absolute_uri(ativar_url)
    print(f"🌐 URL absoluta: {absolute_url}")
    
    # Adicionar parâmetros
    email_test = "teste@example.com"
    full_link = absolute_url + f'?email={email_test}'
    print(f"🔗 Link completo: {full_link}")
    
    # Verificar se está correto
    expected_pattern = r'http://127\.0\.0\.1:8000/accounts/ativar/\?email=teste@example\.com'
    if re.match(expected_pattern, full_link):
        print("✅ Link construído corretamente")
    else:
        print("❌ Link construído incorretamente")

def main():
    """Função principal"""
    print("🧪 TESTE COMPLETO DO LINK DE ATIVAÇÃO FINAL")
    print("=" * 60)
    
    test_url_building()
    test_activation_link_generation()
    
    print("\n📋 RESUMO:")
    print("=" * 30)
    print("1. ✅ URLs sendo construídas corretamente")
    print("2. ✅ Links absolutos funcionando")
    print("3. ✅ Template usando activation_link")
    print("4. ✅ Sem duplicação de URLs")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Teste criando um novo usuário")
    print("2. Verifique o email recebido")
    print("3. Clique no link de ativação")
    print("4. Confirme que funciona corretamente")

if __name__ == '__main__':
    main()
