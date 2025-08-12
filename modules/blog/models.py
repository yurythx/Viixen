from .domain.post import BlogPost, Category, Tag, Comment, Favorite

# Exportar para que o Django encontre os modelos
__all__ = ['BlogPost', 'Category', 'Tag', 'Comment', 'Favorite']
