"""
Repositório para o modelo BlogPost.
"""
from datetime import datetime
from typing import List, Optional, Tuple

from django.db.models import Count, F, Prefetch, Q, QuerySet

from ..domain.post import BlogPost, Category, Tag
from .django_repository import DjangoRepository


class PostRepository(DjangoRepository[BlogPost]):
    """
    Repositório para operações com posts do blog.
    """
    
    def __init__(self):
        super().__init__(BlogPost)
    
    def get_published_posts(self) -> QuerySet[BlogPost]:
        """
        Retorna todos os posts publicados.
        
        Returns:
            QuerySet de posts publicados
        """
        return self.list_all(
            status='published',
            published_at__lte=datetime.now()
        ).select_related('author', 'category')
    
    def get_post_by_slug(self, slug: str) -> Optional[BlogPost]:
        """
        Obtém um post publicado pelo slug.
        
        Args:
            slug: Slug do post
            
        Returns:
            O post encontrado ou None se não existir ou não estiver publicado
        """
        try:
            return self.model_class.objects.select_related('author', 'category')\
                                       .prefetch_related('tags')\
                                       .get(
                                           slug=slug,
                                           status='published',
                                           published_at__lte=datetime.now()
                                       )
        except self.model_class.DoesNotExist:
            return None
    
    def get_posts_by_category(self, category_slug: str) -> QuerySet[BlogPost]:
        """
        Retorna posts publicados por categoria.
        
        Args:
            category_slug: Slug da categoria
            
        Returns:
            QuerySet de posts da categoria
        """
        return self.get_published_posts().filter(
            category__slug=category_slug,
            category__is_active=True
        )
    
    def get_posts_by_tag(self, tag_slug: str) -> QuerySet[BlogPost]:
        """
        Retorna posts publicados por tag.
        
        Args:
            tag_slug: Slug da tag
            
        Returns:
            QuerySet de posts com a tag
        """
        return self.get_published_posts().filter(
            tags__slug=tag_slug,
            tags__is_active=True
        ).distinct()
    
    def get_related_posts(self, post: BlogPost, limit: int = 3) -> QuerySet[BlogPost]:
        """
        Retorna posts relacionados a um post específico.
        
        Args:
            post: Post de referência
            limit: Número máximo de posts relacionados a retornar
            
        Returns:
            QuerySet de posts relacionados
        """
        # Posts da mesma categoria, excluindo o próprio post
        related = self.get_published_posts().filter(
            category=post.category
        ).exclude(
            pk=post.pk
        ).order_by(
            '-published_at', '-created_at'
        )[:limit]
        
        # Se não houver posts suficientes na mesma categoria,
        # completa com os mais recentes
        if related.count() < limit:
            additional = self.get_published_posts().exclude(
                Q(pk=post.pk) | Q(pk__in=[p.pk for p in related])
            ).order_by('-published_at', '-created_at')[:limit - related.count()]
            related = list(related) + list(additional)
        
        return related
    
    def increment_views(self, post_id: int) -> None:
        """
        Incrementa o contador de visualizações de um post.
        
        Args:
            post_id: ID do post
        """
        self.model_class.objects.filter(pk=post_id).update(
            views_count=F('views_count') + 1
        )
    
    def get_popular_posts(self, limit: int = 5) -> QuerySet[BlogPost]:
        """
        Retorna os posts mais populares.
        
        Args:
            limit: Número máximo de posts a retornar
            
        Returns:
            QuerySet dos posts mais visualizados
        """
        return self.get_published_posts().order_by('-views_count', '-published_at')[:limit]
    
    def get_archive_months(self) -> List[Tuple[int, int]]:
        """
        Retorna uma lista de tuplas (ano, mês) para arquivamento.
        
        Returns:
            Lista de tuplas (ano, mês) ordenadas por data decrescente
        """
        return list(self.get_published_posts().datetimes(
            'published_at', 'month', order='DESC'
        ).values_list('year', 'month').distinct())
    
    def get_posts_by_month(self, year: int, month: int) -> QuerySet[BlogPost]:
        """
        Retorna posts publicados em um determinado mês/ano.
        
        Args:
            year: Ano de publicação
            month: Mês de publicação (1-12)
            
        Returns:
            QuerySet de posts publicados no período
        """
        return self.get_published_posts().filter(
            published_at__year=year,
            published_at__month=month
        )
