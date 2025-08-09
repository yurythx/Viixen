from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.urls import reverse_lazy

from ..domain.module import Module, CompanyModule
from ..domain.company import Company
from ..services.company_service import CompanyService
from core.mixins import GlobalAdminRequiredMixin, CompanyAdminRequiredMixin


class ModuleGlobalListView(LoginRequiredMixin, GlobalAdminRequiredMixin, ListView):
    """
    View para gerenciamento global de módulos (apenas superadmin/admin)
    """
    model = Module
    template_name = 'config/modules/global_list.html'
    context_object_name = 'modules'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CompanyService()
        
        context.update({
            'core_modules': service.get_core_modules(),
            'optional_modules': service.get_optional_modules(),
            'total_companies': Company.objects.count(),
            'is_global_admin': True,
        })
        return context


class ModuleGlobalToggleView(LoginRequiredMixin, GlobalAdminRequiredMixin, View):
    """
    View para ativar/desativar módulos globalmente (apenas superadmin/admin)
    """
    
    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        
        # Não permitir desativar módulos core
        if module.is_core and request.POST.get('action') == 'deactivate':
            messages.error(request, f'O módulo "{module.name}" é core e não pode ser desativado.')
            return redirect('config:module_global_list')
        
        action = request.POST.get('action')
        if action == 'activate':
            module.is_active = True
            module.save()
            messages.success(request, f'Módulo "{module.name}" ativado globalmente.')
        elif action == 'deactivate':
            module.is_active = False
            module.save()
            # Desativar para todas as empresas também
            CompanyModule.objects.filter(module=module).update(is_active=False)
            messages.success(request, f'Módulo "{module.name}" desativado globalmente.')
        
        return redirect('config:module_global_list')


class CompanyModuleListView(LoginRequiredMixin, CompanyAdminRequiredMixin, ListView):
    """
    View para gerenciamento de módulos da empresa
    """
    model = Module
    template_name = 'config/modules/company_list.html'
    context_object_name = 'modules'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CompanyService()
        
        # Verificar se é admin global
        is_global_admin = (self.request.user.is_superuser or 
                          (hasattr(self.request.user, 'groups') and 
                           self.request.user.groups.filter(name='Administrador').exists()))
        
        if is_global_admin:
            # Admin global pode gerenciar qualquer empresa
            company = self.request.company if hasattr(self.request, 'company') else None
        else:
            # Admin de empresa só gerencia própria empresa
            company = self.request.user.company if hasattr(self.request.user, 'company') else None
        
        if company:
            # Módulos core (sempre ativos)
            core_modules = service.get_core_modules()
            
            # Buscar módulos opcionais disponíveis (ativos globalmente e licenciados)
            optional_modules = service.get_optional_modules()
            
            # Filtrar apenas módulos licenciados para a empresa
            licensed_modules = CompanyModule.objects.filter(
                company=company,
                module__in=optional_modules,
                is_licensed=True
            ).values_list('module', flat=True)
            
            optional_modules = optional_modules.filter(id__in=licensed_modules)
            
            # Buscar módulos ativos para a empresa
            active_company_modules = CompanyModule.objects.filter(
                company=company,
                is_active=True,
                module__is_active=True,
                is_licensed=True
            ).values_list('module_id', flat=True)
            
            context.update({
                'company': company,
                'core_modules': core_modules,
                'optional_modules': optional_modules,
                'active_module_ids': active_company_modules,
                'is_global_admin': is_global_admin,
            })
        
        return context


