from django.contrib import admin
from .models import SocialProviderConfig, EmailConfig, SystemConfig, AppConfig

@admin.register(SocialProviderConfig)
class SocialProviderConfigAdmin(admin.ModelAdmin):
    list_display = ('provider', 'is_active', 'created_at', 'updated_at')
    list_filter = ('provider', 'is_active')
    search_fields = ('provider',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informações do Provedor', {
            'fields': ('provider', 'client_id', 'secret_key', 'is_active')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(EmailConfig)
class EmailConfigAdmin(admin.ModelAdmin):
    list_display = ('email_host', 'email_port', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email_host', 'email_host_user')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Configurações do Servidor', {
            'fields': ('email_host', 'email_port', 'email_use_tls')
        }),
        ('Credenciais', {
            'fields': ('email_host_user', 'email_host_password', 'default_from_email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'maintenance_mode', 'allow_registration', 'enable_app_management', 'created_at')
    list_filter = ('maintenance_mode', 'allow_registration', 'require_email_verification', 'enable_app_management')
    search_fields = ('site_name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informações do Site', {
            'fields': ('site_name', 'site_description')
        }),
        ('Configurações de Sistema', {
            'fields': ('maintenance_mode', 'allow_registration', 'require_email_verification', 'enable_app_management')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'is_active', 'is_core', 'order', 'created_at')
    list_filter = ('is_active', 'is_core')
    search_fields = ('name', 'label', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informações do App', {
            'fields': ('name', 'label', 'description')
        }),
        ('Configurações', {
            'fields': ('is_active', 'is_core', 'order')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at')
        }),
    )
