from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

# Classe para criptografia de senhas
class PasswordEncryptor:
    @staticmethod
    def get_key():
        # Usar SECRET_KEY como base para a chave de criptografia
        # Em produção, seria melhor usar uma chave separada armazenada de forma segura
        secret = settings.SECRET_KEY.encode()
        salt = b'django_secure_salt'  # Salt fixo para consistência

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(secret))
        return key

    @staticmethod
    def encrypt_password(password):
        if not password:
            return ''

        key = PasswordEncryptor.get_key()
        f = Fernet(key)
        encrypted = f.encrypt(password.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    @staticmethod
    def decrypt_password(encrypted_password):
        if not encrypted_password:
            return ''

        try:
            key = PasswordEncryptor.get_key()
            f = Fernet(key)
            decrypted = f.decrypt(base64.urlsafe_b64decode(encrypted_password))
            return decrypted.decode()
        except (InvalidToken, ValueError, TypeError):
            # Se houver erro na descriptografia, retornar string vazia
            return ''

class SocialProviderConfig(models.Model):
    provider = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    client_id = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.provider)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Configuração de Provedor Social'
        verbose_name_plural = 'Configurações de Provedores Sociais'

    def __str__(self):
        return f'{self.provider} - {"Ativo" if self.is_active else "Inativo"}'

class EmailConfig(models.Model):
    email_host = models.CharField(max_length=255)
    slug = models.SlugField(max_length=60, unique=True, blank=True, default='email-config')
    email_port = models.IntegerField()
    email_host_user = models.CharField(max_length=255)
    email_host_password = models.CharField(max_length=500)  # Aumentado para acomodar texto criptografado
    email_use_tls = models.BooleanField(default=True)
    default_from_email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campo para armazenar a senha em texto simples temporariamente
    _password_plain = None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = 'email-config'

        # Criptografar a senha se for nova ou se foi alterada
        if self._password_plain:
            self.email_host_password = PasswordEncryptor.encrypt_password(self._password_plain)
            self._password_plain = None

        super().save(*args, **kwargs)

    def set_password(self, password):
        """Define a senha em texto simples para ser criptografada no save()"""
        self._password_plain = password

    def get_password(self):
        """Retorna a senha descriptografada"""
        return PasswordEncryptor.decrypt_password(self.email_host_password)

    class Meta:
        verbose_name = 'Configuração de Email'
        verbose_name_plural = 'Configurações de Email'

    def __str__(self):
        return f'Configuração de Email - {"Ativa" if self.is_active else "Inativa"}'

class LDAPConfig(models.Model):
    server = models.CharField(max_length=255)
    server_uri = models.CharField(max_length=255, blank=True, help_text='URI completa do servidor LDAP (ex: ldap://servidor:389)')
    slug = models.SlugField(max_length=60, unique=True, blank=True, default='ldap-config')
    port = models.IntegerField(default=389)
    base_dn = models.CharField(max_length=255)
    bind_dn = models.CharField(max_length=255, blank=True)
    bind_password = models.CharField(max_length=500, blank=True)  # Aumentado para acomodar texto criptografado
    domain = models.CharField(max_length=255, blank=True, help_text='Domínio para criação de emails de usuários LDAP')
    search_filter = models.CharField(max_length=255, default='(objectClass=person)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campo para armazenar a senha em texto simples temporariamente
    _password_plain = None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = 'ldap-config'

        # Gerar server_uri se não estiver definido
        if not self.server_uri and self.server:
            self.server_uri = f'ldap://{self.server}:{self.port}'

        # Criptografar a senha se for nova ou se foi alterada
        if self._password_plain:
            self.bind_password = PasswordEncryptor.encrypt_password(self._password_plain)
            self._password_plain = None

        # Validar o domínio
        if self.domain and '.' not in self.domain:
            raise models.ValidationError({'domain': 'O domínio deve ser válido (ex: exemplo.com.br)'})

        super().save(*args, **kwargs)

    def set_password(self, password):
        """Define a senha em texto simples para ser criptografada no save()"""
        self._password_plain = password

    def get_password(self):
        """Retorna a senha descriptografada"""
        return PasswordEncryptor.decrypt_password(self.bind_password)

    class Meta:
        verbose_name = 'Configuração LDAP'
        verbose_name_plural = 'Configurações LDAP'

    def __str__(self):
        return f'Configuração LDAP - {self.server}'

    def get_server_uri(self):
        """Retorna a URI completa do servidor LDAP"""
        if self.server_uri:
            return self.server_uri
        return f'ldap://{self.server}:{self.port}'


class SystemConfig(models.Model):
    site_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=60, unique=True, blank=True, default='system-config')
    site_description = models.TextField()
    maintenance_mode = models.BooleanField(default=False)
    allow_registration = models.BooleanField(default=True)
    require_email_verification = models.BooleanField(default=True)
    enable_app_management = models.BooleanField(default=True, help_text="Permite ativar/desativar módulos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = 'system-config'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'

    def __str__(self):
        return f'Configuração do Sistema - {self.site_name}'


class AppConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_core = models.BooleanField(default=False, help_text="Apps core não podem ser desativados")
    order = models.PositiveIntegerField(default=0)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependents', help_text="Módulos que este app depende para funcionar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração de App'
        verbose_name_plural = 'Configurações de Apps'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {'Ativo' if self.is_active else 'Inativo'}"

    def save(self, *args, **kwargs):
        # Não permitir desativar apps core ou o app pages
        if self.is_core or self.label == 'pages':
            self.is_active = True
            if self.label == 'pages' and not self.is_core:
                self.is_core = True  # Garantir que pages seja marcado como core

        # Salvar primeiro para poder verificar dependências (necessário para objetos novos)
        super().save(*args, **kwargs)

        # Se o app está sendo ativado, verificar e ativar suas dependências
        if self.is_active and self.pk:
            for dependency in self.dependencies.all():
                if not dependency.is_active:
                    dependency.is_active = True
                    dependency.save()

    def clean(self):
        """Validação adicional para garantir que apps core e pages não possam ser desativados."""
        from django.core.exceptions import ValidationError

        # Verificar se apps core e pages não podem ser desativados
        if (self.is_core or self.label == 'pages') and not self.is_active:
            raise ValidationError("Apps core e o app 'pages' não podem ser desativados.")

        # Verificar se há apps dependentes ativos
        if not self.is_active and self.pk:  # Verificar apenas para objetos existentes
            active_dependents = self.dependents.filter(is_active=True)
            if active_dependents.exists():
                dependent_names = ", ".join([app.name for app in active_dependents])
                raise ValidationError(
                    f"Não é possível desativar este módulo porque os seguintes módulos dependem dele: {dependent_names}. "
                    f"Desative esses módulos primeiro."
                )