class CompanyModuleToggleView(LoginRequiredMixin, CompanyAdminRequiredMixin, View):
    """
    View para ativar/desativar módulos para uma empresa
    """
    
    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        service = CompanyService()
        
        # Verificar se é admin global
        is_global_admin = (request.user.is_superuser or 
                          (hasattr(request.user, 'groups') and 
                           request.user.groups.filter(name='Administrador').exists()))
        
        if is_global_admin:
            # Admin global pode gerenciar qualquer empresa
            company_id = request.POST.get('company_id')
            if company_id:
                company = get_object_or_404(Company, id=company_id)
            else:
                company = request.company if hasattr(request, 'company') else None
        else:
            # Admin de empresa só gerencia própria empresa
            company = request.user.company if hasattr(request.user, 'company') else None
        
        if not company:
            messages.error(request, 'Empresa não encontrada.')
            return redirect('config:company_module_list')
        
        # Não permitir desativar módulos core
        if module.is_core:
            messages.error(request, f'O módulo "{module.name}" é core e não pode ser desativado.')
            return redirect('config:company_module_list')
        
        # Verificar se módulo está ativo globalmente
        if not module.is_active:
            messages.error(request, f'O módulo "{module.name}" está desativado globalmente.')
            return redirect('config:company_module_list')
        
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            
            # Verificar se a empresa tem licença para o módulo
            if not company_module.is_licensed:
                messages.error(
                    request,
                    f'Sua empresa não possui licença para o módulo "{module.name}". '
                    'Entre em contato com o administrador do sistema.'
                )
                return redirect('config:company_module_list')
            
            # Alternar status
            company_module.is_active = not company_module.is_active
            company_module.save()
            
            status = 'ativado' if company_module.is_active else 'desativado'
            messages.success(
                request, 
                f'Módulo "{module.name}" {status} com sucesso!'
            )
        
        except CompanyModule.DoesNotExist:
            # Verificar se pode criar (módulo deve estar ativo globalmente)
            if not module.is_active:
                messages.error(
                    request,
                    f'O módulo "{module.name}" não está disponível no sistema.'
                )
                return redirect('config:company_module_list')
            
            # Criar registro licenciado e ativado (apenas se for admin global ou se já houver licença)
            if is_global_admin:
                CompanyModule.objects.create(
                    company=company,
                    module=module,
                    is_active=True,
                    is_licensed=True
                )
                messages.success(
                    request, 
                    f'Módulo "{module.name}" licenciado e ativado com sucesso!'
                )
            else:
                messages.error(
                    request,
                    f'Sua empresa não possui licença para o módulo "{module.name}". '
                    'Entre em contato com o administrador do sistema.'
                )
        
        return redirect('config:company_module_list')


class CompanyModuleToggleAjaxView(LoginRequiredMixin, CompanyAdminRequiredMixin, View):
    """
    View AJAX para toggle rápido de módulos
    """
    
    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        service = CompanyService()
        
        # Verificar se é admin global
        is_global_admin = (request.user.is_superuser or 
                          (hasattr(request.user, 'groups') and 
                           request.user.groups.filter(name='Administrador').exists()))
        
        if is_global_admin:
            company_id = request.POST.get('company_id')
            if company_id:
                company = get_object_or_404(Company, id=company_id)
            else:
                company = request.company if hasattr(request, 'company') else None
        else:
            company = request.user.company if hasattr(request.user, 'company') else None
        
        if not company:
            return JsonResponse({'success': False, 'message': 'Empresa não encontrada.'})
        
        # Verificar se módulo pode ser alterado
        if module.is_core:
            return JsonResponse({'success': False, 'message': 'Módulos core não podem ser desativados.'})
        
        if not module.is_active:
            return JsonResponse({'success': False, 'message': 'Módulo desativado globalmente.'})
        
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            
            # Verificar se a empresa tem licença para o módulo
            if not company_module.is_licensed:
                return JsonResponse({
                    'success': False,
                    'message': f'Sua empresa não possui licença para o módulo "{module.name}".'
                })
            
            # Alternar status
            new_status = not company_module.is_active
            company_module.is_active = new_status
            company_module.save()
            
            return JsonResponse({
                'success': True,
                'is_active': new_status,
                'message': f'Módulo "{module.name}" {"ativado" if new_status else "desativado"} com sucesso!'
            })
        
        except CompanyModule.DoesNotExist:
            # Verificar se pode criar (apenas admin global pode licenciar automaticamente)
            if is_global_admin:
                CompanyModule.objects.create(
                    company=company,
                    module=module,
                    is_active=True,
                    is_licensed=True
                )
                
                return JsonResponse({
                    'success': True,
                    'is_active': True,
                    'message': f'Módulo "{module.name}" licenciado e ativado com sucesso!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'Sua empresa não possui licença para o módulo "{module.name}".'
                })
