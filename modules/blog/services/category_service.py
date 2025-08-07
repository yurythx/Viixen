from ..domain.category import Category
from ..repositories.category_repo import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get_active_categories(self):
        """Retorna categorias ativas"""
        return self.repository.get_active()
    
    def get_categories_with_posts_count(self):
        """Retorna categorias com contagem de posts"""
        from django.db.models import Count
        return self.get_active_categories().annotate(
            posts_count=Count('posts', filter=models.Q(posts__status='published'))
        )
    
    def get_category_by_slug(self, slug):
        """Retorna categoria por slug"""
        return self.repository.get_by_slug(slug)