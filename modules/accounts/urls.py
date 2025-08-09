from django.urls import path
from django.contrib.auth import views as auth_views
from .views.user_management import (
    UserListView, UserDetailView, UserCreateView, 
    UserUpdateView, UserDeleteView, UserProfileView
)

app_name = 'accounts'

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Gerenciamento de usuários
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    
    # Perfil
    path('profile/', UserProfileView.as_view(), name='profile'),
]