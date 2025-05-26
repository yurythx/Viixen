from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.db import models
from django.core.exceptions import PermissionDenied
from .models import (
    SocialProviderConfig, EmailConfig, SystemConfig, AppConfig, LDAPConfig,
    EnvironmentVariable, DatabaseConfig, Widget, MenuConfig, Plugin, ConfigBackup
)
from .forms import SocialProviderConfigForm, EmailConfigForm, SystemConfigForm, AppConfigForm, EnvironmentVariableForm, EnvironmentVariableFilterForm, DatabaseConfigForm, LDAPConfigForm

def staff_required(view_func):
    """Decorator personalizado que verifica se o usuário é staff e redireciona para o login correto."""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())

        if not request.user.is_staff:
            raise PermissionDenied("Você precisa ser um usuário staff para acessar esta página.")

        return view_func(request, *args, **kwargs)
    return _wrapped_view

@method_decorator(staff_required, name='dispatch')
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
            context['ldap_config'] = LDAPConfig.objects.first()

            # Estatísticas de Social Providers
            context['social_provider_count'] = SocialProviderConfig.objects.count()
            context['active_social_provider_count'] = SocialProviderConfig.objects.filter(is_active=True).count()

            # Estatísticas de Email
            context['email_config_count'] = EmailConfig.objects.count()
            context['active_email_config_count'] = EmailConfig.objects.filter(is_active=True).count()

            # Estatísticas de LDAP
            context['ldap_config_count'] = LDAPConfig.objects.count()
            context['active_ldap_config_count'] = LDAPConfig.objects.filter(is_active=True).count()

            # Estatísticas de Environment Variables
            context['env_variable_count'] = EnvironmentVariable.objects.count()
            context['active_env_variable_count'] = EnvironmentVariable.objects.filter(is_active=True).count()
            context['sensitive_env_variable_count'] = EnvironmentVariable.objects.filter(is_sensitive=True).count()

            # Estatísticas de Database Config
            context['database_config_count'] = DatabaseConfig.objects.count()
            context['active_database_config_count'] = DatabaseConfig.objects.filter(is_active=True).count()

            # Estatísticas de Widgets
            context['widget_count'] = Widget.objects.count()
            context['active_widget_count'] = Widget.objects.filter(is_active=True).count()

            # Estatísticas de Menus
            context['menu_count'] = MenuConfig.objects.count()
            context['active_menu_count'] = MenuConfig.objects.filter(is_active=True).count()

            # Estatísticas de Plugins
            context['plugin_count'] = Plugin.objects.count()
            context['active_plugin_count'] = Plugin.objects.filter(status='active').count()

            # Estatísticas de Backups
            context['backup_count'] = ConfigBackup.objects.count()
            context['protected_backup_count'] = ConfigBackup.objects.filter(is_protected=True).count()

            # Último backup
            last_backup = ConfigBackup.objects.order_by('-created_at').first()
            context['last_backup_date'] = last_backup.created_at if last_backup else None
        else:
            context['is_admin'] = False

        return context

@method_decorator(staff_required, name='dispatch')
class SocialProviderConfigListView(ListView):
    """View para listar provedores sociais"""
    model = SocialProviderConfig
    template_name = 'config/social_provider_list.html'
    context_object_name = 'social_providers'
    ordering = ['-is_active', 'provider']


@method_decorator(staff_required, name='dispatch')
class SocialProviderConfigCreateView(View):
    """View para criar novo provedor social"""
    template_name = 'config/social_provider_form.html'

    def get(self, request):
        form = SocialProviderConfigForm()
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})

    def post(self, request):
        form = SocialProviderConfigForm(request.POST)
        if form.is_valid():
            provider_config = form.save()
            messages.success(request, f'Provedor social "{provider_config.provider}" criado com sucesso!')
            return redirect('config:social-provider-list')
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})


