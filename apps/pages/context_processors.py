"""
Context processors para o app pages.
Fornece variáveis globais para todos os templates.
"""

from django.conf import settings


def layout_context(request):
    """
    Context processor que fornece informações de layout e tema.
    """
    return {
        'current_theme': getattr(settings, 'CURRENT_THEME', 'default'),
        'site_name': getattr(settings, 'SITE_NAME', 'Viixen'),
        'site_description': getattr(settings, 'SITE_DESCRIPTION', 'Sistema de Gerenciamento'),
        'layout_config': {
            'show_sidebar': True,
            'show_footer': True,
            'show_breadcrumb': True,
            'container_fluid': True,
        }
    }


def app_context(request):
    """
    Context processor que fornece informações sobre apps ativos.
    """
    try:
        from apps.config.models import AppConfig
        
        # Obter apps ativos
        active_apps = AppConfig.objects.filter(is_active=True).values_list('name', flat=True)
        
        return {
            'active_apps': list(active_apps),
            'app_count': AppConfig.objects.count(),
            'active_app_count': AppConfig.objects.filter(is_active=True).count(),
        }
    except Exception:
        # Em caso de erro (ex: tabelas não criadas ainda), retornar valores padrão
        return {
            'active_apps': [],
            'app_count': 0,
            'active_app_count': 0,
        }


def navigation_context(request):
    """
    Context processor que fornece informações de navegação.
    """
    # Determinar se estamos em uma área administrativa
    is_admin_area = False
    if request.resolver_match:
        namespace = request.resolver_match.namespace
        is_admin_area = namespace in ['config', 'admin'] or (
            hasattr(request.user, 'is_staff') and request.user.is_staff
        )
    
    return {
        'is_admin_area': is_admin_area,
        'current_namespace': request.resolver_match.namespace if request.resolver_match else None,
        'current_url_name': request.resolver_match.url_name if request.resolver_match else None,
    }
