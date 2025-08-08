from django.utils import timezone
from django.db.models import Q, F
from ..domain.post import BlogPost, Category
from ..repositories.post_repo import PostRepository

class PostService:
    def __init__(self):
        self.repository = PostRepository()
    
    def get_published_posts(self, company=None):
        """Retorna posts publicados"""
        queryset = self.repository.get_published()
        if company:
            queryset = queryset.filter(company=company)
        return queryset
    
    def get_featured_posts(self, company=None, limit=5):
        """Retorna posts em destaque"""
        queryset = self.get_published_posts(company)
        return queryset.filter(is_featured=True)[:limit]
    
    def get_recent_posts(self, company=None, limit=5):
        """Retorna posts recentes"""
        queryset = self.get_published_posts(company)
        return queryset.order_by('-created_at')[:limit]
    
    def search_posts(self, query, company=None):
        """Busca posts por título ou conteúdo"""
        queryset = self.get_published_posts(company)
        return queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    def publish_post(self, post_id):
        """Publica um post"""
        post = self.repository.get_by_id(post_id)
        post.status = 'published'
        post.published_at = timezone.now()
        post.save()
        return post
    
    def increment_post_views(self, post_id):
        """Incrementa visualizações do post"""
        BlogPost.objects.filter(id=post_id).update(
            views_count=F('views_count') + 1
        )
    
    def get_related_posts(self, post, limit=5):
        """Retorna posts relacionados baseados nas categorias"""
        if not post.categories.exists():
            return BlogPost.objects.none()
        
        related_posts = self.get_published_posts(post.company).filter(
            categories__in=post.categories.all()
        ).exclude(id=post.id).distinct()[:limit]
        
        return related_posts
    
    def get_posts_by_category(self, category, company=None):
        """Retorna posts de uma categoria específica"""
        queryset = self.get_published_posts(company)
        return queryset.filter(categories=category)
    
    def get_posts_by_author(self, author, company=None):
        """Retorna posts de um autor específico"""
        queryset = self.get_published_posts(company)
        return queryset.filter(author=author)