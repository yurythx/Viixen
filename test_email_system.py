#!/usr/bin/env python
"""
Sistema de teste completo para configuração de email
Testa desde a configuração até o envio efetivo de emails
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import send_mail, get_connection
from django.core.mail.backends.smtp import EmailBackend
from apps.config.models import EmailConfig
from django.test import override_settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_config_model():
    """Testa o modelo EmailConfig"""
    print("🔧 TESTANDO MODELO EmailConfig")
    print("=" * 50)
    
    # Verificar se existe configuração
    email_configs = EmailConfig.objects.all()
    print(f"📊 Configurações existentes: {email_configs.count()}")
    
    for config in email_configs:
        print(f"📧 {config.email_host}:{config.email_port}")
        print(f"   Usuário: {config.email_host_user}")
        print(f"   TLS: {config.email_use_tls}")
        print(f"   Ativo: {config.is_active}")
        print(f"   Email padrão: {config.default_from_email}")
        
        # Testar descriptografia de senha
        try:
            decrypted_password = config.get_password()
            print(f"   Senha descriptografada: {'*' * len(decrypted_password) if decrypted_password else 'Vazia'}")
        except Exception as e:
            print(f"   ❌ Erro ao descriptografar senha: {e}")
    
    return email_configs

def create_test_email_config():
    """Cria uma configuração de email de teste"""
    print("\n🔧 CRIANDO CONFIGURAÇÃO DE TESTE")
    print("=" * 50)
    
    # Configuração para Gmail (mais comum)
    config, created = EmailConfig.objects.get_or_create(
        slug='email-config',
        defaults={
            'email_host': 'smtp.gmail.com',
            'email_port': 587,
            'email_host_user': 'yurymenezes@hotmail.com',  # Seu email
            'default_from_email': 'yurymenezes@hotmail.com',
            'email_use_tls': True,
            'is_active': True
        }
    )
    
    if created:
        print("✅ Nova configuração criada")
    else:
        print("📝 Configuração existente encontrada")
    
    # Definir senha (você precisará inserir a senha real)
    print("⚠️  ATENÇÃO: Para teste real, você precisa configurar a senha")
    print("   Para Gmail, use uma 'Senha de App' em vez da senha normal")
    print("   Acesse: https://myaccount.google.com/apppasswords")
    
    return config

def test_smtp_connection(config):
    """Testa conexão SMTP diretamente"""
    print(f"\n🔌 TESTANDO CONEXÃO SMTP: {config.email_host}:{config.email_port}")
    print("=" * 50)
    
    try:
        # Testar conexão básica
        if config.email_use_tls:
            server = smtplib.SMTP(config.email_host, config.email_port)
            server.starttls()
        else:
            server = smtplib.SMTP(config.email_host, config.email_port)
        
        print("✅ Conexão SMTP estabelecida")
        
        # Testar login (se tiver credenciais)
        password = config.get_password()
        if config.email_host_user and password:
            try:
                server.login(config.email_host_user, password)
                print("✅ Login SMTP realizado com sucesso")
                server.quit()
                return True
            except smtplib.SMTPAuthenticationError as e:
                print(f"❌ Erro de autenticação: {e}")
                print("💡 Verifique se está usando uma 'Senha de App' para Gmail")
                server.quit()
                return False
        else:
            print("⚠️  Credenciais não configuradas")
            server.quit()
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_django_email_backend(config):
    """Testa o backend de email do Django"""
    print(f"\n📧 TESTANDO BACKEND DJANGO")
    print("=" * 50)
    
    # Configurar backend dinamicamente
    email_settings = {
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'EMAIL_HOST': config.email_host,
        'EMAIL_PORT': config.email_port,
        'EMAIL_HOST_USER': config.email_host_user,
        'EMAIL_HOST_PASSWORD': config.get_password(),
        'EMAIL_USE_TLS': config.email_use_tls,
        'DEFAULT_FROM_EMAIL': config.default_from_email,
    }
    
    print(f"🔧 Host: {email_settings['EMAIL_HOST']}")
    print(f"🔧 Porta: {email_settings['EMAIL_PORT']}")
    print(f"🔧 Usuário: {email_settings['EMAIL_HOST_USER']}")
    print(f"🔧 TLS: {email_settings['EMAIL_USE_TLS']}")
    
    try:
        # Criar conexão personalizada
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=config.email_host,
            port=config.email_port,
            username=config.email_host_user,
            password=config.get_password(),
            use_tls=config.email_use_tls,
        )
        
        # Testar conexão
        connection.open()
        print("✅ Conexão Django estabelecida")
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro no backend Django: {e}")
        return False

def send_test_email(config, recipient_email):
    """Envia um email de teste"""
    print(f"\n📤 ENVIANDO EMAIL DE TESTE PARA: {recipient_email}")
    print("=" * 50)
    
    if not config.get_password():
        print("❌ Senha não configurada. Configure a senha primeiro.")
        return False
    
    try:
        # Criar conexão personalizada
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=config.email_host,
            port=config.email_port,
            username=config.email_host_user,
            password=config.get_password(),
            use_tls=config.email_use_tls,
        )
        
        # Enviar email
        result = send_mail(
            subject='🧪 Teste de Configuração de Email - Viixen',
            message=f'''
Olá!

Este é um email de teste do sistema Viixen.

Configuração utilizada:
- Servidor: {config.email_host}:{config.email_port}
- TLS: {config.email_use_tls}
- Usuário: {config.email_host_user}

Se você recebeu este email, a configuração está funcionando corretamente! ✅

Atenciosamente,
Sistema Viixen
            ''',
            from_email=config.default_from_email,
            recipient_list=[recipient_email],
            connection=connection,
            fail_silently=False,
        )
        
        if result:
            print("✅ Email enviado com sucesso!")
            return True
        else:
            print("❌ Falha no envio do email")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

def test_environment_variables():
    """Testa as variáveis de ambiente de email"""
    print(f"\n🌍 TESTANDO VARIÁVEIS DE AMBIENTE")
    print("=" * 50)
    
    env_vars = [
        'EMAIL_HOST',
        'EMAIL_PORT', 
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'EMAIL_USE_TLS',
        'DEFAULT_FROM_EMAIL'
    ]
    
    for var in env_vars:
        value = getattr(settings, var, 'NÃO DEFINIDA')
        if var == 'EMAIL_HOST_PASSWORD' and value:
            value = '*' * len(str(value))
        print(f"📝 {var}: {value}")

def main():
    """Função principal de teste"""
    print("🧪 SISTEMA DE TESTE DE EMAIL - VIIXEN")
    print("=" * 60)
    
    # 1. Testar modelo
    configs = test_email_config_model()
    
    # 2. Criar configuração se não existir
    if not configs.exists():
        config = create_test_email_config()
    else:
        config = configs.first()
    
    # 3. Testar variáveis de ambiente
    test_environment_variables()
    
    # 4. Testar conexão SMTP
    smtp_ok = test_smtp_connection(config)
    
    # 5. Testar backend Django
    django_ok = test_django_email_backend(config)
    
    # 6. Enviar email de teste (apenas se tudo estiver OK)
    if smtp_ok and django_ok:
        print(f"\n🎯 PRONTO PARA ENVIAR EMAIL DE TESTE")
        print("=" * 50)
        print("⚠️  Para enviar o email de teste, você precisa:")
        print("1. Configurar a senha no modelo EmailConfig")
        print("2. Executar: send_test_email(config, 'yurymenezes@hotmail.com')")
        print("\n💡 Para Gmail, use uma 'Senha de App':")
        print("   https://myaccount.google.com/apppasswords")
    
    print(f"\n📊 RESUMO DOS TESTES")
    print("=" * 50)
    print(f"✅ Modelo EmailConfig: OK")
    print(f"{'✅' if smtp_ok else '❌'} Conexão SMTP: {'OK' if smtp_ok else 'FALHOU'}")
    print(f"{'✅' if django_ok else '❌'} Backend Django: {'OK' if django_ok else 'FALHOU'}")
    
    return config

if __name__ == '__main__':
    config = main()
