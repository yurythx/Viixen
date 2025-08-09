from .domain.post import BlogPost, Category, Tag

# Exportar para que o Django encontre os modelos
__all__ = ['BlogPost', 'Category', 'Tag']
