from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

@require_POST
@ensure_csrf_cookie
def ajax_login(request):
    """
    View para lidar com solicitações de login via AJAX.
    Retorna JSON com status de sucesso/erro e URL de redirecionamento se bem-sucedido.
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if not username or not password:
        return JsonResponse({
            'success': False,
            'error': 'Por favor, forneça nome de usuário e senha.'
        }, status=400)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        # Determinar URL de redirecionamento com base no tipo de usuário
        redirect_url = request.GET.get('next', '/')
        
        return JsonResponse({
            'success': True,
            'redirect_url': redirect_url
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Nome de usuário ou senha incorretos.'
        }, status=401)

def get_csrf_token(request):
    """
    View para obter um token CSRF.
    Útil para aplicativos que precisam obter um token antes de fazer solicitações POST.
    """
    token = get_token(request)
    return JsonResponse({'csrfToken': token})