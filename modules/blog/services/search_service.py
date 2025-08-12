"""
Serviço para gerenciar buscas no blog.
"""
from typing import Dict, List, Optional, Tuple

from django.conf import settings
from django.db.models import Q

from ..domain.post import BlogPost, Category, Tag
from ..repositories import (
    CategoryRepository, 
    PostRepository, 
    TagRepository
)


class SearchService:
    """
    Serviço para gerenciar buscas no blog.
    """
    
    def __init__(self, post_repo=None, category_repo=None, tag_repo=None):
        self.post_repo = post_repo or PostRepository()
        self.category_repo = category_repo or CategoryRepository()
        self.tag_repo = tag_repo or TagRepository()
    
    def search_posts(
        self,
        query: str,
        category_slug: str = None,
        tag_slug: str = None,
        author_id: int = None,
        status: str = 'published',
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[BlogPost], int]:
        """
        Busca posts com base em uma consulta e filtros opcionais.
        
        Args:
            query: Termo de busca
            category_slug: Slug da categoria para filtrar (opcional)
            tag_slug: Slug da tag para filtrar (opcional)
            author_id: ID do autor para filtrar (opcional)
            status: Status dos posts a serem buscados (padrão: 'published')
            limit: Número máximo de resultados a retornar
            offset: Número de resultados a pular
            
        Returns:
            Tupla contendo a lista de posts encontrados e o total de resultados
        """
        # Filtra os posts por status
        queryset = self.post_repo.list_all(status=status)
        
        # Aplica filtros adicionais
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
            
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Aplica a busca por texto
        if query:
            queryset = self._apply_search_query(queryset, query)
        
        # Ordena por data de publicação (mais recentes primeiro)
        queryset = queryset.order_by('-published_at')
        
        # Conta o total de resultados
        total = queryset.count()
        
        # Aplica paginação
        results = list(queryset[offset:offset + limit])
        
        return results, total
    
    def _apply_search_query(self, queryset, query: str):
        """
        Aplica a consulta de busca ao queryset.
        
        Args:
            queryset: QuerySet inicial
            query: Termo de busca
            
        Returns:
            QuerySet filtrado
        """
        # Divide a consulta em termos
        terms = query.split()
        
        # Cria uma lista de condições OR para cada termo
        or_conditions = Q()
        
        for term in terms:
            # Busca no título, resumo, conteúdo e slug
            or_conditions |= Q(title__icontains=term)
            or_conditions |= Q(excerpt__icontains=term)
            or_conditions |= Q(content__icontains=term)
            or_conditions |= Q(slug__icontains=term)
        
        # Aplica as condições ao queryset
        return queryset.filter(or_conditions)
    
    def search_categories(
        self,
        query: str = None,
        is_active: bool = True,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[Category], int]:
        """
        Busca categorias com base em uma consulta e filtros opcionais.
        
        Args:
            query: Termo de busca (opcional)
            is_active: Filtro por categorias ativas/inativas
            limit: Número máximo de resultados a retornar
            offset: Número de resultados a pular
            
        Returns:
            Tupla contendo a lista de categorias encontradas e o total de resultados
        """
        queryset = self.category_repo.list_all(is_active=is_active)
        
        # Aplica a busca por texto, se fornecido
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(slug__icontains=query)
            )
        
        # Ordena por nome
        queryset = queryset.order_by('name')
        
        # Conta o total de resultados
        total = queryset.count()
        
        # Aplica paginação
        results = list(queryset[offset:offset + limit])
        
        return results, total
    
    def search_tags(
        self,
        query: str = None,
        is_active: bool = True,
        min_posts: int = 0,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[Tag], int]:
        """
        Busca tags com base em uma consulta e filtros opcionais.
        
        Args:
            query: Termo de busca (opcional)
            is_active: Filtro por tags ativas/inativas
            min_posts: Número mínimo de posts associados à tag
            limit: Número máximo de resultados a retornar
            offset: Número de resultados a pular
            
        Returns:
            Tupla contendo a lista de tags encontradas e o total de resultados
        """
        from django.db.models import Count
        
        queryset = self.tag_repo.list_all(is_active=is_active)
        
        # Filtra por número mínimo de posts, se especificado
        if min_posts > 0:
            queryset = queryset.annotate(
                post_count=Count('posts')
            ).filter(
                post_count__gte=min_posts
            )
        
        # Aplica a busca por texto, se fornecido
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(slug__icontains=query)
            )
        
        # Ordena por nome
        queryset = queryset.order_by('name')
        
        # Conta o total de resultados
        total = queryset.count()
        
        # Aplica paginação
        results = list(queryset[offset:offset + limit])
        
        return results, total
    
    def global_search(
        self,
        query: str,
        limit_per_type: int = 5
    ) -> Dict[str, dict]:
        """
        Realiza uma busca global em posts, categorias e tags.
        
        Args:
            query: Termo de busca
            limit_per_type: Número máximo de resultados por tipo
            
        Returns:
            Dicionário com os resultados da busca agrupados por tipo
        """
        # Busca posts
        posts, posts_total = self.search_posts(
            query=query,
            limit=limit_per_type
        )
        
        # Busca categorias
        categories, categories_total = self.search_categories(
            query=query,
            limit=limit_per_type
        )
        
        # Busca tags
        tags, tags_total = self.search_tags(
            query=query,
            limit=limit_per_type
        )
        
        return {
            'posts': {
                'results': posts,
                'total': posts_total,
                'has_more': posts_total > len(posts)
            },
            'categories': {
                'results': categories,
                'total': categories_total,
                'has_more': categories_total > len(categories)
            },
            'tags': {
                'results': tags,
                'total': tags_total,
                'has_more': tags_total > len(tags)
            },
            'query': query
        }
