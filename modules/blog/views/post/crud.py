from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404

from core.mixins import CompanyFilterMixin, CompanyAdminRequiredMixin
from ...domain.post import BlogPost
from ...forms import BlogPostForm


class PostCreateView(LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post/form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.company = self.request.company
        messages.success(self.request, 'Post criado com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Post'
        return context


class PostUpdateView(LoginRequiredMixin, CompanyAdminRequiredMixin, CompanyFilterMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post/form.html'
    context_object_name = 'post'
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        messages.success(self.request, 'Post atualizado com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar: {self.object.title}'
        return context


class PostDeleteView(LoginRequiredMixin, CompanyAdminRequiredMixin, CompanyFilterMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post/confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post excluído com sucesso!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Excluir: {self.object.title}'
        return context
