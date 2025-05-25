from django.contrib import admin
from .models import SocialProviderConfig, EmailConfig, SystemConfig, AppConfig, EnvironmentVariable, DatabaseConfig, LDAPConfig

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


@admin.register(EnvironmentVariable)
class EnvironmentVariableAdmin(admin.ModelAdmin):
    list_display = ('key', 'category', 'var_type', 'is_required', 'is_sensitive', 'is_active', 'created_at')
    list_filter = ('category', 'var_type', 'is_required', 'is_sensitive', 'is_active')
    search_fields = ('key', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('category', 'order', 'key')

    fieldsets = (
        ('Informações da Variável', {
            'fields': ('key', 'description', 'category', 'var_type', 'order')
        }),
        ('Valores', {
            'fields': ('value', 'default_value')
        }),
        ('Configurações', {
            'fields': ('is_required', 'is_sensitive', 'is_active')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Mascarar campo de valor se for sensível
        if obj and obj.is_sensitive:
            form.base_fields['value'].widget.attrs['type'] = 'password'

        return form


@admin.register(DatabaseConfig)
class DatabaseConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'engine', 'host', 'database_name', 'is_active', 'is_default', 'created_at')
    list_filter = ('engine', 'is_active', 'is_default')
    search_fields = ('name', 'database_name', 'host')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['-is_default', 'name']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'engine', 'is_active', 'is_default')
        }),
        ('Configurações de Conexão', {
            'fields': ('database_name', 'host', 'port', 'user', 'password')
        }),
        ('Configurações Avançadas', {
            'fields': ('conn_max_age', 'conn_health_checks', 'atomic_requests', 'autocommit'),
            'classes': ('collapse',)
        }),
        ('Configurações SSL', {
            'fields': ('ssl_require', 'ssl_ca', 'ssl_cert', 'ssl_key'),
            'classes': ('collapse',)
        }),
        ('Configurações Específicas', {
            'fields': ('charset', 'test_database_name'),
            'classes': ('collapse',)
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Mascarar campo de senha
        form.base_fields['password'].widget.attrs['type'] = 'password'

        return form


@admin.register(LDAPConfig)
class LDAPConfigAdmin(admin.ModelAdmin):
    list_display = ('server', 'port', 'base_dn', 'is_active', 'created_at')
    list_filter = ('is_active', 'port')
    search_fields = ('server', 'base_dn', 'bind_dn')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['-is_active', 'server']

    fieldsets = (
        ('Configurações do Servidor', {
            'fields': ('server', 'port', 'server_uri')
        }),
        ('Configurações de Autenticação', {
            'fields': ('bind_dn', 'bind_password')
        }),
        ('Configurações de Busca', {
            'fields': ('base_dn', 'search_filter', 'domain')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Mascarar campo de senha
        form.base_fields['bind_password'].widget.attrs['type'] = 'password'

        return form