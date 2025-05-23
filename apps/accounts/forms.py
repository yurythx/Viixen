from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import CustomUser, Cargo, Departamento

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'autocomplete': 'username'}),
        help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'email'}),
        help_text='Digite um email válido. Este será usado para recuperação de senha.'
    )

    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'autocomplete': 'new-password'}),
        help_text='Sua senha deve conter pelo menos 8 caracteres e não pode ser comum.'
    )

    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a senha', 'autocomplete': 'new-password'}),
        help_text='Digite a mesma senha do campo anterior, para verificação.'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email já está sendo usado.')
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({
            'onchange': 'previewImage(this)'
        })
        # Adicionar opções para cargo e departamento
        self.fields['cargo'].queryset = Cargo.objects.all()
        self.fields['departamento'].queryset = Departamento.objects.all()

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
        help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        help_text='Digite um email válido. Este será usado para recuperação de senha.',
        validators=[EmailValidator(message="Digite um endereço de email válido.")]
    )

    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nome'}),
        help_text='Seu nome.'
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
        help_text='Seu sobrenome.'
    )

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Fale um pouco sobre você', 'rows': 3}),
        max_length=500,
        required=False
    )

    data_nascimento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    telefone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(99) 99999-9999'})
    )

    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecione um cargo"
    )

    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecione um departamento"
    )

    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'avatar', 'bio',
            'data_nascimento', 'telefone', 'cargo', 'departamento'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("O email é obrigatório.")
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este email já está em uso por outro usuário.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name.strip()) < 2:
            raise ValidationError("O nome deve ter pelo menos 2 caracteres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name.strip()) < 2:
            raise ValidationError("O sobrenome deve ter pelo menos 2 caracteres.")
        return last_name

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError('A imagem deve ter no máximo 2MB.')
        return avatar

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remove caracteres não numéricos
            telefone_numerico = ''.join(filter(str.isdigit, telefone))

            # Verifica se o telefone tem pelo menos 10 dígitos (DDD + número)
            if len(telefone_numerico) < 10:
                raise ValidationError('O telefone deve ter pelo menos 10 dígitos, incluindo o DDD.')

            # Formata o telefone como (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
            if len(telefone_numerico) == 11:  # Celular com 9 dígitos
                telefone_formatado = f'({telefone_numerico[:2]}) {telefone_numerico[2:7]}-{telefone_numerico[7:]}'
            elif len(telefone_numerico) == 10:  # Telefone fixo
                telefone_formatado = f'({telefone_numerico[:2]}) {telefone_numerico[2:6]}-{telefone_numerico[6:]}'
            else:
                telefone_formatado = telefone_numerico

            return telefone_formatado
        return telefone


class UserProfileForm(forms.ModelForm):
    """Formulário somente leitura opcional para ProfileView, se quiser exibir com form."""
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control-plaintext'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'form-control-plaintext'}),
        }


class EmailSettingsForm(forms.Form):
    host = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    port = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    user = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    use_tls = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class SocialAuthSettingsForm(forms.Form):
    google_client_id = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    google_secret = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    github_client_id = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    github_secret = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )


class LDAPSettingsForm(forms.Form):
    server_uri = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='URI do servidor LDAP (ex: ldap://servidor.exemplo.com:389)'
    )
    bind_dn = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='DN de ligação para autenticação no servidor LDAP'
    )
    bind_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        help_text='Senha para autenticação no servidor LDAP'
    )
    domain = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'exemplo.com.br'}),
        help_text='Domínio para criação de emails de usuários LDAP'
    )
    user_search_base = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Base de pesquisa para usuários (ex: ou=users,dc=exemplo,dc=com)'
    )
    group_search_base = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Base de pesquisa para grupos (ex: ou=groups,dc=exemplo,dc=com)'
    )

    def clean_server_uri(self):
        server_uri = self.cleaned_data.get('server_uri')
        if not server_uri:
            raise ValidationError("A URI do servidor é obrigatória.")

        # Verificar se a URI começa com ldap:// ou ldaps://
        if not server_uri.startswith(('ldap://', 'ldaps://')):
            raise ValidationError("A URI deve começar com 'ldap://' ou 'ldaps://'")

        return server_uri

    def clean_domain(self):
        domain = self.cleaned_data.get('domain')
        if not domain:
            raise ValidationError("O domínio é obrigatório.")

        # Verificar se o domínio tem pelo menos um ponto
        if '.' not in domain:
            raise ValidationError("O domínio deve ser válido (ex: exemplo.com.br)")

        # Verificar se o domínio tem pelo menos 4 caracteres
        if len(domain) < 4:
            raise ValidationError("O domínio deve ter pelo menos 4 caracteres.")

        return domain
