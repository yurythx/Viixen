class CompanyModuleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and hasattr(user, 'company') and user.company:
            request.company = user.company
            request.active_modules = set(
                user.company.companymodule_set.filter(is_active=True)
                .values_list('module__app_label', flat=True)
            )
        else:
            request.company = None
            request.active_modules = set()
        
        return self.get_response(request)