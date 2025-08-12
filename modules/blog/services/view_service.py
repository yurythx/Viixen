"""
Serviço para gerenciar visualizações de posts.
"""
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Set, Tuple, List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone

from ..domain.post import BlogPost, View
from ..repositories import PostRepository

User = get_user_model()

# Tempo de vida do cache em segundos (1 hora)
VIEW_CACHE_TIMEOUT = 60 * 60


def get_client_ip(request) -> str:
    """
    Obtém o endereço IP do cliente a partir da requisição.
    
    Args:
        request: Objeto de requisição do Django
        
    Returns:
        Endereço IP do cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_session_key(request) -> str:
    """
    Gera uma chave de sessão única para o usuário.
    
    Args:
        request: Objeto de requisição do Django
        
    Returns:
        Chave de sessão única
    """
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


class ViewService:
    """
    Serviço para gerenciar visualizações de posts.
    """
    
    def __init__(self, post_repo=None):
        self.post_repo = post_repo or PostRepository()
    
    def track_view(
        self, 
        post_slug: str, 
        request,
        user: Optional[User] = None
    ) -> Tuple[bool, Optional[View]]:
        """
        Registra uma visualização de post, garantindo que não haja duplicações.
        
        Args:
            post_slug: Slug do post visualizado
            request: Objeto de requisição do Django
            user: Usuário autenticado (opcional)
            
        Returns:
            Tupla (criado, visualização) onde 'criado' indica se uma nova visualização 
            foi registrada e 'visualização' é o objeto View criado ou None
        """
        post = self.post_repo.get_post_by_slug(post_slug)
        if not post or not post.is_published:
            return False, None
        
        # Gera uma chave única para esta visualização
        ip = get_client_ip(request)
        session_key = get_session_key(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        
        # Cria um hash para identificar unicamente esta visualização
        view_hash = self._generate_view_hash(post.id, ip, session_key, user_agent)
        
        # Verifica no cache se já registramos esta visualização recentemente
        cache_key = f'post_view:{view_hash}'
        if cache.get(cache_key):
            return False, None
        
        # Verifica no banco de dados se já existe uma visualização semelhante recente
        time_threshold = timezone.now() - timedelta(hours=24)
        
        view_exists = View.objects.filter(
            view_hash=view_hash,
            created_at__gte=time_threshold
        ).exists()
        
        if view_exists:
            # Atualiza o cache para evitar consultas repetidas
            cache.set(cache_key, True, VIEW_CACHE_TIMEOUT)
            return False, None
        
        # Cria um novo registro de visualização
        view = View.objects.create(
            post=post,
            user=user if user and user.is_authenticated else None,
            ip_address=ip,
            user_agent=user_agent,
            view_hash=view_hash,
            session_key=session_key
        )
        
        # Atualiza o contador de visualizações do post
        self._increment_post_views(post)
        
        # Armazena no cache para evitar duplicações
        cache.set(cache_key, True, VIEW_CACHE_TIMEOUT)
        
        return True, view
    
    def _generate_view_hash(
        self, 
        post_id: int, 
        ip: str, 
        session_key: str, 
        user_agent: str
    ) -> str:
        """
        Gera um hash único para identificar uma visualização.
        
        Args:
            post_id: ID do post
            ip: Endereço IP do usuário
            session_key: Chave de sessão do usuário
            user_agent: User-Agent do navegador
            
        Returns:
            Hash SHA-256 da visualização
        """
        hash_input = f"{post_id}:{ip}:{session_key}:{user_agent}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
    def _increment_post_views(self, post: BlogPost) -> None:
        """
        Incrementa o contador de visualizações de um post de forma atômica.
        
        Args:
            post: Instância do post a ser atualizada
        """
        # Usa F() para evitar condições de corrida
        BlogPost.objects.filter(id=post.id).update(
            views_count=models.F('views_count') + 1
        )
        
        # Atualiza o objeto em memória
        post.views_count = models.F('views_count') + 1
    
    def get_post_views_count(self, post_slug: str) -> int:
        """
        Retorna o número total de visualizações de um post.
        
        Args:
            post_slug: Slug do post
            
        Returns:
            Número total de visualizações
        """
        post = self.post_repo.get_post_by_slug(post_slug)
        if not post:
            return 0
            
        return post.views_count
    
    def get_post_views_timeline(
        self, 
        post_slug: str,
        days: int = 30
    ) -> Dict[str, int]:
        """
        Retorna um histórico de visualizações do post ao longo do tempo.
        
        Args:
            post_slug: Slug do post
            days: Número de dias para trás a partir de hoje
            
        Returns:
            Dicionário com datas e contagem de visualizações
        """
        post = self.post_repo.get_post_by_slug(post_slug)
        if not post:
            return {}
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Agrupa visualizações por data
        views_by_date = (
            View.objects
            .filter(
                post=post,
                created_at__range=(start_date, end_date)
            )
            .extra({'date': "date(created_at)"})
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        
        # Cria um dicionário com todas as datas no intervalo
        date_dict = {}
        current_date = start_date.date()
        
        while current_date <= end_date.date():
            date_str = current_date.isoformat()
            date_dict[date_str] = 0
            current_date += timedelta(days=1)
        
        # Preenche com os dados reais
        for item in views_by_date:
            date_str = item['date']
            if date_str in date_dict:
                date_dict[date_str] = item['count']
        
        return date_dict
    
    def get_popular_posts(
        self, 
        limit: int = 10,
        days: Optional[int] = None
    ) -> List[Dict]:
        """
        Retorna os posts mais visualizados.
        
        Args:
            limit: Número máximo de posts a retornar
            days: Número de dias para trás a partir de hoje (opcional)
            
        Returns:
            Lista de dicionários com informações dos posts populares
        """
        queryset = BlogPost.objects.filter(status='published')
        
        if days is not None:
            start_date = timezone.now() - timedelta(days=days)
            queryset = queryset.filter(
                views__created_at__gte=start_date
            ).annotate(
                recent_views=Count('views')
            ).order_by('-recent_views', '-published_at')
        else:
            queryset = queryset.order_by('-views_count', '-published_at')
        
        popular_posts = queryset[:limit]
        
        return [
            {
                'post': post,
                'views': post.recent_views if days is not None else post.views_count,
                'url': post.get_absolute_url(),
                'title': post.title,
                'excerpt': post.excerpt,
                'published_at': post.published_at,
                'author': post.author.get_full_name() if post.author else 'Desconhecido',
                'category': post.category.name if post.category else None,
                'category_slug': post.category.slug if post.category else None,
            }
            for post in popular_posts
        ]
    
    def get_user_view_history(
        self, 
        user: User,
        limit: int = 10
    ) -> List[Dict]:
        """
        Retorna o histórico de visualizações de um usuário.
        
        Args:
            user: Usuário autenticado
            limit: Número máximo de itens a retornar
            
        Returns:
            Lista de dicionários com informações das visualizações
        """
        views = (
            View.objects
            .filter(user=user)
            .select_related('post')
            .order_by('-created_at')
            .distinct('post_id')  # Apenas a visualização mais recente de cada post
            [:limit]
        )
        
        return [
            {
                'post': view.post,
                'viewed_at': view.created_at,
                'url': view.post.get_absolute_url(),
                'title': view.post.title,
                'excerpt': view.post.excerpt,
                'author': view.post.author.get_full_name() if view.post.author else 'Desconhecido',
            }
            for view in views
        ]
    
    def get_views_by_country(self, post_slug: str) -> Dict[str, int]:
        """
        Retorna a distribuição de visualizações por país.
        
        Args:
            post_slug: Slug do post
            
        Returns:
            Dicionário com códigos de país e contagem de visualizações
        """
        post = self.post_repo.get_post_by_slug(post_slug)
        if not post:
            return {}
        
        # Esta implementação assume que você tem um campo 'country' no modelo View
        # que é preenchido por um middleware ou serviço de geolocalização
        return (
            View.objects
            .filter(post=post, country__isnull=False)
            .values('country')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
    
    def get_views_by_device(self, post_slug: str) -> Dict[str, int]:
        """
        Retorna a distribuição de visualizações por tipo de dispositivo.
        
        Args:
            post_slug: Slug do post
            
        Returns:
            Dicionário com tipos de dispositivo e contagem de visualizações
        """
        post = self.post_repo.get_post_by_slug(post_slug)
        if not post:
            return {}
        
        # Esta é uma implementação simplificada
        # Em produção, use uma biblioteca como django-user-agents
        from django.db.models import Case, When, Value, IntegerField
        
        return (
            View.objects
            .filter(post=post)
            .annotate(
                device_type=Case(
                    When(user_agent__icontains='mobile', then=Value('mobile')),
                    When(user_agent__icontains='tablet', then=Value('tablet')),
                    When(user_agent__icontains='android', then=Value('mobile')),
                    When(user_agent__icontains='iphone', then=Value('mobile')),
                    When(user_agent__icontains='ipad', then=Value('tablet')),
                    default=Value('desktop'),
                    output_field=Value('str')
                )
            )
            .values('device_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
