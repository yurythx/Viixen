from django import template
from django.contrib.auth.models import AnonymousUser
from modules.config.domain.module import Module, CompanyModule

register = template.Library()


@register.simple_tag
def is_module_active(user, module_app_label):
    """
    Verifica se um módulo está ativo para o usuário/empresa
    
    Usage: {% is_module_active user 'modules.blog' as blog_active %}
    """
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return False
    
    # Superadmins e admins globais têm acesso a tudo
    if user.is_superuser or getattr(user, 'is_global_admin', False):
        return True
    
    try:
        module = Module.objects.get(app_label=module_app_label)
        
        # Módulos core estão sempre ativos
        if module.is_core:
            return True
        
        # Verificar se o módulo está ativo globalmente
        if not module.is_active:
            return False
        
        # Verificar se o usuário tem empresa
        if not user.company:
            return False
        
        # Verificar se o módulo está licenciado e ativo para a empresa
        try:
            company_module = CompanyModule.objects.get(
                company=user.company,
                module=module
            )
            return (company_module.is_licensed and 
                    company_module.is_active and 
                    not company_module.is_license_expired)
        except CompanyModule.DoesNotExist:
            return False
            
    except Module.DoesNotExist:
        return False


@register.simple_tag
def get_active_modules(user):
    """
    Retorna lista de módulos ativos para o usuário
    
    Usage: {% get_active_modules user as active_modules %}
    """
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return []
    
    # Superadmins e admins globais veem todos os módulos ativos
    if user.is_superuser or getattr(user, 'is_global_admin', False):
        return Module.objects.filter(is_active=True).order_by('order', 'name')
    
    # Usuários sem empresa só veem módulos core
    if not user.company:
        return Module.objects.filter(is_core=True, is_active=True).order_by('order', 'name')
    
    # Buscar módulos ativos para a empresa
    active_modules = []
    
    # Adicionar módulos core (sempre ativos)
    core_modules = Module.objects.filter(is_core=True, is_active=True)
    active_modules.extend(core_modules)
    
    # Adicionar módulos opcionais licenciados e ativos para a empresa
    company_modules = CompanyModule.objects.filter(
        company=user.company,
        is_licensed=True,
        is_active=True,
        module__is_active=True,
        module__is_core=False
    ).select_related('module')
    
    for company_module in company_modules:
        active_modules.append(company_module.module)
    
    # Ordenar por ordem e nome
    return sorted(active_modules, key=lambda m: (m.order, m.name))


@register.simple_tag
def get_module_count(user, module_type='all'):
    """
    Retorna contagem de módulos por tipo
    
    Usage: 
    {% get_module_count user 'active' as active_count %}
    {% get_module_count user 'core' as core_count %}
    {% get_module_count user 'optional' as optional_count %}
    {% get_module_count user 'licensed' as licensed_count %}
    {% get_module_count user 'available' as available_count %}
    """
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return 0
    
    if module_type == 'core':
        return Module.objects.filter(is_core=True, is_active=True).count()
    
    elif module_type == 'optional':
        if user.is_superuser or getattr(user, 'is_global_admin', False):
            return Module.objects.filter(is_core=False, is_active=True).count()
        elif user.company:
            return CompanyModule.objects.filter(
                company=user.company,
                is_licensed=True,
                is_active=True,
                module__is_active=True,
                module__is_core=False
            ).count()
        else:
            return 0
    
    elif module_type == 'active':
        active_modules = get_active_modules(user)
        return len(active_modules)
    
    elif module_type == 'all':
        if user.is_superuser or getattr(user, 'is_global_admin', False):
            return Module.objects.filter(is_active=True).count()
        else:
            active_modules = get_active_modules(user)
            return len(active_modules)
    
    return 0


@register.inclusion_tag('config/includes/module_status_badge.html')
def module_status_badge(module, user=None):
    """
    Renderiza badge de status do módulo
    
    Usage: {% module_status_badge module user %}
    """
    context = {
        'module': module,
        'is_core': module.is_core,
        'is_active': module.is_active,
    }
    
    if user and not isinstance(user, AnonymousUser) and user.is_authenticated:
        if user.company and not module.is_core:
            try:
                company_module = CompanyModule.objects.get(
                    company=user.company,
                    module=module
                )
                context['is_active_for_company'] = company_module.is_active
            except CompanyModule.DoesNotExist:
                context['is_active_for_company'] = False
        else:
            context['is_active_for_company'] = module.is_core
    
    return context


@register.inclusion_tag('config/components/license_alerts.html', takes_context=True)
def license_expiration_alerts(context):
    """Exibe alertas de licenças expirando ou expiradas"""
    user = context['user']
    
    # Apenas para admins globais
    if not (user.is_superuser or user.groups.filter(name='Administrador').exists()):
        return {'show_alerts': False}
    
    # Import local para evitar circular imports
    from django.utils import timezone
    from datetime import timedelta
    
    # Query direta para melhor performance
    expiring_soon = CompanyModule.objects.filter(
        is_licensed=True,
        license_expires_at__isnull=False,
        license_expires_at__lte=timezone.now() + timedelta(days=7),
        license_expires_at__gt=timezone.now()
    ).select_related('company', 'module')[:5]
    
    expired = CompanyModule.objects.filter(
        is_licensed=True,
        license_expires_at__isnull=False,
        license_expires_at__lte=timezone.now()
    ).select_related('company', 'module')[:5]
    
    expiring_count = CompanyModule.objects.filter(
        is_licensed=True,
        license_expires_at__isnull=False,
        license_expires_at__lte=timezone.now() + timedelta(days=7),
        license_expires_at__gt=timezone.now()
    ).count()
    
    expired_count = CompanyModule.objects.filter(
        is_licensed=True,
        license_expires_at__isnull=False,
        license_expires_at__lte=timezone.now()
    ).count()
    
    return {
        'show_alerts': expiring_count > 0 or expired_count > 0,
        'expiring_count': expiring_count,
        'expired_count': expired_count,
        'expiring_licenses': expiring_soon,
        'expired_licenses': expired,
    }
