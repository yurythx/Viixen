from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta, datetime
from core.mixins import GlobalAdminRequiredMixin
from modules.config.domain.module import Module, CompanyModule
from modules.config.domain.company import Company
from modules.config.services.company_service import CompanyService


class LicenseExpirationView(LoginRequiredMixin, GlobalAdminRequiredMixin, ListView):
    """
    View para gerenciar expiração de licenças (apenas superadmin/admin)
    """
    template_name = 'config/modules/expiration.html'
    context_object_name = 'expiring_licenses'
    
    def get_queryset(self):
        service = CompanyService()
        return service.get_expiring_licenses(days_ahead=30)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CompanyService()
        
        # Estatísticas de expiração
        context['expiring_licenses'] = service.get_expiring_licenses(days_ahead=30)
        context['expired_licenses'] = service.get_expired_licenses()
        context['expiring_count'] = context['expiring_licenses'].count()
        context['expired_count'] = context['expired_licenses'].count()
        
        # Licenças por período
        context['expiring_7_days'] = service.get_expiring_licenses(days_ahead=7).count()
        context['expiring_15_days'] = service.get_expiring_licenses(days_ahead=15).count()
        context['expiring_30_days'] = service.get_expiring_licenses(days_ahead=30).count()
        
        return context


class LicenseRenewalView(LoginRequiredMixin, GlobalAdminRequiredMixin, View):
    """
    View para renovar licenças específicas
    """
    
    def post(self, request, module_id, company_id):
        module = get_object_or_404(Module, id=module_id, is_core=False)
        company = get_object_or_404(Company, id=company_id, is_active=True)
        service = CompanyService()
        
        duration_days = int(request.POST.get('duration_days', 365))
        
        if service.renew_license(company, module, duration_days):
            messages.success(
                request,
                f'Licença do módulo "{module.name}" renovada por {duration_days} dias '
                f'para a empresa "{company.name}".'
            )
        else:
            messages.error(request, 'Erro ao renovar licença.')
        
        return redirect(request.META.get('HTTP_REFERER', 'config:license_expiration'))


class BulkLicenseRenewalView(LoginRequiredMixin, GlobalAdminRequiredMixin, View):
    """
    View para renovação em massa de licenças
    """
    
    def post(self, request):
        service = CompanyService()
        action = request.POST.get('action')
        
        if action == 'renew_expiring':
            # Renovar licenças que expiram em 30 dias
            expiring_licenses = service.get_expiring_licenses(days_ahead=30)
            duration_days = int(request.POST.get('duration_days', 365))
            renewed_count = 0
            
            for company_module in expiring_licenses:
                if service.renew_license(company_module.company, company_module.module, duration_days):
                    renewed_count += 1
            
            messages.success(
                request,
                f'{renewed_count} licença(s) renovada(s) por {duration_days} dias.'
            )
        
        elif action == 'deactivate_expired':
            # Desativar licenças expiradas
            deactivated_count = service.auto_deactivate_expired_licenses()
            messages.success(
                request,
                f'{deactivated_count} módulo(s) desativado(s) por licença expirada.'
            )
        
        return redirect('config:license_expiration')


class LicenseExpirationAjaxView(LoginRequiredMixin, GlobalAdminRequiredMixin, View):
    """
    View AJAX para ações de expiração de licenças
    """
    
    def post(self, request):
        service = CompanyService()
        action = request.POST.get('action')
        
        if action == 'check_expiring':
            # Verificar licenças expirando
            expiring_count = service.get_expiring_licenses(days_ahead=7).count()
            expired_count = service.get_expired_licenses().count()
            
            return JsonResponse({
                'success': True,
                'expiring_count': expiring_count,
                'expired_count': expired_count,
                'has_alerts': expiring_count > 0 or expired_count > 0
            })
        
        elif action == 'renew_license':
            module_id = request.POST.get('module_id')
            company_id = request.POST.get('company_id')
            duration_days = int(request.POST.get('duration_days', 365))
            
            try:
                module = Module.objects.get(id=module_id, is_core=False)
                company = Company.objects.get(id=company_id, is_active=True)
                
                if service.renew_license(company, module, duration_days):
                    return JsonResponse({
                        'success': True,
                        'message': f'Licença renovada por {duration_days} dias'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Erro ao renovar licença'
                    })
            except (Module.DoesNotExist, Company.DoesNotExist):
                return JsonResponse({
                    'success': False,
                    'message': 'Módulo ou empresa não encontrado'
                })
        
        return JsonResponse({
            'success': False,
            'message': 'Ação não reconhecida'
        })
