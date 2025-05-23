from django.core.management.base import BaseCommand
from django.apps import apps
from apps.config.models import AppConfig

class Command(BaseCommand):
    help = 'Registra os apps instalados no sistema'

    def handle(self, *args, **options):
        # Apps core que não podem ser desativados
        core_apps = ['accounts', 'config', 'pages']
        
        # Registrar apps do projeto
        for app_config in apps.get_app_configs():
            if app_config.name.startswith('apps.'):
                app_label = app_config.name.split('.')[-1]
                
                # Verificar se o app já está registrado
                app, created = AppConfig.objects.get_or_create(
                    label=app_label,
                    defaults={
                        'name': app_config.verbose_name or app_label.capitalize(),
                        'is_core': app_label in core_apps,
                        'is_active': True,
                        'description': f'Módulo {app_label.capitalize()} do sistema',
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'App "{app.name}" registrado com sucesso!'))
                else:
                    self.stdout.write(f'App "{app.name}" já está registrado.')
