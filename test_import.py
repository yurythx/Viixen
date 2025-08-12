import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

try:
    from core.mixins import GlobalAdminRequiredMixin
    print("Importação bem-sucedida!")
    print(f"GlobalAdminRequiredMixin: {GlobalAdminRequiredMixin}")
except ImportError as e:
    print(f"Erro ao importar: {e}")
    print("\nTentando importar diretamente do módulo...")
    try:
        from core.mixins.company_mixins import GlobalAdminRequiredMixin
        print("Importação direta bem-sucedida!")
        print(f"GlobalAdminRequiredMixin: {GlobalAdminRequiredMixin}")
    except ImportError as e2:
        print(f"Erro na importação direta: {e2}")
        print("\nConteúdo do diretório core/mixins:")
        print(os.listdir(os.path.join(os.path.dirname(__file__), 'core', 'mixins')))