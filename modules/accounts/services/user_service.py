from typing import List, Optional
from django.db.models import QuerySet
from django.contrib.auth import authenticate
from ..domain.user import CustomUser
from ..repositories.user_repository import UserRepository
from ...config.domain.company import Company

class UserService:
    def __init__(self):
        self.repository = UserRepository()
    
    def get_user_by_id(self, user_id: int) -> Optional[CustomUser]:
        return self.repository.get_by_id(user_id)
    
    def get_users_by_company(self, company: Company) -> QuerySet[CustomUser]:
        return self.repository.get_by_company(company)
    
    def get_active_users_by_company(self, company: Company) -> QuerySet[CustomUser]:
        return self.repository.get_active_by_company(company)
    
    def create_user(self, company: Company, **user_data) -> CustomUser:
        user_data['company'] = company
        return self.repository.create(**user_data)
    
    def update_user(self, user: CustomUser, **kwargs) -> CustomUser:
        return self.repository.update(user, **kwargs)
    
    def deactivate_user(self, user: CustomUser) -> CustomUser:
        return self.repository.update(user, is_active=False)
    
    def activate_user(self, user: CustomUser) -> CustomUser:
        return self.repository.update(user, is_active=True)
    
    def authenticate_user(self, username: str, password: str) -> Optional[CustomUser]:
        return authenticate(username=username, password=password)
    
    def get_company_admins(self, company: Company) -> QuerySet[CustomUser]:
        return self.repository.get_company_admins(company)