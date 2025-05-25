from django import forms
from .models import SocialProviderConfig, EmailConfig, SystemConfig, AppConfig, LDAPConfig, EnvironmentVariable, DatabaseConfig

class SocialProviderConfigForm(forms.ModelForm):
    class Meta:
        model = SocialProviderConfig
        fields = ['provider', 'client_id', 'secret_key', 'is_active']
        widgets = {
            'secret_key': forms.PasswordInput(),
        }

class EmailConfigForm(forms.ModelForm):
    class Meta:
        model = EmailConfig
        fields = ['email_host', 'email_port', 'email_host_user', 'email_host_password',
                 'email_use_tls', 'default_from_email', 'is_active']
        widgets = {
            'email_host_password': forms.PasswordInput(),
        }

class SystemConfigForm(forms.ModelForm):
    class Meta:
        model = SystemConfig
        fields = ['site_name', 'site_description', 'maintenance_mode',
                 'allow_registration', 'require_email_verification', 'enable_app_management']

class AppConfigForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = ['name', 'description', 'is_active', 'dependencies', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'dependencies': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Desabilitar campo is_active para apps core
        if self.instance and self.instance.is_core:
            self.fields['is_active'].disabled = True
            self.fields['is_active'].help_text = "Apps core não podem ser desativados"


class EnvironmentVariableForm(forms.ModelForm):
    class Meta:
        model = EnvironmentVariable
        fields = ['key', 'value', 'default_value', 'description', 'category',
                 'var_type', 'is_required', 'is_sensitive', 'is_active', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'value': forms.Textarea(attrs={'rows': 2}),
            'default_value': forms.Textarea(attrs={'rows': 2}),
            'key': forms.TextInput(attrs={'placeholder': 'Ex: DEBUG, SECRET_KEY'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Campo de valor sensível
        if self.instance and self.instance.is_sensitive:
            self.fields['value'].widget = forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o valor (será mascarado)'
            })

        # Ajustar widget baseado no tipo
        if self.instance and self.instance.var_type:
            self._adjust_widget_by_type()

    def _adjust_widget_by_type(self):
        """Ajusta o widget baseado no tipo da variável"""
        var_type = self.instance.var_type

        if var_type == 'boolean':
            self.fields['value'].widget = forms.Select(
                choices=[('', '---'), ('True', 'True'), ('False', 'False')],
                attrs={'class': 'form-select'}
            )
        elif var_type == 'integer':
            self.fields['value'].widget = forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1'
            })
        elif var_type == 'float':
            self.fields['value'].widget = forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any'
            })
        elif var_type == 'email':
            self.fields['value'].widget = forms.EmailInput(attrs={
                'class': 'form-control'
            })
        elif var_type == 'url':
            self.fields['value'].widget = forms.URLInput(attrs={
                'class': 'form-control'
            })

    def clean_key(self):
        """Validar formato da chave"""
        key = self.cleaned_data.get('key', '').upper()

        # Verificar se contém apenas letras, números e underscore
        import re
        if not re.match(r'^[A-Z0-9_]+$', key):
            raise forms.ValidationError(
                'A chave deve conter apenas letras maiúsculas, números e underscore.'
            )

        return key

    def clean_value(self):
        """Validar valor baseado no tipo"""
        value = self.cleaned_data.get('value', '')
        var_type = self.cleaned_data.get('var_type', 'string')

        if not value:
            return value

        try:
            if var_type == 'boolean':
                if value.lower() not in ['true', 'false', '1', '0', 'yes', 'no', 'on', 'off']:
                    raise forms.ValidationError(
                        'Valor booleano deve ser: true/false, 1/0, yes/no, on/off'
                    )
            elif var_type == 'integer':
                int(value)
            elif var_type == 'float':
                float(value)
            elif var_type == 'json':
                import json
                json.loads(value)
            elif var_type == 'email':
                from django.core.validators import validate_email
                validate_email(value)
            elif var_type == 'url':
                from django.core.validators import URLValidator
                validator = URLValidator()
                validator(value)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            raise forms.ValidationError(f'Valor inválido para o tipo {var_type}: {str(e)}')
        except forms.ValidationError:
            raise

        return value


