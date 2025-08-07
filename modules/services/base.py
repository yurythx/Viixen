from abc import ABC, abstractmethod
from typing import Any, Optional, List
from django.db.models import QuerySet, Model

class BaseService(ABC):
    """Service base abstrato seguindo princípios SOLID"""
    
    def __init__(self):
        self.repository = self.get_repository()
    
    @abstractmethod
    def get_repository(self):
        """Retorna o repositório específico do service"""
        pass
    
    def get_by_id(self, id: int) -> Optional[Any]:
        """Busca objeto por ID"""
        return self.repository.get_by_id(id)
    
    def get_all(self) -> QuerySet:
        """Retorna todos os objetos"""
        return self.repository.get_all()
    
    def create(self, **kwargs) -> Any:
        """Cria novo objeto"""
        return self.repository.create(**kwargs)
    
    def update(self, obj: Model, **kwargs) -> Any:
        """Atualiza objeto existente"""
        return self.repository.update(obj, **kwargs)
    
    def delete(self, obj: Model) -> bool:
        """Remove objeto"""
        return self.repository.delete(obj)
    
    @abstractmethod
    def get_by_company(self, company) -> QuerySet:
        """Filtra objetos por empresa - deve ser implementado por cada service"""
        pass