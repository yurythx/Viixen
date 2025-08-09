from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import GlobalAdminRequiredMixin
from modules.config.domain.module import Module, CompanyModule
from modules.config.domain.company import Company
from modules.config.services.company_service import CompanyService


class ModuleLicensingView(LoginRequiredMixin, GlobalAdminRequiredMixin, ListView):
    """
    View para gerenciar licenças de módulos por empresa (apenas superadmin/admin)
    """
    template_name = 'config/modules/licensing.html'
    context_object_name = 'modules'
    
    def get_queryset(self):
        return Module.objects.filter(is_core=False).order_by('order', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CompanyService()
        
        # Estatísticas
        context['total_companies'] = Company.objects.filter(is_active=True).count()
        context['total_optional_modules'] = self.get_queryset().count()
        
        # Dados para cada módulo
        modules_data = []
        for module in self.get_queryset():
            licensed_companies = service.get_licensed_companies_for_module(module)
            unlicensed_companies = service.get_unlicensed_companies_for_module(module)
            
            modules_data.append({
                'module': module,
                'licensed_companies': licensed_companies,
                'unlicensed_companies': unlicensed_companies,
                'licensed_count': licensed_companies.count(),
                'unlicensed_count': unlicensed_companies.count(),
            })
        
        context['modules_data'] = modules_data
        context['all_companies'] = Company.objects.filter(is_active=True).order_by('name')
        
        # Calcular total de licenças ativas
        total_licenses = sum(data['licensed_count'] for data in modules_data)
        context['total_licenses'] = total_licenses
        
        return context


class ModuleLicenseDetailView(LoginRequiredMixin, GlobalAdminRequiredMixin, View):
    """
    View para gerenciar licenças de um módulo específico
    """
    template_name = 'config/modules/license_detail.html'
    
    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, is_core=False)
        service = CompanyService()
        
        licensed_companies = service.get_licensed_companies_for_module(module)
        unlicensed_companies = service.get_unlicensed_companies_for_module(module)
        
        context = {
            'module': module,
            'licensed_companies': licensed_companies,
            'unlicensed_companies': unlicensed_companies,
            'licensed_count': licensed_companies.count(),
            'unlicensed_count': unlicensed_companies.count(),
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, is_core=False)
        service = CompanyService()
        action = request.POST.get('action')
        
        if action == 'license_companies':
            company_ids = request.POST.getlist('company_ids')
            if company_ids:
                licensed_count = service.bulk_license_module(module, company_ids)
                messages.success(
                    request, 
                    f'Módulo "{module.name}" licenciado para {licensed_count} empresa(s).'
                )
            else:
                messages.warning(request, 'Nenhuma empresa selecionada.')
        
        elif action == 'revoke_licenses':
            company_ids = request.POST.getlist('company_ids')
            if company_ids:
                revoked_count = service.bulk_revoke_module_license(module, company_ids)
                messages.success(
                    request, 
                    f'Licença do módulo "{module.name}" removida de {revoked_count} empresa(s).'
                )
            else:
                messages.warning(request, 'Nenhuma empresa selecionada.')
        
        return redirect('config:module_license_detail', module_id=module_id)


class CompanyLicenseToggleView(LoginRequiredMixin, GlobalAdminRequiredMixin, View):
    """
    View para alternar licença de um módulo para uma empresa específica
    """
    
    def post(self, request, module_id, company_id):
        module = get_object_or_404(Module, id=module_id, is_core=False)
        company = get_object_or_404(Company, id=company_id, is_active=True)
        service = CompanyService()
        
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            
            if company_module.is_licensed:
                # Remover licença
                if service.revoke_module_license(company, module):
                    messages.success(
                        request, 
                        f'Licença do módulo "{module.name}" removida da empresa "{company.name}".'
                    )
                else:
                    messages.error(request, 'Erro ao remover licença.')
            else:
                # Adicionar licença
                if service.license_module_for_company(company, module):
                    messages.success(
                        request, 
                        f'Módulo "{module.name}" licenciado para a empresa "{company.name}".'
                    )
                else:
                    messages.error(request, 'Erro ao licenciar módulo.')
        
        except CompanyModule.DoesNotExist:
            # Criar licença
            if service.license_module_for_company(company, module):
                messages.success(
                    request, 
                    f'Módulo "{module.name}" licenciado para a empresa "{company.name}".'
                )
            else:
                messages.error(request, 'Erro ao licenciar módulo.')
        
        # Redirecionar de volta
        return redirect(request.META.get('HTTP_REFERER', 'config:module_licensing'))


class CompanyLicenseAjaxToggleView(LoginRequiredMixin, GlobalAdminRequiredMixin, View):
    """
    View AJAX para alternar licença de módulo para empresa
    """
    
    def post(self, request, module_id, company_id):
        module = get_object_or_404(Module, id=module_id, is_core=False)
        company = get_object_or_404(Company, id=company_id, is_active=True)
        service = CompanyService()
        
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            
            # Alternar status da licença
            new_license_status = not company_module.is_licensed
            
            if new_license_status:
                success = service.license_module_for_company(company, module)
                message = f'Módulo "{module.name}" licenciado para "{company.name}"'
            else:
                success = service.revoke_module_license(company, module)
                message = f'Licença do módulo "{module.name}" removida de "{company.name}"'
            
            if success:
                return JsonResponse({
                    'success': True,
                    'is_licensed': new_license_status,
                    'message': message
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro ao alterar licença do módulo'
                })
        
        except CompanyModule.DoesNotExist:
            # Criar licença
            if service.license_module_for_company(company, module):
                return JsonResponse({
                    'success': True,
                    'is_licensed': True,
                    'message': f'Módulo "{module.name}" licenciado para "{company.name}"'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro ao licenciar módulo'
                })
