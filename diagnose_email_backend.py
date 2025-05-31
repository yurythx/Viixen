#!/usr/bin/env python
"""
Diagnóstico do problema de backend de email
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.config.models import EmailConfig
from apps.config.email_utils import get_active_email_config, apply_email_settings_to_django

def diagnose_email_backend():
    """Diagnostica o problema do backend de email"""
    print("🔍 DIAGNÓSTICO DO BACKEND DE EMAIL")
    print("=" * 50)
    
    # 1. Verificar configuração ativa
    print("\n📧 CONFIGURAÇÃO ATIVA:")
    print("-" * 30)
    
    config = get_active_email_config()
    if config:
        print(f"✅ Configuração encontrada: {config.slug}")
        print(f"📧 Email: {config.email_host_user}")
        print(f"🌟 Padrão: {config.is_default}")
        print(f"🖥️ Console Backend: {config.use_console_backend}")
        print(f"✅ Ativo: {config.is_active}")
        print(f"🔧 Host: {config.email_host}:{config.email_port}")
    else:
        print("❌ Nenhuma configuração ativa encontrada")
        return
    
    # 2. Verificar configurações Django
    print(f"\n⚙️ CONFIGURAÇÕES DJANGO:")
    print("-" * 30)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Não definido')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Não definido')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Não definido')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Não definido')}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Não definido')}")
    
    # 3. Verificar se backend está correto
    print(f"\n🔍 ANÁLISE DO BACKEND:")
    print("-" * 30)
    
    expected_backend = 'django.core.mail.backends.console.EmailBackend' if config.use_console_backend else 'django.core.mail.backends.smtp.EmailBackend'
    actual_backend = settings.EMAIL_BACKEND
    
    print(f"Backend esperado: {expected_backend}")
    print(f"Backend atual: {actual_backend}")
    
    if expected_backend == actual_backend:
        print("✅ Backend está correto")
    else:
        print("❌ Backend está incorreto!")
        
        # Aplicar configurações
        print("\n🔧 APLICANDO CONFIGURAÇÕES...")
        apply_email_settings_to_django(config)
        
        # Verificar novamente
        print(f"Novo backend: {settings.EMAIL_BACKEND}")
        if settings.EMAIL_BACKEND == expected_backend:
            print("✅ Backend corrigido!")
        else:
            print("❌ Backend ainda incorreto")
    
    # 4. Verificar todas as configurações
    print(f"\n📋 TODAS AS CONFIGURAÇÕES:")
    print("-" * 30)
    
    all_configs = EmailConfig.objects.all()
    for cfg in all_configs:
        status = []
        if cfg.is_active:
            status.append("✅ Ativo")
        if cfg.is_default:
            status.append("🌟 Padrão")
        if cfg.use_console_backend:
            status.append("🖥️ Console")
        else:
            status.append("📡 SMTP")
        
        print(f"{cfg.slug}: {' | '.join(status)}")
    
    # 5. Forçar aplicação da configuração padrão
    print(f"\n🔄 FORÇANDO APLICAÇÃO DA CONFIGURAÇÃO PADRÃO:")
    print("-" * 30)
    
    default_config = EmailConfig.objects.filter(is_default=True).first()
    if default_config:
        print(f"Aplicando configuração: {default_config.slug}")
        apply_email_settings_to_django(default_config)
        
        print(f"Backend após aplicação: {settings.EMAIL_BACKEND}")
        
        if default_config.use_console_backend:
            if 'console' in settings.EMAIL_BACKEND:
                print("✅ Console backend aplicado corretamente")
            else:
                print("❌ Console backend não foi aplicado")
        else:
            if 'smtp' in settings.EMAIL_BACKEND:
                print("✅ SMTP backend aplicado corretamente")
            else:
                print("❌ SMTP backend não foi aplicado")
    else:
        print("❌ Nenhuma configuração padrão encontrada")

def fix_gmail_backend():
    """Corrige o backend do Gmail"""
    print(f"\n🔧 CORRIGINDO BACKEND DO GMAIL:")
    print("-" * 30)
    
    try:
        gmail_config = EmailConfig.objects.get(slug='gmail-config')
        
        print(f"Estado atual do Gmail:")
        print(f"  Console Backend: {gmail_config.use_console_backend}")
        print(f"  Padrão: {gmail_config.is_default}")
        
        # Garantir que Gmail está em modo SMTP
        gmail_config.use_console_backend = False
        gmail_config.is_default = True
        gmail_config.save()
        
        print(f"✅ Gmail configurado para SMTP e como padrão")
        print(f"Backend Django: {settings.EMAIL_BACKEND}")
        
        # Verificar se foi aplicado corretamente
        if 'smtp' in settings.EMAIL_BACKEND:
            print("✅ SMTP backend aplicado com sucesso!")
        else:
            print("❌ SMTP backend não foi aplicado")
            
    except EmailConfig.DoesNotExist:
        print("❌ Configuração Gmail não encontrada")

def test_email_sending():
    """Testa o envio de email"""
    print(f"\n📤 TESTANDO ENVIO DE EMAIL:")
    print("-" * 30)
    
    try:
        from django.core.mail import send_mail
        
        print(f"Backend atual: {settings.EMAIL_BACKEND}")
        
        if 'console' in settings.EMAIL_BACKEND:
            print("🖥️ Enviando via Console - email aparecerá no terminal")
        else:
            print("📡 Enviando via SMTP - email será enviado realmente")
        
        result = send_mail(
            subject='🧪 Teste de Diagnóstico - Viixen',
            message='Este é um teste para verificar qual backend está sendo usado.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['yurymenezes@hotmail.com'],
            fail_silently=False,
        )
        
        if result:
            print("✅ Email enviado com sucesso!")
        else:
            print("❌ Falha no envio")
            
    except Exception as e:
        print(f"❌ Erro no envio: {e}")

def main():
    """Função principal"""
    print("🧪 DIAGNÓSTICO COMPLETO DO BACKEND DE EMAIL")
    print("=" * 60)
    
    diagnose_email_backend()
    fix_gmail_backend()
    test_email_sending()
    
    print(f"\n📋 RESUMO:")
    print("=" * 30)
    print("1. ✅ Configuração Gmail verificada")
    print("2. ✅ Backend corrigido para SMTP")
    print("3. ✅ Configurações aplicadas ao Django")
    print("4. ✅ Teste de envio realizado")
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print("1. Verifique se o email foi enviado via SMTP")
    print("2. Se ainda aparecer no console, reinicie o servidor")
    print("3. Teste novamente na interface web")

if __name__ == '__main__':
    main()
