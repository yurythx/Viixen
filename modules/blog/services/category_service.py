"""
Serviço para gerenciar operações relacionadas a categorias do blog.
"""
from typing import List, Optional

from django.db.models import Count, Q

from ..domain.post import Category
from ..repositories import CategoryRepository, PostRepository
from .base import BaseService


class CategoryService(BaseService[Category]):
    """
    Serviço para gerenciar operações relacionadas a categorias do blog.
    """
    
    def __init__(self, repository=None):
        super().__init__(repository or CategoryRepository())
        self.post_repo = PostRepository()
    
    def get_active_categories(self) -> List[Category]:
        """
        Retorna todas as categorias ativas.
        
        Returns:
            Lista de categorias ativas
        """
        return list(self.repository.get_published_categories())
    
    def get_categories_with_posts_count(self) -> List[Category]:
        """
        Retorna categorias com contagem de posts publicados.
        
        Returns:
            Lista de categorias anotadas com contagem de posts
        """
        categories = self.get_active_categories()
        
        # Para cada categoria, adiciona a contagem de posts publicados
        for category in categories:
            category.posts_count = self.post_repo.list_all(
                category=category,
                status='published'
            ).count()
            
        return categories
    
    def get_category_with_posts(self, slug: str) -> Optional[Category]:
        """
        Obtém uma categoria com seus posts relacionados.
        
        Args:
            slug: Slug da categoria
            
        Returns:
            A categoria com os posts relacionados ou None se não encontrada
        """
        return self.repository.get_category_with_posts(slug)
    
    def create_category(
        self,
        name: str,
        description: str = '',
        is_active: bool = True,
        **extra_fields
    ) -> Category:
        """
        Cria uma nova categoria.
        
        Args:
            name: Nome da categoria
            description: Descrição da categoria (opcional)
            is_active: Se a categoria está ativa
            **extra_fields: Campos adicionais
            
        Returns:
            A categoria criada
        """
        return self.repository.create(
            name=name,
            description=description,
            is_active=is_active,
            **extra_fields
        )
    
    def update_category(
        self,
        category: Category,
        name: str = None,
        description: str = None,
        is_active: bool = None,
        **extra_fields
    ) -> Category:
        """
        Atualiza uma categoria existente.
        
        Args:
            category: Categoria a ser atualizada
            name: Novo nome (opcional)
            description: Nova descrição (opcional)
            is_active: Novo status de ativação (opcional)
            **extra_fields: Campos adicionais
            
        Returns:
            A categoria atualizada
        """
        update_fields = {}
        
        if name is not None:
            update_fields['name'] = name
        if description is not None:
            update_fields['description'] = description
        if is_active is not None:
            update_fields['is_active'] = is_active
            
        update_fields.update(extra_fields)
        
        return self.repository.update(category, **update_fields)
    
    def delete_category(self, category: Category) -> None:
        """
        Remove uma categoria.
        
        Args:
            category: Categoria a ser removida
            
        Note:
            A categoria só pode ser removida se não tiver posts associados
        """
        # Verifica se a categoria tem posts
        if self.post_repo.list_all(category=category).exists():
            raise ValueError("Não é possível excluir uma categoria que possui posts associados.")
            
        self.repository.delete(category)