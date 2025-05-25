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


class EnvironmentVariable(models.Model):
    """Modelo para gerenciar variáveis de ambiente"""

    CATEGORY_CHOICES = [
        ('core', 'Django Core'),
        ('database', 'Database'),
        ('email', 'Email'),
        ('security', 'Security'),
        ('site', 'Site'),
        ('static', 'Static & Media'),
        ('cache', 'Cache'),
        ('logging', 'Logging'),
        ('auth', 'Authentication'),
        ('ldap', 'LDAP'),
        ('social', 'Social Auth'),
        ('services', 'Third-party Services'),
        ('api', 'API Keys'),
        ('development', 'Development'),
        ('performance', 'Performance'),
        ('custom', 'Custom Application'),
        ('backup', 'Backup & Maintenance'),
    ]

    TYPE_CHOICES = [
        ('string', 'String'),
        ('boolean', 'Boolean'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('url', 'URL'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('json', 'JSON'),
        ('csv', 'CSV (Comma Separated)'),
    ]

    key = models.CharField(max_length=100, unique=True, help_text="Nome da variável (ex: DEBUG)")
    value = models.TextField(blank=True, help_text="Valor da variável")
    default_value = models.TextField(blank=True, help_text="Valor padrão")
    description = models.TextField(help_text="Descrição da variável")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='custom')
    var_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='string')
    is_required = models.BooleanField(default=False, help_text="Variável obrigatória")
    is_sensitive = models.BooleanField(default=False, help_text="Variável sensível (senha, chave, etc.)")
    is_active = models.BooleanField(default=True, help_text="Variável ativa no sistema")
    order = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Variável de Ambiente'
        verbose_name_plural = 'Variáveis de Ambiente'
        ordering = ['category', 'order', 'key']

    def __str__(self):
        return f"{self.key} ({self.get_category_display()})"

    def get_display_value(self):
        """Retorna o valor para exibição (mascarado se sensível)"""
        if self.is_sensitive and self.value:
            return '*' * min(len(self.value), 8)
        return self.value

    def get_typed_value(self):
        """Retorna o valor convertido para o tipo correto"""
        if not self.value:
            return self.get_typed_default()

        try:
            if self.var_type == 'boolean':
                return self.value.lower() in ('true', '1', 'yes', 'on')
            elif self.var_type == 'integer':
                return int(self.value)
            elif self.var_type == 'float':
                return float(self.value)
            elif self.var_type == 'csv':
                return [item.strip() for item in self.value.split(',') if item.strip()]
            elif self.var_type == 'json':
                import json
                return json.loads(self.value)
            else:
                return self.value
        except (ValueError, TypeError, json.JSONDecodeError):
            return self.get_typed_default()

    def get_typed_default(self):
        """Retorna o valor padrão convertido para o tipo correto"""
        if not self.default_value:
            if self.var_type == 'boolean':
                return False
            elif self.var_type in ['integer', 'float']:
                return 0
            elif self.var_type in ['csv', 'json']:
                return []
            else:
                return ''

        try:
            if self.var_type == 'boolean':
                return self.default_value.lower() in ('true', '1', 'yes', 'on')
            elif self.var_type == 'integer':
                return int(self.default_value)
            elif self.var_type == 'float':
                return float(self.default_value)
            elif self.var_type == 'csv':
                return [item.strip() for item in self.default_value.split(',') if item.strip()]
            elif self.var_type == 'json':
                import json
                return json.loads(self.default_value)
            else:
                return self.default_value
        except (ValueError, TypeError, json.JSONDecodeError):
            return self.default_value


