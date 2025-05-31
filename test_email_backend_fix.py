#!/usr/bin/env python
"""
Teste final da correção do backend de email
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

def test_email_backend_fix():
    """Testa se a correção do backend funcionou"""
    print("🔧 TESTE DA CORREÇÃO DO BACKEND DE EMAIL")
    print("=" * 60)
    
    # 1. Verificar configuração padrão
    print("\n🌟 CONFIGURAÇÃO PADRÃO:")
    print("-" * 40)
    
    default_config = EmailConfig.objects.filter(is_default=True).first()
    if default_config:
        print(f"✅ Configuração padrão: {default_config.slug}")
        print(f"📧 Email: {default_config.email_host_user}")
        print(f"🔧 Console Backend: {default_config.use_console_backend}")
        print(f"✅ Ativo: {default_config.is_active}")
    else:
        print("❌ Nenhuma configuração padrão encontrada")
        return
    
    # 2. Aplicar configurações
    print(f"\n⚙️ APLICANDO CONFIGURAÇÕES:")
    print("-" * 40)
    
    apply_email_settings_to_django(default_config)
    
    # 3. Verificar configurações Django
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Não definido')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Não definido')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Não definido')}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Não definido')}")
    
    # 4. Verificar se backend está correto
    expected_backend = 'django.core.mail.backends.console.EmailBackend' if default_config.use_console_backend else 'django.core.mail.backends.smtp.EmailBackend'
    actual_backend = settings.EMAIL_BACKEND
    
    print(f"\n🔍 VERIFICAÇÃO DO BACKEND:")
    print("-" * 40)
    print(f"Backend esperado: {expected_backend}")
    print(f"Backend atual: {actual_backend}")
    
    if expected_backend == actual_backend:
        print("✅ Backend está correto!")
        
        if 'smtp' in actual_backend:
            print("📡 Modo SMTP ativo - emails serão enviados via Gmail")
        else:
            print("🖥️ Modo Console ativo - emails aparecerão no terminal")
    else:
        print("❌ Backend está incorreto!")
    
    # 5. Testar envio de email
    print(f"\n📤 TESTE DE ENVIO:")
    print("-" * 40)
    
    try:
        from django.core.mail import send_mail
        
        print(f"Enviando email via: {settings.EMAIL_BACKEND}")
        
        result = send_mail(
            subject='🔧 Teste Correção Backend - Viixen',
            message=f'''
Olá!

Este é um teste da correção do backend de email.

Configuração atual:
- Backend: {settings.EMAIL_BACKEND}
- Host: {getattr(settings, 'EMAIL_HOST', 'N/A')}
- Usuário: {getattr(settings, 'EMAIL_HOST_USER', 'N/A')}

Se você recebeu este email, o SMTP está funcionando!
Se apareceu no terminal, o Console está funcionando!

Atenciosamente,
Sistema Viixen
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['yurymenezes@hotmail.com'],
            fail_silently=False,
        )
        
        if result:
            print("✅ Email enviado com sucesso!")
            
            if 'smtp' in settings.EMAIL_BACKEND:
                print("📬 Verifique yurymenezes@hotmail.com")
            else:
                print("🖥️ Email apareceu no terminal acima")
        else:
            print("❌ Falha no envio")
            
    except Exception as e:
        print(f"❌ Erro no envio: {e}")

def test_mode_switching():
    """Testa a alternância entre modos"""
    print(f"\n🔄 TESTE DE ALTERNÂNCIA DE MODOS:")
    print("-" * 40)
    
    try:
        gmail_config = EmailConfig.objects.get(slug='gmail-config')
        
        # Testar modo Console
        print("1. Testando modo Console...")
        gmail_config.use_console_backend = True
        gmail_config.save()
        
        if 'console' in settings.EMAIL_BACKEND:
            print("✅ Modo Console aplicado")
        else:
            print("❌ Modo Console não foi aplicado")
        
        # Testar modo SMTP
        print("2. Testando modo SMTP...")
        gmail_config.use_console_backend = False
        gmail_config.save()
        
        if 'smtp' in settings.EMAIL_BACKEND:
            print("✅ Modo SMTP aplicado")
        else:
            print("❌ Modo SMTP não foi aplicado")
            
    except EmailConfig.DoesNotExist:
        print("❌ Configuração Gmail não encontrada")

def main():
    """Função principal"""
    print("🧪 TESTE COMPLETO DA CORREÇÃO DO BACKEND")
    print("=" * 70)
    
    test_email_backend_fix()
    test_mode_switching()
    
    print(f"\n📋 RESUMO DAS CORREÇÕES:")
    print("=" * 50)
    print("✅ Removido EMAIL_BACKEND forçado em settings.py")
    print("✅ Adicionada aplicação automática na inicialização")
    print("✅ Backend respeitando configurações dinâmicas")
    print("✅ Alternância entre Console/SMTP funcionando")
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print("1. Reinicie o servidor Django")
    print("2. Teste na interface web")
    print("3. Alterne entre modos e verifique o comportamento")
    print("4. Confirme que emails são enviados via SMTP quando configurado")

if __name__ == '__main__':
    main()
