from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin


class SessionSecurityMiddleware(MiddlewareMixin):
    """
    Middleware para garantir segurança de sessão e prevenir acesso a páginas protegidas
    após logout usando o botão voltar do navegador.
    """

    def process_response(self, request, response):
        # Adicionar cabeçalhos de segurança para todas as respostas
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'

        # Para páginas que requerem autenticação, adicionar cabeçalhos anti-cache
        if request.user.is_authenticated:
            # Adicionar cabeçalhos para prevenir cache em páginas protegidas
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response

    def process_request(self, request):
        # Verificar se a sessão expirou para usuários que têm cookie de sessão
        # mas a sessão foi invalidada no servidor
        if not request.user.is_authenticated and request.COOKIES.get(settings.SESSION_COOKIE_NAME):
            # Lista de prefixos de URLs protegidas
            protected_urls = [
                '/accounts/profile',
                '/accounts/admin',
                '/accounts/password_change',
                '/config/',
                '/articles/create',
                '/articles/edit',
                '/articles/delete',
            ]

            # Verificar se estamos tentando acessar uma página protegida
            for protected_url in protected_urls:
                if request.path.startswith(protected_url):
                    messages.warning(request, 'Sua sessão expirou. Por favor, faça login novamente.')
                    return redirect('accounts:login')

        return None
