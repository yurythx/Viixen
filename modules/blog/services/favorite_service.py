"""
Serviço para gerenciar posts favoritos dos usuários.

Exemplo de uso:
    ```python
    # Obter instância do serviço
    from django.contrib.auth import get_user_model
    from blog.services import FavoriteService
    
    user = get_user_model().objects.get(username='usuario')
    service = FavoriteService()
    
    # Adicionar aos favoritos
    service.add_to_favorites(user, 'meu-post')
    
    # Verificar se está nos favoritos
    is_fav = service.is_favorite(user, 'meu-post')
    
    # Listar favoritos
    favoritos = service.get_user_favorites(user, limit=10)
    ```
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone

from ..domain.post import BlogPost, Favorite
from ..repositories import PostRepository

# Tempo de expiração do cache em segundos (1 hora)
CACHE_TIMEOUT = 60 * 60

User = get_user_model()


class FavoriteService:
    """
    Serviço para gerenciar posts favoritos dos usuários.
    
    Este serviço fornece métodos para:
    - Adicionar/remover posts dos favoritos
    - Verificar se um post está nos favoritos
    - Listar posts favoritos de um usuário
    - Obter estatísticas sobre favoritos
    - Encontrar usuários com interesses semelhantes
    """
    
    def __init__(self, post_repo=None):
        """
        Inicializa o serviço de favoritos.
        
        Args:
            post_repo: Repositório de posts (opcional, será instanciado se não fornecido)
        """
        self.post_repo = post_repo or PostRepository()
        self.cache = cache
    
    def get_user_favorites(
        self, 
        user: User,
        limit: Optional[int] = None,
        offset: int = 0,
        use_cache: bool = True
    ) -> List[BlogPost]:
        """
        Retorna os posts favoritos de um usuário com suporte a cache.
        
        Args:
            user: Instância do usuário
            limit: Número máximo de favoritos a retornar
            offset: Número de itens a pular
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            Lista de posts favoritos do usuário
            
        Raises:
            ValueError: Se o usuário não estiver autenticado
        """
        if not user.is_authenticated:
            raise ValueError("O usuário deve estar autenticado")
            
        cache_key = f'user_{user.id}_favorites_{offset}_{limit}'
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
        
        try:
            queryset = BlogPost.objects.filter(
                favorites__user=user,
                status='published'
            ).order_by('-favorites__created_at')
            
            if limit is not None:
                queryset = queryset[offset:offset + limit]
                
            result = list(queryset)
            
            if use_cache:
                self.cache.set(cache_key, result, CACHE_TIMEOUT)
                
            return result
            
        except Exception as e:
            # Log do erro e retorna lista vazia em caso de falha
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao buscar favoritos do usuário {user.id}: {str(e)}")
            return []
    
    def add_to_favorites(self, user: User, post_slug: str) -> Tuple[bool, str]:
        """
        Adiciona um post aos favoritos do usuário.
        
        Args:
            user: Instância do usuário
            post_slug: Slug do post a ser favoritado
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
            
        Example:
            >>> success, message = service.add_to_favorites(user, 'meu-post')
            >>> if success:
            ...     print(f"Sucesso: {message}")
            ... else:
            ...     print(f"Erro: {message}")
        """
        if not user.is_authenticated:
            return False, "Usuário não autenticado"
            
        try:
            post = self.post_repo.get_post_by_slug(post_slug)
            if not post:
                return False, f"Post com slug '{post_slug}' não encontrado"
                
            if post.status != 'published':
                return False, "Não é possível favoritar um post não publicado"
                
            favorite, created = Favorite.objects.get_or_create(
                user=user,
                post=post
            )
            
            if created:
                # Invalida o cache de favoritos do usuário
                self._invalidate_user_cache(user.id)
                return True, "Post adicionado aos favoritos com sucesso"
            else:
                return False, "Este post já está nos seus favoritos"
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao adicionar favorito: {str(e)}")
            return False, f"Erro ao adicionar favorito: {str(e)}"
    
    def remove_from_favorites(self, user: User, post_slug: str) -> Tuple[bool, str]:
        """
        Remove um post dos favoritos do usuário.
        
        Args:
            user: Instância do usuário
            post_slug: Slug do post a ser removido dos favoritos
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
            
        Example:
            >>> success, message = service.remove_from_favorites(user, 'meu-post')
            >>> if success:
            ...     print(f"Sucesso: {message}")
            ... else:
            ...     print(f"Erro: {message}")
        """
        if not user.is_authenticated:
            return False, "Usuário não autenticado"
            
        try:
            post = self.post_repo.get_post_by_slug(post_slug)
            if not post:
                return False, f"Post com slug '{post_slug}' não encontrado"
                
            deleted, _ = Favorite.objects.filter(
                user=user,
                post=post
            ).delete()
            
            if deleted > 0:
                # Invalida o cache de favoritos do usuário
                self._invalidate_user_cache(user.id)
                return True, "Post removido dos favoritos com sucesso"
            else:
                return False, "Este post não estava nos seus favoritos"
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao remover favorito: {str(e)}")
            return False, f"Erro ao remover favorito: {str(e)}"
    
    def is_favorite(self, user: User, post_slug: str, use_cache: bool = True) -> bool:
        """
        Verifica se um post está nos favoritos do usuário com suporte a cache.
        
        Args:
            user: Instância do usuário
            post_slug: Slug do post a ser verificado
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            True se o post está nos favoritos, False caso contrário
            
        Example:
            >>> if service.is_favorite(user, 'meu-post'):
            ...     print("Este post está nos seus favoritos!")
        """
        if not user.is_authenticated:
            return False
            
        cache_key = f'user_{user.id}_is_favorite_{post_slug}'
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
                
        try:
            post = self.post_repo.get_post_by_slug(post_slug)
            if not post:
                return False
                
            result = Favorite.objects.filter(
                user=user,
                post=post
            ).exists()
            
            if use_cache:
                self.cache.set(cache_key, result, CACHE_TIMEOUT)
                
            return result
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao verificar favorito: {str(e)}")
            return False
    
    def get_favorite_count(self, post_slug: str, use_cache: bool = True) -> int:
        """
        Retorna o número de vezes que um post foi favoritado, com suporte a cache.
        
        Args:
            post_slug: Slug do post
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            Número de favoritos do post
            
        Example:
            >>> count = service.get_favorite_count('meu-post')
            >>> print(f"Este post tem {count} favoritos")
        """
        cache_key = f'post_{post_slug}_favorite_count'
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
                
        try:
            post = self.post_repo.get_post_by_slug(post_slug)
            if not post:
                return 0
                
            count = Favorite.objects.filter(post=post).count()
            
            if use_cache:
                # Cache por 5 minutos para contagem de favoritos
                self.cache.set(cache_key, count, 300)
                
            return count
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao contar favoritos do post {post_slug}: {str(e)}")
            return 0
    
    def get_most_favorited_posts(
        self, 
        limit: int = 10,
        days: Optional[int] = None,
        category_slug: Optional[str] = None,
        min_favorites: int = 1,
        use_cache: bool = True
    ) -> List[Dict[str, any]]:
        """
        Retorna os posts mais favoritados com opções avançadas de filtro.
        
        Args:
            limit: Número máximo de posts a retornar (padrão: 10)
            days: Número de dias para trás a partir de hoje (opcional)
            category_slug: Slug da categoria para filtrar (opcional)
            min_favorites: Número mínimo de favoritos para incluir (padrão: 1)
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            Lista de dicionários com informações detalhadas dos posts mais favoritados
            
        Example:
            # Posts mais favoritados (todos os tempos)
            >>> popular = service.get_most_favorited_posts(limit=5)
            
            # Posts mais favoritados nos últimos 30 dias
            >>> recent_popular = service.get_most_favorited_posts(days=30)
            
            # Posts mais favoritos em uma categoria específica
            >>> tech_popular = service.get_most_favorited_posts(
            ...     category_slug='tecnologia',
            ...     min_favorites=5
            ... )
        """
        cache_key = f'most_favorited_{limit}_{days}_{category_slug}_{min_favorites}'
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
                
        try:
            from django.db.models import Count, Q, F
            from django.utils import timezone
            
            # Construção da consulta base
            queryset = BlogPost.objects.filter(
                status='published',
                favorites__isnull=False
            ).annotate(
                favorite_count=Count('favorites')
            ).filter(
                favorite_count__gte=min_favorites
            ).order_by('-favorite_count', '-published_at')
            
            # Filtro por período
            if days is not None:
                start_date = timezone.now() - timezone.timedelta(days=days)
                queryset = queryset.filter(
                    favorites__created_at__gte=start_date
                )
            
            # Filtro por categoria
            if category_slug:
                queryset = queryset.filter(
                    categories__slug=category_slug
                )
            
            # Executa a consulta e formata os resultados
            popular_posts = queryset.distinct()[:limit]
            
            result = [
                {
                    'id': post.id,
                    'slug': post.slug,
                    'title': post.title,
                    'excerpt': post.excerpt,
                    'content': post.content,
                    'published_at': post.published_at,
                    'updated_at': post.updated_at,
                    'favorite_count': post.favorite_count,
                    'comment_count': post.comments.filter(is_approved=True).count(),
                    'view_count': getattr(post, 'view_count', 0),
                    'url': post.get_absolute_url(),
                    'author': {
                        'id': post.author.id if post.author else None,
                        'username': post.author.username if post.author else 'Anônimo',
                        'full_name': post.author.get_full_name() if post.author else 'Anônimo',
                        'avatar': post.author.profile.avatar.url if hasattr(post.author, 'profile') and post.author.profile.avatar else None
                    } if post.author else None,
                    'categories': [
                        {
                            'id': cat.id,
                            'name': cat.name,
                            'slug': cat.slug,
                            'description': cat.description
                        } for cat in post.categories.all()
                    ],
                    'tags': [
                        {
                            'id': tag.id,
                            'name': tag.name,
                            'slug': tag.slug
                        } for tag in post.tags.all()
                    ],
                    'featured_image': post.featured_image.url if post.featured_image else None,
                    'reading_time': getattr(post, 'reading_time', None),
                    'metadata': {
                        'created_at': post.created_at,
                        'updated_at': post.updated_at,
                        'status': post.status,
                        'comment_status': post.comment_status,
                        'ping_status': post.ping_status
                    }
                }
                for post in popular_posts
            ]
            
            # Armazena em cache por 1 hora
            if use_cache:
                self.cache.set(cache_key, result, 3600)
                
            return result
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao buscar posts mais favoritados: {str(e)}")
            return []
    
    def get_user_favorite_categories(
        self, 
        user: User,
        limit: int = 5,
        min_posts: int = 1,
        use_cache: bool = True
    ) -> List[Dict[str, any]]:
        """
        Retorna as categorias mais favoritadas por um usuário, com suporte a cache.
        
        Este método analisa os posts favoritados pelo usuário e retorna as categorias
        mais comuns, ordenadas pelo número de posts favoritados em cada categoria.
        
        Args:
            user: Instância do usuário
            limit: Número máximo de categorias a retornar (padrão: 5)
            min_posts: Número mínimo de posts que a categoria deve ter para ser incluída (padrão: 1)
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            Lista de dicionários com informações detalhadas das categorias favoritas,
            ordenadas pelo número de posts favoritados em cada categoria.
            
        Example:
            # Obter as 3 categorias mais favoritadas
            >>> categories = service.get_user_favorite_categories(user, limit=3)
            
            # Obter categorias com pelo menos 5 posts favoritados
            >>> popular_cats = service.get_user_favorite_categories(
            ...     user,
            ...     min_posts=5
            ... )
            
            # Desativar cache para obter dados atualizados
            >>> fresh_data = service.get_user_favorite_categories(
            ...     user,
            ...     use_cache=False
            ... )
        """
        if not user.is_authenticated:
            return []
            
        cache_key = f'user_{user.id}_fav_cats_{limit}_{min_posts}'
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
                
        try:
            from django.db.models import Count, F, Value
            from django.db.models.functions import Coalesce
            
            # Consulta para obter as categorias mais favoritadas
            categories = BlogPost.objects.filter(
                favorites__user=user,
                status='published',
                categories__isnull=False
            ).values(
                'categories__id',
                'categories__name',
                'categories__slug',
                'categories__description',
                'categories__image',
                'categories__created_at',
                'categories__updated_at'
            ).annotate(
                post_count=Count('id', distinct=True),
                total_favorites=Count('favorites', distinct=True)
            ).filter(
                post_count__gte=min_posts
            ).order_by(
                '-post_count',
                '-total_favorites',
                'categories__name'
            )
            
            # Formata os resultados
            result = []
            for cat in categories[:limit]:
                result.append({
                    'id': cat['categories__id'],
                    'name': cat['categories__name'],
                    'slug': cat['categories__slug'],
                    'description': cat['categories__description'],
                    'image': cat['categories__image'],
                    'post_count': cat['post_count'],
                    'total_favorites': cat['total_favorites'],
                    'metadata': {
                        'created_at': cat['categories__created_at'],
                        'updated_at': cat['categories__updated_at']
                    },
                    'url': f"/categoria/{cat['categories__slug']}/"
                })
            
            # Armazena em cache por 6 horas
            if use_cache:
                self.cache.set(cache_key, result, 21600)  # 6 horas em segundos
                
            return result
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Erro ao buscar categorias favoritas do usuário {user.id}: {str(e)}"
            )
            return []
    
    def get_similar_users(
        self, 
        user: User,
        limit: int = 5,
        min_common: int = 2,
        use_cache: bool = True
    ) -> List[Dict[str, any]]:
        """
        Encontra usuários com interesses semelhantes com base nos favoritos em comum.
        
        Este método identifica usuários que têm padrões de favoritos semelhantes,
        o que pode ser útil para recomendações personalizadas.
        
        Args:
            user: Instância do usuário para o qual buscar similares
            limit: Número máximo de usuários similares a retornar (padrão: 5)
            min_common: Número mínimo de favoritos em comum para considerar (padrão: 2)
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            Lista de dicionários com informações sobre usuários similares,
            ordenados por similaridade (maior número de favoritos em comum primeiro)
            
        Example:
            # Encontrar usuários com interesses semelhantes
            >>> similar_users = service.get_similar_users(user)
            
            # Buscar apenas usuários com pelo menos 3 favoritos em comum
            >>> close_matches = service.get_similar_users(
            ...     user,
            ...     min_common=3
            ... )
        """
        if not user.is_authenticated:
            return []
            
        cache_key = f'user_{user.id}_similar_users_{limit}_{min_common}'
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
                
        try:
            from django.db.models import Count, F, Q
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            
            # Obtém os IDs dos posts favoritos do usuário
            user_favorites = set(Favorite.objects.filter(
                user=user
            ).values_list('post_id', flat=True))
            
            if not user_favorites or len(user_favorites) < min_common:
                return []
            
            # Encontra outros usuários que também favoritaram esses posts
            similar_users = Favorite.objects.filter(
                post_id__in=user_favorites
            ).exclude(
                user=user
            ).values(
                'user__id',
                'user__username',
                'user__first_name',
                'user__last_name',
                'user__email',
                'user__date_joined',
                'user__last_login'
            ).annotate(
                common_favorites=Count('post_id', distinct=True),
                total_favorites=Count('user__favorites', distinct=True)
            ).filter(
                common_favorites__gte=min_common
            ).order_by(
                '-common_favorites',
                '-total_favorites'
            )[:limit]
            
            # Formata os resultados
            result = []
            for similar in similar_users:
                match_percent = int((similar['common_favorites'] / len(user_favorites)) * 100)
                
                result.append({
                    'id': similar['user__id'],
                    'username': similar['user__username'],
                    'first_name': similar['user__first_name'],
                    'last_name': similar['user__last_name'],
                    'email': similar['user__email'],
                    'stats': {
                        'common_favorites': similar['common_favorites'],
                        'total_favorites': similar['total_favorites'],
                        'match_percentage': match_percent,
                        'user_total_favorites': len(user_favorites)
                    },
                    'metadata': {
                        'date_joined': similar['user__date_joined'],
                        'last_login': similar['user__last_login']
                    },
                    'profile_url': f"/usuario/{similar['user__username']}/"
                })
            
            # Armazena em cache por 1 dia
            if use_cache:
                self.cache.set(cache_key, result, 86400)  # 24 horas em segundos
                
            return result
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Erro ao buscar usuários similares para o usuário {user.id}: {str(e)}"
            )
            return []
            
    def get_favorite_stats(
        self,
        days: int = 30,
        use_cache: bool = True
    ) -> Dict[str, any]:
        """
        Retorna estatísticas detalhadas sobre os favoritos do sistema.
        
        Este método fornece uma visão abrangente das métricas de favoritos,
        incluindo totais, médias e tendências ao longo do tempo.
        
        Args:
            days: Número de dias para análise de tendência (padrão: 30)
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            Dicionário com estatísticas detalhadas sobre os favoritos
            
        Example:
            # Obter estatísticas padrão (últimos 30 dias)
            >>> stats = service.get_favorite_stats()
            
            # Obter estatísticas para os últimos 90 dias
            >>> long_term_stats = service.get_favorite_stats(days=90)
            
            # Forçar atualização dos dados ignorando o cache
            >>> fresh_stats = service.get_favorite_stats(use_cache=False)
        """
        cache_key = f'favorite_stats_{days}'
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
                
        try:
            from django.db.models import Count, Avg, Max, Min
            from datetime import datetime, timedelta, date
            
            now = datetime.now()
            period_start = now - timedelta(days=days)
            
            # Estatísticas gerais
            total_favorites = Favorite.objects.count()
            
            # Estatísticas por usuário
            user_stats = Favorite.objects.values('user').annotate(
                count=Count('id')
            ).aggregate(
                avg=Avg('count'),
                max=Max('count'),
                min=Min('count'),
                total_users=Count('user', distinct=True)
            )
            
            # Estatísticas por post
            post_stats = Favorite.objects.values('post').annotate(
                count=Count('id')
            ).aggregate(
                avg=Avg('count'),
                max=Max('count'),
                min=Min('count'),
                total_posts=Count('post', distinct=True)
            )
            
            # Análise de tendência diária
            daily_stats = []
            date_cursor = period_start.date()
            
            # Inicializa o dicionário com todas as datas do período
            while date_cursor <= date.today():
                daily_stats.append({
                    'date': date_cursor.isoformat(),
                    'count': 0,
                    'new_users': 0,
                    'new_posts': 0
                })
                date_cursor += timedelta(days=1)
            
            # Obtém os dados diários reais
            daily_data = Favorite.objects.filter(
                created_at__gte=period_start
            ).extra({
                'date': "date(created_at)"
            }).values('date').annotate(
                count=Count('id'),
                new_users=Count('user', distinct=True),
                new_posts=Count('post', distinct=True)
            ).order_by('date')
            
            # Preenche os dados diários
            for day in daily_data:
                date_str = day['date'].strftime('%Y-%m-%d')
                for stat in daily_stats:
                    if stat['date'] == date_str:
                        stat.update({
                            'count': day['count'],
                            'new_users': day['new_users'],
                            'new_posts': day['new_posts']
                        })
                        break
            
            # Cálculo de crescimento
            if len(daily_stats) > 1:
                first_day = daily_stats[0]['count'] or 1
                last_day = daily_stats[-1]['count']
                growth_percentage = ((last_day - first_day) / first_day * 100) if first_day > 0 else 0
            else:
                growth_percentage = 0
            
            # Médias diárias
            avg_daily_favorites = round(sum(d['count'] for d in daily_stats) / len(daily_stats), 2) if daily_stats else 0
            
            # Prepara o resultado completo
            result = {
                'totals': {
                    'favorites': total_favorites,
                    'users': user_stats.get('total_users', 0),
                    'posts': post_stats.get('total_posts', 0),
                    'days': days,
                    'daily_avg': avg_daily_favorites
                },
                'averages': {
                    'favorites_per_user': round(user_stats.get('avg', 0), 2),
                    'favorites_per_post': round(post_stats.get('avg', 0), 2),
                    'daily_favorites': avg_daily_favorites,
                    'daily_new_users': round(sum(d['new_users'] for d in daily_stats) / len(daily_stats), 2) if daily_stats else 0,
                    'daily_new_posts': round(sum(d['new_posts'] for d in daily_stats) / len(daily_stats), 2) if daily_stats else 0
                },
                'ranges': {
                    'user_favorites': {
                        'min': user_stats.get('min', 0),
                        'max': user_stats.get('max', 0),
                        'avg': round(user_stats.get('avg', 0), 2)
                    },
                    'post_favorites': {
                        'min': post_stats.get('min', 0),
                        'max': post_stats.get('max', 0),
                        'avg': round(post_stats.get('avg', 0), 2)
                    },
                    'daily_favorites': {
                        'min': min(d['count'] for d in daily_stats) if daily_stats else 0,
                        'max': max(d['count'] for d in daily_stats) if daily_stats else 0,
                        'avg': avg_daily_favorites
                    }
                },
                'trends': {
                    'growth_percentage': round(growth_percentage, 2),
                    'is_growing': growth_percentage > 0,
                    'daily_data': daily_stats,
                    'period': f'Últimos {days} dias'
                },
                'metadata': {
                    'generated_at': now.isoformat(),
                    'cache_key': cache_key,
                    'days_analyzed': days,
                    'period_start': period_start.date().isoformat(),
                    'period_end': date.today().isoformat()
                }
            }
            
            # Armazena em cache por 1 hora
            if use_cache:
                self.cache.set(cache_key, result, 3600)  # 1 hora em segundos
                
            return result
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Erro ao gerar estatísticas de favoritos: {str(e)}",
                exc_info=True
            )
            
            # Retorna um objeto vazio em caso de erro
            return {
                'error': 'Não foi possível recuperar as estatísticas no momento',
                'details': str(e),
                'totals': {'favorites': 0, 'users': 0, 'posts': 0, 'days': days},
                'averages': {'favorites_per_user': 0, 'favorites_per_post': 0},
                'ranges': {
                    'user_favorites': {'min': 0, 'max': 0, 'avg': 0},
                    'post_favorites': {'min': 0, 'max': 0, 'avg': 0}
                },
                'metadata': {
                    'error': True,
                    'generated_at': datetime.now().isoformat()
                }
            }
