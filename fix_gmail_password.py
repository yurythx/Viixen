#!/usr/bin/env python
"""
Script para diagnosticar e corrigir problemas com senha de app do Gmail
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
import smtplib

def diagnose_gmail_issue():
    """Diagnostica problemas com Gmail"""
    print("🔍 DIAGNÓSTICO GMAIL - VIIXEN")
    print("=" * 50)
    
    # 1. Verificar configuração
    try:
        config = EmailConfig.objects.get(slug='gmail-config')
        print("✅ Configuração Gmail encontrada")
        print(f"📧 Email: {config.email_host_user}")
        print(f"🔧 Host: {config.email_host}:{config.email_port}")
        print(f"🔒 TLS: {config.email_use_tls}")
        print(f"🔑 Senha: {'Configurada' if config.get_password() else 'NÃO CONFIGURADA'}")
    except EmailConfig.DoesNotExist:
        print("❌ Configuração Gmail não encontrada!")
        return
    
    # 2. Configurar senha de app
    print(f"\n🔑 CONFIGURANDO SENHA DE APP")
    print("-" * 30)
    
    app_password = "hzlbeaeyxttjrhob"
    config.set_password(app_password)
    config.save()
    
    print(f"✅ Senha configurada: {app_password}")
    print(f"🔑 Verificação: {'OK' if config.get_password() == app_password else 'ERRO'}")
    
    # 3. Teste direto SMTP
    print(f"\n🔌 TESTE DIRETO SMTP")
    print("-" * 30)
    
    try:
        print("Conectando ao Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("✅ Conexão estabelecida")
        
        print("Iniciando TLS...")
        server.starttls()
        print("✅ TLS iniciado")
        
        print("Fazendo login...")
        server.login('projetohavoc@gmail.com', app_password)
        print("✅ Login realizado com sucesso!")
        
        server.quit()
        print("✅ Conexão encerrada")
        
        smtp_success = True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Erro de autenticação: {e}")
        print("\n💡 POSSÍVEIS CAUSAS:")
        print("1. Senha de app incorreta")
        print("2. Verificação em 2 etapas não ativada")
        print("3. Senha de app não gerada corretamente")
        smtp_success = False
        
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        smtp_success = False
    
    # 4. Teste com utilitários do sistema
    print(f"\n🧪 TESTE COM UTILITÁRIOS DO SISTEMA")
    print("-" * 30)
    
    success, message = test_email_connection(config)
    print(f"Resultado: {'✅ SUCESSO' if success else '❌ FALHA'}")
    print(f"Mensagem: {message}")
    
    # 5. Enviar email de teste se conexão OK
    if smtp_success and success:
        print(f"\n📤 ENVIANDO EMAIL DE TESTE")
        print("-" * 30)
        
        test_success, test_message = send_test_email('yurymenezes@hotmail.com', config)
        print(f"Resultado: {'✅ SUCESSO' if test_success else '❌ FALHA'}")
        print(f"Mensagem: {test_message}")
    
    # 6. Verificações adicionais
    print(f"\n🔍 VERIFICAÇÕES ADICIONAIS")
    print("-" * 30)
    
    # Verificar se a conta Gmail está correta
    if config.email_host_user != 'projetohavoc@gmail.com':
        print(f"⚠️  Email configurado: {config.email_host_user}")
        print("💡 Deveria ser: projetohavoc@gmail.com")
    else:
        print("✅ Email correto: projetohavoc@gmail.com")
    
    # Verificar configurações SMTP
    if config.email_host != 'smtp.gmail.com':
        print(f"⚠️  Host configurado: {config.email_host}")
        print("💡 Deveria ser: smtp.gmail.com")
    else:
        print("✅ Host correto: smtp.gmail.com")
    
    if config.email_port != 587:
        print(f"⚠️  Porta configurada: {config.email_port}")
        print("💡 Deveria ser: 587")
    else:
        print("✅ Porta correta: 587")
    
    if not config.email_use_tls:
        print("⚠️  TLS desativado")
        print("💡 TLS deve estar ativado para Gmail")
    else:
        print("✅ TLS ativado")
    
    return smtp_success

def fix_gmail_config():
    """Corrige configuração do Gmail"""
    print(f"\n🔧 CORRIGINDO CONFIGURAÇÃO GMAIL")
    print("-" * 30)
    
    try:
        config = EmailConfig.objects.get(slug='gmail-config')
        
        # Corrigir todas as configurações
        config.email_host = 'smtp.gmail.com'
        config.email_port = 587
        config.email_host_user = 'projetohavoc@gmail.com'
        config.default_from_email = 'projetohavoc@gmail.com'
        config.email_use_tls = True
        config.is_active = True
        
        # Configurar senha de app
        config.set_password('hzlbeaeyxttjrhob')
        config.save()
        
        print("✅ Configuração corrigida!")
        print(f"📧 Email: {config.email_host_user}")
        print(f"🔧 Host: {config.email_host}:{config.email_port}")
        print(f"🔒 TLS: {config.email_use_tls}")
        print(f"🔑 Senha: Configurada")
        
        return config
        
    except Exception as e:
        print(f"❌ Erro ao corrigir: {e}")
        return None

def test_alternative_methods():
    """Testa métodos alternativos"""
    print(f"\n🔄 TESTANDO MÉTODOS ALTERNATIVOS")
    print("-" * 30)
    
    # Teste com diferentes configurações
    alternatives = [
        {'host': 'smtp.gmail.com', 'port': 587, 'tls': True},
        {'host': 'smtp.gmail.com', 'port': 465, 'tls': False},  # SSL
    ]
    
    for i, alt in enumerate(alternatives, 1):
        print(f"\n🧪 Teste {i}: {alt['host']}:{alt['port']} (TLS: {alt['tls']})")
        
        try:
            if alt['tls']:
                server = smtplib.SMTP(alt['host'], alt['port'])
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(alt['host'], alt['port'])
            
            server.login('projetohavoc@gmail.com', 'hzlbeaeyxttjrhob')
            print(f"✅ Teste {i} SUCESSO!")
            server.quit()
            return alt
            
        except Exception as e:
            print(f"❌ Teste {i} falhou: {e}")
    
    return None

def main():
    """Função principal"""
    print("🔧 CORRETOR DE PROBLEMAS GMAIL")
    print("=" * 60)
    
    # 1. Diagnóstico inicial
    smtp_success = diagnose_gmail_issue()
    
    if not smtp_success:
        print(f"\n🔧 TENTANDO CORRIGIR...")
        
        # 2. Corrigir configuração
        config = fix_gmail_config()
        
        if config:
            # 3. Testar novamente
            print(f"\n🔄 TESTANDO APÓS CORREÇÃO")
            print("-" * 30)
            
            success, message = test_email_connection(config)
            print(f"Resultado: {'✅ SUCESSO' if success else '❌ FALHA'}")
            print(f"Mensagem: {message}")
            
            if not success:
                # 4. Testar métodos alternativos
                alt_config = test_alternative_methods()
                
                if alt_config:
                    print(f"\n✅ Configuração alternativa funcionou!")
                    print(f"Use: {alt_config['host']}:{alt_config['port']} (TLS: {alt_config['tls']})")
    
    print(f"\n📋 RESUMO FINAL")
    print("-" * 30)
    print("🔗 Teste na interface: http://127.0.0.1:8000/config/email/")
    print("📖 Guia completo: http://127.0.0.1:8000/config/email/guide/")
    print("🔑 Gmail App Passwords: https://myaccount.google.com/apppasswords")
    
    print(f"\n💡 SE AINDA NÃO FUNCIONAR:")
    print("1. Verifique se a verificação em 2 etapas está ATIVADA")
    print("2. Gere uma NOVA senha de app")
    print("3. Use a conta projetohavoc@gmail.com para gerar")
    print("4. Certifique-se de copiar a senha corretamente")

if __name__ == '__main__':
    main()
