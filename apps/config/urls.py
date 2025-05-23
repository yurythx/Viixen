from django.urls import path
from .views import (
    ConfigView,
    SocialProviderConfigUpdateView,
    EmailConfigUpdateView,
    SystemConfigUpdateView,
    AppConfigListView,
    AppConfigUpdateView,
    ModuleDisabledTestView
)

app_name = 'config'

urlpatterns = [
    path('', ConfigView.as_view(), name='config'),
    path('social-provider/<slug:slug>/', SocialProviderConfigUpdateView.as_view(), name='social-provider-update'),
    path('email/<slug:slug>/', EmailConfigUpdateView.as_view(), name='email-update'),
    path('system/<slug:slug>/', SystemConfigUpdateView.as_view(), name='system-update'),
    path('apps/', AppConfigListView.as_view(), name='app-list'),
    path('apps/<int:pk>/', AppConfigUpdateView.as_view(), name='app-update'),
    path('test-module-disabled/', ModuleDisabledTestView.as_view(), name='test-module-disabled'),
]