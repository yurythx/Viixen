from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from modules.config.domain.module import Module, CompanyModule


class ModuleAccessMiddleware:
    """
    Middleware para verificar se os módulos estão ativos antes de permitir acesso
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que não devem ser verificadas
        self.exempt_urls = [
            '/admin/',
            '/accounts/login/',
            '/accounts/logout/',
            '/static/',
            '/media/',
            '/config/dashboard/',
            '/config/company/',
            '/config/modules/',
            '/config/companies/',
        ]
        
        # Mapeamento de apps para módulos
        self.app_module_mapping = {
            'blog': 'modules.blog',
            'pages': 'modules.pages',
            'accounts': 'modules.accounts',
            'config': 'modules.config',
        }

    def __call__(self, request):
        # Verificar se a URL deve ser verificada
        if self.should_check_module_access(request):
            # Verificar acesso ao módulo
            if not self.check_module_access(request):
                # Redirecionar para dashboard com mensagem de erro
                messages.error(
                    request, 
                    'Este módulo não está disponível para sua empresa.'
                )
                return redirect('config:dashboard')
        
        response = self.get_response(request)
        return response

    def should_check_module_access(self, request):
        """
        Verifica se a URL deve ter o acesso ao módulo verificado
        """
        path = request.path
        
        # Não verificar URLs isentas
        for exempt_url in self.exempt_urls:
            if path.startswith(exempt_url):
                return False
        
        # Não verificar se usuário não está autenticado
        if not request.user.is_authenticated:
            return False
        
        # Não verificar para superadmins ou admins globais
        if (request.user.is_superuser or 
            hasattr(request, 'is_global_admin') and request.is_global_admin):
            return False
        
        return True

    def check_module_access(self, request):
        """
        Verifica se o usuário tem acesso ao módulo baseado na URL
        """
        path = request.path
        
        # Determinar qual módulo está sendo acessado
        app_name = self.get_app_from_path(path)
        if not app_name:
            return True  # Se não conseguir determinar o app, permitir acesso
        
        # Buscar o módulo correspondente
        module_app_label = self.app_module_mapping.get(app_name)
        if not module_app_label:
            return True  # Se não houver mapeamento, permitir acesso
        
        try:
            module = Module.objects.get(app_label=module_app_label)
            
            # Módulos core estão sempre disponíveis
            if module.is_core:
                return True
            
            # Verificar se o módulo está ativo globalmente
            if not module.is_active:
                return False
            
            # Verificar se o usuário tem empresa
            if not request.user.company:
                return False
            
            # Verificar se o módulo está ativo e licenciado para a empresa do usuário
            try:
                company_module = CompanyModule.objects.get(
                    company=request.user.company,
                    module=module
                )
                # Módulo deve estar licenciado, ativo e não expirado para a empresa
                return (company_module.is_licensed and 
                        company_module.is_active and 
                        not company_module.is_license_expired)
            except CompanyModule.DoesNotExist:
                # Se não existe registro, o módulo não está disponível para a empresa
                return False
                
        except Module.DoesNotExist:
            # Se o módulo não existe, permitir acesso
            return True

    def get_app_from_path(self, path):
        """
        Extrai o nome do app da URL
        """
        path_parts = path.strip('/').split('/')
        if path_parts:
            return path_parts[0]
        return None
