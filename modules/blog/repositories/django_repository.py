"""
Implementação concreta de repositório para Django ORM.
"""
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from django.db import models
from django.db.models import QuerySet

from . import BaseRepository

T = TypeVar('T', bound=models.Model)

class DjangoRepository(BaseRepository[T]):
    """
    Implementação concreta de repositório usando Django ORM.
    """
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtém uma entidade pelo ID.
        
        Args:
            id: ID da entidade
            
        Returns:
            A entidade encontrada ou None se não existir
        """
        try:
            return self.model_class.objects.get(pk=id)
        except self.model_class.DoesNotExist:
            return None
    
    def get_by_slug(self, slug: str) -> Optional[T]:
        """
        Obtém uma entidade pelo slug.
        
        Args:
            slug: Slug da entidade
            
        Returns:
            A entidade encontrada ou None se não existir
        """
        try:
            return self.model_class.objects.get(slug=slug)
        except (self.model_class.DoesNotExist, AttributeError):
            return None
    
    def list_all(self, **filters) -> QuerySet[T]:
        """
        Lista todas as entidades, opcionalmente filtradas.
        
        Args:
            **filters: Filtros opcionais para aplicar na consulta
            
        Returns:
            QuerySet das entidades encontradas
        """
        return self.model_class.objects.filter(**filters).all()
    
    def create(self, **kwargs) -> T:
        """
        Cria uma nova entidade.
        
        Args:
            **kwargs: Atributos da entidade
            
        Returns:
            A entidade criada
        """
        return self.model_class.objects.create(**kwargs)
    
    def update(self, entity: T, **kwargs) -> T:
        """
        Atualiza uma entidade existente.
        
        Args:
            entity: Entidade a ser atualizada
            **kwargs: Atributos para atualizar
            
        Returns:
            A entidade atualizada
        """
        for field, value in kwargs.items():
            setattr(entity, field, value)
        entity.save()
        return entity
    
    def delete(self, entity: T) -> None:
        """
        Remove uma entidade.
        
        Args:
            entity: Entidade a ser removida
        """
        entity.delete()
    
    def get_or_create(self, defaults: Optional[Dict[str, Any]] = None, **kwargs) -> tuple[T, bool]:
        """
        Obtém uma entidade ou a cria se não existir.
        
        Args:
            defaults: Valores padrão para criação
            **kwargs: Filtros para busca
            
        Returns:
            Tupla contendo a entidade e um booleano indicando se foi criada
        """
        if defaults is None:
            defaults = {}
        return self.model_class.objects.get_or_create(defaults=defaults, **kwargs)
