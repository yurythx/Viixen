from django import forms
from .models import SocialProviderConfig, EmailConfig, SystemConfig, AppConfig

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

        # Filtrar dependências disponíveis (excluir o próprio app e apps que dependem dele)
        if self.instance and self.instance.pk:
            # Excluir o próprio app das opções de dependência
            self.fields['dependencies'].queryset = AppConfig.objects.exclude(pk=self.instance.pk)

            # Excluir apps que já dependem deste app (para evitar dependências circulares)
            dependent_apps = self.instance.dependents.all()
            if dependent_apps.exists():
                self.fields['dependencies'].queryset = self.fields['dependencies'].queryset.exclude(
                    pk__in=dependent_apps.values_list('pk', flat=True)
                )

        # Adicionar help text para o campo de dependências
        self.fields['dependencies'].help_text = (
            "Selecione os módulos que este app precisa para funcionar. "
            "Quando este app for ativado, suas dependências serão ativadas automaticamente."
        )