class EnvironmentVariableFilterForm(forms.Form):
    """Formulário para filtrar variáveis de ambiente"""

    category = forms.ChoiceField(
        choices=[('', 'Todas as categorias')] + EnvironmentVariable.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    var_type = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + EnvironmentVariable.TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    is_required = forms.ChoiceField(
        choices=[('', 'Todas'), ('true', 'Obrigatórias'), ('false', 'Opcionais')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    is_sensitive = forms.ChoiceField(
        choices=[('', 'Todas'), ('true', 'Sensíveis'), ('false', 'Não sensíveis')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por chave ou descrição...'
        })
    )


class DatabaseConfigForm(forms.ModelForm):
    """Formulário para configuração de banco de dados"""

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Confirmar Senha'
    )

    class Meta:
        model = DatabaseConfig
        fields = [
            'name', 'engine', 'database_name', 'host', 'port', 'user', 'password',
            'conn_max_age', 'conn_health_checks', 'ssl_require', 'ssl_ca', 'ssl_cert', 'ssl_key',
            'charset', 'atomic_requests', 'autocommit', 'test_database_name', 'is_active', 'is_default'
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'ssl_ca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/path/to/ca-cert.pem'}),
            'ssl_cert': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/path/to/client-cert.pem'}),
            'ssl_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/path/to/client-key.pem'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if field_name not in ['password', 'password_confirm']:
                field.widget.attrs.update({'class': 'form-control'})

        # Configurar campos específicos
        self.fields['engine'].widget.attrs.update({'class': 'form-select'})
        self.fields['port'].widget.attrs.update({'placeholder': 'Deixe vazio para usar porta padrão'})

        # Se editando, preencher senha atual
        if self.instance and self.instance.pk:
            self.fields['password'].widget.attrs['placeholder'] = 'Deixe vazio para manter senha atual'
            self.fields['password_confirm'].widget.attrs['placeholder'] = 'Deixe vazio para manter senha atual'

    def clean_password_confirm(self):
        """Validar confirmação de senha"""
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')

        return password_confirm

    def clean_port(self):
        """Validar porta"""
        port = self.cleaned_data.get('port')
        if port and (port < 1 or port > 65535):
            raise forms.ValidationError('A porta deve estar entre 1 e 65535.')
        return port

    def clean(self):
        """Validação geral do formulário"""
        cleaned_data = super().clean()
        engine = cleaned_data.get('engine')
        database_name = cleaned_data.get('database_name')
        host = cleaned_data.get('host')
        user = cleaned_data.get('user')

        # Validações específicas por engine
        if engine == 'django.db.backends.sqlite3':
            if not database_name:
                raise forms.ValidationError({'database_name': 'Nome do arquivo SQLite é obrigatório.'})
        else:
            if not host:
                raise forms.ValidationError({'host': 'Host é obrigatório para este tipo de banco.'})
            if not database_name:
                raise forms.ValidationError({'database_name': 'Nome do banco é obrigatório.'})
            if not user:
                raise forms.ValidationError({'user': 'Usuário é obrigatório para este tipo de banco.'})

        return cleaned_data

    def save(self, commit=True):
        """Salvar com tratamento de senha"""
        instance = super().save(commit=False)

        # Tratar senha
        password = self.cleaned_data.get('password')
        if password:
            instance.set_password(password)

        if commit:
            instance.save()

        return instance


class LDAPConfigForm(forms.ModelForm):
    """Formulário para configuração LDAP"""

    bind_password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Confirmar Senha de Bind'
    )

    class Meta:
        model = LDAPConfig
        fields = [
            'server', 'port', 'server_uri', 'base_dn', 'bind_dn', 'bind_password',
            'domain', 'search_filter', 'is_active'
        ]
        widgets = {
            'bind_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'search_filter': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(objectClass=person)'
            }),
            'server_uri': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ldap://servidor.exemplo.com:389'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if field_name not in ['bind_password', 'bind_password_confirm']:
                field.widget.attrs.update({'class': 'form-control'})

        # Configurar placeholders
        self.fields['server'].widget.attrs.update({
            'placeholder': 'servidor.exemplo.com'
        })
        self.fields['base_dn'].widget.attrs.update({
            'placeholder': 'dc=exemplo,dc=com'
        })
        self.fields['bind_dn'].widget.attrs.update({
            'placeholder': 'cn=admin,dc=exemplo,dc=com'
        })
        self.fields['domain'].widget.attrs.update({
            'placeholder': 'exemplo.com'
        })

        # Se editando, preencher senha atual
        if self.instance and self.instance.pk:
            self.fields['bind_password'].widget.attrs['placeholder'] = 'Deixe vazio para manter senha atual'
            self.fields['bind_password_confirm'].widget.attrs['placeholder'] = 'Deixe vazio para manter senha atual'

    def clean_bind_password_confirm(self):
        """Validar confirmação de senha"""
        password = self.cleaned_data.get('bind_password')
        password_confirm = self.cleaned_data.get('bind_password_confirm')

        if password and password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')

        return password_confirm

    def clean_port(self):
        """Validar porta LDAP"""
        port = self.cleaned_data.get('port')
        if port and (port < 1 or port > 65535):
            raise forms.ValidationError('A porta deve estar entre 1 e 65535.')
        return port

    def clean_server_uri(self):
        """Validar URI do servidor"""
        server_uri = self.cleaned_data.get('server_uri')
        if server_uri and not (server_uri.startswith('ldap://') or server_uri.startswith('ldaps://')):
            raise forms.ValidationError('URI deve começar com ldap:// ou ldaps://')
        return server_uri

    def save(self, commit=True):
        """Salvar com tratamento de senha"""
        instance = super().save(commit=False)

        # Tratar senha
        password = self.cleaned_data.get('bind_password')
        if password:
            instance.set_password(password)

        if commit:
            instance.save()

        return instance