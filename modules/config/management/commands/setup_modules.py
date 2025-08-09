from django.core.management.base import BaseCommand
from django.db import transaction
from modules.config.domain.module import Module


class Command(BaseCommand):
    help = 'Configura os módulos iniciais do sistema'

    def handle(self, *args, **options):
        self.stdout.write('Configurando módulos do sistema...')
        
        modules_data = [
            {
                'name': 'Configurações',
                'slug': 'config',
                'app_label': 'modules.config',
                'description': 'Gerenciamento de empresas, usuários e configurações do sistema',
                'icon': 'fas fa-cogs',
                'is_core': True,
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Contas e Usuários',
                'slug': 'accounts',
                'app_label': 'modules.accounts',
                'description': 'Gerenciamento de usuários, autenticação e permissões',
                'icon': 'fas fa-users',
                'is_core': True,
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Páginas',
                'slug': 'pages',
                'app_label': 'modules.pages',
                'description': 'Gerenciamento de páginas institucionais e conteúdo estático',
                'icon': 'fas fa-file-alt',
                'is_core': True,
                'is_active': True,
                'order': 3
            },
            {
                'name': 'Blog',
                'slug': 'blog',
                'app_label': 'modules.blog',
                'description': 'Sistema de blog com posts, categorias e tags',
                'icon': 'fas fa-blog',
                'is_core': False,
                'is_active': True,
                'order': 10
            }
        ]
        
        with transaction.atomic():
            created_count = 0
            updated_count = 0
            
            for module_data in modules_data:
                module, created = Module.objects.get_or_create(
                    app_label=module_data['app_label'],
                    defaults=module_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Módulo "{module.name}" criado')
                    )
                else:
                    # Atualizar dados do módulo existente
                    for key, value in module_data.items():
                        if key != 'app_label':  # Não atualizar app_label
                            setattr(module, key, value)
                    module.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Módulo "{module.name}" atualizado')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Configuração concluída!\n'
                f'   • {created_count} módulos criados\n'
                f'   • {updated_count} módulos atualizados\n'
                f'   • Total: {Module.objects.count()} módulos no sistema'
            )
        )
        
        # Mostrar resumo dos módulos
        self.stdout.write('\n📋 Resumo dos Módulos:')
        core_modules = Module.objects.filter(is_core=True).order_by('order')
        optional_modules = Module.objects.filter(is_core=False).order_by('order')
        
        self.stdout.write('\n🔒 Módulos Core (não podem ser desabilitados):')
        for module in core_modules:
            status = '✅ Ativo' if module.is_active else '❌ Inativo'
            self.stdout.write(f'   • {module.name} ({module.app_label}) - {status}')
        
        self.stdout.write('\n🧩 Módulos Opcionais (podem ser habilitados/desabilitados):')
        for module in optional_modules:
            status = '✅ Ativo' if module.is_active else '❌ Inativo'
            self.stdout.write(f'   • {module.name} ({module.app_label}) - {status}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Sistema de módulos configurado com sucesso!'
            )
        )
