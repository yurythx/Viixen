#!/usr/bin/env python
"""
Script para configurar senha de app do Gmail
Execute este script após gerar uma senha de app no Gmail
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.config.models import EmailConfig
from apps.config.email_utils import test_email_connection, send_test_email

def configure_gmail_app_password():
    """Configura senha de app do Gmail"""
    print("🔑 CONFIGURAÇÃO DE SENHA DE APP - GMAIL")
    print("=" * 60)
    print("📧 Email: projetohavoc@gmail.com")
    print("=" * 60)
    
    print("\n📋 PASSOS PARA GERAR SENHA DE APP:")
    print("1. Acesse: https://myaccount.google.com/apppasswords")
    print("2. Faça login com projetohavoc@gmail.com")
    print("3. Selecione 'Email' como aplicativo")
    print("4. Selecione 'Outro' como dispositivo")
    print("5. Digite 'Viixen System' como nome")
    print("6. Clique em 'Gerar'")
    print("7. Copie a senha de 16 caracteres gerada")
    
    print("\n⚠️  IMPORTANTE:")
    print("- A verificação em 2 etapas deve estar ATIVADA")
    print("- Use a senha de app, NÃO a senha normal da conta")
    print("- A senha de app tem formato: xxxx xxxx xxxx xxxx")
    
    # Obter configuração existente
    try:
        config = EmailConfig.objects.get(slug='gmail-config')
        print(f"\n✅ Configuração encontrada: {config.email_host_user}")
    except EmailConfig.DoesNotExist:
        print("\n❌ Configuração Gmail não encontrada!")
        return
    
    # Solicitar senha de app
    print("\n🔑 Digite a senha de app do Gmail:")
    print("(Formato: xxxx xxxx xxxx xxxx ou xxxxxxxxxxxxxxxx)")
    app_password = input("Senha de app: ").strip()
    
    if not app_password:
        print("❌ Senha não fornecida!")
        return
    
    # Remover espaços da senha de app
    app_password = app_password.replace(' ', '')
    
    if len(app_password) != 16:
        print(f"⚠️  Aviso: Senha tem {len(app_password)} caracteres (esperado: 16)")
    
    # Configurar senha
    config.set_password(app_password)
    config.save()
    
    print("✅ Senha de app configurada!")
    
    # Testar conexão
    print("\n🔌 TESTANDO CONEXÃO COM SENHA DE APP...")
    success, message = test_email_connection(config)
    
    if success:
        print(f"✅ Conexão OK: {message}")
        
        # Enviar email de teste
        print("\n📤 ENVIANDO EMAIL DE TESTE...")
        test_success, test_message = send_test_email('yurymenezes@hotmail.com', config)
        
        if test_success:
            print(f"✅ {test_message}")
            print("\n🎉 GMAIL CONFIGURADO COM SUCESSO!")
            print("Agora você pode usar a interface web para enviar emails.")
        else:
            print(f"❌ Erro no teste: {test_message}")
    else:
        print(f"❌ Erro na conexão: {message}")
        print("\n🔧 POSSÍVEIS SOLUÇÕES:")
        print("1. Verifique se a senha de app está correta")
        print("2. Confirme que a verificação em 2 etapas está ativa")
        print("3. Tente gerar uma nova senha de app")
        print("4. Verifique se o Gmail não está bloqueando o acesso")

def test_existing_config():
    """Testa configuração existente"""
    print("\n🧪 TESTANDO CONFIGURAÇÃO EXISTENTE")
    print("=" * 50)
    
    try:
        config = EmailConfig.objects.get(slug='gmail-config')
        
        print(f"📧 Email: {config.email_host_user}")
        print(f"🔒 Senha configurada: {'Sim' if config.get_password() else 'Não'}")
        
        if config.get_password():
            print("\n🔌 Testando conexão...")
            success, message = test_email_connection(config)
            
            if success:
                print(f"✅ {message}")
                
                # Perguntar se quer enviar teste
                send_test = input("\n📤 Enviar email de teste? (s/n): ").lower().strip()
                if send_test in ['s', 'sim', 'y', 'yes']:
                    test_success, test_message = send_test_email('yurymenezes@hotmail.com', config)
                    if test_success:
                        print(f"✅ {test_message}")
                    else:
                        print(f"❌ {test_message}")
            else:
                print(f"❌ {message}")
        else:
            print("❌ Senha não configurada")
            
    except EmailConfig.DoesNotExist:
        print("❌ Configuração Gmail não encontrada")

def show_current_configs():
    """Mostra todas as configurações de email"""
    print("\n📋 CONFIGURAÇÕES DE EMAIL EXISTENTES")
    print("=" * 50)
    
    configs = EmailConfig.objects.all()
    
    if not configs:
        print("❌ Nenhuma configuração encontrada")
        return
    
    for config in configs:
        print(f"\n📧 {config.slug}")
        print(f"   Host: {config.email_host}:{config.email_port}")
        print(f"   Usuário: {config.email_host_user}")
        print(f"   TLS: {config.email_use_tls}")
        print(f"   Ativo: {config.is_active}")
        print(f"   Senha: {'Configurada' if config.get_password() else 'Não configurada'}")

def main():
    """Menu principal"""
    print("🔧 CONFIGURADOR GMAIL - SISTEMA VIIXEN")
    print("=" * 60)
    
    while True:
        print("\n📋 OPÇÕES:")
        print("1. Configurar senha de app do Gmail")
        print("2. Testar configuração existente")
        print("3. Mostrar todas as configurações")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção (1-4): ").strip()
        
        if choice == '1':
            configure_gmail_app_password()
        elif choice == '2':
            test_existing_config()
        elif choice == '3':
            show_current_configs()
        elif choice == '4':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == '__main__':
    main()
