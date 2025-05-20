# apps/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

def avatar_upload_path(instance, filename):
    return f'avatars/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    
    is_active = models.BooleanField(default=False)  # necessário para ativação por e-mail

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/img/default_avatar.png'

    def __str__(self):
        return self.username