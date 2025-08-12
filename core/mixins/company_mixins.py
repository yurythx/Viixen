from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import get_object_or_404


class CompanyObjectMixin:
    """
    Mixin para obter a empresa do usuário atual.
    """
    def get_company(self):
        """
        Obtém a empresa do usuário atual.
        Se o usuário for superusuário, retorna a primeira empresa.
        """
        # Usando get_model para evitar problemas de importação circular
        Company = models.get_model('config', 'Company')
        user = self.request.user
        if user.is_superuser:
            return Company.objects.first()
        return user.company


class CompanyFilterMixin:
    """
    Mixin para filtrar querysets pela empresa do usuário.
    """
    def get_queryset(self):
        """
        Filtra o queryset pela empresa do usuário.
        Superusuários podem ver todos os registros.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_superuser:
            return queryset
            
        if hasattr(user, 'company'):
            # Usando get_model para evitar problemas de importação circular
            Company = models.get_model('config', 'Company')
            company_field = models.fields.related.ForeignKey(Company, on_delete=models.CASCADE)
            return queryset.filter(company=user.company)
            
        return queryset.none()


class CompanyAdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar se o usuário é administrador da empresa.
    """
    def test_func(self):
        """
        Verifica se o usuário é administrador da empresa ou superusuário.
        """
        user = self.request.user
        if user.is_superuser:
            return True
            
        if not hasattr(user, 'company'):
            return False
            
        return user.is_company_admin


class GlobalAdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar se o usuário é um administrador global ou superusuário.
    """
    def test_func(self):
        """
        Verifica se o usuário é um administrador global ou superusuário.
        """
        user = self.request.user
        return user.is_superuser or getattr(user, 'is_global_admin', False)


class GlobalAdminFilterMixin:
    """
    Mixin para filtrar por empresa apenas para não administradores globais.
    """
    def get_queryset(self):
        """
        Filtra o queryset por empresa se o usuário não for superusuário.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_superuser or getattr(user, 'is_global_admin', False):
            return queryset
            
        if hasattr(user, 'company'):
            # Usando get_model para evitar problemas de importação circular
            Company = models.get_model('config', 'Company')
            company_field = models.fields.related.ForeignKey(Company, on_delete=models.CASCADE)
            return queryset.filter(company=user.company)
            
        return queryset.none()
