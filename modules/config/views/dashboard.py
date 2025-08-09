from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from ..domain.company import Company
from ..domain.module import Module, CompanyModule
from ...accounts.domain.user import CustomUser
from ...blog.domain.post import BlogPost
from ...pages.domain.page import Page
from ...mixins import CompanyAdminRequiredMixin, CompanyFilterMixin, CompanyOwnerMixin, GlobalAdminFilterMixin

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, GlobalAdminFilterMixin, TemplateView):
    template_name = 'config/dashboard.html'
    
    def test_func(self):
        # Permite acesso para admins globais ou admins da empresa
        return (getattr(self.request, 'is_global_admin', False) or 
                self.request.user.is_company_admin)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.company
        
        # Estatísticas baseadas em permissões
        if getattr(self.request, 'is_global_admin', False):
            # Admin global vê estatísticas de todas as empresas
            context.update({
                'total_users': CustomUser.objects.count(),
                'active_users': CustomUser.objects.filter(is_active=True).count(),
                'total_posts': BlogPost.objects.count(),
                'published_posts': BlogPost.objects.filter(status='published').count(),
                'total_pages': Page.objects.count(),
                'published_pages': Page.objects.filter(is_published=True).count(),
                'total_companies': Company.objects.count(),
                'active_modules': CompanyModule.objects.filter(is_active=True).count(),
                'total_modules': Module.objects.filter(is_active=True).count(),
                'is_global_admin': True,
            })
        else:
            # Admin da empresa vê apenas dados da sua empresa
            context.update({
                'total_users': CustomUser.objects.filter(company=company).count(),
                'active_users': CustomUser.objects.filter(company=company, is_active=True).count(),
                'total_posts': BlogPost.objects.filter(company=company).count(),
                'published_posts': BlogPost.objects.filter(company=company, status='published').count(),
                'total_pages': Page.objects.filter(company=company).count(),
                'published_pages': Page.objects.filter(company=company, is_published=True).count(),
                'active_modules': CompanyModule.objects.filter(company=company, is_active=True).count(),
                'total_modules': Module.objects.filter(is_active=True).count(),
                'is_global_admin': False,
            })
        
        # Dados recentes baseados em permissões
        if getattr(self.request, 'is_global_admin', False):
            # Admin global vê dados de todas as empresas
            context['recent_posts'] = BlogPost.objects.order_by('-created_at')[:5]
            context['recent_users'] = CustomUser.objects.order_by('-date_joined')[:5]
            context['all_companies'] = Company.objects.order_by('name')[:10]
        else:
            # Admin da empresa vê apenas dados da sua empresa
            context['recent_posts'] = BlogPost.objects.filter(
                company=company
            ).order_by('-created_at')[:5]
            context['recent_users'] = CustomUser.objects.filter(
                company=company
            ).order_by('-date_joined')[:5]
        
        # Módulos da empresa (sempre filtrado por empresa atual)
        if company:
            context['company_modules'] = CompanyModule.objects.filter(
                company=company
            ).select_related('module')
        else:
            context['company_modules'] = CompanyModule.objects.none()
        
        return context