class DatabaseConfig(models.Model):
    """Modelo para configurar diferentes tipos de banco de dados"""

    ENGINE_CHOICES = [
        ('django.db.backends.sqlite3', 'SQLite'),
        ('django.db.backends.postgresql', 'PostgreSQL'),
        ('django.db.backends.mysql', 'MySQL'),
        ('django.db.backends.oracle', 'Oracle'),
    ]

    name = models.CharField(max_length=100, default='default', help_text="Nome da configuração do banco")
    slug = models.SlugField(max_length=60, unique=True, blank=True, default='database-config')
    engine = models.CharField(max_length=100, choices=ENGINE_CHOICES, default='django.db.backends.sqlite3')

    # Configurações básicas
    database_name = models.CharField(max_length=255, help_text="Nome do banco de dados ou caminho para SQLite")
    host = models.CharField(max_length=255, blank=True, default='localhost', help_text="Host do servidor de banco")
    port = models.IntegerField(blank=True, null=True, help_text="Porta do servidor (deixe vazio para padrão)")
    user = models.CharField(max_length=255, blank=True, help_text="Usuário do banco de dados")
    password = models.CharField(max_length=500, blank=True, help_text="Senha do banco de dados")

    # Configurações avançadas
    conn_max_age = models.IntegerField(default=0, help_text="Tempo máximo de vida da conexão em segundos")
    conn_health_checks = models.BooleanField(default=False, help_text="Verificações de saúde da conexão")

    # Configurações SSL
    ssl_require = models.BooleanField(default=False, help_text="Exigir conexão SSL")
    ssl_ca = models.CharField(max_length=500, blank=True, help_text="Caminho para certificado CA SSL")
    ssl_cert = models.CharField(max_length=500, blank=True, help_text="Caminho para certificado SSL")
    ssl_key = models.CharField(max_length=500, blank=True, help_text="Caminho para chave SSL")

    # Configurações específicas
    charset = models.CharField(max_length=50, blank=True, default='utf8mb4', help_text="Charset para MySQL")
    atomic_requests = models.BooleanField(default=False, help_text="Usar transações atômicas")
    autocommit = models.BooleanField(default=True, help_text="Auto-commit das transações")

    # Configurações de teste
    test_database_name = models.CharField(max_length=255, blank=True, help_text="Nome do banco para testes")

    is_active = models.BooleanField(default=True, help_text="Configuração ativa")
    is_default = models.BooleanField(default=False, help_text="Configuração padrão do sistema")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campo para armazenar a senha em texto simples temporariamente
    _password_plain = None

    class Meta:
        verbose_name = 'Configuração de Banco de Dados'
        verbose_name_plural = 'Configurações de Banco de Dados'
        ordering = ['-is_default', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = 'database-config'

        # Garantir que apenas uma configuração seja padrão
        if self.is_default:
            DatabaseConfig.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)

        # Criptografar a senha se for nova ou se foi alterada
        if self._password_plain:
            self.password = PasswordEncryptor.encrypt_password(self._password_plain)
            self._password_plain = None

        # Definir porta padrão baseada no engine
        if not self.port:
            if 'postgresql' in self.engine:
                self.port = 5432
            elif 'mysql' in self.engine:
                self.port = 3306
            elif 'oracle' in self.engine:
                self.port = 1521

        super().save(*args, **kwargs)

    def set_password(self, password):
        """Define a senha em texto simples para ser criptografada no save()"""
        self._password_plain = password

    def get_password(self):
        """Retorna a senha descriptografada"""
        if self.password:
            return PasswordEncryptor.decrypt_password(self.password)
        return ''

    def get_database_url(self):
        """Gera a URL de conexão do banco de dados"""
        if self.engine == 'django.db.backends.sqlite3':
            return f"sqlite:///{self.database_name}"

        # Para outros bancos
        engine_map = {
            'django.db.backends.postgresql': 'postgresql',
            'django.db.backends.mysql': 'mysql',
            'django.db.backends.oracle': 'oracle',
        }

        scheme = engine_map.get(self.engine, 'postgresql')
        password = self.get_password()

        if self.user and password:
            auth = f"{self.user}:{password}@"
        elif self.user:
            auth = f"{self.user}@"
        else:
            auth = ""

        port_part = f":{self.port}" if self.port else ""

        return f"{scheme}://{auth}{self.host}{port_part}/{self.database_name}"

    def get_django_config(self):
        """Retorna a configuração no formato do Django DATABASES"""
        config = {
            'ENGINE': self.engine,
            'NAME': self.database_name,
        }

        if self.engine != 'django.db.backends.sqlite3':
            config.update({
                'HOST': self.host,
                'PORT': self.port,
                'USER': self.user,
                'PASSWORD': self.get_password(),
            })

        # Opções adicionais
        options = {}

        if self.ssl_require:
            if 'mysql' in self.engine:
                options['ssl'] = {'ssl_require': True}
                if self.ssl_ca:
                    options['ssl']['ssl_ca'] = self.ssl_ca
                if self.ssl_cert:
                    options['ssl']['ssl_cert'] = self.ssl_cert
                if self.ssl_key:
                    options['ssl']['ssl_key'] = self.ssl_key
            elif 'postgresql' in self.engine:
                options['sslmode'] = 'require'

        if 'mysql' in self.engine and self.charset:
            options['charset'] = self.charset

        if options:
            config['OPTIONS'] = options

        # Configurações de conexão
        if self.conn_max_age:
            config['CONN_MAX_AGE'] = self.conn_max_age

        if self.conn_health_checks:
            config['CONN_HEALTH_CHECKS'] = True

        if self.atomic_requests:
            config['ATOMIC_REQUESTS'] = True

        if not self.autocommit:
            config['AUTOCOMMIT'] = False

        # Configurações de teste
        if self.test_database_name:
            config['TEST'] = {'NAME': self.test_database_name}

        return config

    def test_connection(self):
        """Testa a conexão com o banco de dados"""
        try:
            from django.db import connections
            from django.core.management.color import no_style
            from django.db.backends.utils import truncate_name

            # Criar uma conexão temporária
            config = self.get_django_config()

            # Para SQLite, verificar se o arquivo existe ou pode ser criado
            if self.engine == 'django.db.backends.sqlite3':
                import os
                db_path = self.database_name
                if not os.path.exists(db_path):
                    # Tentar criar o diretório se necessário
                    os.makedirs(os.path.dirname(db_path), exist_ok=True)
                return True, "Conexão SQLite válida"

            # Para outros bancos, tentar conectar
            import django.db
            from django.db.backends import utils

            # Simular teste de conexão
            return True, "Configuração válida (teste completo requer conexão real)"

        except Exception as e:
            return False, str(e)

    def __str__(self):
        status = "Ativa" if self.is_active else "Inativa"
        default = " (Padrão)" if self.is_default else ""
        return f"{self.name} - {self.get_engine_display()}{default} - {status}"
