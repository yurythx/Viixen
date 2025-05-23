from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from .models import SocialProviderConfig, EmailConfig, SystemConfig, AppConfig
from .forms import SocialProviderConfigForm, EmailConfigForm, SystemConfigForm, AppConfigForm

@method_decorator(staff_member_required, name='dispatch')
class ConfigView(TemplateView):
    template_name = 'config/config.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_config'] = SystemConfig.objects.first()
        context['app_count'] = AppConfig.objects.count()
        context['active_app_count'] = AppConfig.objects.filter(is_active=True).count()

        # Verificar se o usuário é admin ou superuser para mostrar configurações avançadas
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            context['is_admin'] = True
            context['social_providers'] = SocialProviderConfig.objects.all()
            context['email_config'] = EmailConfig.objects.first()
            context['ldap_config'] = None

            # Verificar se o app LDAP está instalado
            try:
                from apps.config.models import LDAPConfig
                context['ldap_config'] = LDAPConfig.objects.first()
            except ImportError:
                pass
        else:
            context['is_admin'] = False

        return context

@method_decorator(staff_member_required, name='dispatch')
class SocialProviderConfigUpdateView(UpdateView):
    model = SocialProviderConfig
    form_class = SocialProviderConfigForm
    template_name = 'config/social_provider_form.html'
    success_url = reverse_lazy('config:config')

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário é admin ou superuser
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('config:config')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Configurações do provedor social atualizadas com sucesso!')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class EmailConfigUpdateView(UpdateView):
    model = EmailConfig
    form_class = EmailConfigForm
    template_name = 'config/email_config_form.html'
    success_url = reverse_lazy('config:config')

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário é admin ou superuser
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('config:config')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Configurações de email atualizadas com sucesso!')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class SystemConfigUpdateView(UpdateView):
    model = SystemConfig
    form_class = SystemConfigForm
    template_name = 'config/system_config_form.html'
    success_url = reverse_lazy('config:config')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Se o usuário não for admin ou superuser, remover campos avançados
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            if 'enable_app_management' in form.fields:
                form.fields.pop('enable_app_management')
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Configurações do sistema atualizadas com sucesso!')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class AppConfigListView(ListView):
    model = AppConfig
    template_name = 'config/app_config_list.html'
    context_object_name = 'apps'

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o gerenciamento de apps está ativado
        system_config = SystemConfig.objects.first()
        if system_config and not system_config.enable_app_management:
            messages.warning(request, "O gerenciamento de módulos está desativado nas configurações do sistema.")
            return redirect('config:config')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(staff_member_required, name='dispatch')
class AppConfigUpdateView(UpdateView):
    model = AppConfig
    form_class = AppConfigForm
    template_name = 'config/app_config_form.html'
    success_url = reverse_lazy('config:app-list')

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o gerenciamento de apps está ativado
        system_config = SystemConfig.objects.first()
        if system_config and not system_config.enable_app_management:
            messages.warning(request, "O gerenciamento de módulos está desativado nas configurações do sistema.")
            return redirect('config:config')

        # Verificar se o usuário está tentando editar um app core
        app = self.get_object()
        if app.is_core and not request.user.is_superuser:
            messages.error(request, f"O módulo '{app.name}' é um módulo core e só pode ser editado por superusuários.")
            return redirect('config:app-list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'Configurações do app {form.instance.name} atualizadas com sucesso!')
        return super().form_valid(form)

class ModuleDisabledTestView(View):
    """
    View para testar a exibição da página de módulo desabilitado.
    Útil para administradores verificarem como a página aparece para os usuários.
    """
    def get(self, request):
        context = {
            'module_name': 'Teste',
            'module_label': 'test',
            'user': request.user
        }
        return render(request, 'config/module_disabled.html', context)