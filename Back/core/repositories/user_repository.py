"""
Repositório para usuários
Implementa o padrão de repositório para encapsular a lógica de acesso a dados de usuários
"""

from typing import List, Optional, Dict, Any
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from apps.accounts.models import UserSettings
from core.repositories.base_repository import BaseRepository

User = get_user_model()

class UserRepository(BaseRepository):
    """
    Repositório para usuários
    """
    def __init__(self):
        """
        Inicializa o repositório com o modelo User
        """
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtém um usuário pelo email
        """
        try:
            return self.model_class.objects.get(email=email)
        except self.model_class.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Obtém um usuário pelo nome de usuário
        """
        try:
            return self.model_class.objects.get(username=username)
        except self.model_class.DoesNotExist:
            return None

    def get_active_users(self) -> QuerySet:
        """
        Obtém usuários ativos
        """
        return self.model_class.objects.filter(is_active=True)

    def get_staff_users(self) -> QuerySet:
        """
        Obtém usuários da equipe (staff)
        """
        return self.model_class.objects.filter(is_staff=True)

    def create_user(self, username: str, email: str, password: str, **extra_fields) -> User:
        """
        Cria um novo usuário
        """
        return self.model_class.objects.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

    def create_superuser(self, username: str, email: str, password: str, **extra_fields) -> User:
        """
        Cria um novo superusuário
        """
        return self.model_class.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

    def update_last_login(self, user_id: str) -> None:
        """
        Atualiza a data do último login
        """
        from django.utils import timezone
        self.model_class.objects.filter(pk=user_id).update(last_login=timezone.now())

    def change_password(self, user_id: str, new_password: str) -> bool:
        """
        Altera a senha de um usuário
        """
        user = self.get_by_id(user_id)
        if not user:
            return False

        user.set_password(new_password)
        user.save()
        return True


class UserSettingsRepository(BaseRepository):
    """
    Repositório para configurações de usuário
    """
    def __init__(self):
        """
        Inicializa o repositório com o modelo UserSettings
        """
        super().__init__(UserSettings)

    def get_by_user(self, user_id: str) -> Optional[UserSettings]:
        """
        Obtém as configurações de um usuário
        """
        try:
            return self.model_class.objects.get(user_id=user_id)
        except self.model_class.DoesNotExist:
            return None

    def get_or_create_for_user(self, user_id: str) -> UserSettings:
        """
        Obtém ou cria as configurações para um usuário
        """
        settings, created = self.model_class.objects.get_or_create(user_id=user_id)
        return settings

    def update_theme(self, user_id: str, theme: str) -> bool:
        """
        Atualiza o tema de um usuário
        """
        settings = self.get_by_user(user_id)
        if not settings:
            return False

        settings.theme = theme
        settings.save(update_fields=['theme', 'updated_at'])
        return True

    def update_language(self, user_id: str, language: str) -> bool:
        """
        Atualiza o idioma de um usuário
        """
        settings = self.get_by_user(user_id)
        if not settings:
            return False

        settings.language = language
        settings.save(update_fields=['language', 'updated_at'])
        return True

    def update_comment_settings(self, user_id: str, require_approval: bool, allow_anonymous: bool) -> bool:
        """
        Atualiza as configurações de comentários de um usuário
        """
        settings = self.get_by_user(user_id)
        if not settings:
            return False

        settings.require_comment_approval = require_approval
        settings.allow_anonymous_comments = allow_anonymous
        settings.save(update_fields=['require_comment_approval', 'allow_anonymous_comments', 'updated_at'])
        return True


# Instâncias únicas dos repositórios (Singleton)
user_repository = UserRepository()
user_settings_repository = UserSettingsRepository()
