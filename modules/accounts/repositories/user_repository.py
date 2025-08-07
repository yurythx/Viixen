from typing import Optional
from django.db.models import QuerySet
from ..domain.user import CustomUser
from ...config.domain.company import Company

class UserRepository:
    def get_by_id(self, user_id: int) -> Optional[CustomUser]:
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    
    def get_by_username(self, username: str) -> Optional[CustomUser]:
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[CustomUser]:
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
    
    def get_by_company(self, company: Company) -> QuerySet[CustomUser]:
        return CustomUser.objects.filter(company=company)
    
    def get_active_by_company(self, company: Company) -> QuerySet[CustomUser]:
        return CustomUser.objects.filter(company=company, is_active=True)
    
    def get_company_admins(self, company: Company) -> QuerySet[CustomUser]:
        return CustomUser.objects.filter(
            company=company, 
            is_company_admin=True, 
            is_active=True
        )
    
    def create(self, **kwargs) -> CustomUser:
        return CustomUser.objects.create_user(**kwargs)
    
    def update(self, user: CustomUser, **kwargs) -> CustomUser:
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user
    
    def delete(self, user: CustomUser) -> bool:
        user.delete()
        return True