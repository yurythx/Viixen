"""
Core mixins for the Viixen project.
Provides common functionality for views including company filtering and permissions.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import Http404


class CompanyFilterMixin:
    """
    Mixin to filter objects by company based on user permissions.
    Global admins can see all companies, regular users only see their company.
    """
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Global admins can see all objects
        if hasattr(self.request, 'is_global_admin') and self.request.is_global_admin:
            return queryset
        
        # Regular users only see objects from their company
        if hasattr(self.request.user, 'company') and self.request.user.company:
            return queryset.filter(company=self.request.user.company)
        
        # If user has no company, return empty queryset
        return queryset.none()


class CompanyAdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin to require company admin permissions.
    Allows global admins and company admins.
    """
    
    def test_func(self):
        user = self.request.user
        
        # Global admins always pass
        if hasattr(self.request, 'is_global_admin') and self.request.is_global_admin:
            return True
        
        # Check if user is admin of their company
        if hasattr(user, 'company') and user.company:
            return user.is_staff or user.groups.filter(name='Admin Empresa').exists()
        
        return False
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar esta área.')
        raise PermissionDenied


class GlobalAdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin to require global admin permissions.
    Only allows superusers and users in 'Administrador' group.
    """
    
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Administrador').exists()
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar esta área. Apenas administradores globais.')
        raise PermissionDenied


class SuperAdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin to require superuser permissions.
    Only allows superusers.
    """
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar esta área. Apenas superusuários.')
        raise PermissionDenied


class GlobalAdminFilterMixin:
    """
    Mixin to provide different querysets based on global admin status.
    Global admins see all objects, regular users see only their company objects.
    """
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Global admins can see all objects
        if hasattr(self.request, 'is_global_admin') and self.request.is_global_admin:
            return queryset
        
        # Regular users only see objects from their company
        if hasattr(self.request.user, 'company') and self.request.user.company:
            return queryset.filter(company=self.request.user.company)
        
        # If user has no company, return empty queryset
        return queryset.none()


class CompanyContextMixin:
    """
    Mixin to add company context to views.
    """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add global admin status to context
        context['is_global_admin'] = getattr(self.request, 'is_global_admin', False)
        
        # Add user company to context
        if hasattr(self.request.user, 'company'):
            context['user_company'] = self.request.user.company
        
        return context


class CompanyObjectMixin:
    """
    Mixin to ensure objects belong to user's company (unless global admin).
    """
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Global admins can access any object
        if hasattr(self.request, 'is_global_admin') and self.request.is_global_admin:
            return obj
        
        # Check if object belongs to user's company
        if hasattr(obj, 'company') and hasattr(self.request.user, 'company'):
            if obj.company != self.request.user.company:
                raise Http404("Objeto não encontrado ou você não tem permissão para acessá-lo.")
        
        return obj