@method_decorator(staff_required, name='dispatch')
class SocialProviderConfigUpdateView(UpdateView):
    model = SocialProviderConfig
    form_class = SocialProviderConfigForm
    template_name = 'config/social_provider_form.html'
    success_url = reverse_lazy('config:social-provider-list')

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário é admin ou superuser
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('config:config')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Configurações do provedor social atualizadas com sucesso!')
        return super().form_valid(form)

@method_decorator(staff_required, name='dispatch')
class EmailConfigListView(ListView):
    """View para listar configurações de email"""
    model = EmailConfig
    template_name = 'config/email_config_list.html'
    context_object_name = 'email_configs'
    ordering = ['-is_active', 'email_host']


@method_decorator(staff_required, name='dispatch')
class EmailConfigCreateView(View):
    """View para criar nova configuração de email"""
    template_name = 'config/email_config_form.html'

    def get(self, request):
        form = EmailConfigForm()
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})

    def post(self, request):
        form = EmailConfigForm(request.POST)
        if form.is_valid():
            email_config = form.save()
            messages.success(request, f'Configuração de email criada com sucesso!')
            return redirect('config:email-list')
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})


@method_decorator(staff_required, name='dispatch')
class EmailConfigUpdateView(UpdateView):
    model = EmailConfig
    form_class = EmailConfigForm
    template_name = 'config/email_config_form.html'
    success_url = reverse_lazy('config:email-list')

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário é admin ou superuser
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('config:config')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Retorna o objeto EmailConfig ou cria um se não existir"""
        try:
            return EmailConfig.objects.get(slug='email-config')
        except EmailConfig.DoesNotExist:
            # Criar configuração padrão se não existir
            return EmailConfig.objects.create(
                email_host='smtp.gmail.com',
                email_port=587,
                email_host_user='',
                email_host_password='',
                email_use_tls=True,
                default_from_email='noreply@example.com',
                is_active=False
            )

    def form_valid(self, form):
        messages.success(self.request, 'Configurações de email atualizadas com sucesso!')
        return super().form_valid(form)

@method_decorator(staff_required, name='dispatch')
class SystemConfigUpdateView(UpdateView):
    model = SystemConfig
    form_class = SystemConfigForm
    template_name = 'config/system_config_form.html'
    success_url = reverse_lazy('config:config')

    def get_object(self, queryset=None):
        """Retorna o objeto SystemConfig ou cria um se não existir"""
        try:
            return SystemConfig.objects.get(slug='system-config')
        except SystemConfig.DoesNotExist:
            # Criar configuração padrão se não existir
            return SystemConfig.objects.create(
                site_name='Viixen',
                site_description='Sistema de Gerenciamento Modular',
                maintenance_mode=False,
                allow_registration=True,
                require_email_verification=False,
                enable_app_management=True,
                theme='default',
                primary_color='#4361ee',
                secondary_color='#6c757d',
                accent_color='#f72585',
                sidebar_style='default',
                header_style='default',
                enable_dark_mode_toggle=True,
                enable_breadcrumbs=True,
                enable_search=True,
                enable_notifications=True,
                notification_position='top-right'
            )

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

@method_decorator(staff_required, name='dispatch')
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

@method_decorator(staff_required, name='dispatch')
class AppConfigCreateView(View):
    """View para criar nova configuração de app"""
    template_name = 'config/app_config_form.html'

    def get(self, request):
        form = AppConfigForm()
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})

    def post(self, request):
        form = AppConfigForm(request.POST)
        if form.is_valid():
            app_config = form.save()
            messages.success(request, f'Configuração do app "{app_config.name}" criada com sucesso!')
            return redirect('config:app-list')
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})


@method_decorator(staff_required, name='dispatch')
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


@method_decorator(staff_required, name='dispatch')
class EnvironmentVariableListView(ListView):
    """View para listar e filtrar variáveis de ambiente"""
    model = EnvironmentVariable
    template_name = 'config/environment_variables.html'
    context_object_name = 'variables'
    paginate_by = 20

    def get_queryset(self):
        queryset = EnvironmentVariable.objects.all()

        # Aplicar filtros
        form = EnvironmentVariableFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('category'):
                queryset = queryset.filter(category=form.cleaned_data['category'])

            if form.cleaned_data.get('var_type'):
                queryset = queryset.filter(var_type=form.cleaned_data['var_type'])

            if form.cleaned_data.get('is_required'):
                is_required = form.cleaned_data['is_required'] == 'true'
                queryset = queryset.filter(is_required=is_required)

            if form.cleaned_data.get('is_sensitive'):
                is_sensitive = form.cleaned_data['is_sensitive'] == 'true'
                queryset = queryset.filter(is_sensitive=is_sensitive)

            if form.cleaned_data.get('search'):
                search = form.cleaned_data['search']
                queryset = queryset.filter(
                    models.Q(key__icontains=search) |
                    models.Q(description__icontains=search)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = EnvironmentVariableFilterForm(self.request.GET)
        context['categories'] = EnvironmentVariable.CATEGORY_CHOICES

        # Adicionar estatísticas
        variables = context['variables']
        context['stats'] = {
            'total': variables.count() if hasattr(variables, 'count') else len(variables),
            'active': sum(1 for var in variables if var.is_active),
            'required': sum(1 for var in variables if var.is_required),
            'sensitive': sum(1 for var in variables if var.is_sensitive),
        }

        return context


@method_decorator(staff_required, name='dispatch')
class EnvironmentVariableCreateView(View):
    """View para criar nova variável de ambiente"""
    template_name = 'config/environment_variable_form.html'

    def get(self, request):
        form = EnvironmentVariableForm()
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})

    def post(self, request):
        form = EnvironmentVariableForm(request.POST)
        if form.is_valid():
            variable = form.save()
            messages.success(request, f'Variável {variable.key} criada com sucesso!')
            return redirect('config:env-variables')
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})


@method_decorator(staff_required, name='dispatch')
class EnvironmentVariableUpdateView(UpdateView):
    """View para editar variável de ambiente"""
    model = EnvironmentVariable
    form_class = EnvironmentVariableForm
    template_name = 'config/environment_variable_form.html'
    success_url = reverse_lazy('config:env-variables')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Variável {form.instance.key} atualizada com sucesso!')
        return super().form_valid(form)


@method_decorator(staff_required, name='dispatch')
class EnvironmentVariableDeleteView(View):
    """View para deletar variável de ambiente"""

    def post(self, request, pk):
        try:
            variable = EnvironmentVariable.objects.get(pk=pk)
            key = variable.key
            variable.delete()
            messages.success(request, f'Variável {key} removida com sucesso!')
        except EnvironmentVariable.DoesNotExist:
            messages.error(request, 'Variável não encontrada.')

        return redirect('config:env-variables')


@method_decorator(staff_required, name='dispatch')
class EnvironmentVariableExportView(View):
    """View para exportar variáveis como arquivo .env"""

    def get(self, request):
        variables = EnvironmentVariable.objects.filter(is_active=True).order_by('category', 'order', 'key')

        # Gerar conteúdo do arquivo .env
        content = self._generate_env_content(variables)

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=".env"'
        return response

    def _generate_env_content(self, variables):
        """Gera o conteúdo do arquivo .env"""
        content = []
        current_category = None

        for var in variables:
            # Adicionar separador de categoria
            if var.category != current_category:
                if current_category is not None:
                    content.append('')

                category_name = dict(EnvironmentVariable.CATEGORY_CHOICES).get(var.category, var.category)
                content.append(f'# {category_name.upper()}')
                content.append('# ' + '=' * (len(category_name) + 10))
                content.append('')
                current_category = var.category

            # Adicionar comentário com descrição
            if var.description:
                for line in var.description.split('\n'):
                    content.append(f'# {line.strip()}')

            # Adicionar a variável
            value = var.value if var.value else var.default_value
            if var.is_sensitive and value:
                value = 'your-secret-value-here'

            content.append(f'{var.key}={value}')
            content.append('')

        return '\n'.join(content)


@method_decorator(staff_required, name='dispatch')
class EnvironmentVariableImportView(View):
    """View para importar variáveis de um arquivo .env"""
    template_name = 'config/environment_variable_import.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if 'env_file' not in request.FILES:
            messages.error(request, 'Nenhum arquivo foi enviado.')
            return render(request, self.template_name)

        env_file = request.FILES['env_file']

        try:
            content = env_file.read().decode('utf-8')
            imported_count = self._import_env_content(content)
            messages.success(request, f'{imported_count} variáveis importadas com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao importar arquivo: {str(e)}')

        return redirect('config:env-variables')

    def _import_env_content(self, content):
        """Importa variáveis do conteúdo do arquivo .env"""
        imported_count = 0
        current_category = 'custom'

        for line in content.split('\n'):
            line = line.strip()

            # Pular linhas vazias e comentários
            if not line or line.startswith('#'):
                # Tentar extrair categoria dos comentários
                if line.startswith('# ') and '=' in line:
                    category_line = line[2:].strip()
                    if category_line.endswith('='):
                        # Mapear nome da categoria para código
                        category_map = {v.upper(): k for k, v in EnvironmentVariable.CATEGORY_CHOICES}
                        category_name = category_line[:-1].strip()
                        current_category = category_map.get(category_name, 'custom')
                continue

            # Processar linha de variável
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Criar ou atualizar variável
                variable, created = EnvironmentVariable.objects.get_or_create(
                    key=key,
                    defaults={
                        'value': value,
                        'category': current_category,
                        'description': f'Importado automaticamente',
                        'var_type': 'string',
                        'is_active': True,
                    }
                )

                if not created:
                    variable.value = value
                    variable.save()

                imported_count += 1

        return imported_count


@method_decorator(staff_required, name='dispatch')
class DatabaseConfigListView(ListView):
    """View para listar configurações de banco de dados"""
    model = DatabaseConfig
    template_name = 'config/database_config_list.html'
    context_object_name = 'database_configs'
    ordering = ['-is_default', 'name']


@method_decorator(staff_required, name='dispatch')
class DatabaseConfigCreateView(View):
    """View para criar nova configuração de banco"""
    template_name = 'config/database_config_form.html'

    def get(self, request):
        form = DatabaseConfigForm()
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})

    def post(self, request):
        form = DatabaseConfigForm(request.POST)
        if form.is_valid():
            database_config = form.save()
            messages.success(request, f'Configuração de banco "{database_config.name}" criada com sucesso!')
            return redirect('config:database-list')
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})


@method_decorator(staff_required, name='dispatch')
class DatabaseConfigUpdateView(UpdateView):
    """View para editar configuração de banco"""
    model = DatabaseConfig
    form_class = DatabaseConfigForm
    template_name = 'config/database_config_form.html'
    success_url = reverse_lazy('config:database-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Configuração "{form.instance.name}" atualizada com sucesso!')
        return super().form_valid(form)


@method_decorator(staff_required, name='dispatch')
class DatabaseConfigDeleteView(View):
    """View para deletar configuração de banco"""

    def post(self, request, pk):
        try:
            database_config = DatabaseConfig.objects.get(pk=pk)

            # Não permitir deletar configuração padrão
            if database_config.is_default:
                messages.error(request, 'Não é possível excluir a configuração padrão do banco de dados.')
                return redirect('config:database-list')

            name = database_config.name
            database_config.delete()
            messages.success(request, f'Configuração "{name}" removida com sucesso!')
        except DatabaseConfig.DoesNotExist:
            messages.error(request, 'Configuração não encontrada.')

        return redirect('config:database-list')


@method_decorator(staff_required, name='dispatch')
class DatabaseConfigTestView(View):
    """View para testar conexão com banco"""

    def post(self, request, pk):
        try:
            database_config = DatabaseConfig.objects.get(pk=pk)
            success, message = database_config.test_connection()

            if success:
                messages.success(request, f'Conexão testada com sucesso: {message}')
            else:
                messages.error(request, f'Erro na conexão: {message}')

        except DatabaseConfig.DoesNotExist:
            messages.error(request, 'Configuração não encontrada.')

        return redirect('config:database-list')


@method_decorator(staff_required, name='dispatch')
class LDAPConfigListView(ListView):
    """View para listar configurações LDAP"""
    model = LDAPConfig
    template_name = 'config/ldap_config_list.html'
    context_object_name = 'ldap_configs'
    ordering = ['-is_active', 'server']


@method_decorator(staff_required, name='dispatch')
class LDAPConfigCreateView(View):
    """View para criar nova configuração LDAP"""
    template_name = 'config/ldap_config_form.html'

    def get(self, request):
        form = LDAPConfigForm()
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})

    def post(self, request):
        form = LDAPConfigForm(request.POST)
        if form.is_valid():
            ldap_config = form.save()
            messages.success(request, f'Configuração LDAP "{ldap_config.server}" criada com sucesso!')
            return redirect('config:ldap-list')
        return render(request, self.template_name, {'form': form, 'action': 'Criar'})


@method_decorator(staff_required, name='dispatch')
class LDAPConfigUpdateView(UpdateView):
    """View para editar configuração LDAP"""
    model = LDAPConfig
    form_class = LDAPConfigForm
    template_name = 'config/ldap_config_form.html'
    success_url = reverse_lazy('config:ldap-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Configuração LDAP "{form.instance.server}" atualizada com sucesso!')
        return super().form_valid(form)


@method_decorator(staff_required, name='dispatch')
class LDAPConfigDeleteView(View):
    """View para deletar configuração LDAP"""

    def post(self, request, pk):
        try:
            ldap_config = LDAPConfig.objects.get(pk=pk)
            server = ldap_config.server
            ldap_config.delete()
            messages.success(request, f'Configuração LDAP "{server}" removida com sucesso!')
        except LDAPConfig.DoesNotExist:
            messages.error(request, 'Configuração LDAP não encontrada.')

        return redirect('config:ldap-list')


@method_decorator(staff_required, name='dispatch')
class LDAPConfigTestView(View):
    """View para testar conexão LDAP"""

    def post(self, request, pk):
        try:
            ldap_config = LDAPConfig.objects.get(pk=pk)

            # Importar bibliotecas LDAP
            try:
                from ldap3 import Server, Connection, ALL, NTLM, SIMPLE
                from ldap3.core.exceptions import LDAPException
            except ImportError:
                messages.error(request, 'Biblioteca ldap3 não instalada. Execute: pip install ldap3')
                return redirect('config:ldap-list')

            try:
                # Testar conexão
                server = Server(ldap_config.server_uri or f'ldap://{ldap_config.server}:{ldap_config.port}', get_info=ALL)

                if ldap_config.bind_dn and ldap_config.get_password():
                    conn = Connection(server, ldap_config.bind_dn, ldap_config.get_password(), auto_bind=True)
                else:
                    conn = Connection(server, auto_bind=True)

                # Testar busca simples
                conn.search(ldap_config.base_dn, ldap_config.search_filter, size_limit=1)

                messages.success(request, f'Conexão LDAP testada com sucesso! Servidor: {server.info.host}')
                conn.unbind()

            except LDAPException as e:
                messages.error(request, f'Erro na conexão LDAP: {str(e)}')
            except Exception as e:
                messages.error(request, f'Erro inesperado: {str(e)}')

        except LDAPConfig.DoesNotExist:
            messages.error(request, 'Configuração LDAP não encontrada.')

        return redirect('config:ldap-list')