from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from ..domain.user import CustomUser
from ..forms.user_form import UserForm, UserCreateForm
from ..services.user_service import UserService
from core.mixins import CompanyAdminRequiredMixin, CompanyFilterMixin, CompanyObjectMixin, GlobalAdminFilterMixin

class UserListView(LoginRequiredMixin, CompanyAdminRequiredMixin, GlobalAdminFilterMixin, CompanyFilterMixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Superadmin e grupo "Administrador" veem todos os usuários
        is_global_admin = (self.request.user.is_superuser or 
                          (hasattr(self.request.user, 'groups') and 
                           self.request.user.groups.filter(name='Administrador').exists()))
        
        if is_global_admin:
            return queryset  # Veem todos os usuários
        
        # Admins de empresa só veem usuários da própria empresa
        if hasattr(self.request.user, 'company') and self.request.user.company:
            return queryset.filter(company=self.request.user.company)
        
        # Usuários sem empresa não veem ninguém
        return queryset.none()

class UserDetailView(LoginRequiredMixin, CompanyObjectMixin, GlobalAdminFilterMixin, CompanyFilterMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'

class UserCreateView(LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = form.save(commit=False)
        
        # Se não é admin global e não definiu empresa, usar empresa do usuário atual
        is_global_admin = (
            self.request.user.is_superuser or 
            self.request.user.groups.filter(name='Administrador').exists()
        )
        
        if not is_global_admin and not user.company:
            if hasattr(self.request.user, 'company') and self.request.user.company:
                user.company = self.request.user.company
        
        user.save()
        
        # Adicionar usuário ao grupo apropriado se necessário
        from django.contrib.auth.models import Group
        
        if user.company and user.is_company_admin:
            admin_group, created = Group.objects.get_or_create(name='Admin Empresa')
            user.groups.add(admin_group)
        
        # Usuários sem empresa ficam como "usuários globais" sem grupos específicos
        # Apenas superadmins explícitos ficam no grupo "Administrador"
        
        messages.success(self.request, f'Usuário {user.username} criado com sucesso!')
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, CompanyObjectMixin, GlobalAdminFilterMixin, CompanyFilterMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = form.save(commit=False)
        old_company = CustomUser.objects.get(pk=user.pk).company if user.pk else None
        
        # Verificar se pode alterar empresa
        is_global_admin = (
            self.request.user.is_superuser or 
            self.request.user.groups.filter(name='Administrador').exists()
        )
        
        if not is_global_admin and old_company != user.company:
            messages.error(self.request, 'Você não tem permissão para alterar a empresa do usuário.')
            return self.form_invalid(form)
        
        user.save()
        
        # Atualizar grupos do usuário baseado na empresa e status
        from django.contrib.auth.models import Group
        
        # Verificar se quem está editando é admin global
        is_editor_global_admin = (self.request.user.is_superuser or 
                                 (hasattr(self.request.user, 'groups') and 
                                  self.request.user.groups.filter(name='Administrador').exists()))
        
        # Apenas admins globais podem alterar grupos relacionados a empresa
        if is_editor_global_admin:
            # Remover grupos antigos relacionados a empresa
            user.groups.filter(name__in=['Admin Empresa']).delete()
            
            # Adicionar grupos apropriados
            if user.company and user.is_company_admin:
                admin_group, created = Group.objects.get_or_create(name='Admin Empresa')
                user.groups.add(admin_group)
            
            # Gerenciar grupo "Administrador" apenas para superusers
            if user.is_superuser:
                admin_group, created = Group.objects.get_or_create(name='Administrador')
                if admin_group not in user.groups.all():
                    user.groups.add(admin_group)
            else:
                # Remover do grupo Administrador se não for mais superuser
                user.groups.filter(name='Administrador').delete()
        
        messages.success(self.request, f'Usuário {user.username} atualizado com sucesso!')
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, CompanyObjectMixin, GlobalAdminFilterMixin, CompanyFilterMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Verificar se o usuário pode deletar
        if user == request.user:
            messages.error(request, 'Você não pode deletar a si mesmo!')
            return redirect('accounts:user_list')
        
        # Verificar permissões de deleção
        is_global_admin = (request.user.is_superuser or 
                          (hasattr(request.user, 'groups') and 
                           request.user.groups.filter(name='Administrador').exists()))
        
        if not is_global_admin:
            # Admins de empresa só podem deletar usuários da própria empresa
            if hasattr(request.user, 'company') and request.user.company:
                if user.company != request.user.company:
                    messages.error(request, 'Você só pode deletar usuários da sua empresa!')
                    return redirect('accounts:user_list')
            else:
                messages.error(request, 'Você não tem permissão para deletar usuários!')
                return redirect('accounts:user_list')
        
        messages.success(request, f'Usuário {user.username} deletado com sucesso!')
        return super().delete(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user_obj'
    
    def get_object(self, queryset=None):
        return self.request.user