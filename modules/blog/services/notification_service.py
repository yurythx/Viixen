"""
Serviço para gerenciar notificações do sistema.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

# Atualizando o caminho de importação para usar o módulo correto
from ..domain import Notification, NotificationType
from ..domain.post import Comment
from ..repositories import PostRepository

User = get_user_model()


class NotificationService:
    """
    Serviço para gerenciar notificações do sistema.
    """
    
    def __init__(self, post_repo=None):
        self.post_repo = post_repo or PostRepository()
    
    def create_notification(
        self,
        recipient: User,
        notification_type: NotificationType,
        message: str,
        target_url: str = None,
        sender: User = None,
        related_comment: Comment = None,
        related_post = None,
        **extra_data
    ) -> Notification:
        """
        Cria uma nova notificação para um usuário.
        
        Args:
            recipient: Usuário que receberá a notificação
            notification_type: Tipo da notificação
            message: Mensagem da notificação
            target_url: URL de destino ao clicar na notificação
            sender: Usuário que disparou a notificação (opcional)
            related_comment: Comentário relacionado (opcional)
            related_post: Post relacionado (opcional)
            **extra_data: Dados adicionais para a notificação
            
        Returns:
            A notificação criada
        """
        # Verifica se já existe uma notificação semelhante recente
        if self._is_duplicate_notification(
            recipient=recipient,
            notification_type=notification_type,
            related_comment=related_comment,
            related_post=related_post,
            sender=sender
        ):
            return None
            
        # Cria a notificação
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            message=message,
            target_url=target_url,
            sender=sender,
            related_comment=related_comment,
            related_post=related_post,
            extra_data=extra_data or {}
        )
        
        # Envia notificação por e-mail, se configurado
        if recipient.email_notifications_enabled:
            self._send_email_notification(notification)
            
        return notification
    
    def _is_duplicate_notification(
        self,
        recipient: User,
        notification_type: NotificationType,
        related_comment: Comment = None,
        related_post = None,
        sender: User = None
    ) -> bool:
        """
        Verifica se já existe uma notificação semelhante recente.
        
        Args:
            recipient: Usuário que receberá a notificação
            notification_type: Tipo da notificação
            related_comment: Comentário relacionado (opcional)
            related_post: Post relacionado (opcional)
            sender: Usuário que disparou a notificação (opcional)
            
        Returns:
            True se for uma notificação duplicada, False caso contrário
        """
        # Define o período de tempo para considerar notificações como duplicadas
        time_threshold = timezone.now() - timedelta(minutes=5)
        
        # Filtra notificações semelhantes recentes
        filters = {
            'recipient': recipient,
            'notification_type': notification_type,
            'created_at__gte': time_threshold,
            'is_read': False
        }
        
        if related_comment:
            filters['related_comment'] = related_comment
        elif related_post:
            filters['related_post'] = related_post
            
        if sender:
            filters['sender'] = sender
            
        return Notification.objects.filter(**filters).exists()
    
    def _send_email_notification(self, notification: Notification) -> int:
        """
        Envia uma notificação por e-mail.
        
        Args:
            notification: Instância da notificação
            
        Returns:
            Número de e-mails enviados
        """
        subject = f"{settings.SITE_NAME}: {notification.get_notification_type_display()}"
        
        # Renderiza o template de e-mail
        context = {
            'notification': notification,
            'site_name': settings.SITE_NAME,
            'site_domain': settings.SITE_DOMAIN,
        }
        
        message = render_to_string(
            'emails/notification.html',
            context
        )
        
        # Envia o e-mail
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient.email],
            html_message=message,
            fail_silently=True
        )
    
    def get_user_notifications(
        self,
        user: User,
        is_read: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Notification]:
        """
        Retorna as notificações de um usuário.
        
        Args:
            user: Usuário
            is_read: Filtro por notificações lidas/não lidas (opcional)
            limit: Número máximo de notificações a retornar
            offset: Número de notificações a pular
            
        Returns:
            Lista de notificações
        """
        queryset = Notification.objects.filter(recipient=user)
        
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)
            
        return list(queryset.order_by('-created_at')[offset:offset + limit])
    
    def mark_as_read(
        self, 
        notification_id: int = None, 
        user: User = None
    ) -> int:
        """
        Marca uma notificação específica ou todas as notificações de um usuário como lidas.
        
        Args:
            notification_id: ID da notificação a ser marcada como lida (opcional)
            user: Usuário (obrigatório se notification_id não for fornecido)
            
        Returns:
            Número de notificações atualizadas
        """
        if notification_id:
            # Marca uma notificação específica como lida
            updated = Notification.objects.filter(
                id=notification_id
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
        elif user:
            # Marca todas as notificações não lidas do usuário como lidas
            updated = Notification.objects.filter(
                recipient=user,
                is_read=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
        else:
            return 0
            
        return updated
    
    def get_unread_count(self, user: User) -> int:
        """
        Retorna o número de notificações não lidas de um usuário.
        
        Args:
            user: Usuário
            
        Returns:
            Número de notificações não lidas
        """
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).count()
    
    def notify_new_comment(
        self,
        comment: Comment,
        mentioned_users: List[User] = None
    ) -> List[Notification]:
        """
        Notifica sobre um novo comentário.
        
        Args:
            comment: Comentário criado
            mentioned_users: Lista de usuários mencionados (opcional)
            
        Returns:
            Lista de notificações criadas
        """
        notifications = []
        post = comment.post
        
        # Notifica o autor do post (se diferente do autor do comentário)
        if post.author and post.author != comment.author:
            notification = self.create_notification(
                recipient=post.author,
                notification_type=NotificationType.NEW_COMMENT,
                message=f"{comment.author_name} comentou no seu post: {post.title}",
                target_url=post.get_absolute_url(),
                sender=comment.author,
                related_comment=comment,
                related_post=post
            )
            if notification:
                notifications.append(notification)
        
        # Notifica usuários mencionados
        if mentioned_users:
            for user in mentioned_users:
                # Verifica se o usuário não é o autor do comentário
                if user != comment.author:
                    notification = self.create_notification(
                        recipient=user,
                        notification_type=NotificationType.MENTION,
                        message=f"{comment.author_name} mencionou você em um comentário",
                        target_url=comment.get_absolute_url(),
                        sender=comment.author,
                        related_comment=comment,
                        related_post=post
                    )
                    if notification:
                        notifications.append(notification)
        
        # Notifica outros usuários que comentaram no post
        if post.comments.exists():
            # Obtém usuários únicos que comentaram no post
            commenters = User.objects.filter(
                comments__post=post
            ).exclude(
                id__in=[u.id for u in [comment.author, post.author] + (mentioned_users or [])]
            ).distinct()
            
            for user in commenters:
                notification = self.create_notification(
                    recipient=user,
                    notification_type=NotificationType.COMMENT_REPLY,
                    message=f"{comment.author_name} também comentou em: {post.title}",
                    target_url=comment.get_absolute_url(),
                    sender=comment.author,
                    related_comment=comment,
                    related_post=post
                )
                if notification:
                    notifications.append(notification)
        
        return notifications
    
    def notify_comment_reply(
        self,
        comment: Comment,
        parent_comment: Comment,
        mentioned_users: List[User] = None
    ) -> List[Notification]:
        """
        Notifica sobre uma resposta a um comentário.
        
        Args:
            comment: Resposta ao comentário
            parent_comment: Comentário original respondido
            mentioned_users: Lista de usuários mencionados (opcional)
            
        Returns:
            Lista de notificações criadas
        """
        notifications = []
        post = comment.post
        
        # Notifica o autor do comentário original (se diferente do autor da resposta)
        if parent_comment.author and parent_comment.author != comment.author:
            notification = self.create_notification(
                recipient=parent_comment.author,
                notification_type=NotificationType.COMMENT_REPLY,
                message=f"{comment.author_name} respondeu ao seu comentário em: {post.title}",
                target_url=comment.get_absolute_url(),
                sender=comment.author,
                related_comment=comment,
                related_post=post
            )
            if notification:
                notifications.append(notification)
        
        # Notifica usuários mencionados
        if mentioned_users:
            for user in mentioned_users:
                # Verifica se o usuário não é o autor do comentário
                if user != comment.author:
                    notification = self.create_notification(
                        recipient=user,
                        notification_type=NotificationType.MENTION,
                        message=f"{comment.author_name} mencionou você em uma resposta",
                        target_url=comment.get_absolute_url(),
                        sender=comment.author,
                        related_comment=comment,
                        related_post=post
                    )
                    if notification:
                        notifications.append(notification)
        
        return notifications
