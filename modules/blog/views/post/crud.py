from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from core.mixins import CompanyAdminRequiredMixin, SuccessMessageMixin
from ...domain.post import BlogPost
from ...forms import BlogPostForm


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post/form.html'
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Post criado com sucesso!'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.company = self.request.user.company
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Post'
        return context


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post/form.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = 'Post atualizado com sucesso!'
    
    def get_queryset(self):
        return BlogPost.objects.filter(company=self.request.user.company)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar: {self.object.title}'
        return context


class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post/confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    delete_success_message = 'Post excluído com sucesso!'
    
    def get_queryset(self):
        return BlogPost.objects.filter(company=self.request.user.company)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Excluir: {self.object.title}'
        return context
