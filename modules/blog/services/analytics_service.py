"""
Serviço para gerenciar análises e métricas do blog.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from django.db.models import Count, F, Q
from django.utils import timezone

from ..domain.post import BlogPost, Category, Tag
from ..repositories import PostRepository, CategoryRepository, TagRepository


class AnalyticsService:
    """
    Serviço para gerenciar análises e métricas do blog.
    """
    
    def __init__(self):
        self.post_repo = PostRepository()
        self.category_repo = CategoryRepository()
        self.tag_repo = TagRepository()
    
    def get_popular_posts(
        self, 
        days: int = 30, 
        limit: int = 5
    ) -> List[Dict]:
        """
        Retorna os posts mais populares em um período.
        
        Args:
            days: Número de dias para trás a partir de hoje
            limit: Número máximo de posts a retornar
            
        Returns:
            Lista de dicionários com informações dos posts populares
        """
        start_date = timezone.now() - timedelta(days=days)
        
        posts = self.post_repo.list_all(
            status='published',
            published_at__gte=start_date
        ).order_by('-views_count')[:limit]
        
        return [
            {
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'views': post.views_count,
                'published_at': post.published_at,
                'author': post.author.get_full_name() if post.author else 'Desconhecido',
                'url': post.get_absolute_url()
            }
            for post in posts
        ]
    
    def get_category_stats(self) -> List[Dict]:
        """
        Retorna estatísticas de visualização por categoria.
        
        Returns:
            Lista de dicionários com estatísticas por categoria
        """
        categories = self.category_repo.list_all(is_active=True)
        
        return [
            {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'post_count': self.post_repo.list_all(
                    category=category,
                    status='published'
                ).count(),
                'total_views': sum(
                    post.views_count 
                    for post in self.post_repo.list_all(
                        category=category,
                        status='published'
                    )
                )
            }
            for category in categories
        ]
    
    def get_tag_stats(self) -> List[Dict]:
        """
        Retorna estatísticas de visualização por tag.
        
        Returns:
            Lista de dicionários com estatísticas por tag
        """
        tags = self.tag_repo.get_active_tags()
        
        return [
            {
                'id': tag.id,
                'name': tag.name,
                'slug': tag.slug,
                'post_count': self.post_repo.list_all(
                    tags=tag,
                    status='published'
                ).count(),
                'total_views': sum(
                    post.views_count 
                    for post in self.post_repo.list_all(
                        tags=tag,
                        status='published'
                    )
                )
            }
            for tag in tags
        ]
    
    def get_views_over_time(
        self, 
        days: int = 30
    ) -> Dict[str, List[Dict]]:
        """
        Retorna o número de visualizações ao longo do tempo.
        
        Args:
            days: Número de dias para trás a partir de hoje
            
        Returns:
            Dicionário com dados de visualizações por período
        """
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Agrupa por dia
        daily_views = self.post_repo.list_all(
            status='published',
            published_at__range=(start_date, end_date)
        ).values('published_at__date').annotate(
            views=Count('views_count')
        ).order_by('published_at__date')
        
        # Preenche os dias sem visualizações com zero
        date_dict = {}
        current_date = start_date.date()
        
        while current_date <= end_date.date():
            date_dict[str(current_date)] = {'date': current_date, 'views': 0}
            current_date += timedelta(days=1)
        
        # Atualiza com os dados reais
        for item in daily_views:
            date_str = str(item['published_at__date'])
            if date_str in date_dict:
                date_dict[date_str]['views'] = item['views']
        
        # Converte para o formato de saída
        result = {
            'labels': [],
            'datasets': [{
                'label': 'Visualizações',
                'data': [],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        }
        
        for date, data in sorted(date_dict.items()):
            result['labels'].append(data['date'].strftime('%d/%m/%Y'))
            result['datasets'][0]['data'].append(data['views'])
        
        return result
    
    def get_author_stats(self) -> List[Dict]:
        """
        Retorna estatísticas de posts por autor.
        
        Returns:
            Lista de dicionários com estatísticas por autor
        """
        posts = self.post_repo.list_all(status='published')
        
        author_stats = {}
        
        for post in posts:
            if not post.author:
                continue
                
            author_id = post.author.id
            author_name = post.author.get_full_name() or post.author.username
            
            if author_id not in author_stats:
                author_stats[author_id] = {
                    'id': author_id,
                    'name': author_name,
                    'post_count': 0,
                    'total_views': 0,
                    'average_views': 0
                }
            
            author_stats[author_id]['post_count'] += 1
            author_stats[author_id]['total_views'] += post.views_count
        
        # Calcula a média de visualizações
        for author in author_stats.values():
            if author['post_count'] > 0:
                author['average_views'] = author['total_views'] / author['post_count']
        
        return sorted(
            list(author_stats.values()),
            key=lambda x: x['total_views'],
            reverse=True
        )
    
    def get_reading_time_stats(self) -> Dict[str, float]:
        """
        Retorna estatísticas sobre o tempo de leitura dos posts.
        
        Returns:
            Dicionário com estatísticas de tempo de leitura
        """
        posts = self.post_repo.list_all(status='published')
        
        if not posts:
            return {
                'average_reading_time': 0,
                'min_reading_time': 0,
                'max_reading_time': 0,
                'total_posts': 0
            }
        
        reading_times = [post.reading_time for post in posts if post.reading_time]
        
        if not reading_times:
            return {
                'average_reading_time': 0,
                'min_reading_time': 0,
                'max_reading_time': 0,
                'total_posts': len(posts)
            }
        
        return {
            'average_reading_time': sum(reading_times) / len(reading_times),
            'min_reading_time': min(reading_times),
            'max_reading_time': max(reading_times),
            'total_posts': len(posts)
        }
