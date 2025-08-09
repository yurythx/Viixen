from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..domain.user import CustomUser
from modules.config.domain.company import Company

class UserForm(forms.ModelForm):
    """
    Formulário para edição de usuários.
    Permite alterar empresa apenas para Administradores globais e superusuários.
    """
    
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        
        # Apenas Administradores globais e superusuários podem alterar empresa
        if self.request_user:
            is_global_admin = (
                self.request_user.is_superuser or 
                (hasattr(self.request_user, 'groups') and 
                 self.request_user.groups.filter(name='Administrador').exists())
            )
            
            if is_global_admin:
                # Administradores globais podem alterar empresa e status de superusuário
                self.fields['company'] = forms.ModelChoiceField(
                    queryset=Company.objects.all(),
                    required=False,
                    empty_label="Sem empresa (usuário global)",
                    widget=forms.Select(attrs={'class': 'form-control'}),
                    label='Empresa',
                    help_text='Apenas administradores globais podem alterar a empresa de um usuário'
                )
                self.fields['is_superuser'] = forms.BooleanField(
                    required=False,
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    label='Superusuário',
                    help_text='Concede acesso total ao sistema'
                )
            else:
                # Usuários normais não podem alterar empresa
                if 'company' in self.fields:
                    del self.fields['company']
                if 'is_superuser' in self.fields:
                    del self.fields['is_superuser']
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'is_company_admin', 'is_superuser', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'is_company_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'phone': 'Telefone',
            'company': 'Empresa',
            'is_company_admin': 'Administrador da Empresa',
            'is_superuser': 'Superusuário',
            'is_active': 'Ativo',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Usuários sem empresa mantêm status atual (não são promovidos automaticamente)
        if not user.company and not user.is_superuser:
            user.is_staff = False  # Usuários globais não têm acesso ao admin por padrão
        
        if commit:
            user.save()
        return user

class UserCreateForm(UserCreationForm):
    """
    Formulário para criação de usuários.
    Permite definir empresa na criação. Se não definir empresa, usuário será superadmin.
    """
    first_name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nome'
    )
    last_name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Sobrenome'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )
    phone = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Telefone'
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        empty_label="Sem empresa (usuário global)",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Empresa',
        help_text='Administradores globais podem criar usuários para qualquer empresa ou sem empresa'
    )
    is_company_admin = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Administrador da Empresa',
        help_text='Apenas válido se uma empresa for selecionada'
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'company', 'is_company_admin', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nome de usuário',
        }
    
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Controle de permissões para criação de usuários
        if self.request_user:
            # Superadmin e grupo "Administrador" podem criar usuários para qualquer empresa
            is_global_admin = (self.request_user.is_superuser or 
                             (hasattr(self.request_user, 'groups') and 
                              self.request_user.groups.filter(name='Administrador').exists()))
            
            if is_global_admin:
                # Administradores globais veem todas as empresas + opção "sem empresa"
                self.fields['company'].queryset = Company.objects.all()
                self.fields['company'].empty_label = "Sem empresa (usuário global)"
                self.fields['company'].help_text = 'Administradores globais podem criar usuários para qualquer empresa ou sem empresa'
            else:
                # Admins de empresa só podem criar usuários da própria empresa
                if hasattr(self.request_user, 'company') and self.request_user.company:
                    self.fields['company'].queryset = Company.objects.filter(id=self.request_user.company.id)
                    self.fields['company'].initial = self.request_user.company
                    self.fields['company'].required = True
                    self.fields['company'].empty_label = None  # Não podem criar sem empresa
                    self.fields['company'].help_text = 'Você só pode criar usuários para sua empresa'
                else:
                    # Usuários sem empresa não podem criar outros usuários
                    self.fields['company'].queryset = Company.objects.none()
                    self.fields['company'].help_text = 'Você não tem permissão para criar usuários'
    
    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        is_company_admin = cleaned_data.get('is_company_admin')
        
        # Se não tem empresa, não pode ser admin da empresa
        if not company and is_company_admin:
            raise forms.ValidationError(
                'Usuário sem empresa não pode ser administrador da empresa.'
            )
        
        # Apenas superadmins e grupo "Administrador" podem criar usuários sem empresa
        if not company and self.request_user:
            is_global_admin = (self.request_user.is_superuser or 
                             (hasattr(self.request_user, 'groups') and 
                              self.request_user.groups.filter(name='Administrador').exists()))
            if not is_global_admin:
                raise forms.ValidationError(
                    'Apenas superadministradores e administradores globais podem criar usuários sem empresa.'
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Usuários sem empresa são "usuários globais" mas não superadmins automaticamente
        if not user.company:
            user.is_superuser = False  # Não é superadmin automaticamente
            user.is_staff = False      # Não tem acesso ao admin por padrão
            user.is_company_admin = False  # Não pode ser admin de empresa se não tem empresa
        
        if commit:
            user.save()
        return user