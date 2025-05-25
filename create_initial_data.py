#!/usr/bin/env python
"""
Script para criar dados iniciais para o sistema de configuração
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.config.models import SystemConfig, EmailConfig, SocialProviderConfig, AppConfig, EnvironmentVariable

def create_system_config():
    """Criar configuração do sistema"""
    system_config, created = SystemConfig.objects.get_or_create(
        slug='system-config',
        defaults={
            'site_name': 'Viixen',
            'site_description': 'Sistema de Gerenciamento Viixen',
            'maintenance_mode': False,
            'allow_registration': True,
            'require_email_verification': True,
            'enable_app_management': True,
        }
    )
    if created:
        print("✅ Configuração do sistema criada")
    else:
        print("ℹ️ Configuração do sistema já existe")
    return system_config

def create_email_config():
    """Criar configuração de email"""
    email_config, created = EmailConfig.objects.get_or_create(
        slug='email-config',
        defaults={
            'email_host': 'smtp.gmail.com',
            'email_port': 587,
            'email_host_user': 'your-email@gmail.com',
            'email_host_password': 'your-app-password',
            'email_use_tls': True,
            'default_from_email': 'no-reply@viixen.com',
            'is_active': False,
        }
    )
    if created:
        print("✅ Configuração de email criada")
    else:
        print("ℹ️ Configuração de email já existe")
    return email_config

def create_social_providers():
    """Criar provedores sociais"""
    providers = [
        {
            'provider': 'google',
            'client_id': 'your-google-client-id',
            'secret_key': 'your-google-client-secret',
            'is_active': False,
        },
        {
            'provider': 'github',
            'client_id': 'your-github-client-id',
            'secret_key': 'your-github-client-secret',
            'is_active': False,
        },
        {
            'provider': 'facebook',
            'client_id': 'your-facebook-app-id',
            'secret_key': 'your-facebook-app-secret',
            'is_active': False,
        }
    ]
    
    created_count = 0
    for provider_data in providers:
        provider, created = SocialProviderConfig.objects.get_or_create(
            provider=provider_data['provider'],
            defaults=provider_data
        )
        if created:
            created_count += 1
    
    print(f"✅ {created_count} provedores sociais criados")

def create_app_configs():
    """Criar configurações de apps"""
    apps = [
        {
            'name': 'Páginas',
            'label': 'pages',
            'description': 'Sistema de páginas e navegação',
            'is_active': True,
            'is_core': True,
            'order': 1,
        },
        {
            'name': 'Contas de Usuário',
            'label': 'accounts',
            'description': 'Sistema de autenticação e gerenciamento de usuários',
            'is_active': True,
            'is_core': True,
            'order': 2,
        },
        {
            'name': 'Artigos',
            'label': 'articles',
            'description': 'Sistema de criação e gerenciamento de artigos',
            'is_active': True,
            'is_core': False,
            'order': 3,
        },
        {
            'name': 'Configurações',
            'label': 'config',
            'description': 'Sistema de configuração e administração',
            'is_active': True,
            'is_core': True,
            'order': 4,
        },
    ]
    
    created_count = 0
    for app_data in apps:
        app_config, created = AppConfig.objects.get_or_create(
            label=app_data['label'],
            defaults=app_data
        )
        if created:
            created_count += 1
    
    print(f"✅ {created_count} configurações de apps criadas")

def create_environment_variables():
    """Criar algumas variáveis de ambiente de exemplo"""
    variables = [
        {
            'key': 'DEBUG',
            'value': 'True',
            'default_value': 'False',
            'description': 'Ativa o modo de debug do Django',
            'category': 'core',
            'var_type': 'boolean',
            'is_required': True,
            'is_sensitive': False,
            'order': 1,
        },
        {
            'key': 'SECRET_KEY',
            'value': 'django-insecure-example-key',
            'default_value': '',
            'description': 'Chave secreta do Django para criptografia',
            'category': 'core',
            'var_type': 'password',
            'is_required': True,
            'is_sensitive': True,
            'order': 2,
        },
        {
            'key': 'DATABASE_URL',
            'value': 'sqlite:///db.sqlite3',
            'default_value': 'sqlite:///db.sqlite3',
            'description': 'URL de conexão com o banco de dados',
            'category': 'database',
            'var_type': 'url',
            'is_required': True,
            'is_sensitive': False,
            'order': 1,
        },
        {
            'key': 'EMAIL_HOST',
            'value': 'smtp.gmail.com',
            'default_value': 'localhost',
            'description': 'Servidor SMTP para envio de emails',
            'category': 'email',
            'var_type': 'string',
            'is_required': False,
            'is_sensitive': False,
            'order': 1,
        },
        {
            'key': 'EMAIL_HOST_PASSWORD',
            'value': '',
            'default_value': '',
            'description': 'Senha do servidor SMTP',
            'category': 'email',
            'var_type': 'password',
            'is_required': False,
            'is_sensitive': True,
            'order': 3,
        },
    ]
    
    created_count = 0
    for var_data in variables:
        variable, created = EnvironmentVariable.objects.get_or_create(
            key=var_data['key'],
            defaults=var_data
        )
        if created:
            created_count += 1
    
    print(f"✅ {created_count} variáveis de ambiente criadas")

def main():
    """Função principal"""
    print("🚀 Criando dados iniciais...")
    print()
    
    try:
        create_system_config()
        create_email_config()
        create_social_providers()
        create_app_configs()
        create_environment_variables()
        
        print()
        print("✅ Dados iniciais criados com sucesso!")
        print()
        print("📋 Resumo:")
        print(f"   • Configurações do sistema: {SystemConfig.objects.count()}")
        print(f"   • Configurações de email: {EmailConfig.objects.count()}")
        print(f"   • Provedores sociais: {SocialProviderConfig.objects.count()}")
        print(f"   • Configurações de apps: {AppConfig.objects.count()}")
        print(f"   • Variáveis de ambiente: {EnvironmentVariable.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
