"""
Módulo base para serviços.
Define a interface comum para operações de negócio.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from django.db.models import Model, QuerySet

T = TypeVar('T', bound=Model)

class BaseService(Generic[T], ABC):
    """
    Classe base abstrata para serviços.
    Define a interface comum para operações de negócio.
    """
    
    def __init__(self, repository=None):
        """
        Inicializa o serviço com um repositório opcional.
        
        Args:
            repository: Instância do repositório a ser usado
        """
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtém uma entidade pelo ID.
        
        Args:
            id: ID da entidade
            
        Returns:
            A entidade encontrada ou None se não existir
        """
        return self.repository.get_by_id(id)
    
    def get_by_slug(self, slug: str) -> Optional[T]:
        """
        Obtém uma entidade pelo slug.
        
        Args:
            slug: Slug da entidade
            
        Returns:
            A entidade encontrada ou None se não existir
        """
        return self.repository.get_by_slug(slug)
    
    def list_all(self, **filters) -> QuerySet[T]:
        """
        Lista todas as entidades, opcionalmente filtradas.
        
        Args:
            **filters: Filtros opcionais para aplicar na consulta
            
        Returns:
            QuerySet das entidades encontradas
        """
        return self.repository.list_all(**filters)
    
    def create(self, **kwargs) -> T:
        """
        Cria uma nova entidade.
        
        Args:
            **kwargs: Atributos da entidade
            
        Returns:
            A entidade criada
            
        Raises:
            ValidationError: Se a validação falhar
        """
        self._validate_create(**kwargs)
        return self.repository.create(**kwargs)
    
    def update(self, entity: T, **kwargs) -> T:
        """
        Atualiza uma entidade existente.
        
        Args:
            entity: Entidade a ser atualizada
            **kwargs: Atributos para atualizar
            
        Returns:
            A entidade atualizada
            
        Raises:
            ValidationError: Se a validação falhar
        """
        self._validate_update(entity, **kwargs)
        return self.repository.update(entity, **kwargs)
    
    def delete(self, entity: T) -> None:
        """
        Remove uma entidade.
        
        Args:
            entity: Entidade a ser removida
            
        Raises:
            ValidationError: Se a validação falhar
        """
        self._validate_delete(entity)
        self.repository.delete(entity)
    
    def _validate_create(self, **kwargs) -> None:
        """
        Valida os dados antes de criar uma entidade.
        
        Args:
            **kwargs: Atributos da entidade
            
        Raises:
            ValidationError: Se a validação falhar
        """
        pass
    
    def _validate_update(self, entity: T, **kwargs) -> None:
        """
        Valida os dados antes de atualizar uma entidade.
        
        Args:
            entity: Entidade a ser atualizada
            **kwargs: Atributos para atualizar
            
        Raises:
            ValidationError: Se a validação falhar
        """
        pass
    
    def _validate_delete(self, entity: T) -> None:
        """
        Valida se uma entidade pode ser excluída.
        
        Args:
            entity: Entidade a ser removida
            
        Raises:
            ValidationError: Se a validação falhar
        """
        pass
