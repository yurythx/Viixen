from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..domain.company import Company
from ..forms.company_form import CompanyForm
from ..services.company_service import CompanyService

class CompanyDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Company
    template_name = 'config/company_detail.html'
    context_object_name = 'company'
    
    def test_func(self):
        return self.request.user.is_company_admin
    
    def get_object(self):
        return self.request.company
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CompanyService()
        context['available_modules'] = service.get_available_modules()
        context['active_modules'] = service.get_company_active_modules(self.request.company)
        return context

class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'config/company_form.html'
    success_url = reverse_lazy('config:company_detail')
    
    def test_func(self):
        return self.request.user.is_company_admin
    
    def get_object(self):
        return self.request.company
    
    def form_valid(self, form):
        messages.success(self.request, 'Empresa atualizada com sucesso!')
        return super().form_valid(form)