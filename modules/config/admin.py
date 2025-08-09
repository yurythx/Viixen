from django.contrib import admin
from .models import Company, Module, CompanyModule

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'domain', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'domain')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'app_label', 'is_core', 'is_active', 'order', 'created_at')
    list_filter = ('is_core', 'is_active', 'created_at')
    search_fields = ('name', 'app_label', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at',)

    def get_readonly_fields(self, request, obj=None):
        # Não permitir alterar is_core para módulos já criados
        if obj and obj.is_core:
            return self.readonly_fields + ('is_core',)
        return self.readonly_fields

@admin.register(CompanyModule)
class CompanyModuleAdmin(admin.ModelAdmin):
    list_display = ['company', 'module', 'is_active', 'is_licensed', 'license_status_display', 'activated_at', 'license_expires_at']
    list_filter = ['is_active', 'is_licensed', 'module__is_core', 'activated_at', 'licensed_at', 'license_expires_at']
    search_fields = ['company__name', 'module__name']
    list_editable = ['is_active', 'is_licensed', 'license_expires_at']
    readonly_fields = ['activated_at', 'licensed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('company', 'module')
    
    def license_status_display(self, obj):
        """Exibe o status da licença com cores"""
        status = obj.license_status
        colors = {
            'active': 'green',
            'expiring_soon': 'orange', 
            'expired': 'red',
            'unlicensed': 'gray'
        }
        labels = {
            'active': 'Ativa',
            'expiring_soon': f'Expira em {obj.days_until_expiration} dias',
            'expired': 'Expirada',
            'unlicensed': 'Não Licenciada'
        }
        
        from django.utils.html import format_html
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(status, 'black'),
            labels.get(status, status)
        )
    
    license_status_display.short_description = 'Status da Licença'
