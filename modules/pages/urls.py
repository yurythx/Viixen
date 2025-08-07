from django.urls import path
from .views.home import HomeView
from .views.detail import PageDetailView

app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', HomeView.as_view(template_name='pages/about.html'), name='about'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]