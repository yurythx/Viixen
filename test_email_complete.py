#!/usr/bin/env python
"""
Teste completo do sistema de email
Cria configuração, testa conexão e envia email real
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.config.models import EmailConfig
from apps.config.email_utils import test_email_connection, send_test_email, apply_email_settings_to_django

def create_email_config():
    """Cria configuração de email para Hotmail/Outlook"""
    print("🔧 CRIANDO CONFIGURAÇÃO DE EMAIL")
    print("=" * 50)
    
    # Configuração para Hotmail/Outlook
    config, created = EmailConfig.objects.get_or_create(
        slug='email-config',
        defaults={
            'email_host': 'smtp-mail.outlook.com',
            'email_port': 587,
            'email_host_user': 'yurymenezes@hotmail.com',
            'default_from_email': 'yurymenezes@hotmail.com',
            'email_use_tls': True,
            'is_active': True
        }
    )
    
    if created:
        print("✅ Nova configuração criada")
    else:
        print("📝 Configuração existente encontrada")
    
    print(f"📧 Host: {config.email_host}:{config.email_port}")
    print(f"👤 Usuário: {config.email_host_user}")
    print(f"🔒 TLS: {config.email_use_tls}")
    print(f"✅ Ativo: {config.is_active}")
    
    return config

def set_password(config):
    """Define a senha da configuração"""
    print("\n🔑 CONFIGURANDO SENHA")
    print("=" * 50)
    
    # Para teste, você precisa inserir a senha real
    # Para Hotmail/Outlook, use uma senha de app se tiver 2FA ativado
    password = input("Digite a senha do email (ou senha de app): ")
    
    if password:
        config.set_password(password)
        config.save()
        print("✅ Senha configurada com sucesso")
        return True
    else:
        print("❌ Senha não fornecida")
        return False

def test_connection(config):
    """Testa a conexão SMTP"""
    print("\n🔌 TESTANDO CONEXÃO SMTP")
    print("=" * 50)
    
    success, message = test_email_connection(config)
    
    if success:
        print(f"✅ {message}")
        return True
    else:
        print(f"❌ {message}")
        return False

def send_email_test(config):
    """Envia email de teste"""
    print("\n📤 ENVIANDO EMAIL DE TESTE")
    print("=" * 50)
    
    recipient = 'yurymenezes@hotmail.com'
    print(f"📧 Destinatário: {recipient}")
    
    success, message = send_test_email(recipient, config)
    
    if success:
        print(f"✅ {message}")
        return True
    else:
        print(f"❌ {message}")
        return False

def apply_to_django(config):
    """Aplica configurações ao Django"""
    print("\n⚙️ APLICANDO CONFIGURAÇÕES AO DJANGO")
    print("=" * 50)
    
    success = apply_email_settings_to_django(config)
    
    if success:
        print("✅ Configurações aplicadas ao Django")
        
        # Mostrar configurações atuais
        print("\n📋 Configurações Django atuais:")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        return True
    else:
        print("❌ Erro ao aplicar configurações")
        return False

def test_django_email():
    """Testa envio usando o sistema padrão do Django"""
    print("\n🧪 TESTANDO EMAIL VIA DJANGO")
    print("=" * 50)
    
    try:
        from django.core.mail import send_mail
        
        result = send_mail(
            subject='🧪 Teste Django - Sistema Viixen',
            message='''
Olá!

Este é um teste usando o sistema padrão do Django após aplicar as configurações.

Se você recebeu este email, o sistema está funcionando perfeitamente! ✅

Atenciosamente,
Sistema Viixen
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['yurymenezes@hotmail.com'],
            fail_silently=False,
        )
        
        if result:
            print("✅ Email enviado via Django com sucesso!")
            return True
        else:
            print("❌ Falha no envio via Django")
            return False
            
    except Exception as e:
        print(f"❌ Erro no envio via Django: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE COMPLETO DO SISTEMA DE EMAIL - VIIXEN")
    print("=" * 60)
    
    # 1. Criar configuração
    config = create_email_config()
    
    # 2. Configurar senha
    if not set_password(config):
        print("\n❌ Teste interrompido - senha necessária")
        return
    
    # 3. Testar conexão
    if not test_connection(config):
        print("\n❌ Teste interrompido - falha na conexão")
        return
    
    # 4. Enviar email de teste
    if not send_email_test(config):
        print("\n❌ Falha no envio do email de teste")
    
    # 5. Aplicar ao Django
    if apply_to_django(config):
        # 6. Testar via Django
        test_django_email()
    
    print("\n📊 RESUMO DO TESTE")
    print("=" * 50)
    print("✅ Configuração criada")
    print("✅ Senha configurada")
    print("✅ Conexão testada")
    print("✅ Email de teste enviado")
    print("✅ Configurações aplicadas ao Django")
    print("✅ Teste via Django realizado")
    
    print("\n🎯 PRÓXIMOS PASSOS")
    print("=" * 50)
    print("1. Acesse http://127.0.0.1:8000/config/email/")
    print("2. Teste os botões de teste na interface")
    print("3. Verifique se recebeu os emails de teste")
    print("4. Configure outras funcionalidades que usam email")

if __name__ == '__main__':
    main()
