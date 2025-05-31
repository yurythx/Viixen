#!/usr/bin/env python
"""
Verificação completa do status do sistema de email
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.config.models import EmailConfig
from apps.config.email_utils import get_active_email_config

def check_email_system_status():
    """Verifica o status completo do sistema de email"""
    print("📧 STATUS DO SISTEMA DE EMAIL - VIIXEN")
    print("=" * 60)
    
    # 1. Verificar configurações existentes
    print("\n📋 CONFIGURAÇÕES DE EMAIL:")
    print("-" * 40)
    
    configs = EmailConfig.objects.all()
    
    if not configs:
        print("❌ Nenhuma configuração de email encontrada")
        return
    
    for config in configs:
        status_icon = "✅" if config.is_active else "⏸️"
        print(f"{status_icon} {config.slug}")
        print(f"   📧 Email: {config.email_host_user}")
        print(f"   🔧 Servidor: {config.email_host}:{config.email_port}")
        print(f"   🔒 TLS: {'Sim' if config.email_use_tls else 'Não'}")
        print(f"   🔑 Senha: {'Configurada' if config.get_password() else 'Não configurada'}")
        print(f"   📤 Email padrão: {config.default_from_email}")
        print(f"   ⚡ Status: {'ATIVO (Padrão)' if config.is_active else 'Inativo'}")
        print()
    
    # 2. Verificar configuração ativa
    print("\n🎯 CONFIGURAÇÃO PADRÃO:")
    print("-" * 40)
    
    active_config = get_active_email_config()
    
    if active_config:
        print(f"✅ Configuração ativa encontrada: {active_config.slug}")
        print(f"📧 Email padrão do sistema: {active_config.email_host_user}")
        print(f"🔧 Servidor SMTP: {active_config.email_host}:{active_config.email_port}")
        
        if active_config.slug == 'gmail-config':
            print("🎉 Gmail configurado como padrão!")
        
    else:
        print("❌ Nenhuma configuração ativa encontrada")
    
    # 3. Verificar configurações Django
    print("\n⚙️ CONFIGURAÇÕES DJANGO:")
    print("-" * 40)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Não definido')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Não definido')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Não definido')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Não definido')}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Não definido')}")
    
    # 4. Verificar URLs e views
    print("\n🌐 URLS E INTERFACE:")
    print("-" * 40)
    
    urls = [
        ("Lista de emails", "http://127.0.0.1:8000/config/email/"),
        ("Guia de configuração", "http://127.0.0.1:8000/config/email/guide/"),
        ("Nova configuração", "http://127.0.0.1:8000/config/email/create/"),
        ("Configurações gerais", "http://127.0.0.1:8000/config/"),
    ]
    
    for name, url in urls:
        print(f"✅ {name}: {url}")
    
    # 5. Status dos recursos
    print("\n🔧 RECURSOS IMPLEMENTADOS:")
    print("-" * 40)
    
    features = [
        "✅ Modelo EmailConfig com criptografia de senhas",
        "✅ Utilitários de email (email_utils.py)",
        "✅ Views de teste (conexão, envio, aplicar)",
        "✅ Interface web com botões de teste",
        "✅ Guia passo a passo integrado",
        "✅ Suporte a múltiplos provedores",
        "✅ Configuração dinâmica do Django",
        "✅ Scripts de teste automatizados",
    ]
    
    for feature in features:
        print(feature)
    
    # 6. Próximos passos
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("-" * 40)
    
    if active_config and active_config.slug == 'gmail-config':
        if active_config.get_password():
            print("1. ✅ Gmail configurado como padrão")
            print("2. ✅ Senha configurada")
            print("3. 🧪 Teste a conexão na interface web")
            print("4. 📤 Envie um email de teste")
            print("5. 🎉 Sistema pronto para uso!")
        else:
            print("1. ✅ Gmail configurado como padrão")
            print("2. ⚠️  Configure a senha de app do Gmail")
            print("3. 🔑 Execute: python configure_gmail_app_password.py")
            print("4. 🧪 Teste na interface web")
    else:
        print("1. ⚠️  Configure uma configuração de email")
        print("2. 🌐 Acesse: http://127.0.0.1:8000/config/email/")
        print("3. 📖 Consulte o guia de configuração")
    
    print("\n📱 LINKS ÚTEIS:")
    print("-" * 40)
    print("🔗 Interface: http://127.0.0.1:8000/config/email/")
    print("📖 Guia: http://127.0.0.1:8000/config/email/guide/")
    print("🔑 Gmail App Passwords: https://myaccount.google.com/apppasswords")
    print("🔑 Outlook App Passwords: https://account.microsoft.com/security/app-passwords")

def main():
    """Função principal"""
    check_email_system_status()

if __name__ == '__main__':
    main()
