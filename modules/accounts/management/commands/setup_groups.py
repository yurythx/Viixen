from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Cria grupos e permissões padrão do sistema'

    def handle(self, *args, **options):
        # Criar grupo Administrador
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Administrador" criado com sucesso!')
            )
        else:
            self.stdout.write('Grupo "Administrador" já existe.')

        # Adicionar todas as permissões ao grupo Administrador
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Grupo "Administrador" configurado com {all_permissions.count()} permissões.'
            )
        )

        # Criar outros grupos se necessário
        company_admin_group, created = Group.objects.get_or_create(name='Admin Empresa')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Admin Empresa" criado com sucesso!')
            )

        user_group, created = Group.objects.get_or_create(name='Usuário')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Usuário" criado com sucesso!')
            )

        self.stdout.write(
            self.style.SUCCESS('Setup de grupos concluído!')
        )
