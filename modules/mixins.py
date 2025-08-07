from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class CompanyAdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requer que o usuário seja admin da empresa"""
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company_admin
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Você precisa ser administrador da empresa para acessar esta página.")
        return super().handle_no_permission()

class CompanyFilterMixin:
    """Mixin que filtra objetos pela empresa do usuário"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'company') and self.request.company:
            return queryset.filter(company=self.request.company)
        return queryset.none()

class CompanyOwnerMixin:
    """Mixin que verifica se o usuário é dono do objeto ou admin da empresa"""
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
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