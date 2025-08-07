from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from ..domain.company import Company
from ..domain.module import Module, CompanyModule
from ...accounts.domain.user import CustomUser
from ...blog.domain.post import BlogPost
from ...pages.domain.page import Page

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'config/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_company_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.company
        
        # Estatísticas gerais
        context.update({
            'total_users': CustomUser.objects.filter(company=company).count(),
            'active_users': CustomUser.objects.filter(company=company, is_active=True).count(),
            'total_posts': BlogPost.objects.filter(company=company).count(),
            'published_posts': BlogPost.objects.filter(company=company, status='published').count(),
            'total_pages': Page.objects.filter(company=company).count(),
            'published_pages': Page.objects.filter(company=company, is_published=True).count(),
            'active_modules': CompanyModule.objects.filter(company=company, is_active=True).count(),
            'total_modules': Module.objects.filter(is_active=True).count(),
        })
        
        # Posts recentes
        context['recent_posts'] = BlogPost.objects.filter(
            company=company
        ).order_by('-created_at')[:5]
        
        # Usuários recentes
        context['recent_users'] = CustomUser.objects.filter(
            company=company
        ).order_by('-date_joined')[:5]
        
        # Módulos da empresa
        context['company_modules'] = CompanyModule.objects.filter(
            company=company
        ).select_related('module')
        
        return context