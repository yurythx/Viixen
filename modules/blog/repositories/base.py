"""
Módulo base para repositórios.
Define a interface comum para operações CRUD.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Type
from django.db.models import Model, QuerySet

T = TypeVar('T', bound=Model)

class BaseRepository(Generic[T], ABC):
    """
    Classe base abstrata para repositórios.
    Define a interface comum para operações CRUD.
    """
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtém uma entidade pelo ID.
        
        Args:
            id: ID da entidade
            
        Returns:
            A entidade encontrada ou None se não existir
        """
        pass
    
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[T]:
        """
        Obtém uma entidade pelo slug.
        
        Args:
            slug: Slug da entidade
            
        Returns:
            A entidade encontrada ou None se não existir
        """
        pass
    
    @abstractmethod
    def list_all(self, **filters) -> QuerySet[T]:
        """
        Lista todas as entidades, opcionalmente filtradas.
        
        Args:
            **filters: Filtros opcionais para aplicar na consulta
            
        Returns:
            QuerySet das entidades encontradas
        """
        pass
    
    @abstractmethod
    def create(self, **kwargs) -> T:
        """
        Cria uma nova entidade.
        
        Args:
            **kwargs: Atributos da entidade
            
        Returns:
            A entidade criada
        """
        pass
    
    @abstractmethod
    def update(self, entity: T, **kwargs) -> T:
        """
        Atualiza uma entidade existente.
        
        Args:
            entity: Entidade a ser atualizada
            **kwargs: Atributos para atualizar
            
        Returns:
            A entidade atualizada
        """
        pass
    
    @abstractmethod
    def delete(self, entity: T) -> None:
        """
        Remove uma entidade.
        
        Args:
            entity: Entidade a ser removida
        """
        pass
