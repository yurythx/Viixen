"""
Script para testar importações
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Tentar importar os serviços
try:
    from core.services.article_service import article_service, comment_service
    print("Importação dos serviços bem-sucedida!")
    print(f"article_service: {article_service}")
    print(f"comment_service: {comment_service}")
except Exception as e:
    print(f"Erro ao importar serviços: {e}")

# Tentar importar os repositórios
try:
    from core.repositories.article_repository import article_repository, comment_repository
    print("Importação dos repositórios bem-sucedida!")
    print(f"article_repository: {article_repository}")
    print(f"comment_repository: {comment_repository}")
except Exception as e:
    print(f"Erro ao importar repositórios: {e}")

# Tentar importar os serviços através do módulo apps.articles.services
try:
    from apps.articles.services import article_service as app_article_service
    from apps.articles.services import comment_service as app_comment_service
    print("Importação dos serviços através do app bem-sucedida!")
    print(f"app_article_service: {app_article_service}")
    print(f"app_comment_service: {app_comment_service}")
except Exception as e:
    print(f"Erro ao importar serviços através do app: {e}")

print("Teste de importações concluído!")
