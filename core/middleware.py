class CompanyModuleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        
        # Verificar se é superadmin ou membro do grupo Administrador
        request.is_global_admin = False
        if user.is_authenticated:
            request.is_global_admin = (
                user.is_superuser or 
                user.groups.filter(name='Administrador').exists()
            )
        
        # Se é admin global, tem acesso a tudo
        if request.is_global_admin:
            request.company = None  # Pode ver todas as empresas
            request.active_modules = set()  # Todos os módulos disponíveis
            request.can_access_all_companies = True
        elif user.is_authenticated and hasattr(user, 'company') and user.company:
            request.company = user.company
            request.active_modules = set(
                user.company.companymodule_set.filter(is_active=True)
                .values_list('module__app_label', flat=True)
            )
            request.can_access_all_companies = False
        else:
            request.company = None
            request.active_modules = set()
            request.can_access_all_companies = False
        
        return self.get_response(request)