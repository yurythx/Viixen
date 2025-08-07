from typing import Optional
from django.db.models import QuerySet
from ..domain.company import Company

class CompanyRepository:
    def get_by_id(self, company_id: int) -> Optional[Company]:
        try:
            return Company.objects.get(id=company_id, is_active=True)
        except Company.DoesNotExist:
            return None
    
    def get_by_domain(self, domain: str) -> Optional[Company]:
        try:
            return Company.objects.get(domain=domain, is_active=True)
        except Company.DoesNotExist:
            return None
    
    def get_by_slug(self, slug: str) -> Optional[Company]:
        try:
            return Company.objects.get(slug=slug, is_active=True)
        except Company.DoesNotExist:
            return None
    
    def get_all_active(self) -> QuerySet[Company]:
        return Company.objects.filter(is_active=True)
    
    def create(self, **kwargs) -> Company:
        return Company.objects.create(**kwargs)
    
    def update(self, company: Company, **kwargs) -> Company:
        for key, value in kwargs.items():
            setattr(company, key, value)
        company.save()
        return company
    
    def delete(self, company: Company) -> bool:
        company.is_active = False
        company.save()
        return True