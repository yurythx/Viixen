from django.apps import AppConfig


class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.config'
    verbose_name = 'Configurações'

    def ready(self):
        from . import signals  # Importa os signals para registrá-los
        # Aplicar configurações de email na inicialização
        self.apply_email_settings()

    def apply_email_settings(self):
        """Aplica as configurações de email na inicialização do Django"""
        try:
            # Importar aqui para evitar problemas de inicialização
            from .models import EmailConfig
            from .email_utils import apply_email_settings_to_django

            # Obter configuração padrão
            default_config = EmailConfig.objects.filter(is_default=True, is_active=True).first()

            if default_config:
                apply_email_settings_to_django(default_config)
                print(f"✅ Configurações de email aplicadas na inicialização: {default_config.email_host_user}")
            else:
                print("⚠️  Nenhuma configuração de email padrão encontrada na inicialização")

        except Exception as e:
            # Ignorar erros durante migrações ou quando o banco não existe
            pass
