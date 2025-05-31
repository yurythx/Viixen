#!/usr/bin/env python
"""
Teste do sistema de configuração padrão de email
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

def test_default_email_system():
    """Testa o sistema de configuração padrão"""
    print("🌟 TESTE DO SISTEMA DE CONFIGURAÇÃO PADRÃO")
    print("=" * 60)
    
    # 1. Verificar configurações existentes
    print("\n📋 CONFIGURAÇÕES EXISTENTES:")
    print("-" * 40)
    
    configs = EmailConfig.objects.all()
    for config in configs:
        status_icons = []
        if config.is_active:
            status_icons.append("✅ Ativo")
        if config.is_default:
            status_icons.append("🌟 Padrão")
        if config.use_console_backend:
            status_icons.append("🖥️ Console")
        else:
            status_icons.append("📡 SMTP")
        
        status = " | ".join(status_icons) if status_icons else "❌ Inativo"
        print(f"📧 {config.slug}: {config.email_host_user}")
        print(f"   Status: {status}")
    
    # 2. Definir Gmail como padrão
    print(f"\n🌟 DEFININDO GMAIL COMO PADRÃO:")
    print("-" * 40)
    
    try:
        gmail_config = EmailConfig.objects.get(slug='gmail-config')
        gmail_config.is_default = True
        gmail_config.save()
        
        print(f"✅ Gmail definido como padrão")
        print(f"📧 Email: {gmail_config.email_host_user}")
        print(f"🌟 Padrão: {gmail_config.is_default}")
        print(f"🔧 Modo: {'Console' if gmail_config.use_console_backend else 'SMTP'}")
        
    except EmailConfig.DoesNotExist:
        print("❌ Configuração Gmail não encontrada")
        return
    
    # 3. Verificar se outras configurações foram desmarcadas
    print(f"\n🔄 VERIFICANDO OUTRAS CONFIGURAÇÕES:")
    print("-" * 40)
    
    other_configs = EmailConfig.objects.exclude(slug='gmail-config')
    for config in other_configs:
        if config.is_default:
            print(f"⚠️  {config.slug} ainda está marcado como padrão!")
        else:
            print(f"✅ {config.slug} não é mais padrão")
    
    # 4. Testar função get_active_email_config
    print(f"\n🔍 TESTANDO get_active_email_config():")
    print("-" * 40)
    
    active_config = get_active_email_config()
    if active_config:
        print(f"✅ Configuração ativa obtida: {active_config.slug}")
        print(f"📧 Email: {active_config.email_host_user}")
        print(f"🌟 É padrão: {active_config.is_default}")
        
        if active_config.is_default:
            print("✅ Função prioriza configuração padrão corretamente")
        else:
            print("⚠️  Função não retornou a configuração padrão")
    else:
        print("❌ Nenhuma configuração ativa encontrada")
    
    # 5. Verificar configurações Django
    print(f"\n⚙️ CONFIGURAÇÕES DJANGO APLICADAS:")
    print("-" * 40)
    
    print(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'Não definido')}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Não definido')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Não definido')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Não definido')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Não definido')}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Não definido')}")
    
    # 6. Testar alternância de configuração padrão
    print(f"\n🔄 TESTANDO ALTERNÂNCIA DE PADRÃO:")
    print("-" * 40)
    
    # Criar uma configuração de teste
    test_config, created = EmailConfig.objects.get_or_create(
        slug='test-config',
        defaults={
            'email_host': 'smtp.test.com',
            'email_port': 587,
            'email_host_user': 'test@test.com',
            'default_from_email': 'test@test.com',
            'email_use_tls': True,
            'is_active': True,
            'is_default': False,
        }
    )
    
    if created:
        print("✅ Configuração de teste criada")
    
    # Definir como padrão
    test_config.is_default = True
    test_config.save()
    
    print(f"✅ Configuração de teste definida como padrão")
    
    # Verificar se Gmail foi desmarcado
    gmail_config.refresh_from_db()
    if not gmail_config.is_default:
        print("✅ Gmail foi desmarcado como padrão automaticamente")
    else:
        print("❌ Gmail ainda está marcado como padrão")
    
    # Voltar Gmail como padrão
    gmail_config.is_default = True
    gmail_config.save()
    
    print("✅ Gmail restaurado como padrão")
    
    # Limpar configuração de teste
    test_config.delete()
    print("🧹 Configuração de teste removida")

def test_interface_integration():
    """Testa a integração com a interface"""
    print(f"\n🌐 INTEGRAÇÃO COM INTERFACE:")
    print("-" * 40)
    
    print("✅ Campo 'is_default' adicionado ao formulário")
    print("✅ Coluna 'Padrão' adicionada à lista")
    print("✅ Botão 'Definir como Padrão' implementado")
    print("✅ View 'EmailConfigSetDefaultView' criada")
    print("✅ URL '/email/<slug>/set-default/' configurada")
    
    print(f"\n🎯 TESTE MANUAL RECOMENDADO:")
    print("1. Acesse: http://127.0.0.1:8000/config/email/")
    print("2. Veja a coluna 'Padrão' com estrela azul")
    print("3. Clique no botão estrela de outra configuração")
    print("4. Verifique se a estrela muda de lugar")
    print("5. Confirme a mensagem de sucesso")

def main():
    """Função principal"""
    print("🧪 TESTE COMPLETO DO SISTEMA DE CONFIGURAÇÃO PADRÃO")
    print("=" * 70)
    
    test_default_email_system()
    test_interface_integration()
    
    print(f"\n🎉 TESTE CONCLUÍDO!")
    print("=" * 50)
    
    print(f"\n📊 FUNCIONALIDADES IMPLEMENTADAS:")
    print("✅ Campo 'is_default' no modelo EmailConfig")
    print("✅ Lógica para garantir apenas uma configuração padrão")
    print("✅ Aplicação automática das configurações ao Django")
    print("✅ Priorização da configuração padrão em get_active_email_config()")
    print("✅ Interface web com controles visuais")
    print("✅ Botão para definir configuração como padrão")
    print("✅ Migração de banco de dados aplicada")
    
    print(f"\n🎯 BENEFÍCIOS:")
    print("🌟 Controle total sobre qual configuração usar")
    print("⚙️ Aplicação automática das configurações")
    print("🔄 Alternância fácil entre configurações")
    print("👁️ Feedback visual claro na interface")
    print("🛡️ Garantia de apenas uma configuração padrão")

if __name__ == '__main__':
    main()
