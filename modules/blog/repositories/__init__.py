"""
Módulo de repositórios para o aplicativo de blog.
Fornece interfaces e implementações para acesso a dados.
"""

from .base import BaseRepository
from .django_repository import DjangoRepository
from .category_repository import CategoryRepository
from .post_repository import PostRepository
from .tag_repository import TagRepository

__all__ = [
    'BaseRepository',
    'DjangoRepository',
    'CategoryRepository',
    'PostRepository',
    'TagRepository',
]
