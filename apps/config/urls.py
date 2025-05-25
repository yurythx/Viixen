from django.urls import path
from .views import (
    ConfigView,
    SocialProviderConfigUpdateView,
    EmailConfigUpdateView,
    SystemConfigUpdateView,
    AppConfigListView,
    AppConfigUpdateView,
    ModuleDisabledTestView,
    EnvironmentVariableListView,
    EnvironmentVariableCreateView,
    EnvironmentVariableUpdateView,
    EnvironmentVariableDeleteView,
    EnvironmentVariableExportView,
    EnvironmentVariableImportView,
    DatabaseConfigListView,
    DatabaseConfigCreateView,
    DatabaseConfigUpdateView,
    DatabaseConfigDeleteView,
    DatabaseConfigTestView,
    LDAPConfigListView,
    LDAPConfigCreateView,
    LDAPConfigUpdateView,
    LDAPConfigDeleteView,
    LDAPConfigTestView,
)

app_name = 'config'

urlpatterns = [
    path('', ConfigView.as_view(), name='config'),
    path('social-provider/<slug:slug>/', SocialProviderConfigUpdateView.as_view(), name='social-provider-update'),
    path('email/', EmailConfigUpdateView.as_view(), name='email-config'),
    path('email/<slug:slug>/', EmailConfigUpdateView.as_view(), name='email-update'),
    path('system/<slug:slug>/', SystemConfigUpdateView.as_view(), name='system-update'),
    path('apps/', AppConfigListView.as_view(), name='app-list'),
    path('apps/<int:pk>/', AppConfigUpdateView.as_view(), name='app-update'),
    path('test-module-disabled/', ModuleDisabledTestView.as_view(), name='test-module-disabled'),

    # Environment Variables URLs
    path('environment-variables/', EnvironmentVariableListView.as_view(), name='env-variables'),
    path('environment-variables/create/', EnvironmentVariableCreateView.as_view(), name='env-variable-create'),
    path('environment-variables/<int:pk>/edit/', EnvironmentVariableUpdateView.as_view(), name='env-variable-edit'),
    path('environment-variables/<int:pk>/delete/', EnvironmentVariableDeleteView.as_view(), name='env-variable-delete'),
    path('environment-variables/export/', EnvironmentVariableExportView.as_view(), name='env-variables-export'),
    path('environment-variables/import/', EnvironmentVariableImportView.as_view(), name='env-variables-import'),

    # Database Configuration URLs
    path('database/', DatabaseConfigListView.as_view(), name='database-list'),
    path('database/create/', DatabaseConfigCreateView.as_view(), name='database-create'),
    path('database/<int:pk>/edit/', DatabaseConfigUpdateView.as_view(), name='database-edit'),
    path('database/<int:pk>/delete/', DatabaseConfigDeleteView.as_view(), name='database-delete'),
    path('database/<int:pk>/test/', DatabaseConfigTestView.as_view(), name='database-test'),

    # LDAP Configuration URLs
    path('ldap/', LDAPConfigListView.as_view(), name='ldap-list'),
    path('ldap/create/', LDAPConfigCreateView.as_view(), name='ldap-create'),
    path('ldap/<int:pk>/edit/', LDAPConfigUpdateView.as_view(), name='ldap-edit'),
    path('ldap/<int:pk>/delete/', LDAPConfigDeleteView.as_view(), name='ldap-delete'),
    path('ldap/<int:pk>/test/', LDAPConfigTestView.as_view(), name='ldap-test'),
]