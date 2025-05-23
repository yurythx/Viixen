from . import views

from django.urls import path, reverse_lazy
from .views import (
    RegisterView, ProfileView, EditProfileView, AdminSettingsView,
    ActivateAccountView, TestPageView, CustomLoginView, CustomLogoutView
)
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('ldap/', views.ldap_login, name='ldap_login'),

    path('test/', TestPageView.as_view(), name='test_page'),

    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

    # Registro
    path('register/', RegisterView.as_view(), name='register'),

    # Login e logout personalizados com mensagens
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout/confirm/', CustomLogoutView.as_view(template_name='accounts/logout_confirm.html'), name='logout_confirm'),

    # Perfil
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),

    # Troca de senha
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        success_url=reverse_lazy('accounts:password_change_done')),
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'),
        name='password_change_done'),

    # Redefinição de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

    # Configurações de Administrador
    path('admin/settings/', AdminSettingsView.as_view(), name='admin_settings'),


]