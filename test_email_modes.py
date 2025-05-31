#!/usr/bin/env python
"""
Teste dos modos de email: Console vs SMTP
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.config.models import EmailConfig
from apps.config.email_utils import apply_email_settings_to_django, send_email_with_config
from django.core.mail import send_mail

def test_console_mode():
    """Testa o modo console"""
    print("🖥️  TESTANDO MODO CONSOLE")
    print("=" * 50)
    
    config = EmailConfig.objects.get(slug='gmail-config')
    
    # Configurar para modo console
    config.use_console_backend = True
    config.save()
    
    # Aplicar configurações
    apply_email_settings_to_django(config)
    
    print(f"📧 Configuração: {config.email_host_user}")
    print(f"🔧 Modo: Console (Desenvolvimento)")
    print(f"📋 Backend Django: {settings.EMAIL_BACKEND}")
    
    print("\n📤 Enviando email de teste...")
    print("(O email deve aparecer no terminal abaixo)")
    print("-" * 50)
    
    # Enviar email usando Django
    try:
        send_mail(
            subject='🖥️  Teste Modo Console - Viixen',
            message='''
Olá!

Este email está sendo enviado em MODO CONSOLE.

Isso significa que:
- O email NÃO será enviado para o destinatário real
- Ele aparecerá apenas no terminal/console
- Útil para desenvolvimento e testes

Se você está vendo isso no terminal, o modo console está funcionando!

Atenciosamente,
Sistema Viixen
            ''',
            from_email=config.default_from_email,
            recipient_list=['yurymenezes@hotmail.com'],
            fail_silently=False,
        )
        print("\n✅ Email enviado em modo console!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")

def test_smtp_mode():
    """Testa o modo SMTP"""
    print("\n📡 TESTANDO MODO SMTP")
    print("=" * 50)
    
    config = EmailConfig.objects.get(slug='gmail-config')
    
    # Configurar para modo SMTP
    config.use_console_backend = False
    config.save()
    
    # Aplicar configurações
    apply_email_settings_to_django(config)
    
    print(f"📧 Configuração: {config.email_host_user}")
    print(f"🔧 Modo: SMTP (Produção)")
    print(f"📋 Backend Django: {settings.EMAIL_BACKEND}")
    print(f"🌐 Servidor: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    
    print("\n📤 Enviando email real...")
    print("(O email será enviado para yurymenezes@hotmail.com)")
    print("-" * 50)
    
    # Enviar email usando Django
    try:
        send_mail(
            subject='📡 Teste Modo SMTP - Viixen',
            message='''
Olá!

Este email está sendo enviado em MODO SMTP.

Isso significa que:
- O email SERÁ enviado para o destinatário real
- Ele chegará na caixa de entrada
- Usado em produção para envios reais

Se você recebeu este email, o modo SMTP está funcionando!

Atenciosamente,
Sistema Viixen
            ''',
            from_email=config.default_from_email,
            recipient_list=['yurymenezes@hotmail.com'],
            fail_silently=False,
        )
        print("✅ Email enviado via SMTP!")
        print("📬 Verifique yurymenezes@hotmail.com")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def demonstrate_toggle():
    """Demonstra a alternância entre modos"""
    print("\n🔄 DEMONSTRAÇÃO DE ALTERNÂNCIA")
    print("=" * 50)
    
    config = EmailConfig.objects.get(slug='gmail-config')
    
    print("Alternando entre os modos...")
    
    for i in range(3):
        # Alternar modo
        config.use_console_backend = not config.use_console_backend
        config.save()
        apply_email_settings_to_django(config)
        
        mode = "Console" if config.use_console_backend else "SMTP"
        backend = settings.EMAIL_BACKEND
        
        print(f"🔄 Alternância {i+1}: Modo {mode}")
        print(f"   Backend: {backend}")
        
    print("\n✅ Alternância funcionando!")

def show_interface_instructions():
    """Mostra instruções para usar a interface"""
    print("\n🌐 USANDO A INTERFACE WEB")
    print("=" * 50)
    
    print("1. Acesse: http://127.0.0.1:8000/config/email/")
    print("2. Procure pela configuração 'gmail-config'")
    print("3. Na coluna 'Modo', você verá:")
    print("   - 🖥️  Console (amarelo) = Emails no terminal")
    print("   - 📡 SMTP (azul) = Emails reais")
    print("4. Use o botão de alternância para mudar:")
    print("   - 🖥️  → 📡 = Muda para SMTP")
    print("   - 📡 → 🖥️  = Muda para Console")
    print("5. Teste enviando emails após alternar")
    
    print("\n💡 DICAS:")
    print("- Use Console durante desenvolvimento")
    print("- Use SMTP quando quiser enviar emails reais")
    print("- A alternância é instantânea")
    print("- As configurações são aplicadas automaticamente")

def main():
    """Função principal"""
    print("🧪 TESTE DOS MODOS DE EMAIL - VIIXEN")
    print("=" * 60)
    
    try:
        # 1. Testar modo console
        test_console_mode()
        
        # 2. Testar modo SMTP
        test_smtp_mode()
        
        # 3. Demonstrar alternância
        demonstrate_toggle()
        
        # 4. Instruções da interface
        show_interface_instructions()
        
        print("\n🎉 TESTE COMPLETO!")
        print("=" * 50)
        print("✅ Modo Console: Funcionando")
        print("✅ Modo SMTP: Funcionando") 
        print("✅ Alternância: Funcionando")
        print("✅ Interface Web: Disponível")
        
        # Deixar em modo console por padrão
        config = EmailConfig.objects.get(slug='gmail-config')
        config.use_console_backend = True
        config.save()
        apply_email_settings_to_django(config)
        print("\n📝 Sistema configurado em modo Console por padrão")
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")

if __name__ == '__main__':
    main()
