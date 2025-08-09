from django.urls import path
from .views.dashboard import DashboardView
from .views.company import CompanyDetailView as UserCompanyDetailView, CompanyUpdateView
from .views.company_management import (
    CompanyListView, CompanyDetailView as GlobalCompanyDetailView, CompanyCreateView, 
    CompanyUpdateView as CompanyGlobalUpdateView, 
    CompanyDeleteView
)
from .views.module_management import (
    ModuleGlobalListView, ModuleGlobalToggleView,
    CompanyModuleListView, CompanyModuleToggleView, CompanyModuleToggleAjaxView
)
from .views.module_licensing import (
    ModuleLicensingView, 
    ModuleLicenseDetailView, 
    CompanyLicenseToggleView, 
    CompanyLicenseAjaxToggleView
)
from .views.license_expiration import (
    LicenseExpirationView,
    LicenseRenewalView,
    BulkLicenseRenewalView,
    LicenseExpirationAjaxView
)

app_name = 'config'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # URLs para empresa do usuário atual
    path('company/', UserCompanyDetailView.as_view(), name='company_detail'),
    path('company/edit/', CompanyUpdateView.as_view(), name='company_update'),
    
    # URLs para gerenciamento global de empresas (apenas superadmins)
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/create/', CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>/', GlobalCompanyDetailView.as_view(), name='company_global_detail'),
    path('companies/<int:pk>/edit/', CompanyGlobalUpdateView.as_view(), name='company_global_edit'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
    
    # URLs para gerenciamento de módulos
    # Gerenciamento global (apenas superadmins/admins)
    path('modules/', ModuleGlobalListView.as_view(), name='module_global_list'),
    path('modules/<int:module_id>/toggle/', ModuleGlobalToggleView.as_view(), name='module_global_toggle'),
    
    # Gerenciamento por empresa
    path('company/modules/', CompanyModuleListView.as_view(), name='company_module_list'),
    path('company/modules/<int:module_id>/toggle/', CompanyModuleToggleView.as_view(), name='company_module_toggle'),
    path('company/modules/<int:module_id>/ajax-toggle/', CompanyModuleToggleAjaxView.as_view(), name='company_module_ajax_toggle'),
    
    # Module Licensing URLs
    path('modules/licensing/', ModuleLicensingView.as_view(), name='module_licensing'),
    path('modules/<int:module_id>/license-detail/', ModuleLicenseDetailView.as_view(), name='module_license_detail'),
    path('modules/<int:module_id>/companies/<int:company_id>/license-toggle/', CompanyLicenseToggleView.as_view(), name='company_license_toggle'),
    path('modules/<int:module_id>/companies/<int:company_id>/ajax-license-toggle/', CompanyLicenseAjaxToggleView.as_view(), name='company_license_ajax_toggle'),
    
    # License Expiration URLs
    path('modules/expiration/', LicenseExpirationView.as_view(), name='license_expiration'),
    path('modules/<int:module_id>/companies/<int:company_id>/renew/', LicenseRenewalView.as_view(), name='license_renewal'),
    path('modules/bulk-renewal/', BulkLicenseRenewalView.as_view(), name='bulk_license_renewal'),
    path('modules/expiration-ajax/', LicenseExpirationAjaxView.as_view(), name='license_expiration_ajax'),
]