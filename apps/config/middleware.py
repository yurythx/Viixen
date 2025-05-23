from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import resolve, Resolver404
from django.template.response import TemplateResponse
from .models import AppConfig

class AppControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Ignorar admin, accounts, config e pages (páginas essenciais)
            if (request.path.startswith('/admin/') or
                request.path.startswith('/accounts/') or
                request.path.startswith('/config/') or
                request.path.startswith('/') and request.path == '/'):  # Rota raiz (home)
                return self.get_response(request)

            # Resolver a URL para obter o app
            resolver_match = resolve(request.path)
            app_name = resolver_match.app_name.split('.')[1] if '.' in resolver_match.app_name else resolver_match.app_name

            # Verificar se o app está ativo
            try:
                app_config = AppConfig.objects.get(label=app_name)
                if not app_config.is_active:
                    # Em vez de redirecionar, mostrar um template informativo
                    context = {
                        'module_name': app_config.name,
                        'module_label': app_config.label,
                        'user': request.user
                    }
                    # Usar render em vez de TemplateResponse para evitar erros de renderização
                    return render(
                        request,
                        'config/module_disabled.html',
                        context
                    )
            except AppConfig.DoesNotExist:
                # Se o app não estiver registrado, permitir o acesso (para compatibilidade)
                pass

        except Resolver404:
            # Se não conseguir resolver a URL, continuar normalmente
            pass

        return self.get_response(request)
