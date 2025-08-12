"""
Repositório para o modelo Tag.
"""
from typing import List, Optional

from django.db.models import Count, QuerySet

from ..domain.post import Tag
from .django_repository import DjangoRepository


class TagRepository(DjangoRepository[Tag]):
    """
    Repositório para operações com tags.
    """
    
    def __init__(self):
        super().__init__(Tag)
    
    def get_active_tags(self) -> QuerySet[Tag]:
        """
        Retorna todas as tags ativas.
        
        Returns:
            QuerySet de tags ativas
        """
        return self.list_all(is_active=True)
    
    def get_popular_tags(self, limit: int = 10) -> QuerySet[Tag]:
        """
        Retorna as tags mais populares (com mais posts).
        
        Args:
            limit: Número máximo de tags a retornar
            
        Returns:
            QuerySet das tags mais populares
        """
        return self.model_class.objects.filter(
            is_active=True
        ).annotate(
            post_count=Count('blogpost')
        ).filter(
            post_count__gt=0
        ).order_by(
            '-post_count', 'name'
        )[:limit]
    
    def get_or_create_tags(self, tag_names: List[str]):
        """
        Obtém ou cria tags a partir de uma lista de nomes.
        
        Args:
            tag_names: Lista de nomes de tags
            
        Returns:
            QuerySet das tags encontradas ou criadas
        """
        if not tag_names:
            return self.model_class.objects.none()
            
        tags = []
        for name in tag_names:
            name = name.strip()
            if not name:
                continue
                
            tag, _ = self.model_class.objects.get_or_create(
                name=name,
                defaults={'name': name, 'is_active': True}
            )
            tags.append(tag)
            
        return tags
    
    def get_tag_with_posts(self, slug: str) -> Optional[Tag]:
        """
        Obtém uma tag com seus posts relacionados.
        
        Args:
            slug: Slug da tag
            
        Returns:
            A tag com os posts relacionados ou None se não encontrada
        """
        try:
            return self.model_class.objects.prefetch_related(
                'blogpost_set',
                'blogpost_set__author',
                'blogpost_set__category'
            ).get(
                slug=slug,
                is_active=True
            )
        except self.model_class.DoesNotExist:
            return None
