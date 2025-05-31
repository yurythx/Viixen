#!/usr/bin/env python
"""
Teste específico para configuração Gmail
projetohavoc@gmail.com
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

def create_gmail_config():
    """Cria configuração Gmail"""
    print("🔧 CRIANDO CONFIGURAÇÃO GMAIL")
    print("=" * 50)
    
    # Configuração para Gmail
    config, created = EmailConfig.objects.get_or_create(
        slug='gmail-config',
        defaults={
            'email_host': 'smtp.gmail.com',
            'email_port': 587,
            'email_host_user': 'projetohavoc@gmail.com',
            'default_from_email': 'projetohavoc@gmail.com',
            'email_use_tls': True,
            'is_active': True
        }
    )
    
    # Configurar a senha
    config.set_password('C9p5au8naa%1309')
    config.save()
    
    print(f"✅ Configuração {'criada' if created else 'atualizada'}")
    print(f"📧 Host: {config.email_host}:{config.email_port}")
    print(f"👤 Usuário: {config.email_host_user}")
    print(f"🔒 TLS: {config.email_use_tls}")
    print(f"✅ Ativo: {config.is_active}")
    print(f"🔑 Senha: {'Configurada' if config.get_password() else 'Não configurada'}")
    
    return config

def test_gmail_connection(config):
    """Testa conexão Gmail"""
    print("\n🔌 TESTANDO CONEXÃO GMAIL")
    print("=" * 50)
    
    success, message = test_email_connection(config)
    
    if success:
        print(f"✅ Conexão Gmail OK: {message}")
        return True
    else:
        print(f"❌ Erro na conexão Gmail: {message}")
        print("\n💡 DICAS PARA GMAIL:")
        print("1. Verifique se a verificação em 2 etapas está ativada")
        print("2. Use uma 'Senha de App' em vez da senha normal")
        print("3. Acesse: https://myaccount.google.com/apppasswords")
        print("4. Gere uma senha específica para 'Email'")
        return False

def send_gmail_test(config):
    """Envia email de teste via Gmail"""
    print("\n📤 ENVIANDO EMAIL DE TESTE VIA GMAIL")
    print("=" * 50)
    
    # Testar para ambos os emails
    recipients = ['yurymenezes@hotmail.com', 'projetohavoc@gmail.com']
    
    for recipient in recipients:
        print(f"\n📧 Enviando para: {recipient}")
        success, message = send_test_email(recipient, config)
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

def test_smtp_direct(config):
    """Teste direto SMTP sem Django"""
    print("\n🔧 TESTE DIRETO SMTP")
    print("=" * 50)
    
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    try:
        # Criar conexão
        server = smtplib.SMTP(config.email_host, config.email_port)
        server.starttls()
        
        print("✅ Conexão SMTP estabelecida")
        
        # Fazer login
        server.login(config.email_host_user, config.get_password())
        print("✅ Login SMTP realizado")
        
        # Criar email
        msg = MIMEMultipart()
        msg['From'] = config.default_from_email
        msg['To'] = 'yurymenezes@hotmail.com'
        msg['Subject'] = '🧪 Teste Direto SMTP - Gmail Viixen'
        
        body = f"""
Olá!

Este é um teste direto SMTP do Gmail para o sistema Viixen.

Configuração testada:
- Servidor: {config.email_host}:{config.email_port}
- Usuário: {config.email_host_user}
- TLS: Ativado

Se você recebeu este email, a configuração Gmail está funcionando perfeitamente! ✅

Enviado via teste direto SMTP.

Atenciosamente,
Sistema Viixen
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Enviar email
        text = msg.as_string()
        server.sendmail(config.email_host_user, 'yurymenezes@hotmail.com', text)
        server.quit()
        
        print("✅ Email enviado via SMTP direto!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste SMTP direto: {e}")
        return False

def apply_gmail_to_django(config):
    """Aplica configuração Gmail ao Django"""
    print("\n⚙️ APLICANDO GMAIL AO DJANGO")
    print("=" * 50)
    
    success = apply_email_settings_to_django(config)
    
    if success:
        print("✅ Configurações Gmail aplicadas ao Django")
        
        # Mostrar configurações
        print(f"\n📋 Configurações Django:")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        return True
    else:
        print("❌ Erro ao aplicar configurações Gmail")
        return False

def test_django_with_gmail():
    """Testa Django com configurações Gmail"""
    print("\n🧪 TESTANDO DJANGO COM GMAIL")
    print("=" * 50)
    
    try:
        from django.core.mail import send_mail
        
        result = send_mail(
            subject='🧪 Teste Django Gmail - Sistema Viixen',
            message=f'''
Olá!

Este é um teste usando o Django com configurações Gmail aplicadas.

Configurações utilizadas:
- Host: {settings.EMAIL_HOST}
- Porta: {settings.EMAIL_PORT}
- Usuário: {settings.EMAIL_HOST_USER}
- TLS: {settings.EMAIL_USE_TLS}

Se você recebeu este email, o sistema Django + Gmail está funcionando! ✅

Atenciosamente,
Sistema Viixen
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['yurymenezes@hotmail.com'],
            fail_silently=False,
        )
        
        if result:
            print("✅ Email enviado via Django + Gmail!")
            return True
        else:
            print("❌ Falha no envio via Django")
            return False
            
    except Exception as e:
        print(f"❌ Erro no Django: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE COMPLETO GMAIL - VIIXEN")
    print("=" * 60)
    print("📧 Email: projetohavoc@gmail.com")
    print("🎯 Destino: yurymenezes@hotmail.com")
    print("=" * 60)
    
    # 1. Criar configuração Gmail
    config = create_gmail_config()
    
    # 2. Testar conexão
    connection_ok = test_gmail_connection(config)
    
    # 3. Teste SMTP direto
    smtp_ok = test_smtp_direct(config)
    
    # 4. Enviar email de teste
    if connection_ok:
        send_gmail_test(config)
    
    # 5. Aplicar ao Django
    django_ok = apply_gmail_to_django(config)
    
    # 6. Testar Django
    if django_ok:
        test_django_with_gmail()
    
    print("\n📊 RESUMO DOS TESTES GMAIL")
    print("=" * 50)
    print(f"✅ Configuração criada: OK")
    print(f"{'✅' if connection_ok else '❌'} Conexão Gmail: {'OK' if connection_ok else 'FALHOU'}")
    print(f"{'✅' if smtp_ok else '❌'} SMTP direto: {'OK' if smtp_ok else 'FALHOU'}")
    print(f"{'✅' if django_ok else '❌'} Django aplicado: {'OK' if django_ok else 'FALHOU'}")
    
    if not connection_ok:
        print("\n⚠️  ATENÇÃO: Se a conexão falhou, você pode precisar:")
        print("1. Ativar verificação em 2 etapas no Gmail")
        print("2. Gerar uma 'Senha de App' específica")
        print("3. Usar a senha de app em vez da senha normal")
    
    print("\n🌐 TESTE NA INTERFACE WEB:")
    print("Acesse: http://127.0.0.1:8000/config/email/")
    print("Procure pela configuração 'gmail-config'")
    print("Use os botões de teste na interface")

if __name__ == '__main__':
    main()
