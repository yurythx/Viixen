from django.apps import AppConfig


class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.config'
    verbose_name = 'Configurações'

    def ready(self):
        from . import signals  # Importa os signals para registrá-los
