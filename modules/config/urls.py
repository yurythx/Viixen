from django.urls import path
from .views.dashboard import DashboardView
from .views.company import CompanyDetailView, CompanyUpdateView

app_name = 'config'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('company/', CompanyDetailView.as_view(), name='company_detail'),
    path('company/edit/', CompanyUpdateView.as_view(), name='company_edit'),
]