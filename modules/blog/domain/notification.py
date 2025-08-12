from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from enum import Enum
from typing import Optional

User = get_user_model()

class NotificationType(Enum):
    """Tipos de notificações disponíveis no sistema."""
    NEW_COMMENT = 'new_comment'
    COMMENT_REPLY = 'comment_reply'
    COMMENT_APPROVED = 'comment_approved'
    POST_PUBLISHED = 'post_published'
    MENTION = 'mention'
    SYSTEM = 'system'


class Notification(models.Model):
    """
    Modelo para notificações do sistema.
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Destinatário'
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.name.replace('_', ' ').title()) for tag in NotificationType],
        verbose_name='Tipo de Notificação'
    )
    
    title = models.CharField(max_length=255, verbose_name='Título')
    message = models.TextField(verbose_name='Mensagem')
    
    # Referência ao objeto relacionado (opcional)
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    
    is_read = models.BooleanField(default=False, verbose_name='Lida')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Marca a notificação como lida."""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    @classmethod
    def create_notification(
        cls,
        recipient: User,
        notification_type: NotificationType,
        title: str,
        message: str,
        content_object: Optional[models.Model] = None
    ) -> 'Notification':
        """
        Método auxiliar para criar uma nova notificação.
        """
        notification = cls(
            recipient=recipient,
            notification_type=notification_type.value,
            title=title,
            message=message,
            is_read=False
        )
        
        if content_object:
            notification.content_type = type(content_object).objects.get_for_model(content_object)
            notification.object_id = content_object.pk
        
        notification.save()
        return notification
