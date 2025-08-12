from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group


class GlobalAdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar se o usuário é um administrador global ou superusuário.
    
    Um administrador global é definido como:
    1. Um superusuário (is_superuser=True), OU
    2. Um usuário que pertence ao grupo 'Administrador'
    """
    
    def test_func(self):
        """
        Verifica se o usuário tem permissão de administrador global.
        """
        if not self.request.user.is_authenticated:
            return False
            
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Administrador').exists()
    
    def handle_no_permission(self):
        """
        Mensagem de erro quando o usuário não tem permissão.
        """
        if not self.request.user.is_authenticated:
            # Redireciona para a página de login se não estiver autenticado
            return super().handle_no_permission()
            
        # Mensagem de erro personalizada para usuários autenticados sem permissão
        raise PermissionDenied(
            "Você não tem permissão para acessar esta página. "
            "Apenas administradores globais têm acesso a este recurso."
        )
