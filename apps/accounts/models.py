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

    # Campos para ativação por código
    codigo_ativacao = models.CharField(max_length=6, blank=True, null=True)
    codigo_ativacao_criado_em = models.DateTimeField(null=True, blank=True)
    tentativas_codigo = models.IntegerField(default=0)

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

    def gerar_codigo_ativacao(self):
        """Gerar um código de ativação de 6 dígitos"""
        import random
        from django.utils import timezone

        self.codigo_ativacao = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.codigo_ativacao_criado_em = timezone.now()
        self.tentativas_codigo = 0
        self.save()
        return self.codigo_ativacao

    def codigo_ativacao_valido(self):
        """Verificar se o código de ativação ainda é válido (30 minutos)"""
        if not self.codigo_ativacao or not self.codigo_ativacao_criado_em:
            return False

        from django.utils import timezone
        from datetime import timedelta

        tempo_limite = self.codigo_ativacao_criado_em + timedelta(minutes=30)
        return timezone.now() <= tempo_limite

    def verificar_codigo_ativacao(self, codigo):
        """Verificar se o código fornecido está correto"""
        if not self.codigo_ativacao_valido():
            return False, "Código expirado. Solicite um novo código."

        if self.tentativas_codigo >= 5:
            return False, "Muitas tentativas incorretas. Solicite um novo código."

        if self.codigo_ativacao == codigo:
            return True, "Código válido."
        else:
            self.tentativas_codigo += 1
            self.save()
            tentativas_restantes = 5 - self.tentativas_codigo
            return False, f"Código incorreto. Você tem {tentativas_restantes} tentativas restantes."

    def limpar_codigo_ativacao(self):
        """Limpar dados do código de ativação após uso"""
        self.codigo_ativacao = None
        self.codigo_ativacao_criado_em = None
        self.tentativas_codigo = 0
        self.save()


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