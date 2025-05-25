#!/usr/bin/env python
"""
Script para criar um superusuário automaticamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """Criar superusuário"""
    username = 'admin'
    email = 'admin@viixen.com'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"ℹ️ Superusuário '{username}' já existe")
        return
    
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print(f"✅ Superusuário criado com sucesso!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print()
    print("🔗 Acesse: http://localhost:8000/admin/")
    print("🔗 Config: http://localhost:8000/config/")

if __name__ == '__main__':
    create_superuser()
