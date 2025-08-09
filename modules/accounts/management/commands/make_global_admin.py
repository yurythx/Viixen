from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Adiciona um usuário ao grupo Administrador (admin global)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nome do usuário para tornar admin global')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuário "{username}" não encontrado.')
            )
            return

        # Obter ou criar grupo Administrador
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        
        # Adicionar usuário ao grupo
        user.groups.add(admin_group)
        
        # Tornar superuser também (para garantir acesso total)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Usuário "{username}" agora é um administrador global com acesso total ao sistema!'
            )
        )
