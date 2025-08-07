from typing import List, Optional
from django.db.models import QuerySet
from ..domain.company import Company
from ..domain.module import Module, CompanyModule
from ..repositories.company_repository import CompanyRepository

class CompanyService:
    def __init__(self):
        self.repository = CompanyRepository()
    
    def get_company_by_id(self, company_id: int) -> Optional[Company]:
        return self.repository.get_by_id(company_id)
    
    def get_company_by_domain(self, domain: str) -> Optional[Company]:
        return self.repository.get_by_domain(domain)
    
    def get_available_modules(self) -> QuerySet[Module]:
        return Module.objects.filter(is_active=True).order_by('order')
    
    def get_company_active_modules(self, company: Company) -> QuerySet[Module]:
        return Module.objects.filter(
            companymodule__company=company,
            companymodule__is_active=True
        ).order_by('order')
    
    def activate_module(self, company: Company, module: Module) -> CompanyModule:
        company_module, created = CompanyModule.objects.get_or_create(
            company=company,
            module=module,
            defaults={'is_active': True}
        )
        
        if not created and not company_module.is_active:
            company_module.is_active = True
            company_module.save()
        
        return company_module
    
    def deactivate_module(self, company: Company, module: Module) -> bool:
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            company_module.is_active = False
            company_module.save()
            return True
        except CompanyModule.DoesNotExist:
            return False
    
    def update_company(self, company: Company, **kwargs) -> Company:
        return self.repository.update(company, **kwargs)