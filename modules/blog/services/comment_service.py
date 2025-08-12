"""
Serviço para gerenciar operações relacionadas a comentários do blog.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone

from ..domain.post import Comment, BlogPost
from ..repositories import PostRepository

User = get_user_model()


class CommentService:
    """
    Serviço para gerenciar operações relacionadas a comentários do blog.
    """
    
    def __init__(self, post_repo=None):
        self.post_repo = post_repo or PostRepository()
    
    def get_comments_for_post(
        self, 
        post_slug: str,
        include_pending: bool = False,
        include_spam: bool = False
    ) -> List[Comment]:
        """
        Retorna os comentários de um post.
        
        Args:
            post_slug: Slug do post
            include_pending: Incluir comentários pendentes de moderação
            include_spam: Incluir comentários marcados como spam
            
        Returns:
            Lista de comentários do post
        """
        post = self.post_repo.get_post_by_slug(post_slug)
        if not post:
            return []
            
        comments = post.comments.all()
        
        # Filtra por status
        if not include_pending:
            comments = comments.filter(is_approved=True)
        if not include_spam:
            comments = comments.filter(is_spam=False)
            
        return list(comments.order_by('created_at'))
    
    def get_recent_comments(
        self, 
        limit: int = 10,
        include_pending: bool = False,
        include_spam: bool = False
    ) -> List[Comment]:
        """
        Retorna os comentários mais recentes.
        
        Args:
            limit: Número máximo de comentários a retornar
            include_pending: Incluir comentários pendentes de moderação
            include_spam: Incluir comentários marcados como spam
            
        Returns:
            Lista de comentários recentes
        """
        comments = Comment.objects.all()
        
        # Filtra por status
        if not include_pending:
            comments = comments.filter(is_approved=True)
        if not include_spam:
            comments = comments.filter(is_spam=False)
            
        return list(comments.order_by('-created_at')[:limit])
    
    def create_comment(
        self,
        post_slug: str,
        author_name: str,
        author_email: str,
        content: str,
        author: User = None,
        parent_comment_id: int = None,
        **extra_fields
    ) -> Optional[Comment]:
        """
        Cria um novo comentário.
        
        Args:
            post_slug: Slug do post
            author_name: Nome do autor do comentário
            author_email: Email do autor do comentário
            content: Conteúdo do comentário
            author: Usuário autenticado (opcional)
            parent_comment_id: ID do comentário pai (para respostas)
            **extra_fields: Campos adicionais
            
        Returns:
            O comentário criado ou None em caso de erro
        """
        post = self.post_repo.get_post_by_slug(post_slug)
        if not post or not post.comments_enabled:
            return None
            
        # Verifica se o comentário é uma resposta
        parent_comment = None
        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(
                    id=parent_comment_id,
                    post=post,
                    is_approved=True,
                    is_spam=False
                )
            except Comment.DoesNotExist:
                return None
        
        # Cria o comentário
        comment = Comment(
            post=post,
            author=author,
            author_name=author_name,
            author_email=author_email,
            content=content,
            parent_comment=parent_comment,
            **extra_fields
        )
        
        # Aprovação automática para usuários autenticados ou comentários de respostas
        if author or parent_comment:
            comment.is_approved = True
        else:
            # Verifica se é spam (implementação básica)
            comment.is_spam = self._check_for_spam(content, author_name, author_email)
            comment.is_approved = not comment.is_spam
        
        comment.save()
        return comment
    
    def update_comment(
        self,
        comment_id: int,
        content: str = None,
        is_approved: bool = None,
        is_spam: bool = None,
        **extra_fields
    ) -> Optional[Comment]:
        """
        Atualiza um comentário existente.
        
        Args:
            comment_id: ID do comentário
            content: Novo conteúdo do comentário
            is_approved: Novo status de aprovação
            is_spam: Novo status de spam
            **extra_fields: Campos adicionais
            
        Returns:
            O comentário atualizado ou None se não encontrado
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            
            if content is not None:
                comment.content = content
            if is_approved is not None:
                comment.is_approved = is_approved
            if is_spam is not None:
                comment.is_spam = is_spam
                
            for key, value in extra_fields.items():
                setattr(comment, key, value)
                
            comment.save()
            return comment
            
        except Comment.DoesNotExist:
            return None
    
    def delete_comment(self, comment_id: int) -> bool:
        """
        Remove um comentário.
        
        Args:
            comment_id: ID do comentário
            
        Returns:
            True se o comentário foi removido, False caso contrário
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return True
        except Comment.DoesNotExist:
            return False
    
    def approve_comment(self, comment_id: int) -> bool:
        """
        Aprova um comentário pendente.
        
        Args:
            comment_id: ID do comentário
            
        Returns:
            True se o comentário foi aprovado, False caso contrário
        """
        try:
            comment = Comment.objects.get(id=comment_id, is_approved=False)
            comment.is_approved = True
            comment.is_spam = False
            comment.save()
            return True
        except Comment.DoesNotExist:
            return False
    
    def mark_as_spam(self, comment_id: int) -> bool:
        """
        Marca um comentário como spam.
        
        Args:
            comment_id: ID do comentário
            
        Returns:
            True se o comentário foi marcado como spam, False caso contrário
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.is_spam = True
            comment.is_approved = False
            comment.save()
            return True
        except Comment.DoesNotExist:
            return False
    
    def get_comment_stats(self) -> Dict[str, int]:
        """
        Retorna estatísticas sobre os comentários.
        
        Returns:
            Dicionário com estatísticas de comentários
        """
        total = Comment.objects.count()
        approved = Comment.objects.filter(is_approved=True).count()
        pending = Comment.objects.filter(is_approved=False, is_spam=False).count()
        spam = Comment.objects.filter(is_spam=True).count()
        
        return {
            'total': total,
            'approved': approved,
            'pending': pending,
            'spam': spam,
            'approval_rate': (approved / total * 100) if total > 0 else 0,
            'spam_rate': (spam / total * 100) if total > 0 else 0
        }
    
    def get_comments_by_author(
        self, 
        author_email: str,
        include_pending: bool = False,
        include_spam: bool = False
    ) -> List[Comment]:
        """
        Retorna os comentários de um autor específico.
        
        Args:
            author_email: Email do autor
            include_pending: Incluir comentários pendentes
            include_spam: Incluir comentários marcados como spam
            
        Returns:
            Lista de comentários do autor
        """
        comments = Comment.objects.filter(author_email=author_email)
        
        if not include_pending:
            comments = comments.filter(is_approved=True)
        if not include_spam:
            comments = comments.filter(is_spam=False)
            
        return list(comments.order_by('-created_at'))
    
    def _check_for_spam(
        self, 
        content: str, 
        author_name: str, 
        author_email: str
    ) -> bool:
        """
        Verifica se um comentário é spam.
        
        Args:
            content: Conteúdo do comentário
            author_name: Nome do autor
            author_email: Email do autor
            
        Returns:
            True se for considerado spam, False caso contrário
        """
        # Implementação básica de detecção de spam
        # Pode ser estendida com serviços como Akismet
        
        # Palavras-chave comuns em spam
        spam_keywords = [
            'http://', 'https://', 'www.', '.ru', '.xyz', '.top',
            'buy', 'cheap', 'discount', 'viagra', 'casino', 'loan',
            'money', 'earn', 'work from home', 'make money'
        ]
        
        # Verifica palavras-chave no conteúdo
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in spam_keywords):
            return True
            
        # Verifica emails suspeitos
        if any(domain in author_email.lower() for domain in ['@mail.ru', '@yandex.ru', '@gmail.com']):
            # Verifica se o nome parece ser gerado aleatoriamente
            if len(author_name.split()) < 2 or len(author_name) > 30:
                return True
                
        return False
