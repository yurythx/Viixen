from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

class GlobalAdminMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário é admin global (superuser ou grupo Administrador)"""
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return (
            self.request.user.is_superuser or 
            self.request.user.groups.filter(name='Administrador').exists()
        )
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Você precisa ser administrador global para acessar esta página.")
        return super().handle_no_permission()

class CompanyAdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requer que o usuário seja admin da empresa OU admin global"""
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        # Admin global tem acesso total
        if getattr(self.request, 'is_global_admin', False):
            return True
            
        # Admin da empresa também tem acesso
        return self.request.user.is_company_admin
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Você precisa ser administrador da empresa para acessar esta página.")
        return super().handle_no_permission()

class CompanyFilterMixin:
    """Mixin que filtra objetos pela empresa do usuário (admins globais veem tudo)"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Admin global vê todos os objetos
        if getattr(self.request, 'is_global_admin', False):
            return queryset
        
        # Usuários normais veem apenas da sua empresa
        if hasattr(self.request, 'company') and self.request.company:
            return queryset.filter(company=self.request.company)
        return queryset.none()

class CompanyOwnerMixin(UserPassesTestMixin):
    """Mixin que verifica se o usuário é dono do objeto, admin da empresa OU admin global"""
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        # Admin global tem acesso total
        if getattr(self.request, 'is_global_admin', False):
            return True
        
        obj = self.get_object()
        
        # Se é admin da empresa, pode acessar
        if self.request.user.is_company_admin:
            return True
        
        # Se é o próprio usuário (para perfis)
        if hasattr(obj, 'user') and obj.user == self.request.user:
            return True
        
        # Se é o próprio objeto (para usuários)
        if obj == self.request.user:
            return True
        
        return False

class GlobalAdminFilterMixin:
    """Mixin que permite admins globais verem todos os dados, independente da empresa"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Admin global vê todos os objetos de todas as empresas
        if getattr(self.request, 'is_global_admin', False):
            return queryset
        
        # Aplicar filtro normal para usuários comuns
        return queryset

class SuperAdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requer que o usuário seja superusuário"""
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Apenas superusuários podem acessar esta página.")
        return super().handle_no_permission()