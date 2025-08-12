"""
Repositório para o modelo Category.
"""
from typing import List, Optional

from django.db.models import QuerySet

from ..domain.post import Category
from .django_repository import DjangoRepository


class CategoryRepository(DjangoRepository[Category]):
    """
    Repositório para operações com categorias.
    """
    
    def __init__(self):
        super().__init__(Category)
    
    def get_published_categories(self) -> QuerySet[Category]:
        """
        Retorna todas as categorias publicadas.
        
        Returns:
            QuerySet de categorias publicadas
        """
        return self.list_all(is_active=True)
    
    def get_category_with_posts(self, slug: str) -> Optional[Category]:
        """
        Obtém uma categoria com seus posts relacionados.
        
        Args:
            slug: Slug da categoria
            
        Returns:
            A categoria com os posts relacionados ou None se não encontrada
        """
        try:
            return self.model_class.objects.select_related('author')\
                                        .prefetch_related('blogpost_set')\
                                        .get(slug=slug, is_active=True)
        except self.model_class.DoesNotExist:
            return None
