"""
Serviço para gerenciar operações relacionadas a posts do blog.
"""
from datetime import datetime
from typing import List, Optional, Tuple

from django.db.models import Q, F
from django.utils import timezone

from ..domain.post import BlogPost, Category, Tag
from ..repositories import PostRepository, CategoryRepository, TagRepository
from .base import BaseService


class PostService(BaseService[BlogPost]):
    """
    Serviço para gerenciar operações relacionadas a posts do blog.
    """
    
    def __init__(self, repository=None):
        super().__init__(repository or PostRepository())
        self.category_repo = CategoryRepository()
        self.tag_repo = TagRepository()
    
    def get_published_posts(self) -> List[BlogPost]:
        """
        Retorna todos os posts publicados.
        
        Returns:
            Lista de posts publicados
        """
        return list(self.repository.get_published_posts())
    
    def get_featured_posts(self, limit: int = 5) -> List[BlogPost]:
        """
        Retorna posts em destaque.
        
        Args:
            limit: Número máximo de posts a retornar
            
        Returns:
            Lista de posts em destaque
        """
        return list(self.get_published_posts().filter(
            is_featured=True
        ).order_by('-published_at')[:limit])
    
    def get_recent_posts(self, limit: int = 5) -> List[BlogPost]:
        """
        Retorna os posts mais recentes.
        
        Args:
            limit: Número máximo de posts a retornar
            
        Returns:
            Lista de posts mais recentes
        """
        return list(self.get_published_posts().order_by(
            '-published_at'
        )[:limit])
    
    def search_posts(self, query: str) -> List[BlogPost]:
        """
        Busca posts por termo de pesquisa.
        
        Args:
            query: Termo de busca
            
        Returns:
            Lista de posts que correspondem à busca
        """
        return list(self.get_published_posts().filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        ).distinct())
    
    def get_posts_by_category(self, category_slug: str) -> List[BlogPost]:
        """
        Retorna posts por categoria.
        
        Args:
            category_slug: Slug da categoria
            
        Returns:
            Lista de posts da categoria
        """
        return list(self.repository.get_posts_by_category(category_slug))
    
    def get_posts_by_tag(self, tag_slug: str) -> List[BlogPost]:
        """
        Retorna posts por tag.
        
        Args:
            tag_slug: Slug da tag
            
        Returns:
            Lista de posts com a tag
        """
        return list(self.repository.get_posts_by_tag(tag_slug))
    
    def get_related_posts(self, post: BlogPost, limit: int = 3) -> List[BlogPost]:
        """
        Retorna posts relacionados a um post específico.
        
        Args:
            post: Post de referência
            limit: Número máximo de posts relacionados
            
        Returns:
            Lista de posts relacionados
        """
        return list(self.repository.get_related_posts(post, limit))
    
    def get_popular_posts(self, limit: int = 5) -> List[BlogPost]:
        """
        Retorna os posts mais populares.
        
        Args:
            limit: Número máximo de posts a retornar
            
        Returns:
            Lista de posts mais visualizados
        """
        return list(self.repository.get_popular_posts(limit))
    
    def get_archive_months(self) -> List[Tuple[int, int]]:
        """
        Retorna uma lista de tuplas (ano, mês) para arquivamento.
        
        Returns:
            Lista de tuplas (ano, mês) ordenadas por data decrescente
        """
        return self.repository.get_archive_months()
    
    def get_posts_by_month(self, year: int, month: int) -> List[BlogPost]:
        """
        Retorna posts publicados em um determinado mês/ano.
        
        Args:
            year: Ano de publicação
            month: Mês de publicação (1-12)
            
        Returns:
            Lista de posts publicados no período
        """
        return list(self.repository.get_posts_by_month(year, month))
    
    def publish_post(self, post_id: int) -> Optional[BlogPost]:
        """
        Publica um post.
        
        Args:
            post_id: ID do post a ser publicado
            
        Returns:
            O post publicado ou None se não encontrado
        """
        post = self.get_by_id(post_id)
        if post:
            post.status = 'published'
            if not post.published_at:
                post.published_at = timezone.now()
            post.save()
        return post
    
    def increment_views(self, post_id: int) -> None:
        """
        Incrementa o contador de visualizações de um post.
        
        Args:
            post_id: ID do post
        """
        self.repository.increment_views(post_id)
    
    def create_post(
        self,
        title: str,
        content: str,
        author_id: int,
        category_id: int,
        excerpt: str = '',
        is_featured: bool = False,
        status: str = 'draft',
        tags: List[str] = None,
        **extra_fields
    ) -> BlogPost:
        """
        Cria um novo post.
        
        Args:
            title: Título do post
            content: Conteúdo do post
            author_id: ID do autor
            category_id: ID da categoria
            excerpt: Resumo do post (opcional)
            is_featured: Se o post é destaque
            status: Status do post (draft, published, archived)
            tags: Lista de tags (nomes)
            **extra_fields: Campos adicionais
            
        Returns:
            O post criado
        """
        if tags is None:
            tags = []
            
        # Cria o post
        post = self.repository.create(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category_id,
            excerpt=excerpt,
            is_featured=is_featured,
            status=status,
            **extra_fields
        )
        
        # Adiciona as tags
        if tags:
            tag_objs = self.tag_repo.get_or_create_tags(tags)
            post.tags.set(tag_objs)
        
        return post