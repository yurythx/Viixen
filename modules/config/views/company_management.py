from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..domain.company import Company
from ..forms.company_form import CompanyForm
from ...mixins import SuperAdminRequiredMixin, GlobalAdminFilterMixin


class CompanyListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    """Lista todas as empresas - apenas para superadmins"""
    model = Company
    template_name = 'config/company_list.html'
    context_object_name = 'companies'
    paginate_by = 20
    ordering = ['name']


class CompanyDetailView(LoginRequiredMixin, SuperAdminRequiredMixin, DetailView):
    """Detalhes de uma empresa - apenas para superadmins"""
    model = Company
    template_name = 'config/company_detail.html'
    context_object_name = 'company'


class CompanyCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    """Criar nova empresa - apenas para superadmins"""
    model = Company
    form_class = CompanyForm
    template_name = 'config/company_form.html'
    success_url = reverse_lazy('config:company_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empresa criada com sucesso!')
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    """Atualizar empresa - apenas para superadmins"""
    model = Company
    form_class = CompanyForm
    template_name = 'config/company_form.html'
    success_url = reverse_lazy('config:company_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empresa atualizada com sucesso!')
        return super().form_valid(form)


class CompanyDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    """Deletar empresa - apenas para superadmins"""
    model = Company
    template_name = 'config/company_confirm_delete.html'
    success_url = reverse_lazy('config:company_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Empresa removida com sucesso!')
        return super().delete(request, *args, **kwargs)
