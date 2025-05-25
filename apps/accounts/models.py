from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import FileExtensionValidator

def avatar_upload_path(instance, filename):
    return f'avatar/{instance.username}/{filename}'

class Departamento(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Cargo(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class CustomUser(AbstractUser):
    """
    Modelo de usuário personalizado com campos adicionais para:
    - Perfil do usuário (avatar, bio, cargo)
    - Autenticação por email
    - Autenticação social
    """
    # Campos de perfil
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    bio = models.TextField(blank=True, max_length=500)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)

    # Campos de autenticação
    is_active = models.BooleanField(default=False)
    email_verificado = models.BooleanField(default=False)  # Tornar default explícito
    ultimo_login_social = models.DateTimeField(null=True, blank=True)
    provedor_social = models.CharField(max_length=30, blank=True)
    uid_social = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else '/static/img/default_avatar.png'

    def get_nome_completo(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_full_name(self):
        # Sobrescrever o método padrão para compatibilidade com templates
        return self.get_nome_completo()

    def __str__(self):
        return self.email or self.username

    def clean(self):
        if self.data_nascimento and self.data_nascimento > timezone.now().date():
            raise ValidationError('Data de nascimento não pode ser futura.')

    def save(self, *args, **kwargs):
        # Chamar clean() antes de salvar para garantir validação
        self.clean()
        super().save(*args, **kwargs)


class SocialAuthSettings(models.Model):
    """
    Configurações para autenticação social
    """
    provider = models.CharField(max_length=30)
    client_id = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração de Autenticação Social'
        verbose_name_plural = 'Configurações de Autenticação Social'
        unique_together = ('provider',)

    def __str__(self):
        return f'{self.provider} - {self.client_id}'