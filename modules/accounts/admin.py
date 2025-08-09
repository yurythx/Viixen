from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'company', 'is_company_admin', 'is_staff')
    list_filter = ('company', 'is_company_admin', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'company__name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações da Empresa', {
            'fields': ('company', 'phone', 'is_company_admin')
        }),
    )
