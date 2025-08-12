"""
Serviço para gerenciar operações relacionadas a tags do blog.
"""
from typing import List, Optional

from ..domain.post import Tag
from ..repositories import TagRepository, PostRepository
from .base import BaseService


class TagService(BaseService[Tag]):
    """
    Serviço para gerenciar operações relacionadas a tags do blog.
    """
    
    def __init__(self, repository=None):
        super().__init__(repository or TagRepository())
        self.post_repo = PostRepository()
    
    def get_active_tags(self) -> List[Tag]:
        """
        Retorna todas as tags ativas.
        
        Returns:
            Lista de tags ativas
        """
        return list(self.repository.get_active_tags())
    
    def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """
        Retorna as tags mais populares (com mais posts).
        
        Args:
            limit: Número máximo de tags a retornar
            
        Returns:
            Lista de tags populares
        """
        return list(self.repository.get_popular_tags(limit))
    
    def get_tag_with_posts(self, slug: str) -> Optional[Tag]:
        """
        Obtém uma tag com seus posts relacionados.
        
        Args:
            slug: Slug da tag
            
        Returns:
            A tag com os posts relacionados ou None se não encontrada
        """
        return self.repository.get_tag_with_posts(slug)
    
    def get_or_create_tags(self, tag_names: List[str]) -> List[Tag]:
        """
        Obtém ou cria tags a partir de uma lista de nomes.
        
        Args:
            tag_names: Lista de nomes de tags
            
        Returns:
            Lista de instâncias de Tag
        """
        if not tag_names:
            return []
            
        return list(self.repository.get_or_create_tags(tag_names))
    
    def create_tag(
        self,
        name: str,
        description: str = '',
        is_active: bool = True,
        **extra_fields
    ) -> Tag:
        """
        Cria uma nova tag.
        
        Args:
            name: Nome da tag
            description: Descrição da tag (opcional)
            is_active: Se a tag está ativa
            **extra_fields: Campos adicionais
            
        Returns:
            A tag criada
        """
        return self.repository.create(
            name=name,
            description=description,
            is_active=is_active,
            **extra_fields
        )
    
    def update_tag(
        self,
        tag: Tag,
        name: str = None,
        description: str = None,
        is_active: bool = None,
        **extra_fields
    ) -> Tag:
        """
        Atualiza uma tag existente.
        
        Args:
            tag: Tag a ser atualizada
            name: Novo nome (opcional)
            description: Nova descrição (opcional)
            is_active: Novo status de ativação (opcional)
            **extra_fields: Campos adicionais
            
        Returns:
            A tag atualizada
        """
        update_fields = {}
        
        if name is not None:
            update_fields['name'] = name
        if description is not None:
            update_fields['description'] = description
        if is_active is not None:
            update_fields['is_active'] = is_active
            
        update_fields.update(extra_fields)
        
        return self.repository.update(tag, **update_fields)
    
    def delete_tag(self, tag: Tag) -> None:
        """
        Remove uma tag.
        
        Args:
            tag: Tag a ser removida
            
        Note:
            A tag só pode ser removida se não estiver associada a nenhum post
        """
        # Verifica se a tag está associada a algum post
        if self.post_repo.list_all(tags=tag).exists():
            raise ValueError("Não é possível excluir uma tag que está associada a posts.")
            
        self.repository.delete(tag)
    
    def merge_tags(self, source_tag: Tag, target_tag: Tag) -> Tag:
        """
        Mescla uma tag de origem em uma tag de destino.
        
        Args:
            source_tag: Tag de origem (será removida após a mesclagem)
            target_tag: Tag de destino (receberá os posts da tag de origem)
            
        Returns:
            A tag de destino atualizada
            
        Note:
            A tag de origem será removida após a mesclagem
        """
        if source_tag.id == target_tag.id:
            raise ValueError("Não é possível mesclar uma tag com ela mesma.")
            
        # Obtém todos os posts associados à tag de origem
        posts_with_source_tag = self.post_repo.list_all(tags=source_tag)
        
        # Adiciona a tag de destino a todos os posts que tinham a tag de origem
        for post in posts_with_source_tag:
            if target_tag not in post.tags.all():
                post.tags.add(target_tag)
            post.tags.remove(source_tag)
        
        # Remove a tag de origem
        self.repository.delete(source_tag)
        
        return target_tag
