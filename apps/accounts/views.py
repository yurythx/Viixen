from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, View
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.debug import sensitive_variables
from django.contrib.auth.password_validation import validate_password
from apps.config.models import LDAPConfig, EmailConfig
from ldap3 import Server, Connection, ALL, Tls
from django.contrib.auth.backends import ModelBackend
from apps.accounts.forms import (
    EditProfileForm, UserProfileForm, EmailSettingsForm,
    SocialAuthSettingsForm, LDAPSettingsForm, CustomUserCreationForm
)
from apps.accounts.models import SocialAuthSettings, Cargo, Departamento
import logging
import ssl

# Configuração de logging
logger = logging.getLogger(__name__)
User = get_user_model()

# Mixins e classes auxiliares
class MessageMixin:
    def add_message(self, level, message):
        messages.add_message(self.request, level, message)

# --- PÁGINA DE TESTES ---
class TestPageView(TemplateView):
    template_name = 'accounts/test_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# --- Limitação de tentativas ---
def limit_attempts(request, key_prefix, limit=5, timeout=300):
    ip = request.META.get('REMOTE_ADDR')
    cache_key = f'{key_prefix}:{ip}'
    attempts = cache.get(cache_key, 0) + 1
    cache.set(cache_key, attempts, timeout=timeout)
    return attempts

