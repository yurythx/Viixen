from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...domain.company import Company
from ...services.company_service import CompanyService

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'config/companies/list.html'
    context_object_name = 'companies'
    paginate_by = 10
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CompanyService()
    
    def get_queryset(self):
        return self.service.get_companies_with_stats()