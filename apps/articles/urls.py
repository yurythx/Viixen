# apps/pages/urls.py
from django.urls import path
from . import views

app_name = 'apps.articles'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]