from .post import BlogPost, Category, Tag, Comment, Favorite
from .notification import Notification, NotificationType

# Exportar para que outros módulos possam importar facilmente
__all__ = [
    'BlogPost',
    'Category',
    'Tag',
    'Comment',
    'Favorite',
    'Notification',
    'NotificationType',
]