# --- Login LDAP ---
def ldap_login(request):
    """View para autenticação via LDAP"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validar campos
        if not username or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'accounts/ldap_login.html')

        # Verificar tentativas de login
        if limit_attempts(request, 'ldap_login_attempts') > 5:
            messages.error(request, 'Muitas tentativas. Tente novamente em 5 minutos.')
            return redirect('accounts:ldap_login')

        # Obter configurações LDAP
        ldap_config = LDAPConfig.objects.filter(is_active=True).first()
        if not ldap_config:
            messages.error(request, 'Configuração LDAP não encontrada ou inativa.')
            logger.error('Tentativa de login LDAP sem configuração ativa')
            return render(request, 'accounts/ldap_login.html')

        try:
            # Configurar TLS para conexão segura
            tls_config = Tls(validate=ssl.CERT_NONE)  # Em produção, use CERT_REQUIRED

            # Conectar ao servidor LDAP
            server_uri = ldap_config.server_uri
            if not server_uri.startswith(('ldap://', 'ldaps://')):
                server_uri = f'ldap://{server_uri}'

            server = Server(server_uri, get_info=ALL, tls=tls_config)

            # Tentar conexão com o servidor
            try:
                conn = Connection(
                    server,
                    user=f"{ldap_config.bind_dn}\\{username}",
                    password=password,
                    auto_bind=True
                )
            except Exception as conn_error:
                logger.error(f'Erro de conexão LDAP: {str(conn_error)}')

                # Verificar o tipo de erro para fornecer mensagens mais específicas
                error_str = str(conn_error).lower()

                if 'invalidcredentials' in error_str or 'invalid credentials' in error_str:
                    messages.error(request, 'Senha incorreta. Por favor, verifique suas credenciais corporativas.')
                elif 'user not found' in error_str or 'no such user' in error_str:
                    messages.error(request, 'Usuário não encontrado no diretório corporativo.')
                elif 'timeout' in error_str:
                    messages.error(request, 'Tempo de conexão esgotado. O servidor LDAP pode estar indisponível.')
                elif 'connection' in error_str:
                    messages.error(request, 'Não foi possível conectar ao servidor LDAP. Verifique sua conexão de rede.')
                else:
                    messages.error(request, 'Não foi possível conectar ao servidor LDAP. Verifique com o administrador.')

                # Adicionar classe de erro ao formulário
                return render(request, 'accounts/ldap_login.html', {'error_field': 'password'})

            # Se chegou aqui, a autenticação foi bem-sucedida
            # Verificar se o usuário existe no Django ou criar um novo
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Criar novo usuário
                email = f"{username}@{ldap_config.domain}" if ldap_config.domain else f"{username}@example.com"
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=None  # Não definimos senha local para usuários LDAP
                )
                user.set_unusable_password()
                user.is_active = True  # Ativar o usuário imediatamente
                user.save()

                # Registrar a criação do usuário
                logger.info(f'Novo usuário LDAP criado: {username}')

            # Fazer login do usuário
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Bem-vindo, {username}! Login LDAP realizado com sucesso.')
            return redirect('accounts:profile')

        except Exception as e:
            messages.error(request, 'Falha na autenticação LDAP. Verifique suas credenciais.')
            logger.error(f'Erro LDAP: {str(e)}')

    return render(request, 'accounts/ldap_login.html')

# --- Registro ---
class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if limit_attempts(request, 'register_attempts') > 5:
            messages.error(request, 'Muitas tentativas. Tente novamente mais tarde.')
            return redirect('accounts:register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            form.add_error('email', 'Este email já está cadastrado')
            return self.form_invalid(form)

        try:
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = self.request.build_absolute_uri(
                reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
            )

            subject = "Ative sua conta"
            message = render_to_string('accounts/email_activation.html', {
                'user': user,
                'activation_link': activation_link,
            })

            # Manter EmailMessage para compatibilidade com o código existente
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.content_subtype = "html"
            email.send()

            messages.info(self.request, "Verifique seu e-mail para ativar sua conta.")
            return redirect('accounts:login')

        except Exception as e:
            logger.error(f"Erro ao enviar e-mail de ativação: {e}")
            messages.error(self.request, "Erro ao enviar e-mail. Tente novamente.")
            return self.form_invalid(form)

# --- Ativação por e-mail ---
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            # Ativar a conta
            user.is_active = True
            user.email_verificado = True  # Atualizar o campo email_verificado
            user.save()

            # Fazer login automático após a ativação
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            messages.success(request, "Conta ativada com sucesso! Você foi logado automaticamente.")
            return redirect('accounts:profile')  # Redirecionar para o perfil em vez da página de login
        return render(request, 'accounts/activation_invalid.html')


# --- Perfil ---
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        # Adicionar cabeçalhos para prevenir cache
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserProfileForm(instance=self.request.user)
        return context

# --- Editar Perfil ---
class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')

    def dispatch(self, request, *args, **kwargs):
        # Adicionar cabeçalhos para prevenir cache
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Perfil atualizado com sucesso!")
        return super().form_valid(form)


# --- Configurações administrativas ---
class AdminSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'accounts/admin_settings.html'

    def test_func(self):
        # Verificar se o usuário é um administrador
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para acessar esta página.")
        return redirect('accounts:profile')

    def get(self, request):
        # Obter configurações sociais
        google_settings = SocialAuthSettings.objects.filter(provider='google').first()
        github_settings = SocialAuthSettings.objects.filter(provider='github').first()

        # Obter configurações de email
        from apps.config.models import EmailConfig
        email_config = EmailConfig.objects.filter(is_active=True).first()

        # Obter configurações LDAP
        ldap_config = LDAPConfig.objects.filter(is_active=True).first()

        # Preparar dados iniciais para formulários
        social_initial = {}
        if google_settings:
            social_initial.update({
                'google_client_id': google_settings.client_id,
                'google_secret': google_settings.secret
            })
        if github_settings:
            social_initial.update({
                'github_client_id': github_settings.client_id,
                'github_secret': github_settings.secret
            })

        email_initial = {}
        if email_config:
            email_initial = {
                'host': email_config.email_host,
                'port': email_config.email_port,
                'user': email_config.email_host_user,
                'password': email_config.email_host_password,
                'use_tls': email_config.email_use_tls
            }

        ldap_initial = {}
        if ldap_config:
            ldap_initial = {
                'server_uri': ldap_config.server_uri,
                'bind_dn': ldap_config.bind_dn,
                'bind_password': ldap_config.bind_password,
                'domain': ldap_config.domain,
                'user_search_base': ldap_config.base_dn,
                'group_search_base': ''  # Não temos este campo no modelo ainda
            }

        context = {
            'email_form': EmailSettingsForm(initial=email_initial),
            'social_form': SocialAuthSettingsForm(initial=social_initial),
            'ldap_form': LDAPSettingsForm(initial=ldap_initial),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form_type = request.POST.get('form_type')

        if form_type == 'email_settings':
            form = EmailSettingsForm(request.POST)
            if form.is_valid():
                try:
                    # Salvar no modelo em vez de modificar settings diretamente
                    email_config, created = EmailConfig.objects.get_or_create(
                        slug='email-config',
                        defaults={
                            'email_host': form.cleaned_data['host'],
                            'email_port': form.cleaned_data['port'],
                            'email_host_user': form.cleaned_data['user'],
                            'email_host_password': form.cleaned_data['password'],
                            'email_use_tls': form.cleaned_data['use_tls'],
                            'default_from_email': form.cleaned_data['user'],
                            'is_active': True
                        }
                    )

                    if not created:
                        email_config.email_host = form.cleaned_data['host']
                        email_config.email_port = form.cleaned_data['port']
                        email_config.email_host_user = form.cleaned_data['user']
                        email_config.email_host_password = form.cleaned_data['password']
                        email_config.email_use_tls = form.cleaned_data['use_tls']
                        email_config.save()

                    # Atualizar as configurações em tempo de execução
                    settings.EMAIL_HOST = form.cleaned_data['host']
                    settings.EMAIL_PORT = form.cleaned_data['port']
                    settings.EMAIL_HOST_USER = form.cleaned_data['user']
                    settings.EMAIL_HOST_PASSWORD = form.cleaned_data['password']
                    settings.EMAIL_USE_TLS = form.cleaned_data['use_tls']

                    # Testar a conexão com o servidor de email
                    try:
                        from django.core.mail import get_connection
                        connection = get_connection()
                        connection.open()
                        connection.close()
                        messages.success(request, 'Configurações de email atualizadas e testadas com sucesso!')
                    except Exception as e:
                        logger.warning(f"Configurações de email salvas, mas o teste de conexão falhou: {e}")
                        messages.warning(request, 'Configurações de email salvas, mas não foi possível testar a conexão. Verifique os dados.')
                except Exception as e:
                    logger.error(f"Erro ao salvar configurações de email: {e}")
                    messages.error(request, f'Erro ao salvar configurações de email: {str(e)}')
                    return self.get(request)
            else:
                messages.error(request, 'Verifique os erros no formulário de email.')
                return self.get(request)

        elif form_type == 'social_settings':
            form = SocialAuthSettingsForm(request.POST)
            if form.is_valid():
                try:
                    google_settings, _ = SocialAuthSettings.objects.get_or_create(provider='google')
                    google_settings.client_id = form.cleaned_data['google_client_id']
                    google_settings.secret = form.cleaned_data['google_secret']
                    google_settings.save()

                    github_settings, _ = SocialAuthSettings.objects.get_or_create(provider='github')
                    github_settings.client_id = form.cleaned_data['github_client_id']
                    github_settings.secret = form.cleaned_data['github_secret']
                    github_settings.save()

                    messages.success(request, 'Autenticação social atualizada com sucesso!')
                except Exception as e:
                    logger.error(f"Erro ao salvar configurações de autenticação social: {e}")
                    messages.error(request, f'Erro ao salvar configurações de autenticação social: {str(e)}')
                    return self.get(request)
            else:
                messages.error(request, 'Verifique os erros no formulário de autenticação social.')
                return self.get(request)

        elif form_type == 'ldap_settings':
            form = LDAPSettingsForm(request.POST)
            if form.is_valid():
                try:
                    # Extrair servidor e porta da URI
                    server_uri = form.cleaned_data['server_uri']
                    if server_uri.startswith('ldap://'):
                        server_uri = server_uri[7:]  # Remover 'ldap://'
                    elif server_uri.startswith('ldaps://'):
                        server_uri = server_uri[8:]  # Remover 'ldaps://'

                    server_parts = server_uri.split(':')
                    server = server_parts[0]
                    port = 389  # Porta padrão LDAP

                    if len(server_parts) > 1:
                        try:
                            port = int(server_parts[1])
                        except ValueError:
                            form.add_error('server_uri', 'Formato de URI inválido. Use ldap://servidor:porta')
                            messages.error(request, 'Verifique os erros no formulário.')
                            return self.get(request)

                    # Configurar TLS para conexão segura
                    tls_config = Tls(validate=ssl.CERT_NONE)  # Em produção, use CERT_REQUIRED

                    # Tentar conectar ao servidor LDAP para validar as configurações
                    try:
                        test_server = Server(f"ldap://{server}:{port}", get_info=ALL, tls=tls_config)
                        test_conn = Connection(
                            test_server,
                            user=form.cleaned_data['bind_dn'],
                            password=form.cleaned_data['bind_password'],
                            auto_bind=True
                        )
                        test_conn.unbind()
                    except Exception as e:
                        logger.error(f"Erro ao testar conexão LDAP: {e}")
                        form.add_error('server_uri', f'Não foi possível conectar ao servidor LDAP: {str(e)}')
                        messages.error(request, 'Não foi possível conectar ao servidor LDAP. Verifique as configurações.')
                        return self.get(request)

                    # Salvar configurações LDAP
                    ldap_config, created = LDAPConfig.objects.get_or_create(
                        slug='ldap-config',
                        defaults={
                            'server_uri': form.cleaned_data['server_uri'],
                            'server': server,
                            'port': port,
                            'base_dn': form.cleaned_data['user_search_base'],
                            'bind_dn': form.cleaned_data['bind_dn'],
                            'bind_password': form.cleaned_data['bind_password'],
                            'domain': form.cleaned_data['domain'],
                            'is_active': True
                        }
                    )

                    if not created:
                        ldap_config.server_uri = form.cleaned_data['server_uri']
                        ldap_config.server = server
                        ldap_config.port = port
                        ldap_config.base_dn = form.cleaned_data['user_search_base']
                        ldap_config.bind_dn = form.cleaned_data['bind_dn']
                        ldap_config.bind_password = form.cleaned_data['bind_password']
                        ldap_config.domain = form.cleaned_data['domain']
                        ldap_config.is_active = True
                        ldap_config.save()

                    messages.success(request, 'Configurações LDAP atualizadas com sucesso!')
                except Exception as e:
                    logger.error(f"Erro ao salvar configurações LDAP: {e}")
                    messages.error(request, f'Erro ao salvar configurações LDAP: {str(e)}')
                    return self.get(request)
            else:
                messages.error(request, 'Verifique os erros no formulário LDAP.')
                return self.get(request)
        else:
            messages.error(request, 'Formulário inválido.')
            return self.get(request)

        return redirect('accounts:admin_settings')


# --- Login personalizado ---
class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        # Adicionar cabeçalhos para prevenir cache
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def form_invalid(self, form):
        if limit_attempts(self.request, 'login_attempts') > 5:
            messages.error(self.request, 'Muitas tentativas. Tente novamente em 5 minutos.')
            return redirect('accounts:login')

        # Verificar se há erros específicos para fornecer mensagens mais claras
        if form.errors:
            # Verificar se há erro de credenciais inválidas
            if '__all__' in form.errors:
                for error in form.errors['__all__']:
                    if 'Please enter a correct username and password' in error:
                        messages.error(self.request, 'Senha incorreta. Por favor, verifique suas credenciais.')
                    else:
                        messages.error(self.request, error)

            # Verificar erros específicos de campo
            if 'username' in form.errors:
                messages.error(self.request, 'Nome de usuário inválido ou não encontrado.')

            if 'password' in form.errors:
                messages.error(self.request, 'Senha inválida. Por favor, tente novamente.')

        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Conta inativa. Verifique seu e-mail para ativar.")
            return redirect('accounts:login')

        # Registrar o login bem-sucedido
        logger.info(f"Login bem-sucedido para o usuário: {user.username}")
        messages.success(self.request, f"Bem-vindo de volta, {user.get_nome_completo() or user.username}! Login realizado com sucesso.")
        return super().form_valid(form)


# --- LOGOUT PERSONALIZADO ---
class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

    def dispatch(self, request, *args, **kwargs):
        """Adiciona mensagem de sucesso antes de fazer logout"""
        if request.user.is_authenticated:
            messages.success(request, 'Você saiu do sistema com sucesso. Até logo!')
        response = super().dispatch(request, *args, **kwargs)

        # Adicionar cabeçalhos para prevenir cache
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response

    def get(self, request, *args, **kwargs):
        """Permitir logout via GET se configurado"""
        if hasattr(settings, 'ACCOUNT_LOGOUT_ON_GET') and settings.ACCOUNT_LOGOUT_ON_GET:
            return self.post(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
