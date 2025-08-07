from django.db.models import QuerySet
from ..domain.company import Company

class CompanyRepository:
    def get_all(self) -> QuerySet[Company]:
        return Company.objects.all()
    
    def get_active(self) -> QuerySet[Company]:
        return Company.objects.filter(is_active=True)
    
    def get_by_id(self, company_id: int) -> Company:
        return Company.objects.get(id=company_id)
    
    def get_by_slug(self, slug: str) -> Company:
        return Company.objects.get(slug=slug)
    
    def create(self, **kwargs) -> Company:
        return Company.objects.create(**kwargs)
    
    def update(self, company_id: int, **kwargs) -> Company:
        company = self.get_by_id(company_id)
        for key, value in kwargs.items():
            setattr(company, key, value)
        company.save()
        return company