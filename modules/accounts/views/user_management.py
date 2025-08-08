from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..domain.user import CustomUser
from ..forms.user_form import UserForm, UserCreateForm
from ..services.user_service import UserService
from ...mixins import CompanyAdminRequiredMixin, CompanyFilterMixin, CompanyOwnerMixin

class UserListView(LoginRequiredMixin, CompanyAdminRequiredMixin, CompanyFilterMixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

class UserDetailView(LoginRequiredMixin, CompanyOwnerMixin, CompanyFilterMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'

class UserCreateView(LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        form.instance.company = self.request.company
        messages.success(self.request, 'Usuário criado com sucesso!')
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, CompanyOwnerMixin, CompanyFilterMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, CompanyAdminRequiredMixin, CompanyFilterMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def test_func(self):
        # Admin não pode deletar a si mesmo
        return super().test_func() and self.get_object() != self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuário removido com sucesso!')
        return super().delete(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'
    
    def get_object(self, queryset=None):
        return self.request.user